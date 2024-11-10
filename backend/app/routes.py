from flask import Blueprint, jsonify, request
from flask_cors import CORS
from datetime import datetime

main = Blueprint('main',__name__)

'''Dictionary to store traffic analytics data:
- requests: List of timestamp strings for all requests
- endpoints: Dict mapping endpoint paths to request counts
- details: List of request information including status codes'''
traffic_data = {
    "requests": [],
}

@main.before_request
def log_request():
    '''
    Logs traffic data before each request including IP, timestamp, endpoint, and status
    '''
    request_data = {
        "ip": request.remote_addr,
        "timestamp": datetime.now().isoformat(),
        "endpoint": request.path,
        "method": request.method,
        "statusCode": 200,  # Default success code
        "success": True     # Default success state
    }
    traffic_data["requests"].append(request_data)

@main.route('/api/sample', methods=["GET"])
def sample_endpoint():
    '''
    Initial endpoint that receives GET requests from frontend
    Returns: Basic response to confirm functionality
    '''
    return jsonify({"message": "Sample response", "status": "success"})

@main.route('/api/traffic', methods=['GET'])
def get_traffic():
    '''
    Returns traffic analytics with IP, timestamp, endpoint, status code and success
    '''
    return jsonify(traffic_data)

@main.route('/api/health', methods=['GET'])
def health_check():
    '''
    Health check endpoint.
    Returns: JSON indicating API is functioning.
    '''
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    main.run(debug=True) # runs the flask app in debug mode