import React from 'react';
import { Line } from 'react-chartjs-2';

// ChartJS is already registered in PriceChart.jsx, so we don't need to do it again here.

export default function SupplyDemandChart({ chartData }) {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Total Supply vs. Demand',
      },
    },
     scales: {
      y: {
        beginAtZero: true,
      }
    }
  };

  const data = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Total Supply (Inventory)',
        data: chartData.supply,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Total Demand',
        data: chartData.demand,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md h-96">
        <Line options={options} data={data} />
    </div>
  );
}