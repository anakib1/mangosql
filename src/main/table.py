from datetime import datetime


class Table:
    def __init__(self, db, name, schema):
        """
        Initializes the table with a name and schema (dictionary of column_name: data_type).
        """
        self.name = name
        self.schema = schema  # A dictionary like {"id": "integer", "name": "string"}
        self.rows = []
        self.db = db

    def insert(self, row):
        """
        Inserts a row (dictionary of column_name: value) into the table.
        """
        # Validate the row matches the schema
        if len(row) != len(self.schema):
            raise ValueError("Row length does not match table schema")

        for col, value in row.items():
            if col not in self.schema:
                raise ValueError(f"Column {col} not in schema")
            if not self._validate_type(self.schema[col], value):
                raise ValueError(f"Invalid data type for column {col}. Given: {value}")

        self.rows.append(row)
        self.db.save_to_json()

    def _validate_type(self, expected_type, value):
        """
        Validates the data type of the value against the expected type from the schema.
        """
        if expected_type == "integer" and not isinstance(value, int):
            return False
        elif expected_type == "real" and not isinstance(value, float):
            return False
        elif expected_type == "char" and not isinstance(value, str) and len(value) != 1:
            return False
        elif expected_type == "string" and not isinstance(value, str):
            return False
        elif expected_type == "date" and not isinstance(value, datetime):
            return False
        return True

    def display(self):
        return self.rows

    def __str__(self):
        """
        Displays the table content in a tabular form.
        """
        print(f"Table: {self.name}")
        print(" | ".join(self.schema.keys()))
        print("-" * 40)
        for row in self.rows:
            print(" | ".join(str(row[col]) for col in self.schema.keys()))
