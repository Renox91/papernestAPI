from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils.geocode import get_coverage
import requests

@api_view(['GET'])
def getCoverage(request):
    """
    Get mobile network coverage for a given address.
    
    Args:
        request: Django request object with 'q' parameter (address)
    
    Returns:
        Response: JSON with operator coverage information
        {
            "Orange": {"2G": true, "3G": true, "4G": false},
            "SFR": {"2G": true, "3G": true, "4G": true},
            "Free": {"2G": false, "3G": true, "4G": true},
            "Bouygues": {"2G": true, "3G": false, "4G": true},
        }
    
    Raises:
        400: Missing address parameter
        503: External service unavailable
        500: Internal server error
    """
    try:
        address = request.query_params.get('q')
        if not address:
            return Response({'error': 'Address parameter (q=<address>) required'}, status=400)
        
        result = get_coverage(address)
        return Response(result)
    
    except requests.RequestException as e:
        return Response({'error': 'Geocoding service unavailable'}, status=503)
    
    except Exception as e:
        return Response({'error': 'Internal server error'}, status=500)