#!/usr/bin/python
#
# This file is part of django-emporio project.
#
# Copyright (C) 2011-2020 William Oliveira de Lagos <william.lagos@icloud.com>
#
# Emporio is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Emporio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Emporio. If not, see <http://www.gnu.org/licenses/>.
#

from urllib.request import urlopen
from urllib.parse import urlparse,parse_qs
from xml.etree import ElementTree as ETree

from django.views.generic import View, ListView, DetailView
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.http import HttpResponse as response
from django.shortcuts import get_object_or_404,redirect,render

from .models import Product, Basket, Order
from .mixins import HybridDetailView, HybridListView
from .services import *

class ProductsDetailView(HybridDetailView):
    
    model = Product

    def get(self, request, *args, **kwargs):
        ''' Specific logic for GET on loading product own image '''
        store_manager = Store()
        image = store_manager.view_image(request)
        product = store_manager.view_product(request)
        return super(ProductsDetailView, self).get(request, *args, **kwargs)        

class ProductsListView(HybridListView):

    model = Product

    def post(self, request, *args, **kwargs):
        ''' Specific logic for POST on creating a product with its own image '''
        store_manager = Store()
        store_manager.create_image(request)
        store_manager.create_product(request)
        return super(ProductsListView, self).post(request, *args, **kwargs)


class BasketsDetailView(HybridDetailView):

    model = Basket

    def post(self, request, *args, **kwargs):
        ''' Adds item to basket '''
        basket_manager = Baskets(Product())
        basket_manager.add_item(request)
        return super(BasketsDetailView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        ''' Clear one specific basket from user / key '''
        basket_manager = Baskets()
        basket_manager.clean_basket(request)
        return super(BasketsDetailView, self).delete(request, *args, **kwargs)

class BasketsListView(HybridListView):

    model = Basket

    def get(self, request, *args, **kwargs):
        ''' Specific logic for GET on retrieving items basket '''
        basket_manager = Baskets()
        items = basket_manager.view_items(request)
        return super(BasketsListView, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        ''' Clears all baskets from specific user / key '''
        cancel_manager = Cancel()
        cancel_manager.cancel(request)
        return super(BasketsListView, self).delete(request, *args, **kwargs)


class OrdersDetailView(HybridDetailView):

    model = Order

class OrdersListView(HybridListView):

    model = Order

class PaymentsView(View):

    def get(self, request, order, *args, **kwargs):
        ''' Accepts or rejects a payment '''
        # template="shop/payment_confirmation.html"
        order = None
        lookup = {}
        # PayPal IPN code
        # input = request.GET # remember to decode this! you could run into errors with charsets!
        # if 'txn_id' in input and 'verified' in input['payer_status'][0]: pass
        # else: raise Exception # Erro 402
        # 
        # PayPal redirect code
        paypal_api()
        payment = Payment.find(order.transaction_id)
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
                url = urlparse(link.href)
                params = parse_qs(url.query)
                redirect_token = params['token'][0]
                order.paypal_redirect_token = redirect_token
                order.save()
        if request.GET.has_key('token'):
            paypal_api()
            token = request.GET['token']
            payer_id = request.GET['PayerID']
            order = get_object_or_404(Order, paypal_redirect_token=token)
            payment = Payment.find(order.transaction_id)
            payment.execute({ "payer_id": payer_id })
        #
        # PagSeguro redirect code
        # if request.GET.has_key('transaction_id'):
        #     api = pagseguro_api()
        #     email = api.data['email']
        #     token = api.data['token']
        #     transaction = request.GET['transaction_id']
        #     url = api.config.TRANSACTION_URL % transaction
        #     resp = urlopen("%s?email=%s&token=%s" % (url,email,token)).read()
        #     lookup["id"] = ETree.fromstring(resp).findall("reference")[0].text
        #     print(ETree.fromstring(resp).findall("reference")[0].text)
        #     if not request.user.is_authenticated(): lookup["key"] = request.session.session_key
        #     if not request.user.is_staff: lookup["user_id"] = request.user.id
        #     order = get_object_or_404(Order, **lookup)
        #     order.transaction_id = transaction
        #
        # Cartridge specific code
        # lookup = {"id": order_id}
        # if not request.user.is_authenticated(): lookup["key"] = request.session.session_key
        # elif not request.user.is_staff: lookup["user_id"] = request.user.id
        # order = get_object_or_404(Order, **lookup)
        # order.status = 2
        # order.save()
        # context = { "order" : order }
        # response = render(request, template, context)
        # return response
        return JsonResponse({'payment_finish': 'success'})

    def post(self, request, *args, **kwargs):
        ''' Order processing method '''
        paypal = PayPal()
        paypal.process(request)
        paypal.process_cart(request)
        # PagSeguro Option
        # pagseguro = PagSeguro()
        # pagseguro.process(request)
        # pagseguro.process_cart(request)
        #
        # Bank Slip Option
        # orderid = request.GET['id']
        # order = Order.objects.filter(id=orderid)[0]
        # send_mail('Pedido de boleto', 'O pedido de boleto foi solicitado ao Efforia para o pedido %s. Em instantes voc� estar� recebendo pelo e-mail. Aguarde instru��es.' % order.id, 'oi@efforia.com.br',
        # [order.billing_detail_email,'contato@efforia.com.br'], fail_silently=False)
        # context = { "order": order }
        # resp = render(request,"shop/slip_confirmation.html",context)
        # return resp
        #
        # Bank Transfer Option
        # orderid = request.GET['order_id']
        # order = Order.objects.filter(id=orderid)[0]
        # context = {
        #     "order": order,
        #     "agency": settings.BANK_AGENCY,
        #     "account": settings.BANK_ACCOUNT,
        #     "socname": settings.BANK_SOCIALNAME
        # }
        # resp = render(request,"shop/bank_confirmation.html",context)
        # return resp
        return JsonResponse({'payment_process': 'success'})

class CancelView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'payment_cancel': 'success'})