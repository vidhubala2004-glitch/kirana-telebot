"""
seed_blinkit.py
---------------
Seeds / updates the kirana.db with accurate prices sourced from Blinkit (2024-26).

Prices are stored in PAISE (₹1 = 100 paise), matching the existing schema:
  cost_price  – what the shopkeeper pays (approx. 8-12 % below MRP / sell price)
  sell_price  – what you charge the customer (≈ Blinkit / market price)
  mrp         – Maximum Retail Price printed on pack

All products use INSERT OR REPLACE so re-running is safe.
"""

from datetime import datetime
from database import init_db, get_db

NOW = datetime.now().isoformat(timespec="seconds")

# ---------------------------------------------------------------------------
# Helper: rupees → paise
# ---------------------------------------------------------------------------
def p(rupees: float) -> int:
    return int(round(rupees * 100))


# ---------------------------------------------------------------------------
# Master product list  (Blinkit-sourced prices, Sept 2024-26)
# ---------------------------------------------------------------------------
PRODUCTS = [

    # ── ATTA / FLOUR ────────────────────────────────────────────────────────
    {
        "name": "Aashirvaad Atta 5kg",
        "brand": "Aashirvaad",
        "sku": "ATT-AASH-5KG",
        "unit": "kg", "pack_size": "5kg", "loose": 0,
        "cost_price": p(218),   # trade price ~10 % off MRP
        "sell_price": p(244),   # Blinkit price Rs.244
        "mrp":        p(255),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "1101", "gst_rate": 5,
    },
    {
        "name": "Aashirvaad Multigrain Atta 5kg",
        "brand": "Aashirvaad",
        "sku": "ATT-AASH-MULTI-5KG",
        "unit": "kg", "pack_size": "5kg", "loose": 0,
        "cost_price": p(268),
        "sell_price": p(296),
        "mrp":        p(310),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "1101", "gst_rate": 5,
    },
    {
        "name": "Pillsbury Chakki Fresh Atta 5kg",
        "brand": "Pillsbury",
        "sku": "ATT-PILL-5KG",
        "unit": "kg", "pack_size": "5kg", "loose": 0,
        "cost_price": p(215),
        "sell_price": p(238),
        "mrp":        p(250),
        "quantity": 15, "reorder_level": 5,
        "hsn_code": "1101", "gst_rate": 5,
    },

    # ── RICE ────────────────────────────────────────────────────────────────
    {
        "name": "India Gate Basmati Rice 5kg",
        "brand": "India Gate",
        "sku": "RICE-IG-BASM-5KG",
        "unit": "kg", "pack_size": "5kg", "loose": 0,
        "cost_price": p(430),
        "sell_price": p(475),
        "mrp":        p(499),
        "quantity": 15, "reorder_level": 4,
        "hsn_code": "1006", "gst_rate": 0,
    },
    {
        "name": "Daawat Basmati Rice 1kg",
        "brand": "Daawat",
        "sku": "RICE-DAAWAT-1KG",
        "unit": "kg", "pack_size": "1kg", "loose": 0,
        "cost_price": p(92),
        "sell_price": p(105),
        "mrp":        p(110),
        "quantity": 25, "reorder_level": 8,
        "hsn_code": "1006", "gst_rate": 0,
    },
    {
        "name": "Loose Rice",
        "brand": "Local",
        "sku": "RICE-LOOSE",
        "unit": "kg", "pack_size": "loose", "loose": 1,
        "cost_price": p(45),
        "sell_price": p(52),
        "mrp":        p(52),
        "quantity": 60, "reorder_level": 15,
        "hsn_code": "1006", "gst_rate": 0,
    },

    # ── SALT, SUGAR ────────────────────────────────────────────────────────
    {
        "name": "Tata Salt 1kg",
        "brand": "Tata",
        "sku": "SALT-TATA-1KG",
        "unit": "kg", "pack_size": "1kg", "loose": 0,
        "cost_price": p(22),
        "sell_price": p(26),   # Blinkit Rs.25-28
        "mrp":        p(28),
        "quantity": 40, "reorder_level": 10,
        "hsn_code": "2501", "gst_rate": 0,
    },
    {
        "name": "Aashirvaad Salt 1kg",
        "brand": "Aashirvaad",
        "sku": "SALT-AASH-1KG",
        "unit": "kg", "pack_size": "1kg", "loose": 0,
        "cost_price": p(24),
        "sell_price": p(27),
        "mrp":        p(30),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "2501", "gst_rate": 0,
    },
    {
        "name": "Loose Sugar",
        "brand": "Local",
        "sku": "SUGAR-LOOSE",
        "unit": "kg", "pack_size": "loose", "loose": 1,
        "cost_price": p(40),
        "sell_price": p(46),   # market rate Rs.44-48/kg
        "mrp":        p(46),
        "quantity": 50, "reorder_level": 10,
        "hsn_code": "1701", "gst_rate": 0,
    },
    {
        "name": "Uttam Sugar 1kg",
        "brand": "Uttam",
        "sku": "SUGAR-UTT-1KG",
        "unit": "kg", "pack_size": "1kg", "loose": 0,
        "cost_price": p(41),
        "sell_price": p(47),
        "mrp":        p(50),
        "quantity": 30, "reorder_level": 8,
        "hsn_code": "1701", "gst_rate": 0,
    },

    # ── DAL / PULSES ────────────────────────────────────────────────────────
    {
        "name": "Toor Dal",
        "brand": "Local",
        "sku": "DAL-TOOR",
        "unit": "kg", "pack_size": "loose", "loose": 1,
        "cost_price": p(100),
        "sell_price": p(115),  # market Rs.110-120/kg
        "mrp":        p(115),
        "quantity": 30, "reorder_level": 8,
        "hsn_code": "0713", "gst_rate": 0,
    },
    {
        "name": "Tata Sampann Toor Dal 1kg",
        "brand": "Tata Sampann",
        "sku": "DAL-TATA-TOOR-1KG",
        "unit": "kg", "pack_size": "1kg", "loose": 0,
        "cost_price": p(108),
        "sell_price": p(125),  # Blinkit ~Rs.122-130
        "mrp":        p(135),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "0713", "gst_rate": 0,
    },
    {
        "name": "Moong Dal (loose) 1kg",
        "brand": "Local",
        "sku": "DAL-MOONG-LOOSE",
        "unit": "kg", "pack_size": "loose", "loose": 1,
        "cost_price": p(105),
        "sell_price": p(120),
        "mrp":        p(120),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "0713", "gst_rate": 0,
    },
    {
        "name": "Chana Dal (loose) 1kg",
        "brand": "Local",
        "sku": "DAL-CHANA-LOOSE",
        "unit": "kg", "pack_size": "loose", "loose": 1,
        "cost_price": p(75),
        "sell_price": p(88),
        "mrp":        p(88),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "0713", "gst_rate": 0,
    },
    {
        "name": "Masoor Dal (loose) 1kg",
        "brand": "Local",
        "sku": "DAL-MASOOR-LOOSE",
        "unit": "kg", "pack_size": "loose", "loose": 1,
        "cost_price": p(82),
        "sell_price": p(95),
        "mrp":        p(95),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "0713", "gst_rate": 0,
    },

    # ── OILS ────────────────────────────────────────────────────────────────
    {
        "name": "Fortune Sunflower Oil 1L",
        "brand": "Fortune",
        "sku": "OIL-FORT-1L",
        "unit": "litre", "pack_size": "1L", "loose": 0,
        "cost_price": p(148),
        "sell_price": p(165),  # Blinkit ~Rs.160-170
        "mrp":        p(175),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "1512", "gst_rate": 5,
    },
    {
        "name": "Fortune Sunflower Oil 5L",
        "brand": "Fortune",
        "sku": "OIL-FORT-5L",
        "unit": "litre", "pack_size": "5L", "loose": 0,
        "cost_price": p(715),
        "sell_price": p(795),
        "mrp":        p(840),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "1512", "gst_rate": 5,
    },
    {
        "name": "Saffola Gold Oil 1L",
        "brand": "Saffola",
        "sku": "OIL-SAFF-1L",
        "unit": "litre", "pack_size": "1L", "loose": 0,
        "cost_price": p(162),
        "sell_price": p(182),  # Blinkit Rs.179-190
        "mrp":        p(195),
        "quantity": 12, "reorder_level": 4,
        "hsn_code": "1512", "gst_rate": 5,
    },
    {
        "name": "Dhara Mustard Oil 1L",
        "brand": "Dhara",
        "sku": "OIL-DHAR-MUST-1L",
        "unit": "litre", "pack_size": "1L", "loose": 0,
        "cost_price": p(148),
        "sell_price": p(165),
        "mrp":        p(175),
        "quantity": 12, "reorder_level": 4,
        "hsn_code": "1514", "gst_rate": 5,
    },

    # ── DAIRY ───────────────────────────────────────────────────────────────
    {
        "name": "Amul Butter 100g",
        "brand": "Amul",
        "sku": "BUT-AMUL-100G",
        "unit": "packet", "pack_size": "100g", "loose": 0,
        "cost_price": p(54),
        "sell_price": p(62),   # Blinkit Rs.60-63
        "mrp":        p(65),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "0405", "gst_rate": 12,
    },
    {
        "name": "Amul Butter 500g",
        "brand": "Amul",
        "sku": "BUT-AMUL-500G",
        "unit": "packet", "pack_size": "500g", "loose": 0,
        "cost_price": p(255),
        "sell_price": p(295),  # Blinkit ~Rs.290-300
        "mrp":        p(310),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "0405", "gst_rate": 12,
    },
    {
        "name": "Amul Taaza Milk 500ml",
        "brand": "Amul",
        "sku": "MILK-AMUL-500ML",
        "unit": "packet", "pack_size": "500ml", "loose": 0,
        "cost_price": p(26),
        "sell_price": p(30),   # Blinkit Rs.29-31
        "mrp":        p(31),
        "quantity": 30, "reorder_level": 10,
        "hsn_code": "0401", "gst_rate": 0,
    },
    {
        "name": "Amul Taaza Milk 1L",
        "brand": "Amul",
        "sku": "MILK-AMUL-1L",
        "unit": "packet", "pack_size": "1L", "loose": 0,
        "cost_price": p(52),
        "sell_price": p(60),
        "mrp":        p(62),
        "quantity": 25, "reorder_level": 8,
        "hsn_code": "0401", "gst_rate": 0,
    },
    {
        "name": "Amul Dahi 400g",
        "brand": "Amul",
        "sku": "DAHI-AMUL-400G",
        "unit": "packet", "pack_size": "400g", "loose": 0,
        "cost_price": p(40),
        "sell_price": p(47),   # Blinkit Rs.45-50
        "mrp":        p(50),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "0403", "gst_rate": 5,
    },
    {
        "name": "Amul Gold Milk 1L",
        "brand": "Amul",
        "sku": "MILK-AMUL-GOLD-1L",
        "unit": "packet", "pack_size": "1L", "loose": 0,
        "cost_price": p(58),
        "sell_price": p(66),
        "mrp":        p(68),
        "quantity": 20, "reorder_level": 8,
        "hsn_code": "0401", "gst_rate": 0,
    },
    {
        "name": "Nestle Milkmaid 400g",
        "brand": "Nestle",
        "sku": "MLKM-NEST-400G",
        "unit": "tin", "pack_size": "400g", "loose": 0,
        "cost_price": p(112),
        "sell_price": p(130),  # Blinkit ~Rs.128-135
        "mrp":        p(138),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "0402", "gst_rate": 12,
    },

    # ── NOODLES / PASTA / INSTANT ────────────────────────────────────────────
    {
        "name": "Maggi 70g",
        "brand": "Nestle",
        "sku": "MAGGI-70G",
        "unit": "packet", "pack_size": "70g", "loose": 0,
        "cost_price": p(12),
        "sell_price": p(14),   # Blinkit Rs.14
        "mrp":        p(15),
        "quantity": 80, "reorder_level": 20,
        "hsn_code": "1902", "gst_rate": 12,
    },
    {
        "name": "Maggi 4-Pack (280g)",
        "brand": "Nestle",
        "sku": "MAGGI-4PK-280G",
        "unit": "packet", "pack_size": "280g", "loose": 0,
        "cost_price": p(50),
        "sell_price": p(58),
        "mrp":        p(60),
        "quantity": 30, "reorder_level": 10,
        "hsn_code": "1902", "gst_rate": 12,
    },
    {
        "name": "Yippee Magic Masala 70g",
        "brand": "Sunfeast",
        "sku": "YIPPEE-70G",
        "unit": "packet", "pack_size": "70g", "loose": 0,
        "cost_price": p(12),
        "sell_price": p(15),
        "mrp":        p(15),
        "quantity": 50, "reorder_level": 10,
        "hsn_code": "1902", "gst_rate": 12,
    },

    # ── BISCUITS / SNACKS ────────────────────────────────────────────────────
    {
        "name": "Parle-G 250g",
        "brand": "Parle",
        "sku": "PARLE-G-250G",
        "unit": "packet", "pack_size": "250g", "loose": 0,
        "cost_price": p(26),
        "sell_price": p(30),   # Blinkit Rs.30
        "mrp":        p(30),
        "quantity": 50, "reorder_level": 10,
        "hsn_code": "1905", "gst_rate": 12,
    },
    {
        "name": "Parle-G",
        "brand": "Parle",
        "sku": "PARLE-G",
        "unit": "packet", "pack_size": "standard", "loose": 0,
        "cost_price": p(5),
        "sell_price": p(6),
        "mrp":        p(6),
        "quantity": 80, "reorder_level": 20,
        "hsn_code": "1905", "gst_rate": 12,
    },
    {
        "name": "Britannia Bourbon 120g",
        "brand": "Britannia",
        "sku": "BIS-BRIT-BOUR-120G",
        "unit": "packet", "pack_size": "120g", "loose": 0,
        "cost_price": p(26),
        "sell_price": p(30),
        "mrp":        p(30),
        "quantity": 30, "reorder_level": 8,
        "hsn_code": "1905", "gst_rate": 12,
    },
    {
        "name": "Britannia Good Day 100g",
        "brand": "Britannia",
        "sku": "BIS-BRIT-GD-100G",
        "unit": "packet", "pack_size": "100g", "loose": 0,
        "cost_price": p(22),
        "sell_price": p(25),
        "mrp":        p(25),
        "quantity": 30, "reorder_level": 8,
        "hsn_code": "1905", "gst_rate": 12,
    },
    {
        "name": "Lay's Chips Classic Salted 26g",
        "brand": "Lay's",
        "sku": "CHIPS-LAYS-26G",
        "unit": "packet", "pack_size": "26g", "loose": 0,
        "cost_price": p(18),
        "sell_price": p(20),
        "mrp":        p(20),
        "quantity": 60, "reorder_level": 15,
        "hsn_code": "1905", "gst_rate": 12,
    },
    {
        "name": "Kurkure Masala Munch 60g",
        "brand": "Kurkure",
        "sku": "KURK-MASA-60G",
        "unit": "packet", "pack_size": "60g", "loose": 0,
        "cost_price": p(18),
        "sell_price": p(20),
        "mrp":        p(20),
        "quantity": 50, "reorder_level": 15,
        "hsn_code": "1905", "gst_rate": 12,
    },

    # ── DETERGENT / CLEANING ─────────────────────────────────────────────────
    {
        "name": "Surf Excel Easy Wash 1kg",
        "brand": "Surf Excel",
        "sku": "SURF-EXCEL-1KG",
        "unit": "packet", "pack_size": "1kg", "loose": 0,
        "cost_price": p(210),
        "sell_price": p(237),  # Blinkit Rs.237
        "mrp":        p(255),
        "quantity": 15, "reorder_level": 4,
        "hsn_code": "3402", "gst_rate": 18,
    },
    {
        "name": "Surf Excel",
        "brand": "Surf Excel",
        "sku": "SURF-EXCEL",
        "unit": "packet", "pack_size": "standard", "loose": 0,
        "cost_price": p(65),
        "sell_price": p(75),
        "mrp":        p(80),
        "quantity": 15, "reorder_level": 5,
        "hsn_code": "3402", "gst_rate": 18,
    },
    {
        "name": "Ariel Powder 1kg",
        "brand": "Ariel",
        "sku": "DET-ARIEL-1KG",
        "unit": "packet", "pack_size": "1kg", "loose": 0,
        "cost_price": p(225),
        "sell_price": p(255),  # Blinkit ~Rs.249-260
        "mrp":        p(270),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "3402", "gst_rate": 18,
    },
    {
        "name": "Vim Dishwash Liquid 750ml",
        "brand": "Vim",
        "sku": "VIM-LIQ-750ML",
        "unit": "bottle", "pack_size": "750ml", "loose": 0,
        "cost_price": p(115),
        "sell_price": p(130),  # Blinkit ~Rs.125-135
        "mrp":        p(140),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "3402", "gst_rate": 18,
    },
    {
        "name": "Harpic Power Plus 500ml",
        "brand": "Harpic",
        "sku": "HARP-500ML",
        "unit": "bottle", "pack_size": "500ml", "loose": 0,
        "cost_price": p(96),
        "sell_price": p(112),  # Blinkit Rs.109-115
        "mrp":        p(120),
        "quantity": 8, "reorder_level": 3,
        "hsn_code": "3402", "gst_rate": 18,
    },

    # ── BEVERAGES ────────────────────────────────────────────────────────────
    {
        "name": "Tata Tea Premium 250g",
        "brand": "Tata Tea",
        "sku": "TEA-TATA-250G",
        "unit": "packet", "pack_size": "250g", "loose": 0,
        "cost_price": p(90),
        "sell_price": p(105),  # Blinkit ~Rs.102-110
        "mrp":        p(115),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "0902", "gst_rate": 5,
    },
    {
        "name": "Red Label Tea 500g",
        "brand": "Brooke Bond",
        "sku": "TEA-RL-500G",
        "unit": "packet", "pack_size": "500g", "loose": 0,
        "cost_price": p(192),
        "sell_price": p(220),  # Blinkit ~Rs.215-225
        "mrp":        p(235),
        "quantity": 15, "reorder_level": 4,
        "hsn_code": "0902", "gst_rate": 5,
    },
    {
        "name": "Nescafe Classic 50g",
        "brand": "Nestle",
        "sku": "COFF-NESC-50G",
        "unit": "jar", "pack_size": "50g", "loose": 0,
        "cost_price": p(222),
        "sell_price": p(255),  # Blinkit ~Rs.249-260
        "mrp":        p(270),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "2101", "gst_rate": 12,
    },
    {
        "name": "Bournvita 500g",
        "brand": "Cadbury",
        "sku": "BOUR-CAD-500G",
        "unit": "jar", "pack_size": "500g", "loose": 0,
        "cost_price": p(245),
        "sell_price": p(280),  # Blinkit ~Rs.275-285
        "mrp":        p(295),
        "quantity": 8, "reorder_level": 3,
        "hsn_code": "2106", "gst_rate": 18,
    },
    {
        "name": "Frooti Mango 200ml",
        "brand": "Parle Agro",
        "sku": "BEV-FROOTI-200ML",
        "unit": "packet", "pack_size": "200ml", "loose": 0,
        "cost_price": p(14),
        "sell_price": p(18),
        "mrp":        p(20),
        "quantity": 48, "reorder_level": 12,
        "hsn_code": "2202", "gst_rate": 12,
    },
    {
        "name": "Limca 750ml",
        "brand": "Coca-Cola",
        "sku": "BEV-LIMCA-750ML",
        "unit": "bottle", "pack_size": "750ml", "loose": 0,
        "cost_price": p(35),
        "sell_price": p(42),
        "mrp":        p(45),
        "quantity": 24, "reorder_level": 8,
        "hsn_code": "2202", "gst_rate": 12,
    },
    {
        "name": "Coca-Cola 600ml",
        "brand": "Coca-Cola",
        "sku": "BEV-COKE-600ML",
        "unit": "bottle", "pack_size": "600ml", "loose": 0,
        "cost_price": p(36),
        "sell_price": p(42),
        "mrp":        p(45),
        "quantity": 24, "reorder_level": 8,
        "hsn_code": "2202", "gst_rate": 12,
    },

    # ── SPICES / MASALA ──────────────────────────────────────────────────────
    {
        "name": "MDH Chana Masala 100g",
        "brand": "MDH",
        "sku": "SPICE-MDH-CHNM-100G",
        "unit": "packet", "pack_size": "100g", "loose": 0,
        "cost_price": p(55),
        "sell_price": p(65),   # Blinkit ~Rs.62-68
        "mrp":        p(70),
        "quantity": 15, "reorder_level": 4,
        "hsn_code": "0910", "gst_rate": 5,
    },
    {
        "name": "Everest Kitchen King 100g",
        "brand": "Everest",
        "sku": "SPICE-EVR-KK-100G",
        "unit": "packet", "pack_size": "100g", "loose": 0,
        "cost_price": p(58),
        "sell_price": p(68),
        "mrp":        p(72),
        "quantity": 15, "reorder_level": 4,
        "hsn_code": "0910", "gst_rate": 5,
    },
    {
        "name": "MDH Turmeric Powder 100g",
        "brand": "MDH",
        "sku": "SPICE-MDH-TURM-100G",
        "unit": "packet", "pack_size": "100g", "loose": 0,
        "cost_price": p(40),
        "sell_price": p(48),
        "mrp":        p(52),
        "quantity": 15, "reorder_level": 4,
        "hsn_code": "0910", "gst_rate": 5,
    },
    {
        "name": "Red Chilli Powder 100g",
        "brand": "Local",
        "sku": "SPICE-RCHP-LOOSE",
        "unit": "packet", "pack_size": "100g", "loose": 0,
        "cost_price": p(18),
        "sell_price": p(22),
        "mrp":        p(22),
        "quantity": 40, "reorder_level": 10,
        "hsn_code": "0904", "gst_rate": 5,
    },

    # ── PERSONAL CARE / SOAP ─────────────────────────────────────────────────
    {
        "name": "Dettol Soap 75g",
        "brand": "Dettol",
        "sku": "SOAP-DETT-75G",
        "unit": "piece", "pack_size": "75g", "loose": 0,
        "cost_price": p(42),
        "sell_price": p(50),   # Blinkit ~Rs.48-52
        "mrp":        p(55),
        "quantity": 24, "reorder_level": 6,
        "hsn_code": "3401", "gst_rate": 18,
    },
    {
        "name": "Lux Jasmine Soap 125g",
        "brand": "HUL",
        "sku": "SOAP-LUX-125G",
        "unit": "piece", "pack_size": "125g", "loose": 0,
        "cost_price": p(35),
        "sell_price": p(42),
        "mrp":        p(45),
        "quantity": 24, "reorder_level": 6,
        "hsn_code": "3401", "gst_rate": 18,
    },
    {
        "name": "Colgate Strong Teeth 200g",
        "brand": "Colgate",
        "sku": "TP-COLG-200G",
        "unit": "tube", "pack_size": "200g", "loose": 0,
        "cost_price": p(70),
        "sell_price": p(82),   # Blinkit ~Rs.80-85
        "mrp":        p(90),
        "quantity": 12, "reorder_level": 4,
        "hsn_code": "3306", "gst_rate": 18,
    },
    {
        "name": "Close-Up Toothpaste 150g",
        "brand": "HUL",
        "sku": "TP-CLOSEUP-150G",
        "unit": "tube", "pack_size": "150g", "loose": 0,
        "cost_price": p(62),
        "sell_price": p(75),
        "mrp":        p(80),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "3306", "gst_rate": 18,
    },
    {
        "name": "Head & Shoulders Shampoo 180ml",
        "brand": "P&G",
        "sku": "SHP-HNS-180ML",
        "unit": "bottle", "pack_size": "180ml", "loose": 0,
        "cost_price": p(158),
        "sell_price": p(185),  # Blinkit ~Rs.180-190
        "mrp":        p(199),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "3305", "gst_rate": 18,
    },
    {
        "name": "Clinic Plus Shampoo 175ml",
        "brand": "HUL",
        "sku": "SHP-CLINIC-175ML",
        "unit": "bottle", "pack_size": "175ml", "loose": 0,
        "cost_price": p(88),
        "sell_price": p(102),
        "mrp":        p(110),
        "quantity": 12, "reorder_level": 4,
        "hsn_code": "3305", "gst_rate": 18,
    },

    # ── PACKAGED FOODS ────────────────────────────────────────────────────────
    {
        "name": "Amul Cheese Slices 200g",
        "brand": "Amul",
        "sku": "CHEESE-AMUL-200G",
        "unit": "packet", "pack_size": "200g", "loose": 0,
        "cost_price": p(91),
        "sell_price": p(107),  # Blinkit ~Rs.105-110
        "mrp":        p(115),
        "quantity": 10, "reorder_level": 3,
        "hsn_code": "0406", "gst_rate": 12,
    },
    {
        "name": "Haldiram's Bhujia 200g",
        "brand": "Haldiram's",
        "sku": "BHUJIA-HALD-200G",
        "unit": "packet", "pack_size": "200g", "loose": 0,
        "cost_price": p(72),
        "sell_price": p(85),   # Blinkit ~Rs.82-88
        "mrp":        p(90),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "1905", "gst_rate": 12,
    },
    {
        "name": "Cadbury Dairy Milk 45g",
        "brand": "Cadbury",
        "sku": "CHOC-CDM-45G",
        "unit": "piece", "pack_size": "45g", "loose": 0,
        "cost_price": p(42),
        "sell_price": p(50),
        "mrp":        p(50),
        "quantity": 30, "reorder_level": 10,
        "hsn_code": "1806", "gst_rate": 18,
    },
    {
        "name": "Kit Kat 37g",
        "brand": "Nestle",
        "sku": "CHOC-KITKAT-37G",
        "unit": "piece", "pack_size": "37g", "loose": 0,
        "cost_price": p(27),
        "sell_price": p(32),
        "mrp":        p(35),
        "quantity": 30, "reorder_level": 10,
        "hsn_code": "1806", "gst_rate": 18,
    },

    # ── HOUSEHOLD / MISC ─────────────────────────────────────────────────────
    {
        "name": "Good Knight Coil 10 pack",
        "brand": "Good Knight",
        "sku": "MOS-GK-COIL-10",
        "unit": "packet", "pack_size": "10 coils", "loose": 0,
        "cost_price": p(38),
        "sell_price": p(45),   # Blinkit ~Rs.43-48
        "mrp":        p(50),
        "quantity": 20, "reorder_level": 5,
        "hsn_code": "3808", "gst_rate": 18,
    },
    {
        "name": "Phenyl Floor Cleaner 1L",
        "brand": "Local",
        "sku": "PHNYL-1L",
        "unit": "bottle", "pack_size": "1L", "loose": 0,
        "cost_price": p(55),
        "sell_price": p(65),
        "mrp":        p(70),
        "quantity": 12, "reorder_level": 4,
        "hsn_code": "3402", "gst_rate": 18,
    },
    {
        "name": "Lizol Disinfectant 500ml",
        "brand": "Lizol",
        "sku": "LIZOL-500ML",
        "unit": "bottle", "pack_size": "500ml", "loose": 0,
        "cost_price": p(118),
        "sell_price": p(140),  # Blinkit ~Rs.135-145
        "mrp":        p(150),
        "quantity": 8, "reorder_level": 3,
        "hsn_code": "3808", "gst_rate": 18,
    },
]


# ---------------------------------------------------------------------------
# Seed function
# ---------------------------------------------------------------------------
def seed_products():
    init_db()

    inserted = 0
    updated = 0

    with get_db() as db:
        for product in PRODUCTS:
            existing = db.execute(
                "SELECT id FROM products WHERE sku = ?",
                (product["sku"],)
            ).fetchone()

            if existing:
                db.execute(
                    """
                    UPDATE products
                    SET cost_price = ?,
                        sell_price = ?,
                        mrp        = ?,
                        name       = ?,
                        brand      = ?,
                        unit       = ?,
                        pack_size  = ?,
                        gst_rate   = ?
                    WHERE sku = ?
                    """,
                    (
                        product["cost_price"],
                        product["sell_price"],
                        product["mrp"],
                        product["name"],
                        product["brand"],
                        product["unit"],
                        product["pack_size"],
                        product["gst_rate"],
                        product["sku"],
                    ),
                )
                updated += 1
            else:
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
                        product["name"],
                        product["brand"],
                        product["sku"],
                        product["unit"],
                        product["pack_size"],
                        product["loose"],
                        product["cost_price"],
                        product["sell_price"],
                        product["mrp"],
                        product["quantity"],
                        product["reorder_level"],
                        product["hsn_code"],
                        product["gst_rate"],
                        NOW,
                    ),
                )
                inserted += 1

    print(f"Done - {inserted} products inserted, {updated} products updated.")
    print(f"Total products in DB: {inserted + updated}")


if __name__ == "__main__":
    seed_products()
