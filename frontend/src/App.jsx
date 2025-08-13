import React from "react";
import useWebSocket from "./hooks/useWebSocket";
import MarketTable from "./components/MarketTable";

export default function App() {
  const marketData = useWebSocket("ws://localhost:8000/ws");

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Marketplace Dashboard</h1>
      {marketData ? (
        <MarketTable data={marketData} />
      ) : (
        <p>Connecting to market...</p>
      )}
    </div>
  );
}
