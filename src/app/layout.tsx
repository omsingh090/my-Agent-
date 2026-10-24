import type { Metadata } from "next";
import "./globals.css";
import { asSafeUrl, siteConfig } from "@/lib/config";

const canonical = asSafeUrl(siteConfig.baseUrl);
const ogImage = asSafeUrl(siteConfig.ogImageUrl);

export const metadata: Metadata = {
  metadataBase: canonical ? new URL(canonical) : undefined,
  title: siteConfig.siteName,
  description: siteConfig.description,
  alternates: canonical ? { canonical } : undefined,
  openGraph: {
    title: siteConfig.siteName,
    description: siteConfig.description,
    type: "website",
    url: canonical,
    images: ogImage ? [{ url: ogImage }] : undefined,
  },
  twitter: {
    card: "summary_large_image",
    title: siteConfig.siteName,
    description: siteConfig.description,
    images: ogImage ? [ogImage] : undefined,
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full bg-zinc-950 text-zinc-100">{children}</body>
    </html>
  );
}
