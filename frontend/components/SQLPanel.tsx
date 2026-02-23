"use client";

import { useState } from "react";
import api from "@/lib/api";

export default function SQLPanel() {
  const [query, setQuery] = useState("SELECT * FROM users LIMIT 5;");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runQuery = async () => {
    try {
        setLoading(true);
        const res = await api.post("/analytics/sql/query", { query });
        setResult(res.data);
        setResult(res.data);
    } catch (err: any) {
        setResult({error: err.message });
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="bg-gradient-to-br from-slate-50 to-slate-100 p-8 rounded-2xl shadow-xl space-y-6 border border-slate-200">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-slate-800">
          SQL Insights
        </h2>

        {loading && (
          <span className="text-sm text-blue-600 animate-pulse">
            Running query...
          </span>
        )}
      </div>

      <textarea
        className="w-full rounded-xl p-4 font-mono text-sm bg-slate-900 text-emerald-400 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
        rows={5}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button
        onClick={runQuery}
        className="bg-blue-600 hover:bg-blue-700 active:scale-95 transition text-white px-6 py-2 rounded-lg font-medium shadow-md"
      >
        Run Query
      </button>

      {result?.error && (
        <div className="bg-red-50 border border-red-200 text-red-600 p-3 rounded-lg text-sm">
          {result.error}
        </div>
      )}

      {result?.rows && (
        <div className="overflow-x-auto rounded-xl border border-slate-200 shadow-sm">
          <table className="min-w-full text-sm">
            <thead className="bg-slate-100 text-slate-700 uppercase text-xs tracking-wide">
              <tr>
                {result.columns.map((col: string) => (
                  <th key={col} className="px-4 py-3 text-left border-b">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {result.rows.map((row: any[], i: number) => (
                <tr key={i} className="even:bg-slate-50 hover:bg-blue-50 transition">
                  {row.map((cell, j) => (
                    <td key={j} className="px-4 py-2 border-b text-slate-700">
                      {String(cell)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}