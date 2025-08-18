# -*- coding: utf--8 -*-
import logging  # <-- Loglama kütüphanesini import et
from odoo import models, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)  # <-- Logger'ı tanımla


class ReportActionCustom(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):

        # LOG 1: Metodun çalışıp çalışmadığını kontrol et
        _logger.info(f"Rapor oluşturma metodu tetiklendi. Çalıştırılan rapor: {self.report_name}")

        if self.report_name == 'ozenel_reports.report_sale_order_template2':

            # LOG 2: Doğru raporun içine girip girmediğini kontrol et
            _logger.info("Doğru rapor (Teklif Açık) yakalandı, fiyat kontrolü başlıyor...")

            orders = self.env['sale.order'].browse(res_ids)

            for order in orders:
                if any(line.price_unit == 0.0 for line in order.order_line):
                    # LOG 3: Sıfır fiyatlı ürün bulup bulmadığını kontrol et
                    _logger.warning(f"{order.name} içinde sıfır fiyatlı ürün bulundu! Hata verilecek.")

                    raise UserError(
                        f"'{order.name}' numaralı teklifte birim fiyatı sıfır (0.00) olan ürünler bulunmaktadır.\n\n"
                        "Lütfen tüm ürün fiyatlarını kontrol edip tekrar yazdırmayı deneyin."
                    )

            _logger.info(f"Kontrol tamamlandı, '{self.report_name}' raporunda sıfır fiyatlı ürün bulunamadı.")

        return super(ReportActionCustom, self)._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)