"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function RetentionChart() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    api.get("/analytics/retention/cohort?max_days=3").then((res) => {
      const cohorts = res.data;

      // Convert backend format to chart-friendly format
      const formatted: any[] = [];

      Object.entries(cohorts).forEach(([date, values]: any) => {
        formatted.push({
          cohort: date,
          day1: values.day_1 || 0,
          day2: values.day_2 || 0,
          day3: values.day_3 || 0,
        });
      });

      setData(formatted);
    });
  }, []);

  if (!data.length) return <p>Loading retention...</p>;

  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-900">
        Cohort Retention (Day 1–3)
      </h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="cohort" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="day1" stroke="#2563eb" />
          <Line type="monotone" dataKey="day2" stroke="#16a34a" />
          <Line type="monotone" dataKey="day3" stroke="#dc2626" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}