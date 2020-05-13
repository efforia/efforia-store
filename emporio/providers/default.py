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

import locale, os

from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse as response
from django.template import Template, Context
from django.http import HttpResponseRedirect as redirect

def bancobrasil_payment(request,order):
    order.paypal_redirect_token = 'none'
    order.pagseguro_redirect = 'none'
    order.save()
    return order.id

def multiple_payment_handler(request, order_form, order):
	data = order_form.cleaned_data
	cart_items = []
	cart = Cart.objects.from_request(request)
	currency = settings.SHOP_CURRENCY
	for item in cart.items.all():
		cart_items.append({
			"name":item.description,
			"sku":item.sku,
			"price":'%.2f' % item.unit_price,
			"currency":currency,
			"quantity":item.quantity
		})
	price = cart.total_price() # + shipping TODO: integrate shipping_payment_handler
	if '1' in data['card_pay_option']:
		return paypal_payment(request,cart_items,price,currency,order)
	elif '2' in data['card_pay_option']:
		return pagseguro_payment(request,cart_items,price,order)
	elif '3' in data['card_pay_option']:
		return bancobrasil_payment(request,order)

def payment_redirect(self, request, order_id):
	logger.debug("feedly.views.payment_redirect(%s)" % order_id)
	lookup = {"id": order_id}
	if not request.user.is_authenticated():
		lookup["key"] = request.session.session_key
	elif not request.user.is_staff:
		lookup["user_id"] = request.user.id
	order = get_object_or_404(Order, **lookup)
	is_pagseguro = order.pagseguro_redirect
	if is_pagseguro is not None: return redirect(str(is_pagseguro))
	else: return self.paypal_redirect(request,order)

def process():
	# Bank Slip Option
	orderid = request.GET['id']
	order = Order.objects.filter(id=orderid)[0]
	send_mail('Pedido de boleto', 'O pedido de boleto foi solicitado ao Efforia para o pedido %s. Em instantes voc� estar� recebendo pelo e-mail. Aguarde instru��es.' % order.id, 'oi@efforia.com.br',
	[order.billing_detail_email,'contato@efforia.com.br'], fail_silently=False)
	context = { "order": order }
	resp = render(request,"shop/slip_confirmation.html",context)
	# return resp

	# Bank Transfer Option
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

def redirect():
	# Cartridge specific code
	order = None
	lookup = {"id": order_id}
	if not request.user.is_authenticated(): lookup["key"] = request.session.session_key
	elif not request.user.is_staff: lookup["user_id"] = request.user.id
	order = get_object_or_404(Order, **lookup)
	order.status = 2
	order.save()
	context = { "order" : order }
	response = render(request, template, context)
	return response