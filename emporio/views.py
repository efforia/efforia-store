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
from django.shortcuts import get_object_or_404,redirect,render

from .models import Product, Basket, Order
from .services import *

class ProductsDetailView(DetailView):
    
    model = Product

    def get(self, request, *args, **kwargs):
        ''' Specific logic for GET on loading product own image '''
        store_manager = Store()
        image = store_manager.view_image(request)
        product = store_manager.view_product(request)
        return super(ProductsDetailView, self).get(request, *args, **kwargs)        

class ProductsListView(ListView):

    model = Product

    def post(self, request, *args, **kwargs):
        ''' Specific logic for POST on creating a product with its own image '''
        store_manager = Store()
        store_manager.create_image(request)
        store_manager.create_product(request)
        return super(ProductsListView, self).post(request, *args, **kwargs)


class BasketsDetailView(DetailView):

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

class BasketsListView(ListView):

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


class OrdersDetailView(DetailView):

    model = Order

class OrdersListView(ListView):

    model = Order

class PaymentsView(View):

    service = PaymentService()

    def get(self, request, *args, **kwargs):
        ''' Accepts or rejects a payment '''
        return self.service.redirect()

    def post(self, request, *args, **kwargs):
        ''' Order processing method '''
        return self.service.process()

    def delete(self, request, *args, **kwargs):
        ''' Order payment cancelling method '''
        return self.service.cancel()

class PaymentCancelView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        self.url = 'orders/%s/cancel/' % kwargs['pk'] 
        return super().get_redirect_url(*args, **kwargs)

class PaymentRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        self.url = 'orders/%s/redirect/' % kwargs['pk']
        return super().get_redirect_url(*args, **kwargs)
