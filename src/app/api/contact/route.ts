import { contactSchema } from "@/lib/contact-schema";
import { Resend } from "resend";
import { NextResponse } from "next/server";

type RateRecord = { count: number; resetAt: number };

const WINDOW_MS = 15 * 60 * 1000;
const LIMIT = 5;

const store = globalThis as typeof globalThis & { __contactRate?: Map<string, RateRecord> };
const rateMap = store.__contactRate ?? new Map<string, RateRecord>();
store.__contactRate = rateMap;

function getClientIp(request: Request) {
  const forwarded = request.headers.get("x-forwarded-for")?.split(",")[0]?.trim();
  return forwarded || "unknown";
}

function rateLimited(ip: string, now = Date.now()) {
  const current = rateMap.get(ip);

  if (!current || current.resetAt < now) {
    rateMap.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return false;
  }

  if (current.count >= LIMIT) {
    return true;
  }

  current.count += 1;
  rateMap.set(ip, current);
  return false;
}

export async function POST(request: Request) {
  const ip = getClientIp(request);

  if (rateLimited(ip)) {
    return NextResponse.json({ message: "Too many attempts. Please try again later." }, { status: 429 });
  }

  const parsed = contactSchema.safeParse(await request.json().catch(() => null));

  if (!parsed.success) {
    return NextResponse.json({ message: "Please check the form fields and try again." }, { status: 400 });
  }

  const apiKey = process.env.RESEND_API_KEY?.trim();
  const contactEmail = process.env.CONTACT_EMAIL?.trim();

  if (!apiKey || !contactEmail) {
    return NextResponse.json(
      {
        message:
          "Email delivery is not configured yet. Set RESEND_API_KEY and CONTACT_EMAIL. You can still use mailto or WhatsApp contact options.",
      },
      { status: 503 },
    );
  }

  const resend = new Resend(apiKey);

  try {
    await resend.emails.send({
      from: "Portfolio Contact <onboarding@resend.dev>",
      to: contactEmail,
      replyTo: parsed.data.email,
      subject: `[Portfolio] ${parsed.data.subject}`,
      text: `Name: ${parsed.data.name}\nEmail: ${parsed.data.email}\n\n${parsed.data.message}`,
    });

    return NextResponse.json({ message: "Message sent successfully." });
  } catch {
    return NextResponse.json(
      {
        message:
          "Message could not be delivered right now. Please retry shortly or use the fallback contact links.",
      },
      { status: 502 },
    );
  }
}
