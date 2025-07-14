from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ping")
def ping():
    return {"message": "pong!"}

if __name__ == "__main__":
    app.run(debug=True)
