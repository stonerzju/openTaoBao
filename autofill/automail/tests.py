"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from automail.models import Order, Product
from django.core.exceptions import ObjectDoesNotExist
from automail.gmail import GMailParser
from datetime import datetime

class AutoMailTest(TestCase):
    def setUp(self):
        Product.objects.create(name = 'Culturelle Probiotic Digestive Health with Dairy Free Lactobacillus GG - 30 capsules', dr_id = '3D215150')
        Product.objects.create(name = 'Culturelle Kids! Chewables Probiotic, For Kids 50-100lbs, Tablets', dr_id = '3D394891')
        Product.objects.create(name = 'Culturelle Probiotic All Natural Dairy & Gluten Free Vegetable Capsules Lactobacillus GG - 30 ea', dr_id = '3D221973')
        Product.objects.create(name = 'Culturelle Probiotics for Kids!, Probiotic Packets - 30 ea', dr_id = '3D215151')
        Order.objects.create(order_id = '03300303326100',
                             tracking_no = '9102901061434002965479',
                             shipping_company = 'USPS',
                             carrier_name = 'HMUS',
                             shipping_time = datetime.now()
                             )
                             
    def test_get_gmail(self):
        parser = GMailParser()
        parser.readMail()
        print parser.numNewOrder
        print parser.numUpdateOrder
        print parser.numNewOrderItem
        print parser.numDuplicateOrderItem
'''
        try:
            order1 = Order.objects.get(order_id = u'03284392992100')
            self.assertEqual(order1.tracking_no, u'C11217613002819')
            self.assertEqual(order1.shipping_company, u'On Trac')

            order1 = Order.objects.get(order_id = u'03278286077100')
            self.assertEqual(order1.tracking_no, u'C11217611555282')
            self.assertEqual(order1.shipping_company, u'On Trac')

            order1 = Order.objects.get(order_id = u'03275818316100')
            self.assertEqual(order1.tracking_no, u'1Z4A662R0317677551')
            self.assertEqual(order1.shipping_company, u'UPS')
        except ObjectDoesNotExist:
            self.assertEqual(True, False)        

    def test_get_mail(self):
        parseMail(0,50,True)
        try:
            order1 = Order.objects.get(order_id = u'03303845583100')
            self.assertEqual(order1.tracking_no, u'1Z4A662R0342493765')
            self.assertEqual(order1.shipping_company, u'UPS')
            
            order2 = Order.objects.get(order_id = u'03303844733100')
            self.assertEqual(order2.tracking_no, u'1Z4A662R0342493694')
            self.assertEqual(order2.shipping_company, u'UPS')
            
            order3 = Order.objects.get(order_id = u'03303844961100')
            self.assertEqual(order3.tracking_no, u'1Z4A662R0342493676')
            self.assertEqual(order3.shipping_company, u'UPS')
            
            order4 = Order.objects.get(order_id = u'03303845659100')
            self.assertEqual(order4.tracking_no, u'1Z4A662R0342489878')
            self.assertEqual(order4.shipping_company, u'UPS')
            
            order5 = Order.objects.get(order_id = u'03303844857100')
            self.assertEqual(order5.tracking_no, u'1Z4A662R0342489850')
            self.assertEqual(order5.shipping_company, u'UPS')            
        except ObjectDoesNotExist:
            self.assertEqual(True, False)            
'''
