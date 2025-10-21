from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils.geocode import get_geocode

@api_view(['GET'])
def getData(request):
    operators = { 'name': 'orange', '2G': True, '3G': True, '4G': False }
    return Response(operators)

@api_view(['GET'])
def getGeocode(request):
    address = request.query_params.get('q')
    if not address:
        return Response({'error': 'Address parameter required'}, status=400)
    return Response(get_geocode(address))