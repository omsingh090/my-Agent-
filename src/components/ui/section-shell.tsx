import { PropsWithChildren } from "react";

type SectionShellProps = PropsWithChildren<{
  id: string;
  title: string;
  subtitle?: string;
}>;

export function SectionShell({ id, title, subtitle, children }: SectionShellProps) {
  return (
    <section id={id} className="scroll-mt-24 border-t border-zinc-800/80 py-16 sm:py-20" aria-labelledby={`${id}-title`}>
      <div className="mx-auto w-full max-w-6xl px-5 sm:px-8">
        <div className="mb-8">
          <p className="font-mono text-xs uppercase tracking-[0.18em] text-cyan-300/80">{id.replace("-", " ")}</p>
          <h2 id={`${id}-title`} className="mt-2 text-2xl font-semibold text-zinc-100 sm:text-3xl">
            {title}
          </h2>
          {subtitle ? <p className="mt-3 max-w-3xl text-zinc-300">{subtitle}</p> : null}
        </div>
        {children}
      </div>
    </section>
  );
}
