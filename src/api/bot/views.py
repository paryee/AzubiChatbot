import json
from django.core.cache import cache
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import telegram

from bot.models import Area,FAQ

class TelegramBotView(APIView):

    def post(self,request,*args,**kwargs):
        bot = telegram.Bot(settings.BOT_TOKEN)
        update = telegram.Update.de_json(request.data, bot)

        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        query = cache.get(chat_id,{"area":None,"question":None})

        text = update.message.text.encode('utf-8').decode()
        
        if text == "/start":
            response = respond(start=True)
        else:
            if not query["area"]:
                query["area"] = text
            elif not query["question"]:
                query["question"] = text
            else:
                query["area"] = None
                query["question"] = None

            response = respond(**query)
            cache.set(chat_id,query)
        try:

            bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
        except Exception as e:
            pass

        return Response({"response":response})

class AppView(APIView):
    def post(self,request,*args,**kwargs):
        query = request.data
        response = respond(**query)
        return Response({"response":response})



def respond(area=None,question=None,start=False):
    """
    Respond to the user's query

    Args
    ----
    area: str
        The area
    question: str
        The area
    start: bool
        If this is supposed to be the first
        response
    
    Returns
    -------

    response: str
        The chatbot response
    """

    if start:
        message = "Hello and welcome to Azubi. I am AzubiGPT, here to answer all your questions.\nWhich area would you like to hear about?\n"
        areas = Area.objects.all().values_list("area",flat=True)
        area_list = "\n".join([f"{i}. {area.title()}" for i, area in enumerate(areas, 1)])
        return message + area_list
    
    # Check if no arguments are passed
    if not area and not question:
        message = "Which area would you like to hear about?\n"
        areas = Area.objects.all().values_list("area",flat=True)
        area_list = "\n".join([f"{i}. {area.title()}" for i, area in enumerate(areas, 1)])
        return message + area_list
    
    # Check if only the area argument is passed
    if area:
        try:
            area = Area.objects.get(area__icontains=area)
            
            if not question:
                questions = FAQ.objects.filter(area=area).values_list("question",flat=True)
                question_list = "\n".join([f"{i}. {q.capitalize()}" for i, q in enumerate(questions, 1)])
                return f"Here are a few FAQs in this area:\n{question_list}"
            else:
                question = FAQ.objects.get(area=area,question__icontains=question)
                return question.answer
            
        except Area.DoesNotExist as e:
            pass
        except FAQ.DoesNotExist as e:
            pass

    # Handle other cases or invalid input
    return "Sorry, I don't quite understand."