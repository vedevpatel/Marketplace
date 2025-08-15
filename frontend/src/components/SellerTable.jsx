import React from 'react';

export default function SellerTable({ sellers }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-2">Sellers</h2>
      <div className="overflow-y-auto h-64">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b">
              <th className="py-2 px-4 bg-gray-100">ID</th>
              <th className="py-2 px-4 bg-gray-100">Price</th>
              <th className="py-2 px-4 bg-gray-100">Inventory</th>
              <th className="py-2 px-4 bg-gray-100">Revenue</th>
            </tr>
          </thead>
          <tbody>
            {sellers?.map((seller) => (
              <tr key={seller.id} className="border-t">
                <td className="py-2 px-4">{seller.id}</td>
                <td className="py-2 px-4">${seller.price.toFixed(2)}</td>
                <td className="py-2 px-4">{seller.inventory}</td>
                <td className="py-2 px-4">${seller.revenue.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}