class TableSchema:
    def __init__(self, columns):
        """
        Initializes schema with columns (a dictionary of column_name: data_type).
        """
        self.columns = columns
