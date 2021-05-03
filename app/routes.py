from flask import Blueprint
from app import db
from app.models.book import Book
from flask import request, Blueprint, make_response, jsonify

hello_world_bp = Blueprint("hello_world", __name__)

# @hello_world_bp.route('/hello-world', methods=["GET"])
# def get_hello_world():
#     my_response = "Hello, World!"
#     return my_response

# @hello_world_bp.route('/hello-world/JSON', methods=["GET"])
# def hello_world_json():
#     return {
#         "name": "Crintion!",
#         "message": "Heya!",
#         "hobbies": ["Coding, loving Fissick"]
#     }, 201

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body

books_bp = Blueprint('books', __name__, url_prefix='/books')
@books_bp.route('', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'GET':
        books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append({
                'id': book.id,
                'title': book.title,
                'description': book.description
            })
        return jsonify(books_response)
    elif request.method == 'POST':
        request_body = request.get_json()
        new_book = Book(title=request_body['title'],
                        description=request_body['description'])
        db.session.add(new_book)
        db.session.commit()
        return make_response(f'Book {new_book.title} successfully created', 201)