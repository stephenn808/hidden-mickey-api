from flask import Flask, request, jsonify
from match_utils import match_mickey
from datetime import datetime

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    result = match_mickey(image_file)

    return jsonify({
        "version": "1.0",
        "match_percent": result["score"],
        "highlighted_image_url": result["image_url"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
