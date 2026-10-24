# Om Singh — AI Engineer Portfolio (Next.js)

This repository now includes a production-ready interactive portfolio web app for **Om Singh (AI Engineer / Generative AI Engineer)** while preserving the original Python codebase.

## Overview

The portfolio is built with:
- Next.js App Router
- Strict TypeScript
- Tailwind CSS
- Motion for React
- Lucide React
- React Hook Form + Zod
- Resend (optional contact email delivery)

It includes:
- Responsive section navigation (Home, Experience, AI Systems, Skills, Tools, Projects, Certifications, Contact)
- Interactive AI systems explorer, tools toolbox, skills explorer, and project gallery
- Honest placeholder handling for unverified details
- Contact form with server-side validation and rate limiting
- Conditional social/WhatsApp/resume actions
- SEO basics (metadata, robots, sitemap, not-found route)

## Repository Structure

```text
src/
  app/
    api/contact/route.ts
    globals.css
    icon.svg
    layout.tsx
    not-found.tsx
    page.tsx
    robots.ts
    sitemap.ts
  components/
    layout/site-header.tsx
    sections/*.tsx
    ui/*.tsx
  data/portfolio.ts
  lib/*.ts
  types/portfolio.ts

public/
  certificates/
  images/
  resume/

# Legacy Python code is preserved under existing src/*.py modules and tests/
```

## Prerequisites

- Node.js 20+ (tested with Node 22)
- npm 10+

## Install

```bash
npm install
```

## Development

```bash
npm run dev
```

Open http://localhost:3000.

## Build & Run

```bash
npm run lint
npm run build
npm run start
```

## Environment Setup

Copy the template:

```bash
cp .env.example .env.local
```

### Required for email delivery
- `RESEND_API_KEY`
- `CONTACT_EMAIL`

If these are missing, the contact API returns a truthful configuration message (no fake success).

### Public configuration
- `NEXT_PUBLIC_SITE_URL`
- `NEXT_PUBLIC_LINKEDIN_URL`
- `NEXT_PUBLIC_GITHUB_URL`
- `NEXT_PUBLIC_WHATSAPP_NUMBER` (digits only)
- `NEXT_PUBLIC_CONTACT_EMAIL` (optional display)
- `NEXT_PUBLIC_RESUME_PATH` or `NEXT_PUBLIC_RESUME_URL`
- `NEXT_PUBLIC_OG_IMAGE_URL` (optional)

## Updating Portfolio Content

Edit centralized data in:
- `src/data/portfolio.ts`

This file controls:
- Profile summary
- Experience timeline
- AI systems entries
- Skills explorer
- Tools toolbox
- Projects
- Certifications

Keep unverified details marked as draft/placeholder until confirmed.

## Resume Setup

### Local PDF
1. Put your file in `public/resume/` (example: `public/resume/om-singh-resume.pdf`)
2. Set `NEXT_PUBLIC_RESUME_PATH=/resume/om-singh-resume.pdf`

### Hosted URL
Set `NEXT_PUBLIC_RESUME_URL=https://...`

If neither is set, Resume buttons stay disabled with explanatory text.

## Contact + WhatsApp

- WhatsApp link is generated only when `NEXT_PUBLIC_WHATSAPP_NUMBER` is valid digits.
- Contact form posts to `src/app/api/contact/route.ts`.
- Server validates using Zod and applies a simple IP-based rate limit.

## Deployment (Vercel)

1. Import repository in Vercel
2. Set all required environment variables in Vercel project settings
3. Deploy

## Troubleshooting

- **Form says email not configured**: set `RESEND_API_KEY` and `CONTACT_EMAIL`
- **Resume button disabled**: set `NEXT_PUBLIC_RESUME_PATH` or `NEXT_PUBLIC_RESUME_URL`
- **WhatsApp button missing**: ensure digits-only number in `NEXT_PUBLIC_WHATSAPP_NUMBER`
- **Missing social links**: add `NEXT_PUBLIC_LINKEDIN_URL` / `NEXT_PUBLIC_GITHUB_URL`

## Notes

- No fake testimonials, metrics, credentials, or links are included.
- Legacy Python artifacts remain intact in the repository and are not deleted.
