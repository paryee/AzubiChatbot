import os
import json
import pathlib
import requests
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv

load_dotenv()


class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("AzubiGPT Chatbot")

        # Create a scrolled text widget to display the conversation
        self.conversation_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
        self.conversation_text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Create an entry widget for user input
        self.user_input = tk.Entry(root, width=40)
        self.user_input.grid(row=3, column=0, padx=10, pady=5, columnspan=2)
        self.user_input.bind("<Return>", self.send_user_input)

        # Create a button to send user input
        self.send_button = tk.Button(root, text="Send", command=self.send_user_input)
        self.send_button.grid(row=3, column=2, padx=10, pady=5)

        self.area = None
        self.question = None

        response = self.respond(self.area, self.question, True)
        self.conversation_text.insert(tk.END, f"AzubiGPT: {response}\n\n")
    
    def load_data(self):
        # Define and return the dictionary with responses
        data_dir = pathlib.Path(__file__).parent.parent/"data"

        responses = {}

        area_json = {
            "Career Opportunities": "career.json",
            "Eligibility Criteria": "criteria.json",
            "Curriculum": "curriculum.json",
            "Payment Options": "payment.json",
            "Program Duration": "program_duration.json"
        }

        for area in area_json:
            with open(data_dir/area_json[area]) as f:
                responses[area] = json.loads(f.read())

        return responses

    def respond(self,area=None, question=None, start=False):
        url = os.environ.get("SERVER_URL")
        
        response = requests.post(url,json={"start":start,"area":area,"question":question})
        response = response.json()
        return response["response"]
        
        
    def send_user_input(self, event=None):
        
        user_input = self.user_input.get()

        if not user_input:
            return
        
        self.conversation_text.insert(tk.END, f"User: {user_input}\n\n")

        if not self.area:
            self.area = user_input
        elif not self.question:
            self.question = user_input
            response = self.respond(self.area, self.question)
            self.conversation_text.insert(tk.END, f"AzubiGPT: {response}\n\n")
            
            self.area = None
            self.question = None

        response = self.respond(self.area, self.question)
        self.conversation_text.insert(tk.END, f"AzubiGPT: {response}\n\n")
        
        if response[0:5] == "Sorry":
            self.area = None
            self.question = None
            
        self.conversation_text.see(tk.END)
        self.user_input.delete(0, tk.END)
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Chatbot(root)
    root.mainloop()
