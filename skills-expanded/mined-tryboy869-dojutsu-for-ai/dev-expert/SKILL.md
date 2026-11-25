---
name: dev-expert
description: "Apply this skill whenever generating code, projects, or technical architectures. Forces the AI to think like an accomplished full stack developer BEFORE writing any code."
---

# DEV EXPERT — Full Stack Developer Mindset

## Core Rule: Understand → Architect → Code (never the reverse)

## Domain Identification
SaaS | E-commerce | Portfolio | API | AI App | Dashboard | Internal Tool
Sub-domains: auth, payments, search, files, realtime, email

## Stack Selection Criteria (in order)
1. Maintainability 2. Domain fit 3. Performance 4. Scale 5. TTM

**Recommended stacks:**
- Portfolio → HTML/CSS vanilla or Astro (NEVER React SPA for static)
- SaaS → Next.js + TailwindCSS + Fastify + PostgreSQL + Redis
- API → FastAPI (Python) or Hono/Fastify (Node, NOT Express in 2025)
- DB default → PostgreSQL. Cache → Redis. ORM → Drizzle or SQLAlchemy 2.0

## Architecture
- < 10k users: Modular monolith (no premature microservices)
- 10k-1M: Domain-driven modules
- > 1M: Justified microservices + event-driven

## Security (NON-NEGOTIABLE)
1. Input validation everywhere (Zod/Pydantic)
2. Secrets in env vars ONLY
3. ORM/parameterized queries (no SQL concatenation)
4. Rate limiting on all public routes
5. CSP, HSTS, X-Frame-Options headers

## SEO (if applicable)
- Unique <title> + <meta description> per page
- LCP < 2.5s, CLS < 0.1
- sitemap.xml, robots.txt, canonical URLs, JSON-LD

## Forbidden patterns
❌ Hardcoded secrets ❌ SELECT * without LIMIT ❌ .env in git
❌ "Security later" ❌ Deploy without tests ❌ Framework by trend
