from pathlib import Path
import unittest
import json
import os

class CareerJSONTestCase(unittest.TestCase):

    def setUp(self):
        current_directory = Path(__file__).resolve().parent
        self.file_path =  current_directory.parent.parent/"data"/"career.json"

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.file_path), f"File '{self.file_path}' does not exist.")

    def test_file_contains_json(self):
        try:
            with open(self.file_path, 'r') as file:
                json_data = json.load(file)
            self.assertTrue(isinstance(json_data, dict), "File does not contain JSON data.")
        except FileNotFoundError:
            self.fail(f"Error reading JSON data from {self.file_path}")

    def test_json_contains_ge_3_questions(self):
        try:
            with open(self.file_path, 'r') as file:
                json_data = json.load(file)
            self.assertTrue(isinstance(json_data, dict), "File does not contain JSON data.")
            self.assertGreaterEqual(len(json_data), 3, "JSON data does not contain at least 3 questions.")
        except FileNotFoundError:
            self.fail(f"Error reading JSON data from {self.file_path}")

if __name__ == '__main__':
    unittest.main()
