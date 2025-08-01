from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from models.user import User
from db import db
from utils.jwt_helper import generate_token
from utils.auth import login_required

auth_bp = Blueprint('auth_bp', __name__)

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

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    user_id = request.user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': '사용자를 찾을 수 없습니다'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    # JWT 서버에서 토큰 직접 삭제 못함 - 프론트에서 삭제
    return jsonify({'message': '로그아웃되었습니다. 토큰을 삭제해주세요'}), 200


#테스트용
test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/protected')
@login_required
def protected_route():
    return jsonify({'message': 'This is a protected route!', 'user_id': request.user_id})