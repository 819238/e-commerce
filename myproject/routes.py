from flask import Blueprint, render_template, request, redirect, url_for
from .utils import validate_product_data

routes = Blueprint('routes', __name__)

@routes.route('/')
def pages():
    products = [
        {'id': 1, 'name': 'Mie Ayam', 'price': 20000, 'img': 'images/product1.jpg'},
        {'id': 2, 'name': 'Mie Ayam Pangsit', 'price': 22000, 'img': 'images/product2.jpg'},
        {'id': 3, 'name': 'Bakso', 'price': 20000, 'img': 'images/product3.jpg'},
    ]
    return render_template('page.html', products=products)

@routes.route('/search')
def search():
    query = request.args.get('q', '')
    products = [
        {'id': 1, 'name': 'Mie Ayam', 'price': 20000, 'img': 'images/product1.jpg'},
        {'id': 2, 'name': 'Mie Ayam Pangsit', 'price': 22000, 'img': 'images/product2.jpg'},
        {'id': 3, 'name': 'Bakso', 'price': 20000, 'img': 'images/product3.jpg'},
    ]
    filtered_products = [p for p in products if query.lower() in p['name'].lower()]
    return render_template('search_results.html', products=filtered_products, query=query)

@routes.route('/product/<int:product_id>')
def product_detail(product_id):
    products = [
        {'id': 1, 'name': 'Mie Ayam', 'price': 20000, 'description': 'p', 'specification': 'asas', 'img': 'images/product1.jpg'},
        {'id': 2, 'name': 'Mie Ayam Pangsit', 'price': 22000, 'description': 'p.', 'specification': 'p', 'img': 'images/product2.jpg'},
        {'id': 3, 'name': 'Bakso', 'price': 20000, 'description': 'p', 'specification': 'p', 'img': 'images/product3.jpg'},
    ]
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return "Product not found", 404
    return render_template('product_detail.html', product=product)

@routes.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        data = request.form
        errors = validate_product_data(data)
        if errors:
            return render_template('add_product.html', errors=errors)
        # Logic to handle product addition, e.g., saving to database
        return redirect(url_for('routes.pages'))
    return render_template('add_product.html', errors=None)
