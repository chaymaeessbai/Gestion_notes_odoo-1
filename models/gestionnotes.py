from odoo import models, fields, api

class Etudiant(models.Model):
    _name = 'gestion.etudiant'
    _description = 'Étudiant'

    name = fields.Char(string='Nom', required=True)
    num_apogee = fields.Char(string='Numéro Apogée', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Téléphone')
    date_naissance = fields.Date(string='Date de Naissance')
    adresse = fields.Text(string='Adresse')
    filiere_id = fields.Many2one('gestion.filiere', string="Filière")
    notes_ids = fields.One2many('gestion.note', 'etudiant_id', string='Notes')
    presences_ids = fields.One2many('gestion.presence', 'etudiant_id', string='Présences')
    





class Enseignant(models.Model):
    _name = 'gestion.enseignant'
    _description = 'Enseignant'

    name = fields.Char(string='Nom', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Téléphone')
    specialite = fields.Char(string='Spécialité')
    module_ids = fields.One2many('gestion.module', 'enseignant_id', string='Modules enseignés')

class Module(models.Model):
    _name = 'gestion.module'
    _description = 'Module (Matière)'

    name = fields.Char(string='Nom du Module', required=True)
    code = fields.Char(string='Code', required=True, unique=True)
    description = fields.Text(string='Description')
    enseignant_id = fields.Many2one('gestion.enseignant', string='Enseignant Responsable')
    filiere_id = fields.Many2one('gestion.filiere', string='Filière')
    note_ids = fields.One2many('gestion.note', 'module_id', string='Notes')
    presence_ids = fields.One2many('gestion.presence', 'module_id', string='Présences')
    etudiant_id = fields.Many2one('gestion.etudiant', string="Étudiants")
    num_apogee = fields.Char(related='etudiant_id.num_apogee', string="Numéro Apogée", store=True)

    semestre = fields.Selection([
        ('S1', 'Semestre 1'),
        ('S2', 'Semestre 2'),
        ('S3', 'Semestre 3'),
        ('S4', 'Semestre 4'),
        ('S5', 'Semestre 5'),
        ('S6', 'Semestre 6'),
    ], string='Semestre', required=True)

class Filiere(models.Model):
    _name = 'gestion.filiere'
    _description = 'Filière'

    name = fields.Char(string='Nom de la Filière', required=True)
    description = fields.Text(string='Description')
    niveau = fields.Selection([('1A', 'Première Année'), ('2A', 'Deuxième Année'), ('3A', 'Troisième Année')], string='Niveau')
    etudiant_ids = fields.One2many('gestion.etudiant', 'filiere_id', string='Étudiants')
    module_ids = fields.One2many('gestion.module', 'filiere_id', string='Modules')

class Presence(models.Model):
    _name = 'gestion.presence'
    _description = 'Présence aux examens'

    etudiant_id = fields.Many2one('gestion.etudiant', string='Étudiant', required=True)
    module_id = fields.Many2one('gestion.module', string='Module', required=True)
    date_examen = fields.Date(string='Date de l^Examen', required=True)
    statut = fields.Selection([('present', 'Présent'), ('absent', 'Absent')], string='Statut', required=True)

class Note(models.Model):
    _name = 'gestion.note'
    _description = 'Note de l\'Étudiant'

    etudiant_id = fields.Many2one('gestion.etudiant', string='Étudiant', required=True)
    module_id = fields.Many2one('gestion.module', string='Module', required=True)
    date_examen = fields.Date(string='Date de l\'Examen')
    num_apogee = fields.Char(related='etudiant_id.num_apogee', string="Numéro Apogée", store=True)

    note = fields.Float(string="Note", required=True)
    session = fields.Selection([
        ('normale', 'Session Normale'),
        ('rattrapage', 'Session Rattrapage')
    ], string='Session')


    etat = fields.Selection([
        ('V', 'Validé'),
        ('RATT', 'Rattrapage'),
        ('NV', 'Non Validé'),
        ('ABS', 'Absent')
    ], string='État', compute='_compute_etat', store=True)


    moyenne_generale = fields.Float(
        string="Moyenne Générale", compute="_compute_moyenne_generale", store=True
    )
    presence_id = fields.Many2one('gestion.presence', string='Présence')

    @api.depends('note', 'presence_id', 'presence_id.statut', 'session')
    def _compute_etat(self):
        """
        Détermine l'état de validation en fonction de la note et la session.
        """
        for record in self:
            if record.presence_id and record.presence_id.statut == 'absent':
                record.etat = 'ABS'
            elif record.session == 'normale':
                if record.note >= 12:
                    record.etat = 'V'
                else:
                    record.etat = 'RATT'
            elif record.session == 'rattrapage':
                if record.note >= 12:
                    record.etat = 'V'
                else:
                    record.etat = 'NV'



    @api.depends('etudiant_id', 'note')
    def _compute_moyenne_generale(self):
        for record in self:
            
            notes_etudiant = self.filtered(lambda n: n.etudiant_id == record.etudiant_id).mapped('note')
            
            record.moyenne_generale = sum(notes_etudiant) / len(notes_etudiant) if notes_etudiant else 0.0



class SemestreResultat(models.Model):
    _name = 'gestion.semestre.resultat'
    _description = 'Résultat du Semestre'

    etudiant_id = fields.Many2one('gestion.etudiant', string='Étudiant', required=True)
    filiere_id = fields.Many2one('gestion.filiere', string='Filière', required=True)
    semestre = fields.Selection([
        ('S1', 'Semestre 1'),
        ('S2', 'Semestre 2'),
        ('S3', 'Semestre 3'),
        ('S4', 'Semestre 4'),
        ('S5', 'Semestre 5'),
        ('S6', 'Semestre 6'),
    ], string='Semestre', required=True)