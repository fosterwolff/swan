import psycopg2
from suppliers import Suppliers  # Make sure this class is imported

# DB connection params
db_params = {
    'dbname': 'swan',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

# Connect to the database
conn = psycopg2.connect(**db_params)

# Create an instance of the Suppliers class
suppliers_db = Suppliers(conn)

# Insert a new supplier
supplier_id = suppliers_db.insert_supplier(name="Supplier A", contact_email="contact@supplierA.com", phone="555-1234", address="456 Supplier St")

# Fetch all suppliers
all_suppliers = suppliers_db.fetch_all()
print("All Suppliers:", all_suppliers)

# Fetch supplier by ID
supplier = suppliers_db.fetch_by_id(supplier_id)
print(f"Supplier with ID {supplier_id}:", supplier)

# Close the connection when done
conn.close()
