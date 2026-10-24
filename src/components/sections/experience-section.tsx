"use client";

import { experience, profile } from "@/data/portfolio";
import { statusLabel } from "@/lib/status";
import { ChevronDown } from "lucide-react";
import { useState } from "react";
import { SectionShell } from "@/components/ui/section-shell";

export function ExperienceSection() {
  const [openId, setOpenId] = useState<string | null>(experience[0]?.id ?? null);

  return (
    <SectionShell
      id="experience"
      title="Experience"
      subtitle={`${profile.experienceLabel}. Timeline intentionally keeps dates editable until confirmed.`}
    >
      <div className="space-y-4">
        {experience.map((item) => {
          const open = item.id === openId;
          return (
            <article key={item.id} className="rounded-lg border border-zinc-800 bg-zinc-900/35">
              <button
                type="button"
                className="flex w-full items-center justify-between gap-4 p-4 text-left"
                onClick={() => setOpenId(open ? null : item.id)}
                aria-expanded={open}
                aria-controls={`${item.id}-panel`}
              >
                <div>
                  <p className="font-semibold text-zinc-100">{item.role}</p>
                  <p className="mt-1 text-sm text-zinc-300">{item.organization}</p>
                  <p className="mt-1 font-mono text-xs text-zinc-400">{item.durationLabel}</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className="rounded-full border border-zinc-700 px-2 py-1 text-xs text-zinc-300">{statusLabel(item.status)}</span>
                  <ChevronDown className={`h-4 w-4 text-zinc-300 transition ${open ? "rotate-180" : ""}`} />
                </div>
              </button>
              {open ? (
                <div id={`${item.id}-panel`} className="space-y-4 border-t border-zinc-800 p-4 text-zinc-300">
                  <p>{item.summary}</p>
                  <ul className="list-disc space-y-1 pl-5 text-sm">
                    {item.highlights.map((point) => (
                      <li key={point}>{point}</li>
                    ))}
                  </ul>
                  <p className="font-mono text-xs text-cyan-300">Tech: {item.technologies.join(" · ")}</p>
                  {item.editableNotes ? <p className="text-xs text-zinc-400">{item.editableNotes}</p> : null}
                </div>
              ) : null}
            </article>
          );
        })}
      </div>
      <div className="mt-6 rounded-md border border-zinc-800 bg-zinc-900/30 p-4 text-sm text-zinc-300">
        <p>{profile.chatbotExperienceLabel}</p>
        <p className="mt-1">{profile.llmExperienceLabel}</p>
      </div>
    </SectionShell>
  );
}
