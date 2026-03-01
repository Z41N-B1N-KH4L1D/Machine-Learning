from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import util
import os

app = Flask(__name__, static_folder="../client", static_url_path="")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.join(BASE_DIR, "..", "client")

@app.route("/")
def home():
    return send_from_directory(CLIENT_DIR, "app.html")

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(CLIENT_DIR, filename)

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations' : util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_society_names')
def get_society_names():
    response = jsonify({
        'societies' : util.get_society_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_area_type_names')
def get_area_type_names():
    response = jsonify({
        'area_types' : util.get_area_type_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict_price():
    try:
        data = request.get_json(silent=True)
        if data is None:
            data = request.form
        
        total_sqft = float(data.get('total_sqft'))
        location = data.get('location')
        bhk = int(data.get('bhk'))
        bath = int(data.get('bath'))
        society = data.get('society')
        area_type = data.get('area_type')
        balcony = int(data.get('balcony'))
        
        estimated_price = util.get_estimated_price(location, society, area_type, total_sqft, bath, balcony, bhk)
        
        response = jsonify({
            'estimated_price': estimated_price
        })

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(f"Error in prediction: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error':str(e)}), 400

if __name__ == '__main__':
    util.load_saved_artifacts()
    app.run()