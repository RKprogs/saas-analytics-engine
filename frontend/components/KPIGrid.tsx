"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

export default function KPIGrid() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    api.get("/analytics/executive").then((res) => {
      setData(res.data);
    });
  }, []);

  if (!data) return <p>Loading metrics...</p>;

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      {Object.entries(data).map(([key, value]) => (
        <div
          key={key}
          className="bg-white shadow rounded-xl p-4"
        >
          <p className="text-sm text-gray-500">{key}</p>
          <p className="text-xl font-semibold text-emerald-600">{String(value)}</p>
        </div>
      ))}
    </div>
  );
}