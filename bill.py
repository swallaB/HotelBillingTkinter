import tkinter as tk
from tkinter import ttk, messagebox,PhotoImage
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HotelBill:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x700")
        self.root.title("Hotel Bill Generator")
        self.setup_database()

        #creating tabs
        self.tabs = ttk.Notebook(self.root)
        self.bill_tab = tk.Frame(self.tabs)
        self.analysis_tab = tk.Frame(self.tabs)

        self.tabs.add(self.bill_tab,text="BILL")
        self.tabs.add(self.analysis_tab, text="Analysis")

        self.tabs.pack(expand=True,fill="both")
        self.total_label = tk.Label()
        self.date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.time = tk.StringVar(value=datetime.now().strftime("%H:%M:%S"))
        self.name = tk.StringVar()
        self.bill_no = tk.StringVar(value=self.generate_bill_no())
        self.selected_item = tk.StringVar()
        self.quantity = tk.IntVar(value=1)
        self.items = {"Pizza": 200,
    "Pasta": 150,
    "Burger": 100,
    "French Fries": 80,
    "Sandwich": 60,
    "Spring Rolls": 90,
    "Cheese Nachos": 120,
    "Garlic Bread": 70,
    "Onion Rings": 100}
        self.total_amount = tk.DoubleVar(value=0.0)
        self.table_data = []

        self.bill_ui()
        self.create_analysis()


    def setup_database(self):
        conn = sqlite3.connect("bills_data.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS bills (
                                    bill_no INTEGER PRIMARY KEY AUTOINCREMENT,
                                    date TEXT,
                                    name TEXT,
                                    total_amount REAL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS bill_items (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    bill_no INTEGER,
                                    item TEXT,
                                    quantity INTEGER,
                                    price REAL,
                                    FOREIGN KEY (bill_no) REFERENCES bills(bill_no))''')
        conn.commit()
        print("Tables created successfully!")
        conn.close()

    def generate_bill_no(self):
        conn = sqlite3.connect("bills_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(bill_no) FROM bills")
        result = cursor.fetchone()[0]
        conn.close()
        return (result + 1) if result else 1

    def bill_ui(self):
        frame_bill = tk.Frame(self.bill_tab)
        frame_bill.pack(fill="both", expand =True, padx=5,pady=5)

        self.tit_frame = tk.Frame(frame_bill, bg="#1E90FF",height=50,bd=5,relief="sunken")
        self.tit = tk.Label(self.tit_frame, text="HOTEL MANAGEMENT SYSTEM",bg="#1E90FF",font=("Georgia", 20))
        self.tit.pack(pady=15)
        self.tit_frame.pack(fill="x")


        self.head_frame = tk.Frame(frame_bill, bg="black", height = 70,bd=5,relief="sunken")
        self.head_frame.pack(fill="x")

        #headframe- date,time,name,billno
        tk.Label(self.head_frame, text="Name:", bg="black", fg="white", font=("Georgia", 18)).pack(expand=True,side="left",
                                                                                                 padx=10, pady=30,
                                                                                                 )
        tk.Entry(self.head_frame, textvariable=self.name,font=("Georgia", 10)).pack(expand=True,side="left", pady=10)

        tk.Label(self.head_frame, text="Bill number:", bg="black", fg="white", font=("Georgia", 18)).pack(expand=True,side="left",
                                                                                                 padx=10, pady=10,
                                                                                                 )
        tk.Entry(self.head_frame, textvariable=self.bill_no,state="readonly",font=("Georgia", 10)).pack(expand=True,side="left", pady=10)

        tk.Label(self.head_frame, text="Date:", bg="black",fg="white",font=("Georgia", 18)).pack(expand=True,side="left", padx=10,pady=10)
        tk.Entry(self.head_frame, textvariable=self.date, state="readonly",font=("Georgia", 10)).pack(expand=True,side="left",pady=10)

        tk.Label(self.head_frame, text="Time:", bg="black",fg="white",font=("Georgia", 18)).pack(expand=True,side="left", padx=10,pady=10)
        tk.Entry(self.head_frame, textvariable=self.time, state="readonly",font=("Georgia", 10)).pack(expand=True,side="left",pady=10)

        #frame for menu list
        menulist_frame = tk.Frame(frame_bill, bg="lightblue",bd=5,relief="ridge")
        menulist_frame.pack(side="left", fill="both", expand=True)

        menu_title = tk.Label(menulist_frame,text="MENU",bg="lightblue",font=("Georgia", 20))
        menu_title.pack(pady=20)

        frame_menu = tk.Frame(menulist_frame,bg="lightblue")
        frame_menu.pack(fill="x", pady=10,anchor="n")

        tk.Label(frame_menu, text="Select Item:",font=("Georgia", 12),bg="lightblue").grid(row=0, column=0, padx=5, sticky="w")
        menu_dropdown = ttk.Combobox(frame_menu, textvariable=self.selected_item, values=list(self.items.keys()))
        menu_dropdown.grid(row=0, column=1, padx=5)

        tk.Label(frame_menu, text="Quantity:",font=("Georgia", 12),bg="lightblue").grid(row=0, column=2, padx=5, sticky="w")
        tk.Entry(frame_menu, textvariable=self.quantity).grid(row=0, column=3, padx=5)

        list_frame = tk.Frame(menulist_frame, bg="lightblue", bd=5, relief="ridge")
        image=PhotoImage(file="menulist.png")
        label = tk.Label(list_frame, image=image)
        list_frame.pack(side="left", fill="y", padx=10, pady=10, expand=True)
        label.image = image  # Keep a reference of the image to prevent garbage collection
        label.pack()




        # Frame for Added Items and Bill
        order_frame = tk.Frame(frame_bill, bg="#B0C4DE",bd=5,relief="ridge")
        order_frame.pack(side="right", fill="both", expand=True)

        menu_title = tk.Label(order_frame, text="YOUR ORDER", bg="#B0C4DE", font=("Georgia", 20))
        menu_title.pack(pady=20)

        button_frame = tk.Frame(order_frame,bg="#4682B4",bd=5,relief="ridge")
        button_frame.pack(fill="x")
        tk.Button(button_frame, text="Add Item",font=("Georgia", 9),bg="#B0C4DE", command=self.add_item).pack(side="left", padx=20,pady=10)
        tk.Button(button_frame, text="Delete Item",font=("Georgia", 9),bg="#B0C4DE", command=self.delete_item).pack(side="left", padx=20,pady=10)
        tk.Button(button_frame, text="Update Quantity",font=("Georgia", 9),bg="#B0C4DE", command=self.update_quantity).pack(side="left", padx=20,pady=10)
        tk.Button(button_frame, text="Generate Bill",font=("Georgia", 9),bg="#B0C4DE", command=self.generate_bill).pack(side="left", padx=20,pady=10)

        # Table
        frame_table = tk.Frame(order_frame)
        frame_table.pack(fill="both", pady=10,padx=20, expand=True)

        columns = ("Item", "Quantity", "Price", "Total")
        self.table = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)
        self.table.pack(side="left", fill="both", expand=True)

        for col in columns:
            self.table.heading(col, text=col)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscroll=scrollbar.set)

        frame_total = tk.Frame(order_frame,bg="#4682B4",bd=5,relief="ridge")  # Replace self.root with the appropriate parent frame if needed
        frame_total.pack(fill="x", pady=10,anchor="center")
        tk.Label(frame_total, text="Total Amount:",font=("Georgia", 12),bg="#4682B4").pack(side="left", padx=5,pady=10)
        tk.Entry(frame_total, textvariable=self.total_amount, state="readonly").pack(side="left", padx=5)
        tk.Label(frame_total, text="Payment Method:",font=("Georgia", 12),bg="#4682B4").pack(side="left", padx=10)
        payment_options = ["Cash", "Card", "UPI", "Net Banking"]
        payment_dropdown = ttk.Combobox(frame_total, values=payment_options, state="readonly")
        payment_dropdown.pack(side="left", padx=5)


    def add_item(self):
        item = self.selected_item.get()
        quantity = self.quantity.get()
        if item and quantity > 0:
            price = self.items[item]
            total = price * quantity
            self.table_data.append((item, quantity, price, total))
            self.update_table()
        else:
            messagebox.showerror("Error", "Please select an item and enter a valid quantity.")

    # Delete Item Function
    def delete_item(self):
        selected = self.table.selection()
        if selected:
            index = self.table.index(selected[0])
            self.table_data.pop(index)
            self.update_table()
        else:
            messagebox.showerror("Error", "No item selected to delete.")

 # Update Quantity Function
    def update_quantity(self):
        selected = self.table.selection()
        if selected:
            index = self.table.index(selected[0])
            new_quantity = self.quantity.get()
            if new_quantity > 0:
                item, _, price, _ = self.table_data[index]
                total = price * new_quantity
                self.table_data[index] = (item, new_quantity, price, total)
                self.update_table()
            else:
                messagebox.showerror("Error", "Quantity must be greater than zero.")
        else:
            messagebox.showerror("Error", "No item selected to update.")

    # Update Table Function
    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        self.total_amount.set(0.0)
        for item, quantity, price, total in self.table_data:
            self.table.insert("", "end", values=(item, quantity, price, total))
            self.total_amount.set(self.total_amount.get() + total)
        self.total_label.config(text=f"Total Amount: ₹{self.total_amount.get():.2f}")

    def generate_bill(self):
        if not self.name.get():
            messagebox.showerror("Error", "Customer name is required to generate the bill.")
            return

        conn = sqlite3.connect("bills_data.db")
        cursor = conn.cursor()

        # Insert into bills table
        cursor.execute(
            '''INSERT INTO bills (date, name, total_amount) VALUES (?, ?, ?)''',
            (self.date.get(), self.name.get(), self.total_amount.get()),
        )
        bill_no = cursor.lastrowid

        # Insert into bill_items table
        for item, quantity, price, total in self.table_data:
            cursor.execute(
                '''INSERT INTO bill_items (bill_no, item, quantity, price) VALUES (?, ?, ?, ?)''',
                (bill_no, item, quantity, price),
            )

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Bill {bill_no} generated successfully!")
        self.reset()

    # Reset the form
    def reset(self):
        self.name.set("")
        self.selected_item.set("")
        self.quantity.set(1)
        self.table_data = []
        self.update_table()

    def get_datewise_revenue(self):
        conn = sqlite3.connect("bills_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, SUM(total_amount) 
            FROM bills 
            GROUP BY date
            ORDER BY date
        """)
        data = cursor.fetchall()
        print("Fetched Data:", data)
        conn.close()
        return data

    def get_itemwise_revenue(self):
        conn = sqlite3.connect("bills_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item, SUM(quantity) as total_quantity, SUM(quantity * price) as total_revenue
            FROM bill_items
            GROUP BY item
            ORDER BY total_revenue DESC
        """)
        data = cursor.fetchall()
        print("Fetched Data:", data)
        conn.close()
        return data

    def create_analysis(self):
        date_graph_frame = tk.Frame(self.analysis_tab, bg="lightblue", bd=5, relief="ridge")
        date_graph_frame.pack(side="top", fill="x", padx=10, pady=10)

        tk.Label(date_graph_frame, text="Date-Wise Revenue Graph", font=("Georgia", 14), bg="lightblue").pack()
        self.date_graph_canvas = None  # Placeholder for Matplotlib canvas
        tk.Button(date_graph_frame, text="Show Date-Wise Revenue Graph", command=self.plot_datewise_revenue).pack(
            pady=5)

        # Frame for Item-wise Revenue Graph
        item_graph_frame = tk.Frame(self.analysis_tab, bg="lightblue", bd=5, relief="ridge")
        item_graph_frame.pack(side="top", fill="x", padx=10, pady=10)

        tk.Label(item_graph_frame, text="Item-Wise Revenue Graph", font=("Georgia", 14), bg="lightblue").pack()
        self.item_graph_canvas = None  # Placeholder for Matplotlib canvas
        tk.Button(item_graph_frame, text="Show Item-Wise Revenue Graph", command=self.plot_itemwise_revenue).pack(
            pady=5)

    def plot_datewise_revenue(self):
        # Fetch Date-Wise Revenue Data
        data = self.get_datewise_revenue()
        dates = [row[0] for row in data]
        revenues = [row[1] for row in data]

        # Plot the Data
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(dates, revenues, color="skyblue")
        ax.set_title("Date-Wise Revenue")
        ax.set_xlabel("Date")
        ax.set_ylabel("Revenue (₹)")
        ax.set_xticklabels(dates, rotation=45)

        # Display the Graph in the UI
        if self.date_graph_canvas:
            self.date_graph_canvas.get_tk_widget().destroy()  # Remove old canvas
        self.date_graph_canvas = FigureCanvasTkAgg(fig, master=self.analysis_tab)
        self.date_graph_canvas.get_tk_widget().pack(side="top", padx=10, pady=10)

        plt.close(fig)  # Close the figure to avoid overlapping

    def plot_itemwise_revenue(self):
        # Fetch Item-Wise Revenue Data
        data = self.get_itemwise_revenue()
        items = [row[0] for row in data]
        revenues = [row[2] for row in data]

        # Plot the Data
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(items, revenues, color="orange")
        ax.set_title("Item-Wise Revenue")
        ax.set_xlabel("Item")
        ax.set_ylabel("Revenue (₹)")
        ax.set_xticklabels(items, rotation=45)

        # Display the Graph in the UI
        if self.item_graph_canvas:
            self.item_graph_canvas.get_tk_widget().destroy()  # Remove old canvas
        self.item_graph_canvas = FigureCanvasTkAgg(fig, master=self.analysis_tab)
        self.item_graph_canvas.get_tk_widget().pack(side="top", padx=10, pady=10)

        plt.close(fig)  # Close the figure to avoid overlapping





if __name__ == "__main__":
    root = tk.Tk()
    b = HotelBill(root)
    root.mainloop()
