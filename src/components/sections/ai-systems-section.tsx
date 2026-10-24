"use client";

import { DetailDrawer } from "@/components/ui/detail-drawer";
import { SectionShell } from "@/components/ui/section-shell";
import { StatusBadge } from "@/components/ui/status-badge";
import { aiSystems } from "@/data/portfolio";
import type { SystemCategory } from "@/types/portfolio";
import { Search } from "lucide-react";
import { useMemo, useState } from "react";

const allCategories: Array<SystemCategory | "All"> = [
  "All",
  "AI Research and Web Intelligence",
  "RAG",
  "Conversational AI and Chatbots",
  "Agentic Workflows",
  "Document Intelligence",
  "Automation and Data Processing",
];

export function AiSystemsSection() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<SystemCategory | "All">("All");
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const filtered = useMemo(() => {
    const needle = query.toLowerCase().trim();
    return aiSystems.filter((item) => {
      const categoryOk = category === "All" || item.category === category;
      const searchHaystack = `${item.name} ${item.description} ${item.technologies.join(" ")}`.toLowerCase();
      return categoryOk && (!needle || searchHaystack.includes(needle));
    });
  }, [category, query]);

  const selected = aiSystems.find((item) => item.id === selectedId) ?? null;

  return (
    <SectionShell
      id="ai-systems"
      title="AI Systems Explorer"
      subtitle="Implemented and illustrative system modules are shown explicitly. Draft labels indicate editable assumptions."
    >
      <div className="mb-5 grid gap-3 md:grid-cols-[1fr_auto]">
        <label className="relative">
          <span className="sr-only">Search AI systems</span>
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search by name, description, or technologies"
            className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-10 py-2 text-zinc-100 outline-none focus:border-cyan-300"
          />
        </label>
        <div className="flex flex-wrap gap-2">
          {allCategories.map((item) => (
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
        <div className="rounded-md border border-zinc-800 bg-zinc-900/30 p-6 text-zinc-300">No systems matched your filters.</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {filtered.map((item) => (
            <article key={item.id} className="rounded-lg border border-zinc-800 bg-zinc-900/35 p-4">
              <div className="mb-2 flex items-start justify-between gap-3">
                <h3 className="text-base font-semibold text-zinc-100">{item.name}</h3>
                <StatusBadge status={item.status} />
              </div>
              <p className="text-sm text-zinc-300">{item.description}</p>
              <p className="mt-3 text-xs text-zinc-400">{item.category}</p>
              <p className="mt-2 text-xs text-zinc-400">{item.implemented ? "Implemented architecture" : "Illustrative architecture"}</p>
              <button
                type="button"
                onClick={() => setSelectedId(item.id)}
                className="mt-4 rounded-md border border-zinc-700 px-3 py-2 text-sm text-zinc-100 hover:border-zinc-500"
              >
                View workflow
              </button>
            </article>
          ))}
        </div>
      )}

      <DetailDrawer title={selected?.name ?? "System details"} open={Boolean(selected)} onClose={() => setSelectedId(null)}>
        {selected ? (
          <>
            <StatusBadge status={selected.status} />
            <p>{selected.description}</p>
            <p className="font-mono text-xs text-zinc-400">{selected.implemented ? "Implemented" : "Illustrative"}</p>
            <p className="text-sm text-zinc-300">Technologies: {selected.technologies.join(" · ")}</p>
            <div className="space-y-2">
              <h4 className="font-semibold text-zinc-100">Workflow steps</h4>
              <ol className="space-y-2">
                {selected.workflow.map((step, index) => (
                  <li key={step} className="rounded-md border border-zinc-700 p-3 text-sm">
                    <span className="font-mono text-xs text-cyan-200">Step {index + 1}</span>
                    <p className="mt-1">{step}</p>
                  </li>
                ))}
              </ol>
            </div>
            {selected.notes ? <p className="text-xs text-zinc-400">{selected.notes}</p> : null}
          </>
        ) : null}
      </DetailDrawer>
    </SectionShell>
  );
}
