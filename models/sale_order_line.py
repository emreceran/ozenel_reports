from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_brand_name = fields.Char(string='Marka')

    # Kullanıcının manuel sayfa sonu istemesi için yeni bir alan ekliyoruz.
    x_force_page_break = fields.Boolean(
        string="Yeni Sayfada Başlat",
        help="Bu seçenek işaretlenirse, rapor yazdırılırken bu satırdan sonra yeni bir sayfa başlar."
    )

    @api.onchange('product_id')
    def _onchange_product_id_brand(self):
        for line in self:
            brand_value = line.product_id.product_template_attribute_value_ids.filtered(
                lambda attr: attr.attribute_id.name.lower() == 'marka'
            )
            line.x_brand_name = brand_value.name if brand_value else ''
