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
from django.urls import path, re_path

from .views import *

orders_patterns = ([
    re_path('<int:pk>/redirect/', PaymentRedirectView.as_view(), name="payment_redirect"),
    re_path('<int:pk>/process/', PaymentsView.as_view(), name="payment_execute"),
    re_path('<int:pk>/cancel/', PaymentCancelView.as_view(), name="payment_cancel"),
    path('<int:pk>/', OrdersDetailView.as_view()),
    re_path('', OrdersListView.as_view()),
], 'orders')

baskets_patterns = ([
    re_path('(?P<pk>\d+)/', BasketsDetailView.as_view()),
    re_path('', BasketsListView.as_view()),
], 'baskets')

products_patterns = ([
    re_path('(?P<pk>\d+)/', ProductsDetailView.as_view()),
    re_path('', ProductsListView.as_view()),
], 'products')

urlpatterns = [
    path('orders/', include(orders_patterns)),
    path('baskets/', include(baskets_patterns)),
    path('products/', include(products_patterns)),
]