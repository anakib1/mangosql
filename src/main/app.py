from flask import Flask, request, jsonify, render_template
from datetime import datetime
from database import Database

app = Flask(__name__)

# Initialize the database
db = Database()


@app.route('/')
def index():
    return render_template('index.html')


# Route for creating a new table
@app.route('/create_table', methods=['POST'])
def create_table():
    table_name = request.form.get('table_name')
    schema = request.form.get('schema')  # Expected format: {"col1": "integer", "col2": "string"}
    try:
        schema_dict = eval(schema)  # You can replace this with a more secure parser
        db.create_table(table_name, schema_dict)
        return jsonify({"message": f"Table {table_name} created successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route for inserting data into a table
@app.route('/insert_row', methods=['POST'])
def insert_row():
    table_name = request.form.get('table_name')
    row_data = request.form.get('row')  # Expected format: {"col1": 1, "col2": "Alice"}
    try:
        row_dict = eval(row_data)
        table = db.get_table(table_name)
        table.insert(row_dict)
        return jsonify({"message": "Row inserted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Route for displaying the contents of a table
@app.route('/display_table/<table_name>', methods=['GET'])
def display_table(table_name):
    try:
        table = db.get_table(table_name)
        schema = table.schema.keys()  # Column names
        rows = table.display()  # Table rows
        return render_template('display_table.html', table_name=table_name, schema=schema, rows=rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
