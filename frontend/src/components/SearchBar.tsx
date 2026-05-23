"use client";

interface Props {
  player1: string;
  player2: string;
  setPlayer1: (v: string) => void;
  setPlayer2: (v: string) => void;
  onSearch: () => void;
  loading: boolean;
}

export default function SearchBar({ player1, player2, setPlayer1, setPlayer2, onSearch, loading }: Props) {
  return (
    <div className="flex flex-col sm:flex-row gap-3">
      <input
        type="text"
        placeholder="Player 1 (e.g. Rohit)"
        value={player1}
        onChange={(e) => setPlayer1(e.target.value)}
        className="flex-1 px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-yellow-500"
        onKeyDown={(e) => e.key === "Enter" && onSearch()}
      />
      <input
        type="text"
        placeholder="Player 2 (optional, e.g. Dhoni)"
        value={player2}
        onChange={(e) => setPlayer2(e.target.value)}
        className="flex-1 px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-yellow-500"
        onKeyDown={(e) => e.key === "Enter" && onSearch()}
      />
      <button
        onClick={onSearch}
        disabled={loading || !player1}
        className="px-6 py-3 bg-yellow-500 text-black font-bold rounded-lg hover:bg-yellow-400 disabled:opacity-50 transition"
      >
        {loading ? "..." : "🔍 Discover"}
      </button>
    </div>
  );
}
