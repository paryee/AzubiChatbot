from django.urls import path
from bot.views import TelegramBotView,AppView

urlpatterns = [
    path("", AppView.as_view(),name="app_view"),
    path("bot", TelegramBotView.as_view(),name="telegram_view")
]