from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import CategoryTypeViewSet, CategoryViewSet, AccountViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'category-types', CategoryTypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

@api_view(['GET'])
def api_root(request):
    return Response({
        "category-types": request.build_absolute_uri('category-types/'),
        "categories": request.build_absolute_uri('categories/'),
        "accounts": request.build_absolute_uri('accounts/'),
        "transactions": request.build_absolute_uri('transactions/'),
    })

urlpatterns = [
    path('', api_root),  # This adds the index at /api/
    path('', include(router.urls)),
]