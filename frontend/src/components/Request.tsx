import { RequestData } from "../App";

interface RequestProps {
    requestData: RequestData;
}

export default function Request({ requestData }: RequestProps) {
    return (
        <div className="flex flex-row bg-orange-300 min-h-16">
            <span className="font-bold">{`${requestData.method} /${requestData.endpoint} ${requestData.statusCode}`}</span>
            <span>{requestData.ip}</span>
            <span>{requestData.timestamp}</span>
        </div>
    );
}
