from django.contrib import admin
from .models import CategoriaProd, Producto

class CategoriaProdAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "update")

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields =  ("created", "update")   

admin.site.register(CategoriaProd, CategoriaProdAdmin)    
admin.site.register(Producto, ProductoAdmin)


