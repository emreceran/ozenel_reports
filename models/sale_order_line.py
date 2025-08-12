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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # _get_lines_for_report_grouped fonksiyonu isteğiniz üzerine kaldırıldı.

    def _get_section_subtotals(self):
        """
        Kapak sayfasındaki 'İcmal' tablosu için her bölümün ara toplamını hesaplar.
        """
        self.ensure_one()
        section_totals = []
        current_section = None
        current_subtotal = 0.0

        lines_to_report = self._get_order_lines_to_report()

        for line in lines_to_report:
            if line.display_type == 'line_section':
                if current_section:
                    section_totals.append({
                        'name': current_section.name,
                        'subtotal': current_subtotal,
                    })
                current_section = line
                current_subtotal = 0.0
            elif not line.display_type and current_section:
                current_subtotal += line.price_subtotal

        if current_section:
            section_totals.append({
                'name': current_section.name,
                'subtotal': current_subtotal,
            })

        return section_totals