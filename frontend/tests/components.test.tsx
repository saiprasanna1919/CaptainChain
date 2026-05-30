import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import SearchBar from "@/components/SearchBar";
import TrendingSection from "@/components/TrendingSection";
import HiddenFacts from "@/components/HiddenFacts";
import Timeline from "@/components/Timeline";

// Mock fetch globally
const mockFetch = vi.fn();
global.fetch = mockFetch;

beforeEach(() => {
  mockFetch.mockReset();
});

describe("SearchBar", () => {
  it("renders both inputs and button", () => {
    render(
      <SearchBar player1="" player2="" setPlayer1={vi.fn()} setPlayer2={vi.fn()} onSearch={vi.fn()} loading={false} />
    );
    expect(screen.getByPlaceholderText(/Player 1/)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Player 2/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Discover/ })).toBeInTheDocument();
  });

  it("calls onSearch when button clicked", () => {
    const onSearch = vi.fn();
    render(
      <SearchBar player1="Dhoni" player2="" setPlayer1={vi.fn()} setPlayer2={vi.fn()} onSearch={onSearch} loading={false} />
    );
    fireEvent.click(screen.getByRole("button", { name: /Discover/ }));
    expect(onSearch).toHaveBeenCalledOnce();
  });

  it("disables button when loading", () => {
    render(
      <SearchBar player1="Dhoni" player2="" setPlayer1={vi.fn()} setPlayer2={vi.fn()} onSearch={vi.fn()} loading={true} />
    );
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("disables button when player1 is empty", () => {
    render(
      <SearchBar player1="" player2="" setPlayer1={vi.fn()} setPlayer2={vi.fn()} onSearch={vi.fn()} loading={false} />
    );
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("calls onSearch on Enter key", () => {
    const onSearch = vi.fn();
    render(
      <SearchBar player1="Dhoni" player2="" setPlayer1={vi.fn()} setPlayer2={vi.fn()} onSearch={onSearch} loading={false} />
    );
    fireEvent.keyDown(screen.getByPlaceholderText(/Player 1/), { key: "Enter" });
    expect(onSearch).toHaveBeenCalledOnce();
  });
});

describe("TrendingSection", () => {
  it("fetches and displays trending players", async () => {
    mockFetch.mockResolvedValueOnce({
      json: async () => ({ trending: [{ player: "MS Dhoni", connections: 42 }, { player: "Virat Kohli", connections: 38 }] }),
    });

    render(<TrendingSection api="http://localhost:8000" />);

    await waitFor(() => {
      expect(screen.getByText("MS Dhoni")).toBeInTheDocument();
      expect(screen.getByText("42 connections")).toBeInTheDocument();
      expect(screen.getByText("Virat Kohli")).toBeInTheDocument();
    });
  });

  it("handles fetch error gracefully", async () => {
    mockFetch.mockRejectedValueOnce(new Error("Network error"));
    render(<TrendingSection api="http://localhost:8000" />);
    await waitFor(() => {
      expect(screen.getByText(/Most Connected Players/)).toBeInTheDocument();
    });
  });
});

describe("HiddenFacts", () => {
  it("shows placeholder when no player searched", () => {
    render(<HiddenFacts player="" api="http://localhost:8000" />);
    expect(screen.getByText(/Search a player to discover hidden facts/)).toBeInTheDocument();
  });

  it("fetches and displays facts for a player", async () => {
    mockFetch.mockResolvedValueOnce({
      json: async () => ({
        facts: [{ fact: "Dhoni captained Kohli in IPL 2008", context: "CSK - IPL 2008" }],
      }),
    });

    render(<HiddenFacts player="Dhoni" api="http://localhost:8000" />);

    await waitFor(() => {
      expect(screen.getByText("Dhoni captained Kohli in IPL 2008")).toBeInTheDocument();
      expect(screen.getByText("CSK - IPL 2008")).toBeInTheDocument();
    });
  });

  it("shows no facts message when empty", async () => {
    mockFetch.mockResolvedValueOnce({ json: async () => ({ facts: [] }) });
    render(<HiddenFacts player="Unknown" api="http://localhost:8000" />);
    await waitFor(() => {
      expect(screen.getByText("No hidden facts found")).toBeInTheDocument();
    });
  });
});

describe("Timeline", () => {
  it("shows placeholder when no player searched", () => {
    render(<Timeline player="" api="http://localhost:8000" />);
    expect(screen.getByText(/Search a player to see their captain timeline/)).toBeInTheDocument();
  });

  it("fetches and displays timeline entries", async () => {
    mockFetch.mockResolvedValueOnce({
      json: async () => ({
        timeline: [
          { captain: "MS Dhoni", team: "CSK", season: "IPL 2018", year: 2018 },
          { captain: "Rohit Sharma", team: "India", season: "ODI 2023", year: 2023 },
        ],
      }),
    });

    render(<Timeline player="Kohli" api="http://localhost:8000" />);

    await waitFor(() => {
      expect(screen.getByText("Under MS Dhoni")).toBeInTheDocument();
      expect(screen.getByText(/CSK.*IPL 2018/)).toBeInTheDocument();
      expect(screen.getByText("Under Rohit Sharma")).toBeInTheDocument();
    });
  });

  it("shows no data message when timeline is empty", async () => {
    mockFetch.mockResolvedValueOnce({ json: async () => ({ timeline: [] }) });
    render(<Timeline player="Unknown" api="http://localhost:8000" />);
    await waitFor(() => {
      expect(screen.getByText("No timeline data found")).toBeInTheDocument();
    });
  });
});
