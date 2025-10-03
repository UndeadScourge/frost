from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Flask backend is running"})

# Task 2: GET request interface
@app.route('/api/get_message', methods=['GET'])
def get_message():
    # Get parameter from URL
    param = request.args.get('param', '')
    return jsonify({
        "message": f"Parameter is {param}",
        "received_param": param
    })

# Task 3: POST request interface
@app.route('/api/post_message', methods=['POST'])
def post_message():
    # Get parameter from URL
    url_param = request.args.get('param', '')
    
    # Get parameter from request body
    if request.is_json:
        body_data = request.get_json()
        body_param = body_data.get('bodyParam', '')
    else:
        body_param = ''
    
    return jsonify({
        "message": f"Body parameter is {body_param}, URL parameter is {url_param}",
        "received_body_param": body_param,
        "received_url_param": url_param
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)