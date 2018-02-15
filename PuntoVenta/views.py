from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import PuntoventaCarrito, PuntoventaProducto, PuntoventaCategoria
from django.utils import timezone
import datetime
from django.db.models import F, FloatField, Sum
import views_reportes_negocio_ventas, views_reportes_negocio_resumen, views_reportes_negocio_compras, views_reportes_general_grupos
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):

    return decision(request, 'PAPELERIA', 'VENTAS_DIA')

def azptec_login(request):

    try:

        if not request.user.is_authenticated:

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Redirect to a success page.
                login(request, user)
                return HttpResponseRedirect('/azptec/PuntoVenta/')

            else:
                # Return an 'invalid login' error message.
                return render(request, 'azptec_puntoventa_login_incorrecto.html')
        else:
            return HttpResponseRedirect('/azptec/PuntoVenta/')

    except KeyError:

        return render(request, 'azptec_puntoventa_login.html')

def azptec_logout(request):
    logout(request)
    return render(request, 'azptec_puntoventa_logout.html')


def decision(request, negocio, reporte):

    if request.user.is_authenticated:

        negocio = negocio.replace("/", "")
        reporte = reporte.replace("/", "")

        if (reporte == 'VENTAS_DIA'):
            return views_reportes_negocio_ventas.reportes_negocio_ventas(request, negocio, reporte)

        if (reporte == 'REPORTE_VETNAS'):
            return views_reportes_negocio_resumen.reportes_negocio_resumen(request, negocio, reporte)

        if (reporte == 'REPORTE_COMPRAS'):
            return views_reportes_negocio_compras.reportes_negocio_compras(request, negocio, reporte)

        if (reporte == 'CATEGORIAS'):
            return views_reportes_general_grupos.reportes_general_grupos(request, negocio, reporte)

    else:

        return HttpResponseRedirect('/azptec/PuntoVenta/login')
