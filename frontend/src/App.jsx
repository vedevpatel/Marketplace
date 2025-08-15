import React, { useState, useEffect } from 'react';
import useWebSocket from './hooks/useWebSocket';
import SellerTable from './components/SellerTable';
import BuyerTable from './components/BuyerTable';
import OrderBook from './components/OrderBook';
import PriceChart from './components/PriceChart';

export default function App() {
  const { marketData, isConnected } = useWebSocket("ws://localhost:8000/ws");
  const [chartData, setChartData] = useState({ labels: [], prices: [] });

  useEffect(() => {
    if (marketData?.transactions?.length > 0) {
      const avgPrice = marketData.transactions.reduce((acc, t) => acc + t.price_per_unit, 0) / marketData.transactions.length;
      
      setChartData(prevData => {
        const newLabels = [...prevData.labels, `Tick ${marketData.tick}`];
        const newPrices = [...prevData.prices, avgPrice];
        
        // Keep the chart from getting too crowded by showing the last 50 ticks
        if (newLabels.length > 50) {
          newLabels.shift();
          newPrices.shift();
        }

        return { labels: newLabels, prices: newPrices };
      });
    }
  }, [marketData]);

  if (!isConnected || !marketData) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-2xl font-semibold animate-pulse">Connecting to market...</div>
      </div>
    );
  }

  return (
    <div className="bg-gray-100 min-h-screen p-4 sm:p-8">
      <header className="mb-8">
        <h1 className="text-3xl sm:text-4xl font-bold text-center text-gray-800">Marketplace Dashboard</h1>
        <p className="text-center text-lg text-gray-600">Tick: {marketData.tick}</p>
      </header>
      <main className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <PriceChart chartData={chartData} />
        <OrderBook offers={marketData.offers} requests={marketData.requests} />
        <SellerTable sellers={marketData.sellers} />
        <BuyerTable buyers={marketData.buyers} />
      </main>
    </div>
  );
}
