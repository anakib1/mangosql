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

        print(row)
        print(self.schema)
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
        elif expected_type == "real" and not isinstance(value, (int, float)):
            return False
        elif expected_type == "char" and not isinstance(value, str) and len(value) != 1:
            return False
        elif expected_type == "string" and not isinstance(value, str):
            return False
        elif expected_type == "date":
            try:
                datetime.strptime(value, "%d.%m.%Y")  # Adjust format as needed
                return True
            except ValueError:
                return False
        elif expected_type == "dateInterval":
            try:
                start_date_str, end_date_str = value.split(";")
                start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
                end_date = datetime.strptime(end_date_str, "%d.%m.%Y")
                return start_date < end_date  # Ensure the first date is earlier than the second
            except (ValueError, IndexError):
                return False
        return True

    def delete_row(self, condition):
        """
        Deletes a row from the table based on the condition provided.
        Condition should be a dictionary with column name and value to match.
        """
        column, value = next(iter(condition.items()))  # Assuming one condition for simplicity
        if column not in self.schema:
            raise ValueError(f"Column {column} does not exist in the table schema.")

        # Find the row that matches the condition
        initial_row_count = len(self.rows)
        self.rows = [row for row in self.rows if row.get(column) != value]

        if len(self.rows) == initial_row_count:
            raise ValueError(f"No row found matching {condition}")

        return f"Row where {condition} has been deleted."

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
