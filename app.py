from flask import Flask
from db import db
from models import User, Book
from routes.auth import auth_bp
from routes.auth import test_bp 
from routes.books import book_bp
import os
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybooks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(test_bp)
app.register_blueprint(book_bp)


@app.route('/')
def home():
    return "Hello, Flask + DB"

# 테이블 만들기 위한 코드
with app.app_context():
    db.create_all()

# 테스트 유저 1명 추가
with app.app_context():
    if not User.query.filter_by(username='testuser').first():
        test_user = User(
            username="testuser",
            email="test@example.com",
            password="hashedpassword123"
        )
        db.session.add(test_user)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)