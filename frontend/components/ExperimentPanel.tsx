"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

export default function ExperimentPanel() {
  const [data, setData] = useState<any>(null);
  const experimentName = "button_test"; // change if needed

  useEffect(() => {
    api
      .get(`/analytics/experiments/evaluate/${experimentName}`)
      .then((res) => setData(res.data))
      .catch(() => setData(null));
  }, []);

  if (!data) return <p>Loading experiment data...</p>;

  if (data.error) {
    return (
      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="text-lg font-semibold mb-2">
          Experiment: {experimentName}
        </h2>
        <p className="text-red-500">{data.error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow space-y-4">
      <h2 className="text-lg font-semibold text-emerald-600">
        Experiment: {experimentName}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {data.variants?.map((variant: any) => (
          <div
            key={variant.variant_name}
            className="border rounded-lg p-4"
          >
            <p className="font-medium text-slate-800">{variant.variant_name}</p>
            <p className="text-orange-800">Total Users: {variant.total_users}</p>
            <p className="text-orange-800">Conversions: {variant.conversions}</p>
            <p className="text-orange-800">
              Conversion Rate:{" "}
              {(variant.conversion_rate * 100).toFixed(2)}%
            </p>
          </div>
        ))}
      </div>

      {data.p_value !== undefined && (
        <div className="mt-4">
          <p className="text-sm text-gray-600">
            P-Value:{" "}
            <span
              className={`font-semibold ${
                data.p_value < 0.05
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {data.p_value}
            </span>
          </p>

          <p className="text-xs text-gray-500 mt-1">
            {data.p_value < 0.05
              ? "Statistically significant difference detected."
              : "No statistically significant difference yet."}
          </p>
        </div>
      )}
    </div>
  );
}