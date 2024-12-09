import sqlite3

class Databaase:
    def __init__(self, db_name="store_arisu.db"):
        """Initialize the database connection and create the table if it doesn't exist."""
        print(f"Connecting to database: {db_name}")  # Debugging line
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        
        # Create the login table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS login (
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        
        # Insert a default admin user if the table is empty
        self.cursor.execute("SELECT COUNT(*) FROM login")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO login (username, password) VALUES ('admin', 'admin')")
            self.connection.commit()

        self.create_product_table()

    def login(self, username, password):
        """Check if the username and password match an entry in the login table."""
        self.cursor.execute("SELECT * FROM login WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def create_product_table(self):
        """Create the product table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_name TEXT NOT NULL,
            product_category TEXT NOT NULL,
            product_quantity INTEGER,
            product_price REAL  -- Use REAL for decimal prices
        )
        """)
        self.connection.commit()  # Commit the changes to the database

    def insert_product(self, product_name, product_category, product_quantity, product_price):
        """Insert a new product into the product table."""
        try:
            self.cursor.execute("""
                INSERT INTO product (product_name, product_category, product_quantity, product_price)
                VALUES (?, ?, ?, ?)
            """, (product_name, product_category, product_quantity, product_price))
            self.connection.commit()  # Commit the changes to the database
            print(f"Successfully inserted product: {product_name}, Category: {product_category}, Quantity: {product_quantity}, Price: {product_price}")
        except sqlite3.Error as e:
            print(f"Error inserting product: {e}")  # Log the error
            raise  # Optionally re-raise the exception to handle it further up the call stack

    def fetch_all_products(self):
        """Fetch all products from the product table."""
        self.cursor.execute("SELECT product_name, product_category, product_quantity, product_price FROM product")
        return self.cursor.fetchall()  # Return all rows as a list of tuples

    def delete_product(self, product_name):
        """Delete a product from the product table."""
        try:
            self.cursor.execute("DELETE FROM product WHERE product_name=?", (product_name,))
            self.connection.commit()  # Commit the changes to the database
            print(f"Successfully deleted product: {product_name}")  # Debugging line
        except sqlite3.Error as e:
            print(f"Error deleting product: {e}")  # Log the error
            raise  # Optionally re-raise the exception to handle it further up the call stack

    def update_product(self, current_product_name, new_product_name, new_category, new_quantity, new_price):
        """Update an existing product in the product table."""
        self.cursor.execute("""
            UPDATE product
            SET product_name = ?, product_category = ?, product_quantity = ?, product_price = ?
            WHERE product_name = ?
        """, (new_product_name, new_category, new_quantity, new_price, current_product_name))
        self.connection.commit()  # Commit the changes to the database

    def fetch_product_by_name(self, product_name):
        """Fetch products from the product table that match the given name exactly (case-sensitive)."""
        try:
            # Use the equality operator for an exact case-sensitive match
            self.cursor.execute("SELECT product_name, product_category, product_quantity, product_price FROM product WHERE product_name = ?", (product_name,))
            
            # Fetch all matching records
            results = self.cursor.fetchall()
            
            # Debug: Print the results
            print(f"Fetched Products: {results}")  # Debug: Print the fetched products
            
            return results
        except Exception as e:
            print(f"Error fetching products: {e}")  # Debug: Print any errors
            return []  # Return an empty list in case of error
    
    def get_current_stock(self, product_name):
        """Fetch the current stock for a given product name."""
        self.cursor.execute("SELECT product_quantity FROM product WHERE product_name = ?", (product_name,))
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def close(self):
        """Close the database connection."""
        self.connection.close()
        print("Database connection closed.")  # Debugging line
