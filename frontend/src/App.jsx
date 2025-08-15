import React, { useState, useEffect } from 'react';
import useWebSocket from './hooks/useWebSocket';
import SellerTable from './components/SellerTable';
import BuyerTable from './components/BuyerTable';
import PriceChart from './components/PriceChart';
import TopSellersChart from './components/TopSellersChart';
import SupplyDemandChart from './components/SupplyDemandChart';

export default function App() {
  const { marketData, isConnected } = useWebSocket("ws://localhost:8000/ws");
  const [priceChartData, setPriceChartData] = useState({ labels: [], prices: [] });
  const [supplyDemandData, setSupplyDemandData] = useState({ labels: [], supply: [], demand: [] });

  useEffect(() => {
    if (marketData) {
      // Update Price Chart Data
      if (marketData.transactions?.length > 0) {
        const avgPrice = marketData.transactions.reduce((acc, t) => acc + t.price_per_unit, 0) / marketData.transactions.length;
        setPriceChartData(prevData => {
          const newLabels = [...prevData.labels, `Tick ${marketData.tick}`].slice(-50); // Keep last 50
          const newPrices = [...prevData.prices, avgPrice].slice(-50);
          return { labels: newLabels, prices: newPrices };
        });
      }

      // Update Supply vs. Demand Chart Data
      const totalSupply = marketData.sellers.reduce((sum, s) => sum + s.inventory, 0);
      const totalDemand = marketData.buyers.reduce((sum, b) => sum + b.demand, 0);
      setSupplyDemandData(prevData => {
        const newLabels = [...prevData.labels, `Tick ${marketData.tick}`].slice(-50);
        const newSupply = [...prevData.supply, totalSupply].slice(-50);
        const newDemand = [...prevData.demand, totalDemand].slice(-50);
        return { labels: newLabels, supply: newSupply, demand: newDemand };
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
      
      <main className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-2">
          <PriceChart chartData={priceChartData} />
        </div>
        <div className="lg:col-span-2">
          <SupplyDemandChart chartData={supplyDemandData} />
        </div>
        <div className="lg:col-span-2">
          <SellerTable sellers={marketData.sellers} />
        </div>
        <div className="lg:col-span-2">
          <BuyerTable buyers={marketData.buyers} />
        </div>
        <div className="lg:col-span-4">
          <TopSellersChart sellers={marketData.sellers} />
        </div>
      </main>
    </div>
  );
}