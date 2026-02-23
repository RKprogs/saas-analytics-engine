import KPIGrid from "@/components/KPIGrid";
import RetentionChart from "@/components/RetentionChart";
import ChurnTable from "@/components/ChurnTable";
import ExperimentPanel from "@/components/ExperimentPanel";
import SQLPanel from "@/components/SQLPanel";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 p-8 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">
        AI SaaS Intelligence Dashboard
      </h1>

      <KPIGrid />

      <RetentionChart />

      <ChurnTable />

      <ExperimentPanel />

      <SQLPanel />
    </main>
  );
}