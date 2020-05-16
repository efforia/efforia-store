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

from django.views.generic import View, ListView, DetailView, RedirectView
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.http import HttpResponse as response
from django.template import Context,Template
from django.shortcuts import get_object_or_404,redirect,render

from .models import Product, Basket, Order
from .services import *

class ProductsDetailView(DetailView):
    
    model = Product

    def get(self, request, *args, **kwargs):
        ''' Specific logic for GET on loading product own image '''
        store_manager = MarketplaceService()
        image = store_manager.view_image(request)
        product = store_manager.view_product(request)
        return super(ProductsDetailView, self).get(request, *args, **kwargs)        

class ProductsListView(ListView):

    model = Product

    def get(self, request, *args, **kwargs):
        source = """
            <div class="col-xs-12 col-sm-6 col-md-3 col-lg-2 brick">
                <a class="block sellable" href="#" style="display:block; background-color:white">
                <div class="box" style="background-color:#333">
                <div class="content">
                <h2 class="title" style="color:white">{{nametrim}}</h2>
                {% if paid %}
                    <h2 class="lightgreen"> Valor j&aacute; pago </h2>
                {% endif %}
                <h1 class="centered"><span class="label label-info big-label"> R$ {{value}}0 </span></h1>
                <h1 class="centered"><span class="glyphicon glyphicon-shopping-cart giant-glyphicon style="color:white; margin-bottom:10px"></span></h1>
                <div class="id hidden">{{id}}</div>
            </div></div></div></a></div>
        """
        return Template(source).render(Context({
            'nametrim':  object.name_trimmed,
            'paid':      object.paid,
            'id':        object.id,
            'value':     object.value,
            'bio':       object.bio,
            'day':       object.date.day,
            'month':     object.month
        }))

    def post(self, request, *args, **kwargs):
        ''' Specific logic for POST on creating a product with its own image '''
        store_manager = MarketplaceService()
        store_manager.create_image(request)
        store_manager.create_product(request)
        return super(ProductsListView, self).post(request, *args, **kwargs)


class BasketsDetailView(DetailView):

    model = Basket

    def post(self, request, *args, **kwargs):
        ''' Adds item to basket '''
        basket_manager = MarketplaceService(Product())
        basket_manager.add_item(request)
        return super(BasketsDetailView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        ''' Clear one specific basket from user / key '''
        basket_manager = MarketplaceService()
        basket_manager.clean_basket(request)
        return super(BasketsDetailView, self).delete(request, *args, **kwargs)

class BasketsListView(ListView):

    model = Basket

    def get(self, request, *args, **kwargs):
        ''' Specific logic for GET on retrieving items basket '''
        basket_manager = MarketplaceService()
        items = basket_manager.view_items(request)
        return super(BasketsListView, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        ''' Clears all baskets from specific user / key '''
        cancel_manager = MarketplaceService()
        cancel_manager.cancel(request)
        return super(BasketsListView, self).delete(request, *args, **kwargs)


class OrdersDetailView(DetailView):

    model = Order

class OrdersListView(ListView):

    model = Order

class PaymentsView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'payments': 'success'})

class PaymentProcessView(View):

    service = PaymentService()

    def get(self, request, *args, **kwargs):
        ''' Accepts or rejects a payment '''
        return self.service.redirect()

class PaymentCancelView(View):

    service = PaymentService()

    def get(self, request, *args, **kwargs):
        ''' Order processing method '''
        return self.service.process()

class PaymentRedirectView(View):

    service = PaymentService()

    def get(self, request, *args, **kwargs):
        ''' Order payment cancelling method '''
        return self.service.cancel()
