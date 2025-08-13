import { useEffect, useState } from "react";

export default function useWebSocket(url) {
    const [data, setData] = useState(null);

    useEffect(() => {
        const ws = new WebSocket (url); // creating connection

        // Event handler for incoming messages
        ws.onmessage = (event) => {
            setData(JSON.parse(event.data)); // parse & update state
        };

        // Event handler for connection closure
        ws.onclose = () => {
            console.log("WebSocket closed");
        };

        // Cleanup func. to close connection on unmount
        return () => ws.close();
    }, [url]);

    return data;
}