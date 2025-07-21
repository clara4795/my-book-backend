from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from models.user import User
from db import db
from utils.jwt_helper import generate_token

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

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': '모든 필드를 입력해주세요'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': '이메일 또는 비밀번호가 올바르지 않습니다'}), 401

    token = generate_token(user.id)
    return jsonify({'token': token}), 200
