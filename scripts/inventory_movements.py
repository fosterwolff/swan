class InventoryMovements:
    def __init__(self, conn, parts_db):
        self.conn = conn
        self.parts_db = parts_db  # Store the Parts instance to interact with it
        

    def insert_inventory_movement(self, bom_id, order_id, change_type, quantity, part_id, remarks, transaction_type):
        """Insert an inventory movement."""
        with self.conn.cursor() as cur:
            query = """
                INSERT INTO inventory_movements (bom_id, order_id, change_type, quantity, part_id, remarks, transaction_type, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            cur.execute(query, (bom_id, order_id, change_type, quantity, part_id, remarks, transaction_type))
            self.conn.commit()
        
        # After inserting the movement, update the part's quantity
        if change_type == "Gained":
            self.parts_db.update_part_quantity(part_id, quantity)  # Increase quantity
        elif change_type == "Lost":
            self.parts_db.update_part_quantity(part_id, -quantity)  # Decrease quantity


    def fetch_inventory_movements_by_order(self, order_id):
        """Fetch all inventory movements for a given order."""
        with self.conn.cursor() as cur:
            query = "SELECT * FROM inventory_movements WHERE order_id = %s"
            cur.execute(query, (order_id,))
            return cur.fetchall()

    def fetch_inventory_movements_by_bom_id(self, bom_id):
        query = "SELECT * FROM inventory_movements WHERE bom_id = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (bom_id,))
            return cur.fetchall()


    def fetch_inventory_movements_by_part(self, part_id):
        """Fetch all inventory movements for a given part."""
        with self.conn.cursor() as cur:
            query = "SELECT * FROM inventory_movements WHERE part_id = %s"
            cur.execute(query, (part_id,))
            return cur.fetchall()
