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

from django.utils.translation import ugettext_lazy as _
from django.forms import Form,CharField,ChoiceField,RadioSelect,BooleanField,CheckboxInput,Textarea

from cartridge.shop.forms import OrderForm

class BasketForm(Form):
    business = CharField(max_length=100)
    notify_url = CharField(max_length=100)
    return_url = CharField(max_length=100)
    cancel_return = CharField(max_length=100)
    currency_code = CharField(max_length=10)
    def render(self): return ''
    def form(self): return ''

class ExternalPaymentOrderForm(OrderForm):
	GATEWAYS = (
       (1, "PayPal"),
       (2, "PagSeguro"),
       (3, "BancoBrasil") 
   	)   
	# Billing and shipping step
	billing_detail_complement = CharField(max_length=100,label="Número ou complemento do endereço")
	shipping_detail_complement = CharField(max_length=100,label="Número ou complemento do endereço")
	same_billing_shipping = BooleanField(required=False,initial=True,label=_("My delivery details are the same as my billing details"),
									     widget=CheckboxInput(attrs={'checked':'checked'}))
	additional_instructions = CharField(widget=Textarea,label="CPF e outras informações",initial="Favor informar CPF para a nota fiscal e observações sobre a entrega neste campo.")

	# Online payment step
	card_pay_option = ChoiceField(widget=RadioSelect,choices=GATEWAYS,label="Forma de pagamento online")
	def __init__(self,*args,**kwargs):
		super(ExternalPaymentOrderForm,self).__init__(*args,**kwargs)
		del self.fields['card_expiry_year']

excluded = ('card_name','card_type','card_number','card_expiry_month','card_ccv',
			'billing_detail_street','billing_detail_city','billing_detail_state',
			'billing_detail_country','shipping_detail_street','shipping_detail_city',
			'shipping_detail_state','shipping_detail_country') # ,'same_billing_shipping')

for field in excluded:
	del ExternalPaymentOrderForm.base_fields[field]