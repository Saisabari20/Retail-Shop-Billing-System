from tkinter import *
from tkinter import messagebox
import sqlite3

product_data = [
    ["Product_name", "Price", "Quantity"],
    ["Laptop", 60000, 10],
    ["Smartphone", 15000, 20],
    ["Keyboard", 700, 50],
    ["Mouse", 400, 80],
    ["Monitor", 12000, 15],
    ["Charger", 500, 40],
    ["Pendrive", 300, 100],
    ["Speaker", 2000, 30],
    ["Router", 1800, 25],
    ["Tablet", 25000, 12]
]

conn = sqlite3.connect("Retail.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS retail_shop(
        Name TEXT PRIMARY KEY,
        Price FLOAT,
        Quantity INTEGER
    )
''')

for row in product_data[1:]:
    cursor.execute('INSERT OR IGNORE INTO retail_shop (Name, Price, Quantity) VALUES (?, ?, ?)', row)

conn.commit()

cart = []

def purchase_item():
    name = name_entry.get().strip()
    qty = qty_entry.get().strip()

    if name and qty:
        try:
            qty = int(qty)
            cursor.execute("SELECT Price, Quantity FROM retail_shop WHERE Name = ?", (name,))
            result = cursor.fetchone()

            if result:
                price, available_qty = result
                if qty <= available_qty:
                    item = {
                        "name": name,
                        "qty": qty,
                        "price": price,
                        "total": price * qty
                    }
                    cart.append(item)

                    new_qty = available_qty - qty
                    cursor.execute("UPDATE retail_shop SET Quantity = ? WHERE Name = ?", (new_qty, name))
                    conn.commit()

                    messagebox.showinfo("Success", "Item added to cart.")
                    name_entry.delete(0, END)
                    qty_entry.delete(0, END)
                else:
                    messagebox.showerror("Stock Error", f"Only {available_qty} available.")
            else:
                messagebox.showerror("Product Error", "Item not found.")
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a number.")
    else:
        messagebox.showerror("Input Error", "Please enter both product name and quantity.")

def view_items():
    display.delete('1.0', END)
    display.insert(END, "Available Stock:\n")

    cursor.execute("SELECT Name, Price, Quantity FROM retail_shop")
    rows = cursor.fetchall()

    for row in rows:
        display.insert(END, f"{row[0]}: ₹{row[1]} (Qty: {row[2]})\n")

    display.insert(END, "\nItems in Cart:\n")
    if not cart:
        display.insert(END, "Cart is empty!\n")
    else:
        for idx, item in enumerate(cart, 1):
            display.insert(END, f"{idx}. {item['name']} - ₹{item['price']} x {item['qty']} = ₹{item['total']}\n")

def print_bill():
    display.delete('1.0', END)
    if not cart:
        display.insert(END, "Cart is empty. Add items first.\n")
        return

    display.insert(END, "Customer Bill\n------------------\n")
    total_amount = 0
    for idx, item in enumerate(cart, 1):
        display.insert(END, f"{idx}. {item['name']} - ₹{item['price']} x {item['qty']} = ₹{item['total']}\n")
        total_amount += item['total']
    display.insert(END, "------------------\n")
    display.insert(END, f"Total Amount: ₹{total_amount:.2f}\n")
    display.insert(END, "Thank you for shopping!\n")

    cart.clear()

root = Tk()
root.title("Retail Shop Billing System")
root.geometry("400x500")

Label(root, text="Product Name").pack()
name_entry = Entry(root)
name_entry.pack()

Label(root, text="Quantity").pack()
qty_entry = Entry(root)
qty_entry.pack()

Button(root, text="Purchase Item", command=purchase_item).pack(pady=5)
Button(root, text="View Stock & Cart", command=view_items).pack(pady=5)
Button(root, text="Print Bill", command=print_bill).pack(pady=5)

Label(root, text="-----------------------------").pack()
Label(root, text="Output:").pack()

display = Text(root, height=15, width=45)
display.pack()

root.mainloop()
