from django.contrib import admin
from .models import Coffee
# Register your models here.

class CoffeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity',)
   
admin.site.register(Coffee, CoffeAdmin)  # Assuming you have a model named Coffe in models.py