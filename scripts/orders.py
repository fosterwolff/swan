import psycopg2

class Orders:
    def __init__(self, conn):
        self.conn = conn

    def fetch_all_orders(self):
        """Fetch all orders from the 'orders' table."""
        with self.conn.cursor() as cur:
            query = "SELECT * FROM orders"
            cur.execute(query)
            return cur.fetchall()

    def fetch_order_by_id(self, order_id):
        """Fetch an order by its ID."""
        with self.conn.cursor() as cur:
            query = "SELECT * FROM public.orders WHERE id = %s"
            cur.execute(query, (order_id,))
            return cur.fetchone()

    def insert_order(self, customer_id, status, total_price, shipping_address):
        """Insert a new order into the 'orders' table."""
        with self.conn.cursor() as cur:
            query = """
                INSERT INTO orders (customer_id, status, total_price, shipping_address, created_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            cur.execute(query, (customer_id, status, total_price, shipping_address))
            self.conn.commit()

    def update_order(self, order_id, status=None, total_price=None, shipping_address=None):
        """Update an existing order in the 'orders' table."""
        updates = []
        values = []
        
        if status:
            updates.append("status = %s")
            values.append(status)
        
        if total_price:
            updates.append("total_price = %s")
            values.append(total_price)
        
        if shipping_address:
            updates.append("shipping_address = %s")
            values.append(shipping_address)
        
        if updates:
            query = f"UPDATE public.orders SET {', '.join(updates)} WHERE id = %s"
            values.append(order_id)
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(values))
                self.conn.commit()

    def delete_order(self, order_id):
        """Delete an order from the 'orders' table."""
        with self.conn.cursor() as cur:
            query = "DELETE FROM public.orders WHERE id = %s"
            cur.execute(query, (order_id,))
            self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()
