from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

Base = declarative_base()

# Database setup
DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

# Define Product class
class Product(Base):
    __tablename__ = 'PrDATA'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(Float)
    count = Column(Integer)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    products = db_session.query(Product).all()
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    product = db_session.query(Product).filter_by(product_id=product_id).first()
    
    if not product or product.count < quantity:
        return redirect(url_for('index'))
    
    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {'name': product.product_name, 'price': product.price, 'quantity': quantity}
    
    session['cart'] = cart
    product.count -= quantity
    db_session.commit()
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)

# HTML Templates

# index.html
index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Shop</title>
</head>
<body>
    <h1>Available Products</h1>
    <ul>
        {% for product in products %}
        <li>
            {{ product.product_name }} - ${{ product.price }}
            <form action="/add_to_cart" method="post">
                <input type="hidden" name="product_id" value="{{ product.product_id }}">
                <input type="number" name="quantity" value="1" min="1">
                <button type="submit">Add to Cart</button>
            </form>
        </li>
        {% endfor %}
    </ul>
    <a href="/cart">View Cart</a>
</body>
</html>
"""

# cart.html
cart_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Cart</title>
</head>
<body>
    <h1>Your Cart</h1>
    <ul>
        {% for key, item in cart.items() %}
        <li>{{ item.name }} - ${{ item.price }} x {{ item.quantity }}</li>
        {% endfor %}
    </ul>
    <p>Total: ${{ total }}</p>
    <a href="/checkout">Checkout</a>
    <a href="/">Continue Shopping</a>
</body>
</html>
"""

# checkout.html
checkout_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Checkout</title>
</head>
<body>
    <h1>Thank you for your purchase!</h1>
    <a href="/">Back to Home</a>
</body>
</html>
"""

# from sqlalchemy import create_engine, Column, String, Integer, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Create a base class for ORM classes
# Base = declarative_base()

# # Define Product class (mapping to the "PrDATA" table)
# class Product(Base):
#     __tablename__ = 'PrDATA'
#     product_id = Column(Integer, primary_key=True)
#     product_name = Column(String)
#     price = Column(Float)
#     count = Column(Integer)

# # Database connection setup using SQLAlchemy
# DATABASE_URL = "sqlite:///test.db"
# engine = create_engine(DATABASE_URL, echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()

# # Sample product list (to be used as initial data if needed)
# products = {
#     "1": {"product": "Apple", "price": 0.5, "count": 50},
#     "2": {"product": "Banana", "price": 0.3, "count": 200},
#     "3": {"product": "Orange", "price": 0.7, "count": 100},
#     "4": {"product": "Bread", "price": 1.0, "count": 30},
# }

# # Cart to hold selected products
# cart = {}

# def initialize_db():
#     # Create the table in the database (if not exists)
#     Base.metadata.create_all(engine)

#     # Insert sample products if the table is empty
#     if session.query(Product).count() == 0:
#         for product_id, product_info in products.items():
#             product = Product(product_id=int(product_id), product_name=product_info["product"], 
#                               price=product_info["price"], count=product_info["count"])
#             session.add(product)
#         session.commit()

# def display_products():
#     print("\nAvailable Products:")
#     all_products = session.query(Product).all()
#     for product in all_products:
#         print(f"{product.product_id}. \t{product.product_name} - \t${product.price} - \t{product.count}")
    
# def add_to_cart(product_id, quantity):
#     product = session.query(Product).filter_by(product_id=product_id).first()
#     if product:
#         if product.count >= quantity:
#             if product_id in cart:
#                 cart[product_id]['quantity'] += quantity
#             else:
#                 cart[product_id] = {'product': product.product_name, 'price': product.price, 'quantity': quantity}
#             product.count -= quantity
#             session.commit()
#             print(f"Added {quantity} x {product.product_name} to cart.")
#         else:
#             print(f"Not enough {product.product_name} in stock.")
#     else:
#         print("Invalid product ID.")

# def view_cart():
#     if not cart:
#         print("Your cart is empty.")
#         return
#     print("\nYour Cart:")
#     total = 0
#     for item in cart.values():
#         item_total = item['price'] * item['quantity']
#         total += item_total
#         print(f"{item['product']} - ${item['price']:.2f} x {item['quantity']} = ${item_total:.2f}")
#     print(f"Total: ${total:.2f}")

# def checkout():
#     if not cart:
#         print("Your cart is empty. Please add items before checking out.")
#         return
#     total = sum(item['price'] * item['quantity'] for item in cart.values())
#     print(f"\nCheckout complete! Your total is: ${total:.2f}")
#     cart.clear()  # Clear the cart after checkout

# def main():
#     initialize_db()  # Set up the database and load initial data

#     while True:
#         print("\nWelcome to the Shop!")
#         print("1. View Products")
#         print("2. Add to Cart")
#         print("3. View Cart")
#         print("4. Checkout")
#         print("5. Exit")
        
#         choice = input("Please choose an option (1-5): ")
        
#         if choice == '1':
#             display_products()
#         elif choice == '2':
#             product_id = int(input("Enter the product ID to add to cart: "))
#             quantity = int(input("Enter the quantity: "))
#             add_to_cart(product_id, quantity)
#         elif choice == '3':
#             view_cart()
#         elif choice == '4':
#             checkout()
#         elif choice == '5':
#             print("Thank you for visiting the shop!")
#             break
#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "__main__":
#     main()

