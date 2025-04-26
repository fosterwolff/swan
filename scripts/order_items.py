import psycopg2

class OrderItems:
    def __init__(self, conn):
        self.conn = conn

    def fetch_all_order_items(self):
        """Fetch all order items from the 'order_items' table."""
        query = "SELECT * FROM order_items"
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def fetch_order_items_by_order_id(self, order_id):
        """Fetch all items associated with a specific order from the 'order_items' table."""
        query = "SELECT * FROM order_items WHERE order_id = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (order_id,))
            return cur.fetchall()

    def insert_order_item(self, order_id, product_id, quantity, unit_price):
        """Insert a new order item into the 'order_items' table."""
        query = """
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (%s, %s, %s, %s)
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (order_id, product_id, quantity, unit_price))
            self.conn.commit()

    def update_order_item(self, order_item_id, quantity=None, unit_price=None):
        """Update an existing order item in the 'order_items' table."""
        updates = []
        values = []

        if quantity is not None:
            updates.append("quantity = %s")
            values.append(quantity)
        
        if unit_price is not None:
            updates.append("unit_price = %s")
            values.append(unit_price)
        
        if updates:
            query = f"UPDATE order_items SET {', '.join(updates)} WHERE id = %s"
            values.append(order_item_id)
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(values))
                self.conn.commit()

    def delete_order_item(self, order_item_id):
        """Delete an order item from the 'order_items' table."""
        query = "DELETE FROM order_items WHERE id = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (order_item_id,))
            self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()
