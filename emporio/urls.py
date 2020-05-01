from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url("^pay/(?P<order_id>\d+)/$", payment_redirect, name="payment_redirect"),
    url("^execute", payment_execute, name="payment_execute"),
    url(r'^basketclean', basketclean),
    url(r'^basket', basket),
    url(r'^pagseguro/cart', pagsegurocart),
    url(r'^pagseguro', pagseguro),
    url(r'^paypal/cart', paypalcart),
    url(r'^paypal', paypal),
]