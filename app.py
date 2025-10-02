from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask Backend!"})

@app.route('/api/test')
def test_api():
    return jsonify({
        "status": "success",
        "message": "Frontend and backend are connected!",
        "data": {"number": 42, "text": "Hello World"}
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
