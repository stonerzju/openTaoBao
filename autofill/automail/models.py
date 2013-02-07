# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Order(models.Model):
    ShippingCompanys = (
        (u'UPS', u'UPS'),
        (u'USPS', u'USPS'),
        (u'Fedex', u'Fedex'),
        (u'On Trac', u'On Trac'),
        (u'other', u'other'),
        )
    CarrierNames = (
        (u'HMUS', u'华美'),
        (u'SOONDAA', u'Soondaa'),
        (u'CULEXPRESS', u'中美'),
        )
    OrderStatus = (
        (u'vender_shipped', u'网站发货'),
        (u'broken', u'破损'),
        (u'lost', u'丢失'),
        (u'received', u'收到'),
        (u'canceled', u'取消'),
        )
    order_id = models.CharField(max_length = 20, unique = True)
    tracking_no = models.CharField(max_length = 50)
    shipping_company = models.CharField(max_length = 50, choices = ShippingCompanys)
    shipping_time = models.DateTimeField()
    filled_time = models.DateTimeField(blank = True, null=True)

    carrier_track_no = models.CharField(max_length = 100, blank = True)
    carrier_name = models.CharField(max_length = 20, blank = True, choices = CarrierNames)

    int_track_no = models.CharField(max_length = 100, blank = True)

    domestic_track_no = models.CharField(max_length = 20, blank = True)

    order_status = models.CharField(max_length = 20, blank = True, choices = OrderStatus)

    notes = models.CharField(max_length = 100, blank = True)

    isMultishipment = models.BooleanField(default = False)
    def __unicode__(self):
        return self.order_id
    

    
class Product(models.Model):
    name = models.CharField(max_length = 100)
    dr_id = models.CharField(max_length = 100, blank = True)
    vitacost_id = models.CharField(max_length = 100, blank = True)
    def __unicode__(self):
        return self.name

class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    num = models.IntegerField()
    def __unicode__(self):
        return repr(self.num)    
class ErrorLog(models.Model):
    name = models.CharField(max_length = 255)
    time = models.DateTimeField(auto_now = True)
