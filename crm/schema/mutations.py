import graphene
from graphene import String, Field, List, Int, Decimal, Boolean, InputObjectType
from graphene.relay import Node
from graphql_relay import from_global_id
from django.db import transaction
from django.core.exceptions import ValidationError
from .. import models
from . import types, inputs


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = inputs.CustomerInput(required=True)
    
    customer = Field(types.CustomerType)
    success = Boolean()
    errors = List(String)
    
    @classmethod
    def mutate(cls, root, info, input):
        try:
            customer = models.Customer(
                name=input.get('name'),
                email=input.get('email'),
                phone=input.get('phone')
            )
            customer.full_clean()
            customer.save()
            return CreateCustomer(customer=customer, success=True)
        except ValidationError as e:
            errors = []
            for field, messages in e.message_dict.items():
                for message in messages:
                    errors.append(f"{field}: {message}")
            return CreateCustomer(customer=None, success=False, errors=errors)


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = inputs.BulkCustomerInput(required=True)
    
    customers = List(types.CustomerType)
    success = Boolean()
    errors = List(String)
    
    @classmethod
    def mutate(cls, root, info, input):
        customers_data = input.get('customers', [])
        customers = []
        errors = []
        
        with transaction.atomic():
            for idx, customer_data in enumerate(customers_data):
                try:
                    customer = models.Customer(
                        name=customer_data.get('name'),
                        email=customer_data.get('email'),
                        phone=customer_data.get('phone')
                    )
                    customer.full_clean()
                    customer.save()
                    customers.append(customer)
                except ValidationError as e:
                    for field, messages in e.message_dict.items():
                        for message in messages:
                            errors.append(f"Customer {idx + 1} - {field}: {message}")
                except Exception as e:
                    errors.append(f"Error creating customer {idx + 1}: {str(e)}")
        
        if errors and not customers:
            return BulkCreateCustomers(customers=None, success=False, errors=errors)
        
        return BulkCreateCustomers(customers=customers, success=bool(customers), errors=errors or None)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = inputs.ProductInput(required=True)
    
    product = Field(types.ProductType)
    success = Boolean()
    errors = List(String)
    
    @classmethod
    def mutate(cls, root, info, input):
        try:
            product = models.Product(
                name=input.get('name'),
                price=input.get('price'),
                description=input.get('description'),
                stock=input.get('stock', 0)
            )
            product.full_clean()
            product.save()
            return CreateProduct(product=product, success=True)
        except ValidationError as e:
            errors = []
            for field, messages in e.message_dict.items():
                for message in messages:
                    errors.append(f"{field}: {message}")
            return CreateProduct(product=None, success=False, errors=errors)


class OrderItemInput(InputObjectType):
    product_id = String(required=True)
    quantity = Int(required=True)


class OrderInput(InputObjectType):
    customer_id = String(required=True)
    items = List(OrderItemInput, required=True)


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)
    
    order = Field(types.OrderType)
    success = Boolean()
    errors = List(String)
    
    @classmethod
    def mutate(cls, root, info, input):
        try:
            customer_id = input.get('customer_id')
            items_data = input.get('items', [])
            
            if not items_data:
                return CreateOrder(
                    order=None,
                    success=False,
                    errors=["At least one product is required"]
                )
            
            try:
                # Convert from global ID to database ID
                _, customer_pk = from_global_id(customer_id)
                customer = models.Customer.objects.get(pk=customer_pk)
            except (models.Customer.DoesNotExist, ValueError, TypeError):
                return CreateOrder(
                    order=None,
                    success=False,
                    errors=["Customer not found"]
                )
            
            with transaction.atomic():
                order = models.Order(customer=customer)
                order.save()
                
                total_amount = 0
                for item_data in items_data:
                    try:
                        # Convert from global ID to database ID
                        _, product_pk = from_global_id(item_data.get('product_id'))
                        product = models.Product.objects.get(pk=product_pk)
                    except (models.Product.DoesNotExist, ValueError, TypeError):
                        transaction.set_rollback(True)
                        return CreateOrder(
                            order=None,
                            success=False,
                            errors=[f"Product not found"]
                        )
                    
                    quantity = item_data.get('quantity', 1)
                    if quantity < 1:
                        transaction.set_rollback(True)
                        return CreateOrder(
                            order=None,
                            success=False,
                            errors=[f"Invalid quantity for product {product.name}"]
                        )
                    
                    if product.stock < quantity:
                        transaction.set_rollback(True)
                        return CreateOrder(
                            order=None,
                            success=False,
                            errors=[f"Not enough stock for product {product.name}"]
                        )
                    
                    item_total = product.price * quantity
                    total_amount += item_total
                    
                    order_item = models.OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price_at_purchase=product.price
                    )
                    order_item.save()
                    
                    # Update product stock
                    product.stock -= quantity
                    product.save()
                
                order.total_amount = total_amount
                order.save()
                
                return CreateOrder(order=order, success=True)
                
        except Exception as e:
            return CreateOrder(
                order=None,
                success=False,
                errors=[f"Error creating order: {str(e)}"]
            )


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
