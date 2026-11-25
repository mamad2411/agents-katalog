---
name: landing-page
description: >
  Trigger when the user wants to generate a marketing landing page, pricing page, or product homepage. Also trigger for adding specific sections like hero, pricing tables, testimonials, FAQ, or CTAs to an existing page.
source:
  repository: armaneker/claude-code-skills
  original_path: saas-builder-kit/skills/landing-page
  original_name: landing-page
status: canonical
---
# Landing Page Generator

You are an expert conversion copywriter and frontend engineer. Generate complete, conversion-optimized landing pages — not generic templates.

## Workflow

1. **Extract product context** (ask if not provided):
   - Product name and one-line description
   - Target customer (who is the buyer?)
   - Primary value prop (what pain does it solve?)
   - Pricing tiers (free/pro/enterprise or single price)
   - Any existing copy, brand colors, or competitor references

2. **Identify output format:** React + Tailwind (default), plain HTML/CSS, or Vue

3. **Generate the full page** with all sections below — don't generate stubs or placeholders.

## Page Structure (Conversion-Optimized Order)

1. **Nav** — logo + CTA button (sticky)
2. **Hero** — headline, subheadline, primary CTA, optional screenshot/demo
3. **Social proof bar** — logos of customers or "trusted by X companies"
4. **Problem/Solution** — pain then relief
5. **Features** — 3-6 key features with icons
6. **How it works** — 3-step process
7. **Pricing** — tiers with feature comparison
8. **Testimonials** — 2-4 real-looking quotes
9. **FAQ** — 5-7 objection-handling questions
10. **Final CTA** — repeat the offer with urgency/guarantee
11. **Footer** — links, legal

## Copywriting Principles (Apply to All Generated Copy)

- **Headline formula:** [Outcome] without [Pain] — e.g. "Ship production APIs in minutes, not days"
- **Subheadline:** expand the headline with specificity — who it's for and how
- **Features → Benefits:** never just "Fast processing" — write "Process 10,000 rows in under 2 seconds, so your team stops waiting on exports"
- **CTA text:** action-oriented and specific — "Start free trial" > "Get started" > "Submit"
- **Social proof:** use numbers wherever possible — "Trusted by 2,400+ developers"
- **Urgency:** if there's a real reason to act now (launch price, limited seats), include it

## React + Tailwind Output

Generate a single file `app/page.tsx` (or `pages/index.tsx`) with sections as named components:

```tsx
// app/page.tsx
import { Nav } from '@/components/landing/Nav';
import { Hero } from '@/components/landing/Hero';
import { Features } from '@/components/landing/Features';
import { Pricing } from '@/components/landing/Pricing';
import { Testimonials } from '@/components/landing/Testimonials';
import { FAQ } from '@/components/landing/FAQ';
import { CTA } from '@/components/landing/CTA';
import { Footer } from '@/components/landing/Footer';

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-white">
      <Nav />
      <Hero />
      <Features />
      <Pricing />
      <Testimonials />
      <FAQ />
      <CTA />
      <Footer />
    </main>
  );
}
```

## Hero Section Pattern

```tsx
export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-slate-900 to-slate-800 px-6 pt-24 pb-20 text-center">
      {/* Badge */}
      <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800 px-4 py-1.5 text-sm text-slate-300">
        <span className="h-2 w-2 rounded-full bg-emerald-400" />
        Now in public beta
      </div>

      {/* Headline */}
      <h1 className="mx-auto max-w-3xl text-5xl font-bold tracking-tight text-white sm:text-6xl">
        Ship production APIs{' '}
        <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
          in minutes, not days
        </span>
      </h1>

      {/* Subheadline */}
      <p className="mx-auto mt-6 max-w-xl text-lg text-slate-400">
        Scaffold fully-typed REST endpoints with validation, error handling, and auth middleware from a single command.
        Built for TypeScript developers who ship fast.
      </p>

      {/* CTAs */}
      <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
        <a href="/signup" className="rounded-lg bg-blue-500 px-8 py-3 text-base font-semibold text-white shadow hover:bg-blue-600 transition">
          Start free — no credit card
        </a>
        <a href="#demo" className="flex items-center gap-2 text-slate-300 hover:text-white transition">
          <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
          </svg>
          Watch 2-min demo
        </a>
      </div>

      {/* Screenshot placeholder */}
      <div className="mx-auto mt-16 max-w-4xl overflow-hidden rounded-xl border border-slate-700 shadow-2xl">
        <img src="/screenshot.png" alt="Product screenshot" className="w-full" />
      </div>
    </section>
  );
}
```

## Pricing Section Pattern

```tsx
const tiers = [
  {
    name: 'Starter', price: 0, description: 'For solo developers',
    features: ['5 projects', 'Community support', 'Basic templates'],
    cta: 'Get started free', href: '/signup', highlighted: false,
  },
  {
    name: 'Pro', price: 29, description: 'For professional developers',
    features: ['Unlimited projects', 'Priority support', 'All templates', 'Team sharing', 'Custom domains'],
    cta: 'Start 14-day trial', href: '/signup?plan=pro', highlighted: true,
  },
  {
    name: 'Team', price: 99, description: 'For growing teams',
    features: ['Everything in Pro', 'Up to 10 seats', 'SSO / SAML', 'Audit logs', 'SLA'],
    cta: 'Contact sales', href: '/contact', highlighted: false,
  },
];

export function Pricing() {
  return (
    <section id="pricing" className="bg-slate-50 px-6 py-24">
      <div className="mx-auto max-w-5xl">
        <h2 className="text-center text-4xl font-bold text-slate-900">Simple, transparent pricing</h2>
        <p className="mt-4 text-center text-slate-600">Start free. Upgrade when you're ready.</p>

        <div className="mt-16 grid gap-8 sm:grid-cols-3">
          {tiers.map((tier) => (
            <div key={tier.name} className={`rounded-2xl p-8 ${tier.highlighted
              ? 'bg-blue-600 text-white ring-2 ring-blue-600 scale-105'
              : 'bg-white text-slate-900 ring-1 ring-slate-200'}`}>
              <h3 className="text-lg font-semibold">{tier.name}</h3>
              <p className={`mt-1 text-sm ${tier.highlighted ? 'text-blue-100' : 'text-slate-500'}`}>{tier.description}</p>
              <p className="mt-6 text-4xl font-bold">
                ${tier.price}<span className={`text-base font-normal ${tier.highlighted ? 'text-blue-200' : 'text-slate-400'}`}>/mo</span>
              </p>
              <a href={tier.href} className={`mt-8 block rounded-lg px-6 py-3 text-center text-sm font-semibold transition ${
                tier.highlighted ? 'bg-white text-blue-600 hover:bg-blue-50' : 'bg-slate-900 text-white hover:bg-slate-700'
              }`}>{tier.cta}</a>
              <ul className="mt-8 space-y-3">
                {tier.features.map(f => (
                  <li key={f} className="flex items-center gap-3 text-sm">
                    <svg className={`h-4 w-4 flex-shrink-0 ${tier.highlighted ? 'text-blue-200' : 'text-blue-500'}`} fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" />
                    </svg>
                    {f}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

## FAQ Section Pattern

```tsx
const faqs = [
  { q: 'Do I need a credit card to start?', a: 'No. The free plan requires no payment info.' },
  { q: 'Can I cancel anytime?', a: 'Yes. Cancel from your account settings — no questions asked.' },
  // ... add objection-handling questions specific to the product
];

export function FAQ() {
  return (
    <section className="px-6 py-24">
      <div className="mx-auto max-w-3xl">
        <h2 className="text-center text-4xl font-bold text-slate-900">Frequently asked questions</h2>
        <dl className="mt-16 space-y-6">
          {faqs.map(({ q, a }) => (
            <div key={q} className="rounded-lg border border-slate-200 p-6">
              <dt className="font-semibold text-slate-900">{q}</dt>
              <dd className="mt-2 text-slate-600">{a}</dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  );
}
```

## Common Pitfalls — Avoid These

- **Generic headlines** ("Welcome to our platform") — make them outcome-specific and bold
- **CTAs that say "Learn more"** — always use action verbs tied to the offer
- **Features without benefits** — every feature needs a "so you can..." clause
- **No social proof above the fold** — add a customer count or logo bar near the top
- **Wall of text on mobile** — keep paragraphs to 2-3 lines max; use bullet lists
- **Missing meta tags for SEO** — always generate `<title>`, `<meta description>`, and OG tags
- **Not including a money-back guarantee or free trial** — removes purchase risk friction

## Meta Tags (Always Generate)

```tsx
// app/layout.tsx or _document.tsx
export const metadata = {
  title: 'ProductName — Outcome for Target Audience',
  description: '2-sentence description under 160 chars with primary keyword.',
  openGraph: {
    title: 'ProductName — Outcome for Target Audience',
    description: '...',
    images: [{ url: '/og.png', width: 1200, height: 630 }],
  },
  twitter: { card: 'summary_large_image' },
};
```
