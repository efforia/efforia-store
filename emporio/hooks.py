import locale, os
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse as response
from django.template import Template, Context
from django.http import HttpResponseRedirect as redirect

try:
	from mezzanine.conf import settings
	from cartridge.shop.utils import set_shipping
	from cartridge.shop.forms import OrderForm
	from cartridge.shop.models import Cart
	from cartridge.shop.checkout import CheckoutError
	import paypalrestsdk
	import pagseguro
except ImportError as e:
	pass

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

def paypal_api():
	try:
		if settings.PAYPAL_SANDBOX_MODE:
			mode = 'sandbox'
			client_id = settings.PAYPAL_SANDBOX_CLIENT_ID
			client_secret = settings.PAYPAL_SANDBOX_CLIENT_SECRET
		else:
			mode = 'live'
			client_id = settings.PAYPAL_CLIENT_ID
			client_secret = settings.PAYPAL_CLIENT_SECRET
	except AttributeError:
		raise ImproperlyConfigured(_("Credenciais de acesso ao paypal estao faltando, "
								 "isso inclui PAYPAL_SANDBOX_MODE, PAYPAL_CLIENT_ID e PAYPAL_CLIENT_SECRET "
								 "basta inclui-las no settings.py para serem utilizadas "
								 "no processador de pagamentos do paypal."))
	api = paypalrestsdk.set_config(mode = mode,	client_id = client_id, client_secret = client_secret)
	os.environ['PAYPAL_MODE'] = mode
	os.environ['PAYPAL_CLIENT_ID'] = client_id
	os.environ['PAYPAL_CLIENT_SECRET'] = client_secret
	return api

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

def bancobrasil_payment(request,order):
    order.paypal_redirect_token = 'none'
    order.pagseguro_redirect = 'none'
    order.save()
    return order.id

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

def paypal_payment(request,items,price,currency,order):
	paypal_api()
	server_host = request.get_host()
	payment = paypalrestsdk.Payment({
		"intent": "sale",
		"payer": {
			"payment_method": "paypal",
		},
		"redirect_urls" : {
			"return_url" : "http://%s/store/execute" % server_host,
			"cancel_url" : "http://%s/store/cancel" % server_host
		},
		"transactions": [{
			"item_list":{ "items":items	},
			"amount": {
				"total": '%.2f' % price,
				"currency": currency
			},
			"description": "Compra de Produtos na loja."
		}]
	})
	order.paypal_redirect_token = ""
	order.pagseguro_redirect = 'none'
	if payment.create(): return payment.id
	else: raise CheckoutError(payment.error)

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