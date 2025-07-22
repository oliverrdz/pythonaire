from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    index,
    CategoryTypeViewSet, CategoryViewSet,
    AccountViewSet, TransactionViewSet
)

router = DefaultRouter()
router.register(r'category-types', CategoryTypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
]
