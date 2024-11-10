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
threat_data = []

@main.before_request
def log_request():
    '''
    Logs traffic data before each request including IP, timestamp, endpoint, and status
    '''

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
   

@main.route('/traffic', methods=['POST'])
def get_request():
    data = request.json
    
    request_data = {
        "ip": data["ip"],
        "timestamp": datetime.now().isoformat(),
        "endpoint": data["endpoint"],
        "method": data["method"],
        "statusCode": 200,  # Default success code
        "success": True     # Default success state
    }
    traffic_data["requests"].append(request_data)
    update_last_five_sec_data()

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
    else:
        graph_data.append(["eoijrg", 0])
    
    
    last_five_sec_data.clear()  # Clear the last five seconds data
    return jsonify(graph_data)

@main.route('/threat', methods=['GET'])
def get_threat():
    '''
    Returns the threat level based on:
        - Red: if traffic exceeds > 100 requests in the last 5 seconds
        - Yellow: find outlier in traffic data using IQR
        - Green: server status is normal
    '''
    current_time = datetime.now().isoformat()
    current_threat = "green"

    if len(graph_data) >= 4:
        # Calculate IQR to detect outliers in traffic data
        data = [point[1] for point in graph_data]
        data.sort()
        q1 = data[int(len(data)*0.25)]
        q3 = data[int(len(data)*0.75)]
        iqr = q3 - q1
        upper_bound = q3 + 1.5*iqr

        # Check if the last data point is an outlier or exceeds 100 requests
        if graph_data[-1][1] > upper_bound:
            current_threat = "yellow"
        elif graph_data[-1][1] > 100:
            current_threat = "red"

    threat_data.append([current_time, current_threat])

    return jsonify({"threat": current_threat})

if __name__ == '__main__':
    main.run(debug=True) # runs the flask app in debug mode