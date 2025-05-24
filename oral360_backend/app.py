from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.process import run_detection

app = Flask(__name__)
CORS(app)  # Allow cross-origin from Flutter

@app.route('/')
def home():
    return jsonify({"message": "Oral360 YOLO backend running 🚀"})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        image_b64 = data.get("image")
        tooth = data.get("tooth")

        if not image_b64 or not tooth:
            return jsonify({"error": "Missing image or tooth"}), 400

        result = run_detection(image_b64, tooth)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # app.run(debug=True, port=5000)
    app.run(host="0.0.0.0", debug=True, port=5050)


