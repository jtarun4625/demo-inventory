from django.contrib import admin
from Inventory.models import Company, Product, Purchase


# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "code"]

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["code","Product_price","Purchase_price","stock","units","company"]

admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase,PurchaseAdmin)
