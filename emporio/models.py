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

from django.db import models
from django.db.models import *
from django.template import Context,Template
from django.contrib.auth.models import User

# Create your models here.

class Basket(Model):
    name = CharField(default='++',max_length=2)
    user = ForeignKey(User,related_name='+', on_delete=CASCADE)
    deliverable = BooleanField(default=False)
    product = IntegerField(default=1)
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    # def total_value(self): return self.quantity*self.product.credit
    # def product_trimmed(self): return self.product.name_trimmed()
    # def product_month(self): return self.product.real_month()

class Sellable(Model):
    name = CharField(default='$$',max_length=100)
    user = ForeignKey(User,related_name='+', on_delete=CASCADE)
    paid = BooleanField(default=False)
    returnable = BooleanField(default=False)
    value = FloatField(default=1.00)
    visual = CharField(default='',max_length=150)
    sellid = IntegerField(default=1)
    date = DateTimeField(auto_now_add=True)
    def token(self): return '$$'
    def name_trimmed(self): return self.name
    def type_object(self): return self.name[:2]
    def render(self):
        source = """
            <div class="col-xs-12 col-sm-6 col-md-3 col-lg-2 brick">
                <a class="block sellable" href="#" style="display:block; background-color:white">
                <div class="box" style="background-color:#333">
                <div class="content">
                <h2 class="title" style="color:white">{{nametrim}}</h2>
                {% if paid %}
                    <h2 class="lightgreen"> Valor j&aacute; pago </h2>
                {% endif %}
                <h1 class="centered"><span class="label label-info big-label"> R$ {{value}}0 </span></h1>
                <h1 class="centered"><span class="glyphicon glyphicon-shopping-cart giant-glyphicon style="color:white; margin-bottom:10px"></span></h1>
                <div class="id hidden">{{id}}</div>
            </div></div></div></a></div>
        """
        return Template(source).render(Context({
            'nametrim':  object.name_trimmed,
            'paid':      object.paid,
            'id':        object.id,
            'value':     object.value,
            'bio':       object.bio,
            'day':       object.date.day,
            'month':     object.month
        }))

class Product(Sellable):
    category = IntegerField(default=1)
    description = TextField()
    def token(self): return self.name[:3]
    def name_trimmed(self): return self.name.split(';')[0][2:]
    def month(self): return locale[self.date.month-1]

class Order(Model):
    user = ForeignKey(User,related_name='+', on_delete=CASCADE)