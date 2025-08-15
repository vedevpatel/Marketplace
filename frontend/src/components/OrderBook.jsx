import React from 'react';

export default function OrderBook({ offers, requests }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md col-span-2">
      <h2 className="text-xl font-bold mb-2">Live Order Book (Current Tick)</h2>
      <div className="grid grid-cols-2 gap-4 h-48 overflow-y-auto">
        <div>
          <h3 className="font-semibold text-red-600 border-b pb-1">Asks (Sellers)</h3>
          <ul>
            {offers?.slice(0, 10).map((offer, index) => (
              <li key={index} className="flex justify-between text-sm py-1 border-t">
                <span>${offer.price_per_unit.toFixed(2)}</span>
                <span className="text-gray-500">{offer.quantity} units</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3 className="font-semibold text-green-600 border-b pb-1">Bids (Buyers)</h3>
          <ul>
            {requests?.slice(0, 10).map((req, index) => (
              <li key={index} className="flex justify-between text-sm py-1 border-t">
                <span>${req.price_per_unit.toFixed(2)}</span>
                <span className="text-gray-500">{req.quantity} units</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}