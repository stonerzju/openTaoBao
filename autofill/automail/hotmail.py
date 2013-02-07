from automail.models import Order
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

import poplib
import email
import string
import re

def parseMail(startnum, endnum, force):
    mailConnector = poplib.POP3_SSL('pop3.live.com', 995) #Connect to hotmail pop3 server
    try:
        mailConnector.user('kittyzhangly@msn.com')
        mailConnector.pass_('zhanglingyan18')
    except:
        print "username or password incorrect"
    else:
        print "Successful login"

    (numMsg, numSize) =  mailConnector.stat()
    print 'numMsg: ' + repr(numMsg) + '   numBoxSize: ' + repr(numSize)

    for msgID in range(numMsg-startnum, numMsg-endnum, -1):
        print 'Start process Msg ID'+repr(msgID)
        
        (respMsg, mailMsg, octet) = mailConnector.retr(msgID)
        mail = email.message_from_string(string.join(mailMsg, '\n'))

        subject = email.Header.decode_header(mail['subject'])[0][0]
        subcode =    email.Header.decode_header(mail['subject'])[0][1]
        if subcode == None:
            subject = subject
        else:
            subject = unicode(subject, subcode)

        sender = email.Header.decode_header(mail['From'])[0][0]
        subcode = email.Header.decode_header(mail['From'])[0][1]
        if subcode == None:
            sender = sender
        else:
            sender = unicode(sender, subcode)
        #print unicode(subject) == u'Shipment Confirmation'
        #print unicode(sender) == u'drugstore.com <orders@drugstore.com>'
        
        if unicode(subject) == u'Shipment Confirmation':
            order = Order()
            
            message = mail.get_payload()
            searchResult = re.search(r'EmailOrderNoInfo">\d{14}', message,re.DOTALL)
            orderID = re.search(r'\d{14}', searchResult.group(0), re.DOTALL)
            orderID = orderID.group(0)
            order.order_id = orderID
            try:
                Order.objects.get(order_id = orderID)   #if the order alredy exist, quit
                if force:
                    continue
                else:
                    break
            except ObjectDoesNotExist:
                searchResult = re.search(r'Delivery/Tracking.*information will be ', message, re.DOTALL)
                searchResult = searchResult.group(0)

                #get the shipping company
                comanpy = searchResult
                if '- UPS -' in comanpy:
                    order.shipping_company = u'UPS'
                elif '- US Mail -' in comanpy:
                    order.shipping_company = u'USPS'
                else:
                    order.shipping_company = u'other'

                #get shipping date time
                timeSearch = re.search(r'\d{1,2}/\d{1,2}/\d{2}', searchResult)
                timeString = timeSearch.group(0)
                order.shipping_time = datetime.strptime(timeString, '%m/%d/%y')
                
                searchResult = re.search(r'">.*</a>', searchResult, re.DOTALL)
                searchResult = searchResult.group(0)
                length = len(searchResult)
                trackingNo = searchResult[2:(length-4)]
                order.tracking_no = trackingNo
            
                order.save()
        else:
            continue
    mailConnector.quit()            #disconnect to the mail server
