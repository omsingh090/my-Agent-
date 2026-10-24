import type { MetadataRoute } from "next";
import { asSafeUrl, siteConfig } from "@/lib/config";

export default function sitemap(): MetadataRoute.Sitemap {
  const base = asSafeUrl(siteConfig.baseUrl);
  if (!base) return [];

  return [
    {
      url: base,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 1,
    },
  ];
}
