from django.contrib import admin
from .models import PuntoventaCategoria, PuntoventaProducto, PuntoventaVenta, PuntoventaCarrito

# Register your models here.

class PuntoventaCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria', 'id_categoria_padre')
    search_fields = [ 'nombre_categoria' ]


class PuntoventaProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre_producto', 'id_categoria', 'precio_compra', 'precio_venta', 'cantidad_disponible', 'id_codigo_barra']
    search_fields = [ 'nombre_producto', 'id_categoria__nombre_categoria', 'id_categoria__id_categoria_padre__nombre_categoria' ]

class PuntoventaCarritoAdmin(admin.ModelAdmin):
    list_display = [ 'id_venta', 'get_nombre_producto', 'get_fecha_venta' ]
    search_fields = [ 'id_venta__fecha_venta', 'id_producto__nombre_producto' ]

    def get_nombre_producto(self, obj):
        return obj.id_producto.nombre_producto

    get_nombre_producto.short_description = 'Nombre Producto'

    def get_fecha_venta(self, obj):
        return obj.id_venta.fecha_venta

    get_fecha_venta.admin_order_field  = '-fecha_venta'
    get_fecha_venta.short_description = 'Fecha Venta'

class PuntoventaCarritoInline(admin.TabularInline):
    model = PuntoventaCarrito

class PuntoventaVentaAdmin(admin.ModelAdmin):
    list_display = [ 'id_venta', 'fecha_venta', 'total_venta']
    inlines = [
        PuntoventaCarritoInline
    ]





admin.site.register(PuntoventaCategoria, PuntoventaCategoriaAdmin)
admin.site.register(PuntoventaProducto,PuntoventaProductoAdmin)
admin.site.register(PuntoventaCarrito,PuntoventaCarritoAdmin)
admin.site.register(PuntoventaVenta,PuntoventaVentaAdmin)
