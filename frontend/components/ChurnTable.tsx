"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

export default function ChurnTable() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/analytics/churn/top-risk?limit=10")
      .then((res) => setUsers(res.data))
      .finally(() => setLoading(false));
  }, []);

  const getRiskStyles = (prob: number) => {
    if (prob > 0.7)
      return {
        badge: "bg-red-500 text-white",
        bar: "bg-red-500",
        label: "High Risk",
      };
    if (prob > 0.4)
      return {
        badge: "bg-amber-500 text-white",
        bar: "bg-amber-500",
        label: "Medium Risk",
      };
    return {
      badge: "bg-emerald-500 text-white",
      bar: "bg-emerald-500",
      label: "Low Risk",
    };
  };

  return (
    <div className="bg-gradient-to-br from-white to-slate-50 p-8 rounded-2xl shadow-xl border border-slate-200">

      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-slate-800">
          Top 10 High-Risk Users
        </h2>
      </div>

      {loading ? (
        <div className="animate-pulse space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-6 bg-slate-200 rounded" />
          ))}
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl">
          <table className="w-full text-sm">
            <thead className="text-left border-b text-slate-600 uppercase text-xs tracking-wide">
              <tr>
                <th className="py-3">Email</th>
                <th className="py-3">Churn Probability</th>
              </tr>
            </thead>
          <tbody> 
            {users.map((user) => {
                const risk = getRiskStyles(user.churn_probability);
                const percent = (user.churn_probability * 100).toFixed(1);

                return (
                  <tr
                    key={user.user_id}
                    className="border-b hover:bg-slate-100 transition"
                  >
                    <td className="py-4 text-slate-800 font-medium">
                      {user.email}
                    </td>

                    <td className="py-4 w-1/2">
                      <div className="flex items-center gap-4">

                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${risk.badge}`}
                        >
                          {risk.label}
                        </span>

                        <div className="flex-1">
                          <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                            <div
                              className={`h-2 ${risk.bar} transition-all duration-500`}
                              style={{ width: `${percent}%` }}
                            />
                          </div>
                        </div>

                        <span className="text-slate-700 font-semibold w-14 text-right">
                          {percent}%
                        </span>

                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}