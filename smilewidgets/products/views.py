from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import *
import json
import datetime

# Create your views here.
@api_view(["POST"])
def get_price(request):
	try:
		data = request.POST.dict()
		productCode = data['productCode']
		productdate = datetime.datetime.strptime(data['date'],  "%Y-%m-%d").date()

		product = Product.objects.get(code=productCode)
		try:
			productprice = ProductPrice.objects.get(product=product, 
			start_date__lte=productdate,
			end_date__gte=productdate).updated_price
		except:
			productprice = product.price
		if 'giftCardCode' in data:
			discount = GiftCard.objects.get(code=data['giftCardCode']).amount
			productprice = productprice - discount
		if productprice < 0:
			productprice = 0
		return JsonResponse({"price": productprice}, safe=False)

	except ValueError as e:
	    return Response(e.args[0], status.HTTP_400_BAD_REQUEST)