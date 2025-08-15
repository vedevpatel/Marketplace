import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function PriceChart({ chartData }) {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Average Transaction Price Over Time',
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      }
    }
  };

  const data = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Average Price',
        data: chartData.prices,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
    ],
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md col-span-2 h-96">
      <Line options={options} data={data} />
    </div>
  );
}