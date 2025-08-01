from flask import Blueprint, request, jsonify
from models.book import Book
from db import db
from utils.auth import login_required
from datetime import datetime

book_bp = Blueprint('book', __name__)

@book_bp.route('/books', methods=['POST'])
@login_required
def add_book():
    user_id = request.user_id
    data = request.get_json()

    title = data.get('title')
    author = data.get('author')
    status = data.get('status')
    memo = data.get('memo', '')
    rating = data.get('rating')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    if not title or not status:
        return jsonify({"error": "title과 status는 필수입니다."}), 400

    new_book = Book(
        title=title,
        author=author,
        status=status,
        memo=memo,
        rating=rating,
        start_date=start_date,
        end_date=end_date,
        created_by=user_id,
        created_at=datetime.utcnow()
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': '책이 성공적으로 등록되었습니다'}), 201

@book_bp.route('/books', methods=['GET'])
@login_required
def get_books():
    books = Book.query.filter_by(created_by=request.user_id).order_by(Book.created_at.desc()).all()

    result = []
    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "status": book.status,
            "memo": book.memo,
            "rating": book.rating,
            "start_date": book.start_date.isoformat() if book.start_date else None,
            "end_date": book.end_date.isoformat() if book.end_date else None,
            "created_at": book.created_at.isoformat()
        })

    return jsonify(result), 200