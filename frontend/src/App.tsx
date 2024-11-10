import { useEffect, useState } from 'react';

// Function to call sample endpoint and log request
async function callSampleEndpoint() {
    try {
        // Call the sample endpoint
        const response = await fetch('http://localhost:4001/api/sample', {
            method: 'GET',
        });
        
        // Request data is automatically logged by @main.before_request in backend
        
        // Return the response data
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Function to get traffic data
async function getTrafficData() {
    try {
        const response = await fetch('http://localhost:4001/api/traffic', {
            method: 'GET'
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Function to check API health
async function checkHealth() {
    try {
        const response = await fetch('http://localhost:4001/api/health', {
            method: 'GET'
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error); 
        throw error;
    }
}

export default function App() {
    const [traffic, setTraffic] = useState<any[]>([]);

    useEffect(() => {
        // Get initial traffic data
        getTrafficData().then(data => setTraffic(data.requests || []));
        
        // Make sample request
        callSampleEndpoint();
        
        // Check health
        checkHealth();
    }, []);

    return (
        <div className="w-full h-full p-8">
            <h1>Traffic Status</h1>
            <button onClick={callSampleEndpoint}>Make Sample Request</button>
            
            <div className="mt-4">
                {traffic.map((request, index) => (
                    <div key={index} className="mb-2">
                        <p>IP: {request.ip}</p>
                        <p>Time: {request.timestamp}</p>
                        <p>Endpoint: {request.endpoint}</p>
                        <p>Status: {request.statusCode}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}