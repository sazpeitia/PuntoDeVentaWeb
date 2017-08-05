from django.shortcuts import render
from django.http import HttpResponse
from .models import PuntoventaCarrito, PuntoventaProducto, PuntoventaCategoria
from django.utils import timezone
import datetime
from django.db.models import F, FloatField, Sum
#from datetime import datetime, timedelta, time



# Create your views here.
def index(request):

    return negocio_ventas(request, 'PAPELERIA')

def negocio_ventas(request, negocio):

    if (request.method == 'POST'):
        fechaInicio = request.POST['fechaInicio']
        fechaFin = request.POST['fechaFin']

    else:
        now = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
        day=str(now.day).zfill(2)
        month=str(now.month).zfill(2)
        year=str(now.year)
        fechaInicio=year+"-"+month+"-"+day
        fechaFin=fechaInicio

    negocio = negocio.replace("/", "")

    categoriasList = list(PuntoventaCategoria.objects.filter(id_categoria_padre__nombre_categoria=negocio).values('nombre_categoria'))

    categoriasStringList =  [o['nombre_categoria'] for o in categoriasList]
    categoriasStringList.extend([negocio])


    # Query para obtener las ventas realizadas y el producto comprado
    ventas = PuntoventaCarrito.objects.filter(
        id_venta__fecha_venta__range=[fechaInicio,fechaFin]).filter(
            id_producto__id_categoria__nombre_categoria__in=categoriasStringList
        ).annotate(
            ganancia=Sum(
                F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
                )
            ).order_by('-id_venta__fecha_venta', 'id_producto__id_categoria__nombre_categoria', 'id_producto__nombre_producto')

    # Query para obtener las ganancias y el total de ventas
    ganancias = PuntoventaCarrito.objects.filter(
        id_venta__fecha_venta__range=[fechaInicio,fechaFin]).filter(
            id_producto__id_categoria__nombre_categoria__in=categoriasStringList
    ).aggregate(
        total_ganancia=Sum(
            F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
        ),
        total_venta=Sum(
            'total'
        )
    )

    # Query para obtener el total de ventas por categoria y el total de ganancia
    categoriasGanancias = PuntoventaCarrito.objects.filter(
        id_venta__fecha_venta__range=[fechaInicio,fechaFin]
    ).filter(
        id_producto__id_categoria__nombre_categoria__in=categoriasStringList
    ).values(
        'id_producto__id_categoria__nombre_categoria'
    ).annotate(
        total_venta=Sum(
            'total'
        ),
        total_ganancia=Sum(
            F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
        )
    ).order_by('-total_ganancia')

    print categoriasGanancias

    context = {
        'ventas':ventas,
        'ganancias': ganancias,
        'categoriasGanancias' : categoriasGanancias,
        'negocio' : negocio,
        'fechaInicio' : fechaInicio,
        'fechaFin' : fechaFin
    }

    return render(request, 'negocio_resumen_ventas.html', context)
