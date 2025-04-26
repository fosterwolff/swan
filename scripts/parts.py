class Parts:
    def __init__(self, conn):
        self.conn = conn

    def fetch_all_parts(self):
        """Fetch all parts."""
        with self.conn.cursor() as cur:
            query = "SELECT id, name, part_number, unit_cost, supplier_id, amount FROM parts"
            cur.execute(query)
            return cur.fetchall()

    def fetch_part_by_id(self, part_id):
        """Fetch a part by its ID."""
        with self.conn.cursor() as cur:
            query = "SELECT id, name, part_number, unit_cost, supplier_id, amount FROM parts WHERE id = %s"
            cur.execute(query, (part_id,))
            return cur.fetchone()

    def insert_part(self, name, part_number, unit_cost, supplier_id, amount):
        """
        Insert a new part into the 'parts' table, checking for duplicate part numbers.
        """
        # Check if the part already exists by part_number
        with self.conn.cursor() as cur:
            query = "SELECT id FROM parts WHERE part_number = %s"
            cur.execute(query, (part_number,))
            existing_part = cur.fetchone()

            if existing_part:
                print(f"Part with part_number '{part_number}' already exists.")
                return  # Skip insertion or update if necessary
            
            # If part doesn't exist, insert it
            query = """
            INSERT INTO parts (name, part_number, unit_cost, supplier_id, amount)
            VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(query, (name, part_number, unit_cost, supplier_id, amount))
            self.conn.commit()
            print(f"Part '{part_number}' inserted successfully.")

    def update_part(self, part_id, name=None, part_number=None, unit_cost=None, supplier_id=None, amount=None):
        """Update an existing part."""
        updates = []
        values = []

        if name:
            updates.append("name = %s")
            values.append(name)
        if part_number:
            updates.append("part_number = %s")
            values.append(part_number)
        if unit_cost:
            updates.append("unit_cost = %s")
            values.append(unit_cost)
        if supplier_id:
            updates.append("supplier_id = %s")
            values.append(supplier_id)
        if amount is not None:
            updates.append("amount = %s")
            values.append(amount)

        if updates:
            query = f"UPDATE parts SET {', '.join(updates)} WHERE id = %s"
            values.append(part_id)
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(values))
                self.conn.commit()

    def update_part_quantity(self, part_id, quantity):
        """Update the amount (quantity) of a part."""
        with self.conn.cursor() as cur:
            query = "UPDATE parts SET amount = amount + %s WHERE id = %s"
            cur.execute(query, (quantity, part_id))
            self.conn.commit()
