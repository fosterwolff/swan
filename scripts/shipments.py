class Shipments:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def insert_shipment(self, carrier, tracking_number, status='Pending', shipped_at=None, delivered_at=None, notes=None):
        query = """
        INSERT INTO shipments (carrier, tracking_number, status, shipped_at, delivered_at, notes)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        self.cursor.execute(query, (carrier, tracking_number, status, shipped_at, delivered_at, notes))
        shipment_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return shipment_id

    def assign_order_to_shipment(self, order_id, shipment_id):
        query = "UPDATE orders SET shipment_id = %s WHERE id = %s;"
        self.cursor.execute(query, (shipment_id, order_id))
        self.conn.commit()

    def fetch_orders_by_shipment(self, shipment_id):
        query = "SELECT * FROM orders WHERE shipment_id = %s;"
        self.cursor.execute(query, (shipment_id,))
        return self.cursor.fetchall()

    def update_status(self, shipment_id, new_status):
        query = "UPDATE shipments SET status = %s WHERE id = %s;"
        self.cursor.execute(query, (new_status, shipment_id))
        self.conn.commit()

    def delete_shipment(self, shipment_id):
        query = "DELETE FROM shipments WHERE id = %s;"
        self.cursor.execute(query, (shipment_id,))
        self.conn.commit()
