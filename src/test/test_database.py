import unittest
from database import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.db.create_table("students", {"id": "integer", "name": "string", "gpa": "real"})
        self.db.get_table("students").insert({"id": 1, "name": "Alice", "gpa": 3.5})

    def test_insert(self):
        table = self.db.get_table("students")
        self.assertEqual(len(table.rows), 1)
        table.insert({"id": 2, "name": "Bob", "gpa": 3.7})
        self.assertEqual(len(table.rows), 2)

    def test_invalid_insert(self):
        table = self.db.get_table("students")
        with self.assertRaises(ValueError):
            table.insert({"id": "one", "name": "Alice", "gpa": "three"})

    def test_product(self):
        self.db.create_table("courses", {"course_id": "integer", "course_name": "string"})
        self.db.get_table("courses").insert({"course_id": 101, "course_name": "Math"})
        product_table = self.db.product("students", "courses")
        self.assertEqual(len(product_table.rows), 1)


if __name__ == '__main__':
    unittest.main()
