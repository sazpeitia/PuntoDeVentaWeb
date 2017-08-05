from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$',views.index, name='index'),
    url(r'^negocios/(?P<negocio>\w{0,50}/$)',views.negocio_ventas)
]
