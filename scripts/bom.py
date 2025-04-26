import psycopg2
from decimal import Decimal

class BOM:
    def __init__(self, conn):
        self.conn = conn

    def fetch_bom_by_product_and_order_id(self, product_id, order_id):
        """Fetch the BOM details for a given product and order, including parts and their quantities."""
        with self.conn.cursor() as cur:
            query = """
            SELECT b.bom_id, p.name AS part_name, p.part_number, p.unit_cost, b.quantity_required
            FROM bom b
            JOIN parts p ON b.part_id = p.id
            WHERE b.product_id = %s AND b.order_id = %s
            """
            cur.execute(query, (product_id, order_id))
            return cur.fetchall()

    def insert_bom(self, product_id, part_id, quantity_required, order_id):
        """Insert a new BOM entry associating a part with a product and order."""
        query = """
        INSERT INTO bom (product_id, part_id, quantity_required, order_id)
        VALUES (%s, %s, %s, %s)
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (product_id, part_id, quantity_required, order_id))
            self.conn.commit()

    def update_bom(self, bom_id, part_id=None, quantity_required=None, order_id=None):
        """Update the BOM for a specific product, part, and order."""
        updates = []
        values = []
        
        if part_id:
            updates.append("part_id = %s")
            values.append(part_id)
        
        if quantity_required is not None:
            updates.append("quantity_required = %s")
            values.append(quantity_required)
        
        if order_id:
            updates.append("order_id = %s")
            values.append(order_id)
        
        if updates:
            query = f"UPDATE bom SET {', '.join(updates)} WHERE bom_id = %s"
            values.append(bom_id)
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(values))
                self.conn.commit()

    def delete_bom(self, bom_id):
        """Delete a BOM entry."""
        query = "DELETE FROM bom WHERE bom_id = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (bom_id,))
            self.conn.commit()

    def calculate_total_bom_price(self, product_id, order_id):
        """Calculate the total price of a product based on its BOM for a specific order."""
        total_price = Decimal(0)
        with self.conn.cursor() as cur:
            query = """
            SELECT p.unit_cost, b.quantity_required
            FROM bom b
            JOIN parts p ON b.part_id = p.id
            WHERE b.product_id = %s AND b.order_id = %s
            """
            cur.execute(query, (product_id, order_id))
            rows = cur.fetchall()
            for row in rows:
                unit_cost = row[0]
                quantity = row[1]
                total_price += unit_cost * quantity
        return total_price

    def fetch_bom_by_order_id(self, order_id):
        query = "SELECT * FROM bom WHERE order_id = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (order_id,))
            return cur.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()
