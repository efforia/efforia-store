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

class Product(Sellable):
    category = IntegerField(default=1)
    description = TextField()
    def token(self): return self.name[:3]
    def name_trimmed(self): return self.name.split(';')[0][2:]
    def month(self): return locale[self.date.month-1]

class Order(Model):
    user = ForeignKey(User,related_name='+', on_delete=CASCADE)