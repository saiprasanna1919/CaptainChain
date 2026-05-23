"use client";
import { useCallback, useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  Node,
  Edge,
  ConnectionMode,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

interface Props {
  data: any;
}

export default function GraphView({ data }: Props) {
  if (!data) {
    return (
      <div className="h-96 flex items-center justify-center text-gray-500">
        Search for a player to see their captain chain graph
      </div>
    );
  }

  // Build nodes and edges from path data or connections data
  const { nodes, edges } = useMemo(() => {
    const nodes: Node[] = [];
    const edges: Edge[] = [];

    if (data.path) {
      // Shortest path result
      data.path.forEach((name: string, i: number) => {
        nodes.push({
          id: name,
          position: { x: 250 * i, y: 100 + (i % 2) * 80 },
          data: { label: name },
          style: {
            background: i === 0 ? "#eab308" : i === data.path.length - 1 ? "#f97316" : "#374151",
            color: "white",
            border: "1px solid #6b7280",
            borderRadius: "8px",
            padding: "10px 16px",
            fontWeight: "bold",
          },
        });
        if (i > 0) {
          const rel = data.relationships?.[i - 1];
          edges.push({
            id: `e-${i}`,
            source: data.path[i - 1],
            target: name,
            label: rel ? `${rel.team} (${rel.season})` : "",
            style: { stroke: "#eab308" },
            labelStyle: { fill: "#9ca3af", fontSize: 11 },
          });
        }
      });
    } else if (data.connections) {
      // Connections result
      const playerName = data.player;
      nodes.push({
        id: playerName,
        position: { x: 300, y: 200 },
        data: { label: playerName },
        style: {
          background: "#eab308",
          color: "black",
          borderRadius: "8px",
          padding: "10px 16px",
          fontWeight: "bold",
        },
      });

      const seen = new Set<string>();
      data.connections.forEach((conn: any, i: number) => {
        const other = conn.connected_to;
        if (seen.has(other)) return;
        seen.add(other);
        const angle = (i / data.connections.length) * 2 * Math.PI;
        nodes.push({
          id: other,
          position: { x: 300 + Math.cos(angle) * 200, y: 200 + Math.sin(angle) * 200 },
          data: { label: other },
          style: {
            background: "#374151",
            color: "white",
            border: "1px solid #6b7280",
            borderRadius: "8px",
            padding: "8px 12px",
          },
        });
        edges.push({
          id: `e-${i}`,
          source: playerName,
          target: other,
          label: `${conn.team} ${conn.season}`,
          style: { stroke: "#6b7280" },
          labelStyle: { fill: "#9ca3af", fontSize: 10 },
        });
      });
    }

    return { nodes, edges };
  }, [data]);

  return (
    <div className="h-96 border border-gray-800 rounded-lg overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        connectionMode={ConnectionMode.Loose}
        fitView
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#374151" gap={20} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
