"""
seed_blinkit_500.py
--------------------
Adds ~440 more products to reach 500+ total in kirana.db.
All prices sourced from Blinkit / Indian market rates (Sept 2024-26).
Prices in PAISE (Rs.1 = 100 paise).
Safe to re-run - uses INSERT OR IGNORE on unique SKU.
"""

from datetime import datetime
from database import init_db, get_db

NOW = datetime.now().isoformat(timespec="seconds")

def p(rupees: float) -> int:
    return int(round(rupees * 100))


PRODUCTS = [

    # ════════════════════════════════════════════════════════════════
    # ATTA / FLOUR  (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Aashirvaad Atta 1kg","brand":"Aashirvaad","sku":"ATT-AASH-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(50),"sell_price":p(58),"mrp":p(60),"quantity":30,"reorder_level":8,"hsn_code":"1101","gst_rate":5},
    {"name":"Aashirvaad Atta 10kg","brand":"Aashirvaad","sku":"ATT-AASH-10KG","unit":"kg","pack_size":"10kg","loose":0,"cost_price":p(440),"sell_price":p(490),"mrp":p(510),"quantity":10,"reorder_level":3,"hsn_code":"1101","gst_rate":5},
    {"name":"Pillsbury Atta 1kg","brand":"Pillsbury","sku":"ATT-PILL-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(48),"sell_price":p(55),"mrp":p(58),"quantity":25,"reorder_level":6,"hsn_code":"1101","gst_rate":5},
    {"name":"Pillsbury Atta 10kg","brand":"Pillsbury","sku":"ATT-PILL-10KG","unit":"kg","pack_size":"10kg","loose":0,"cost_price":p(420),"sell_price":p(468),"mrp":p(490),"quantity":8,"reorder_level":3,"hsn_code":"1101","gst_rate":5},
    {"name":"Nature Fresh Sampoorna Chakki Atta 5kg","brand":"Nature Fresh","sku":"ATT-NF-5KG","unit":"kg","pack_size":"5kg","loose":0,"cost_price":p(210),"sell_price":p(235),"mrp":p(250),"quantity":12,"reorder_level":4,"hsn_code":"1101","gst_rate":5},
    {"name":"Shaktibhog Atta 10kg","brand":"Shaktibhog","sku":"ATT-SHAK-10KG","unit":"kg","pack_size":"10kg","loose":0,"cost_price":p(390),"sell_price":p(435),"mrp":p(460),"quantity":8,"reorder_level":3,"hsn_code":"1101","gst_rate":5},
    {"name":"Loose Wheat Flour (Maida)","brand":"Local","sku":"MAIDA-LOOSE","unit":"kg","pack_size":"loose","loose":1,"cost_price":p(32),"sell_price":p(38),"mrp":p(38),"quantity":30,"reorder_level":8,"hsn_code":"1101","gst_rate":5},
    {"name":"Loose Besan 500g","brand":"Local","sku":"BESAN-LOOSE-500G","unit":"kg","pack_size":"500g","loose":1,"cost_price":p(50),"sell_price":p(58),"mrp":p(58),"quantity":20,"reorder_level":5,"hsn_code":"1106","gst_rate":5},
    {"name":"Tata Sampann Besan 500g","brand":"Tata Sampann","sku":"BESAN-TATA-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(70),"quantity":15,"reorder_level":4,"hsn_code":"1106","gst_rate":5},
    {"name":"MTR Rava (Sooji) 500g","brand":"MTR","sku":"RAVA-MTR-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(40),"sell_price":p(48),"mrp":p(52),"quantity":15,"reorder_level":4,"hsn_code":"1103","gst_rate":5},

    # ════════════════════════════════════════════════════════════════
    # RICE (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"India Gate Basmati Rice 1kg","brand":"India Gate","sku":"RICE-IG-BASM-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(88),"sell_price":p(99),"mrp":p(105),"quantity":20,"reorder_level":6,"hsn_code":"1006","gst_rate":0},
    {"name":"India Gate Basmati Rice 2kg","brand":"India Gate","sku":"RICE-IG-BASM-2KG","unit":"kg","pack_size":"2kg","loose":0,"cost_price":p(172),"sell_price":p(192),"mrp":p(205),"quantity":15,"reorder_level":4,"hsn_code":"1006","gst_rate":0},
    {"name":"Daawat Rozana Basmati 5kg","brand":"Daawat","sku":"RICE-DAAWAT-5KG","unit":"kg","pack_size":"5kg","loose":0,"cost_price":p(382),"sell_price":p(425),"mrp":p(445),"quantity":12,"reorder_level":4,"hsn_code":"1006","gst_rate":0},
    {"name":"Kohinoor Basmati Rice 1kg","brand":"Kohinoor","sku":"RICE-KOH-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(82),"sell_price":p(95),"mrp":p(100),"quantity":20,"reorder_level":5,"hsn_code":"1006","gst_rate":0},
    {"name":"Kohinoor Super Silver Rice 5kg","brand":"Kohinoor","sku":"RICE-KOH-5KG","unit":"kg","pack_size":"5kg","loose":0,"cost_price":p(395),"sell_price":p(445),"mrp":p(465),"quantity":10,"reorder_level":3,"hsn_code":"1006","gst_rate":0},
    {"name":"Fortune Rozana Basmati 1kg","brand":"Fortune","sku":"RICE-FORT-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(80),"sell_price":p(92),"mrp":p(98),"quantity":20,"reorder_level":5,"hsn_code":"1006","gst_rate":0},
    {"name":"Sona Masoori Raw Rice 1kg","brand":"Local","sku":"RICE-SONA-1KG","unit":"kg","pack_size":"1kg","loose":1,"cost_price":p(48),"sell_price":p(58),"mrp":p(58),"quantity":25,"reorder_level":8,"hsn_code":"1006","gst_rate":0},
    {"name":"Ponni Boiled Rice 1kg","brand":"Local","sku":"RICE-PONNI-1KG","unit":"kg","pack_size":"1kg","loose":1,"cost_price":p(52),"sell_price":p(62),"mrp":p(62),"quantity":20,"reorder_level":6,"hsn_code":"1006","gst_rate":0},

    # ════════════════════════════════════════════════════════════════
    # SALT (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Tata Salt 2kg","brand":"Tata","sku":"SALT-TATA-2KG","unit":"kg","pack_size":"2kg","loose":0,"cost_price":p(44),"sell_price":p(50),"mrp":p(55),"quantity":25,"reorder_level":6,"hsn_code":"2501","gst_rate":0},
    {"name":"Tata Rock Salt 1kg","brand":"Tata","sku":"SALT-TATA-ROCK-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":15,"reorder_level":4,"hsn_code":"2501","gst_rate":0},
    {"name":"Catch Sea Salt 500g","brand":"Catch","sku":"SALT-CATCH-SEA-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(38),"quantity":12,"reorder_level":3,"hsn_code":"2501","gst_rate":0},
    {"name":"Sundrop Lite Salt 300g","brand":"Sundrop","sku":"SALT-LITE-300G","unit":"packet","pack_size":"300g","loose":0,"cost_price":p(62),"sell_price":p(75),"mrp":p(80),"quantity":10,"reorder_level":3,"hsn_code":"2501","gst_rate":0},

    # ════════════════════════════════════════════════════════════════
    # SUGAR (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Uttam Sugar 5kg","brand":"Uttam","sku":"SUGAR-UTT-5KG","unit":"kg","pack_size":"5kg","loose":0,"cost_price":p(200),"sell_price":p(230),"mrp":p(245),"quantity":15,"reorder_level":4,"hsn_code":"1701","gst_rate":0},
    {"name":"Dhampure Brown Sugar 500g","brand":"Dhampure","sku":"SUGAR-BRN-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(65),"sell_price":p(78),"mrp":p(85),"quantity":10,"reorder_level":3,"hsn_code":"1701","gst_rate":0},
    {"name":"Organic India Cane Sugar 500g","brand":"Organic India","sku":"SUGAR-ORG-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(112),"quantity":8,"reorder_level":2,"hsn_code":"1701","gst_rate":0},

    # ════════════════════════════════════════════════════════════════
    # DAL / PULSES (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Tata Sampann Moong Dal 1kg","brand":"Tata Sampann","sku":"DAL-TATA-MOONG-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(112),"sell_price":p(130),"mrp":p(140),"quantity":15,"reorder_level":4,"hsn_code":"0713","gst_rate":0},
    {"name":"Tata Sampann Chana Dal 1kg","brand":"Tata Sampann","sku":"DAL-TATA-CHANA-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(82),"sell_price":p(95),"mrp":p(102),"quantity":15,"reorder_level":4,"hsn_code":"0713","gst_rate":0},
    {"name":"Tata Sampann Masoor Dal 1kg","brand":"Tata Sampann","sku":"DAL-TATA-MASOOR-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(90),"sell_price":p(105),"mrp":p(112),"quantity":15,"reorder_level":4,"hsn_code":"0713","gst_rate":0},
    {"name":"Tata Sampann Urad Dal 1kg","brand":"Tata Sampann","sku":"DAL-TATA-URAD-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(120),"sell_price":p(140),"mrp":p(150),"quantity":12,"reorder_level":3,"hsn_code":"0713","gst_rate":0},
    {"name":"Urad Dal (loose)","brand":"Local","sku":"DAL-URAD-LOOSE","unit":"kg","pack_size":"loose","loose":1,"cost_price":p(115),"sell_price":p(130),"mrp":p(130),"quantity":15,"reorder_level":4,"hsn_code":"0713","gst_rate":0},
    {"name":"Rajma (loose) 1kg","brand":"Local","sku":"RAJMA-LOOSE","unit":"kg","pack_size":"loose","loose":1,"cost_price":p(110),"sell_price":p(128),"mrp":p(128),"quantity":15,"reorder_level":4,"hsn_code":"0713","gst_rate":0},
    {"name":"Kabuli Chana (Chole) 1kg","brand":"Local","sku":"CHOLE-LOOSE","unit":"kg","pack_size":"loose","loose":1,"cost_price":p(88),"sell_price":p(102),"mrp":p(102),"quantity":15,"reorder_level":4,"hsn_code":"0713","gst_rate":0},
    {"name":"Lobia (Black Eyed Peas) 1kg","brand":"Local","sku":"LOBIA-LOOSE","unit":"kg","pack_size":"loose","loose":1,"cost_price":p(78),"sell_price":p(90),"mrp":p(90),"quantity":12,"reorder_level":3,"hsn_code":"0713","gst_rate":0},
    {"name":"Tata Sampann Rajma 1kg","brand":"Tata Sampann","sku":"RAJMA-TATA-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(118),"sell_price":p(138),"mrp":p(148),"quantity":10,"reorder_level":3,"hsn_code":"0713","gst_rate":0},

    # ════════════════════════════════════════════════════════════════
    # OILS (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Fortune Sunflower Oil 2L","brand":"Fortune","sku":"OIL-FORT-2L","unit":"litre","pack_size":"2L","loose":0,"cost_price":p(298),"sell_price":p(335),"mrp":p(350),"quantity":15,"reorder_level":4,"hsn_code":"1512","gst_rate":5},
    {"name":"Saffola Gold Oil 5L","brand":"Saffola","sku":"OIL-SAFF-5L","unit":"litre","pack_size":"5L","loose":0,"cost_price":p(782),"sell_price":p(875),"mrp":p(920),"quantity":8,"reorder_level":2,"hsn_code":"1512","gst_rate":5},
    {"name":"Gemini Sunflower Oil 1L","brand":"Gemini","sku":"OIL-GEM-1L","unit":"litre","pack_size":"1L","loose":0,"cost_price":p(138),"sell_price":p(158),"mrp":p(168),"quantity":15,"reorder_level":4,"hsn_code":"1512","gst_rate":5},
    {"name":"Patanjali Mustard Oil 1L","brand":"Patanjali","sku":"OIL-PAT-MUST-1L","unit":"litre","pack_size":"1L","loose":0,"cost_price":p(138),"sell_price":p(158),"mrp":p(170),"quantity":12,"reorder_level":3,"hsn_code":"1514","gst_rate":5},
    {"name":"Engine Brand Coconut Oil 500ml","brand":"Engine","sku":"OIL-COC-500ML","unit":"bottle","pack_size":"500ml","loose":0,"cost_price":p(148),"sell_price":p(172),"mrp":p(185),"quantity":10,"reorder_level":3,"hsn_code":"1513","gst_rate":5},
    {"name":"Parachute Coconut Oil 500ml","brand":"Parachute","sku":"OIL-PAR-COC-500ML","unit":"bottle","pack_size":"500ml","loose":0,"cost_price":p(158),"sell_price":p(182),"mrp":p(195),"quantity":12,"reorder_level":3,"hsn_code":"1513","gst_rate":5},
    {"name":"Parachute Coconut Oil 200ml","brand":"Parachute","sku":"OIL-PAR-COC-200ML","unit":"bottle","pack_size":"200ml","loose":0,"cost_price":p(68),"sell_price":p(78),"mrp":p(85),"quantity":15,"reorder_level":4,"hsn_code":"1513","gst_rate":5},
    {"name":"Figaro Olive Oil 500ml","brand":"Figaro","sku":"OIL-FIG-OLIVE-500ML","unit":"bottle","pack_size":"500ml","loose":0,"cost_price":p(380),"sell_price":p(438),"mrp":p(465),"quantity":8,"reorder_level":2,"hsn_code":"1509","gst_rate":5},
    {"name":"Borges Olive Oil 500ml","brand":"Borges","sku":"OIL-BOR-OLIVE-500ML","unit":"bottle","pack_size":"500ml","loose":0,"cost_price":p(458),"sell_price":p(525),"mrp":p(555),"quantity":6,"reorder_level":2,"hsn_code":"1509","gst_rate":5},
    {"name":"Ghee Pure (loose) 500g","brand":"Local","sku":"GHEE-LOOSE-500G","unit":"kg","pack_size":"500g","loose":1,"cost_price":p(280),"sell_price":p(325),"mrp":p(325),"quantity":10,"reorder_level":3,"hsn_code":"0405","gst_rate":12},
    {"name":"Amul Pure Ghee 500ml","brand":"Amul","sku":"GHEE-AMUL-500ML","unit":"tin","pack_size":"500ml","loose":0,"cost_price":p(285),"sell_price":p(325),"mrp":p(340),"quantity":10,"reorder_level":3,"hsn_code":"0405","gst_rate":12},
    {"name":"Amul Pure Ghee 1L","brand":"Amul","sku":"GHEE-AMUL-1L","unit":"tin","pack_size":"1L","loose":0,"cost_price":p(558),"sell_price":p(638),"mrp":p(670),"quantity":8,"reorder_level":2,"hsn_code":"0405","gst_rate":12},
    {"name":"Patanjali Cow Ghee 1L","brand":"Patanjali","sku":"GHEE-PAT-1L","unit":"tin","pack_size":"1L","loose":0,"cost_price":p(495),"sell_price":p(568),"mrp":p(599),"quantity":6,"reorder_level":2,"hsn_code":"0405","gst_rate":12},

    # ════════════════════════════════════════════════════════════════
    # DAIRY (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Amul Taaza Milk 200ml","brand":"Amul","sku":"MILK-AMUL-200ML","unit":"packet","pack_size":"200ml","loose":0,"cost_price":p(12),"sell_price":p(14),"mrp":p(15),"quantity":30,"reorder_level":10,"hsn_code":"0401","gst_rate":0},
    {"name":"Amul Slim & Trim Milk 500ml","brand":"Amul","sku":"MILK-AMUL-SLIM-500ML","unit":"packet","pack_size":"500ml","loose":0,"cost_price":p(24),"sell_price":p(28),"mrp":p(30),"quantity":20,"reorder_level":6,"hsn_code":"0401","gst_rate":0},
    {"name":"Mother Dairy Milk 500ml","brand":"Mother Dairy","sku":"MILK-MD-500ML","unit":"packet","pack_size":"500ml","loose":0,"cost_price":p(25),"sell_price":p(29),"mrp":p(30),"quantity":25,"reorder_level":8,"hsn_code":"0401","gst_rate":0},
    {"name":"Mother Dairy Milk 1L","brand":"Mother Dairy","sku":"MILK-MD-1L","unit":"packet","pack_size":"1L","loose":0,"cost_price":p(50),"sell_price":p(58),"mrp":p(60),"quantity":20,"reorder_level":6,"hsn_code":"0401","gst_rate":0},
    {"name":"Amul Dahi 200g","brand":"Amul","sku":"DAHI-AMUL-200G","unit":"packet","pack_size":"200g","loose":0,"cost_price":p(22),"sell_price":p(26),"mrp":p(28),"quantity":20,"reorder_level":6,"hsn_code":"0403","gst_rate":5},
    {"name":"Mother Dairy Dahi 400g","brand":"Mother Dairy","sku":"DAHI-MD-400G","unit":"packet","pack_size":"400g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(48),"quantity":15,"reorder_level":4,"hsn_code":"0403","gst_rate":5},
    {"name":"Amul Cream 200ml","brand":"Amul","sku":"CREAM-AMUL-200ML","unit":"packet","pack_size":"200ml","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(70),"quantity":10,"reorder_level":3,"hsn_code":"0401","gst_rate":5},
    {"name":"Amul Mozzarella Cheese 200g","brand":"Amul","sku":"CHEESE-MOZ-200G","unit":"packet","pack_size":"200g","loose":0,"cost_price":p(112),"sell_price":p(130),"mrp":p(140),"quantity":8,"reorder_level":2,"hsn_code":"0406","gst_rate":12},
    {"name":"Britannia Cheese Slices 200g","brand":"Britannia","sku":"CHEESE-BRIT-200G","unit":"packet","pack_size":"200g","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(112),"quantity":8,"reorder_level":2,"hsn_code":"0406","gst_rate":12},
    {"name":"Amul Paneer 200g","brand":"Amul","sku":"PANEER-AMUL-200G","unit":"packet","pack_size":"200g","loose":0,"cost_price":p(72),"sell_price":p(85),"mrp":p(90),"quantity":12,"reorder_level":3,"hsn_code":"0406","gst_rate":5},
    {"name":"Amul Paneer 500g","brand":"Amul","sku":"PANEER-AMUL-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(178),"sell_price":p(205),"mrp":p(218),"quantity":8,"reorder_level":2,"hsn_code":"0406","gst_rate":5},
    {"name":"Amul Lassi Mango 200ml","brand":"Amul","sku":"LASSI-AMUL-MANGO-200ML","unit":"packet","pack_size":"200ml","loose":0,"cost_price":p(18),"sell_price":p(22),"mrp":p(25),"quantity":20,"reorder_level":6,"hsn_code":"0403","gst_rate":12},
    {"name":"Amul Kool Milk 200ml","brand":"Amul","sku":"KOOL-AMUL-200ML","unit":"packet","pack_size":"200ml","loose":0,"cost_price":p(18),"sell_price":p(22),"mrp":p(25),"quantity":20,"reorder_level":6,"hsn_code":"0401","gst_rate":12},
    {"name":"Amul Pro 500g","brand":"Amul","sku":"AMULPRO-500G","unit":"jar","pack_size":"500g","loose":0,"cost_price":p(285),"sell_price":p(325),"mrp":p(345),"quantity":6,"reorder_level":2,"hsn_code":"1901","gst_rate":18},
    {"name":"Nestle A+ Milk 1L","brand":"Nestle","sku":"MILK-NEST-1L","unit":"packet","pack_size":"1L","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(68),"quantity":15,"reorder_level":4,"hsn_code":"0401","gst_rate":0},

    # ════════════════════════════════════════════════════════════════
    # EGGS
    # ════════════════════════════════════════════════════════════════
    {"name":"White Eggs 6 pack","brand":"Local","sku":"EGG-6PK","unit":"piece","pack_size":"6 eggs","loose":0,"cost_price":p(50),"sell_price":p(58),"mrp":p(60),"quantity":20,"reorder_level":6,"hsn_code":"0407","gst_rate":0},
    {"name":"White Eggs 12 pack","brand":"Local","sku":"EGG-12PK","unit":"piece","pack_size":"12 eggs","loose":0,"cost_price":p(96),"sell_price":p(110),"mrp":p(115),"quantity":15,"reorder_level":4,"hsn_code":"0407","gst_rate":0},
    {"name":"Brown Eggs 6 pack","brand":"Local","sku":"EGG-BRN-6PK","unit":"piece","pack_size":"6 eggs","loose":0,"cost_price":p(58),"sell_price":p(68),"mrp":p(72),"quantity":12,"reorder_level":3,"hsn_code":"0407","gst_rate":0},

    # ════════════════════════════════════════════════════════════════
    # NOODLES / PASTA / INSTANT (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Maggi 12-Pack (840g)","brand":"Nestle","sku":"MAGGI-12PK-840G","unit":"packet","pack_size":"840g","loose":0,"cost_price":p(138),"sell_price":p(160),"mrp":p(168),"quantity":20,"reorder_level":6,"hsn_code":"1902","gst_rate":12},
    {"name":"Sunfeast Yippee Mood Masala 70g","brand":"Sunfeast","sku":"YIPPEE-MOOD-70G","unit":"packet","pack_size":"70g","loose":0,"cost_price":p(12),"sell_price":p(15),"mrp":p(15),"quantity":40,"reorder_level":10,"hsn_code":"1902","gst_rate":12},
    {"name":"Knorr Soupy Noodles 70g","brand":"Knorr","sku":"KNORR-NOOD-70G","unit":"packet","pack_size":"70g","loose":0,"cost_price":p(22),"sell_price":p(28),"mrp":p(30),"quantity":20,"reorder_level":6,"hsn_code":"1902","gst_rate":12},
    {"name":"Top Ramen Smoodles 70g","brand":"Top Ramen","sku":"TOPRAM-70G","unit":"packet","pack_size":"70g","loose":0,"cost_price":p(12),"sell_price":p(15),"mrp":p(15),"quantity":30,"reorder_level":8,"hsn_code":"1902","gst_rate":12},
    {"name":"Patanjali Atta Noodles 70g","brand":"Patanjali","sku":"PAT-NOOD-70G","unit":"packet","pack_size":"70g","loose":0,"cost_price":p(10),"sell_price":p(12),"mrp":p(15),"quantity":30,"reorder_level":8,"hsn_code":"1902","gst_rate":12},
    {"name":"Bambino Vermicelli 900g","brand":"Bambino","sku":"BAMB-VERM-900G","unit":"packet","pack_size":"900g","loose":0,"cost_price":p(75),"sell_price":p(88),"mrp":p(95),"quantity":15,"reorder_level":4,"hsn_code":"1902","gst_rate":12},
    {"name":"Borges Penne Pasta 500g","brand":"Borges","sku":"PASTA-BOR-PENNE-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(72),"sell_price":p(85),"mrp":p(92),"quantity":10,"reorder_level":3,"hsn_code":"1902","gst_rate":12},
    {"name":"Maggi Masala Packet","brand":"Nestle","sku":"MAGGI-MASALA-PKT","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(20),"sell_price":p(25),"mrp":p(28),"quantity":30,"reorder_level":8,"hsn_code":"0910","gst_rate":5},

    # ════════════════════════════════════════════════════════════════
    # BISCUITS / SNACKS (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Parle-G 800g","brand":"Parle","sku":"PARLE-G-800G","unit":"packet","pack_size":"800g","loose":0,"cost_price":p(78),"sell_price":p(88),"mrp":p(90),"quantity":25,"reorder_level":6,"hsn_code":"1905","gst_rate":12},
    {"name":"Britannia NutriChoice 5 Grain 100g","brand":"Britannia","sku":"BIS-BNC-5G-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":15,"reorder_level":4,"hsn_code":"1905","gst_rate":12},
    {"name":"Sunfeast Dark Fantasy 150g","brand":"Sunfeast","sku":"BIS-DF-150G","unit":"packet","pack_size":"150g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":15,"reorder_level":4,"hsn_code":"1905","gst_rate":12},
    {"name":"Oreo Original 120g","brand":"Cadbury","sku":"BIS-OREO-120G","unit":"packet","pack_size":"120g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":20,"reorder_level":5,"hsn_code":"1905","gst_rate":12},
    {"name":"Oreo Chocolate 120g","brand":"Cadbury","sku":"BIS-OREO-CHOC-120G","unit":"packet","pack_size":"120g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":20,"reorder_level":5,"hsn_code":"1905","gst_rate":12},
    {"name":"Britannia Marie Gold 250g","brand":"Britannia","sku":"BIS-MARIE-250G","unit":"packet","pack_size":"250g","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(38),"quantity":20,"reorder_level":6,"hsn_code":"1905","gst_rate":12},
    {"name":"McVities Digestive 400g","brand":"McVities","sku":"BIS-MCVIT-400G","unit":"packet","pack_size":"400g","loose":0,"cost_price":p(108),"sell_price":p(125),"mrp":p(135),"quantity":12,"reorder_level":3,"hsn_code":"1905","gst_rate":12},
    {"name":"Hide & Seek Fab 112g","brand":"Parle","sku":"BIS-HNS-112G","unit":"packet","pack_size":"112g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":15,"reorder_level":4,"hsn_code":"1905","gst_rate":12},
    {"name":"Lay's Masala 26g","brand":"Lay's","sku":"CHIPS-LAYS-MASA-26G","unit":"packet","pack_size":"26g","loose":0,"cost_price":p(18),"sell_price":p(20),"mrp":p(20),"quantity":50,"reorder_level":12,"hsn_code":"1905","gst_rate":12},
    {"name":"Lay's American Style Cream & Onion 26g","brand":"Lay's","sku":"CHIPS-LAYS-CO-26G","unit":"packet","pack_size":"26g","loose":0,"cost_price":p(18),"sell_price":p(20),"mrp":p(20),"quantity":50,"reorder_level":12,"hsn_code":"1905","gst_rate":12},
    {"name":"Bingo Mad Angles 60g","brand":"Bingo","sku":"BINGO-MA-60G","unit":"packet","pack_size":"60g","loose":0,"cost_price":p(18),"sell_price":p(20),"mrp":p(20),"quantity":40,"reorder_level":10,"hsn_code":"1905","gst_rate":12},
    {"name":"Uncle Chips 60g","brand":"Uncle Chips","sku":"UNCLE-60G","unit":"packet","pack_size":"60g","loose":0,"cost_price":p(18),"sell_price":p(20),"mrp":p(20),"quantity":40,"reorder_level":10,"hsn_code":"1905","gst_rate":12},
    {"name":"Haldiram's Aloo Bhujia 400g","brand":"Haldiram's","sku":"BHUJIA-HALD-400G","unit":"packet","pack_size":"400g","loose":0,"cost_price":p(135),"sell_price":p(158),"mrp":p(170),"quantity":15,"reorder_level":4,"hsn_code":"1905","gst_rate":12},
    {"name":"Haldiram's Mixture 400g","brand":"Haldiram's","sku":"MIX-HALD-400G","unit":"packet","pack_size":"400g","loose":0,"cost_price":p(130),"sell_price":p(152),"mrp":p(165),"quantity":12,"reorder_level":3,"hsn_code":"1905","gst_rate":12},
    {"name":"Haldiram's Peanuts 200g","brand":"Haldiram's","sku":"PNUT-HALD-200G","unit":"packet","pack_size":"200g","loose":0,"cost_price":p(42),"sell_price":p(50),"mrp":p(55),"quantity":15,"reorder_level":4,"hsn_code":"2008","gst_rate":12},
    {"name":"Too Yumm Multigrain Chips 60g","brand":"Too Yumm","sku":"TY-MULTI-60G","unit":"packet","pack_size":"60g","loose":0,"cost_price":p(18),"sell_price":p(22),"mrp":p(25),"quantity":30,"reorder_level":8,"hsn_code":"1905","gst_rate":12},
    {"name":"Cornitos Nacho Crisps 60g","brand":"Cornitos","sku":"CORN-NACHO-60G","unit":"packet","pack_size":"60g","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(45),"quantity":15,"reorder_level":4,"hsn_code":"1905","gst_rate":12},
    {"name":"Popcorn (Microwave) Act II 99g","brand":"Act II","sku":"POP-ACT-99G","unit":"packet","pack_size":"99g","loose":0,"cost_price":p(40),"sell_price":p(48),"mrp":p(52),"quantity":20,"reorder_level":5,"hsn_code":"2008","gst_rate":12},
    {"name":"Kellogg's Cornflakes 875g","brand":"Kellogg's","sku":"CORN-KELL-875G","unit":"packet","pack_size":"875g","loose":0,"cost_price":p(285),"sell_price":p(330),"mrp":p(350),"quantity":8,"reorder_level":2,"hsn_code":"1904","gst_rate":12},
    {"name":"Kellogg's Muesli Fruit & Nut 500g","brand":"Kellogg's","sku":"MUES-KELL-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(222),"sell_price":p(258),"mrp":p(275),"quantity":8,"reorder_level":2,"hsn_code":"1904","gst_rate":12},
    {"name":"Quaker Oats 500g","brand":"Quaker","sku":"OATS-QUAK-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(92),"sell_price":p(108),"mrp":p(115),"quantity":12,"reorder_level":3,"hsn_code":"1102","gst_rate":5},
    {"name":"Saffola Oats 500g","brand":"Saffola","sku":"OATS-SAFF-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(98),"sell_price":p(115),"mrp":p(125),"quantity":12,"reorder_level":3,"hsn_code":"1102","gst_rate":5},

    # ════════════════════════════════════════════════════════════════
    # CHOCOLATES & CONFECTIONERY (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Cadbury Dairy Milk 13g","brand":"Cadbury","sku":"CHOC-CDM-13G","unit":"piece","pack_size":"13g","loose":0,"cost_price":p(10),"sell_price":p(12),"mrp":p(15),"quantity":60,"reorder_level":15,"hsn_code":"1806","gst_rate":18},
    {"name":"Cadbury Dairy Milk Silk 60g","brand":"Cadbury","sku":"CHOC-SILK-60G","unit":"piece","pack_size":"60g","loose":0,"cost_price":p(85),"sell_price":p(99),"mrp":p(105),"quantity":20,"reorder_level":5,"hsn_code":"1806","gst_rate":18},
    {"name":"5 Star 22g","brand":"Cadbury","sku":"CHOC-5STAR-22G","unit":"piece","pack_size":"22g","loose":0,"cost_price":p(10),"sell_price":p(12),"mrp":p(15),"quantity":50,"reorder_level":12,"hsn_code":"1806","gst_rate":18},
    {"name":"Perk 22g","brand":"Cadbury","sku":"CHOC-PERK-22G","unit":"piece","pack_size":"22g","loose":0,"cost_price":p(10),"sell_price":p(12),"mrp":p(15),"quantity":50,"reorder_level":12,"hsn_code":"1806","gst_rate":18},
    {"name":"Munch 22g","brand":"Nestle","sku":"CHOC-MUNCH-22G","unit":"piece","pack_size":"22g","loose":0,"cost_price":p(8),"sell_price":p(10),"mrp":p(10),"quantity":50,"reorder_level":12,"hsn_code":"1806","gst_rate":18},
    {"name":"Milkybar 22g","brand":"Nestle","sku":"CHOC-MILKY-22G","unit":"piece","pack_size":"22g","loose":0,"cost_price":p(18),"sell_price":p(22),"mrp":p(25),"quantity":30,"reorder_level":8,"hsn_code":"1806","gst_rate":18},
    {"name":"Eclairs (loose) 100g","brand":"Cadbury","sku":"ECLAIR-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(40),"quantity":30,"reorder_level":8,"hsn_code":"1704","gst_rate":18},
    {"name":"Polo Mint 25g","brand":"Nestle","sku":"POLO-25G","unit":"piece","pack_size":"25g","loose":0,"cost_price":p(10),"sell_price":p(12),"mrp":p(15),"quantity":40,"reorder_level":10,"hsn_code":"1704","gst_rate":18},
    {"name":"Mentos Fruit 40g","brand":"Mentos","sku":"MENTOS-40G","unit":"piece","pack_size":"40g","loose":0,"cost_price":p(10),"sell_price":p(12),"mrp":p(15),"quantity":40,"reorder_level":10,"hsn_code":"1704","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # BEVERAGES - TEA / COFFEE (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Tata Tea Gold 250g","brand":"Tata Tea","sku":"TEA-TATA-GOLD-250G","unit":"packet","pack_size":"250g","loose":0,"cost_price":p(120),"sell_price":p(138),"mrp":p(148),"quantity":15,"reorder_level":4,"hsn_code":"0902","gst_rate":5},
    {"name":"Tata Tea Premium 500g","brand":"Tata Tea","sku":"TEA-TATA-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(178),"sell_price":p(205),"mrp":p(220),"quantity":12,"reorder_level":3,"hsn_code":"0902","gst_rate":5},
    {"name":"Wagh Bakri Premium Leaf Tea 500g","brand":"Wagh Bakri","sku":"TEA-WB-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(198),"sell_price":p(228),"mrp":p(245),"quantity":10,"reorder_level":3,"hsn_code":"0902","gst_rate":5},
    {"name":"Society Masala Tea 250g","brand":"Society","sku":"TEA-SOC-MASA-250G","unit":"packet","pack_size":"250g","loose":0,"cost_price":p(108),"sell_price":p(125),"mrp":p(135),"quantity":10,"reorder_level":3,"hsn_code":"0902","gst_rate":5},
    {"name":"Lipton Green Tea 25 bags","brand":"Lipton","sku":"TEA-LIP-GREEN-25","unit":"packet","pack_size":"25 bags","loose":0,"cost_price":p(78),"sell_price":p(92),"mrp":p(100),"quantity":10,"reorder_level":3,"hsn_code":"0902","gst_rate":5},
    {"name":"Taj Mahal Tea 500g","brand":"Brooke Bond","sku":"TEA-TAJ-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(228),"sell_price":p(265),"mrp":p(280),"quantity":8,"reorder_level":2,"hsn_code":"0902","gst_rate":5},
    {"name":"Nescafe Classic 200g","brand":"Nestle","sku":"COFF-NESC-200G","unit":"jar","pack_size":"200g","loose":0,"cost_price":p(728),"sell_price":p(845),"mrp":p(895),"quantity":5,"reorder_level":2,"hsn_code":"2101","gst_rate":12},
    {"name":"Bru Gold Coffee 50g","brand":"Bru","sku":"COFF-BRU-50G","unit":"jar","pack_size":"50g","loose":0,"cost_price":p(162),"sell_price":p(188),"mrp":p(200),"quantity":10,"reorder_level":3,"hsn_code":"2101","gst_rate":12},
    {"name":"Bru Instant Coffee 500g","brand":"Bru","sku":"COFF-BRU-500G","unit":"jar","pack_size":"500g","loose":0,"cost_price":p(718),"sell_price":p(838),"mrp":p(890),"quantity":4,"reorder_level":1,"hsn_code":"2101","gst_rate":12},

    # ════════════════════════════════════════════════════════════════
    # BEVERAGES - SOFT DRINKS / JUICES (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Coca-Cola 2L","brand":"Coca-Cola","sku":"BEV-COKE-2L","unit":"bottle","pack_size":"2L","loose":0,"cost_price":p(75),"sell_price":p(88),"mrp":p(95),"quantity":15,"reorder_level":4,"hsn_code":"2202","gst_rate":12},
    {"name":"Pepsi 600ml","brand":"PepsiCo","sku":"BEV-PEPSI-600ML","unit":"bottle","pack_size":"600ml","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(45),"quantity":20,"reorder_level":6,"hsn_code":"2202","gst_rate":12},
    {"name":"7UP 600ml","brand":"PepsiCo","sku":"BEV-7UP-600ML","unit":"bottle","pack_size":"600ml","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(45),"quantity":20,"reorder_level":6,"hsn_code":"2202","gst_rate":12},
    {"name":"Sprite 600ml","brand":"Coca-Cola","sku":"BEV-SPRITE-600ML","unit":"bottle","pack_size":"600ml","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(45),"quantity":20,"reorder_level":6,"hsn_code":"2202","gst_rate":12},
    {"name":"Thums Up 600ml","brand":"Coca-Cola","sku":"BEV-TU-600ML","unit":"bottle","pack_size":"600ml","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(45),"quantity":20,"reorder_level":6,"hsn_code":"2202","gst_rate":12},
    {"name":"Fanta Orange 600ml","brand":"Coca-Cola","sku":"BEV-FANTA-600ML","unit":"bottle","pack_size":"600ml","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(45),"quantity":15,"reorder_level":4,"hsn_code":"2202","gst_rate":12},
    {"name":"Maaza Mango 600ml","brand":"Coca-Cola","sku":"BEV-MAAZA-600ML","unit":"bottle","pack_size":"600ml","loose":0,"cost_price":p(35),"sell_price":p(40),"mrp":p(42),"quantity":20,"reorder_level":6,"hsn_code":"2202","gst_rate":12},
    {"name":"Slice Mango 600ml","brand":"PepsiCo","sku":"BEV-SLICE-600ML","unit":"bottle","pack_size":"600ml","loose":0,"cost_price":p(35),"sell_price":p(40),"mrp":p(42),"quantity":15,"reorder_level":4,"hsn_code":"2202","gst_rate":12},
    {"name":"Red Bull Energy 250ml","brand":"Red Bull","sku":"BEV-RB-250ML","unit":"can","pack_size":"250ml","loose":0,"cost_price":p(102),"sell_price":p(120),"mrp":p(130),"quantity":15,"reorder_level":4,"hsn_code":"2202","gst_rate":12},
    {"name":"Monster Energy 500ml","brand":"Monster","sku":"BEV-MONS-500ML","unit":"can","pack_size":"500ml","loose":0,"cost_price":p(108),"sell_price":p(125),"mrp":p(135),"quantity":12,"reorder_level":3,"hsn_code":"2202","gst_rate":12},
    {"name":"Real Fruit Juice Mixed 1L","brand":"Dabur","sku":"JUICE-REAL-MIX-1L","unit":"carton","pack_size":"1L","loose":0,"cost_price":p(90),"sell_price":p(105),"mrp":p(115),"quantity":12,"reorder_level":3,"hsn_code":"2009","gst_rate":12},
    {"name":"Tropicana Orange 1L","brand":"PepsiCo","sku":"JUICE-TROP-OJ-1L","unit":"carton","pack_size":"1L","loose":0,"cost_price":p(95),"sell_price":p(110),"mrp":p(120),"quantity":10,"reorder_level":3,"hsn_code":"2009","gst_rate":12},
    {"name":"Paper Boat Aam Panna 250ml","brand":"Paper Boat","sku":"BEV-PB-AAM-250ML","unit":"packet","pack_size":"250ml","loose":0,"cost_price":p(22),"sell_price":p(28),"mrp":p(30),"quantity":20,"reorder_level":5,"hsn_code":"2202","gst_rate":12},
    {"name":"Kinley Water 1L","brand":"Coca-Cola","sku":"WATER-KINLEY-1L","unit":"bottle","pack_size":"1L","loose":0,"cost_price":p(12),"sell_price":p(15),"mrp":p(20),"quantity":24,"reorder_level":6,"hsn_code":"2201","gst_rate":18},
    {"name":"Bisleri Water 1L","brand":"Bisleri","sku":"WATER-BIS-1L","unit":"bottle","pack_size":"1L","loose":0,"cost_price":p(12),"sell_price":p(15),"mrp":p(20),"quantity":24,"reorder_level":6,"hsn_code":"2201","gst_rate":18},
    {"name":"Bisleri Water 2L","brand":"Bisleri","sku":"WATER-BIS-2L","unit":"bottle","pack_size":"2L","loose":0,"cost_price":p(18),"sell_price":p(22),"mrp":p(28),"quantity":12,"reorder_level":4,"hsn_code":"2201","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # HEALTH DRINKS
    # ════════════════════════════════════════════════════════════════
    {"name":"Horlicks 500g","brand":"GSK","sku":"HDRNK-HOR-500G","unit":"jar","pack_size":"500g","loose":0,"cost_price":p(255),"sell_price":p(298),"mrp":p(315),"quantity":8,"reorder_level":2,"hsn_code":"1901","gst_rate":18},
    {"name":"Complan Chocolate 500g","brand":"Kraft Heinz","sku":"HDRNK-COMP-CHOC-500G","unit":"jar","pack_size":"500g","loose":0,"cost_price":p(262),"sell_price":p(305),"mrp":p(325),"quantity":6,"reorder_level":2,"hsn_code":"1901","gst_rate":18},
    {"name":"Protinex Original 400g","brand":"Danone","sku":"HDRNK-PROT-400G","unit":"jar","pack_size":"400g","loose":0,"cost_price":p(440),"sell_price":p(515),"mrp":p(548),"quantity":5,"reorder_level":1,"hsn_code":"2106","gst_rate":18},
    {"name":"Ensure Vanilla 400g","brand":"Abbott","sku":"HDRNK-ENS-400G","unit":"jar","pack_size":"400g","loose":0,"cost_price":p(680),"sell_price":p(785),"mrp":p(835),"quantity":4,"reorder_level":1,"hsn_code":"2106","gst_rate":18},
    {"name":"Glucon-D Orange 1kg","brand":"Heinz","sku":"GLUCD-1KG","unit":"jar","pack_size":"1kg","loose":0,"cost_price":p(108),"sell_price":p(125),"mrp":p(135),"quantity":8,"reorder_level":2,"hsn_code":"1701","gst_rate":12},

    # ════════════════════════════════════════════════════════════════
    # SPICES (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"MDH Rajma Masala 100g","brand":"MDH","sku":"SPICE-MDH-RAJM-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(72),"quantity":10,"reorder_level":3,"hsn_code":"0910","gst_rate":5},
    {"name":"MDH Chicken Masala 100g","brand":"MDH","sku":"SPICE-MDH-CHKN-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(72),"quantity":10,"reorder_level":3,"hsn_code":"0910","gst_rate":5},
    {"name":"Everest Sambhar Masala 100g","brand":"Everest","sku":"SPICE-EVR-SAM-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(58),"sell_price":p(68),"mrp":p(75),"quantity":10,"reorder_level":3,"hsn_code":"0910","gst_rate":5},
    {"name":"Everest Pav Bhaji Masala 100g","brand":"Everest","sku":"SPICE-EVR-PB-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(58),"sell_price":p(68),"mrp":p(75),"quantity":10,"reorder_level":3,"hsn_code":"0910","gst_rate":5},
    {"name":"Badshah Chaat Masala 100g","brand":"Badshah","sku":"SPICE-BAD-CHAAT-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":12,"reorder_level":3,"hsn_code":"0910","gst_rate":5},
    {"name":"Loose Coriander Powder 100g","brand":"Local","sku":"SPICE-CORI-LOOSE","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(15),"sell_price":p(20),"mrp":p(20),"quantity":30,"reorder_level":8,"hsn_code":"0909","gst_rate":5},
    {"name":"Loose Cumin (Jeera) 100g","brand":"Local","sku":"SPICE-JEERA-LOOSE","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(18),"sell_price":p(22),"mrp":p(22),"quantity":25,"reorder_level":6,"hsn_code":"0909","gst_rate":5},
    {"name":"Loose Black Pepper 50g","brand":"Local","sku":"SPICE-PEPP-LOOSE","unit":"packet","pack_size":"50g","loose":0,"cost_price":p(30),"sell_price":p(38),"mrp":p(38),"quantity":20,"reorder_level":5,"hsn_code":"0904","gst_rate":5},
    {"name":"Whole Cardamom 50g","brand":"Local","sku":"SPICE-CARD-50G","unit":"packet","pack_size":"50g","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(65),"quantity":15,"reorder_level":4,"hsn_code":"0908","gst_rate":5},
    {"name":"Bay Leaves (Tej Patta) 25g","brand":"Local","sku":"SPICE-BAY-25G","unit":"packet","pack_size":"25g","loose":0,"cost_price":p(12),"sell_price":p(15),"mrp":p(15),"quantity":20,"reorder_level":5,"hsn_code":"0910","gst_rate":5},
    {"name":"Cloves (Laung) 50g","brand":"Local","sku":"SPICE-CLOVE-50G","unit":"packet","pack_size":"50g","loose":0,"cost_price":p(48),"sell_price":p(58),"mrp":p(58),"quantity":15,"reorder_level":4,"hsn_code":"0907","gst_rate":5},
    {"name":"Catch Garam Masala 100g","brand":"Catch","sku":"SPICE-CATCH-GM-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(48),"sell_price":p(58),"mrp":p(65),"quantity":12,"reorder_level":3,"hsn_code":"0910","gst_rate":5},
    {"name":"Patanjali Haldi 200g","brand":"Patanjali","sku":"SPICE-PAT-HALDI-200G","unit":"packet","pack_size":"200g","loose":0,"cost_price":p(42),"sell_price":p(50),"mrp":p(55),"quantity":12,"reorder_level":3,"hsn_code":"0910","gst_rate":5},
    {"name":"Saffron Strands 1g","brand":"Everest","sku":"SPICE-SAFF-1G","unit":"packet","pack_size":"1g","loose":0,"cost_price":p(55),"sell_price":p(68),"mrp":p(75),"quantity":10,"reorder_level":3,"hsn_code":"0904","gst_rate":5},

    # ════════════════════════════════════════════════════════════════
    # CONDIMENTS / SAUCES / PICKLES
    # ════════════════════════════════════════════════════════════════
    {"name":"Kissan Tomato Ketchup 1kg","brand":"Kissan","sku":"SAUCE-KIS-KETCH-1KG","unit":"bottle","pack_size":"1kg","loose":0,"cost_price":p(95),"sell_price":p(112),"mrp":p(120),"quantity":10,"reorder_level":3,"hsn_code":"2103","gst_rate":12},
    {"name":"Kissan Mixed Fruit Jam 500g","brand":"Kissan","sku":"JAM-KIS-MF-500G","unit":"jar","pack_size":"500g","loose":0,"cost_price":p(92),"sell_price":p(108),"mrp":p(115),"quantity":8,"reorder_level":2,"hsn_code":"2007","gst_rate":12},
    {"name":"Maggi Hot & Sweet Sauce 1kg","brand":"Nestle","sku":"SAUCE-MAGGI-HS-1KG","unit":"bottle","pack_size":"1kg","loose":0,"cost_price":p(105),"sell_price":p(122),"mrp":p(132),"quantity":8,"reorder_level":2,"hsn_code":"2103","gst_rate":12},
    {"name":"Tops Chilli Sauce 400g","brand":"Tops","sku":"SAUCE-TOPS-CHILLI-400G","unit":"bottle","pack_size":"400g","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(72),"quantity":8,"reorder_level":2,"hsn_code":"2103","gst_rate":12},
    {"name":"Priya Mango Pickle 300g","brand":"Priya","sku":"PICKLE-PRIYA-MANGO-300G","unit":"jar","pack_size":"300g","loose":0,"cost_price":p(60),"sell_price":p(72),"mrp":p(78),"quantity":10,"reorder_level":3,"hsn_code":"2001","gst_rate":12},
    {"name":"Mother's Recipe Mango Pickle 500g","brand":"Mother's Recipe","sku":"PICKLE-MR-MANGO-500G","unit":"jar","pack_size":"500g","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(115),"quantity":8,"reorder_level":2,"hsn_code":"2001","gst_rate":12},
    {"name":"Patanjali Amla Murabba 500g","brand":"Patanjali","sku":"MURABBA-PAT-500G","unit":"jar","pack_size":"500g","loose":0,"cost_price":p(72),"sell_price":p(85),"mrp":p(92),"quantity":8,"reorder_level":2,"hsn_code":"2007","gst_rate":12},
    {"name":"Heinz Tomato Ketchup 450g","brand":"Heinz","sku":"SAUCE-HEINZ-450G","unit":"bottle","pack_size":"450g","loose":0,"cost_price":p(95),"sell_price":p(115),"mrp":p(125),"quantity":8,"reorder_level":2,"hsn_code":"2103","gst_rate":12},
    {"name":"Veeba Mayonnaise 900g","brand":"Veeba","sku":"MAYO-VEEBA-900G","unit":"jar","pack_size":"900g","loose":0,"cost_price":p(192),"sell_price":p(225),"mrp":p(240),"quantity":6,"reorder_level":2,"hsn_code":"2103","gst_rate":12},
    {"name":"Ching's Dark Soya Sauce 750ml","brand":"Ching's","sku":"SAUCE-CHING-SOY-750ML","unit":"bottle","pack_size":"750ml","loose":0,"cost_price":p(62),"sell_price":p(75),"mrp":p(82),"quantity":8,"reorder_level":2,"hsn_code":"2103","gst_rate":12},

    # ════════════════════════════════════════════════════════════════
    # DETERGENT / CLEANING (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Surf Excel Easy Wash 500g","brand":"Surf Excel","sku":"SURF-EXCEL-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(108),"sell_price":p(125),"mrp":p(135),"quantity":15,"reorder_level":4,"hsn_code":"3402","gst_rate":18},
    {"name":"Rin Advanced 1kg","brand":"Rin","sku":"DET-RIN-1KG","unit":"packet","pack_size":"1kg","loose":0,"cost_price":p(88),"sell_price":p(102),"mrp":p(110),"quantity":15,"reorder_level":4,"hsn_code":"3402","gst_rate":18},
    {"name":"Wheel Powder Detergent 1kg","brand":"Wheel","sku":"DET-WHEEL-1KG","unit":"packet","pack_size":"1kg","loose":0,"cost_price":p(48),"sell_price":p(58),"mrp":p(65),"quantity":20,"reorder_level":5,"hsn_code":"3402","gst_rate":18},
    {"name":"Tide Ultra 1kg","brand":"Tide","sku":"DET-TIDE-1KG","unit":"packet","pack_size":"1kg","loose":0,"cost_price":p(195),"sell_price":p(228),"mrp":p(245),"quantity":10,"reorder_level":3,"hsn_code":"3402","gst_rate":18},
    {"name":"Comfort Fabric Conditioner 860ml","brand":"Comfort","sku":"FABRIC-COMF-860ML","unit":"bottle","pack_size":"860ml","loose":0,"cost_price":p(175),"sell_price":p(205),"mrp":p(220),"quantity":8,"reorder_level":2,"hsn_code":"3402","gst_rate":18},
    {"name":"Vim Bar 155g","brand":"Vim","sku":"VIM-BAR-155G","unit":"piece","pack_size":"155g","loose":0,"cost_price":p(18),"sell_price":p(22),"mrp":p(25),"quantity":30,"reorder_level":8,"hsn_code":"3402","gst_rate":18},
    {"name":"Vim Dishwash Liquid 250ml","brand":"Vim","sku":"VIM-LIQ-250ML","unit":"bottle","pack_size":"250ml","loose":0,"cost_price":p(48),"sell_price":p(58),"mrp":p(65),"quantity":15,"reorder_level":4,"hsn_code":"3402","gst_rate":18},
    {"name":"Pril Dishwash Liquid 500ml","brand":"Pril","sku":"PRIL-LIQ-500ML","unit":"bottle","pack_size":"500ml","loose":0,"cost_price":p(75),"sell_price":p(90),"mrp":p(98),"quantity":10,"reorder_level":3,"hsn_code":"3402","gst_rate":18},
    {"name":"Harpic Power Plus 1L","brand":"Harpic","sku":"HARP-1L","unit":"bottle","pack_size":"1L","loose":0,"cost_price":p(185),"sell_price":p(215),"mrp":p(230),"quantity":8,"reorder_level":2,"hsn_code":"3402","gst_rate":18},
    {"name":"Colin Glass Cleaner 500ml","brand":"Colin","sku":"COLIN-500ML","unit":"bottle","pack_size":"500ml","loose":0,"cost_price":p(112),"sell_price":p(132),"mrp":p(142),"quantity":8,"reorder_level":2,"hsn_code":"3402","gst_rate":18},
    {"name":"Domex Floor Cleaner 1L","brand":"Domex","sku":"DOMEX-1L","unit":"bottle","pack_size":"1L","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(115),"quantity":8,"reorder_level":2,"hsn_code":"3402","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # PERSONAL CARE (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Lifebuoy Total 10 Soap 125g","brand":"HUL","sku":"SOAP-LB-125G","unit":"piece","pack_size":"125g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(52),"quantity":24,"reorder_level":6,"hsn_code":"3401","gst_rate":18},
    {"name":"Dove Moisturising Soap 75g","brand":"HUL","sku":"SOAP-DOVE-75G","unit":"piece","pack_size":"75g","loose":0,"cost_price":p(42),"sell_price":p(50),"mrp":p(55),"quantity":20,"reorder_level":5,"hsn_code":"3401","gst_rate":18},
    {"name":"Pears Soap 75g","brand":"HUL","sku":"SOAP-PEARS-75G","unit":"piece","pack_size":"75g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":20,"reorder_level":5,"hsn_code":"3401","gst_rate":18},
    {"name":"Santoor Sandal Soap 75g","brand":"Wipro","sku":"SOAP-SANT-75G","unit":"piece","pack_size":"75g","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(38),"quantity":20,"reorder_level":5,"hsn_code":"3401","gst_rate":18},
    {"name":"Medimix Ayurvedic Soap 125g","brand":"Medimix","sku":"SOAP-MEDI-125G","unit":"piece","pack_size":"125g","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(48),"quantity":20,"reorder_level":5,"hsn_code":"3401","gst_rate":18},
    {"name":"Colgate MaxFresh 150g","brand":"Colgate","sku":"TP-COLG-MF-150G","unit":"tube","pack_size":"150g","loose":0,"cost_price":p(65),"sell_price":p(78),"mrp":p(85),"quantity":15,"reorder_level":4,"hsn_code":"3306","gst_rate":18},
    {"name":"Sensodyne Regular 100g","brand":"GSK","sku":"TP-SENS-100G","unit":"tube","pack_size":"100g","loose":0,"cost_price":p(142),"sell_price":p(168),"mrp":p(180),"quantity":8,"reorder_level":2,"hsn_code":"3306","gst_rate":18},
    {"name":"Pepsodent Germicheck 200g","brand":"HUL","sku":"TP-PEPS-200G","unit":"tube","pack_size":"200g","loose":0,"cost_price":p(62),"sell_price":p(75),"mrp":p(82),"quantity":12,"reorder_level":3,"hsn_code":"3306","gst_rate":18},
    {"name":"Oral-B Cavity Protection 150g","brand":"P&G","sku":"TP-ORALB-150G","unit":"tube","pack_size":"150g","loose":0,"cost_price":p(75),"sell_price":p(90),"mrp":p(98),"quantity":10,"reorder_level":3,"hsn_code":"3306","gst_rate":18},
    {"name":"Sunsilk Hairfall Solution 180ml","brand":"HUL","sku":"SHP-SUNSIL-180ML","unit":"bottle","pack_size":"180ml","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(115),"quantity":10,"reorder_level":3,"hsn_code":"3305","gst_rate":18},
    {"name":"Dove Shampoo Daily Shine 180ml","brand":"HUL","sku":"SHP-DOVE-180ML","unit":"bottle","pack_size":"180ml","loose":0,"cost_price":p(122),"sell_price":p(145),"mrp":p(158),"quantity":10,"reorder_level":3,"hsn_code":"3305","gst_rate":18},
    {"name":"TRESemme Keratin Smooth Shampoo 190ml","brand":"HUL","sku":"SHP-TRES-190ML","unit":"bottle","pack_size":"190ml","loose":0,"cost_price":p(158),"sell_price":p(185),"mrp":p(199),"quantity":8,"reorder_level":2,"hsn_code":"3305","gst_rate":18},
    {"name":"Pantene Anti-Hairfall Shampoo 180ml","brand":"P&G","sku":"SHP-PANT-180ML","unit":"bottle","pack_size":"180ml","loose":0,"cost_price":p(148),"sell_price":p(175),"mrp":p(190),"quantity":8,"reorder_level":2,"hsn_code":"3305","gst_rate":18},
    {"name":"Parachute Advansed Hair Oil 300ml","brand":"Marico","sku":"HOIL-PAR-300ML","unit":"bottle","pack_size":"300ml","loose":0,"cost_price":p(118),"sell_price":p(138),"mrp":p(150),"quantity":10,"reorder_level":3,"hsn_code":"3305","gst_rate":18},
    {"name":"Bajaj Almond Drops Hair Oil 200ml","brand":"Bajaj","sku":"HOIL-BAJ-200ML","unit":"bottle","pack_size":"200ml","loose":0,"cost_price":p(102),"sell_price":p(122),"mrp":p(132),"quantity":10,"reorder_level":3,"hsn_code":"3305","gst_rate":18},
    {"name":"Nihar Shanti Amla Hair Oil 200ml","brand":"Marico","sku":"HOIL-NIH-200ML","unit":"bottle","pack_size":"200ml","loose":0,"cost_price":p(75),"sell_price":p(90),"mrp":p(98),"quantity":12,"reorder_level":3,"hsn_code":"3305","gst_rate":18},
    {"name":"Vaseline Petroleum Jelly 100ml","brand":"HUL","sku":"VASEL-100ML","unit":"jar","pack_size":"100ml","loose":0,"cost_price":p(75),"sell_price":p(90),"mrp":p(98),"quantity":12,"reorder_level":3,"hsn_code":"2712","gst_rate":18},
    {"name":"Nivea Moisturising Lotion 200ml","brand":"Nivea","sku":"LOTION-NIV-200ML","unit":"bottle","pack_size":"200ml","loose":0,"cost_price":p(132),"sell_price":p(158),"mrp":p(170),"quantity":8,"reorder_level":2,"hsn_code":"3304","gst_rate":18},
    {"name":"Fair & Lovely (Glow & Lovely) 50g","brand":"HUL","sku":"CREAM-FL-50G","unit":"tube","pack_size":"50g","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(72),"quantity":12,"reorder_level":3,"hsn_code":"3304","gst_rate":18},
    {"name":"Gillette Mach 3 Razor","brand":"Gillette","sku":"RAZOR-GIL-M3","unit":"piece","pack_size":"1 piece","loose":0,"cost_price":p(142),"sell_price":p(168),"mrp":p(180),"quantity":10,"reorder_level":3,"hsn_code":"8212","gst_rate":18},
    {"name":"Gillette Mach 3 Blade 2-pack","brand":"Gillette","sku":"BLADE-GIL-M3-2PK","unit":"packet","pack_size":"2 blades","loose":0,"cost_price":p(182),"sell_price":p(215),"mrp":p(230),"quantity":8,"reorder_level":2,"hsn_code":"8212","gst_rate":18},
    {"name":"Axe Deo Spray 150ml","brand":"HUL","sku":"DEO-AXE-150ML","unit":"can","pack_size":"150ml","loose":0,"cost_price":p(132),"sell_price":p(158),"mrp":p(172),"quantity":10,"reorder_level":3,"hsn_code":"3307","gst_rate":18},
    {"name":"Fogg Deo Fresh 150ml","brand":"Fogg","sku":"DEO-FOGG-150ML","unit":"can","pack_size":"150ml","loose":0,"cost_price":p(148),"sell_price":p(175),"mrp":p(190),"quantity":10,"reorder_level":3,"hsn_code":"3307","gst_rate":18},
    {"name":"Wild Stone Deo Spray 150ml","brand":"Wild Stone","sku":"DEO-WS-150ML","unit":"can","pack_size":"150ml","loose":0,"cost_price":p(102),"sell_price":p(122),"mrp":p(132),"quantity":10,"reorder_level":3,"hsn_code":"3307","gst_rate":18},
    {"name":"Whisper Ultra Thin 7 pads","brand":"P&G","sku":"PAD-WHIS-7PK","unit":"packet","pack_size":"7 pads","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(48),"quantity":12,"reorder_level":3,"hsn_code":"9619","gst_rate":0},
    {"name":"Stayfree Dry Max 7 pads","brand":"J&J","sku":"PAD-STAY-7PK","unit":"packet","pack_size":"7 pads","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(48),"quantity":12,"reorder_level":3,"hsn_code":"9619","gst_rate":0},

    # ════════════════════════════════════════════════════════════════
    # BABY CARE
    # ════════════════════════════════════════════════════════════════
    {"name":"Pampers Baby Diapers XL 40 count","brand":"P&G","sku":"DIAP-PAM-XL-40","unit":"packet","pack_size":"40 pcs","loose":0,"cost_price":p(785),"sell_price":p(915),"mrp":p(975),"quantity":6,"reorder_level":2,"hsn_code":"9619","gst_rate":12},
    {"name":"Huggies Wonder Pants XL 42 count","brand":"Kimberly-Clark","sku":"DIAP-HUG-XL-42","unit":"packet","pack_size":"42 pcs","loose":0,"cost_price":p(795),"sell_price":p(925),"mrp":p(985),"quantity":5,"reorder_level":1,"hsn_code":"9619","gst_rate":12},
    {"name":"Johnsons Baby Powder 200g","brand":"J&J","sku":"BABYPOW-JNJ-200G","unit":"bottle","pack_size":"200g","loose":0,"cost_price":p(115),"sell_price":p(135),"mrp":p(148),"quantity":8,"reorder_level":2,"hsn_code":"3304","gst_rate":18},
    {"name":"Johnsons Baby Shampoo 200ml","brand":"J&J","sku":"BABYSMP-JNJ-200ML","unit":"bottle","pack_size":"200ml","loose":0,"cost_price":p(148),"sell_price":p(175),"mrp":p(188),"quantity":6,"reorder_level":2,"hsn_code":"3305","gst_rate":18},
    {"name":"Johnsons Baby Oil 200ml","brand":"J&J","sku":"BABYOIL-JNJ-200ML","unit":"bottle","pack_size":"200ml","loose":0,"cost_price":p(148),"sell_price":p(175),"mrp":p(188),"quantity":6,"reorder_level":2,"hsn_code":"3304","gst_rate":18},
    {"name":"Nestum Baby Cereal Wheat 300g","brand":"Nestle","sku":"BABYCR-NEST-300G","unit":"packet","pack_size":"300g","loose":0,"cost_price":p(188),"sell_price":p(220),"mrp":p(235),"quantity":6,"reorder_level":2,"hsn_code":"1901","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # MOSQUITO REPELLENT / PEST CONTROL
    # ════════════════════════════════════════════════════════════════
    {"name":"Good Knight Fast Card","brand":"Good Knight","sku":"MOS-GK-CARD","unit":"packet","pack_size":"10 cards","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":20,"reorder_level":5,"hsn_code":"3808","gst_rate":18},
    {"name":"All Out Liquid Machine + Refill","brand":"All Out","sku":"MOS-ALLOUT-MACH","unit":"piece","pack_size":"1 set","loose":0,"cost_price":p(95),"sell_price":p(112),"mrp":p(122),"quantity":10,"reorder_level":3,"hsn_code":"3808","gst_rate":18},
    {"name":"Hit Spray Flying Insects 400ml","brand":"Godrej","sku":"PEST-HIT-400ML","unit":"can","pack_size":"400ml","loose":0,"cost_price":p(132),"sell_price":p(155),"mrp":p(170),"quantity":10,"reorder_level":3,"hsn_code":"3808","gst_rate":18},
    {"name":"Mortein Coil 10 pack","brand":"Mortein","sku":"MOS-MORT-10PK","unit":"packet","pack_size":"10 coils","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":15,"reorder_level":4,"hsn_code":"3808","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # PACKAGED FOODS (extended)
    # ════════════════════════════════════════════════════════════════
    {"name":"Dabur Real Honey 500g","brand":"Dabur","sku":"HONEY-DAB-500G","unit":"jar","pack_size":"500g","loose":0,"cost_price":p(178),"sell_price":p(208),"mrp":p(225),"quantity":8,"reorder_level":2,"hsn_code":"0409","gst_rate":5},
    {"name":"Patanjali Honey 250g","brand":"Patanjali","sku":"HONEY-PAT-250G","unit":"jar","pack_size":"250g","loose":0,"cost_price":p(78),"sell_price":p(92),"mrp":p(100),"quantity":10,"reorder_level":3,"hsn_code":"0409","gst_rate":5},
    {"name":"MTR Gulab Jamun Mix 200g","brand":"MTR","sku":"MIX-MTR-GJ-200G","unit":"packet","pack_size":"200g","loose":0,"cost_price":p(72),"sell_price":p(85),"mrp":p(92),"quantity":10,"reorder_level":3,"hsn_code":"2106","gst_rate":18},
    {"name":"MTR Gajar Halwa Mix 200g","brand":"MTR","sku":"MIX-MTR-GH-200G","unit":"packet","pack_size":"200g","loose":0,"cost_price":p(72),"sell_price":p(85),"mrp":p(92),"quantity":8,"reorder_level":2,"hsn_code":"2106","gst_rate":18},
    {"name":"Gits Idli Mix 500g","brand":"Gits","sku":"MIX-GITS-IDL-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(80),"sell_price":p(95),"mrp":p(102),"quantity":8,"reorder_level":2,"hsn_code":"1901","gst_rate":5},
    {"name":"Gits Dosa Mix 500g","brand":"Gits","sku":"MIX-GITS-DOSA-500G","unit":"packet","pack_size":"500g","loose":0,"cost_price":p(80),"sell_price":p(95),"mrp":p(102),"quantity":8,"reorder_level":2,"hsn_code":"1901","gst_rate":5},
    {"name":"Everest Biryani Pulao Masala 50g","brand":"Everest","sku":"SPICE-EVR-BIR-50G","unit":"packet","pack_size":"50g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":10,"reorder_level":3,"hsn_code":"0910","gst_rate":5},
    {"name":"Knorr Chicken Soup 46g","brand":"Knorr","sku":"SOUP-KNORR-CHK-46G","unit":"packet","pack_size":"46g","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":10,"reorder_level":3,"hsn_code":"2104","gst_rate":12},
    {"name":"Maggi Masala-ae-Magic 72g","brand":"Nestle","sku":"MAGGI-MAGIC-72G","unit":"packet","pack_size":"72g","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(40),"quantity":15,"reorder_level":4,"hsn_code":"0910","gst_rate":5},

    # ════════════════════════════════════════════════════════════════
    # HOUSEHOLD / PAPER & MISC
    # ════════════════════════════════════════════════════════════════
    {"name":"Tissue Paper Roll (set of 4)","brand":"Renova","sku":"TISSUE-4PK","unit":"packet","pack_size":"4 rolls","loose":0,"cost_price":p(75),"sell_price":p(90),"mrp":p(99),"quantity":12,"reorder_level":3,"hsn_code":"4803","gst_rate":18},
    {"name":"Scotch-Brite Sponge Scrub Pad 2-pack","brand":"3M","sku":"SCRUB-3M-2PK","unit":"packet","pack_size":"2 pcs","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":15,"reorder_level":4,"hsn_code":"3401","gst_rate":18},
    {"name":"Ezee Liquid Detergent 1L","brand":"Godrej","sku":"DET-EZEE-1L","unit":"bottle","pack_size":"1L","loose":0,"cost_price":p(142),"sell_price":p(168),"mrp":p(180),"quantity":8,"reorder_level":2,"hsn_code":"3402","gst_rate":18},
    {"name":"Candle (10 pack)","brand":"Local","sku":"CANDLE-10PK","unit":"packet","pack_size":"10 pcs","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(40),"quantity":15,"reorder_level":4,"hsn_code":"3406","gst_rate":12},
    {"name":"Match Box (10 pack)","brand":"Local","sku":"MATCH-10PK","unit":"packet","pack_size":"10 boxes","loose":0,"cost_price":p(12),"sell_price":p(15),"mrp":p(18),"quantity":20,"reorder_level":5,"hsn_code":"3605","gst_rate":12},
    {"name":"Zip Lock Bags 20 pack","brand":"Local","sku":"ZIPBAG-20PK","unit":"packet","pack_size":"20 pcs","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(40),"quantity":12,"reorder_level":3,"hsn_code":"3923","gst_rate":18},
    {"name":"Foil Paper Roll (10m)","brand":"Local","sku":"FOIL-10M","unit":"roll","pack_size":"10m","loose":0,"cost_price":p(35),"sell_price":p(42),"mrp":p(48),"quantity":12,"reorder_level":3,"hsn_code":"7607","gst_rate":18},
    {"name":"Broom (Jhadu) Plastic","brand":"Local","sku":"BROOM-PLAST","unit":"piece","pack_size":"1 piece","loose":0,"cost_price":p(65),"sell_price":p(80),"mrp":p(90),"quantity":10,"reorder_level":3,"hsn_code":"9603","gst_rate":18},
    {"name":"Dustpan Set","brand":"Local","sku":"DUSTPAN-SET","unit":"piece","pack_size":"1 set","loose":0,"cost_price":p(85),"sell_price":p(105),"mrp":p(120),"quantity":8,"reorder_level":2,"hsn_code":"9603","gst_rate":18},
    {"name":"Pigeon Pressure Cooker 3L","brand":"Pigeon","sku":"COOKER-PIG-3L","unit":"piece","pack_size":"3L","loose":0,"cost_price":p(595),"sell_price":p(695),"mrp":p(750),"quantity":4,"reorder_level":1,"hsn_code":"7323","gst_rate":12},
    {"name":"Prestige Pressure Cooker 5L","brand":"Prestige","sku":"COOKER-PRES-5L","unit":"piece","pack_size":"5L","loose":0,"cost_price":p(845),"sell_price":p(995),"mrp":p(1095),"quantity":3,"reorder_level":1,"hsn_code":"7323","gst_rate":12},
    {"name":"Steel Plate (Thali) Set of 6","brand":"Local","sku":"PLATE-STEEL-6PK","unit":"packet","pack_size":"6 pcs","loose":0,"cost_price":p(445),"sell_price":p(525),"mrp":p(580),"quantity":3,"reorder_level":1,"hsn_code":"7323","gst_rate":12},
    {"name":"Steel Katori (Bowl) Set of 6","brand":"Local","sku":"KATORI-STEEL-6PK","unit":"packet","pack_size":"6 pcs","loose":0,"cost_price":p(285),"sell_price":p(338),"mrp":p(375),"quantity":3,"reorder_level":1,"hsn_code":"7323","gst_rate":12},
    {"name":"Polythene Bags 1kg","brand":"Local","sku":"POLYBAG-1KG","unit":"kg","pack_size":"1kg","loose":0,"cost_price":p(85),"sell_price":p(100),"mrp":p(110),"quantity":5,"reorder_level":2,"hsn_code":"3923","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # AGARBATTI / POOJA
    # ════════════════════════════════════════════════════════════════
    {"name":"Cycle Brand Agarbatti 100g","brand":"Cycle","sku":"AGARBATTI-CYC-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(40),"quantity":15,"reorder_level":4,"hsn_code":"3307","gst_rate":12},
    {"name":"Patanjali Agarbatti 100g","brand":"Patanjali","sku":"AGARBATTI-PAT-100G","unit":"packet","pack_size":"100g","loose":0,"cost_price":p(22),"sell_price":p(28),"mrp":p(32),"quantity":15,"reorder_level":4,"hsn_code":"3307","gst_rate":12},
    {"name":"HEM Lavender Incense 120 sticks","brand":"HEM","sku":"AGARBATTI-HEM-120","unit":"packet","pack_size":"120 sticks","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(50),"quantity":12,"reorder_level":3,"hsn_code":"3307","gst_rate":12},
    {"name":"Camphor (Kapoor) 10g","brand":"Local","sku":"CAMPHOR-10G","unit":"packet","pack_size":"10g","loose":0,"cost_price":p(10),"sell_price":p(12),"mrp":p(15),"quantity":20,"reorder_level":5,"hsn_code":"2914","gst_rate":12},

    # ════════════════════════════════════════════════════════════════
    # MEDICINES / OTC (common kirana items)
    # ════════════════════════════════════════════════════════════════
    {"name":"Dettol Antiseptic Liquid 100ml","brand":"Dettol","sku":"ANTIS-DETT-100ML","unit":"bottle","pack_size":"100ml","loose":0,"cost_price":p(62),"sell_price":p(75),"mrp":p(82),"quantity":10,"reorder_level":3,"hsn_code":"3808","gst_rate":18},
    {"name":"Savlon Antiseptic Liquid 100ml","brand":"Savlon","sku":"ANTIS-SAV-100ML","unit":"bottle","pack_size":"100ml","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(72),"quantity":8,"reorder_level":2,"hsn_code":"3808","gst_rate":18},
    {"name":"Band-Aid Flexible Fabric 10 strips","brand":"J&J","sku":"BAND-JNJ-10PK","unit":"packet","pack_size":"10 strips","loose":0,"cost_price":p(38),"sell_price":p(45),"mrp":p(52),"quantity":10,"reorder_level":3,"hsn_code":"3005","gst_rate":12},
    {"name":"Vicks VapoRub 50ml","brand":"P&G","sku":"VICKS-50ML","unit":"jar","pack_size":"50ml","loose":0,"cost_price":p(88),"sell_price":p(108),"mrp":p(118),"quantity":8,"reorder_level":2,"hsn_code":"3004","gst_rate":12},
    {"name":"Iodex Muscle Gel 30g","brand":"GSK","sku":"IODEX-30G","unit":"tube","pack_size":"30g","loose":0,"cost_price":p(65),"sell_price":p(78),"mrp":p(85),"quantity":8,"reorder_level":2,"hsn_code":"3004","gst_rate":12},
    {"name":"ORS Sachets Electral (5 pack)","brand":"Franco","sku":"ORS-ELECTRAL-5PK","unit":"packet","pack_size":"5 sachets","loose":0,"cost_price":p(38),"sell_price":p(48),"mrp":p(55),"quantity":10,"reorder_level":3,"hsn_code":"3004","gst_rate":12},
    {"name":"Himalaya Liv.52 100 tabs","brand":"Himalaya","sku":"LIV52-100T","unit":"packet","pack_size":"100 tablets","loose":0,"cost_price":p(112),"sell_price":p(135),"mrp":p(148),"quantity":6,"reorder_level":2,"hsn_code":"3004","gst_rate":12},

    # ════════════════════════════════════════════════════════════════
    # STATIONERY / MISC
    # ════════════════════════════════════════════════════════════════
    {"name":"Natraj Pencil 12 pack","brand":"Natraj","sku":"PENCIL-NAT-12PK","unit":"packet","pack_size":"12 pcs","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(40),"quantity":12,"reorder_level":3,"hsn_code":"9609","gst_rate":12},
    {"name":"Reynolds 045 Pen 5 pack","brand":"Reynolds","sku":"PEN-REY-5PK","unit":"packet","pack_size":"5 pcs","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(40),"quantity":12,"reorder_level":3,"hsn_code":"9608","gst_rate":12},
    {"name":"Fevicol SH 50g","brand":"Fevicol","sku":"FEVICOL-50G","unit":"tube","pack_size":"50g","loose":0,"cost_price":p(28),"sell_price":p(35),"mrp":p(40),"quantity":10,"reorder_level":3,"hsn_code":"3506","gst_rate":18},
    {"name":"Notebook 200 pages","brand":"Navneet","sku":"NB-200PG","unit":"piece","pack_size":"1 pc","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(75),"quantity":15,"reorder_level":4,"hsn_code":"4820","gst_rate":12},

    # ════════════════════════════════════════════════════════════════
    # FROZEN / READY TO EAT
    # ════════════════════════════════════════════════════════════════
    {"name":"McCain Frozen Fries 420g","brand":"McCain","sku":"FRIES-MCC-420G","unit":"packet","pack_size":"420g","loose":0,"cost_price":p(145),"sell_price":p(172),"mrp":p(185),"quantity":8,"reorder_level":2,"hsn_code":"2004","gst_rate":12},
    {"name":"Haldiram's Ready to Eat Dal Makhani 300g","brand":"Haldiram's","sku":"RTE-HALD-DM-300G","unit":"packet","pack_size":"300g","loose":0,"cost_price":p(95),"sell_price":p(115),"mrp":p(125),"quantity":8,"reorder_level":2,"hsn_code":"2004","gst_rate":12},
    {"name":"MTR Ready to Eat Palak Paneer 300g","brand":"MTR","sku":"RTE-MTR-PP-300G","unit":"packet","pack_size":"300g","loose":0,"cost_price":p(98),"sell_price":p(118),"mrp":p(128),"quantity":8,"reorder_level":2,"hsn_code":"2004","gst_rate":12},
    {"name":"McCain Veggie Burger Patty 240g","brand":"McCain","sku":"PATTY-MCC-240G","unit":"packet","pack_size":"240g","loose":0,"cost_price":p(152),"sell_price":p(178),"mrp":p(195),"quantity":6,"reorder_level":2,"hsn_code":"1601","gst_rate":12},

    # ════════════════════════════════════════════════════════════════
    # BAKERY / BREAD
    # ════════════════════════════════════════════════════════════════
    {"name":"Harvest Gold Bread 400g","brand":"Harvest Gold","sku":"BREAD-HG-400G","unit":"packet","pack_size":"400g","loose":0,"cost_price":p(40),"sell_price":p(48),"mrp":p(52),"quantity":10,"reorder_level":3,"hsn_code":"1905","gst_rate":12},
    {"name":"Modern Bread 400g","brand":"Modern","sku":"BREAD-MOD-400G","unit":"packet","pack_size":"400g","loose":0,"cost_price":p(40),"sell_price":p(48),"mrp":p(52),"quantity":10,"reorder_level":3,"hsn_code":"1905","gst_rate":12},
    {"name":"Britannia Whole Wheat Bread 400g","brand":"Britannia","sku":"BREAD-BRIT-WW-400G","unit":"packet","pack_size":"400g","loose":0,"cost_price":p(45),"sell_price":p(55),"mrp":p(60),"quantity":8,"reorder_level":2,"hsn_code":"1905","gst_rate":12},
    {"name":"Britannia Fruit Cake 55g","brand":"Britannia","sku":"CAKE-BRIT-FR-55G","unit":"piece","pack_size":"55g","loose":0,"cost_price":p(18),"sell_price":p(22),"mrp":p(25),"quantity":20,"reorder_level":5,"hsn_code":"1905","gst_rate":18},
    {"name":"Britannia Cake 60g (Individually Wrapped)","brand":"Britannia","sku":"CAKE-BRIT-60G","unit":"piece","pack_size":"60g","loose":0,"cost_price":p(22),"sell_price":p(28),"mrp":p(30),"quantity":20,"reorder_level":5,"hsn_code":"1905","gst_rate":18},
    {"name":"Monginis Chocolate Pastry","brand":"Monginis","sku":"CAKE-MONG-CHOC","unit":"piece","pack_size":"1 pc","loose":0,"cost_price":p(35),"sell_price":p(45),"mrp":p(50),"quantity":10,"reorder_level":3,"hsn_code":"1905","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # HAIR CARE / COLOUR
    # ════════════════════════════════════════════════════════════════
    {"name":"Garnier Color Naturals Black","brand":"Garnier","sku":"HAIRCOLOR-GAR-BLK","unit":"packet","pack_size":"1 application","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(115),"quantity":8,"reorder_level":2,"hsn_code":"3305","gst_rate":18},
    {"name":"Godrej Expert Rich Creme Black","brand":"Godrej","sku":"HAIRCOLOR-GOD-BLK","unit":"packet","pack_size":"1 application","loose":0,"cost_price":p(55),"sell_price":p(65),"mrp":p(72),"quantity":8,"reorder_level":2,"hsn_code":"3305","gst_rate":18},
    {"name":"Indulekha Bringha Hair Oil 100ml","brand":"Indulekha","sku":"HOIL-IND-100ML","unit":"bottle","pack_size":"100ml","loose":0,"cost_price":p(215),"sell_price":p(250),"mrp":p(268),"quantity":6,"reorder_level":2,"hsn_code":"3305","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # SKINCARE / SUNSCREEN
    # ════════════════════════════════════════════════════════════════
    {"name":"Lakme Sun Expert SPF 50 50ml","brand":"Lakme","sku":"SUNCR-LAK-50ML","unit":"tube","pack_size":"50ml","loose":0,"cost_price":p(178),"sell_price":p(210),"mrp":p(225),"quantity":6,"reorder_level":2,"hsn_code":"3304","gst_rate":18},
    {"name":"Lotus Herbals Safe Sun SPF 30 50g","brand":"Lotus","sku":"SUNCR-LOT-50G","unit":"tube","pack_size":"50g","loose":0,"cost_price":p(145),"sell_price":p(172),"mrp":p(185),"quantity":6,"reorder_level":2,"hsn_code":"3304","gst_rate":18},
    {"name":"Himalaya Neem Face Wash 150ml","brand":"Himalaya","sku":"FACEWASH-HIM-150ML","unit":"tube","pack_size":"150ml","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(115),"quantity":8,"reorder_level":2,"hsn_code":"3304","gst_rate":18},
    {"name":"Clean & Clear Face Wash 150ml","brand":"J&J","sku":"FACEWASH-CC-150ML","unit":"tube","pack_size":"150ml","loose":0,"cost_price":p(112),"sell_price":p(132),"mrp":p(142),"quantity":8,"reorder_level":2,"hsn_code":"3304","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # FOOTWEAR / ACCESSORIES (small kirana stock)
    # ════════════════════════════════════════════════════════════════
    {"name":"Hawai Slipper (pair)","brand":"Local","sku":"SLIP-HAWA-PAIR","unit":"pair","pack_size":"1 pair","loose":0,"cost_price":p(55),"sell_price":p(70),"mrp":p(80),"quantity":10,"reorder_level":3,"hsn_code":"6402","gst_rate":12},
    {"name":"Kiwi Shoe Polish Black 40ml","brand":"Kiwi","sku":"POLISH-KIWI-40ML","unit":"tin","pack_size":"40ml","loose":0,"cost_price":p(65),"sell_price":p(78),"mrp":p(85),"quantity":8,"reorder_level":2,"hsn_code":"3405","gst_rate":18},

    # ════════════════════════════════════════════════════════════════
    # BATTERIES / ELECTRICAL
    # ════════════════════════════════════════════════════════════════
    {"name":"Duracell AA Battery 2 pack","brand":"Duracell","sku":"BATT-DUR-AA-2PK","unit":"packet","pack_size":"2 pcs","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(115),"quantity":10,"reorder_level":3,"hsn_code":"8506","gst_rate":18},
    {"name":"Eveready AA Battery 4 pack","brand":"Eveready","sku":"BATT-EVE-AA-4PK","unit":"packet","pack_size":"4 pcs","loose":0,"cost_price":p(55),"sell_price":p(68),"mrp":p(75),"quantity":10,"reorder_level":3,"hsn_code":"8506","gst_rate":18},
    {"name":"Eveready AAA Battery 4 pack","brand":"Eveready","sku":"BATT-EVE-AAA-4PK","unit":"packet","pack_size":"4 pcs","loose":0,"cost_price":p(55),"sell_price":p(68),"mrp":p(75),"quantity":8,"reorder_level":2,"hsn_code":"8506","gst_rate":18},
    {"name":"Philips LED Bulb 9W","brand":"Philips","sku":"BULB-PHIL-9W","unit":"piece","pack_size":"1 pc","loose":0,"cost_price":p(88),"sell_price":p(105),"mrp":p(115),"quantity":10,"reorder_level":3,"hsn_code":"8539","gst_rate":12},
    {"name":"Syska LED Bulb 7W","brand":"Syska","sku":"BULB-SYSK-7W","unit":"piece","pack_size":"1 pc","loose":0,"cost_price":p(65),"sell_price":p(80),"mrp":p(90),"quantity":10,"reorder_level":3,"hsn_code":"8539","gst_rate":12},
    {"name":"Havells LED Bulb 12W","brand":"Havells","sku":"BULB-HAV-12W","unit":"piece","pack_size":"1 pc","loose":0,"cost_price":p(105),"sell_price":p(125),"mrp":p(138),"quantity":8,"reorder_level":2,"hsn_code":"8539","gst_rate":12},
    {"name":"Extension Cord 4-socket 2m","brand":"Havells","sku":"EXTCORD-HAV-4S-2M","unit":"piece","pack_size":"1 pc","loose":0,"cost_price":p(245),"sell_price":p(295),"mrp":p(325),"quantity":5,"reorder_level":2,"hsn_code":"8544","gst_rate":18},
    {"name":"Wipro 9W LED Bulb","brand":"Wipro","sku":"BULB-WIP-9W","unit":"piece","pack_size":"1 pc","loose":0,"cost_price":p(72),"sell_price":p(88),"mrp":p(98),"quantity":8,"reorder_level":2,"hsn_code":"8539","gst_rate":12},

]


# ---------------------------------------------------------------------------
def seed_products():
    init_db()
    inserted = 0
    skipped = 0

    with get_db() as db:
        for product in PRODUCTS:
            existing = db.execute(
                "SELECT id FROM products WHERE sku = ?",
                (product["sku"],)
            ).fetchone()

            if existing:
                skipped += 1
                continue

            db.execute(
                """
                INSERT INTO products
                (name, brand, sku, unit, pack_size, loose,
                 cost_price, sell_price, mrp,
                 quantity, reorder_level,
                 hsn_code, gst_rate, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    product["name"], product["brand"], product["sku"],
                    product["unit"], product["pack_size"], product["loose"],
                    product["cost_price"], product["sell_price"], product["mrp"],
                    product["quantity"], product["reorder_level"],
                    product["hsn_code"], product["gst_rate"], NOW,
                ),
            )
            inserted += 1

    print(f"Done - {inserted} new products inserted, {skipped} skipped (already exist).")


if __name__ == "__main__":
    seed_products()
    # Print final count
    from database import get_db
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    print(f"Total products in kirana.db: {total}")
