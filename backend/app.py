from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # enables frontend

@app.route('/api/health', methods=['GET'])
def health_check():
    '''
    Checks the health endpoint of the app, specifically
    responding with a JSON response saying status is "ok"
    '''
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True) # runs the flask app in debug mode