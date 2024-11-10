import clsx from "clsx";

interface ThreatProps {
    threat: string;
    message: string;
    timestamp: string;
}

export default function Threat({ threat, message, timestamp }: ThreatProps) {
    const threatClasses = clsx({
        "h-12 flex flex-row justify-between": true,
        "bg-red-200": threat === "red",
        "bg-yellow-200": threat === "yellow",
        "bg-green-200": threat === "green",
    });

    return (
        <div className={threatClasses}>
            <span>{message}</span>
            <span>{timestamp}</span>
        </div>
    );
}
