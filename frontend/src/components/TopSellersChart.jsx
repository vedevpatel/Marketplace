import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function TopSellersChart({ sellers }) {
  const options = {
    indexAxis: 'y', // Makes the bar chart horizontal
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Top 5 Sellers by Revenue',
      },
    },
    scales: {
        x: {
            beginAtZero: true,
        }
    }
  };

  // Sort sellers by revenue, take the top 5, and reverse for a top-to-bottom chart
  const topSellers = sellers.sort((a, b) => b.revenue - a.revenue).slice(0, 5).reverse();
  
  const data = {
    labels: topSellers.map(s => `Seller ${s.id}`),
    datasets: [
      {
        label: 'Total Revenue',
        data: topSellers.map(s => s.revenue),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md h-96">
        <Bar options={options} data={data} />
    </div>
  );
}