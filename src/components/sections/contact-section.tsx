"use client";

import { SectionShell } from "@/components/ui/section-shell";
import { contactSchema, type ContactInput } from "@/lib/contact-schema";
import { getWhatsappHref } from "@/lib/config";
import { zodResolver } from "@hookform/resolvers/zod";
import { Mail, MessageCircle } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";

type ContactSectionProps = {
  linkedinUrl?: string;
  githubUrl?: string;
  publicContactEmail?: string;
};

export function ContactSection({ linkedinUrl, githubUrl, publicContactEmail }: ContactSectionProps) {
  const [serverMessage, setServerMessage] = useState<string | null>(null);
  const [sendState, setSendState] = useState<"idle" | "success" | "error">("idle");
  const whatsappHref = getWhatsappHref();

  const form = useForm<ContactInput>({
    resolver: zodResolver(contactSchema),
    defaultValues: { name: "", email: "", subject: "", message: "" },
  });

  const onSubmit = form.handleSubmit(async (values) => {
    setServerMessage(null);
    setSendState("idle");

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });

      const payload = (await response.json()) as { message?: string };

      if (!response.ok) {
        setSendState("error");
        setServerMessage(payload.message ?? "Unable to send message.");
        return;
      }

      setSendState("success");
      setServerMessage(payload.message ?? "Message sent.");
      form.reset();
    } catch {
      setSendState("error");
      setServerMessage("Network error while sending the form.");
    }
  });

  return (
    <SectionShell
      id="contact"
      title="Contact"
      subtitle="This form validates input and sends only when server configuration is present."
    >
      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <aside className="space-y-3 rounded-lg border border-zinc-800 bg-zinc-900/35 p-4 text-sm text-zinc-300">
          <p className="font-semibold text-zinc-100">Reach out</p>
          {publicContactEmail ? (
            <a className="inline-flex items-center gap-2 text-cyan-200" href={`mailto:${publicContactEmail}`}>
              <Mail className="h-4 w-4" /> {publicContactEmail}
            </a>
          ) : (
            <p className="text-zinc-400">Public contact email not configured (NEXT_PUBLIC_CONTACT_EMAIL).</p>
          )}
          {whatsappHref ? (
            <a href={whatsappHref} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 text-cyan-200">
              <MessageCircle className="h-4 w-4" /> WhatsApp
            </a>
          ) : (
            <p className="text-zinc-400">WhatsApp link disabled until NEXT_PUBLIC_WHATSAPP_NUMBER is set.</p>
          )}
          {linkedinUrl ? (
            <a href={linkedinUrl} target="_blank" rel="noreferrer" className="block text-cyan-200">
              LinkedIn
            </a>
          ) : null}
          {githubUrl ? (
            <a href={githubUrl} target="_blank" rel="noreferrer" className="block text-cyan-200">
              GitHub
            </a>
          ) : null}
        </aside>

        <form onSubmit={onSubmit} noValidate className="space-y-4 rounded-lg border border-zinc-800 bg-zinc-900/35 p-4">
          <div>
            <label htmlFor="contact-name" className="mb-1 block text-sm text-zinc-200">
              Name
            </label>
            <input
              id="contact-name"
              {...form.register("name")}
              className="w-full rounded-md border border-zinc-700 bg-zinc-950 px-3 py-2 text-zinc-100"
            />
            {form.formState.errors.name ? <p className="mt-1 text-xs text-rose-300">{form.formState.errors.name.message}</p> : null}
          </div>

          <div>
            <label htmlFor="contact-email" className="mb-1 block text-sm text-zinc-200">
              Email
            </label>
            <input
              id="contact-email"
              type="email"
              {...form.register("email")}
              className="w-full rounded-md border border-zinc-700 bg-zinc-950 px-3 py-2 text-zinc-100"
            />
            {form.formState.errors.email ? <p className="mt-1 text-xs text-rose-300">{form.formState.errors.email.message}</p> : null}
          </div>

          <div>
            <label htmlFor="contact-subject" className="mb-1 block text-sm text-zinc-200">
              Subject
            </label>
            <input
              id="contact-subject"
              {...form.register("subject")}
              className="w-full rounded-md border border-zinc-700 bg-zinc-950 px-3 py-2 text-zinc-100"
            />
            {form.formState.errors.subject ? <p className="mt-1 text-xs text-rose-300">{form.formState.errors.subject.message}</p> : null}
          </div>

          <div>
            <label htmlFor="contact-message" className="mb-1 block text-sm text-zinc-200">
              Message
            </label>
            <textarea
              id="contact-message"
              rows={6}
              {...form.register("message")}
              className="w-full rounded-md border border-zinc-700 bg-zinc-950 px-3 py-2 text-zinc-100"
            />
            {form.formState.errors.message ? <p className="mt-1 text-xs text-rose-300">{form.formState.errors.message.message}</p> : null}
          </div>

          <button
            type="submit"
            disabled={form.formState.isSubmitting}
            className="rounded-md bg-lime-300 px-4 py-2 text-sm font-medium text-zinc-950 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {form.formState.isSubmitting ? "Sending..." : "Send Message"}
          </button>

          {serverMessage ? (
            <p className={`text-sm ${sendState === "success" ? "text-lime-300" : "text-rose-300"}`}>{serverMessage}</p>
          ) : null}
          <p className="text-xs text-zinc-400">If email delivery is not configured, the API returns guidance without fake success.</p>
        </form>
      </div>
    </SectionShell>
  );
}
