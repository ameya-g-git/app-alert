// Function to call sample endpoint and log request
// async function callSampleEndpoint() {
//     try {
//         // Call the sample endpoint
//         const response = await fetch("http://localhost:4001/api/sample", {
//             method: "GET",
//         });

import { useEffect, useState } from "react";
import Chart from "react-google-charts";
import Threat from "./components/Threat";
import Request from "./components/Request";

//         // Request data is automatically logged by @main.before_request in backend

//         // Return the response data
//         const data = await response.json();
//         return data;
//     } catch (error) {
//         console.error("Error:", error);
//         throw error;
//     }
// }

// // Function to get traffic data
// async function getTrafficData() {
//     try {
//         const response = await fetch("http://localhost:4001/api/traffic", {
//             method: "GET",
//         });
//         const data = await response.json();
//         return data;
//     } catch (error) {
//         console.error("Error:", error);
//         throw error;
//     }
// }

// // Function to check API health
// async function checkHealth() {
//     try {
//         const response = await fetch("http://localhost:4001/api/health", {
//             method: "GET",
//         });
//         const data = await response.json();
//         return data;
//     } catch (error) {
//         console.error("Error:", error);
//         throw error;
//     }
// }

type Threat = [time: string, threat: string, message: string];

export interface RequestData {
    ip: string;
    timestamp: string;
    endpoint: string;
    method: string;
    statusCode: number;
    success: boolean;
}

export default function App() {
    const [graphData, setGraphData] = useState<(string | number)[][]>([
        ["", 2],
    ]);
    const [threatData, setThreatData] = useState<Threat[]>([]);
    const [requestData, setRequestData] = useState<RequestData[]>([]);

    useEffect(() => {
        async function getGraphData() {
            try {
                const response = await fetch("/api/graph");
                if (!response.ok) {
                    throw new Error(`Response Status: ${response.status}`);
                }
                const json: number[][] = await response.json();
                const jsonFiltered = json.map((xy: number[], i) => [
                    i * 5,
                    xy[1],
                ]);

                setGraphData(jsonFiltered);
            } catch (e) {
                console.error(e);
            }
        }

        async function getThreatData() {
            try {
                const response = await fetch("/api/threat");
                if (!response.ok) {
                    throw new Error(`Response Status: ${response.status}`);
                }
                const json: Threat[] = await response.json();
                console.log(threatData);
                setThreatData(json);
            } catch (e) {
                console.error(e);
            }
        }

        async function getRequestData() {
            try {
                const response = await fetch("/api/traffic");
                if (!response.ok) {
                    throw new Error(`Response Status: ${response.status}`);
                }
                const json: RequestData[] = await response.json();
                console.log(json);
                setRequestData(json.requests);
            } catch (e) {
                console.error(e);
            }
        }

        async function getData() {
            getGraphData();
            getThreatData();
            getRequestData();
        }

        const timer1 = setTimeout(getData, 5000);

        return () => {
            clearTimeout(timer1);
        };
    }, [graphData, threatData]);

    return (
        <div className="w-screen h-screen p-8 overflow-hidden">
            <h1>Status</h1>
            <div className="flex flex-col w-full h-full gap-4">
                <div className="flex flex-row w-full gap-4 h-[55%]">
                    <div className="w-1/2 h-full">
                        <Chart
                            chartType="Line"
                            data={[["Time", "Requests / 5s"], ...graphData]}
                            options={{
                                title: "Traffic",
                                hAxis: { title: "Time" },
                                vAxis: { title: "Requests / 5s" },
                                legend: { position: "none" },
                            }}
                            width="100%"
                            height="100%"
                        />
                    </div>
                    <div className="flex flex-col w-1/2 h-full gap-1 overflow-y-scroll">
                        {threatData.length != 0 &&
                            threatData.map(([time, threat, message]) => {
                                return (
                                    <Threat
                                        message={message}
                                        threat={threat}
                                        timestamp={time}
                                    />
                                );
                            })}
                    </div>
                </div>
                <div className="flex flex-row w-full gap-4 h-[35%]">
                    <div className="flex flex-col w-1/3 h-full gap-1">
                        {requestData.map((req) => (
                            <Request requestData={req} />
                        ))}
                    </div>
                    <div className="flex items-center justify-center w-1/3 h-full bg-red-300 ">
                        map showing request traffic geographically
                    </div>
                    <div className="flex items-center justify-center w-1/3 h-full bg-red-300">
                        tracking of computer resources by the API
                    </div>
                </div>
            </div>
        </div>
    );
}
