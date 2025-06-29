import django_filters
from django.db.models import Q
from . import models


class CustomerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')
    
    class Meta:
        model = models.Customer
        fields = {
            'name': ['icontains', 'iexact'],
            'email': ['icontains', 'iexact'],
            'created_at': ['gte', 'lte', 'exact'],
        }
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value)
        )
    
    def filter_phone_pattern(self, queryset, name, value):
        """Filter customers by phone number pattern."""
        if value.startswith('+'):
            return queryset.filter(phone__startswith=value)
        return queryset.filter(phone__contains=value.replace('-', ''))


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')
    
    class Meta:
        model = models.Product
        fields = {
            'name': ['icontains', 'iexact'],
            'price': ['exact', 'gt', 'lt'],
            'stock': ['exact', 'gt', 'lt'],
        }
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)
    
    def filter_low_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__lt=10)
        return queryset


class OrderFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    product_name = django_filters.CharFilter(field_name='items__product__name', lookup_expr='icontains')
    
    class Meta:
        model = models.Order
        fields = {
            'status': ['exact'],
            'total_amount': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'order_date': ['exact', 'gt', 'lt', 'gte', 'lte', 'date'],
        }
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(customer__name__icontains=value) |
            Q(customer__email__icontains=value) |
            Q(items__product__name__icontains=value)
        ).distinct()
