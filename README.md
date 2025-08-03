# 💻 Computer Store Billing System

A desktop-based billing and invoicing system for a computer store built using **Python**, **Tkinter** for the GUI, and **SQLite** for persistent local storage.

> 📌 Built by [Koustab Dutta](https://github.com/Koustabdutta)

---

## 🧾 Features

- 🧍 Customer information capture (name, phone, email)
- 🧮 Product purchase with quantity selection
- 📦 Stock validation and update
- 🧾 Dynamic itemized bill generation
- 🗃️ Local database storage using SQLite
- 📋 Relational schema: customers, products, bills, and bill items

---

## 🛠️ Technologies Used

- Python 3.x
- Tkinter (built-in GUI framework)
- SQLite3 (local embedded database)

---

## 🗃️ Database Schema

The application auto-creates the following tables on first run:

- `customers(customer_id, name, phone, email)`
- `products(product_id, name, price, stock)`
- `bills(bill_id, customer_id, total_amount, bill_date)`
- `bill_items(item_id, bill_id, product_id, quantity, price)`

---

## 🚀 Getting Started

### 🔧 Prerequisites

Ensure you have Python 3.x installed:
```bash
python --version
