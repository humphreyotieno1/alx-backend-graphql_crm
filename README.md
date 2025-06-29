# ALX Backend GraphQL CRM

A GraphQL-based CRM (Customer Relationship Management) system built with Django and Graphene.

## Features

- **Customer Management**: Create, update, and query customer information
- **Product Catalog**: Manage products with pricing and inventory
- **Order Processing**: Create and track customer orders
- **GraphQL API**: Full-featured GraphQL API for all operations
- **Filtering & Search**: Advanced filtering and searching capabilities
- **Data Validation**: Comprehensive input validation and error handling

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- SQLite (included with Python)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/alx-backend-graphql_crm.git
   cd alx-backend-graphql_crm
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed the database with sample data (optional)**
   ```bash
   python seed_db.py
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- **GraphiQL Interface**: http://localhost:8000/graphql
- **Admin Interface**: http://localhost:8000/admin

## Example Queries and Mutations

### Create a Customer
```graphql
mutation {
  createCustomer(input: {
    name: "John Doe",
    email: "john@example.com",
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
      phone
    }
    success
    errors
  }
}
```

### Get All Customers with Filtering
```graphql
query {
  allCustomers(first: 10, filter: {name_Icontains: "john"}) {
    edges {
      node {
        id
        name
        email
        phone
        createdAt
      }
    }
  }
}
```

### Create an Order
```graphql
mutation {
  createOrder(input: {
    customerId: "1",
    items: [
      {productId: "1", quantity: 2},
      {productId: "3", quantity: 1}
    ]
  }) {
    order {
      id
      customer {
        name
        email
      }
      items {
        product {
          name
          price
        }
        quantity
        priceAtPurchase
      }
      totalAmount
      status
      orderDate
    }
    success
    errors
  }
}
```

## Filtering and Sorting

You can filter and sort results using the following parameters:

- **Customers**: Filter by name, email, phone, creation date
- **Products**: Filter by name, price range, stock level
- **Orders**: Filter by customer, product, date range, status, total amount

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
