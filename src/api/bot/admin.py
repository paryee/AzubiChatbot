from django.contrib import admin

from bot.models import Area,FAQ

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass