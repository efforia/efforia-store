import locale,paypalrestsdk,pagseguro,os
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse as response
from django.template import Template,Context
from django.http import HttpResponseRedirect as redirect
from shipping.codes import CorreiosCode
from shipping.fretefacil import FreteFacilShippingService
from shipping.correios import CorreiosShippingService
from shipping.models import DeliverableProperty
from mezzanine.conf import settings
from cartridge.shop.utils import set_shipping
from cartridge.shop.forms import OrderForm
from cartridge.shop.models import Cart
from cartridge.shop.checkout import CheckoutError

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


# Deprecated
def fretefacil_shipping_handler(request, form, order=None):
    if request.session.get("free_shipping"): return
    settings.use_editable()
    if form is not None: user_postcode = form.cleaned_data['shipping_detail_postcode']
    else: user_postcode = settings.STORE_POSTCODE 
    shippingservice = FreteFacilShippingService()
    cart = Cart.objects.from_request(request)
    delivery_value = 0.0
    if cart.has_items():
        for product in cart:
            properties = DeliverableProperty.objects.filter(sku=product.sku)
            if len(properties) > 0:
                props = properties[0]
                deliverable = shippingservice.create_deliverable(settings.STORE_POSTCODE,
                                                                 user_postcode,
                                                                 props.width,
                                                                 props.height,
                                                                 props.length,
                                                                 props.weight)
                delivery_value += float(shippingservice.delivery_value(deliverable))
    set_shipping(request, _("Correios"),delivery_value)

def correios_create_deliverable(obj,service,store_postcode,user_postcode,width,height,length,weight):
    obj.cep_origem = store_postcode
    obj.altura = height
    obj.largura = width
    obj.comprimento = length
    obj.peso = weight
    obj.servico = service
    return {
        'postcode':user_postcode,
        'service':service
    }


def correios_delivery_value(shippingservice,deliverable):
    shippingservice(deliverable['postcode'],deliverable['service'])
    return '.'.join(shippingservice.results[deliverable['service']][1].split(','))

def sedex_shipping_handler(request, form, order=None):
    if request.session.get("free_shipping"): return
    settings.use_editable()
    if form is not None: user_postcode = form.cleaned_data['shipping_detail_postcode']
    else: user_postcode = settings.STORE_POSTCODE 
    shippingservice = CorreiosShippingService()
    cart = Cart.objects.from_request(request)
    delivery_value = 0.0
    if cart.has_items():
        for product in cart:
            properties = DeliverableProperty.objects.filter(sku=product.sku)
            if len(properties) > 0:
                props = properties[0]
                deliverable = correios_create_deliverable(shippingservice,
                                                          'SEDEX',
                                                          settings.STORE_POSTCODE,
                                                          user_postcode,
                                                          props.width,
                                                          props.height,
                                                          props.length,
                                                          props.weight)
                delivery_value += float(correios_delivery_value(shippingservice,deliverable))
    set_shipping(request, _("Correios"),delivery_value)

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

def multiple_payment_handler(request, order_form, order):
	data = order_form.cleaned_data
	shipping = order.shipping_total
	code = CorreiosCode()
	shipping_data = code.consulta(order.billing_detail_postcode)[0]
	order.billing_detail_street  = '%s %s' % (shipping_data['Logradouro'],data['billing_detail_complement'])
	order.billing_detail_city    = shipping_data['Localidade']
	order.billing_detail_state   = shipping_data['UF']
	order.billing_detail_country = settings.STORE_COUNTRY
	order.save()
	cart = Cart.objects.from_request(request)
	currency = settings.SHOP_CURRENCY
	cart_items = []
	has_shipping = False
	for item in cart.items.all():
		quantity = len(DeliverableProperty.objects.filter(sku=item.sku))
		if quantity > 0: has_shipping = True
		cart_items.append({
			"name":item.description,
			"sku":item.sku,
			"price":'%.2f' % item.unit_price,
			"currency":currency,
			"quantity":item.quantity
		})
	if has_shipping:
		cart_items.append({
			"name": "Frete via SEDEX",
			"sku":"1",
			"price":'%.2f' % shipping,
			"currency":currency,
			"quantity":1
		})
	price = cart.total_price()+shipping
	if '1' in data['card_pay_option']:
		return paypal_payment(request,cart_items,price,currency,order)
	elif '2' in data['card_pay_option']:
		return pagseguro_payment(request,cart_items,price,order)
	elif '3' in data['card_pay_option']:
		return bancobrasil_payment(request,order)

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
