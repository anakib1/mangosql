from table import Table


class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, schema):
        """
        Creates a new table in the database with a schema.
        """
        if name in self.tables:
            raise ValueError(f"Table {name} already exists.")
        self.tables[name] = Table(name, schema)

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
        new_table = Table(f"product_{table1_name}_{table2_name}", new_schema)

        # Cross product of rows
        for row1 in table1.rows:
            for row2 in table2.rows:
                combined_row = {**row1, **row2}
                new_table.insert(combined_row)

        return new_table
