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

import logging, urllib.parse

from django.shortcuts import render
from django.http import HttpResponse as response
from django.conf import settings
from django.template import Context,Template
from django import forms
from django.http import Http404,HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _

logger = logging.getLogger("feedly.views")

try:
    from paypalrestsdk import Payment
    import paypalrestsdk
except ImportError as e:
    logging.info("Extension modules deactivated: they could not be found.")

class PagSeguro():
    def process(self,request,cart=None):
        for k,v in request.REQUEST.items():
            if 'product' in k: product = v
            elif 'value' in k: value = float(v)
            elif 'qty' in k: qty = int(v)
        try:
            carrinho = CarrinhoPagSeguro(ref_transacao=1); count = 0
            if cart is not None:
                for p in cart:
                    count += 1
                    carrinho.add_item(ItemPagSeguro(cod=count,descr=p['product'],quant=p['qty'],valor=p['value']))
            else:
                carrinho.add_item(ItemPagSeguro(cod=1,descr=product,quant=qty,valor=value))
        except (ImportError,NameError) as e:
            carrinho = BasketForm()
        t = Template("{{form}}")
        c = Context({'form':carrinho.form()})
        return response(t.render(c))

def pagseguro_payment(request,items,price,order):
	server_host = request.get_host()
	payment = pagseguro_api()
	for product in items:
		payment.add_item(id=product['sku'],
        				 description=product['name'],
        				 amount=product['price'],
        				 quantity=product['quantity'])
	payment.redirect_url = "http://%s/store/execute" % server_host
	payment.reference_prefix = None
	payment.reference = order.id
	resp = payment.checkout()
	order.pagseguro_code = resp.code
	order.pagseguro_redirect = resp.payment_url
	order.paypal_redirect_token = 'none'
	order.save()
	return resp.code

def pagseguro_api():
	try:
		if settings.PAGSEGURO_SANDBOX_MODE:
			email = settings.PAGSEGURO_SANDBOX_EMAIL_COBRANCA
			token = settings.PAGSEGURO_SANDBOX_TOKEN
		else:
			email = settings.PAGSEGURO_EMAIL_COBRANCA
			token = settings.PAGSEGURO_TOKEN
	except AttributeError:
		raise ImproperlyConfigured(_("Credenciais de acesso ao pagseguro estao faltando, "
								 "isso inclui PAGSEGURO_SANDBOX_MODE, PAGSEGURO_CLIENT_ID e PAGSEGURO_CLIENT_SECRET "
								 "basta inclui-las no settings.py para serem utilizadas "
								 "no processador de pagamentos do pagseguro."))
	if settings.PAGSEGURO_SANDBOX_MODE: api = PagSeguroSandbox(email=email,token=token)
	else: api = pagseguro.PagSeguro(email=email,token=token)
	return api

class SandboxConfig(pagseguro.Config):
	BASE_URL = "https://ws.sandbox.pagseguro.uol.com.br"
	PAYMENT_HOST = "https://sandbox.pagseguro.uol.com.br"
	VERSION = "/v2/"
	CHECKOUT_SUFFIX = VERSION + "checkout"
	CHARSET = "UTF-8"  # ISO-8859-1
	NOTIFICATION_SUFFIX = VERSION + "transactions/notifications/%s"
	TRANSACTION_SUFFIX = VERSION + "transactions/%s"
	CHECKOUT_URL = BASE_URL + CHECKOUT_SUFFIX
	NOTIFICATION_URL = BASE_URL + NOTIFICATION_SUFFIX
	TRANSACTION_URL = BASE_URL + TRANSACTION_SUFFIX
	CURRENCY = "BRL"
	CTYPE = "application/x-www-form-urlencoded; charset={0}".format(CHARSET)
	HEADERS = {"Content-Type": CTYPE}
	REFERENCE_PREFIX = "REF%s"
	PAYMENT_URL = PAYMENT_HOST + CHECKOUT_SUFFIX + "/payment.html?code=%s"
	DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

class PagSeguroSandbox(pagseguro.PagSeguro):
	def __init__(self,email,token,data=None):
		self.config = SandboxConfig()
		self.data = {}
		self.data['email'] = email
		self.data['token'] = token
		if data and isinstance(data, dict): self.data.update(data)
		self.items = []
		self.sender = {}
		self.shipping = {}
		self._reference = ""
		self.extra_amount = None
		self.redirect_url = None
		self.notification_url = None
		self.abandon_url = None


def process():
	pagseguro = PagSeguro()
	pagseguro.process(request)
	pagseguro.process_cart(request)

def redirect():
	order = None
	lookup = {}
	if request.GET.has_key('transaction_id'):
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
