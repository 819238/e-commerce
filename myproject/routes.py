from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, jsonify, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, Product
from werkzeug.utils import secure_filename
import os

routes = Blueprint('routes', __name__)

# Existing routes

@routes.route('/')
def home():
    products = Product.query.all()
    cart_count = sum(item['quantity'] for item in session.get('cart', {}).values())
    return render_template('page.html', products=products, cart_count=cart_count)

@routes.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    products = []
    if query:
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    
    cart_count = sum(item['quantity'] for item in session.get('cart', {}).values())
    return render_template('search_results.html', query=query, products=products, cart_count=cart_count)

@routes.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    cart_count = sum(item['quantity'] for item in session.get('cart', {}).values())
    return render_template('product_detail.html', product=product, cart_count=cart_count)

@routes.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        
        if 'img' in request.files:
            file = request.files['img']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
                file.save(file_path)
            else:
                filename = 'default.jpg'
        else:
            filename = 'default.jpg'

        new_product = Product(name=name, price=price, description=description, img=filename)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('routes.pages'))

    return render_template('add_product.html')

@routes.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    if product_id:
        cart = session.get('cart', {})
        product_id = str(product_id)  # Ensure product_id is a string
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {'quantity': 1}
        session['cart'] = cart
        cart_count = sum(item['quantity'] for item in cart.values())
        return jsonify({'success': True, 'cart_count': cart_count})
    
    return jsonify({'success': False, 'message': 'Product ID is required.'}), 400

@routes.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    items = []
    total = 0
    for item_id, item in cart_items.items():
        product = Product.query.get(int(item_id))
        if product:
            item_total = item['quantity'] * product.price
            items.append({
                'id': product.id,
                'name': product.name,
                'quantity': item['quantity'],
                'price': product.price,
                'total': item_total
            })
            total += item_total
    cart_count = sum(item['quantity'] for item in cart_items.values())
    return render_template('cart.html', cart_items=items, total=total, cart_count=cart_count)

@routes.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    product_id = str(request.json.get('product_id'))
    action = request.json.get('action')

    if product_id in cart:
        if action == 'increase':
            cart[product_id]['quantity'] += 1
        elif action == 'decrease':
            cart[product_id]['quantity'] -= 1
            if cart[product_id]['quantity'] <= 0:
                del cart[product_id]
    
    session['cart'] = cart
    cart_count = sum(item['quantity'] for item in cart.values())
    return jsonify({'success': True, 'cart_count': cart_count})

@routes.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        flash('Item removed from cart.', 'success')
    return redirect(url_for('routes.cart'))

# New authentication routes

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('routes.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('routes.login'))
    
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

@routes.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('routes.admin_dashboard'))
    return render_template('user_dashboard.html')

@routes.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('routes.dashboard'))
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

# New admin routes

@routes.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('routes.dashboard'))

    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.description = request.form['description']
        
        if 'img' in request.files:
            file = request.files['img']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
                file.save(file_path)
                product.img = filename

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('routes.admin_dashboard'))

    return render_template('edit_product.html', product=product)

@routes.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('routes.dashboard'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('routes.admin_dashboard'))