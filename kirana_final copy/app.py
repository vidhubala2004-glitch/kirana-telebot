import logging
import uuid
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from agents import Runner, OpenAIConversationsSession
from openai import AsyncOpenAI
from agent import kirana_agent, StoreContext
from config import validate_config, TELEGRAM_BOT_TOKEN, OPENAI_API_KEY
from database import init_db, mark_update_processed, get_db
from seed import seed_products
from tools import inventory, billing, khata, analytics, documents, market_pricing

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
logger=logging.getLogger("kirana-telegram")
sessions={}
workflows={}

IDLE="IDLE"; BILL_CUSTOMER="BILL_CUSTOMER"; BILL_PRODUCT="BILL_PRODUCT"; BILL_QUANTITY="BILL_QUANTITY"; BILL_MORE="BILL_MORE"; BILL_PAYMENT="BILL_PAYMENT"; BILL_UPI_REF="BILL_UPI_REF"; BILL_CONFIRM="BILL_CONFIRM"; STOCK_PRODUCT="STOCK_PRODUCT"; STOCK_RECEIVE_PRODUCT="STOCK_RECEIVE_PRODUCT"; STOCK_RECEIVE_QTY="STOCK_RECEIVE_QTY"; SEARCH_PRODUCT="SEARCH_PRODUCT"; KHATA_BALANCE="KHATA_BALANCE"; KHATA_DEPOSIT="KHATA_DEPOSIT"; PRICE_PRODUCT="PRICE_PRODUCT"; INVOICE_BILL="INVOICE_BILL"

def create_session(): return OpenAIConversationsSession(openai_client=AsyncOpenAI(api_key=OPENAI_API_KEY or "dummy-key"))
def get_user_session(chat_id):
    if chat_id not in sessions: sessions[chat_id]=create_session()
    return sessions[chat_id]

def fresh_workflow(chat_id):
    workflows[chat_id]={"state":IDLE,"customer_name":None,"draft_key":f"tg:{chat_id}","selected_product":None,"payment_mode":None,"payment_reference":None,"last_results":[]}
    return workflows[chat_id]
def get_workflow(chat_id):
    if chat_id not in workflows:
        fresh_workflow(chat_id)
    return workflows[chat_id]
def reset_workflow(chat_id): fresh_workflow(chat_id)

def main_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("🛒 New Bill",callback_data="bill:new")],[InlineKeyboardButton("📦 Inventory",callback_data="menu:inventory"),InlineKeyboardButton("📒 Khata",callback_data="menu:khata")],[InlineKeyboardButton("📊 Sales",callback_data="menu:sales"),InlineKeyboardButton("💰 Market Price",callback_data="menu:price")],[InlineKeyboardButton("📄 Documents",callback_data="menu:docs"),InlineKeyboardButton("❓ Help",callback_data="menu:help")]])
def inventory_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Search / Stock",callback_data="inv:search")],[InlineKeyboardButton("➕ Receive Stock",callback_data="inv:receive"),InlineKeyboardButton("⚠️ Low Stock",callback_data="inv:low")],[InlineKeyboardButton("⬅️ Main Menu",callback_data="main")]])
def khata_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("💰 Check Balance",callback_data="khata:balance")],[InlineKeyboardButton("➕ Deposit Money",callback_data="khata:deposit")],[InlineKeyboardButton("⬅️ Main Menu",callback_data="main")]])
def payment_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("💵 Cash",callback_data="pay:CASH"),InlineKeyboardButton("📱 GPay / UPI",callback_data="pay:UPI")],[InlineKeyboardButton("📒 Khata Wallet",callback_data="pay:KHATA")],[InlineKeyboardButton("⬅️ Back to Bill",callback_data="bill:view")]])
def confirm_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Confirm Sale",callback_data="bill:confirm")],[InlineKeyboardButton("❌ Cancel Bill",callback_data="bill:cancel")]])
def more_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("➕ Add Another Product",callback_data="bill:add")],[InlineKeyboardButton("💳 Choose Payment",callback_data="bill:payment")],[InlineKeyboardButton("❌ Cancel Bill",callback_data="bill:cancel")]])
def khata_result_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Check Another",callback_data="khata:balance")],[InlineKeyboardButton("➕ Deposit Money",callback_data="khata:deposit")],[InlineKeyboardButton("⬅️ Main Menu",callback_data="main")]])
def khata_deposit_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("📒 Check Balance",callback_data="khata:balance")],[InlineKeyboardButton("➕ Deposit More",callback_data="khata:deposit")],[InlineKeyboardButton("⬅️ Main Menu",callback_data="main")]])
def price_result_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Check Another",callback_data="menu:price")],[InlineKeyboardButton("⬅️ Main Menu",callback_data="main")]])
def inventory_receive_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("➕ Receive More",callback_data="inv:receive")],[InlineKeyboardButton("🔎 Search / Stock",callback_data="inv:search")],[InlineKeyboardButton("⬅️ Main Menu",callback_data="main")]])
def back_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Main Menu",callback_data="main")]])
def done_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("🛒 New Bill",callback_data="bill:new")],[InlineKeyboardButton("⬅️ Main Menu",callback_data="main")]])

def product_buttons(results,prefix="billproduct"):
    rows=[]
    for p in results[:8]: rows.append([InlineKeyboardButton(f"{p['name']} — ₹{p['sell_price']:.2f} | stock {p['quantity']}",callback_data=f"{prefix}:{p['id']}")])
    rows.append([InlineKeyboardButton("❌ Cancel",callback_data="main")])
    return InlineKeyboardMarkup(rows)

def format_bill(d):
    if not d.get("success"): return "❌ No active bill."
    lines=["🧾 *CURRENT BILL*",f"Customer: *{d.get('customer_name') or 'Walk-in Customer'}*","", "```"]
    for i in d.get("items",[]): lines.append(f"{i['name']}  x {i['quantity']}  ₹{i['unit_price']:.2f}  = ₹{i['total']:.2f}")
    lines += ["```",f"Subtotal: ₹{d['subtotal']:.2f}",f"GST: ₹{d['total_tax']:.2f}",f"Discount: ₹{d.get('discount',0):.2f}",f"*TOTAL: ₹{d['grand_total']:.2f}*"]
    return "\n".join(lines)

def sales_summary_text():
    r=analytics.daily_sales(); low=inventory.get_low_stock()
    mode=" | ".join(f"{p['mode']}: ₹{p['amount']:.2f}" for p in r.get("payments",[])) or "None"
    top=", ".join(f"{p['name']} ({p['quantity']})" for p in r.get("top_products",[])[:5]) or "No sales yet"
    return (f"📊 *Today's Sales*\n\nRevenue: ₹{r['total']:.2f}\nBills: {r['bill_count']}\n"
            f"GST collected: ₹{r['cgst']+r['sgst']:.2f}\nBy mode: {mode}\nTop items: {top}\n\n"
            f"Low stock: {len(low)}")

async def send_pdf(message,path):
    p=Path(path)
    if p.exists():
        with p.open("rb") as f: await message.reply_document(document=f,filename=p.name)

async def run_ai(chat_id,text):
    ctx=StoreContext(chat_id=chat_id)
    result=await Runner.run(kirana_agent,text,context=ctx,session=get_user_session(chat_id))
    return str(result.final_output or "Request completed."),ctx

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id=str(update.effective_chat.id); reset_workflow(chat_id)
    await update.message.reply_text("🏪 *Kirana Store Assistant*\n\nUse the buttons for real store operations. AI chat is also available by typing a question.",parse_mode="Markdown",reply_markup=main_menu())

async def help_cmd(update,context):
    await update.message.reply_text("🛒 New Bill → customer → product → quantity → payment → confirm → PDF\n\n📦 Inventory → search/check stock or receive stock\n\n📒 Khata → deposit money and use it for purchases\n\nYou can also type natural-language questions.",reply_markup=main_menu())

async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer(); chat_id=str(update.effective_chat.id); w=get_workflow(chat_id); data=q.data
    try:
        if data=="main": reset_workflow(chat_id); await q.message.reply_text("🏪 *Main Menu*",parse_mode="Markdown",reply_markup=main_menu()); return
        if data=="menu:help": await q.message.reply_text("Use *New Bill* for a complete sale. Stock is only deducted after final confirmation. Khata is a prepaid wallet.",parse_mode="Markdown",reply_markup=back_menu()); return
        if data=="menu:inventory": await q.message.reply_text("📦 *Inventory*",parse_mode="Markdown",reply_markup=inventory_menu()); return
        if data=="menu:khata": await q.message.reply_text("📒 *Khata Wallet*\n\nDeposit customer money before using Khata payment.",parse_mode="Markdown",reply_markup=khata_menu()); return
        if data=="menu:sales":
            await q.message.reply_text(sales_summary_text(),parse_mode="Markdown",reply_markup=back_menu()); return
        if data=="menu:price": w["state"]=PRICE_PRODUCT; await q.message.reply_text("💰 Send the product name to check its market price.",reply_markup=back_menu()); return
        if data=="menu:docs":
            await q.message.reply_text("📄 Documents\n\nGenerate an invoice by entering a finalized bill number/id, or use the weekly sales report through AI chat.",reply_markup=back_menu()); w["state"]=INVOICE_BILL; return

        if data=="bill:new":
            billing.cancel_bill_draft(w["draft_key"]); reset_workflow(chat_id); w=get_workflow(chat_id); w["state"]=BILL_CUSTOMER; await q.message.reply_text("🛒 *New Bill*\n\nEnter customer name. Type `walk-in` for a walk-in customer.",parse_mode="Markdown"); return
        if data=="bill:add": w["state"]=BILL_PRODUCT; await q.message.reply_text("Enter product name or SKU to add:"); return
        if data=="bill:view":
            d=billing.get_bill_draft(w["draft_key"]); await q.message.reply_text(format_bill(d),parse_mode="Markdown",reply_markup=more_menu() if d.get("items") else back_menu()); return
        if data=="bill:payment":
            d=billing.get_bill_draft(w["draft_key"])
            if not d.get("items"): await q.message.reply_text("❌ Add at least one product first.",reply_markup=more_menu()); return
            w["state"]=BILL_PAYMENT; await q.message.reply_text(format_bill(d)+"\n\n*Choose payment method:*",parse_mode="Markdown",reply_markup=payment_menu()); return
        if data=="bill:cancel":
            billing.cancel_bill_draft(w["draft_key"]); reset_workflow(chat_id); await q.message.reply_text("❌ Bill cancelled. Stock was not changed.",reply_markup=done_menu()); return
        if data.startswith("billproduct:"):
            pid=int(data.split(":")[1]); w["selected_product"]=pid; w["state"]=BILL_QUANTITY; p=inventory.get_stock(pid); await q.message.reply_text(f"*{p['name']}*\nAvailable: {p['quantity']} {p['unit']}\nPrice: ₹{p['sell_price']:.2f}\n\nEnter quantity:",parse_mode="Markdown"); return
        if data.startswith("pay:"):
            mode=data.split(":",1)[1]; w["payment_mode"]=mode
            if mode=="UPI": w["state"]=BILL_UPI_REF; await q.message.reply_text("📱 Enter UPI transaction/reference number (or type `skip`):"); return
            w["payment_reference"]=None; w["state"]=BILL_CONFIRM; d=billing.get_bill_draft(w["draft_key"]); await q.message.reply_text(format_bill(d)+f"\n\nPayment: *{mode}*\n\nConfirm sale?",parse_mode="Markdown",reply_markup=confirm_menu()); return
        if data=="bill:confirm":
            d=billing.get_bill_draft(w["draft_key"])
            if not d.get("items"): await q.message.reply_text("❌ Bill is empty.",reply_markup=more_menu()); return
            key=f"tg-{chat_id}-{d['bill_id']}-{uuid.uuid4().hex[:8]}"
            result=billing.finalize_bill(w["draft_key"],w["payment_mode"],w.get("payment_reference"),key)
            if not result.get("success"):
                await q.message.reply_text("❌ Sale not completed.\n\n"+result.get("error","Unknown error")+"\n\nNo stock was deducted if finalization failed.",reply_markup=more_menu()); return
            reset_workflow(chat_id); msg=await q.message.reply_text(f"✅ *Sale completed*\n\nInvoice: {result['bill_number']}\nAmount: ₹{result['grand_total']:.2f}\nPayment: {result['payment_mode']}\n\nStock updated and transaction saved.",parse_mode="Markdown",reply_markup=done_menu())
            pdf=documents.generate_invoice_pdf(result["bill_id"])
            if pdf.get("success"): await send_pdf(msg,pdf["file_path"])
            return

        if data=="inv:search": w["state"]=STOCK_PRODUCT; await q.message.reply_text("🔎 Enter product name/SKU:",reply_markup=inventory_menu()); return
        if data=="inv:receive": w["state"]=STOCK_RECEIVE_PRODUCT; await q.message.reply_text("➕ Enter the product name/SKU to receive stock:"); return
        if data=="inv:low":
            low=inventory.get_low_stock(); text="⚠️ *Low Stock*\n\n"+("\n".join(f"• {x['name']}: {x['quantity']} {x['unit']} (reorder {x['reorder_level']})" for x in low) if low else "No low-stock products."); await q.message.reply_text(text,parse_mode="Markdown",reply_markup=inventory_menu()); return
        if data.startswith("invproduct:"):
            p=inventory.get_stock(int(data.split(":")[1])); await q.message.reply_text(f"📦 *{p['name']}*\nStock: {p['quantity']} {p['unit']}\nSelling price: ₹{p['sell_price']:.2f}\nMRP: ₹{p['mrp']:.2f}",parse_mode="Markdown",reply_markup=inventory_menu()); return
        if data.startswith("receiveproduct:"):
            w["selected_product"]=int(data.split(":")[1]); w["state"]=STOCK_RECEIVE_QTY; p=inventory.get_stock(w["selected_product"]); await q.message.reply_text(f"➕ *{p['name']}*\nCurrent stock: {p['quantity']} {p['unit']}\n\nEnter quantity received:",parse_mode="Markdown"); return
        if data=="khata:balance": w["state"]=KHATA_BALANCE; await q.message.reply_text("Enter customer name:"); return
        if data=="khata:deposit": w["state"]=KHATA_DEPOSIT; await q.message.reply_text("Enter: `Customer ₹Amount`\nExample: `Rahul ₹1000`",parse_mode="Markdown"); return
    except Exception as e:
        logger.exception("button error"); await q.message.reply_text(f"❌ Error: {e}",reply_markup=back_menu())

async def message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id=str(update.effective_chat.id); text=(update.message.text or "").strip(); w=get_workflow(chat_id); state=w["state"]
    try:
        if not mark_update_processed(update.update_id): return
        if text.lower() in {"cancel","/cancel"}:
            billing.cancel_bill_draft(w["draft_key"]); reset_workflow(chat_id); await update.message.reply_text("❌ Current operation cancelled.",reply_markup=back_menu()); return
        if state==BILL_CUSTOMER:
            w["customer_name"]=None if text.lower() in {"walk-in","walkin","walk in"} else text
            billing.create_bill_draft(w["draft_key"],w["customer_name"]); w["state"]=BILL_PRODUCT; await update.message.reply_text(f"Customer: {w['customer_name'] or 'Walk-in Customer'}\n\nEnter product name or SKU:"); return
        if state==BILL_PRODUCT:
            results=inventory.search_products(text); w["last_results"]=results
            if not results: await update.message.reply_text("❌ Product not found. Try the name, brand or SKU again."); return
            await update.message.reply_text("Select the product:",reply_markup=product_buttons(results,"billproduct")); return
        if state==BILL_QUANTITY:
            try: qty=float(text.replace(",",""))
            except ValueError: await update.message.reply_text("❌ Enter a valid quantity, e.g. 3"); return
            result=billing.add_bill_item(w["draft_key"],w["selected_product"],qty)
            if not result.get("success"): await update.message.reply_text("❌ "+result.get("error","Could not add item.")); return
            w["state"]=BILL_MORE; await update.message.reply_text(format_bill(result),parse_mode="Markdown",reply_markup=more_menu()); return
        if state==BILL_UPI_REF:
            w["payment_reference"]=None if text.lower()=="skip" else text; w["state"]=BILL_CONFIRM; d=billing.get_bill_draft(w["draft_key"]); await update.message.reply_text(format_bill(d)+f"\n\nPayment: *UPI*\nReference: {w['payment_reference'] or 'Not provided'}\n\nConfirm sale?",parse_mode="Markdown",reply_markup=confirm_menu()); return
        if state==STOCK_PRODUCT:
            results=inventory.search_products(text)
            if not results: await update.message.reply_text("❌ Product not found."); return
            await update.message.reply_text("Select product:",reply_markup=product_buttons(results,"invproduct")); return
        if state==STOCK_RECEIVE_PRODUCT:
            results=inventory.search_products(text)
            if not results: await update.message.reply_text("❌ Product not found."); return
            await update.message.reply_text("Select product to receive:",reply_markup=product_buttons(results,"receiveproduct")); return
        if state==STOCK_RECEIVE_QTY:
            try: qty=float(text.replace(",",""))
            except ValueError: await update.message.reply_text("❌ Enter a valid quantity."); return
            r=inventory.receive_stock(w["selected_product"],qty); reset_workflow(chat_id); await update.message.reply_text(("✅ Stock received\n\n"+f"{r['name']}: +{r['added_quantity']}\nNew stock: {r['new_quantity']}" if r.get("success") else "❌ "+r.get("error","Failed")),reply_markup=inventory_receive_menu() if r.get("success") else inventory_menu()); return
        if state==KHATA_BALANCE:
            r=khata.get_customer_balance(text); reset_workflow(chat_id); await update.message.reply_text((f"💰 *{r['customer']}'s Balance*\nBalance: ₹{r['balance']:.2f}" if r.get("success") else "❌ "+r.get("error","Not found")),parse_mode="Markdown",reply_markup=khata_result_menu()); return
        if state==KHATA_DEPOSIT:
            parts=text.rsplit(" ",1)
            if len(parts)!=2: await update.message.reply_text("Use: Rahul ₹1000"); return
            amount=float(parts[1].replace("₹","").replace(",","")); r=khata.add_credit(parts[0],amount,"Telegram wallet deposit"); reset_workflow(chat_id); await update.message.reply_text((f"✅ Deposit recorded\nCustomer: {r['customer']}\nAdded: ₹{r['deposited']:.2f}\nWallet balance: ₹{r['balance']:.2f}" if r.get("success") else "❌ "+r.get("error","Failed")),reply_markup=khata_deposit_menu()); return
        if state==PRICE_PRODUCT:
            r=market_pricing.get_market_price_context(text); reset_workflow(chat_id); await update.message.reply_text(r.get("answer",r.get("error","Price unavailable.")),reply_markup=price_result_menu()); return
        if state==INVOICE_BILL:
            try: bill_id=int(text)
            except ValueError: await update.message.reply_text("Enter finalized bill ID, e.g. 12"); return
            r=documents.generate_invoice_pdf(bill_id); reset_workflow(chat_id)
            if r.get("success"): await update.message.reply_text("✅ Invoice generated."); await send_pdf(update.message,r["file_path"])
            else: await update.message.reply_text("❌ "+r.get("error","Invoice failed"),reply_markup=back_menu())
            return
        response,ctx=await run_ai(chat_id,text); await update.message.reply_text(response)
        for path in ctx.artifacts: await send_pdf(update.message,path)
    except Exception as e:
        logger.exception("message error"); await update.message.reply_text(f"❌ Error processing request: {e}",reply_markup=back_menu())

async def sales(update,context):
    await update.message.reply_text(sales_summary_text(),parse_mode="Markdown",reply_markup=back_menu())
async def stock(update,context):
    name=" ".join(context.args).strip()
    if not name: await update.message.reply_text("Use /stock Maggi",reply_markup=back_menu()); return
    results=inventory.search_products(name)
    await update.message.reply_text("\n".join(f"{p['name']}: {p['quantity']} {p['unit']} | ₹{p['sell_price']:.2f}" for p in results) or "Product not found.",reply_markup=back_menu())
async def khata_cmd(update,context):
    name=" ".join(context.args).strip()
    if not name: await update.message.reply_text("Use /khata Rahul",reply_markup=back_menu()); return
    r=khata.get_customer_balance(name); await update.message.reply_text((f"{r['customer']}: ₹{r['balance']:.2f}" if r.get("success") else r.get("error","Not found")),reply_markup=back_menu())


def main():
    validate_config(); init_db(); seed_products()
    if not TELEGRAM_BOT_TOKEN: raise RuntimeError("TELEGRAM_BOT_TOKEN missing")
    app=ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start)); app.add_handler(CommandHandler("help",help_cmd)); app.add_handler(CommandHandler("sales",sales)); app.add_handler(CommandHandler("stock",stock)); app.add_handler(CommandHandler("khata",khata_cmd)); app.add_handler(CommandHandler("new",start)); app.add_handler(CommandHandler("clear",start)); app.add_handler(CallbackQueryHandler(button)); app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message))
    print("Bot is running. Press Ctrl+C to stop."); app.run_polling(drop_pending_updates=True)

if __name__=="__main__": main()
