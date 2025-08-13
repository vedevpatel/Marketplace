import React from "react";

export default function MarketTable({ data }) {
  return (
    <table className="table-auto border-collapse border border-gray-400 w-full mt-4">
      <thead>
        <tr>
          <th className="border px-4 py-2">Seller</th>
          <th className="border px-4 py-2">Price</th>
          <th className="border px-4 py-2">Inventory</th>
        </tr>
      </thead>
      <tbody>
        {data.sellers.map((s) => (
          <tr key={s.id}>
            <td className="border px-4 py-2">{s.id}</td>
            <td className="border px-4 py-2">${s.price}</td>
            <td className="border px-4 py-2">{s.inventory}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
