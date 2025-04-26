import psycopg2

class Customers:

    def __init__(self, conn):
        self.conn = conn

    def fetch_all_customers(self):
        """
        Fetch all customers from the 'customers' table.
        """
        query = "SELECT id, name, contact_email, phone, address, created_at FROM customers"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows

    def fetch_customer_by_id(self, customer_id):
        """
        Fetch a customer by their ID from the 'customers' table.
        
        :param customer_id: The ID of the customer to fetch.
        """
        query = "SELECT id, name, contact_email, phone, address, created_at FROM customers WHERE id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            row = cursor.fetchone()
        return row

    def insert_customer(self, name, contact_email, phone, address):
        """
        Insert a new customer into the 'customers' table.
        
        :param name: Customer's name.
        :param contact_email: Customer's email.
        :param phone: Customer's phone number.
        :param address: Customer's address.
        """
        query = """
        INSERT INTO customers (name, contact_email, phone, address, created_at)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (name, contact_email, phone, address))
            self.conn.commit()

    def update_customer(self, customer_id, name=None, contact_email=None, phone=None, address=None):
        """
        Update a customer's information in the 'customers' table.
        
        :param customer_id: The ID of the customer to update.
        :param name: The new name of the customer.
        :param contact_email: The new email of the customer.
        :param phone: The new phone number of the customer.
        :param address: The new address of the customer.
        """
        query = "UPDATE customers SET "
        updates = []
        params = []

        if name:
            updates.append("name = %s")
            params.append(name)
        if contact_email:
            updates.append("contact_email = %s")
            params.append(contact_email)
        if phone:
            updates.append("phone = %s")
            params.append(phone)
        if address:
            updates.append("address = %s")
            params.append(address)

        query += ", ".join(updates) + " WHERE id = %s"
        params.append(customer_id)

        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            self.conn.commit()

    def delete_customer(self, customer_id):
        """
        Delete a customer from the 'customers' table.
        
        :param customer_id: The ID of the customer to delete.
        """
        query = "DELETE FROM customers WHERE id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()
