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

urlpatterns = [
    path('orders/', include([
        path('<int:pk>/redirect/', PaymentRedirectView.as_view(), name="payment_redirect"),
        path('<int:pk>/process/', PaymentsView.as_view(), name="payment_execute"),
        path('<int:pk>/cancel/', PaymentCancelView.as_view(), name="payment_cancel"),
        path('<int:pk>/', OrdersDetailView.as_view()),
        path('', OrdersListView.as_view()),
    ])),
    path('baskets/', include([
        path('<int:pk>/', BasketsDetailView.as_view()),
        path('', BasketsListView.as_view()),
    ])),
    path('products/', include([
        path('<int:pk>/', ProductsDetailView.as_view()),
        path('', ProductsListView.as_view()),
    ])),
]