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

from django.conf.urls import url, include
from django.urls import path

from .views import *

baskets_patterns = ([
    path('', BasketsView.as_view()),
    url(r'^basketclean', basketclean),
    url(r'^basket', basket),
], 'baskets')

products_patterns = ([
    path('', ProductsView.as_view())
], 'products')

urlpatterns = [
    path('baskets', include(baskets_patterns)),
    path('products', include(products_patterns)),
    url("^pay/(?P<order_id>\d+)/$", payment_redirect, name="payment_redirect"),
    url("^execute", payment_execute, name="payment_execute"),
    url(r'^pagseguro/cart', pagsegurocart),
    url(r'^pagseguro', pagseguro),
    url(r'^paypal/cart', paypalcart),
    url(r'^paypal', paypal),
]