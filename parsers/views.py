from django.shortcuts import render
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from parsers.dispatcher import start_coin


@api_view(['GET'])
# @schema(None)
def create_worker(request):
    try:
        res = start_coin()
    except Exception as ex:
        print(ex)
        res = 'Нет подключения'
    # res = start_coin()
    return Response({"answer": res})