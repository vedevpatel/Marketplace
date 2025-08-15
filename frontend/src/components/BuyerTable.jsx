import React from 'react';

export default function BuyerTable({ buyers }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-2">Buyers</h2>
      <div className="overflow-y-auto h-64">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b">
              <th className="py-2 px-4 bg-gray-100">ID</th>
              <th className="py-2 px-4 bg-gray-100">Budget</th>
              <th className="py-2 px-4 bg-gray-100">Demand</th>
              <th className="py-2 px-4 bg-gray-100">Inventory</th>
            </tr>
          </thead>
          <tbody>
            {buyers?.map((buyer) => (
              <tr key={buyer.id} className="border-t">
                <td className="py-2 px-4">{buyer.id}</td>
                <td className="py-2 px-4">${buyer.budget.toFixed(2)}</td>
                <td className="py-2 px-4">{buyer.demand}</td>
                <td className="py-2 px-4">{buyer.inventory}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}