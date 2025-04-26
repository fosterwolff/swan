import psycopg2

class Suppliers:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    # Insert a new supplier
    def insert_supplier(self, name, contact_email, phone, address):
        query = """
        INSERT INTO suppliers (name, contact_email, phone, address)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        self.cursor.execute(query, (name, contact_email, phone, address))
        self.conn.commit()
        return self.cursor.fetchone()[0]  # Return the generated supplier ID

    # Fetch all suppliers
    def fetch_all(self):
        self.cursor.execute("SELECT * FROM suppliers;")
        return self.cursor.fetchall()

    # Fetch a supplier by its ID
    def fetch_by_id(self, supplier_id):
        self.cursor.execute("SELECT * FROM suppliers WHERE id = %s;", (supplier_id,))
        return self.cursor.fetchone()

    # Update supplier details
    def update_supplier(self, supplier_id, name=None, contact_email=None, phone=None, address=None):
        query = """
        UPDATE suppliers
        SET name = COALESCE(%s, name),
            contact_email = COALESCE(%s, contact_email),
            phone = COALESCE(%s, phone),
            address = COALESCE(%s, address)
        WHERE id = %s;
        """
        self.cursor.execute(query, (name, contact_email, phone, address, supplier_id))
        self.conn.commit()

    # Delete a supplier
    def delete_supplier(self, supplier_id):
        self.cursor.execute("DELETE FROM suppliers WHERE id = %s;", (supplier_id,))
        self.conn.commit()
