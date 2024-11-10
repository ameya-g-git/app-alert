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
    "endpoints": {},
    "details": []
}

@main.before_request
def log_request():
    '''
    Logs traffic data before each request, as it captures a timestamp, 
    records the request path, and updates the endpoint counter.
    '''
    current_time = datetime.now().isoformat()
    path = request.path 
    traffic_data['requests'].append(current_time)
    traffic_data['endpoints'][path] = traffic_data['endpoints'].get(path, 0) + 1

@main.route('/api/sample', methods=["GET"])
def sample_endpoint():
    '''
    Initial endpoint that receives GET requests from frontend
    Returns: Basic response to confirm functionality
    '''
    return jsonify({"message": "Sample response", "status": "success"})

@main.route('/api/log', methods=['POST'])
def log_request_details():
    '''
    Receives detailed request information from frontend
    Payload expected:
    {
        "endpoint": str,    # The endpoint that was called
        "statusCode": int,  # HTTP status code
        "success": bool     # Whether request was successful
    }
    '''
    request_info = request.get_json()
    traffic_data['details'].append({
        'timestamp': datetime.now().isoformat(),
        'endpoint': request_info.get('endpoint'),
        'statusCode': request_info.get('statusCode'),
        'success': request_info.get('success')
    })
    return jsonify({"status": "logged"})

@main.route('/api/traffic', methods=['GET'])
def get_traffic():
    '''
    Endpoint to retrieve traffic analytics data.
    Returns: JSON containing requests list, endpoint counters, and details.
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