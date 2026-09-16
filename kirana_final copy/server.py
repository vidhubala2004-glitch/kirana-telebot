import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

from openai import AsyncOpenAI
from agents import Runner, OpenAIConversationsSession
from agent import kirana_agent, StoreContext
from config import BASE_DIR, GENERATED_DIR, OPENAI_API_KEY, validate_config
from database import init_db, get_db
from seed import seed_products
from tools import billing, analytics, inventory, khata, market_pricing


def _extract_product_name(text: str) -> str:
    phrase = text.strip()
    for prefix in [
        "do we have ", "is ", "are ", "stock of ", "availability of ", "check ", "search ", "find ",
        "what is the price of ", "price of ", "mrp of ", "current price of ", "market price of ",
        "how much is ", "how much are ", "what is the market price of ", "what is the mrp of "
    ]:
        if phrase.lower().startswith(prefix):
            phrase = phrase[len(prefix):].strip(" ?.")
            break

    if " in stock" in phrase.lower():
        phrase = phrase.lower().replace(" in stock", "").strip()
    if " available" in phrase.lower():
        phrase = phrase.lower().replace(" available", "").strip()
    if phrase.lower().endswith(" price"):
        phrase = phrase[:-len(" price")].strip()
    return phrase.strip()


def _parse_product_list(text: str):
    cleaned = text.strip().strip("?.,! ")
    if not cleaned:
        return []

    lowered = cleaned.lower()
    for prefix in ["total of ", "sum of ", "total for ", "what is total of ", "what is the total of ", "total "]:
        if lowered.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break

    separators = [",", " and ", " & ", " + ", "/", ";"]
    for sep in separators:
        if sep in cleaned.lower():
            cleaned = cleaned.replace(" and ", ",").replace(" & ", ",").replace(" + ", ",").replace("/", ",").replace(";", ",")
            parts = [p.strip() for p in cleaned.split(",") if p.strip()]
            normalized = []
            for p in parts:
                candidate = p.strip().strip("?.,! ")
                if candidate and candidate.lower() not in {"total", "price", "mrp"}:
                    normalized.append(candidate)
            if normalized:
                return normalized

    if " " in cleaned and cleaned.lower() not in {"total", "price", "mrp"}:
        cleaned = cleaned.replace(" and ", ",").replace(" & ", ",").replace(" + ", ",")
        if "," in cleaned:
            return [p.strip() for p in cleaned.split(",") if p.strip()]

    return [cleaned] if cleaned and cleaned.lower() not in {"total", "price", "mrp"} else []


async def _compute_total_for_products(product_names):
    if not product_names:
        return None

    prices = []
    details = []
    for product_name in product_names:
        product_name = product_name.strip()
        if not product_name:
            continue

        matches = inventory.search_products(product_name)
        if matches:
            product = matches[0]
            sell_price = float(product["sell_price"])
            prices.append(sell_price)
            details.append(f"{product['name']}: ₹{sell_price:.2f}")
            continue

        market = market_pricing.get_market_price_context(product_name)
        if market.get("success"):
            market_price = float(market.get("market", {}).get("market_mrp", 0.0) or 0.0)
            if market_price:
                prices.append(market_price)
                details.append(f"{product_name}: ₹{market_price:.2f} (market)")

    if not prices:
        return None

    return {
        "items": details,
        "total": sum(prices),
    }


async def fallback_chat_response(chat_id: str, user_text: str) -> str:
    text = (user_text or "").strip()
    if not text:
        return "Please ask a product, stock, billing, or pricing question."

    lower_text = text.lower()

    product_names = _parse_product_list(text)
    if len(product_names) > 1 and ("total" in lower_text or "sum" in lower_text):
        total_data = await _compute_total_for_products(product_names)
        if total_data:
            joined = "; ".join(total_data["items"])
            return f"{joined}. Total: ₹{total_data['total']:.2f}."

    if lower_text in {"oil price", "price", "oil", "oil prices", "butter price", "atta price", "rice price", "sugar price", "dal price"} or any(k in lower_text for k in ["market price", "mrp", "price", "price of", "current price", "latest price", "how much is", "what is the price of", "what is the market price of"]):
        candidate = _extract_product_name(text)
        if not candidate:
            candidate = text.replace("price", "").strip(" ?.")
        if not candidate:
            candidate = "atta"
        market = market_pricing.get_market_price_context(candidate)
        if market.get("success"):
            return market.get("answer", "I could not determine a pricing answer right now.")

    sales_summary_keywords = [
        "sales today",
        "today sales",
        "revenue today",
        "today revenue",
        "sales on day",
        "how much sales",
        "how many bills today",
        "bills today",
        "today's sales",
        "day sales",
        "sales of the day",
    ]
    if any(k in lower_text for k in sales_summary_keywords) or ("revenue" in lower_text and "today" in lower_text) or ("sales" in lower_text and "low stock" in lower_text):
        today_sales = analytics.daily_sales()
        low = inventory.get_low_stock()
        low_text = "No products are currently below their reorder level." if not low else ", ".join(f"{item.get('name')} ({item.get('quantity')} left)" for item in low[:5])
        return (
            f"Sales today: ₹{today_sales.get('total', 0):.2f}. "
            f"Revenue today: ₹{today_sales.get('total', 0):.2f}. "
            f"Bills today: {today_sales.get('bill_count', 0)}. "
            f"Low stock: {len(low)} item(s). {low_text}."
        )

    if any(k in lower_text for k in ["low stock", "stock alert", "which items are low", "low inventory"]):
        low = inventory.get_low_stock()
        if not low:
            return "No products are currently below their reorder level."
        items = ", ".join(f"{item.get('name')} ({item.get('quantity')} left)" for item in low[:5])
        return f"Low stock items: {items}."

    if any(k in lower_text for k in ["summary", "dashboard", "store status", "today sales", "revenue"]):
        summary = await get_store_summary(chat_id)
        if summary.get("success"):
            return (
                f"Revenue today: ₹{summary.get('today_revenue', 0):.2f}. "
                f"Bills: {summary.get('today_bills', 0)}. "
                f"Low stock: {summary.get('low_stock_count', 0)} items."
            )

    if any(k in lower_text for k in ["bill", "invoice", "draft"]):
        draft = billing.get_bill_draft(chat_id)
        if draft.get("success"):
            items = draft.get("items", [])
            if not items:
                return "There is no active bill draft right now."
            summary = ", ".join(f"{item['name']} x {item['quantity']}" for item in items[:5])
            return f"Your current draft includes: {summary}. Grand total: ₹{draft.get('grand_total', 0):.2f}."
        return "There is no active bill draft right now."

    if any(k in lower_text for k in ["do we have", "is ", "are ", "stock of", "availability of", "quantity", "available", "in stock"]):
        query = _extract_product_name(text)
        if not query:
            query = text.replace("?", "").strip()
        matches = inventory.search_products(query)
        if not matches:
            return f"I could not find {query!r} in the store database."
        product = matches[0]
        return (
            f"I found {product['name']} in your database. "
            f"Available stock: {product['quantity']} {product['unit']}. "
            f"Selling price: ₹{product['sell_price']:.2f}. MRP: ₹{product['mrp']:.2f}."
        )

    if len(product_names) > 1:
        total_data = await _compute_total_for_products(product_names)
        if total_data:
            joined = "; ".join(total_data["items"])
            return f"{joined}. Total: ₹{total_data['total']:.2f}."

    if lower_text in {"oil", "butter", "atta", "rice", "sugar", "dal"}:
        product = lower_text
        market = market_pricing.get_market_price_context(product)
        if market.get("success"):
            return market.get("answer", f"I could not determine a pricing answer for {product} right now.")

    if any(k in lower_text for k in ["customer", "khata", "credit", "payment"]):
        try:
            with get_db() as db:
                total = db.execute(
                    """
                    SELECT COALESCE(SUM(CASE WHEN transaction_type='CREDIT' THEN amount ELSE 0 END),0) -
                           COALESCE(SUM(CASE WHEN transaction_type='PAYMENT' THEN amount ELSE 0 END),0)
                    FROM khata_transactions
                    """
                ).fetchone()[0]
            return f"Outstanding khata balance: ₹{(total / 100.0):.2f}."
        except Exception:
            return "I could not access khata data right now."

    if any(k in lower_text for k in ["hello", "hi", "namaste", "hey", "namaste!", "namaskar", "नमस्ते", "नमस्कार", "हेलो"]):
        return "Hello! Namaste! I can help with store inventory, pricing checks, bills, khata, and sales. Ask me anything about your store."

    summary = await get_store_summary(chat_id)
    if summary.get("success"):
        return (
            f"Your store is performing well: revenue today ₹{summary.get('today_revenue', 0):.2f}, "
            f"with {summary.get('low_stock_count', 0)} low-stock items and {summary.get('today_bills', 0)} bills."
        )
    return "I’m ready to help with stock, pricing, billing, and sales. Ask a clear question and I’ll answer from your store data and market check."

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("kirana-server")

# Active web sessions mapping chat_id -> OpenAIConversationsSession
web_sessions: dict[str, OpenAIConversationsSession] = {}


def create_session() -> OpenAIConversationsSession:
    client = AsyncOpenAI(api_key=OPENAI_API_KEY or "dummy-key")
    return OpenAIConversationsSession(openai_client=client)


def get_session(chat_id: str) -> OpenAIConversationsSession:
    if chat_id not in web_sessions:
        web_sessions[chat_id] = create_session()
    return web_sessions[chat_id]


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Database & Seeding Products for Web App...")
    init_db()
    seed_products()
    yield

app = FastAPI(
    title="Kirana AI Store Assistant API",
    description="Web Q&A and Store Management Interface",
    version="1.0.0",
    lifespan=lifespan,
)

# Static file serving for generated artifacts (PDFs, PPTXs)
app.mount("/generated", StaticFiles(directory=str(GENERATED_DIR)), name="generated")

# Serve frontend static assets (CSS, JS)
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    chat_id: Optional[str] = "web-default-session"
    message: str


@app.get("/")
async def root():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Web UI index.html not found.")
    return FileResponse(index_path)


@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    chat_id = (payload.chat_id or "web-default-session").strip()
    user_text = payload.message.strip()

    if not user_text:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    session = get_session(chat_id)
    store_context = StoreContext(chat_id=chat_id)

    try:
        if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("YOUR_"):
            response_text = await fallback_chat_response(chat_id, user_text)
        else:
            run_result = await Runner.run(
                kirana_agent,
                user_text,
                context=store_context,
                session=session,
            )

            response_text = (
                str(run_result.final_output)
                if run_result.final_output
                else "Request processed successfully."
            )

        formatted_artifacts = []
        for artifact_path in store_context.artifacts:
            path = Path(artifact_path)
            if path.exists():
                try:
                    rel_path = path.relative_to(GENERATED_DIR)
                    url = f"/generated/{rel_path.as_posix()}"
                except ValueError:
                    url = f"/generated/{path.name}"

                file_type = "pdf" if path.suffix.lower() == ".pdf" else ("pptx" if path.suffix.lower() == ".pptx" else "file")
                formatted_artifacts.append({
                    "name": path.name,
                    "url": url,
                    "type": file_type,
                })

        return {
            "success": True,
            "chat_id": chat_id,
            "response": response_text,
            "artifacts": formatted_artifacts,
        }

    except Exception as e:
        logger.error(f"Error handling web chat request for {chat_id}: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "response": f"❌ Error processing request: {str(e)}",
                "artifacts": [],
            },
        )


@app.get("/api/session/{chat_id}")
async def get_session_info(chat_id: str):
    draft = billing.get_bill_draft(chat_id)
    return {
        "success": True,
        "chat_id": chat_id,
        "draft": draft if draft.get("success") else None,
    }


@app.post("/api/session/{chat_id}/reset")
async def reset_session(chat_id: str):
    web_sessions[chat_id] = create_session()
    with get_db() as db:
        db.execute(
            "DELETE FROM bills WHERE draft_key = ? AND status = 'DRAFT'",
            (chat_id,),
        )
    return {
        "success": True,
        "message": f"Session and bill draft reset for {chat_id}.",
    }


@app.get("/api/store/summary")
async def get_store_summary(chat_id: Optional[str] = "web-default-session"):
    try:
        today_sales = analytics.daily_sales()
        low_stock = inventory.get_low_stock()
        draft = billing.get_bill_draft(chat_id)

        with get_db() as db:
            customer_count = db.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
            total_khata_row = db.execute(
                """
                SELECT 
                    (SELECT COALESCE(SUM(amount), 0) FROM khata_transactions WHERE transaction_type IN ('DEPOSIT','REFUND')) -
                    (SELECT COALESCE(SUM(amount), 0) FROM khata_transactions WHERE transaction_type = 'PURCHASE')
                """
            ).fetchone()
            total_khata = (total_khata_row[0] / 100.0) if total_khata_row and total_khata_row[0] else 0.0

        return {
            "success": True,
            "today_revenue": today_sales.get("total", 0.0),
            "today_bills": today_sales.get("bill_count", 0),
            "low_stock_count": len(low_stock),
            "low_stock_items": low_stock[:5],
            "total_khata_outstanding": total_khata,
            "active_customers": customer_count,
            "active_draft": draft if draft.get("success") else None,
        }
    except Exception as e:
        logger.error(f"Error fetching store summary: {e}")
        return {"success": False, "error": str(e)}


@app.get("/api/market-price")
async def market_price_endpoint(product: str = ""):
    if not product or not product.strip():
        raise HTTPException(status_code=400, detail="Product name is required.")
    return market_pricing.get_market_price_context(product)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
