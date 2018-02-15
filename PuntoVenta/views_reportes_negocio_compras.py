from django.shortcuts import render
from django.http import HttpResponse
from .models import PuntoventaCarrito, PuntoventaProducto, PuntoventaCategoria, PuntoventaHistoriaInventario
from django.utils import timezone
import datetime
from django.db.models import F, Q, FloatField, Sum
from django.db.models.functions import (
    TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth, TruncYear
    )


def reportes_negocio_compras(request, negocio, reporte):

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

    return render(request, 'reportes_negocio_compras.html', context)
