"use client";
import { useEffect, useState } from "react";

interface Props {
  player: string;
  api: string;
}

interface TimelineEntry {
  captain: string;
  team: string;
  season: string;
  year: number;
}

export default function Timeline({ player, api }: Props) {
  const [timeline, setTimeline] = useState<TimelineEntry[]>([]);

  useEffect(() => {
    if (!player) return;
    fetch(`${api}/captain-timeline/${player}`)
      .then((r) => r.json())
      .then((d) => setTimeline(d.timeline || []))
      .catch(() => setTimeline([]));
  }, [player, api]);

  if (!player) return <div className="text-gray-500 p-4">Search a player to see their captain timeline</div>;

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-yellow-400">📅 {player}&apos;s Captain Timeline</h3>
      {timeline.length === 0 && <p className="text-gray-500">No timeline data found</p>}
      {timeline.map((entry, i) => (
        <div key={i} className="flex items-center gap-4 p-3 bg-gray-900 rounded-lg border border-gray-800">
          <div className="text-yellow-500 font-bold text-sm w-12">{entry.year}</div>
          <div className="w-2 h-2 bg-yellow-500 rounded-full" />
          <div>
            <p className="text-white font-medium">Under {entry.captain}</p>
            <p className="text-gray-400 text-sm">{entry.team} • {entry.season}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
