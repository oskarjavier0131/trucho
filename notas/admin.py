from django.contrib import admin
from .models import Categoria, Notas


class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'update')


class NotasaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'update')


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Notas, NotasaAdmin)
