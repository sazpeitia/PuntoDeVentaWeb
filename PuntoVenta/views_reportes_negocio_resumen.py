from django.shortcuts import render
from django.http import HttpResponse
from .models import PuntoventaCarrito, PuntoventaProducto, PuntoventaCategoria, PuntoventaHistoriaInventario
from django.utils import timezone
import datetime
from django.db.models import F, Q, FloatField, Sum
from django.db.models.functions import (
    TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth, TruncYear
    )


def reportes_negocio_resumen(request, negocio, reporte):

    if (request.method == 'POST'):
        radioRango = request.POST['radioRango']
        if ( radioRango == 'radioRango1' ):
            fechaInicio = request.POST['fechaInicio']
            fechaFin = request.POST['fechaFin']
            fechaInicioDT = datetime.datetime.strptime(fechaInicio, '%Y-%m-%d')
            fechaFinDT = datetime.datetime.strptime(fechaFin, '%Y-%m-%d')
            TipoAgrupacion = "PorRango"
        else:
            now = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
            day=str(now.day).zfill(2)
            month=str(now.month).zfill(2)
            year=str(now.year)
            fechaInicio=year+"-"+month+"-"+day
            fechaFin=fechaInicio
            TipoAgrupacion = request.POST['TipoAgrupacion']

    else:
        now = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
        day=str(now.day).zfill(2)
        month=str(now.month).zfill(2)
        year=str(now.year)
        fechaInicio=year+"-"+month+"-"+day
        fechaFin=fechaInicio
        TipoAgrupacion = "PorDia"

    negocio = negocio.replace("/", "")

    categoriasList = list(PuntoventaCategoria.objects.filter(id_categoria_padre__nombre_categoria=negocio).values('nombre_categoria'))

    categoriasStringList =  [o['nombre_categoria'] for o in categoriasList]
    categoriasStringList.extend([negocio])


    if ( TipoAgrupacion == 'PorDia' ):
        print "-------> POR DIA"
        # Query para obtener las ganancias y el total de ventas agrupado por dia del mes actual
        ganancias = PuntoventaCarrito.objects.filter(
            Q(id_venta__fecha_venta__month=now.month) &
            Q(id_venta__fecha_venta__year=now.year)
        ).filter(
                id_producto__id_categoria__nombre_categoria__in=categoriasStringList
        ).annotate(
            day=TruncDay('id_venta__fecha_venta')
        ).values('day'
        ).annotate(
            dayGrouped=TruncDay('id_venta__fecha_venta'),
            total_ganancia=Sum(
                F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
            ),
            total_venta=Sum(
                'total'
            )
        ).order_by('dayGrouped')

    if ( TipoAgrupacion == 'PorMes' ):
        print "-------> POR MES"
        # Query para obtener las ganancias y el total de ventas agrupado por mes del ano actual
        ganancias = PuntoventaCarrito.objects.filter(
            id_venta__fecha_venta__year=now.year).filter(
                id_producto__id_categoria__nombre_categoria__in=categoriasStringList
        ).annotate(
            day=TruncMonth('id_venta__fecha_venta')
        ).values('day'
        ).annotate(
            dayGrouped=TruncMonth('id_venta__fecha_venta'),
            total_ganancia=Sum(
                F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
            ),
            total_venta=Sum(
                'total'
            )
        ).order_by('dayGrouped')

    if ( TipoAgrupacion == 'PorAno' ):
        print "-------> POR ANO"
        # Query para obtener las ganancias y el total de ventas agrupado por ano
        ganancias = PuntoventaCarrito.objects.filter(
                id_producto__id_categoria__nombre_categoria__in=categoriasStringList
        ).annotate(
            day=TruncYear('id_venta__fecha_venta')
        ).values('day'
        ).annotate(
            dayGrouped=TruncYear('id_venta__fecha_venta'),
            total_ganancia=Sum(
                F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
            ),
            total_venta=Sum(
                'total'
            )
        ).order_by('dayGrouped')

    if ( TipoAgrupacion == 'PorRango' ):
        print "-------> POR RANGO"
        # Query para obtener las ganancias y el total de ventas
        ganancias = PuntoventaCarrito.objects.filter(
            id_venta__fecha_venta__range=[fechaInicio,fechaFin]).filter(
                id_producto__id_categoria__nombre_categoria__in=categoriasStringList
        ).annotate(
            day=TruncDay('id_venta__fecha_venta')
        ).values('day'
        ).annotate(
            dayGrouped=TruncDay('id_venta__fecha_venta'),
            total_ganancia=Sum(
                F('cantidad_producto')*(F('id_producto__precio_venta')-F('id_producto__precio_compra')), output_field=FloatField()
            ),
            total_venta=Sum(
                'total'
            )
        ).order_by('dayGrouped')


    context = {

        'ganancias': ganancias,
        'negocio' : negocio,
        'reporte': reporte,
        'fechaInicio' : fechaInicio,
        'fechaFin' : fechaFin,
        'TipoAgrupacion' : TipoAgrupacion
    }

    return render(request, 'reportes_negocio_resumen.html', context)
