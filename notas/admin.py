from django.contrib import admin
from .models import Categoria, Notas


class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


class NotasaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Notas, NotasaAdmin)
