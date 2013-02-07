from automail.models import Order, OrderItem, Product
def checkOrderItemDuplicate():
    orderItems = OrderItem.objects.all()
    for item in orderItems:
        num = len(OrderItem.objects.filter(order = item.order, product = item.product, num = item.num))
        if num > 1:
            item.delete()            
                
            
                
