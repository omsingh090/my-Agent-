import type { MetadataRoute } from "next";
import { asSafeUrl, siteConfig } from "@/lib/config";

export default function robots(): MetadataRoute.Robots {
  const base = asSafeUrl(siteConfig.baseUrl);
  return {
    rules: [{ userAgent: "*", allow: "/" }],
    sitemap: base ? `${base}/sitemap.xml` : undefined,
  };
}
