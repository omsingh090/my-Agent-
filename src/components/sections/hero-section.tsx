"use client";

import { aiNetworkNodes, profile } from "@/data/portfolio";
import { getResumeHref } from "@/lib/config";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { ArrowRight, Github, Linkedin } from "lucide-react";
import { useState } from "react";

type HeroSectionProps = {
  linkedinUrl?: string;
  githubUrl?: string;
};

export function HeroSection({ linkedinUrl, githubUrl }: HeroSectionProps) {
  const [activeNode, setActiveNode] = useState<(typeof aiNetworkNodes)[number]>(aiNetworkNodes[0]);
  const shouldReduceMotion = useReducedMotion();
  const resumeHref = getResumeHref();

  return (
    <section id="home" className="scroll-mt-24 border-b border-zinc-800/80 py-16 sm:py-20" aria-labelledby="home-title">
      <div className="mx-auto grid w-full max-w-6xl gap-10 px-5 sm:px-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-cyan-300">AI Engineer / Generative AI Engineer</p>
          <h1 id="home-title" className="mt-4 text-4xl font-semibold leading-tight text-zinc-100 sm:text-5xl">
            Building intelligent AI systems that connect research, retrieval, reasoning, and response.
          </h1>
          <p className="mt-6 max-w-2xl text-zinc-300">{profile.intro}</p>

          <div className="mt-8 flex flex-wrap gap-3">
            <a
              href="#projects"
              className="inline-flex items-center gap-2 rounded-md bg-lime-300 px-4 py-2 text-sm font-medium text-zinc-950 hover:bg-lime-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-lime-200"
            >
              Explore My Work <ArrowRight className="h-4 w-4" />
            </a>
            <a
              href="#contact"
              className="rounded-md border border-zinc-700 px-4 py-2 text-sm text-zinc-100 hover:border-zinc-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-cyan-300"
            >
              Contact Me
            </a>
            <a
              href={resumeHref ?? "#contact"}
              target={resumeHref?.startsWith("http") ? "_blank" : undefined}
              rel={resumeHref?.startsWith("http") ? "noreferrer" : undefined}
              className={`rounded-md border px-4 py-2 text-sm ${resumeHref ? "border-lime-300/40 text-lime-200" : "border-zinc-700 text-zinc-400"}`}
              aria-disabled={!resumeHref}
            >
              {resumeHref ? "View Resume" : "Resume not configured"}
            </a>
          </div>

          <div className="mt-8 flex flex-wrap items-center gap-3 text-sm text-zinc-300">
            {linkedinUrl ? (
              <a
                href={linkedinUrl}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 rounded-md border border-zinc-700 px-3 py-2 hover:border-zinc-500"
              >
                <Linkedin className="h-4 w-4" /> LinkedIn
              </a>
            ) : null}
            {githubUrl ? (
              <a
                href={githubUrl}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 rounded-md border border-zinc-700 px-3 py-2 hover:border-zinc-500"
              >
                <Github className="h-4 w-4" /> GitHub
              </a>
            ) : null}
            {!linkedinUrl && !githubUrl ? (
              <p className="font-mono text-xs text-zinc-400">Social links are editable via NEXT_PUBLIC_LINKEDIN_URL / NEXT_PUBLIC_GITHUB_URL.</p>
            ) : null}
          </div>
        </div>

        <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5">
          <p className="font-mono text-xs uppercase tracking-[0.16em] text-zinc-400">AI System Sketch (interactive)</p>
          <div className="mt-5 grid grid-cols-2 gap-3">
            {aiNetworkNodes.map((node) => (
              <button
                key={node.id}
                type="button"
                className={`rounded-md border p-3 text-left transition ${
                  activeNode.id === node.id ? "border-lime-300/50 bg-lime-300/10" : "border-zinc-700 hover:border-zinc-500"
                }`}
                onClick={() => setActiveNode(node)}
              >
                <p className="font-mono text-xs uppercase tracking-[0.14em] text-cyan-200">{node.label}</p>
              </button>
            ))}
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={activeNode.id}
              initial={shouldReduceMotion ? false : { opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={shouldReduceMotion ? undefined : { opacity: 0, y: -4 }}
              transition={{ duration: shouldReduceMotion ? 0 : 0.2 }}
              className="mt-4 rounded-md border border-cyan-300/30 bg-cyan-400/10 p-4"
            >
              <p className="font-semibold text-zinc-100">{activeNode.label}</p>
              <p className="mt-2 text-sm text-zinc-300">{activeNode.description}</p>
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}
