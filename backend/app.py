from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app) # enables frontend

'''
Dictionary to store traffic analytics data:
- requests: List of timestamp strings for all requests
- endpoints: Dict mapping endpoint paths to request counts

This should allow for:
    - frontend fetching
    - total request volume over time 
    - most accessed endpoints
    - traffic patterns 
'''
traffic_data = {
    "requests": [],
    "endpoints": {}
}

'''
Example Output:
traffic_data = {
    'requests': ['2024-03-20T14:30:25', '2024-03-20T14:31:00'],
    'endpoints': {
        '/api/health': 5,
        '/api/traffic': 2,
        '/api/other': 1
    }
}
'''

@app.before_request
def log_request():
    '''
    Logs traffic data before each request, as it captures a timestamp, 
    records the request path, and updates the endpoint counter.
    '''
    current_time = datetime.now().isoformat()
    path = request.path 
    traffic_data['requests'].append(current_time) # adds timestamp to list
    traffic_data['endpoints'][path] = traffic_data['endpoints'].get(path, 0) + 1 # adds counter

@app.route('/api/traffic', methods=['GET'])
def get_traffic():
    '''
    Endpoint to retrieve traffic analytics data.
    Returns: JSON containing requests list and endpoint counters.
    '''
    return jsonify(traffic_data)

@app.route('/api/health', methods=['GET'])
def health_check():
    '''
    Health check endpoint.
    Returns: JSON indicating API is functioning.
    '''
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True) # runs the flask app in debug mode