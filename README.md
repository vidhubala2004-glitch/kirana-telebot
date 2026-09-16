 kirana-telebot
Kirana AI Store Assistant is an AI-powered supermarket management system that enables shopkeepers to manage kirana store operations through a Telegram-based conversational interface. Built with Python, OpenAI Agents SDK, SQLite, and FastAPI, the system supports product search, inventory management, multi-item billing, GST calculation
# 🛒 Kirana AI Store Assistant

**AI-Powered Kirana Store Management System**

A conversational AI-powered supermarket management system that allows kirana shopkeepers to manage their daily store operations through **Telegram** using natural-language commands.

The system combines **Telegram, OpenAI Agents SDK, Python, SQLite, and FastAPI** to automate product management, inventory tracking, billing, payments, customer Khata management, invoice generation, and sales analysis.

---

## 🚀 Project Overview

Small kirana stores often manage billing, inventory, customer credit, and sales records manually. This project provides an AI-powered solution where the shopkeeper can simply communicate with the system through Telegram.

Instead of navigating multiple screens, the shopkeeper can send natural-language requests such as:

* Check product stock
* Add new products
* Receive new stock
* Create a bill
* Add multiple products to a bill
* Check low-stock products
* Record payments
* Manage customer Khata
* Check daily sales
* Generate invoices
* Generate sales-analysis reports

The AI agent interprets the request and uses backend business tools to perform the required operation.

---

## ✨ Key Features

### 🤖 AI Conversational Assistant

* Telegram-based AI store assistant
* Understands natural-language commands
* Uses backend tools to perform real business operations

### 📦 Product & Inventory Management

* Add and manage products
* Receive new stock
* Check current inventory
* Track low-stock products
* Configure reorder levels
* Validate stock before completing a sale

### 🧾 Smart Billing

* Create new bills through Telegram
* Add multiple products to a single bill
* Modify bills while they are being created
* Automatic quantity and price calculation
* Automatic GST calculation
* Final stock validation before sale confirmation

### 💳 Payment Management

Supports:

* Cash
* UPI
* Khata Wallet

Payments and transactions are stored in the database.

### 📒 Customer Khata Management

Khata is implemented as a prepaid customer wallet.

Example:

```text
Deposit ₹1000
Balance = ₹1000

Purchase ₹300
Balance = ₹700

Purchase ₹500
Balance = ₹200
```

The system maintains customer balances and transactions.

### 📄 PDF Invoice Generation

After completing a sale, the system automatically:

1. Creates the bill
2. Records the transaction
3. Updates inventory
4. Generates a PDF invoice
5. Sends the invoice through Telegram

### 📊 Sales Analysis

The system can generate sales-analysis reports containing:

* Sales information
* Business insights
* Charts
* Weekly analysis

Reports can be generated as **PPTX presentations**.

---

## 🔄 Core Workflow

```text
             ┌─────────────────┐
             │    Shopkeeper   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │    Telegram     │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   AI Agent      │
             │ OpenAI Agents   │
             │      SDK        │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Backend Tools   │
             └────────┬────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     Inventory      Billing     Khata
          │           │           │
          └───────────┼───────────┘
                      ▼
             ┌─────────────────┐
             │ SQLite Database │
             └────────┬────────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
      PDF Invoice       Sales Analysis
                         PPTX Report
```

---

## 🧾 Billing Workflow

The standard billing workflow is:

```text
/start
   ↓
New Bill
   ↓
Select Customer
   ↓
Select Product
   ↓
Enter Quantity
   ↓
Add Another Product?
   ├── Yes → Add Product
   └── No
        ↓
Choose Payment Method
        ↓
Cash / UPI / Khata Wallet
        ↓
Confirm Sale
        ↓
Recheck Stock
        ↓
Deduct Stock Atomically
        ↓
Store Transaction
        ↓
Generate PDF Invoice
        ↓
Send Invoice to Telegram
```

The system rechecks stock before finalizing the transaction and deducts inventory atomically.

---

## 🗃️ Dataset

The project uses a product dataset containing approximately **500 Indian grocery and FMCG products**.

The dataset was prepared using:

* Kaggle grocery datasets
* Blinkit product listings as references

Product information includes:

* Product name
* Category
* Unit
* Price
* Stock quantity
* Reorder level
* GST information

---

## 🛠️ Technology Stack

| Technology        | Purpose                          |
| ----------------- | -------------------------------- |
| Python            | Backend development              |
| Telegram Bot API  | Conversational interface         |
| OpenAI Agents SDK | AI agent and tool-based workflow |
| SQLite            | Persistent database              |
| FastAPI           | Web/API layer                    |
| PDF Generation    | Invoice generation               |
| PPTX              | Sales-analysis reports           |
| Kaggle Dataset    | Grocery product references       |
| Blinkit Listings  | Product reference data           |

---

## 📁 Project Structure

```text
kirana_final/
│
├── app.py
├── run.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│   └── kirana.db
│
├── tests/
│   ├── test_core_workflow.py
│   └── test_khata.py
│
└── ...
```

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd kirana_final
```

### 2. Create a Virtual Environment

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create your `.env` file from the template:

```bash
cp .env.example .env
```

Add your required API keys and Telegram configuration.

**Never commit your real `.env` file to GitHub.**

---

## ▶️ Run the Application

### Start Telegram Bot

```bash
python app.py
```

### Start Web UI and Telegram Bot

```bash
python run.py
```

The web UI runs at:

```text
http://localhost:8000
```

The project requires only **one Telegram polling process** for a bot token. Running a second polling process with the same token can cause a Telegram `409 Conflict` error.

---

## 🗄️ Database

The application uses **SQLite** for persistent storage.

The database is automatically created at:

```text
data/kirana.db
```

It stores business information such as:

* Products
* Inventory
* Sales
* Customers
* Payments
* Khata transactions
* Bill information

The application also supports lightweight database migrations for newer fields.

---

## 🧪 Testing

Run the project tests using:

```bash
python -m pytest tests/test_core_workflow.py test_khata.py
```

The existing project README documents tests for the core workflow and Khata functionality.

---

## 🔐 Security

* API keys are stored using environment variables
* `.env` should not be committed to GitHub
* Stock is validated before completing sales
* Database transactions are used for persistent business records

---

## 🎯 Project Objective

The objective of this project is to build a practical **AI-powered business assistant for kirana stores** that reduces manual work and makes everyday store management faster and easier.

The system demonstrates how **conversational AI + agent tools + databases + business automation** can be combined into a real-world application.

---

## 🔮 Future Enhancements

* 📱 Dedicated mobile application
* 📈 Real-time business dashboard
* 🧠 AI-based demand forecasting
* 📦 Automatic stock-reorder recommendations
* 👥 Customer purchase analytics
* 💰 Profit and expense tracking
* 🔔 Automated low-stock notifications
* ☁️ Cloud database integration
* 🔐 Role-based access for multiple employees
  SCREEN SHOT:
<img width="1440" height="900" alt="Screenshot 2026-09-15 at 9 33 12 AM" src="https://github.com/user-attachments/assets/71ef3620-340e-493b-b0c0-50ae1a10a322" />

<img width="1440" height="900" alt="Screenshot 2026-09-15 at 9 33 21 AM" src="https://github.com/user-attachments/assets/1add8755-6a84-47f2-bfc0-97ae5ba30766" />
<img width="1440" height="900" alt="Screenshot 2026-09-15 at 9 33 03 AM" src="https://github.com/user-attachments/assets/a24806c0-48ac-4013-ae9b-0d12c9f2b066" />




LINK :https://t.me/Kirana007_bot
