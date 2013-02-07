from automail.models import Order,Product,OrderItem,ErrorLog
from django.contrib import admin


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
   
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'tracking_no', 'shipping_time','order_status','carrier_name','carrier_track_no','int_track_no','domestic_track_no', 'notes')
    search_fields = ['order_id', 'tracking_no','order_status','int_track_no','carrier_track_no','domestic_track_no', 'carrier_name']
    date_hierarchy = 'shipping_time'
    list_filter = ['shipping_time','order_status', 'carrier_name']
    inlines = [OrderItemInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'dr_id')
    search_fields = ['name', 'dr_id']
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'num','product')
    search_fields = ['order__order_id', 'product__name', 'order__tracking_no']

class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time')
    
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ErrorLog, ErrorLogAdmin)

