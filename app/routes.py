from flask import Blueprint
from app import db
from app.models.book import Book
from flask import request, Blueprint, make_response, jsonify

books_bp = Blueprint('books', __name__, url_prefix='/books')

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@books_bp.route("/<book_id>", methods=["GET"], strict_slashes=False)
def get_single_book(book_id):
    book = Book.query.get(book_id)
    #Try to find the book with the given id
    if not is_int(book_id):
        return {
            "message": f"ID {book_id} must be an integer",
            "success": False
        }, 400
    
    elif book:
        return book.to_json(), 200

    return {
        'message': f'Book with id {book_id} was not found',
        'success': False
    }, 404

@books_bp.route('', methods=['GET'], strict_slashes=False)
def books_index():
    books = Book.query.all()
    books_response = []
    for book in books:
        books_response.append(book.to_json() )

    return jsonify(books_response), 200

@books_bp.route('', methods=['POST'], strict_slashes=False)
def handle_books():
    request_body = request.get_json()
    new_book = Book(title=request_body['title'],
                        description=request_body['description'])
    db.session.add(new_book)
    db.session.commit()
    return {
        "success": True,
        "message": f'Book {new_book.title} has been created!!'
    }, 201

@books_bp.route("/<book_id>", methods=["GET", "PUT"])
def handle_book(book_id):
    book = Book.query.get(book_id)

    if request.method == "GET":
        # ... existing code that returned a dictionary
    elif request.method == "PUT":
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()

        return make_response(f"Book #{book.id} successfully updated")
         