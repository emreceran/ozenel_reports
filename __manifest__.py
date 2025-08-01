{
    'name': 'Ozenel Reports',
    'version': '1.0',
    'summary': 'Kapalı Teklif raporu: sadece toplam tutarı gösterir',
    'author': 'Emre',
    'depends': ['sale', 'web', 'sale_management'],
    'data': [
        'report/paperformat.xml',
        'report/sale_report_templates.xml',
        'views/sale_order_line_views.xml',
        'report/sale_report.xml',
        'report/kapali.xml',
        'report/report_kapali.xml',


    ],

    'assets': {
        'web.report_assets_common': [
            'ozenel_reports/static/src/css/report_styles.css',
        ],
    },

    'installable': True,
    'application': False,
}
