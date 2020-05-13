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

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import payment_was_successful

class PayPal():
    def process(self,request,cart=None):
        for k,v in request.REQUEST.items():
            if 'product' in k: product = v
            elif 'value' in k: value = float(v)
            elif 'qty' in k: qty = int(v)
        host = 'http://%s' % request.get_host()
        paypal = {
            'business':      settings.PAYPAL_RECEIVER_EMAIL,
            'notify_url':    '%s%s'%(host,settings.PAYPAL_NOTIFY_URL),
            'return_url':    '%s%s'%(host,settings.PAYPAL_RETURN_URL),
            'cancel_return': '%s%s'%(host,settings.PAYPAL_CANCEL_RETURN),
            'currency_code': 'BRL',
        }
        option = '_cart'; count = 0
        try:
            form_paypal = PayPalPaymentsForm(initial=paypal)
            if cart is not None:
                for p in cart:
                    count += 1
                    form_paypal.fields['amount_%i'%count] = forms.IntegerField(widget=ValueHiddenInput(),initial=p['value'])
                    form_paypal.fields['item_name_%i'%count] = forms.CharField(widget=ValueHiddenInput(),initial=p['product'])
                    form_paypal.fields['quantity_%i'%count] = forms.CharField(widget=ValueHiddenInput(),initial=p['qty'])
            else:
                form_paypal.fields['amount_1'] = forms.IntegerField(widget=ValueHiddenInput(),initial=value)
                form_paypal.fields['item_name_1'] = forms.CharField(widget=ValueHiddenInput(),initial=product)
                form_paypal.fields['quantity_1'] = forms.CharField(widget=ValueHiddenInput(),initial=str(qty))
            form_paypal.fields['cmd'] = forms.CharField(widget=ValueHiddenInput(),initial=option)
            form_paypal.fields['upload'] = forms.CharField(widget=ValueHiddenInput(),initial='1')
        except (NameError,ImportError) as e:
            form_paypal = BasketForm(initial=paypal)
        t = Template('{{form}}')
        c = Context({'form':form_paypal.render()})
        return response(t.render(c))

    def paypal_redirect(self,request,order):
        paypal_api()
        payment = paypalrestsdk.Payment.find(order.transaction_id)
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
                url = urllib.parse.urlparse(link.href)
                params = urllib.parse.parse_qs(url.query)
                redirect_token = params['token'][0]
                order.paypal_redirect_token = redirect_token
                order.save()
        logger.debug("redirect url : %s" % redirect_url)
        return redirect(redirect_url)

    def payment_execute(self, request, template="shop/payment_confirmation.html"):
        paypal_api()
        token = request.GET['token']
        payer_id = request.GET['PayerID']
        logger.debug("feedly.views.payment_execute(token=%s,payer_id=%s)" % (token,payer_id))
        order = get_object_or_404(Order, paypal_redirect_token=token)
        payment = Payment.find(order.transaction_id)
        payment.execute({ "payer_id": payer_id })
        # Pago, falta enviar
        order.status = 3
        order.save()
        context = { "order" : order }
        response = render(request, template, context)
        return response

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

def process():
    paypal = PayPal()
    paypal.process(request)
    paypal.process_cart(request)


def redirect():
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