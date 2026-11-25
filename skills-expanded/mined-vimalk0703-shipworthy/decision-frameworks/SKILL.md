---
name: decision-frameworks
description: Guides non-technical users through technology choices with opinionated defaults. Recommends one option for Builder-tier users, presents comparisons for Engineer-tier users. Covers databases, hosting, payments, auth, email, and build-vs-buy decisions.
invoke_when: Use when choosing a database, hosting provider, payment processor, auth solution, email service, or any technology component, including build-vs-buy decisions.
---

# Decision Frameworks

## Core Principle

**If it's not your competitive advantage, buy it.**

Your app's value is what it does differently. Authentication, email delivery, payment processing, hosting infrastructure — none of these are what makes your product special. Use proven services for these and spend your time on what matters.

## How This Skill Works by Tier

- **Builder-tier:** You get ONE recommendation with a brief "why." No comparison tables, no tradeoff analysis. The recommendation is the one that gets you shipping fastest with the least regret.
- **Engineer-tier:** You get a comparison with tradeoffs so you can make an informed choice. The recommendation is still highlighted, but alternatives are presented with honest pros and cons.

---

## Database

### Recommendation: Supabase

**Builder-tier response:** "Use Supabase. It gives you a Postgres database, authentication, and real-time subscriptions in one service. Free tier is generous. You'll set it up in 10 minutes."

**Why Supabase is the default:**
- Real Postgres database (not a proprietary format — your data is portable)
- Auth built in (one less service to manage)
- Real-time subscriptions included
- Row-level security for fine-grained permissions
- Generous free tier (500MB database, 50K monthly active users on auth)
- Dashboard for viewing and editing data without writing queries

### Engineer-Tier Comparison

| Factor | Supabase | Firebase | PlanetScale | Raw Postgres |
|--------|----------|----------|-------------|-------------|
| **Database type** | Postgres (relational) | Firestore (document/NoSQL) | MySQL (relational) | Postgres (relational) |
| **Auth included** | Yes | Yes | No | No |
| **Real-time** | Yes | Yes | No | Requires setup |
| **Free tier** | 500MB, 2 projects | Spark plan (generous) | 5GB, 1B row reads/mo | Self-host only |
| **Vendor lock-in** | Low (standard Postgres) | High (proprietary) | Medium (MySQL-compatible) | None |
| **Complexity** | Low | Low-Medium | Low | High |
| **Best for** | Most projects | Mobile-first apps, Google ecosystem | High-scale MySQL workloads | Full control needed |
| **Avoid when** | Need NoSQL document model | Need relational data, complex queries | Need built-in auth | Want managed service |

**When to NOT use Supabase:**
- You're deep in the Google/Firebase ecosystem already
- You specifically need a document database (rare for most apps)
- You need MySQL specifically (PlanetScale)
- You have regulatory requirements that mandate self-hosted databases

---

## Hosting

### Recommendation: Vercel (for Next.js), Railway (for anything else)

**Builder-tier response:** "If you're using Next.js, deploy on Vercel — it's made by the same team. Push your code to GitHub, connect Vercel, and you're live. For anything else (Python, Node backends, etc.), use Railway — same idea, works with everything."

**Why Vercel is the default for Next.js:**
- Made by the creators of Next.js (best possible integration)
- Git push to deploy (no configuration needed)
- Automatic preview deployments for every branch
- Edge functions and serverless built in
- Free tier handles most early-stage projects
- Custom domains with automatic HTTPS

### Engineer-Tier Comparison

| Factor | Vercel | Netlify | Railway | AWS |
|--------|--------|---------|---------|-----|
| **Best for** | Next.js, React | Static sites, Jamstack | Full-stack, backends | Everything (at a cost) |
| **Deploy method** | Git push | Git push | Git push | Many options, all complex |
| **Free tier** | 100GB bandwidth | 100GB bandwidth | $5/mo credit | 12-month free tier (limited) |
| **Serverless** | Built-in | Built-in (Functions) | Not serverless (containers) | Lambda (complex setup) |
| **Custom domains** | Easy + auto HTTPS | Easy + auto HTTPS | Easy + auto HTTPS | Route 53 (complex) |
| **Backend support** | API routes, serverless | Functions only | Full containers | Everything |
| **Complexity** | Low | Low | Low-Medium | High |
| **Scaling cost** | Can spike unexpectedly | Predictable | Predictable | Pay-per-use (complex billing) |
| **Avoid when** | Not using React/Next.js | Need persistent backend | Need edge computing | Want simplicity |

**When to NOT use Vercel:**
- You're not using Next.js or React (use Railway or Netlify instead)
- You need a persistent backend process (WebSocket server, cron jobs) — use Railway
- You need full infrastructure control — use AWS (but really consider if you do)
- Budget-sensitive and traffic is unpredictable — Vercel can surprise you on cost

---

## Payments

### Recommendation: Stripe Checkout

**Builder-tier response:** "Use Stripe Checkout. It handles the entire payment flow — card forms, validation, receipts, subscriptions — all hosted by Stripe so you don't touch sensitive payment data. You'll be taking payments in an afternoon."

**Why Stripe Checkout is the default:**
- Pre-built payment UI (no need to design card forms)
- PCI compliance handled for you (critical — you don't want to handle card data)
- Subscriptions, one-time payments, usage-based billing all supported
- 40+ payment methods (cards, Apple Pay, Google Pay, bank transfers)
- Excellent documentation and developer experience
- Test mode for development (no real charges)

### Engineer-Tier Comparison

| Factor | Stripe Checkout | Lemon Squeezy | Paddle |
|--------|----------------|---------------|--------|
| **Fee** | 2.9% + 30c (US) | 5% + 50c | 5% + 50c |
| **Merchant of Record** | You | Lemon Squeezy | Paddle |
| **Sales tax handling** | You manage (or use Stripe Tax) | Included | Included |
| **Global tax compliance** | Add-on (Stripe Tax) | Built-in | Built-in |
| **Best for** | SaaS, e-commerce, marketplaces | Digital products, SaaS | SaaS, digital products |
| **Subscription management** | Yes (Billing) | Yes | Yes |
| **Setup complexity** | Low-Medium | Low | Low |
| **Payout** | 2-day rolling | Monthly | Monthly |

**Merchant of Record explained (plain language):** When Stripe processes a payment, YOU are the seller — you handle refund disputes, tax collection, and legal compliance in every country. When Lemon Squeezy or Paddle process a payment, THEY are the seller — they handle taxes and compliance for you, but take a bigger cut and pay you monthly. If you sell globally and don't want to deal with VAT/GST in 40 countries, Lemon Squeezy or Paddle earn their higher fee.

**When to NOT use Stripe:**
- You sell digital products globally and don't want to handle international tax compliance — use Lemon Squeezy or Paddle
- Your primary market is outside the US/EU and Stripe isn't available — check Paddle's country support
- You want the absolute simplest setup for a digital product — Lemon Squeezy is slightly simpler

---

## Authentication

### Recommendation: Built-In (Supabase Auth if using Supabase, NextAuth if using Next.js without Supabase)

**Builder-tier response:** "If you're using Supabase, use Supabase Auth — it's already there, no extra setup. If you're using Next.js without Supabase, use NextAuth. Both give you email/password and social logins with minimal configuration."

**Why built-in auth is the default:**
- No additional service to manage or pay for
- Already integrated with your stack
- Handles the common cases (email/password, Google, GitHub sign-in)
- Free at the scale most projects need

### Engineer-Tier Comparison

| Factor | Supabase Auth | NextAuth (Auth.js) | Clerk | Auth0 |
|--------|--------------|-------------------|-------|-------|
| **Cost** | Free (included with Supabase) | Free (open source) | Free up to 10K MAU | Free up to 7.5K MAU |
| **Social logins** | Google, GitHub, Apple, etc. | 60+ providers | Google, GitHub, Apple, etc. | 60+ providers |
| **Email/password** | Yes | Yes (with adapter) | Yes | Yes |
| **MFA** | Yes | Manual implementation | Yes | Yes |
| **Pre-built UI** | Basic | None (you build it) | Beautiful, drop-in | Universal Login (hosted) |
| **User management dashboard** | Yes (in Supabase) | No | Yes (excellent) | Yes |
| **Complexity** | Low | Medium | Low | Medium-High |
| **Best for** | Supabase projects | Next.js, full control | Beautiful UI, fast setup | Enterprise requirements |
| **Avoid when** | Not using Supabase | Want pre-built UI | Budget-sensitive at scale | Want simplicity |

**When to NOT use built-in auth:**
- You need a beautiful, pre-built sign-in UI with minimal effort — use Clerk
- You have enterprise requirements (SAML, SSO, compliance) — use Auth0
- You need advanced user management features — use Clerk or Auth0

---

## Email

### Recommendation: Resend

**Builder-tier response:** "Use Resend for sending emails (welcome emails, password resets, notifications). It's simple, reliable, and the free tier covers most early-stage needs. You'll have it working in 15 minutes."

**Why Resend is the default:**
- Simple API (one function call to send an email)
- React Email integration (write emails as React components)
- Free tier: 3,000 emails/month, 100/day
- Excellent developer experience
- Built-in email verification and deliverability
- Modern dashboard with delivery tracking

### Engineer-Tier Comparison

| Factor | Resend | SendGrid | AWS SES |
|--------|--------|----------|---------|
| **Free tier** | 3K/month | 100/day (forever free) | 62K/month (if sent from EC2) |
| **Cost after free** | $20/mo for 50K | $19.95/mo for 50K | $0.10 per 1K emails |
| **DX (developer experience)** | Excellent | Good | Functional |
| **React Email support** | Native | No | No |
| **Setup complexity** | Very low | Low | Medium |
| **Deliverability** | High | High | High (requires setup) |
| **Dashboard** | Modern, clean | Feature-rich | Basic |
| **Best for** | Most projects | High volume, marketing | Very high volume, cost-sensitive |
| **Avoid when** | Sending 1M+/month | Want modern DX | Want simplicity |

**When to NOT use Resend:**
- You're sending 100K+ emails/month and cost matters — use AWS SES
- You need advanced marketing features (A/B testing, automation) — use SendGrid
- You're already deep in the AWS ecosystem — use SES

---

## Build vs Buy Framework

When deciding whether to build something yourself or use a service:

### Buy It (Use a Service) When:
- It's not your competitive advantage (auth, payments, email, hosting)
- The problem is well-solved by existing services
- Security is critical (payments, auth) — battle-tested services have security teams you don't
- You need it to work NOW, not after weeks of building
- The service has a free tier that covers your current needs

### Build It When:
- It IS your competitive advantage (the core thing that makes your product unique)
- No existing service fits your specific requirements
- You need full control over the user experience and no service offers enough customization
- The build is small and well-understood (a utility function, not an infrastructure component)
- Vendor lock-in is a real concern for your specific situation

### The Litmus Test
Ask: "If this component breaks at 3 AM, do I want to fix it myself or do I want someone else's on-call team to fix it?"

If the answer is "someone else" — buy it.

### Common Mistakes
- Building auth from scratch "for learning" in a production app (use a service, learn on a side project)
- Building a custom CMS when WordPress or a headless CMS would work
- Building an email sending system instead of using Resend/SendGrid
- Building a deployment pipeline instead of using Vercel/Railway
- Building analytics instead of using Plausible/PostHog

**The time you spend building commodity infrastructure is time you're NOT spending on what makes your product special.**
