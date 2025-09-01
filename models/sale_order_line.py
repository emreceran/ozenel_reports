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

    urun_aciklama = fields.Text(string="Ürün Açıklaması", compute="_compute_urun_aciklama", store=True)

    @api.depends('name')
    def _compute_urun_aciklama(self):
        for line in self:
            lines = line.name.split('\n')
            if len(lines) > 1:
                line.urun_aciklama = '\n'.join(lines[1:])
            else:
                line.urun_aciklama = line.name


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # İlgili kişiyi seçmek için yeni bir Many2one alanı ekliyoruz.
    ilgili_kisi = fields.Char(
        string="İlgili Kişi",
        help="Müşteriye bağlı kontak kişisini seçin."
    )

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

    def action_preview_sale_report(self):
        """
        Bu metod, "Önizleme" butonuna tıklandığında çalışır.
        Belirtilen raporun URL'ini oluşturur ve yeni bir sekmede açar.
        """
        # Metodun tek bir kayıt üzerinde çalıştığından emin olalım.
        self.ensure_one()

        # Raportun XML tanımındaki 'report_name' alanını buraya yazın.
        report_name = 'ozenel_reports.report_sale_order_template2'

        # Rapor URL'ini dinamik olarak oluştur.
        # Format: /report/pdf/<report_name>/<kayıt_id>
        report_url = f"/report/html/{report_name}/{self.id}"

        # Odoo'nun web arayüzüne bu URL'i yeni bir sekmede açmasını söyleyen
        # bir 'ir.actions.act_url' aksiyonu döndür.
        return {
            'type': 'ir.actions.act_url',
            'url': report_url,
            'target': 'current',  # <-- Bu satır mevcut pencerede açar
        }

    quotation_subject = fields.Html(
        string='Teklif Konusu',
        default="""
                <span>Firmamızdan talep ettiğiniz ürünlere ait ayrıntılı fiyat teklifimiz ekte yer almaktadır.<br>
                Her türlü tamamlayıcı bilgi ihtiyacı ve sorularınız için bize ulaşabilirsiniz.</span>
            """
    )

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    # Teklif konusu için HTML tipinde bir alan ekliyoruz.
    # HTML tipi, metin içinde formatlama (kalın, liste vb.) yapmanıza olanak tanır.
    quotation_subject = fields.Html(string='Teklif Konusu')
