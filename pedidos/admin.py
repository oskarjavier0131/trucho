from django.contrib import admin
from .models import Pedido, LineaPedido


class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio', 'subtotal', 'created_at')
    can_delete = False

    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Subtotal'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'get_total')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'get_total')
    inlines = [LineaPedidoInline]
    ordering = ('-created_at',)

    def get_total(self, obj):
        return f"${obj.total}"
    get_total.short_description = 'Total'


@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio', 'get_subtotal', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('producto__nombre', 'pedido__id')
    readonly_fields = ('created_at', 'get_subtotal')
    ordering = ('-created_at',)

    def get_subtotal(self, obj):
        return obj.subtotal
    get_subtotal.short_description = 'Subtotal'

    