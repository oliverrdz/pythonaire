from django.contrib import admin
from .models import CategoryType, Category, Account, Transaction

admin.site.register(CategoryType)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Transaction)
