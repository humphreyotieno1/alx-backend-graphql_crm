import graphene
from graphene import InputObjectType, String, Decimal, Int, List, Field


class CustomerInput(InputObjectType):
    name = String(required=True)
    email = String(required=True)
    phone = String()


class BulkCustomerInput(InputObjectType):
    customers = List(CustomerInput, required=True)


class ProductInput(InputObjectType):
    name = String(required=True)
    price = Decimal(required=True)
    description = String()
    stock = Int()


class OrderItemInput(InputObjectType):
    product_id = String(required=True)
    quantity = Int(required=True)


class OrderInput(InputObjectType):
    customer_id = String(required=True)
    items = List(OrderItemInput, required=True)
