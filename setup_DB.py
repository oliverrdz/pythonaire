#!/usr/bin/env python
import os
import django

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonaire_api.settings')
    django.setup()

def migrate():
    from django.core.management import call_command
    call_command('makemigrations', 'core')
    call_command('migrate')

def populate_defaults():
    from core.models import CategoryType
    if CategoryType.objects.exists():
        print("Category Types already exist.")
        return
    CategoryType.objects.bulk_create([
        CategoryType(cat_type="Expense"),
        CategoryType(cat_type="Income"),
    ])
    print("Inserted default Category Types.")

if __name__ == '__main__':
    setup_django()
    migrate()
    populate_defaults()
