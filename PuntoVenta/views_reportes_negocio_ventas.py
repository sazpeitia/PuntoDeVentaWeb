from django.shortcuts import render
from django.http import HttpResponse
from .models import PuntoventaCarrito, PuntoventaProducto, PuntoventaCategoria, PuntoventaHistoriaInventario
from django.utils import timezone
import datetime
from django.db.models import F, Q, FloatField, Sum
from django.db.models.functions import (
    TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth, TruncYear
    )



def reportes_negocio_ventas(request, negocio, reporte):

    try:
        fechaInicio = request.POST['fechaInicio']
        fechaFin = request.POST['fechaFin']
        fechaInicioDT = datetime.datetime.strptime(fechaInicio, '%Y-%m-%d')
        fechaFinDT = datetime.datetime.strptime(fechaFin, '%Y-%m-%d')

    except KeyError:

        fechaInicioDT=datetime.datetime.now()
        fechaFinDT=datetime.datetime.now()

        fechaYear=fechaInicioDT.strftime('%Y')
        fechaMonth=fechaInicioDT.strftime('%m')
        fechaDay=fechaInicioDT.strftime('%d')

        fechaInicio=fechaYear+"-"+fechaMonth+"-"+fechaDay
        fechaFin=fechaInicio

    fechaInicioRange=fechaInicioDT.replace(hour=00, minute=00, second=00, microsecond=000000)
    fechaFinRange=fechaFinDT.replace(hour=23, minute=59, second=59, microsecond=999999)

    negocio = negocio.replace("/", "")

    categoriasList = list(PuntoventaCategoria.objects.filter(id_categoria_padre__nombre_categoria=negocio).values('nombre_categoria'))

    categoriasStringList =  [o['nombre_categoria'] for o in categoriasList]
    categoriasStringList.extend([negocio])


    # Query para obtener las ventas realizadas y el producto comprado
    ventas = PuntoventaCarrito.objects.filter(
        id_venta__fecha_venta__range=[fechaInicioRange,fechaFinRange]).filter(
            id_producto__id_categoria__nombre_categoria__in=categoriasStringList
        ).annotate(
            ganancia=Sum(
                F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
                )
            #).order_by('-id_venta__fecha_venta', 'id_producto__id_categoria__nombre_categoria', 'id_producto__nombre_producto')
            ).order_by('-id_venta__fecha_venta', '-total')

    # Query para obtener las ganancias y el total de ventas
    ganancias = PuntoventaCarrito.objects.filter(
        id_venta__fecha_venta__range=[fechaInicioRange,fechaFinRange]).filter(
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
        id_venta__fecha_venta__range=[fechaInicioRange,fechaFinRange]
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
    ).order_by('-total_venta')


    context = {
        'ventas':ventas,
        'ganancias': ganancias,
        'categoriasGanancias' : categoriasGanancias,
        'negocio' : negocio,
        'reporte': reporte,
        'fechaInicio' : fechaInicio,
        'fechaFin' : fechaFin
    }

    return render(request, 'reportes_negocio_ventas.html', context)
