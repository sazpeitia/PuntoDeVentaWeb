# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class PuntoventaCarrito(models.Model):
    id_carrito = models.AutoField(db_column='ID_CARRITO', primary_key=True)  # Field name made lowercase.
    id_venta = models.ForeignKey('PuntoventaVenta', models.DO_NOTHING, db_column='ID_VENTA')  # Field name made lowercase.
    cantidad_producto = models.IntegerField(db_column='CANTIDAD_PRODUCTO')  # Field name made lowercase.
    total = models.FloatField(db_column='TOTAL')  # Field name made lowercase.
    id_producto = models.ForeignKey('PuntoventaProducto', models.DO_NOTHING, db_column='ID_PRODUCTO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUNTOVENTA_CARRITO'


class PuntoventaCategoria(models.Model):
    id_categoria = models.AutoField(db_column='ID_CATEGORIA', primary_key=True)  # Field name made lowercase.
    nombre_categoria = models.CharField(db_column='NOMBRE_CATEGORIA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    id_categoria_padre = models.ForeignKey('self', models.DO_NOTHING, db_column='ID_CATEGORIA_PADRE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUNTOVENTA_CATEGORIA'


class PuntoventaCorteCaja(models.Model):
    id_corte_caja = models.AutoField(db_column='ID_CORTE_CAJA', primary_key=True)  # Field name made lowercase.
    total_recaudado = models.FloatField(db_column='TOTAL_RECAUDADO')  # Field name made lowercase.
    fecha_corte = models.DateField(db_column='FECHA_CORTE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUNTOVENTA_CORTE_CAJA'


class PuntoventaHistoriaInventario(models.Model):
    id_historia_inventario = models.AutoField(db_column='ID_HISTORIA_INVENTARIO', primary_key=True)  # Field name made lowercase.
    fecha_registro = models.DateField(db_column='FECHA_REGISTRO')  # Field name made lowercase.
    id_producto = models.ForeignKey('PuntoventaProducto', models.DO_NOTHING, db_column='ID_PRODUCTO')  # Field name made lowercase.
    cantidad_anterior = models.IntegerField(db_column='CANTIDAD_ANTERIOR')  # Field name made lowercase.
    cantidad_adicionada = models.IntegerField(db_column='CANTIDAD_ADICIONADA')  # Field name made lowercase.
    cantidad_nueva = models.IntegerField(db_column='CANTIDAD_NUEVA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUNTOVENTA_HISTORIA_INVENTARIO'


class PuntoventaProducto(models.Model):
    id_producto = models.AutoField(db_column='ID_PRODUCTO', primary_key=True)  # Field name made lowercase.
    id_codigo_barra = models.CharField(db_column='ID_CODIGO_BARRA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nombre_producto = models.CharField(db_column='NOMBRE_PRODUCTO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id_categoria = models.ForeignKey(PuntoventaCategoria, models.DO_NOTHING, db_column='ID_CATEGORIA', blank=True, null=True)  # Field name made lowercase.
    precio_venta = models.FloatField(db_column='PRECIO_VENTA', blank=True, null=True)  # Field name made lowercase.
    precio_compra = models.FloatField(db_column='PRECIO_COMPRA', blank=True, null=True)  # Field name made lowercase.
    cantidad_disponible = models.IntegerField(db_column='CANTIDAD_DISPONIBLE', blank=True, null=True)  # Field name made lowercase.
    codigo_producto = models.CharField(db_column='CODIGO_PRODUCTO', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUNTOVENTA_PRODUCTO'


class PuntoventaVenta(models.Model):
    id_venta = models.AutoField(db_column='ID_VENTA', primary_key=True)  # Field name made lowercase.
    fecha_venta = models.DateField(db_column='FECHA_VENTA', blank=True, null=True)  # Field name made lowercase.
    total_venta = models.FloatField(db_column='TOTAL_VENTA', blank=True, null=True)  # Field name made lowercase.
    pago_venta = models.FloatField(db_column='PAGO_VENTA', blank=True, null=True)  # Field name made lowercase.
    cambio_venta = models.FloatField(db_column='CAMBIO_VENTA', blank=True, null=True)  # Field name made lowercase.
    id_corte_caja = models.ForeignKey(PuntoventaCorteCaja, models.DO_NOTHING, db_column='ID_CORTE_CAJA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUNTOVENTA_VENTA'
