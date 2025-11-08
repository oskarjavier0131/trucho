from django.contrib import admin
from .models import CategoriaProd, Producto


@admin.register(CategoriaProd)
class CategoriaProdAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created', 'updated')
    search_fields = ('nombre',)
    readonly_fields = ('created', 'updated')
    ordering = ('-created',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categorias', 'precio', 'disponibilidad', 'created')
    list_filter = ('disponibilidad', 'categorias', 'created')
    search_fields = ('nombre',)
    readonly_fields = ('created', 'updated')
    list_editable = ('disponibilidad', 'precio')
    ordering = ('-created',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'categorias', 'precio', 'disponibilidad')
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
        ('Metadatos', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )


