"use client";
import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import GraphView from "@/components/GraphView";
import Timeline from "@/components/Timeline";
import HiddenFacts from "@/components/HiddenFacts";
import TrendingSection from "@/components/TrendingSection";

type Tab = "graph" | "timeline" | "facts" | "trending";

export default function Home() {
  const [player1, setPlayer1] = useState("");
  const [player2, setPlayer2] = useState("");
  const [graphData, setGraphData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<Tab>("graph");
  const [loading, setLoading] = useState(false);

  const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  async function searchRelationship() {
    if (!player1) return;
    setLoading(true);
    try {
      if (player2) {
        const res = await fetch(`${API}/shortest-path?player1=${player1}&player2=${player2}`);
        const data = await res.json();
        setGraphData(data);
      } else {
        const res = await fetch(`${API}/player/connections/${player1}`);
        const data = await res.json();
        setGraphData(data);
      }
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  }

  const tabs: { id: Tab; label: string }[] = [
    { id: "graph", label: "🔗 Graph" },
    { id: "timeline", label: "📅 Timeline" },
    { id: "facts", label: "🤯 Hidden Facts" },
    { id: "trending", label: "🔥 Trending" },
  ];

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      <header className="border-b border-gray-800 p-6">
        <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">
          🏏 CaptainChain
        </h1>
        <p className="text-center text-gray-400 mt-1">Discover hidden cricket relationships</p>
      </header>

      <div className="max-w-5xl mx-auto p-6">
        <SearchBar
          player1={player1}
          player2={player2}
          setPlayer1={setPlayer1}
          setPlayer2={setPlayer2}
          onSearch={searchRelationship}
          loading={loading}
        />

        <div className="flex gap-2 mt-6 border-b border-gray-800 pb-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-t text-sm font-medium transition ${
                activeTab === tab.id
                  ? "bg-gray-800 text-yellow-400"
                  : "text-gray-500 hover:text-gray-300"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="mt-4">
          {activeTab === "graph" && <GraphView data={graphData} />}
          {activeTab === "timeline" && <Timeline player={player1} api={API} />}
          {activeTab === "facts" && <HiddenFacts player={player1} api={API} />}
          {activeTab === "trending" && <TrendingSection api={API} />}
        </div>
      </div>
    </main>
  );
}
