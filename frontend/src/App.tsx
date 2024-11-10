// Function to call sample endpoint and log request
// async function callSampleEndpoint() {
//     try {
//         // Call the sample endpoint
//         const response = await fetch("http://localhost:4001/api/sample", {
//             method: "GET",
//         });

import { useEffect, useState } from "react";
import Chart from "react-google-charts";

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

interface Threat {
    threat: string;
}

export default function App() {
    const [graphData, setGraphData] = useState<(string | number)[][]>([
        ["", 2],
    ]);
    const [threatData, setThreatData] = useState<Threat[]>([]);

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
                console.log(graphData);
            } catch (e) {
                console.error(e);
            }
        }

        async function getThreatData() {
            try {
                const response = await fetch("/api/threats");
                if (!response.ok) {
                    throw new Error(`Response Status: ${response.status}`);
                }
                const json: Threat[] = await response.json();
                setThreatData(json);
            } catch (e) {
                console.error(e);
            }
        }

        async function getData() {
            getGraphData();
            getThreatData();
        }

        const timer1 = setTimeout(getData, 5000);

        return () => {
            clearTimeout(timer1);
        };
    }, [graphData]);

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
                                legend: "none",
                            }}
                            width="100%"
                            height="100%"
                        />
                    </div>
                    <div className="flex flex-col w-1/2 h-full bg-black">
                        {threatData.map((threat) => {
                            return <h1>{threat.threat}</h1>;
                        })}
                    </div>
                </div>
                <div className="flex flex-row w-full gap-4 h-[35%]">
                    <div className="w-1/3 h-full bg-red-300">hi</div>
                    <div className="w-1/3 h-full bg-red-300">hi</div>
                    <div className="w-1/3 h-full bg-red-300">hi</div>
                </div>
            </div>
        </div>
    );
}
