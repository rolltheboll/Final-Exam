from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

#------CLASSES--------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    borrowed_books = db.relationship('Borrow', backref='user')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    borrows = db.relationship('Borrow', backref='book')

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author')

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime)
#------------CRUD--------------------------------------------------------

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added", "id": new_user.id}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{ "id": u.id, "name": u.name, "email": u.email } for u in users]), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
     return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 204


@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author_id=data['author_id'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added", "id": new_book.id}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{ "id": b.id, "title": b.title, "author_id": b.author_id } for b in books]), 200


@app.route('/authors', methods=['POST'])
def add_author():
    data = request.get_json()
    new_author = Author(name=data['name'])
    db.session.add(new_author)
    db.session.commit()
    return jsonify({"message": "Author added", "id": new_author.id}), 201

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify([{ "id": a.id, "name": a.name } for a in authors]), 200


@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    new_borrow = Borrow(user_id=data['user_id'], book_id=data['book_id'])
    db.session.add(new_borrow)
    db.session.commit()
    return jsonify({"message": "Book borrowed", "id": new_borrow.id}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
