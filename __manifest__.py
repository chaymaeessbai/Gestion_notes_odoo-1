{
    'name': "gestion_notes",
    'version': '0.1',
    'author': "chahd Leila Sanae Chaymae",
    'category': 'Gestion des Notes',
    'description': "Description de mon module",
    'depends': ['base'],
    'data': [
        'security/gestion_notes_security.xml',
        'security/ir.model.access.csv',
        'views/gestion_notes_menu.xml',
        'views/gestion_notes_views.xml',
    ],
    'demo' : [],
    'application': True,
    'installable': True,
}
