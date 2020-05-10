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

# from cartridge.shop.models import Product, ProductVariation, Order, OrderItem
from paypalrestsdk import Payment

from .hooks import paypal_api,pagseguro_api
from .payments import PagSeguro,PayPal,Baskets,Cartridge
from .models import Product, Basket, Order
from .store import Store, Cancel
from .mixins import HybridDetailView, HybridListView

class ProductsDetailView(HybridDetailView):

    model = Product

    def product_image(self, request):
        s = Store()
        if request.method == 'GET':
            return s.view_image(request)
        elif request.method == 'POST':
            return s.create_image(request)

class ProductsListView(HybridListView):

    model = Product

    def store_main(self, request):
        prod = Store()
        if request.method == 'GET':
            return prod.view_product(request)
        elif request.method == 'POST':
            return prod.create_product(request)

    def cancel(self, request):
        c = Cancel()
        if request.method == 'POST':
            return c.cancel(request)


class BasketsDetailView(HybridDetailView):

    model = Basket

    def pagsegurocart(self, request):
        p = PagSeguro()
        if request.method == 'GET':
            return p.process_cart(request)

    def paypalcart(self, request):
        p = PayPal()
        if request.method == 'GET':
            return p.process_cart(request)

class BasketsListView(HybridListView):

    model = Basket

    def basket(self, request):
        b = Baskets()
        if request.method == 'GET':
            return b.view_items(request)
        elif request.method == 'POST':
            return b.add_item(request)

    def basketclean(self, request):
        b = Baskets()
        if request.method == 'GET':
            return b.clean_basket(request)

    def spread_basket(self, request):
        b = Baskets(Product())
        if request.method == 'GET':
            return b.view_items(request)
        elif request.method == 'POST':
            return b.add_item(request)


class OrdersDetailView(HybridDetailView):

    model = Order

    def pagseguro(self, request):
        p = PagSeguro()
        if request.method == 'GET':
            return p.process(request)

    def paypal(self, request):
        p = PayPal()
        if request.method == 'GET':
            return p.process(request)

    def paypal_ipn(self, request):
        """Accepts or rejects a Paypal payment notification."""
        input = request.GET # remember to decode this! you could run into errors with charsets!
        if 'txn_id' in input and 'verified' in input['payer_status'][0]: pass
        else: raise Exception # Erro 402
    
    def paypal_redirect(self, request, order):
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
        return redirect(redirect_url)

class OrdersListView(HybridListView):

    model = Order

    def payment_redirect(self, request, order_id):
        lookup = {"id": order_id}
        if not request.user.is_authenticated(): lookup["key"] = request.session.session_key
        elif not request.user.is_staff: lookup["user_id"] = request.user.id
        order = get_object_or_404(Order, **lookup)
        is_pagseguro = order.pagseguro_redirect
        is_paypal = order.paypal_redirect_token
        if 'none' not in is_pagseguro: return redirect(str(is_pagseguro))
        elif 'none' not in is_paypal: return paypal_redirect(request,order)
        else: return redirect("/store/execute?orderid=%s" % lookup["id"])

    def payment_slip(self, request):
        orderid = request.GET['id']
        order = Order.objects.filter(id=orderid)[0]
        send_mail('Pedido de boleto', 'O pedido de boleto foi solicitado ao Efforia para o pedido %s. Em instantes voc� estar� recebendo pelo e-mail. Aguarde instru��es.' % order.id, 'oi@efforia.com.br',
        [order.billing_detail_email,'contato@efforia.com.br'], fail_silently=False)
        context = { "order": order }
        resp = render(request,"shop/slip_confirmation.html",context)
        return resp

    def payment_bank(self, request):
        orderid = request.GET['order_id']
        order = Order.objects.filter(id=orderid)[0]
        context = {
            "order": order,
            "agency": settings.BANK_AGENCY,
            "account": settings.BANK_ACCOUNT,
            "socname": settings.BANK_SOCIALNAME
        }
        resp = render(request,"shop/bank_confirmation.html",context)
        return resp

    def payment_execute(self, request, template="shop/payment_confirmation.html"):
        order = None
        lookup = {}
        if request.GET.has_key('token'):
            paypal_api()
            token = request.GET['token']
            payer_id = request.GET['PayerID']
            order = get_object_or_404(Order, paypal_redirect_token=token)
            payment = Payment.find(order.transaction_id)
            payment.execute({ "payer_id": payer_id })
        elif request.GET.has_key('transaction_id'):
            api = pagseguro_api()
            email = api.data['email']
            token = api.data['token']
            transaction = request.GET['transaction_id']
            url = api.config.TRANSACTION_URL % transaction
            resp = urlopen("%s?email=%s&token=%s" % (url,email,token)).read()
            lookup["id"] = ETree.fromstring(resp).findall("reference")[0].text
            print(ETree.fromstring(resp).findall("reference")[0].text)
            if not request.user.is_authenticated(): lookup["key"] = request.session.session_key
            if not request.user.is_staff: lookup["user_id"] = request.user.id
            order = get_object_or_404(Order, **lookup)
            order.transaction_id = transaction
        elif request.GET.has_key('orderid'):
            return redirect("/store/bank?order_id=%s" % request.GET['orderid'])
        order.status = 2
        order.save()
        context = { "order" : order }
        response = render(request, template, context)
        return response