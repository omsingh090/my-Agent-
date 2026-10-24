"use client";

import { SectionShell } from "@/components/ui/section-shell";
import { StatusBadge } from "@/components/ui/status-badge";
import { skills } from "@/data/portfolio";
import type { SkillCategory } from "@/types/portfolio";
import { useMemo, useState } from "react";

const categories: Array<SkillCategory | "All"> = ["All", "Core AI", "LLM & Prompting", "Engineering", "Data & Analytics", "Delivery"];

export function SkillsSection() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState<SkillCategory | "All">("All");

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    return skills.filter((skill) => {
      const categoryMatch = category === "All" || skill.category === category;
      const text = `${skill.name} ${skill.description} ${skill.relatedTools.join(" ")} ${skill.relatedProjects.join(" ")}`.toLowerCase();
      return categoryMatch && (!q || text.includes(q));
    });
  }, [category, query]);

  return (
    <SectionShell id="skills" title="Skills Explorer" subtitle="Searchable, typed skill map with related tools and projects.">
      <div className="mb-4 flex flex-wrap items-center gap-2">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="min-w-[220px] flex-1 rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-zinc-100"
          placeholder="Search skills"
        />
        <button
          type="button"
          onClick={() => {
            setQuery("");
            setCategory("All");
          }}
          className="rounded-md border border-zinc-700 px-3 py-2 text-sm text-zinc-200"
        >
          Reset
        </button>
      </div>
      <div className="mb-5 flex flex-wrap gap-2">
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

      {filtered.length === 0 ? (
        <p className="rounded-md border border-zinc-800 bg-zinc-900/30 p-5 text-zinc-300">No skills matched the current filters.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {filtered.map((skill) => (
            <article key={skill.id} className="rounded-lg border border-zinc-800 bg-zinc-900/35 p-4">
              <div className="mb-2 flex items-center justify-between gap-3">
                <h3 className="font-semibold text-zinc-100">{skill.name}</h3>
                <StatusBadge status={skill.status} />
              </div>
              <p className="text-sm text-zinc-300">{skill.description}</p>
              <p className="mt-2 text-xs text-zinc-400">{skill.category}</p>
              <p className="mt-3 text-xs text-zinc-400">Tools: {skill.relatedTools.join(" · ")}</p>
              <p className="mt-1 text-xs text-zinc-400">Projects: {skill.relatedProjects.join(" · ")}</p>
            </article>
          ))}
        </div>
      )}
    </SectionShell>
  );
}
