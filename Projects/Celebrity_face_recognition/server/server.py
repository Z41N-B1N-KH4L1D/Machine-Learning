from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/classify_image', methods=['POST', 'OPTIONS'])
def classify_image():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        image_base64 = request.form.get('image_base64')
        if not image_base64:
            return jsonify({'error': 'Missing image_base64'}), 400
        
        file_path = request.form.get('file_path', None)
        result = util.classify_image(image_base64, file_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    util.load_saved_artifacts()
    app.run(debug=False, host='127.0.0.1', port=5000)