from flask import Flask, request, jsonify, render_template
from datetime import datetime

from database import Database
from table import Table

app = Flask(__name__)

# Initialize the database
db = Database('school')


@app.route('/')
def index():
    return render_template('index.html')


# API: Create a new table
@app.route('/api/create_table', methods=['POST'])
def api_create_table():
    data = request.get_json()
    table_name = data.get('table_name')
    schema = data.get('schema')
    try:
        db.create_table(table_name, schema)
        return jsonify({"message": f"Table '{table_name}' created successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# API: Insert a new row into a table
@app.route('/api/insert_row', methods=['POST'])
def api_insert_row():
    data = request.get_json()
    table_name = data.get('table_name')
    row = data.get('row')
    try:
        table = db.get_table(table_name)
        table.insert(row)
        return jsonify({"message": "Row inserted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# API: Display the contents of a table
@app.route('/api/display_table/<table_name>', methods=['GET'])
def api_display_table(table_name):
    try:
        table = db.get_table(table_name)
        return jsonify({"schema": table.schema, "rows": table.display()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/product/<table1>/<table2>', methods=['GET'])
def api_product(table1, table2):
    try:
        result_rows = db.product(table1, table2)
        return jsonify({"rows": result_rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
