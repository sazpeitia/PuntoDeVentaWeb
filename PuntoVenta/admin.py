from django.contrib import admin
from .models import PuntoventaCategoria, PuntoventaProducto, PuntoventaVenta

# Register your models here.

class PuntoventaCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria', 'id_categoria_padre')
    search_fields = [ 'nombre_categoria' ]


class PuntoventaProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre_producto', 'id_categoria', 'precio_compra', 'precio_venta', 'cantidad_disponible', 'id_codigo_barra']
    search_fields = [ 'nombre_producto', 'id_categoria__nombre_categoria', 'id_categoria__id_categoria_padre__nombre_categoria' ]


admin.site.register(PuntoventaCategoria, PuntoventaCategoriaAdmin)
admin.site.register(PuntoventaProducto,PuntoventaProductoAdmin)

admin.site.register(PuntoventaVenta)
