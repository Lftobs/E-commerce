from rest_framework.decorators import api_view
from rest_framework.response import Response
 
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'app-name': 'MyStore API',
        'routes': {
            'Overview-page': '/',
            'User-related-urls': '/user/',
            'product-related-urls': '/product/',
            'order-related-urls': '/order/',
        }
    }
 
    return Response(api_urls)
