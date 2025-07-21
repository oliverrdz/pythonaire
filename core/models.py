from django.db import models

class CategoryType(models.Model):
    cat_type = models.CharField(max_length=100)

class Category(models.Model):
    cat_name = models.CharField(max_length=100, unique=True)

class Account(models.Model):
    acc_name = models.CharField(max_length=100, unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    acc_total = models.FloatField(default=0.0)
    acc_notes = models.TextField(blank=True)

class Transaction(models.Model):
    trans_date = models.DateTimeField(auto_now_add=True)
    acc = models.ForeignKey(Account, on_delete=models.CASCADE)
    trans_amount = models.FloatField()
    cat_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    trans_notes = models.TextField(blank=True)
