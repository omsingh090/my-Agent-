"use client";

import { DetailDrawer } from "@/components/ui/detail-drawer";
import { SectionShell } from "@/components/ui/section-shell";
import { StatusBadge } from "@/components/ui/status-badge";
import { projects } from "@/data/portfolio";
import type { ProjectCategory } from "@/types/portfolio";
import { ExternalLink } from "lucide-react";
import { useMemo, useState } from "react";

const categories: Array<ProjectCategory | "All"> = ["All", "Healthcare", "Enterprise", "Recommendation", "NLP", "Draft"];

export function ProjectsSection() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<ProjectCategory | "All">("All");
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    return projects.filter((project) => {
      const categoryMatch = category === "All" || project.category === category;
      const haystack = `${project.name} ${project.summary} ${project.stack.join(" ")}`.toLowerCase();
      return categoryMatch && (!q || haystack.includes(q));
    });
  }, [category, query]);

  const selected = projects.find((project) => project.id === selectedId) ?? null;

  return (
    <SectionShell
      id="projects"
      title="Projects"
      subtitle="Evidence-backed and draft project cards without fabricated metrics, links, or outcomes."
    >
      <div className="mb-4 grid gap-3 md:grid-cols-[1fr_auto]">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-zinc-100"
          placeholder="Search projects"
        />
        <div className="flex flex-wrap gap-2">
          {categories.map((item) => (
            <button
              key={item}
              type="button"
              className={`rounded-md border px-3 py-2 text-xs sm:text-sm ${
                item === category ? "border-lime-300/50 text-lime-200" : "border-zinc-700 text-zinc-300"
              }`}
              onClick={() => setCategory(item)}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <p className="rounded-md border border-zinc-800 bg-zinc-900/30 p-5 text-zinc-300">No projects matched your filters.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {filtered.map((project) => (
            <article key={project.id} className="rounded-lg border border-zinc-800 bg-zinc-900/35 p-4">
              <div className="mb-2 flex items-start justify-between gap-3">
                <h3 className="text-lg font-semibold text-zinc-100">{project.name}</h3>
                <StatusBadge status={project.status} />
              </div>
              <p className="text-sm text-zinc-300">{project.summary}</p>
              <p className="mt-2 text-xs text-zinc-400">{project.category}</p>
              <p className="mt-2 text-xs text-zinc-400">Stack: {project.stack.join(" · ")}</p>
              <button
                type="button"
                className="mt-4 rounded-md border border-zinc-700 px-3 py-2 text-sm text-zinc-100"
                onClick={() => setSelectedId(project.id)}
              >
                View architecture
              </button>
            </article>
          ))}
        </div>
      )}

      <DetailDrawer title={selected?.name ?? "Project details"} open={Boolean(selected)} onClose={() => setSelectedId(null)}>
        {selected ? (
          <>
            <StatusBadge status={selected.status} />
            <p>{selected.summary}</p>
            <div>
              <h4 className="font-semibold text-zinc-100">Architecture / Workflow</h4>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm">
                {selected.architecture.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-zinc-100">Contribution</h4>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm">
                {selected.contribution.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-zinc-100">Challenges / Learnings</h4>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm">
                {selected.challengesAndLearnings.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            <p className="text-sm">Stack: {selected.stack.join(" · ")}</p>
            <div className="flex flex-wrap gap-2">
              {selected.externalUrl ? (
                <a
                  href={selected.externalUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 rounded-md border border-cyan-300/40 px-3 py-2 text-sm text-cyan-200"
                >
                  Project link <ExternalLink className="h-4 w-4" />
                </a>
              ) : (
                <span className="text-xs text-zinc-400">Project link not configured.</span>
              )}
              {selected.repoUrl ? (
                <a
                  href={selected.repoUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 rounded-md border border-cyan-300/40 px-3 py-2 text-sm text-cyan-200"
                >
                  Repository <ExternalLink className="h-4 w-4" />
                </a>
              ) : null}
            </div>
            {selected.notes ? <p className="text-xs text-zinc-400">{selected.notes}</p> : null}
          </>
        ) : null}
      </DetailDrawer>
    </SectionShell>
  );
}
