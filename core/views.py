from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets
from .models import CategoryType, Category, Account, Transaction
from .serializers import (
    CategoryTypeSerializer, CategorySerializer,
    AccountSerializer, TransactionSerializer
)

def index(request):
    return render(request, 'core/index.html')

class CategoryTypeViewSet(viewsets.ModelViewSet):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'cat_name'

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'acc_name'

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


def index(request):
    return render(request, 'core/index.html')
