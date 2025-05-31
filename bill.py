import sqlite3
from tkinter import *
from tkinter import messagebox

# Connect to SQLite database
conn = sqlite3.connect("computer_store.db")
cur = conn.cursor()

# Create tables
def setup_database():
    cur.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, phone TEXT, email TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS bills (
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER, total_amount REAL,
        bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS bill_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL NOT NULL,
        FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id))''')

    conn.commit()

setup_database()

# GUI setup
root = Tk()
root.title("Computer Store Billing System")
root.geometry("600x500")

# Customer Information Frame
customer_frame = LabelFrame(root, text="Customer Information", padx=10, pady=10)
customer_frame.pack(fill="x")

Label(customer_frame, text="Name").grid(row=0, column=0)
Label(customer_frame, text="Phone").grid(row=0, column=2)
Label(customer_frame, text="Email").grid(row=0, column=4)

name_entry = Entry(customer_frame)
phone_entry = Entry(customer_frame)
email_entry = Entry(customer_frame)

name_entry.grid(row=0, column=1)
phone_entry.grid(row=0, column=3)
email_entry.grid(row=0, column=5)

# Product Entry Frame
product_frame = LabelFrame(root, text="Product Purchase", padx=10, pady=10)
product_frame.pack(fill="x")

Label(product_frame, text="Product ID").grid(row=0, column=0)
Label(product_frame, text="Quantity").grid(row=0, column=2)

pid_entry = Entry(product_frame)
qty_entry = Entry(product_frame)

pid_entry.grid(row=0, column=1)
qty_entry.grid(row=0, column=3)

items = []

# Add item function
def add_item():
    pid = pid_entry.get()
    qty = qty_entry.get()
    try:
        qty = int(qty)
        cur.execute("SELECT name, price, stock FROM products WHERE product_id=?", (pid,))
        result = cur.fetchone()
        if result:
            name, price, stock = result
            if qty > stock:
                messagebox.showerror("Stock Error", f"Only {stock} units in stock.")
                return
            items.append((int(pid), name, price, qty))
            display.insert(END, f"{name} x{qty} = ₹{price*qty}\n")
        else:
            messagebox.showerror("Error", "Product ID not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

Button(product_frame, text="Add", command=add_item).grid(row=0, column=4)

# Display area
display = Text(root, height=10, width=60)
display.pack(pady=10)

# Generate bill
def generate_bill():
    cname = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if not items or not cname:
        messagebox.showerror("Missing Info", "Enter customer info and at least one product.")
        return

    cur.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)", (cname, phone, email))
    cid = cur.lastrowid

    total = sum([price * qty for _, _, price, qty in items])
    cur.execute("INSERT INTO bills (customer_id, total_amount) VALUES (?, ?)", (cid, total))
    bid = cur.lastrowid

    for pid, _, price, qty in items:
        cur.execute("INSERT INTO bill_items (bill_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (bid, pid, qty, price))
        cur.execute("UPDATE products SET stock = stock - ? WHERE product_id = ?", (qty, pid))

    conn.commit()
    display.insert(END, f"\n--- BILL GENERATED ---\nBill ID: {bid}\nTotal: ₹{total:.2f}\nThank you!\n")

Button(root, text="Generate Bill", command=generate_bill).pack(pady=5)

root.mainloop()
