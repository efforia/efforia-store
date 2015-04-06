# -*- coding: UTF-8 -*-

import paypalrestsdk,urlparse,urllib2
from xml.etree import ElementTree as ETree
from hooks import paypal_api,pagseguro_api
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404,HttpResponse
from django.http import HttpResponse as response
from django.shortcuts import get_object_or_404,redirect,render
from cartridge.shop.models import Product, ProductVariation, Order, OrderItem
from paypalrestsdk import Payment

def payment_cancel(request):
    # Not implemented already
    return redirect('/')

def paypal_redirect(request,order):
    paypal_api()
    payment = paypalrestsdk.Payment.find(order.transaction_id)
    for link in payment.links:
        if link.method == "REDIRECT":
            redirect_url = link.href
            url = urlparse.urlparse(link.href)
            params = urlparse.parse_qs(url.query)
            redirect_token = params['token'][0]
            order.paypal_redirect_token = redirect_token
            order.save()
    return redirect(redirect_url)

def payment_redirect(request, order_id):
    lookup = {"id": order_id}
    if not request.user.is_authenticated(): lookup["key"] = request.session.session_key
    elif not request.user.is_staff: lookup["user_id"] = request.user.id
    order = get_object_or_404(Order, **lookup)
    is_pagseguro = order.pagseguro_redirect 
    is_paypal = order.paypal_redirect_token
    if 'none' not in is_pagseguro: return redirect(str(is_pagseguro))
    elif 'none' not in is_paypal: return paypal_redirect(request,order)
    else: return redirect("/store/execute?orderid=%s" % lookup["id"])

def payment_slip(request):
	orderid = request.GET['id']
	order = Order.objects.filter(id=orderid)[0]
	send_mail('Pedido de boleto', 'O pedido de boleto foi solicitado ao Efforia para o pedido %s. Em instantes você estará recebendo pelo e-mail. Aguarde instruções.' % order.id, 'oi@efforia.com.br',
    [order.billing_detail_email,'contato@efforia.com.br'], fail_silently=False)
	context = { "order": order }
	resp = render(request,"shop/slip_confirmation.html",context)
	return resp

def payment_bank(request):
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

def payment_execute(request, template="shop/payment_confirmation.html"):    
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
		resp = urllib2.urlopen("%s?email=%s&token=%s" % (url,email,token)).read()
		lookup["id"] = ETree.fromstring(resp).findall("reference")[0].text
		print ETree.fromstring(resp).findall("reference")[0].text
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
