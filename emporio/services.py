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

import json,time

from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect
from django.http import JsonResponse
from django.shortcuts import render

from .models import Basket, Product
# from .providers import *

class Baskets():#(Mosaic):
    def view_items(self,request):
        u = self.current_user(request); products = []
        basket = list(Basket.objects.filter(user=u))
        for b in basket: products.extend(Sellable.objects.filter(sellid=b.product))
        return self.view_mosaic(request,products)
    def add_item(self,request):
        u = self.current_user(request)
        prodid = int(request.REQUEST['id'])
        if 'value' in request.REQUEST:
            value = request.REQUEST['value']
            token = request.REQUEST['token']
            visual = request.REQUEST['visual']
            s = Sellable(user=u,name=token,value=value,sellid=prodid,visual=visual); s.save()
            if 'qty' in request.REQUEST:
                for i in range(int(request.REQUEST['qty'])-1):
                    s = Sellable(user=u,name=token,value=value,sellid=prodid,visual=visual); s.save()
        exists = Basket.objects.all().filter(user=u,product=prodid)
        if not len(exists):
            basket = Basket(user=u,product=prodid)
            basket.save()
        return self.view_items(request)
    def process_cart(self,request):
        u = self.current_user(request); cart = []
        basket = list(Basket.objects.filter(user=u))
        for b in basket:
            sellables = Sellable.objects.filter(sellid=b.product)
            for s in sellables:
                prod = {}
                prod['value'] = s.value
                prod['product'] = s.name
                prod['qty'] = '1'
                cart.append(prod)
        return self.process(request,cart)
    def clean_basket(self,request):
        u = self.current_user(request); cart = []
        basket = list(Basket.objects.filter(user=u))
        for b in basket:
            Sellable.objects.filter(sellid=b.product).delete()
            b.delete()
        return response("Basket cleaned successfully")
    def process(self,request,cart=None):
        pass

class Cancel():#(Plethora):
    def __init__(self): pass
    def cancel(self,request):
        u = self.current_user(request)
        Cart.objects.all().filter(user=u).delete()
        self.redirect('/')
        #value = int(self.request.arguments['credit'])
        #self.current_user().profile.credit -= value
        #self.current_user().profile.save()

class PaymentService():

    def __init__(self): 
        pass

    def process(self):
        ''' Order processing handler '''
        return JsonResponse({'payment_process': 'success'})

    def redirect(self):
        ''' Accepts or rejects a payment '''
        return JsonResponse({'payment_finish': 'success'})

    def cancel(self):
        return JsonResponse({'payment_cancel': 'success'})

    def view_recharge(self,request):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "1.19",
            "item_name": "Créditos do Plethora",
            "invoice": "unique-invoice-id",
            "notify_url": "http://www.efforia.com.br/paypal",
            "return_url": "http://www.efforia.com.br/",
            "cancel_return": "http://www.efforia.com.br/cancel",
            'currency_code': 'BRL',
            'quantity': '1'
        }
        payments = PayPalPaymentsForm(initial=paypal_dict)
        form = CreditForm()
        return render(request,"recharge.pug",{'form':payments,'credit':form},content_type='text/html')

    def update_credit(self,request):
        value = int(request.POST['credit'][0])
        current_profile = Profile.objects.all().filter(user=self.current_user(request))[0]
        if value > current_profile.credit: return self.view_recharge(request)
        else:
            current_profile.credit -= value
            current_profile.save()
            if 'other' in request.POST:
                iden = int(request.POST['other'][0])
                u = User.objects.all().filter(id=iden)[0]
                p = Profile.objects.all().filter(user=u)[0]
                p.credit += value
                p.save()
            self.accumulate_points(1,request)
            return response('')

class SpreadBasket(Basket):
    def product(self,prodid):
	# for p in basket:
        # quantity += p.quantity
        # value += p.product.credit*p.quantity
        pass

class Store(): #(Plethora):
    def __init__(self): pass
    def view_product(self,request):
        u = self.current_user(request)
        if 'action' in request.GET:
            deliver = list(Deliverable.objects.all().filter(buyer=u))
            if not len(deliver) or 'more' in request.GET:
                products = list(Product.objects.all())
                return self.render_grid(list(products),request)
            else: return self.render_grid(deliver,request)
        elif 'product' in request.GET:
            id = int(request.REQUEST['product'])
            prod = Product.objects.all().filter(id=id)[0]
            return render(request,'productview.pug',{'product':prod})
        else:
            return render(request,'product.pug',{'static_url':settings.STATIC_URL},content_type='text/html')
    def create_product(self,request):
        u = self.current_user(request)
        e = json.load(open('%s/json/elements.json'%settings.STATIC_ROOT))
        c = request.REQUEST['category']
        category = e['locale_cat'].index(c)
        credit = request.REQUEST['credit']
        name = request.REQUEST['name']
        description = request.REQUEST['description']
        product = Product(category=category,credit=credit,visual='',
        name='$$%s'%name,description=description,user=u)
        product.save()
        return redirect('productimage')
    def view_image(self,request):
        return render(request,'upload.pug',{'static_url':settings.STATIC_URL})
    def create_image(self,request):
        images = Images()
        u = self.current_user(request)
        url = images.upload_image(request)
        products = Product.objects.filter(user=u)
        latest = list(products)[-1:][0]
        latest.visual = url
        latest.save()
        return response("Product created successfully")
#payment_was_successful.connect(confirm_payment)
