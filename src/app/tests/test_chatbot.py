import sys
import json
import pathlib
import unittest
import tkinter as tk

APP_DIR = pathlib.Path(__file__).parent.parent
sys.path.append(str(APP_DIR))

from chatbot import Chatbot


class ChatbotTestCase(unittest.TestCase):

    def setUp(self):
        self.areas = [
            "Eligibility Criteria",
            "Payment Options",
            "Career Opportunities",
            "Curriculum",
            "Program Duration"]
        
        data_dir = APP_DIR.parent/"data/"
        self.duration_file = data_dir/"program_duration.json"
        
        with open(self.duration_file,"r") as f:
            self.data = {"Program Duration": json.loads(f.read())}
        
        root = tk.Tk()
        self.chatbot = Chatbot(root)

    def test_load_function(self):
        """Test `load_data` function"""

        data = self.chatbot.load_data()
        areas = list(data.keys())

        with self.subTest("Result is a dict"):
            self.assertIsInstance(data,dict)
        
        with self.subTest("Result contains the correct number of areas"):
            
            self.assertEqual(len(areas),len(self.areas))

        for area in areas:
            with self.subTest(f"Result contains {area} with a least 2 questions"):
                self.assertIn(area,self.areas)
                self.assertGreater(len(data[area]),2)
    

    def test_respond_function(self):
        """Test `respond` function"""

        with self.subTest("Returns the hello message when only start == True"):
            response = self.chatbot.respond(start=True)
            self.assertTrue(response)
            self.assertEqual("Hello", response[0:5])
        
        with self.subTest("Returns the area select message without any arguments"):
            response = self.chatbot.respond()
            self.assertTrue(response)
            self.assertEqual("Which", response[0:5])

        for area in self.data:
            with self.subTest(f"Returns questions for each area when only area is passed"):
                response = self.chatbot.respond(area)
                self.assertTrue(response)
                self.assertEqual("Here", response[0:4])

        for area in self.data:
            for question in self.data[area]:
                with self.subTest(f"Answer to {area} - {question} is correct"):
                    response = self.chatbot.respond(area,question)
                    self.assertTrue(response)
                    self.assertEqual(response,self.data[area][question])
        
        with self.subTest("Returns the sorry message with invalid arguments"):
            response = self.chatbot.respond("invalid")
            self.assertTrue(response)
            self.assertEqual("Sorry", response[0:5])


if __name__ == "__main__":
    unittest.main()