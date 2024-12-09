from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage,ttk,messagebox,simpledialog
import subprocess
import threading
from database import Databaase

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Enoch Gabriel Astor\Desktop\Arisuu-main\ASSETS\Cashier_assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
db = Databaase()
def subproces_open_inventory():
    subprocess.Popen(['python', 'inventory.py'])

def open_inventory():
    # Function to open the inventory window in a new thread
    threading.Thread(target=subproces_open_inventory).start()
    window.after(3000, window.withdraw)  # Hide the current window after 3 seconds

def update_total_cost():
    total_cost = 0.0  # Initialize total cost
    for item in tree.get_children():  # Iterate through all items in the Treeview
        item_values = tree.item(item, 'values')  # Get the values of the item
        if item_values and len(item_values) >= 4:  # Check if there are enough values
            try:
                price = float(item_values[2])  # Convert price to float
                quantity = float(item_values[3])  # Convert quantity to float first
                if quantity < 0:
                    print(f"Warning: Negative quantity for item {item_values}. Skipping.")
                    continue  # Skip this item
                total_cost += price * int(quantity)  # Calculate total cost
            except (ValueError, IndexError) as e:
                # Handle cases where conversion fails or index is out of range
                print(f"Error processing item {item_values}: {e}")
                continue

    # Update the total_text with the calculated total cost
    canvas.itemconfig(total_text, text=f'{total_cost:.2f}')
    
def search_product():
    search_query = entry_1.get()  # Get the search query from the entry
    print(f"Search Query: '{search_query}'")  # Debug: Print the search query

    db = Databaase()  # Create a database instance
    products = db.fetch_product_by_name(search_query)  # Fetch products by name
    print(f"Fetched Products: {products}")  # Debug: Print the fetched products

    # Insert the fetched products into the Treeview
    for product in products:
        product_name, product_category, product_quantity, product_price = product
        print(f"Processing Product: Name={product_name}, Category={product_category}, Price={product_price}, Quantity={product_quantity}")  # Debug: Print product details

        # Check if the product already exists in the Treeview to avoid duplicates
        # Ensure case-sensitive comparison
        if not any(tree.item(item)['values'][0] == product_name for item in tree.get_children()):
            # Check if the product name matches the search query with case sensitivity
            if search_query in product_name:  # This will be case-sensitive
                # Insert values in the new order: Product Name, Category, Stock, Price
                tree.insert("", "end", values=(product_name, product_category, product_quantity, product_price))
                print(f"Inserted Product: {product_name}")  # Debug: Confirm insertion
            else:
                print(f"Product '{product_name}' does not match the case-sensitive search query.")  # Debug: Not matching
        else:
            print(f"Product already exists in Treeview: {product_name}")  # Debug: Product already exists

    update_total_cost()  # Update total cost
    print("Total cost updated.")  # Debug: Confirm total cost update
    
def remove_item():
    # Get the selected item from the Treeview
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to remove.")
        return

    # Remove the item from the Treeview
    tree.delete(selected_item)

    # Optionally, show a success message
    messagebox.showinfo("Success", "Selected item has been removed from the Treeview.")

def remove_all_items():
    # Clear all items from the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Optionally, show a success message
    messagebox.showinfo("Success", "All items have been removed from the table.")

def edit_stock():
    # Get the selected item from the Treeview
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to edit.")
        return

    # Get the current values from the selected item
    item_values = tree.item(selected_item, 'values')
    current_product_name = item_values[0]
    current_stock = int(item_values[2])  # Ensure current stock is an integer

    # Prompt the user for a new stock value
    new_stock_str = simpledialog.askstring("Edit Stock", f"Current stock: {current_stock}\nEnter new stock value:")
    
    if new_stock_str is None:  # User cancelled the input
        return

    # Validate new stock input
    try:
        new_stock = int(new_stock_str)  # Convert stock to int
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid numeric value for Stock.")
        return  # Exit the function if the stock is invalid

    # Update the product in the database using the existing db instance
    db.update_product(current_product_name, current_product_name, item_values[1], new_stock, item_values[3])  # Update stock

    # Update the Treeview
    tree.item(selected_item, values=(current_product_name, item_values[1], new_stock, item_values[3]))

    # Optionally, show a success message
    messagebox.showinfo("Success", f"Stock for '{current_product_name}' has been updated to {new_stock}.")
    
    # Update the total cost to reflect any changes
    update_total_cost()
    
def process_checkout():
    # Get the total cost
    total_cost = 0.0
    sold_items = []  # List to keep track of sold items and their quantities
    for item in tree.get_children():
        item_values = tree.item(item, 'values')
        if item_values and len(item_values) >= 4:  # Ensure there are enough values
            try:
                price = float(item_values[3]) if item_values[3] else 0.0
                quantity = int(item_values[2]) if item_values[2] else 0
                total_cost += price * quantity
                sold_items.append((item_values[0], quantity))  # Store product name and quantity sold
            except (ValueError, IndexError) as e:
                print(f"Error processing item {item_values}: {e}")
                continue

    print(f'Total Cost: {total_cost}')  # Debugging line

    # Get the amount paid from the entry
    amount_paid_str = entry_amount_paid.get().strip()
    if not amount_paid_str:
        messagebox.showerror("Invalid Input", "Amount paid cannot be empty.")
        return

    try:
        amount_paid = float(amount_paid_str)  # Convert to float
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid amount paid. Please enter a valid number.")
        return  # Exit if the input is invalid

    print(f'Amount Paid: {amount_paid}')  # Debugging line

    # Calculate change
    change = amount_paid - total_cost
    print(f'Change: {change}')  # Debugging line

    # Update the change display
    if change < 0:
        messagebox.showwarning("Insufficient Amount", "Insufficient amount paid. Please enter a higher amount.")
    else:
        # Update the change placeholder
        canvas.itemconfig(sukli_text, text=f'{change:.2f}')  # Update the change display

        # Deduct the sold quantity from the database using the existing db instance
        for product_name, sold_quantity in sold_items:
            current_stock = db.get_current_stock(product_name)  # Fetch current stock from the database
            new_stock = current_stock - sold_quantity  # Calculate new stock after sale

            if new_stock <= 0:
                # If stock is zero or less, delete the product
                db.delete_product(product_name)
                print(f"Deleted product: {product_name} as stock reached zero.")
            else:
                # Update the product in the database
                db.update_product(product_name, product_name, item_values[1], new_stock, item_values[3])  # Update stock

        # Clear the Treeview after successful checkout
        remove_all_items()  # Call the function to remove all items from the Treeview

        # Reset the total cost display
        canvas.itemconfig(total_text, text='0.0')  # Reset total cost to 0.0
        canvas.itemconfig(sukli_text, text='0.0')

        # Optionally, clear the amount paid entry
        entry_amount_paid.delete(0, 'end')  # Clear the amount paid entry

        # Optionally, show a success message
        messagebox.showinfo("Checkout Successful", f"Checkout completed. Change: {change:.2f}")
        
window = Tk()
window.title("Cashier")
window.geometry("1280x800")
window.configure(bg="#FFFFFF")

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
tree = ttk.Treeview(window, columns=("Product Name", "Category", "Stock", "Price"), show='')
tree.heading("Product Name", text="Product Name")
tree.heading("Category", text="Category")
tree.heading("Stock", text="Stock")  # Now Stock is before Price
tree.heading("Price", text="Price")

# Set column widths
tree.column("Product Name", width=255)
tree.column("Category", width=100)
tree.column("Stock", width=100)  # Adjusted position
tree.column("Price", width=100)   # Adjusted position

# Place the Treeview on the canvas
tree.place(x=40, y=175, width=1049, height=400)
canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    800.0,
    fill="#97BCC7",
    outline=""
)

canvas.create_rectangle(
    1.0,
    0.0,
    1281.0,
    800.0,
    fill="#97BCC7",
    outline=""
)

canvas.create_rectangle(
    142.0,
    629.0,
    790.0,
    685.0,
    fill="#FFFFFF",
    outline=""
)
entry_amount_paid = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=("Times New Roman", 20),
)

entry_amount_paid.place(x=380.0, y=645.0, width=150.0, height=30.0)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: process_checkout(),
    relief="flat"
)
button_1.place(x=854.0, y=585.0, width=159.0, height=44.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: edit_stock(),
    relief="flat"
)
button_2.place(x=1105.0, y=442.0, width=159.0, height=44.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: remove_all_items(),
    relief="flat"
)
button_3.place(x=854.0, y=641.0, width=159.0, height=44.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window.destroy(),
    relief="flat"
)
button_4.place(x=1105.0, y=506.0, width=159.0, height=44.0)

# Image for the canvas
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(464.99993896484375, 606.0, image=image_image_1)

canvas.create_rectangle(
    43.0,
    183.0,
    1088.0,
    564.0,
    fill="#FFFFFF",
    outline=""
)

button_image_5 = PhotoImage(file= relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: remove_item(),
    relief="flat"
)
button_5.place(x=1105.0, y=378.0, width=159.0, height=44.0)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=open_inventory,  # Open inventory window
    relief="flat"
)
button_6.place(x=1105.0, y=314.0, width=159.0, height=44.0)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(1185.0, 238.0, image=image_image_2)

canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    109.71428680419922,
    fill="#D9D9D9",
    outline=""
)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(1032.0, 55.0, image=image_image_3)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(565.0, 161.0, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(313.0, 55.0, image=image_image_5)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(322.0, 55.5, image=entry_image_1)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(x=85.0, y=42.0, width=474.0, height=25.0)

canvas.create_rectangle(
    363.0,
    638.0,
    569.0,
    675.0,
    fill="#FFFFFF",
    outline=""
)
entry_1.bind("<Return>", lambda event: search_product())

total_text = canvas.create_text(250.0, 655.0, anchor="center", text='0.0', fill="#2C3167", font=("Times New Roman", 20))
sukli_text = canvas.create_text(670.0, 655.0, anchor="center", text='0.0', fill="#2C3167", font=("Times New Roman", 20))
window.resizable(False, False)
window.mainloop()
