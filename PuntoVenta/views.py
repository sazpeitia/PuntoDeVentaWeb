from django.shortcuts import render
from django.http import HttpResponse
from .models import PuntoventaCarrito, PuntoventaProducto, PuntoventaCategoria
from django.utils import timezone
import datetime
from django.db.models import F, FloatField, Sum
import views_reporteVentas, views_reporteGeneral
#from datetime import datetime, timedelta, time



# Create your views here.
def index(request):

    return decision(request, 'PAPELERIA', 'VENTAS_DIA')

def decision(request, negocio, reporte):

    negocio = negocio.replace("/", "")
    reporte = reporte.replace("/", "")


    print negocio, reporte

    if (reporte == 'VENTAS_DIA'):
        return views_reporteVentas.reporte_ventas_dia(request, negocio, reporte)

    if (reporte == 'REPORTE_VETNAS'):
        return views_reporteVentas.reporte_reporte_vetnas(request, negocio, reporte)

    if (reporte == 'REPORTE_COMPRAS'):
        return views_reporteVentas.reporte_reporte_compras(request, negocio, reporte)

    if (reporte == 'CATEGORIAS'):
        return views_reporteGeneral.reporte_general_porCategoria(request, negocio, reporte)
