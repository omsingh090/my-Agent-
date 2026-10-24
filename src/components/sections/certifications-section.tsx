"use client";

import { DetailDrawer } from "@/components/ui/detail-drawer";
import { SectionShell } from "@/components/ui/section-shell";
import { StatusBadge } from "@/components/ui/status-badge";
import { certifications } from "@/data/portfolio";
import { ExternalLink } from "lucide-react";
import { useMemo, useState } from "react";

export function CertificationsSection() {
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    return certifications.filter((item) => `${item.title} ${item.issuer} ${item.category}`.toLowerCase().includes(q));
  }, [query]);

  const selected = certifications.find((item) => item.id === selectedId) ?? null;

  return (
    <SectionShell
      id="certifications"
      title="Certifications"
      subtitle="Only confirmed certifications should be published. Current state is intentionally editable."
    >
      <div className="mb-4">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search certifications"
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-zinc-100"
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {filtered.map((item) => (
          <article key={item.id} className="rounded-lg border border-zinc-800 bg-zinc-900/35 p-4">
            <div className="mb-2 flex items-center justify-between gap-3">
              <h3 className="font-semibold text-zinc-100">{item.title}</h3>
              <StatusBadge status={item.status} />
            </div>
            <p className="text-sm text-zinc-300">{item.issuer}</p>
            <p className="mt-2 text-xs text-zinc-400">{item.category}</p>
            <button
              type="button"
              className="mt-4 rounded-md border border-zinc-700 px-3 py-2 text-sm text-zinc-100"
              onClick={() => setSelectedId(item.id)}
            >
              View details
            </button>
          </article>
        ))}
      </div>

      <DetailDrawer title={selected?.title ?? "Certification details"} open={Boolean(selected)} onClose={() => setSelectedId(null)}>
        {selected ? (
          <>
            <StatusBadge status={selected.status} />
            <p>{selected.summary}</p>
            <p className="text-sm text-zinc-300">Issuer: {selected.issuer}</p>
            <div className="flex flex-wrap gap-2">
              {selected.certificatePath ? (
                <a
                  href={selected.certificatePath}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 rounded-md border border-cyan-300/40 px-3 py-2 text-sm text-cyan-200"
                >
                  View certificate <ExternalLink className="h-4 w-4" />
                </a>
              ) : (
                <span className="text-xs text-zinc-400">Certificate file not configured.</span>
              )}
              {selected.verificationUrl ? (
                <a
                  href={selected.verificationUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 rounded-md border border-cyan-300/40 px-3 py-2 text-sm text-cyan-200"
                >
                  Verify <ExternalLink className="h-4 w-4" />
                </a>
              ) : (
                <span className="text-xs text-zinc-400">Verification link not configured.</span>
              )}
            </div>
          </>
        ) : null}
      </DetailDrawer>
    </SectionShell>
  );
}
