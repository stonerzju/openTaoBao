# Create your views here.
from automail.hotmail import parseMail
from automail.models import Order, OrderItem
from django.http import HttpResponse
from automail.gmail import GMailParser
from django.shortcuts import render_to_response
from automail.util import checkOrderItemDuplicate
from django.http import HttpResponseRedirect
import urllib2;
import urllib;
def GetMail(request):
    parser = GMailParser()
    parser.readMail()
    html = "<html><body>" + repr(parser.numNewOrder) + '  orders added,    '
    html = html + repr(parser.numUpdateOrder) + '  orders updated,    '
    html = html + repr(parser.numNewOrderItem) + ' orderItem added,    '
    html = html + repr(parser.numDuplicateOrderItem) + '  orderItemDuplicated</body></html>'
    return HttpResponse(html)


def deleteDuplicate(request):
    orign = len(OrderItem.objects.all())
    checkOrderItemDuplicate()
    new = len(OrderItem.objects.all())
    html = "<html><body>Totally %d Order is saved in database.</body></html>" % (new-orign)
    return HttpResponse(html)

def main(request):
    return render_to_response('base.html', None)

def authResult(request):    
    if request.method == "GET":
        code = request.GET['code']        
        post_data = [('client_id','21379702'),('client_secret','0cac40fa9899dfd09e8320427f748df4'), ('grant_type', 'authorization_code'),('code', code),('redirect_uri', 'http://127.0.0.1:8000/tokenResult/')]
        result = urllib2.urlopen('https://oauth.taobao.com/token', urllib.urlencode(post_data))
        content = result.read()
        print content
    return render_to_response('base.html', None)

def auth(request):
    auth_url = 'https://oauth.taobao.com/authorize?response_type=code&client_id=21379702&redirect_uri=http://127.0.0.1:8000/authResult/&state=1212&scope=item&view=web'
    return HttpResponseRedirect(auth_url);
