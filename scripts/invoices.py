import psycopg2
from datetime import datetime

class Invoices:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def insert_invoice(self, invoice_number, order_id, seller_name, seller_address, seller_contact, 
                       buyer_name, buyer_address, buyer_contact, description_of_goods, 
                       taxes_and_discounts, amount, total_amount_due, payment_terms, due_date, paid=False):
        query = """
        INSERT INTO invoices (
            invoice_number, order_id, seller_name, seller_address, seller_contact, 
            buyer_name, buyer_address, buyer_contact, description_of_goods, 
            taxes_and_discounts, amount, total_amount_due, payment_terms, 
            due_date, paid
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        self.cursor.execute(query, (
            invoice_number, order_id, seller_name, seller_address, seller_contact, 
            buyer_name, buyer_address, buyer_contact, description_of_goods, 
            taxes_and_discounts, amount, total_amount_due, payment_terms, 
            due_date, paid
        ))
        invoice_id = self.cursor.fetchone()[0]
        self.conn.commit()
        print(f"Invoice {invoice_id} created with number {invoice_number}")
        return invoice_id

    def fetch_invoice_by_order_id(self, order_id):
        query = """
        SELECT id, invoice_number, order_id, seller_name, seller_address, seller_contact, 
               buyer_name, buyer_address, buyer_contact, description_of_goods, 
               taxes_and_discounts, amount, total_amount_due, payment_terms, 
               issue_date, due_date, paid, created_at
        FROM invoices WHERE order_id = %s;
        """
        self.cursor.execute(query, (order_id,))
        invoice = self.cursor.fetchone()
        if invoice:
            return invoice
        else:
            print(f"No invoice found for order {order_id}")
            return None

    def update_invoice_status(self, invoice_id, paid):
        query = """
        UPDATE invoices
        SET paid = %s
        WHERE id = %s;
        """
        self.cursor.execute(query, (paid, invoice_id))
        self.conn.commit()
        print(f"Invoice {invoice_id} updated with paid status: {paid}")

    def fetch_all_invoices(self):
        query = "SELECT * FROM invoices;"
        self.cursor.execute(query)
        invoices = self.cursor.fetchall()
        return invoices
