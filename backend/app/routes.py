from flask import Blueprint, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

main = Blueprint('main',__name__)
request_list = []

# Dictionary to store traffic analytics data
traffic_data = {
    "requests": [],
}

graph_data = []
last_five_sec_data = []

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
    update_last_five_sec_data()

def update_last_five_sec_data():
    '''
    Updates the last five seconds of data with the number of requests
    '''
    now = datetime.now()
    five_seconds_ago = now - timedelta(seconds=5)
    
    # Filter requests in the last 5 seconds
    recent_requests = [req for req in traffic_data["requests"] if datetime.fromisoformat(req["timestamp"]) > five_seconds_ago]
    
    # Update last five seconds data
    last_five_sec_data.append([now.isoformat(), len(recent_requests)])
   

@main.route('/sample', methods=["GET"])
def sample_endpoint():
    '''
    Initial endpoint that receives GET requests from frontend
    Returns: Basic response to confirm functionality
    '''
    return jsonify(request_list)

@main.route('/api/sample', methods=['POST'])
def get_request():
    data = request.json

    request_list.append(data)

@main.route('/traffic', methods=['GET'])
def get_traffic():
    '''
    Returns traffic analytics with IP, timestamp, endpoint, status code and success
    '''
    return jsonify(traffic_data)

@main.route('/health', methods=['GET'])
def health_check():
    '''
    Health check endpoint.
    Returns: JSON indicating API is functioning.
    '''
    return jsonify({"status": "ok"})

@main.route('/graph', methods=['GET'])
def get_graph_data():
    '''
    Returns the graph data with the last five seconds of requests
    '''
    if last_five_sec_data:
        request_count = len(last_five_sec_data)
        timestamp = last_five_sec_data[-1][0] # gets the last timestamp
        graph_data.append([timestamp, request_count])
        last_five_sec_data.clear()  # Clear the last five seconds data
    return jsonify(graph_data)

if __name__ == '__main__':
    main.run(debug=True) # runs the flask app in debug mode