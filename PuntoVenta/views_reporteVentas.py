from django.shortcuts import render
from django.http import HttpResponse
from .models import PuntoventaCarrito, PuntoventaProducto, PuntoventaCategoria, PuntoventaHistoriaInventario
from django.utils import timezone
import datetime
from django.db.models import F, Q, FloatField, Sum
from django.db.models.functions import (
    TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth, TruncYear
    )



def reporte_ventas_dia(request, negocio, reporte):

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

    print categoriasGanancias

    context = {
        'ventas':ventas,
        'ganancias': ganancias,
        'categoriasGanancias' : categoriasGanancias,
        'negocio' : negocio,
        'reporte': reporte,
        'fechaInicio' : fechaInicio,
        'fechaFin' : fechaFin
    }

    return render(request, 'negocio_resumen_ventas.html', context)


def reporte_reporte_vetnas(request, negocio, reporte):

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

    return render(request, 'negocio_resumen_ventas.html', context)


def reporte_reporte_compras(request, negocio, reporte):

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

    negocio = negocio.replace("/", "")

    categoriasList = list(PuntoventaCategoria.objects.filter(id_categoria_padre__nombre_categoria=negocio).values('nombre_categoria'))

    categoriasStringList =  [o['nombre_categoria'] for o in categoriasList]
    categoriasStringList.extend([negocio])


    # Query para obtener el historial del inventario
    compras = PuntoventaHistoriaInventario.objects.filter(
            fecha_registro__range=[fechaInicioRange,fechaFinRange]
        ).filter(
            id_producto__id_categoria__nombre_categoria__in=categoriasStringList
        ).filter(
            cantidad_adicionada__gte=0
        ).annotate(
            total_compra=Sum(
                    F('cantidad_adicionada')*(F('id_producto__precio_compra')), output_field=FloatField()
                )
        ).order_by('-fecha_registro')

    print compras

    context = {
        'compras' : compras,
        'negocio' : negocio,
        'reporte': reporte,
        'fechaInicio' : fechaInicio,
        'fechaFin' : fechaFin
    }

    return render(request, 'negocio_resumen_ventas.html', context)
