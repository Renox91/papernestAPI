from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getData(request):
    operators = { 'name': 'orange', '2G': True, '3G': True, '4G': False }
    return Response(operators)