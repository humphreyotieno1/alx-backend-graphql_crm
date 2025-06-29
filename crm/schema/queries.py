import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene.relay import Node
from graphql_relay import from_global_id
from .. import models
from . import types


class Query(graphene.ObjectType):
    """Root query for the CRM application."""
    # Customer queries
    customer = Node.Field(types.CustomerType)
    all_customers = DjangoFilterConnectionField(
        types.CustomerType,
        description="List all customers with optional filtering and searching"
    )
    
    # Product queries
    product = Node.Field(types.ProductType)
    all_products = DjangoFilterConnectionField(
        types.ProductType,
        description="List all products with optional filtering and searching"
    )
    
    # Order queries
    order = Node.Field(types.OrderType)
    all_orders = DjangoFilterConnectionField(
        types.OrderType,
        description="List all orders with optional filtering and searching"
    )
    
    # Resolvers (kept for backward compatibility)
    def resolve_customer(self, info, id):
        """Resolve a single customer by ID."""
        try:
            _, pk = from_global_id(id)
            return models.Customer.objects.get(pk=pk)
        except (models.Customer.DoesNotExist, ValueError, TypeError):
            return None
    
    def resolve_product(self, info, id):
        """Resolve a single product by ID."""
        try:
            _, pk = from_global_id(id)
            return models.Product.objects.get(pk=pk)
        except (models.Product.DoesNotExist, ValueError, TypeError):
            return None
    
    def resolve_order(self, info, id):
        """Resolve a single order by ID."""
        try:
            _, pk = from_global_id(id)
            return models.Order.objects.get(pk=pk)
        except (models.Order.DoesNotExist, ValueError, TypeError):
            return None
