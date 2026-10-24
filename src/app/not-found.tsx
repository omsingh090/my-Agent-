import Link from "next/link";

export default function NotFound() {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col items-center justify-center px-6 text-center">
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-cyan-300">404</p>
      <h1 className="mt-4 text-3xl font-semibold text-zinc-100">Page not found</h1>
      <p className="mt-3 text-zinc-300">The page you requested does not exist in this portfolio.</p>
      <Link href="/" className="mt-6 rounded-md border border-zinc-700 px-4 py-2 text-zinc-100">
        Return home
      </Link>
    </main>
  );
}
