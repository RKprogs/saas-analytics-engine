"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

export default function ChurnTable() {
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    api.get("/analytics/churn/top-risk?limit=10")
      .then((res) => setUsers(res.data));
  }, []);

  if (!users.length) return <p>Loading churn risk...</p>;

  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900">
        Top 10 High-Risk Users
      </h2>

      <table className="w-full text-sm">
        <thead>
          <tr className="text-left border-b text-sky-600">
            <th className="py-2">Email</th>
            <th className="py-2">Churn Probability</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr
              key={user.user_id}
              className="border-b hover:bg-gray-50 text-slate-800"
            >
              <td className="py-2">{user.email}</td>
              <td className="py-2">
                <span
                  className={`px-2 py-1 rounded text-white ${
                    user.churn_probability > 0.7
                      ? "bg-red-500"
                      : user.churn_probability > 0.4
                      ? "bg-yellow-500"
                      : "bg-green-500"
                  }`}
                >
                  {user.churn_probability}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}