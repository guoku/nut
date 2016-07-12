#encoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.order.manager import OrderManager

class CartItem(models.Model):
    user = models.ForeignKey('core.GKUser', related_name='cart_items',db_index=True)
    sku  = models.ForeignKey('core.SKU', db_index=True)
    volume = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=True,db_index=True)


    class Meta:
        ordering = ['-add_time']

    def generate_order_item(self, order):
        order_item, created = OrderItem.objects.get_or_create(order=order, sku=self.sku)
        if created:
            order_item.volume = self.volume


    @property
    def grand_price(self):
        return self.sku.origin_price * self.volume

    @property
    def discount_price(self):
        return self.sku.promo_price * self.volume

    @property
    def shipping_cost(self):
        raise NotImplemented()
        return 0



class ShippingAddress(models.Model):
    (normal, special) = range(1,3)
    SHIPPINGADDRESS_TYPE_CHOICE = (
        (normal,_('normal address')),
        (special,_('special address'))
    )
    user = models.ForeignKey('core.GKUser', related_name='shipping_addresses')
    country = models.CharField()
    province = models.CharField()
    city = models.CharField()
    street = models.CharField()
    detail = models.CharField()
    post_code = models.CharField()
    type = models.IntegerField(choices=SHIPPINGADDRESS_TYPE_CHOICE, default=normal)
    contact_phone = models.CharField()


    def _cal_shipping_fee(self):
        raise NotImplemented()

    @property
    def shipping_fee(self):
        if self.type == self.special:
            return 0
        else :
            return self._cal_shipping_fee()


class Order(models.Model):

    (   address_unbind, #
        waiting_for_payment,#未付款
            paid, #已经付款,出库中
            send, #货物在途,
            closed, #已经签收
            refund_submit, #收到退款申请
            refund_sku_got, #处理货品回收
            refund_done, #货款已经退回
            ) = range(1,9)

    ORDER_STATUS_CHOICE = [
        (address_unbind, _('address unbind')),
        (waiting_for_payment, _('waiting for payment')),
        (paid, _('order paid')),
        (send, _('order send')),
        (closed, _('order closed')),
        (refund_submit,_('refund processing')),
        (refund_sku_got,_('refund product recieved')),
        (refund_done,_('refund down')),
    ]

    buyer = models.ForeignKey('core.GKUser', related_name='orders')
    number = models.CharField(max_length=128, db_index=True, unique=True)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICE, default=address_unbind)
    shipping_to  = models.ForeignKey(ShippingAddress)
    object = OrderManager()


    @property
    def shipping_fee(self):
        '''
        calculate shipping fee for entire order for specific address(shipping_to)
        :return:
        '''
        # raise NotImplemented()
        return 0

    @property
    def promo_total_price(self):
        return reduce(lambda a,b : a + b,
                        [item.promo_total_price for item in self.items.all()])

    @property
    def grand_total_price(self):
        return reduce(lambda a,b : a+b ,
                        [item.grand_total_price for item in self.items.all()])

    @property
    def order_total_value(self):
        return self.promo_total_price + self.shipping_fee

class Payment(models.Model):
    '''
        user can use multiple method to pay
    '''
    (waiting_for_payment,
            paid, refund) = range(3)

    PAYMENT_STATUS_CHOICES = [
        (waiting_for_payment, _('waiting for payment')),
        (paid, _('paid')),
        (refund, _('refund')),
        ]
    #TODO(anchen) : one to one or many to one ?
    order = models.ForeignKey(Order, related_name='payments')
    payment_status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES)
    created_datetime =  models.DateTimeField(auto_now_add=True)
    updated_datetime =  models.DateTimeField(auto_now=True)


    @property
    def total_price(self):
        return self.order.order_total_value

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items')
    user = models.ForeignKey('core.GKUser', related_name='orders',db_index=True)
    sku  = models.ForeignKey('core.SKU', db_index=True)
    volume = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True, auto_now=True,db_index=True)
    grand_total_price = models.FloatField(null=False) # 当订单生成的时候计算
    promo_total_price = models.FloatField(null=False) # 当订单生成的时候计算

    def calculate_price(self):
        return self.sku.origin_price * self.volume

    def calculate_promo_price(self):
        return self.sku.promo_price * self.volume


class OrderMessage(models.Model):
    '''
        订单意见纪录,可以由用户填写,也可以由客服填写
    '''
    order = models.ForeignKey(Order)
    user = models.ForeignKey('core.GKUser')
    message = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)









