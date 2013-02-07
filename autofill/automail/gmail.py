from automail.models import Order, Product, OrderItem,ErrorLog
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import imaplib
import email
import string
import re

class MailException(Exception):
    def __init__(self, desc):
        self.desc = desc
    def __unicode__(self):
        return self.desc

class GMailParser():
    def ConnectGMail(self):
        ''' Connect To Gmail use imap protocol'''
        self.box = imaplib.IMAP4_SSL('imap.gmail.com', '993')
        self.box.login('kittyzhangly@gmail.com', 'zhanglingyan18')
        
    def readMail(self):
        self.ConnectGMail()
        mailbox_name = 'DR shipment'
        # select mail box
        self.box.select(mailbox_name)

        try:
            self.numNewOrder = 0
            self.numUpdateOrder = 0
            self.numNewOrderItem = 0
            self.numDuplicateOrderItem = 0
            
            #get msg ids with criteria FROM + SUBJECT + UNSEEN
            result, msg_ids = self.box.search(None, '(FROM "drugstore.com <orders@drugstore.com>" SUBJECT "Shipment Confirmation" UNSEEN)')
            if result != 'OK':
                raise MailException("Unable to do the box search: " + orderID)
            if len(msg_ids[0]) == 0:
                print 'No message found'
                return
            for msg_id in msg_ids[0].split():
                print 'Processing Message:' + msg_id
                result, msg_data = self.box.fetch(msg_id, '(RFC822)')
                if result != 'OK':
                    raise MailException("Unable to do the box fetch: " + msg_id)
                self.parseEmail(msg_data)
        except MailException as e:
            log = ErrorLog(name = e.__unicode__())
            print log.name
            log.save()          
        finally: 
            self.box.close()        
                   
    def parseEmail(self,msg_data):
        for response_part in msg_data:
            if(isinstance(response_part, tuple)):
                msg = email.message_from_string(response_part[1])
                msgLines = string.split(msg.get_payload(),'\r\n')

                msgList = []
                for msgLine in msgLines:
                    msgList.append(msgLine.rstrip('\r\n').rstrip('='))
                message = ''.join(msgList)                     
                
                #get order ID
                oids = re.findall(r'(?<=EmailOrderNoInfo">).{14}', message)
                if len(oids) is not 1:
                    raise MailException('find multiple oids in the email: ' + string.join(oids))
                orderID = oids[0]

                order = Order()
                order.order_id = orderID
                
                #Shipping time
                time = re.findall(r'(?<=Delivery/Tracking:).{5,10}(?=-)',message)
                if time is None:
                    raise MailException("can not parse the shipping time for order:" + orderID)
                order.shipping_time = datetime.strptime(time[0].strip(), '%m/%d/%y')

                #shipping comanpy
                company = re.findall(r'Delivery/Tracking.*?<a ', message)
                company =company[0]
                if '- UPS -' in company:
                    order.shipping_company = u'UPS'
                elif '- US Mail -' in company:
                    order.shipping_company = u'USPS'
                elif '- On Trac -' in company:
                    order.shipping_company = u'On Trac'
                else:
                    order.shipping_company = u'other'

                #Track number
                trackNo = re.findall(r'(?<=>).{5,40}?(?=</a> \(Tracking information)', message)
                if len(trackNo) is not 1:
                    raise MailException("multiple track no found in order:" + orderID + string.join(trackNo))
                order.tracking_no = trackNo[0]

                #Carrier Name
                if '00698 Flushing' in message:
                    order.carrier_name = u'HMUS'
                elif '2820 119th St Flushing' in message:
                    order.carrier_name = u'HMUS'
                elif '156-07 45th ave' in message:
                    order.carrier_name = u'SOONDAA'
                elif '4 Lewis Cir' in message:
                    order.carrier_name = u'CULEXPRESS'

                order.order_status = u'vender_shipped'
                try:
                    oldOrder= Order.objects.get(order_id = order.order_id)
                    oldOrder.carrier_name = order.carrier_name
                    oldOrder.tracking_no = order.tracking_no
                    oldOrder.shipping_company = order.shipping_company
                    oldOrder.shipping_time = order.shipping_time
                    oldOrder.save()
                    order = oldOrder
                    self.numUpdateOrder += 1
                except ObjectDoesNotExist:
                    order.save()
                    self.numNewOrder += 1

                #pids & qtys
                pids = re.findall(r'(?<=pid=).{8}', message)                    
                qtys = re.findall(r'(?<=valign=3D"top">)\d{1,3}',message)
                if pids is None:
                    raise MailException("can not parse the pids for order:" + orderID)                        
                if qtys is None:
                    raise MailException("can not parse the qtys for order:" + orderID)
                if len(pids) != len(qtys):
                    raise MailException("pids do not match with qtys" + orderID)
                for item in range(len(pids)):
                    try:
                        product = Product.objects.get(dr_id = pids[item])
                        orderItem = OrderItem()
                        orderItem.product = product
                        orderItem.order = order
                        orderItem.num = qtys[item]
                        try:
                            OrderItem.objects.get(product = orderItem.product, order = orderItem.order, num = orderItem.num)
                            self.numDuplicateOrderItem += 1
                        except ObjectDoesNotExist:                                
                            orderItem.save()
                            self.numNewOrderItem += 1
                    except ObjectDoesNotExist:
                        raise MailException("Product is not find in database, order_ID:" + orderID + " product id:" + pids[item])    

