from table import Table
import json
import os


class Database:
    def __init__(self, name: str):
        self.tables = {}
        self.name = name
        self.filename = f'{self.name}.json'
        self.load_from_json()

    def create_table(self, name, schema):
        """
        Creates a new table in the database with a schema.
        """
        if name in self.tables:
            raise ValueError(f"Table {name} already exists.")
        self.tables[name] = Table(self, name, schema)

    def get_table(self, name):
        """
        Retrieves a table by its name.
        """
        if name not in self.tables:
            raise ValueError(f"Table {name} does not exist.")
        return self.tables[name]

    def product(self, table1_name, table2_name):
        """
        Performs a product of two tables and returns a new Table.
        """
        table1 = self.get_table(table1_name)
        table2 = self.get_table(table2_name)

        # Combine schemas
        new_schema = {**table1.schema, **table2.schema}
        new_table = Table(self, f"product_{table1_name}_{table2_name}", new_schema)

        # Cross product of rows
        for row1 in table1.rows:
            for row2 in table2.rows:
                combined_row = {**row1, **row2}
                new_table.insert(combined_row)

        return new_table.display()

    def save_to_json(self):
        """
        Serializes the database (tables and rows) to a JSON file.
        """
        data = {}
        for table_name, table in self.tables.items():
            data[table_name] = {
                "schema": table.schema,
                "rows": table.display()
            }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

        return f"Database saved to {self.filename}"

    def load_from_json(self):
        """
        Loads the database from the JSON file and reconstructs the tables and rows.
        """
        if not os.path.exists(self.filename):
            print(f"No existing database found, starting with a fresh database.")
            return

        with open(self.filename, 'r') as f:
            data = json.load(f)

        for table_name, table_data in data.items():
            schema = table_data['schema']
            rows = table_data['rows']

            # Recreate the table with its schema
            self.tables[table_name] = Table(self, table_name, schema)

            # Insert the rows into the table
            for row in rows:
                self.tables[table_name].insert(row)

        print(f"Database loaded from {self.filename}")
