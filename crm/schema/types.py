import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from .. import models


class CustomerType(DjangoObjectType):
    class Meta:
        model = models.Customer
        fields = ('id', 'name', 'email', 'phone', 'created_at', 'updated_at')
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'created_at': ['exact', 'lt', 'gt', 'lte', 'gte', 'date'],
        }


class ProductType(DjangoObjectType):
    class Meta:
        model = models.Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'in_stock', 'created_at', 'updated_at')
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['icontains', 'search'],
            'price': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'stock': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'in_stock': ['exact'],
            'created_at': ['exact', 'lt', 'gt', 'lte', 'gte', 'date'],
        }


class OrderItemType(DjangoObjectType):
    class Meta:
        model = models.OrderItem
        fields = ('id', 'order', 'product', 'quantity', 'price_at_purchase', 'created_at')
        interfaces = (relay.Node,)
        filter_fields = {
            'order': ['exact'],
            'product': ['exact'],
            'quantity': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }


class OrderType(DjangoObjectType):
    items = DjangoFilterConnectionField(OrderItemType)
    
    class Meta:
        model = models.Order
        fields = ('id', 'customer', 'status', 'total_amount', 'order_date', 'created_at', 'updated_at')
        interfaces = (relay.Node,)
        filter_fields = {
            'status': ['exact', 'icontains'],
            'total_amount': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'order_date': ['exact', 'lt', 'gt', 'lte', 'gte', 'year', 'month', 'day'],
            'customer__name': ['exact', 'icontains'],
            'customer__email': ['exact', 'icontains'],
            'items__product__name': ['exact', 'icontains'],
        }
    
    def resolve_items(self, info, **kwargs):
        return self.items.all()
