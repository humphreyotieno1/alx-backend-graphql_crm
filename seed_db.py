import os
import django

def run():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
    django.setup()
    
    from crm.models import Customer, Product, Order, OrderItem
    from django.db import transaction
    from datetime import datetime, timedelta
    import random
    
    print("Seeding database...")
    
    # Clear existing data
    with transaction.atomic():
        print("Deleting old data...")
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        Product.objects.all().delete()
    
    # Create customers
    customers = [
        Customer(name="Alice Johnson", email="alice@example.com", phone="+1234567890"),
        Customer(name="Bob Smith", email="bob@example.com", phone="123-456-7890"),
        Customer(name="Carol Williams", email="carol@example.com", phone="+1987654321"),
        Customer(name="David Brown", email="david@example.com"),
        Customer(name="Eve Davis", email="eve@example.com", phone="555-123-4567"),
    ]
    
    with transaction.atomic():
        print("Creating customers...")
        Customer.objects.bulk_create(customers)
    
    # Create products
    products = [
        Product(name="Laptop", description="High-performance laptop", price=999.99, stock=15),
        Product(name="Smartphone", description="Latest smartphone model", price=699.99, stock=30),
        Product(name="Headphones", description="Wireless noise-canceling headphones", price=199.99, stock=50),
        Product(name="Tablet", description="10-inch tablet", price=349.99, stock=20),
        Product(name="Smartwatch", description="Fitness and health tracking", price=249.99, stock=25),
        Product(name="Monitor", description="27-inch 4K monitor", price=299.99, stock=10),
        Product(name="Keyboard", description="Mechanical keyboard", price=129.99, stock=40),
        Product(name="Mouse", description="Wireless mouse", price=59.99, stock=60),
    ]
    
    with transaction.atomic():
        print("Creating products...")
        Product.objects.bulk_create(products)
    
    # Refresh objects to get their IDs
    customers = list(Customer.objects.all())
    products = list(Product.objects.all())
    
    # Create orders
    with transaction.atomic():
        print("Creating orders...")
        for i in range(20):
            customer = random.choice(customers)
            order = Order.objects.create(
                customer=customer,
                order_date=datetime.now() - timedelta(days=random.randint(0, 30)),
                status=random.choice(['pending', 'processing', 'completed', 'cancelled'])
            )
            
            # Add 1-4 random products to the order
            order_products = random.sample(products, k=random.randint(1, 4))
            total_amount = 0
            
            for product in order_products:
                quantity = random.randint(1, 3)
                price = product.price
                total_amount += price * quantity
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_purchase=price
                )
            
            order.total_amount = total_amount
            order.save()
    
    print("Database seeded successfully!")


if __name__ == "__main__":
    run()
