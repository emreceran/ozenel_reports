from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'purchase.order.line'

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

    name_tail = fields.Text(string="Name Tail", compute="_compute_name_tail")

    @api.depends('name')
    def _compute_name_tail(self):
        for line in self:
            lines = line.name.split('\n')
            if len(lines) > 1:
                line.name_tail = '\n'.join(lines[1:])
            else:
                line.name_tail = line.name