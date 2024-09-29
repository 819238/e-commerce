from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    # Relasi satu-ke-banyak (satu produk bisa ada di banyak keranjang)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    # Hubungkan ke produk dengan menggunakan foreign key

    def __repr__(self):
        return f'<CartItem {self.product.name}, Quantity {self.quantity}>'
