from django.contrib import admin
from .models import Package, ShoppingCard,PurchesHistory, TotalPrice,Ticket




admin.site.register(Package)
admin.site.register(ShoppingCard)
admin.site.register(PurchesHistory)
admin.site.register(Ticket)
admin.site.register(TotalPrice)


