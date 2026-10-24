"use client";

import { getResumeHref, getWhatsappHref, navSections } from "@/lib/config";
import { Menu, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

const labels: Record<(typeof navSections)[number], string> = {
  home: "Home",
  experience: "Experience",
  "ai-systems": "AI Systems",
  skills: "Skills",
  tools: "Tools",
  projects: "Projects",
  certifications: "Certifications",
  contact: "Contact",
};

export function SiteHeader() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [active, setActive] = useState<(typeof navSections)[number]>("home");
  const closeBtnRef = useRef<HTMLButtonElement>(null);
  const resumeHref = getResumeHref();
  const whatsappHref = getWhatsappHref();

  useEffect(() => {
    const observers = navSections.map((id) => {
      const section = document.getElementById(id);
      if (!section) return undefined;
      const observer = new IntersectionObserver(
        (entries) => {
          const entry = entries[0];
          if (entry?.isIntersecting) setActive(id);
        },
        { rootMargin: "-40% 0px -40% 0px", threshold: 0.1 },
      );
      observer.observe(section);
      return observer;
    });

    return () => observers.forEach((observer) => observer?.disconnect());
  }, []);

  useEffect(() => {
    if (!mobileOpen) return;
    closeBtnRef.current?.focus();
    const original = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = original;
    };
  }, [mobileOpen]);

  useEffect(() => {
    if (!mobileOpen) return;
    const onEsc = (event: KeyboardEvent) => {
      if (event.key === "Escape") setMobileOpen(false);
    };

    window.addEventListener("keydown", onEsc);
    return () => window.removeEventListener("keydown", onEsc);
  }, [mobileOpen]);

  return (
    <header className="sticky top-0 z-40 border-b border-zinc-800/80 bg-zinc-950/90 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-3 px-5 py-3 sm:px-8">
        <a href="#home" className="font-mono text-xs tracking-[0.16em] text-zinc-200">
          OM SINGH / AI SYSTEMS
        </a>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Primary">
          {navSections.map((section) => (
            <a
              key={section}
              href={`#${section}`}
              className={`rounded-md px-3 py-2 text-sm transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-lime-300 ${
                active === section ? "text-lime-300" : "text-zinc-300 hover:text-zinc-100"
              }`}
              aria-current={active === section ? "page" : undefined}
            >
              {labels[section]}
            </a>
          ))}
        </nav>

        <div className="hidden items-center gap-2 lg:flex">
          {whatsappHref ? (
            <a
              href={whatsappHref}
              target="_blank"
              rel="noreferrer"
              className="rounded-md border border-cyan-300/40 px-3 py-2 text-sm text-cyan-200 hover:bg-cyan-300/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-cyan-300"
            >
              Contact Shortcut
            </a>
          ) : null}
          <a
            href={resumeHref ?? "#contact"}
            target={resumeHref?.startsWith("http") ? "_blank" : undefined}
            rel={resumeHref?.startsWith("http") ? "noreferrer" : undefined}
            className={`rounded-md border px-3 py-2 text-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-lime-300 ${
              resumeHref
                ? "border-lime-300/40 text-lime-200 hover:bg-lime-300/10"
                : "border-zinc-700 text-zinc-400"
            }`}
            aria-disabled={!resumeHref}
          >
            Resume
          </a>
        </div>

        <button
          type="button"
          className="rounded-md border border-zinc-700 p-2 text-zinc-200 lg:hidden"
          onClick={() => setMobileOpen(true)}
          aria-label="Open menu"
          aria-expanded={mobileOpen}
          aria-controls="mobile-menu"
        >
          <Menu className="h-5 w-5" />
        </button>
      </div>

      {mobileOpen ? (
        <div id="mobile-menu" className="fixed inset-0 z-50 bg-zinc-950/95 p-5" role="dialog" aria-modal="true" aria-label="Mobile navigation">
          <div className="mb-5 flex items-center justify-between">
            <p className="text-sm font-semibold text-zinc-100">Navigate</p>
            <button
              ref={closeBtnRef}
              type="button"
              className="rounded-md border border-zinc-700 p-2 text-zinc-200"
              onClick={() => setMobileOpen(false)}
              aria-label="Close menu"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          <nav className="grid gap-2" aria-label="Mobile primary">
            {navSections.map((section) => (
              <a
                key={section}
                href={`#${section}`}
                onClick={() => setMobileOpen(false)}
                className={`rounded-md px-3 py-3 text-base ${active === section ? "bg-zinc-900 text-lime-300" : "text-zinc-200"}`}
                aria-current={active === section ? "page" : undefined}
              >
                {labels[section]}
              </a>
            ))}
          </nav>
        </div>
      ) : null}
    </header>
  );
}
