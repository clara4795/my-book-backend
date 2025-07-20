from flask import Blueprint, request, jsonify
from models.user import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': '모든 필드를 입력해주세요'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': '이미 존재하는 아이디 또는 이메일입니다'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '회원가입이 완료되었습니다'}), 201
