"use client";
import { useEffect, useState } from "react";

interface Props {
  player: string;
  api: string;
}

export default function HiddenFacts({ player, api }: Props) {
  const [facts, setFacts] = useState<{ fact: string; context: string }[]>([]);

  useEffect(() => {
    if (!player) return;
    fetch(`${api}/hidden-facts/${player}`)
      .then((r) => r.json())
      .then((d) => setFacts(d.facts || []))
      .catch(() => setFacts([]));
  }, [player, api]);

  if (!player) return <div className="text-gray-500 p-4">Search a player to discover hidden facts</div>;

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-yellow-400">🤯 Hidden Facts about {player}</h3>
      {facts.length === 0 && <p className="text-gray-500">No hidden facts found</p>}
      {facts.map((fact, i) => (
        <div key={i} className="p-4 bg-gray-900 rounded-lg border border-gray-800">
          <p className="text-white">{fact.fact}</p>
          <p className="text-gray-500 text-sm mt-1">{fact.context}</p>
        </div>
      ))}
    </div>
  );
}
