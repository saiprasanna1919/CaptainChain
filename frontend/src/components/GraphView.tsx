"use client";
import { useMemo } from "react";
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  Controls,
  Node,
  Edge,
  ConnectionMode,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

interface Connection {
  connected_to: string;
  team: string;
  season: string;
}

interface GraphData {
  path?: string[];
  relationships?: { team: string; season: string }[];
  player?: string;
  connections?: Connection[];
}

interface Props {
  data: GraphData | null;
}

function Graph({ data }: Props) {
  const { nodes, edges } = useMemo(() => {
    const nodes: Node[] = [];
    const edges: Edge[] = [];

    if (!data) return { nodes, edges };

    if (data.path) {
      data.path.forEach((name: string, i: number) => {
        nodes.push({
          id: name,
          position: { x: 250 * i, y: 100 + (i % 2) * 80 },
          data: { label: name },
          style: {
            background: i === 0 ? "#eab308" : i === data.path!.length - 1 ? "#f97316" : "#374151",
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
            source: data.path![i - 1],
            target: name,
            label: rel ? `${rel.team} (${rel.season})` : "",
            style: { stroke: "#eab308" },
            labelStyle: { fill: "#9ca3af", fontSize: 11 },
          });
        }
      });
    } else if (data.connections) {
      const playerName = data.player!;
      nodes.push({
        id: playerName,
        position: { x: 300, y: 300 },
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
      const uniqueConns = data.connections.filter((conn) => {
        if (seen.has(conn.connected_to)) return false;
        seen.add(conn.connected_to);
        return true;
      });
      const limited = uniqueConns.slice(0, 20);
      limited.forEach((conn, i: number) => {
        const angle = (i / limited.length) * 2 * Math.PI;
        nodes.push({
          id: conn.connected_to,
          position: { x: 300 + Math.cos(angle) * 220, y: 300 + Math.sin(angle) * 220 },
          data: { label: conn.connected_to },
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
          target: conn.connected_to,
          label: `${conn.team} ${conn.season}`,
          style: { stroke: "#6b7280" },
          labelStyle: { fill: "#9ca3af", fontSize: 10 },
        });
      });
    }

    return { nodes, edges };
  }, [data]);

  if (!data || nodes.length === 0) {
    return (
      <div className="h-96 flex items-center justify-center text-gray-500">
        Search for a player to see their captain chain graph
      </div>
    );
  }

  return (
    <div style={{ width: "100%", height: "500px" }}>
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

export default function GraphView({ data }: Props) {
  return (
    <ReactFlowProvider>
      <Graph data={data} />
    </ReactFlowProvider>
  );
}
