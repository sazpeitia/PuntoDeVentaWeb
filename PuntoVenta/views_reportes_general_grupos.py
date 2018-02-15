from django.shortcuts import render
from django.http import HttpResponse
from .models import PuntoventaCarrito, PuntoventaProducto, PuntoventaCategoria
from django.utils import timezone
import datetime
from django.db.models import F, FloatField, Sum
from django.db.models.functions import (
    TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth, TruncYear
    )



def reportes_general_grupos(request, negocio, reporte):

    if (request.method == 'POST'):
        fechaInicio = request.POST['fechaInicio']
        fechaFin = request.POST['fechaFin']
        fechaInicioDT = datetime.datetime.strptime(fechaInicio, '%Y-%m-%d')
        fechaFinDT = datetime.datetime.strptime(fechaFin, '%Y-%m-%d')

    else:

        fechaInicioDT=datetime.datetime.now()
        fechaFinDT=datetime.datetime.now()

        fechaYear=fechaInicioDT.strftime('%Y')
        fechaMonth=fechaInicioDT.strftime('%m')
        fechaDay=fechaInicioDT.strftime('%d')

        fechaInicio=fechaYear+"-"+fechaMonth+"-"+fechaDay
        fechaFin=fechaInicio

    fechaInicioRange=fechaInicioDT.replace(hour=00, minute=00, second=00, microsecond=000000)
    fechaFinRange=fechaFinDT.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Query para obtener el total de ventas por categoria y el total de ganancia
    categoriasGanancias = PuntoventaCarrito.objects.filter(
        id_venta__fecha_venta__range=[fechaInicioRange,fechaFinRange]
    ).annotate(
        day=TruncDay('id_venta__fecha_venta')
    ).values('day','id_producto__id_categoria__id_grupo__nombre_grupo'
    ).annotate(
        dayGrouped=TruncDay(F('id_venta__fecha_venta')
        ),
        total_ganancia=Sum(
            F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
        ),
        total_venta=Sum(
            'total'
        ),
        unidades_vendidas=Sum(
            'cantidad_producto'
        )
    ).order_by('-dayGrouped', '-total_ganancia')

    # Query para obtener el total de ventas y ganancia de todo
    ventaGanancia = PuntoventaCarrito.objects.filter(
        id_venta__fecha_venta__range=[fechaInicioRange,fechaFinRange]
    ).aggregate(
        total_ganancia=Sum(
            F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
        ),
        total_venta=Sum(
            F('cantidad_producto')*(F('id_producto__precio_venta'))
        )
    )

    context = {
        'categoriasGanancias' : categoriasGanancias,
        'negocio' : negocio,
        'reporte': reporte,
        'fechaInicio' : fechaInicio,
        'fechaFin' : fechaFin,
        'ventaGanancia' : ventaGanancia
    }

    return render(request, 'reportes_general_grupos.html', context)
