"use client";

import { DetailDrawer } from "@/components/ui/detail-drawer";
import { SectionShell } from "@/components/ui/section-shell";
import { StatusBadge } from "@/components/ui/status-badge";
import { tools } from "@/data/portfolio";
import type { ToolCategory } from "@/types/portfolio";
import { ExternalLink } from "lucide-react";
import { useMemo, useState } from "react";

const categories: Array<ToolCategory | "All"> = [
  "All",
  "LLM Providers",
  "Web Search and Extraction",
  "Agent Frameworks",
  "Model/ML Ecosystem",
  "Programming/Libraries",
  "Data/Databases",
  "Development Tools",
  "Deployment/Infrastructure",
];

export function ToolsSection() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<ToolCategory | "All">("All");
  const [selected, setSelected] = useState<string | null>(null);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    return tools.filter((item) => {
      const categoryMatch = category === "All" || item.category === category;
      const haystack = `${item.name} ${item.description} ${item.relatedProjects.join(" ")} ${item.relatedSystems.join(" ")}`.toLowerCase();
      return categoryMatch && (!q || haystack.includes(q));
    });
  }, [category, query]);

  const active = tools.find((item) => item.id === selected) ?? null;

  return (
    <SectionShell id="tools" title="Tools Toolbox" subtitle="Searchable tools list, separated from skills for stack-level visibility.">
      <div className="mb-4 grid gap-3 md:grid-cols-[1fr_auto]">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-zinc-100"
          placeholder="Search tools"
        />
        <div className="flex flex-wrap gap-2">
          {categories.map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setCategory(item)}
              className={`rounded-md border px-3 py-2 text-xs sm:text-sm ${
                category === item ? "border-cyan-300/50 text-cyan-200" : "border-zinc-700 text-zinc-300"
              }`}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <p className="rounded-md border border-zinc-800 bg-zinc-900/30 p-5 text-zinc-300">No tools matched your filters.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((tool) => (
            <article key={tool.id} className="rounded-lg border border-zinc-800 bg-zinc-900/35 p-4">
              <div className="mb-2 flex items-center justify-between gap-3">
                <h3 className="font-semibold text-zinc-100">{tool.name}</h3>
                <StatusBadge status={tool.status} />
              </div>
              <p className="text-sm text-zinc-300">{tool.description}</p>
              <p className="mt-2 text-xs text-zinc-400">{tool.category}</p>
              <button
                type="button"
                className="mt-3 rounded-md border border-zinc-700 px-3 py-2 text-xs text-zinc-200"
                onClick={() => setSelected(tool.id)}
              >
                View details
              </button>
            </article>
          ))}
        </div>
      )}

      <DetailDrawer title={active?.name ?? "Tool details"} open={Boolean(active)} onClose={() => setSelected(null)}>
        {active ? (
          <>
            <StatusBadge status={active.status} />
            <p>{active.description}</p>
            <p className="text-sm text-zinc-300">Category: {active.category}</p>
            <p className="text-sm text-zinc-300">Related projects: {active.relatedProjects.join(" · ")}</p>
            <p className="text-sm text-zinc-300">Related systems: {active.relatedSystems.join(" · ")}</p>
            {active.officialUrl ? (
              <a
                href={active.officialUrl}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 rounded-md border border-cyan-300/40 px-3 py-2 text-sm text-cyan-200"
              >
                Official link <ExternalLink className="h-4 w-4" />
              </a>
            ) : (
              <p className="text-xs text-zinc-400">Official link not configured.</p>
            )}
          </>
        ) : null}
      </DetailDrawer>
    </SectionShell>
  );
}
