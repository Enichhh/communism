from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, messagebox
from database import Databaase
import subprocess
import threading

db = Databaase()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\Arisuu-main\ASSETS\Inventory_assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.title("Inventory")
window.geometry("1280x800")
window.configure(bg="#FFFFFF")

def load_product_treeview():
    # Clear the existing items in the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Fetch all products from the database
    products = db.fetch_all_products()

    # Check if there are no products
    if not products:
        print("There are no Items available in the database")  # Print message if no products
        return  # Exit the function if there are no products

    # Insert each product into the Treeview
    for product in products:
        product_name, product_category, product_quantity, product_price = product
        tree.insert("", "end", values=(product_name, product_category, product_price, product_quantity))

window.after(5000, load_product_treeview)

def add_item():
    product_name = entry_2.get()  # Product Name
    category = entry_3.get()       # Category
    price_str = entry_4.get()      # Price as string
    stock_str = entry_5.get()      # Stock as string

    # Validate price input
    try:
        price = float(price_str)  # Convert price to float
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid numeric value for Price.")
        return  # Exit the function if the price is invalid

    # Validate stock input
    try:
        stock = int(stock_str)  # Convert stock to int
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid numeric value for Stock.")
        return  # Exit the function if the stock is invalid

    # Insert the new product into the database
    db.insert_product(product_name, category, stock, price)  # Pass category to the method
    
    # Insert the new item into the Treeview
    tree.insert("", "end", values=(product_name, category, price, stock))

    # Print success message
    print(f"Inserting Product Name: '{product_name}', Category: '{category}', Price: '{price}', Stock: '{stock}'")
    print("Successfully inserted")
    
    # Clear the entry fields after adding
    entry_2.delete(0, 'end')
    entry_3.delete(0, 'end')
    entry_4.delete(0, 'end')
    entry_5.delete(0, 'end')

def remove_item():
    # Get the selected item from the Treeview
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to remove.")
        return

    # Get the product name from the selected item
    item_values = tree.item(selected_item, 'values')
    product_name = item_values[0]  # Assuming the first column is the product name

    # Remove the product from the database
    db.delete_product(product_name)

    # Remove the item from the Treeview
    tree.delete(selected_item)

def update_item():
    # Get the selected item from the Treeview
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to update.")
        return

    # Get the current values from the selected item
    item_values = tree.item(selected_item, 'values')
    current_product_name = item_values[0]
    current_category = item_values[1]
    current_price = item_values[2]
    current_stock = item_values[3]

    # Get new values from the entry fields
    new_product_name = entry_2.get() or current_product_name  # Use current value if blank
    new_category = entry_3.get() or current_category          # Use current value if blank
    new_price_str = entry_4.get()
    new_stock_str = entry_5.get()

    # Validate new price input
    if new_price_str:
        try:
            new_price = float(new_price_str)  # Convert price to float
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value for Price.")
            return  # Exit the function if the price is invalid
    else:
        new_price = current_price  # Use current price if new price is blank

    # Validate new stock input
    if new_stock_str:
        try:
            new_stock = int(new_stock_str)  # Convert stock to int
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value for Stock.")
            return  # Exit the function if the stock is invalid
    else:
        new_stock = current_stock  # Use current stock if new stock is blank

    # Debug print indicating the update process has started
    print("Updating...")

    # Update the product in the database
    db.update_product(current_product_name, new_product_name, new_category, new_stock, new_price)

    # Update the Treeview
    tree.item(selected_item, values=(new_product_name, new_category, new_price, new_stock))

    # Debug print indicating the product has been updated
    print(f"Product updated: Name: '{new_product_name}', Category: '{new_category}', Price: '{new_price}', Stock: '{new_stock}'")

    # Clear the entry fields after updating
    entry_2.delete(0, 'end')
    entry_3.delete(0, 'end')
    entry_4.delete(0, 'end')
    entry_5.delete(0, 'end')

def search_items():
    search_query = entry_1.get().lower()  # Get the search query and convert it to lowercase
    # Clear the existing items in the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Fetch all products from the database
    products = db.fetch_all_products()

    # If the search query is empty, show all products
    if not search_query:
        for product in products:
            product_name, product_category, product_quantity, product_price = product
            tree.insert("", "end", values=(product_name, product_category, product_price, product_quantity))
        return

    # Filter products based on the search query
    for product in products:
        product_name, product_category, product_quantity, product_price = product
        if search_query in product_name.lower():  # Check if the search query is in the product name
            tree.insert("", "end", values=(product_name, product_category, product_price, product_quantity))
def subprocess_open_cashier():
    subprocess.Popen(['python', 'cashier.py'])
def open_cashier():
    # Function to open the cashier window in a new thread
    threading.Thread(target=subprocess_open_cashier).start()
    window.after(3000, window.withdraw)  # Close the inventory window

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=800,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

style = ttk.Style()
style.configure("Treeview.Heading", bordercolor="black", borderwidth=1)  # Set border color and width
style.configure("Treeview", rowheight=25)

# Create a Treeview widget
tree = ttk.Treeview(window, columns=("Product Name", "Category", "Price", "Stock"), show='')
tree.heading("Product Name", text="Product Name")
tree.heading("Category", text="Category")
tree.heading("Price", text="Price")
tree.heading("Stock", text="Stock")

# Set column widths
tree.column("Product Name", width=255)
tree.column("Category", width=100)
tree.column("Price", width=100)
tree.column("Stock", width=100)

# Place the Treeview on the canvas
tree.place(x=40, y=175, width=1049, height=358)
canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    800.0,
    fill="#97BCC7",
    outline=""
)

canvas.create_rectangle(
    43.0,
    182.0,
    1088.0,
    534.0,
    fill="#FFFFFF",
    outline=""
)

canvas.create_rectangle(
    45.0,
    660.0,
    1089.0,
    712.0,
    fill="#FFFFFF",
    outline=""
)

canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    109.71428680419922,
    fill="#D9D9D9",
    outline=""
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window.destroy(),
    relief="flat"
)
button_1.place(
    x=1105.0,
    y=491.0,
    width=159.0,
    height=44.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: remove_item(),
    relief="flat"
)
button_2.place(
    x=1107.0,
    y=613.0,
    width=159.0,
    height=44.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_item(),
    relief="flat"
)
button_3.place(
    x=1105.0,
    y=432.0,
    width=159.0,
    height=44.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_cashier(),   
    relief="flat"
)
button_4.place(
    x=1105.0,
    y=312.0,
    width=159.0,
    height=44.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_item(),
    relief="flat"
)
button_5.place(
    x=1105.0,
    y=372.0,
    width=159.0,
    height=44.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    565.0,
    161.0,
    image=image_image_1
)

canvas.create_rectangle(
    640.0,
    616.0,
    855.9771118164062,
    661.0,
    fill="#D9D9D9",
    outline=""
)

canvas.create_text(
    708.6694946289062,
    630.0,
    anchor="nw",
    text="Price:",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_rectangle(
    425.0,
    616.0,
    640.9771118164062,
    660.9285697937012,
    fill="#D9D9D9",
    outline=""
)

canvas.create_text(
    502.72003173828125,
    630.0,
    anchor="nw",
    text="Category",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_rectangle(
    45.0,
    616.0,
    426.0,
    661.0,
    fill="#D9D9D9",
    outline=""
)

canvas.create_text(
    178.0,
    630.0,
    anchor="nw",
    text="Product Name",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_rectangle(
    855.0,
    616.0,
    1089.0,
    661.0,
    fill="#D9D9D9",
    outline=""
)

canvas.create_text(
    949.0,
    630.0,
    anchor="nw",
    text="Stock:",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    1185.0,
    238.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    1114.0,
    55.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    313.0,
    55.0,
    image=image_image_4
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    320.0,
    55.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=84.0,
    y=41.0,
    width=472.0,
    height=26.0
)
entry_1.bind("<KeyRelease>", lambda event: search_items()) 

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    235.0,
    686.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=50.0,
    y=664.0,
    width=370.0,
    height=42.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    533.0,
    686.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=430.0,
    y=664.0,
    width=206.0,
    height=42.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    748.0,
    686.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=645.0,
    y=664.0,
    width=206.0,
    height=42.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    972.0,
    686.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=860.0,
    y=664.0,
    width=224.0,
    height=42.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    576.0,
    581.0,
    image=image_image_5
)

canvas.create_text(
    547.0,
    570.0,
    anchor="nw",
    text="Editing",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    782.0,
    58.0,
    image=image_image_6
)

canvas.create_text(
    599.0,
    33.0,
    anchor="nw",
    text="User :",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)
window.resizable(False, False)
window.mainloop()