from rest_framework.decorators import api_view
from rest_framework.response import Response
 
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
