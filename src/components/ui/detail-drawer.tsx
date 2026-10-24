"use client";

import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { X } from "lucide-react";
import { PropsWithChildren, useEffect, useRef } from "react";

type DetailDrawerProps = PropsWithChildren<{
  title: string;
  open: boolean;
  onClose: () => void;
}>;

export function DetailDrawer({ title, open, onClose, children }: DetailDrawerProps) {
  const shouldReduceMotion = useReducedMotion();
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open || !panelRef.current) return;
    const target = panelRef.current.querySelector<HTMLElement>("button, a, input, textarea, [tabindex]");
    target?.focus();
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose, open]);

  return (
    <AnimatePresence>
      {open ? (
        <div className="fixed inset-0 z-50" role="dialog" aria-modal="true" aria-label={title}>
          <motion.button
            type="button"
            className="absolute inset-0 bg-black/70"
            onClick={onClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: shouldReduceMotion ? 0 : 0.2 }}
            aria-label="Close details"
          />
          <motion.div
            ref={panelRef}
            className="absolute right-0 top-0 h-full w-full max-w-2xl border-l border-zinc-700 bg-zinc-950 p-6 sm:p-8"
            initial={{ x: shouldReduceMotion ? 0 : "100%" }}
            animate={{ x: 0 }}
            exit={{ x: shouldReduceMotion ? 0 : "100%" }}
            transition={{ duration: shouldReduceMotion ? 0 : 0.25, ease: "easeOut" }}
          >
            <div className="mb-6 flex items-center justify-between">
              <h3 className="text-xl font-semibold text-zinc-100">{title}</h3>
              <button
                type="button"
                onClick={onClose}
                className="rounded-md border border-zinc-700 p-2 text-zinc-200 hover:bg-zinc-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-lime-300"
                aria-label="Close panel"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="space-y-6 overflow-y-auto pr-1 text-zinc-200">{children}</div>
          </motion.div>
        </div>
      ) : null}
    </AnimatePresence>
  );
}
