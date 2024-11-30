from datetime import datetime
from app import db


products_store = db.Table('products_store',
	db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
	db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
)


class Category(db.Model):
	__tablename__ = "categories"
	id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(100))
	active = db.Column(db.Boolean, default=True)
	# prods

	def __repr__(self):
		return f'<Category: {self.category_name}>'

class Store(db.Model):
	__tablename__ = "stores"
	id = db.Column(db.Integer, primary_key=True)
	store_name = db.Column(db.String(60))

	def __repr__(self):
		return f"<Store: {self.store_name}>"


class Product(db.Model):
	__tablename__ = "products"
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(50))
	description = db.Column(db.Text)
	create_date = db.Column(db.DateTime, default=datetime.now)
	# one to many relation
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	category = db.relationship('Category', backref=db.backref('products', lazy=True))
	# many to many relation
	stores = db.relationship('Store', secondary=products_store, backref=db.backref('products', lazy=True))

	def __repr__(self):
		return f"<User: {self.product_name}>"

