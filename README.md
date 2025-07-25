# Me-Mart API

This is the API for Me-Mart, a simple e-commerce application. It provides endpoints for managing users, products, carts, and orders.

## Features

- User authentication (signup, login) with JWT
- Product management (create, read, update, delete)
- Shopping cart functionality
- Order management
- API documentation with Swagger and ReDoc

## API Endpoints

### Authentication

- `POST /api/signup/`: Register a new user.
- `POST /api/login/`: Log in a user and get an access token.
- `POST /api/token/refresh/`: Refresh an access token.
- `GET /api/users/all/`: Get a list of all users (admin only).
- `GET /api/user/`: Get the current user's details.
- `PUT /api/user/`: Update the current user's details.

### Products

- `GET /api/product/`: Get a list of all products.
- `POST /api/product/`: Create a new product.
- `GET /api/product/<int:pk>/`: Get a single product by its ID.
- `PUT /api/product/<int:pk>/`: Update a product.
- `DELETE /api/product/<int:pk>/`: Delete a product.

### Cart

- `GET /api/cart/`: Get the items in the current user's cart.
- `POST /api/cart/`: Add an item to the cart.
- `PUT /api/cart/<int:pk>/`: Update the quantity of an item in the cart.
- `DELETE /api/cart/<int:pk>/`: Remove an item from the cart.

### Orders

- `GET /api/order/`: Get a list of the current user's orders.
- `POST /api/order/`: Create a new order from the items in the cart.
- `GET /api/order/<int:pk>/`: Get a single order by its ID.

## Technologies Used

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT for Django REST Framework](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) for API documentation
- [SQLite](https://www.sqlite.org/index.html)

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Lftobs/E-commerce.git
    cd E-commerce
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/api/`.

## API Documentation

API documentation is available at the following endpoints:

-   **Swagger UI:** `http://127.0.0.1:8000/api/schema/docs/`
-   **ReDoc:** `http://127.0.0.1:8000/api/schema/redoc/`
