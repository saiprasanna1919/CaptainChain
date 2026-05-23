import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CaptainChain - Cricket Relationship Discovery",
  description: "Discover hidden cricket captain-player relationships",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-gray-950 antialiased">{children}</body>
    </html>
  );
}
