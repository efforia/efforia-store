#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.forms import Form,CharField,ChoiceField,RadioSelect
from cartridge.shop.forms import OrderForm

class ExternalPaymentOrderForm(OrderForm):
	GATEWAYS = (
       (1, "PayPal"),
       (2, "PagSeguro"), 
   	)   
	# Billing and shipping step
	billing_detail_complement = CharField(max_length=100,label="Número ou complemento do endereço")
	shipping_detail_complement = CharField(max_length=100,label="Número ou complemento do endereço")
	# Online payment step
	card_pay_option = ChoiceField(widget=RadioSelect,choices=GATEWAYS,label="Forma de pagamento online")
	def __init__(self,*args,**kwargs):
		super(ExternalPaymentOrderForm,self).__init__(*args,**kwargs)
		del self.fields['card_expiry_year']

excluded = ('card_name','card_type','card_number','card_expiry_month','card_ccv',
			'billing_detail_street','billing_detail_city','billing_detail_state',
			'billing_detail_country','shipping_detail_street','shipping_detail_city',
			'shipping_detail_state','shipping_detail_country')

for field in excluded:
	del ExternalPaymentOrderForm.base_fields[field]