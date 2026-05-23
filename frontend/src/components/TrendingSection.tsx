"use client";
import { useEffect, useState } from "react";

interface Props {
  api: string;
}

export default function TrendingSection({ api }: Props) {
  const [trending, setTrending] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${api}/trending-connections`)
      .then((r) => r.json())
      .then((d) => setTrending(d.trending || []))
      .catch(() => setTrending([]));
  }, [api]);

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-yellow-400">🔥 Most Connected Players</h3>
      {trending.map((item, i) => (
        <div key={i} className="flex items-center justify-between p-3 bg-gray-900 rounded-lg border border-gray-800">
          <span className="text-white font-medium">{item.player}</span>
          <span className="text-yellow-400 text-sm">{item.connections} connections</span>
        </div>
      ))}
    </div>
  );
}
