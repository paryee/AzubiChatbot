from datetime import datetime
from rest_framework.test import APITestCase
from django.urls import reverse
import telegram

from bot.models import Area,FAQ

class BotViewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.area = Area.objects.create(area="test area")
        cls.faq = FAQ.objects.create(area=cls.area,
                                     question="test question",
                                     answer="test answer")


    
    def test_respond_start(self):
        with self.subTest("With Appview"):
            url = reverse("app_view")
            response = self.client.post(url,{"start":True},"json")

            self.assertEqual(response.status_code,200)
            
            response = response.json()["response"].lower()

            self.assertTrue(response.lower().startswith("hello"))
            self.assertIn("test area", response)

        with self.subTest("With TelegramView"):
            url = reverse("telegram_view")
            print(url)

            chat = telegram.Chat(1,"private")
            message = telegram.Message(1,datetime.now(),chat,text="/start")
            update = telegram.Update(1,message)

            response = self.client.post(url,update.to_dict(),"json")

            self.assertEqual(response.status_code,200)

            response = response.json()["response"].lower()

            self.assertTrue(response.lower().startswith("hello"))
            self.assertIn("test area", response)
            

    def test_respond_no_start(self):
        with self.subTest("With Appview"):
            url = reverse("app_view")
            response = self.client.post(url,{"start":False},"json")

            self.assertEqual(response.status_code,200)
            
            response = response.json()["response"].lower()

            self.assertFalse(response.lower().startswith("hello"))
            self.assertIn("test area", response)
        
        with self.subTest("With TelegramView"):
            url = reverse("telegram_view")

            chat = telegram.Chat(1,"private")
            message = telegram.Message(1,datetime.now(),chat,text="")
            update = telegram.Update(1,message)

            response = self.client.post(url,update.to_dict(),"json")

            self.assertEqual(response.status_code,200)

            response = response.json()["response"].lower()

            self.assertFalse(response.lower().startswith("hello"))
            self.assertIn("test area", response)
    

    def test_respond_area(self):
        url = reverse("app_view")
        response = self.client.post(url,{"area": "test area"},"json")

        self.assertEqual(response.status_code,200)
        
        response = response.json()["response"].lower()

        self.assertIn("test question", response)
    

    def test_respond_area(self):
        url = reverse("app_view")
        response = self.client.post(url,{"area": "test area"},"json")

        self.assertEqual(response.status_code,200)
        
        response = response.json()["response"].lower()

        self.assertIn("test question", response)
    
    def test_respond_question(self):
        url = reverse("app_view")
        response = self.client.post(url,{"area": "test area","question": "test question"},"json")

        self.assertEqual(response.status_code,200)
        
        response = response.json()["response"].lower()

        self.assertIn("test answer", response)
    

    def test_respond_invalid(self):
        url = reverse("app_view")
        response = self.client.post(url,{"area": "invalid test"},"json")

        self.assertEqual(response.status_code,200)
        
        response = response.json()["response"].lower()

        self.assertTrue(response.lower().startswith("sorry"))
    

