import psycopg2
from datetime import datetime

class WorkOrders:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def insert_work_order(self, order_id, status, department, assigned_to=None, priority='Medium',
                          start_timestamp=None, end_timestamp=None, notes=None):
        # Set default timestamps if not provided
        if start_timestamp is None:
            start_timestamp = datetime.now()
        if end_timestamp is None:
            end_timestamp = start_timestamp  # Default end time to start time if not provided
        
        query = """
        INSERT INTO work_orders (
            order_id, status, department, assigned_to, priority,
            start_timestamp, end_timestamp, notes, created_at, last_updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        RETURNING id;
        """
        self.cursor.execute(query, (
            order_id, status, department, assigned_to, priority,
            start_timestamp, end_timestamp, notes
        ))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def fetch_all_work_orders(self):
        self.cursor.execute("SELECT * FROM work_orders;")
        return self.cursor.fetchall()

    def fetch_work_order_by_order_id(self, order_id):
        query = "SELECT * FROM work_orders WHERE order_id = %s;"
        self.cursor.execute(query, (order_id,))
        return self.cursor.fetchone()

    def update_status(self, work_order_id, new_status):
        query = """
        UPDATE work_orders SET status = %s, last_updated_at = NOW()
        WHERE id = %s;
        """
        self.cursor.execute(query, (new_status, work_order_id))
        self.conn.commit()

    def delete_work_order(self, work_order_id):
        self.cursor.execute("DELETE FROM work_orders WHERE id = %s;", (work_order_id,))
        self.conn.commit()
