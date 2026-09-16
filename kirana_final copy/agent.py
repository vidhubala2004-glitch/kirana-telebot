from dataclasses import dataclass, field
from pathlib import Path
from agents import Agent, Runner, function_tool, RunContextWrapper
from tools import inventory,billing,khata,analytics,documents,preferences,market_pricing
from config import BASE_DIR

@dataclass
class StoreContext:
    chat_id: str
    artifacts: list[str] = field(default_factory=list)

def load_skills():
    d=BASE_DIR/"skills"; return "\n\n".join(f"--- SKILL: {p.stem.upper()} ---\n{p.read_text(encoding='utf-8')}" for p in sorted(d.glob("*.md")))

@function_tool
def search_products(query:str): return inventory.search_products(query)
@function_tool
def get_stock(product_id:int): return inventory.get_stock(product_id)
@function_tool
def receive_stock(product_id:int,quantity:float,cost_price_rupees:float|None=None,mrp_rupees:float|None=None): return inventory.receive_stock(product_id,quantity,cost_price_rupees,mrp_rupees)
@function_tool
def get_low_stock(): return inventory.get_low_stock()
@function_tool
def add_product(name:str,brand:str,sku:str,unit:str,pack_size:str,cost_price_rupees:float,sell_price_rupees:float,mrp_rupees:float,quantity:float,reorder_level:float,hsn_code:str,gst_rate:float,loose:bool=False): return inventory.add_product(name,brand,sku,unit,pack_size,cost_price_rupees,sell_price_rupees,mrp_rupees,quantity,reorder_level,hsn_code,gst_rate,loose)

@function_tool
def create_bill_draft(ctx:RunContextWrapper[StoreContext],customer_name:str|None=None): return billing.create_bill_draft(ctx.context.chat_id,customer_name)
@function_tool
def add_bill_item(ctx:RunContextWrapper[StoreContext],product_id:int,quantity:float): return billing.add_bill_item(ctx.context.chat_id,product_id,quantity)
@function_tool
def remove_bill_item(ctx:RunContextWrapper[StoreContext],product_id:int): return billing.remove_bill_item(ctx.context.chat_id,product_id)
@function_tool
def update_bill_item(ctx:RunContextWrapper[StoreContext],product_id:int,quantity:float): return billing.update_bill_item(ctx.context.chat_id,product_id,quantity)
@function_tool
def get_bill_draft(ctx:RunContextWrapper[StoreContext]): return billing.get_bill_draft(ctx.context.chat_id)
@function_tool
def set_bill_discount(ctx:RunContextWrapper[StoreContext],discount_rupees:float): return billing.set_bill_discount(ctx.context.chat_id,discount_rupees)
@function_tool
def finalize_bill(ctx:RunContextWrapper[StoreContext],payment_mode:str,payment_reference:str|None=None,idempotency_key:str|None=None):
    result=billing.finalize_bill(ctx.context.chat_id,payment_mode,payment_reference,idempotency_key)
    if result.get("success") and result.get("bill_id"):
        pdf=documents.generate_invoice_pdf(result["bill_id"])
        if pdf.get("success"):
            ctx.context.artifacts.append(pdf["file_path"]); result["invoice_pdf_path"]=pdf["file_path"]
    return result

@function_tool
def get_customer_balance(customer_name:str): return khata.get_customer_balance(customer_name)
@function_tool
def add_credit(customer_name:str,amount_rupees:float,description:str="Wallet deposit"): return khata.add_credit(customer_name,amount_rupees,description)
@function_tool
def record_payment(customer_name:str,amount_rupees:float,description:str="Wallet deposit"): return khata.record_payment(customer_name,amount_rupees,description)
@function_tool
def set_preference(key:str,value:str): return preferences.set_preference(key,value)
@function_tool
def get_preference(key:str): return preferences.get_preference(key)
@function_tool
def list_preferences(): return preferences.list_preferences()
@function_tool
def daily_sales(date_string:str|None=None): return analytics.daily_sales(date_string)
@function_tool
def weekly_sales(): return analytics.weekly_sales()
@function_tool
def generate_sales_deck(ctx:RunContextWrapper[StoreContext]):
    r=documents.generate_sales_deck()
    if r.get("success"): ctx.context.artifacts.append(r["file_path"])
    return r
@function_tool
def generate_invoice_pdf(ctx:RunContextWrapper[StoreContext],bill_id:int):
    r=documents.generate_invoice_pdf(bill_id)
    if r.get("success"): ctx.context.artifacts.append(r["file_path"])
    return r
@function_tool
def get_market_price_context(product_name:str): return market_pricing.get_market_price_context(product_name)

SYSTEM_PROMPT=f"""You are the Kirana Store AI Assistant. Use the database as the source of truth.
Rules:
1. Never invent stock, prices, GST, HSN, totals or wallet balances.
2. Search products before using a product ID.
3. Draft billing never deducts stock. Finalization re-checks stock and deducts atomically.
4. Never oversell.
5. Payment modes are CASH, UPI and KHATA. KHATA is a prepaid wallet: deposits add balance and purchases consume balance.
6. A KHATA purchase must fail if the wallet balance is insufficient.
7. Successful finalization generates a PDF invoice.
8. Weekly analysis requests should use generate_sales_deck.
9. If a request is ambiguous — several products match, a quantity or payment method is missing, or details conflict — ask one short clarifying question before acting. Never silently guess.
10. Answer in short, plain, practical shopkeeper English.

{load_skills()}"""

kirana_agent=Agent[StoreContext](name="KiranaStoreAgent",instructions=SYSTEM_PROMPT,tools=[search_products,get_stock,receive_stock,get_low_stock,add_product,create_bill_draft,add_bill_item,remove_bill_item,update_bill_item,get_bill_draft,set_bill_discount,finalize_bill,get_customer_balance,add_credit,record_payment,set_preference,get_preference,list_preferences,daily_sales,weekly_sales,generate_sales_deck,generate_invoice_pdf,get_market_price_context])
