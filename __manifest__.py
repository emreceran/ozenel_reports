{
    'name': 'Ozenel Reports',
    'version': '1.0',
    'summary': 'Kapalı Teklif raporu: sadece toplam tutarı gösterir',
    'author': 'Emre',
    'depends': ['sale'],
    'data': [
        'report/sale_report.xml',
        'report/sale_report_templates.xml',
        'views/sale_order_line_views.xml',
    ],
    'installable': True,
    'application': False,
}
