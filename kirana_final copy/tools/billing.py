from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import uuid

from database import get_db
from tools.inventory import paise_to_rupees
from tools.khata import consume_wallet

ALLOWED_PAYMENT_MODES = {"CASH", "UPI", "KHATA"}


def calculate_tax(taxable_amount, gst_rate):
    total_tax = (Decimal(taxable_amount) * Decimal(str(gst_rate)) / Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    cgst = int(total_tax // 2)
    sgst = int(total_tax) - cgst
    return cgst, sgst


def calculate_item(quantity, unit_price, gst_rate):
    qty = Decimal(str(quantity))
    taxable = (qty * Decimal(unit_price)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    cgst, sgst = calculate_tax(taxable, gst_rate)
    return {"taxable_amount": int(taxable), "cgst": cgst, "sgst": sgst, "total": int(taxable) + cgst + sgst}


def _new_bill_number(prefix="DRAFT"):
    return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"


def _get_draft(db, draft_key):
    return db.execute("SELECT * FROM bills WHERE draft_key=? AND status='DRAFT'", (str(draft_key),)).fetchone()


def create_bill_draft(draft_key, customer_name=None):
    with get_db() as db:
        bill = _get_draft(db, draft_key)
        if bill:
            if customer_name and bill["customer_name"] != customer_name.strip():
                db.execute("UPDATE bills SET customer_name=? WHERE id=?", (customer_name.strip(), bill["id"]))
        else:
            db.execute(
                "INSERT INTO bills(bill_number,draft_key,customer_name,status,created_at) VALUES (?,?,?,?,?)",
                (_new_bill_number(), str(draft_key), customer_name.strip() if customer_name else None, "DRAFT", datetime.now().isoformat(timespec="seconds")),
            )
    return get_bill_draft(draft_key)


def _ensure_draft(db, draft_key):
    bill = _get_draft(db, draft_key)
    if bill:
        return bill
    db.execute("INSERT INTO bills(bill_number,draft_key,status,created_at) VALUES (?,?,?,?)", (_new_bill_number(), str(draft_key), "DRAFT", datetime.now().isoformat(timespec="seconds")))
    return _get_draft(db, draft_key)


def add_bill_item(draft_key, product_id, quantity):
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        return {"success": False, "error": "Invalid quantity."}
    if quantity <= 0:
        return {"success": False, "error": "Quantity must be greater than zero."}
    with get_db() as db:
        bill = _ensure_draft(db, draft_key)
        product = db.execute("SELECT * FROM products WHERE id=?", (int(product_id),)).fetchone()
        if not product:
            return {"success": False, "error": "Product not found."}
        if product["sell_price"] < product["cost_price"]:
            return {"success": False, "error": f"Sale blocked for {product['name']}: selling price is below cost."}
        existing = db.execute("SELECT * FROM bill_items WHERE bill_id=? AND product_id=?", (bill["id"], product["id"])).fetchone()
        new_qty = quantity + (float(existing["quantity"]) if existing else 0)
        if float(product["quantity"]) < new_qty:
            return {"success": False, "error": f"Insufficient stock for {product['name']}. Available: {product['quantity']} {product['unit']}; requested in bill: {new_qty}."}
        calc = calculate_item(new_qty, product["sell_price"], product["gst_rate"])
        if existing:
            db.execute("UPDATE bill_items SET quantity=?,unit_price=?,gst_rate=?,taxable_amount=?,cgst=?,sgst=?,total=? WHERE id=?", (new_qty, product["sell_price"], product["gst_rate"], calc["taxable_amount"], calc["cgst"], calc["sgst"], calc["total"], existing["id"]))
        else:
            db.execute("""INSERT INTO bill_items(bill_id,product_id,quantity,unit_price,gst_rate,taxable_amount,cgst,sgst,total) VALUES(?,?,?,?,?,?,?,?,?)""", (bill["id"],product["id"],quantity,product["sell_price"],product["gst_rate"],calc["taxable_amount"],calc["cgst"],calc["sgst"],calc["total"]))
    return get_bill_draft(draft_key)


def remove_bill_item(draft_key, product_id):
    with get_db() as db:
        bill = _get_draft(db, draft_key)
        if not bill:
            return {"success": False, "error": "No active bill draft exists."}
        cur = db.execute("DELETE FROM bill_items WHERE bill_id=? AND product_id=?", (bill["id"], int(product_id)))
        if cur.rowcount == 0:
            return {"success": False, "error": "That product is not in the current bill."}
    return get_bill_draft(draft_key)


def update_bill_item(draft_key, product_id, quantity):
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        return {"success": False, "error": "Invalid quantity."}
    if quantity <= 0:
        return remove_bill_item(draft_key, product_id)
    with get_db() as db:
        bill = _get_draft(db, draft_key)
        if not bill:
            return {"success": False, "error": "No active draft."}
        product = db.execute("SELECT * FROM products WHERE id=?", (int(product_id),)).fetchone()
        if not product:
            return {"success": False, "error": "Product not found."}
        if float(product["quantity"]) < quantity:
            return {"success": False, "error": f"Insufficient stock for {product['name']}. Available: {product['quantity']} {product['unit']}; requested: {quantity}."}
        calc = calculate_item(quantity, product["sell_price"], product["gst_rate"])
        cur = db.execute("UPDATE bill_items SET quantity=?,unit_price=?,gst_rate=?,taxable_amount=?,cgst=?,sgst=?,total=? WHERE bill_id=? AND product_id=?", (quantity,product["sell_price"],product["gst_rate"],calc["taxable_amount"],calc["cgst"],calc["sgst"],calc["total"],bill["id"],int(product_id)))
        if cur.rowcount == 0:
            return {"success": False, "error": "Product is not in the bill."}
    return get_bill_draft(draft_key)


def _draft_payload(db, bill):
    rows = db.execute("""SELECT bi.*,p.name,p.brand,p.unit,p.pack_size,p.hsn_code,p.quantity AS stock_quantity FROM bill_items bi JOIN products p ON p.id=bi.product_id WHERE bi.bill_id=? ORDER BY bi.id""", (bill["id"],)).fetchall()
    subtotal = sum(int(r["taxable_amount"]) for r in rows)
    cgst = sum(int(r["cgst"]) for r in rows)
    sgst = sum(int(r["sgst"]) for r in rows)
    items = [{"product_id":r["product_id"],"name":r["name"],"brand":r["brand"],"quantity":r["quantity"],"unit":r["unit"],"unit_price":paise_to_rupees(r["unit_price"]),"gst_rate":r["gst_rate"],"taxable_amount":paise_to_rupees(r["taxable_amount"]),"cgst":paise_to_rupees(r["cgst"]),"sgst":paise_to_rupees(r["sgst"]),"total":paise_to_rupees(r["total"]),"hsn_code":r["hsn_code"],"stock_available":r["stock_quantity"]} for r in rows]
    return {"success":True,"bill_id":bill["id"],"bill_number":bill["bill_number"],"customer_name":bill["customer_name"],"status":bill["status"],"items":items,"subtotal":paise_to_rupees(subtotal),"discount":paise_to_rupees(bill["discount"] or 0),"cgst":paise_to_rupees(cgst),"sgst":paise_to_rupees(sgst),"total_tax":paise_to_rupees(cgst+sgst),"grand_total":paise_to_rupees(max(0,subtotal+cgst+sgst-int(bill["discount"] or 0)))}


def get_bill_draft(draft_key):
    with get_db() as db:
        bill = _get_draft(db, draft_key)
        if not bill:
            return {"success":False,"error":"No active bill draft."}
        return _draft_payload(db, bill)


def set_bill_discount(draft_key, discount_rupees):
    try: discount = float(discount_rupees)
    except (TypeError, ValueError): return {"success":False,"error":"Invalid discount."}
    if discount < 0: return {"success":False,"error":"Discount cannot be negative."}
    with get_db() as db:
        bill = _get_draft(db, draft_key)
        if not bill: return {"success":False,"error":"No active bill draft."}
        payload = _draft_payload(db,bill)
        if discount > payload["subtotal"] + payload["total_tax"]: return {"success":False,"error":"Discount cannot exceed bill total."}
        from tools.inventory import rupees_to_paise
        db.execute("UPDATE bills SET discount=? WHERE id=?", (rupees_to_paise(discount),bill["id"]))
    return get_bill_draft(draft_key)


def finalize_bill(draft_key, payment_mode, payment_reference=None, idempotency_key=None, discount_rupees=None):
    mode = str(payment_mode or "").upper().strip()
    if mode in {"GPAY","G-PAY","GOOGLE PAY","UPI"}: mode="UPI"
    if mode in {"CREDIT","WALLET","KHATA/CREDIT"}: mode="KHATA"
    if mode not in ALLOWED_PAYMENT_MODES:
        return {"success":False,"error":"Payment mode must be CASH, UPI or KHATA."}
    idem = idempotency_key or f"{draft_key}:{mode}"
    with get_db() as db:
        db.execute("BEGIN IMMEDIATE")
        # If the same idempotency key already finalized another bill, return it.
        existing_idem = db.execute("SELECT * FROM bills WHERE idempotency_key=?", (idem,)).fetchone()
        if existing_idem and existing_idem["status"] == "FINALIZED":
            return _get_finalized_bill(db, existing_idem["id"])
        bill = db.execute("SELECT * FROM bills WHERE draft_key=?", (str(draft_key),)).fetchone()
        if not bill:
            return {"success":False,"error":"Bill draft not found."}
        if bill["status"] == "FINALIZED":
            return _get_finalized_bill(db,bill["id"])
        if bill["status"] != "DRAFT":
            return {"success":False,"error":f"Bill is already {bill['status']}."}
        items = db.execute("""SELECT bi.*,p.name,p.quantity AS current_stock,p.cost_price,p.sell_price,p.unit FROM bill_items bi JOIN products p ON p.id=bi.product_id WHERE bi.bill_id=? ORDER BY bi.id""", (bill["id"],)).fetchall()
        if not items: return {"success":False,"error":"Cannot finalize an empty bill."}
        for item in items:
            if float(item["current_stock"]) < float(item["quantity"]):
                return {"success":False,"error":f"Cannot finalize: {item['name']} has only {item['current_stock']} {item['unit']} available, but {item['quantity']} requested."}
            if item["sell_price"] < item["cost_price"]:
                return {"success":False,"error":f"Sale blocked for {item['name']}: selling price is below cost."}
        subtotal=sum(int(x["taxable_amount"]) for x in items); cgst=sum(int(x["cgst"]) for x in items); sgst=sum(int(x["sgst"]) for x in items)
        discount=int(bill["discount"] or 0)
        if discount_rupees is not None:
            from tools.inventory import rupees_to_paise
            discount=rupees_to_paise(discount_rupees)
        gross=subtotal+cgst+sgst
        if discount<0 or discount>gross: return {"success":False,"error":"Invalid discount."}
        grand_total=gross-discount
        if mode=="KHATA":
            if not bill["customer_name"]: return {"success":False,"error":"A customer is required for Khata payment."}
            wallet=consume_wallet(db,bill["customer_name"],grand_total,bill["id"],"Purchase against bill")
            if not wallet.get("success"): return wallet
        for item in items:
            cur=db.execute("UPDATE products SET quantity=quantity-? WHERE id=? AND quantity>=?",(item["quantity"],item["product_id"],item["quantity"]))
            if cur.rowcount!=1: raise RuntimeError(f"Stock changed while finalizing {item['name']}. Please retry.")
        bill_number=f"INV-{bill['id']:06d}"
        now=datetime.now().isoformat(timespec="seconds")
        db.execute("""UPDATE bills SET bill_number=?,subtotal=?,discount=?,cgst=?,sgst=?,total_tax=?,grand_total=?,payment_mode=?,payment_reference=?,status='FINALIZED',idempotency_key=?,finalized_at=? WHERE id=?""",(bill_number,subtotal,discount,cgst,sgst,cgst+sgst,grand_total,mode,payment_reference,idem,now,bill["id"]))
        return _get_finalized_bill(db,bill["id"])


def _get_finalized_bill(db,bill_id):
    bill=db.execute("SELECT * FROM bills WHERE id=?",(bill_id,)).fetchone()
    rows=db.execute("""SELECT bi.*,p.name,p.brand,p.unit,p.pack_size,p.hsn_code FROM bill_items bi JOIN products p ON p.id=bi.product_id WHERE bi.bill_id=? ORDER BY bi.id""",(bill_id,)).fetchall()
    return {"success":True,"bill_id":bill["id"],"bill_number":bill["bill_number"],"customer_name":bill["customer_name"],"status":bill["status"],"payment_mode":bill["payment_mode"],"payment_reference":bill["payment_reference"],"subtotal":paise_to_rupees(bill["subtotal"]),"discount":paise_to_rupees(bill["discount"] or 0),"cgst":paise_to_rupees(bill["cgst"]),"sgst":paise_to_rupees(bill["sgst"]),"total_tax":paise_to_rupees(bill["total_tax"]),"grand_total":paise_to_rupees(bill["grand_total"]),"created_at":bill["created_at"],"finalized_at":bill["finalized_at"],"items":[{"product_id":r["product_id"],"name":r["name"],"quantity":r["quantity"],"unit":r["unit"],"unit_price":paise_to_rupees(r["unit_price"]),"gst_rate":r["gst_rate"],"taxable_amount":paise_to_rupees(r["taxable_amount"]),"cgst":paise_to_rupees(r["cgst"]),"sgst":paise_to_rupees(r["sgst"]),"total":paise_to_rupees(r["total"]),"hsn_code":r["hsn_code"]} for r in rows]}


def cancel_bill_draft(draft_key):
    with get_db() as db:
        bill=_get_draft(db,draft_key)
        if not bill:
            return {"success":True,"message":"No active draft."}
        db.execute("DELETE FROM bills WHERE id=? AND status='DRAFT'",(bill["id"],))
    return {"success":True,"message":"Bill draft cancelled."}
