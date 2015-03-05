import paypalrestsdk,urlparse
from hooks import paypal_api,pagseguro_api
from django.http import Http404,HttpResponse
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
    if not request.user.is_authenticated():
        lookup["key"] = request.session.session_key
    elif not request.user.is_staff:
        lookup["user_id"] = request.user.id
    order = get_object_or_404(Order, **lookup)
    is_pagseguro = order.pagseguro_redirect 
    if is_pagseguro is not None: return redirect(str(is_pagseguro))
    else: return paypal_redirect(request,order)

def payment_execute(request, template="shop/payment_confirmation.html"):    
    paypal_api()
    token = request.GET['token']
    payer_id = request.GET['PayerID']
    order = get_object_or_404(Order, paypal_redirect_token=token)
    payment = Payment.find(order.transaction_id)
    payment.execute({ "payer_id": payer_id })
    order.status = 3
    order.save()
    context = { "order" : order }
    response = render(request, template, context)
    return response