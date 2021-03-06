# encoding: utf-8
from urllib import urlencode
from urlparse import urlparse, urlunparse, parse_qsl

import unicodecsv as csv
from braces.views import AjaxResponseMixin, UserPassesTestMixin, JSONResponseMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_text
from django.views.generic import ListView, View

from apps.core.extend.paginator import ExtentPaginator
from apps.core.mixins.views import FilterMixin, SortMixin
from apps.order.models import Order, OrderItem
from apps.payment.models import PaymentLog
from apps.web.forms.checkout import CheckDeskOrderPayForm, CheckDeskOrderExpireForm
from apps.web.views.seller_management import OrderDetailView


def sum_price(price, next_log):
    return price + next_log.order.order_total_value


class CheckDeskUserTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        return getattr(user, 'is_admin', None) or user.email == 'guokumk@guoku.com'

    def no_permissions_fail(self, request=None):
        raise Http404


class CheckDeskAllOrderListView(CheckDeskUserTestMixin, FilterMixin, SortMixin, ListView):
    default_sort_params = ('created_datetime', 'desc')
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/allorder.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        number = self.request.GET.get('filtervalue', '')
        self.status = self.request.GET.get('status')
        if number:
            if self.status:
                return HttpResponseRedirect(
                    reverse('checkout_order_list') + '?number=' + str(number) + '&status=' + self.status)
            else:
                return HttpResponseRedirect(reverse('checkout_order_list') + '?number=' + str(number))
        else:
            context = self.get_context_data()
            return self.render_to_response(context)

    def get_queryset(self):
        qs = Order.objects.all()
        self.status = self.request.GET.get('status')
        if self.status == 'waiting_for_payment':
            qs = qs.filter(status__in=[1, 2]).filter(status__gt=0)
        elif self.status == 'paid':
            qs = qs.filter(status__in=[3, 4, 5, 6, 7, 8]).filter(status__gt=0)
        elif self.status == 'expired':
            qs = qs.filter(status=0)
        else:
            qs = qs.filter(status__gt=0)

        return self.sort_queryset(qs, *self.get_sort_params())

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'created_datetime':
            qs = qs.order_by('status', '-created_datetime')
            return qs

    def get_context_data(self, **kwargs):
        context = super(CheckDeskAllOrderListView, self).get_context_data(**kwargs)
        context['status'] = self.status
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]
        return context


class CheckoutOrderListView(CheckDeskUserTestMixin, FilterMixin, SortMixin, ListView):
    default_sort_params = ('created_datetime', 'desc')
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/allorder.html'

    def get_queryset(self):
        qs = Order.objects.all()
        self.status = self.request.GET.get('status')
        if self.status == 'waiting_for_payment':
            qs = qs.filter(status__in=[1, 2]).filter(status__gt=0)
        elif self.status == 'paid':
            qs = qs.filter(status__in=[3, 4, 5, 6, 7, 8]).filter(status__gt=0)
        return self.sort_queryset(self.filter_queryset(qs, self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        order_number = self.request.GET.get('number')
        filter_field, filter_value = filter_param
        if filter_value and filter_value != 'all':
            qs = qs.filter(number__icontains=filter_value.strip())
        elif order_number:
            qs = qs.filter(number__icontains=order_number.strip())
        return qs

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'created_datetime':
            qs = qs.order_by('status', '-created_datetime')
        return qs

    def get_context_data(self, **kwargs):
        context = super(CheckoutOrderListView, self).get_context_data(**kwargs)
        context['input_value'] = self.request.GET.get('number')
        context['filter_input_value'] = self.request.GET.get('filtervalue', '')
        context['status'] = self.status
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]
        return context


class SetOrderExpireView(AjaxResponseMixin, JSONResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        _form = CheckDeskOrderExpireForm(request.POST, request=request)
        if _form.is_valid():
            _form.save()
            return self.render_json_response({
                'result': 1
            }, status=200)
        else:
            return self.render_json_resposne({
                'result': 0
            }, status=404)


class CheckDeskPayView(CheckDeskUserTestMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def get_order(self):
        order_id = int(self.request.POST.get('order_id', None))
        return get_object_or_404(Order, pk=order_id)

    def post_ajax(self, request, *args, **kwargs):
        _form = CheckDeskOrderPayForm(request.POST, request=request)
        if _form.is_valid():
            _form.save()
            return self.render_json_response(
                {
                    'result': 1,
                },
                status=200
            )
        else:
            return self.render_json_response(
                {
                    'result': 0,
                    'message': _form.errors.as_text()
                },
                status=400
            )


class CheckDeskOrderStatisticView(CheckDeskUserTestMixin, FilterMixin, SortMixin, ListView):
    default_sort_params = ('dnumber', 'desc')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/checkout/order_statistic.html'
    wait_pay_status = [Order.address_unbind, Order.waiting_for_payment]
    paid_status = [Order.paid, Order.send, Order.closed]
    expired_status = [Order.expired]

    def __init__(self, *args, **kwargs):
        self.extra_query_dic = {}
        super(CheckDeskOrderStatisticView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('csv') == 'orders':
            return self.get_orders_csv()
        elif self.request.GET.get('csv') == 'order_items':
            return self.get_orderitems_csv()
        else:
            return super(CheckDeskOrderStatisticView, self).get(request, *args, **kwargs)

    def get_orders_csv(self):
        order_header_list = ('订单号', '下单时间', '付款时间', '终端账号',
                             '实收款', '果库佣金',
                             '付款路径', '备注')
        orders = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(order_header_list)
        for order in orders:
            data = map(smart_text, [order.number, order.created_datetime, order.updated_datetime,
                                    order.customer.nick, order.order_total_value, order.total_margin_value,
                                    order.payment_source, order.payment_note
                                    ])
            writer.writerow(data)
        return response

    def get_orderitems_csv(self):
        orders = self.get_queryset()
        orderitem_header_list = ('订单号', '下单时间', '付款时间',
                                 '终端账号', '商品名称', '品牌', '商品链接',
                                 'SKU属性', '原价',
                                 '促销价', '佣金比率',
                                 '数量', '实收款', '果库佣金',
                                 '结账路径', '备注')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="order_items.csv"'
        writer = csv.writer(response)
        writer.writerow(orderitem_header_list)

        for order in orders:
            for item in order.items.all():
                data = [order.number, order.created_datetime, order.updated_datetime,
                        order.customer.nick, item.item_title, item.sku.entity.brand,
                        'http://wwwguoku.com' + item.entity_link,
                        item.attrs_display, item.sku.origin_price,
                        item.unit_price, item.margin,
                        item.volume, item.promo_total_price, item.margin_value,
                        order.payment_source, order.payment_note
                        ]
                writer.writerow(data)
        return response

    def get_queryset(self):
        order_ids = list(OrderItem.objects.values_list('order', flat=True))
        qs = Order.objects.filter(id__in=order_ids)
        self.status = self.request.GET.get('status')

        if self.status == 'waiting_for_payment':
            qs = qs.filter(status__in=self.wait_pay_status)
        else:
            qs = qs.filter(status__in=self.paid_status)

        qs = self.apply_date_filter(qs)
        return self.sort_queryset(self.filter_queryset(qs, self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'number':
            qs = qs.filter(number__icontains=filter_value.strip())
        else:
            pass
        return qs

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'dprice':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=True)
        elif sort_by == 'uprice':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=False)
        elif sort_by == 'dnumber':
            qs = qs.order_by('-number')
        elif sort_by == 'unumber':
            qs = qs.order_by('number')
        elif sort_by == 'status':
            qs = qs.order_by('-status')
        else:
            pass
        return qs

    def get_sum_payment(self, order_list):
        sum = 0
        for order in order_list:
            if order.is_paid:
                sum += order.order_total_value
        return sum

    def get_sum_payment_for_payment_source(self, order_list, payment_souce):
        order_ids = list(order_list.values_list('id', flat=True))
        logs = PaymentLog.objects.filter(payment_source=payment_souce, order_id__in=order_ids)
        return reduce(sum_price, list(logs), 0)

    def get_extra_query(self):
        qs = ''
        for key, value in self.extra_query_dic.iteritems():
            qs = qs + key + '=' + value + '&'
        return qs

    def get_context_data(self, **kwargs):
        context = super(CheckDeskOrderStatisticView, self).get_context_data(**kwargs)
        context['status'] = self.status
        context['extra_query'] = self.get_extra_query()

        paged_order_list = context['object_list']

        for order in paged_order_list:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]

        order_list = self.get_queryset()
        context['sum_payment_all'] = self.get_sum_payment(order_list)
        context['sum_payment_wx'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.weixin_pay)
        context['sum_payment_ali'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.ali_pay)
        context['sum_payment_cash'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.cash)
        context['sum_payment_credit_card'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.credit_card)
        context['sum_payment_other'] = self.get_sum_payment_for_payment_source(order_list, PaymentLog.other)
        context['sum_margin_value'] = self.get_sum_margin(order_list)
        context['order_csv_link'] = self.get_order_csv_link()
        context['orderitems_csv_link'] = self.get_orderitems_csv_link()
        return context

    def add_param_to_url(self, param_dic):
        parsed_url_object = list(urlparse(self.request.build_absolute_uri()))
        query = dict(parse_qsl(parsed_url_object[4]))
        query.update(param_dic)
        parsed_url_object[4] = urlencode(query)
        return urlunparse(parsed_url_object)

    def get_order_csv_link(self):
        return self.add_param_to_url({'csv': 'orders'})

    def get_orderitems_csv_link(self):
        return self.add_param_to_url({'csv': 'order_items'})

    def get_sum_margin(self, order_list):
        return reduce(lambda total_margin_value, order: total_margin_value + order.total_margin_value,
                      order_list, 0)

    def apply_date_filter(self, order_list):
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        if start_date:
            order_list = order_list.filter(created_datetime__gte=start_date)
            self.extra_query_dic['start_date'] = start_date
        if end_date:
            order_list = order_list.filter(created_datetime__lte=end_date)
            self.extra_query_dic['end_date'] = end_date

        return order_list


class CheckoutOrderDetailView(OrderDetailView):
    template_name = 'web/checkout/checkout_order_detail.html'

    def test_func(self, user):
        self.order_number = self.kwargs.get('order_number')
        if user.is_admin or user.email == 'fugu@guoku.com':
            return True
        else:
            return False

    def no_permissions_fail(self, request=None):
        raise Http404
