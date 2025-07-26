from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ..serializers.base import ApiOverviewSerializer
 
@extend_schema(responses=ApiOverviewSerializer)
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'app-name': 'MyStore API',
        'routes': {
            'Overview-page': '/api/',
            'User-related-urls': '/api/user/',
            'product-related-urls': '/api/product/',
            'order-related-urls': '/api/order/',
        }
    }
 
    return Response(api_urls)
