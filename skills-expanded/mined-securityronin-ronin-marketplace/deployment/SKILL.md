---
name: deployment
description: Use when deploying applications, choosing deployment platforms, or troubleshooting deployment issues - routes to platform-specific skills (Vercel, Fly.io, Cloudflare)
---

# Deployment Router

Quick guide to choose the right deployment platform and skill for your workload.

## Platform Decision Matrix

| Workload | Platform | Skill |
|----------|----------|-------|
| Next.js / React frontend | **Vercel** | `vercel-deployment` |
| Static sites, SPAs | **Vercel** or **Cloudflare Pages** | `vercel-deployment` |
| FastAPI / Python backend | **Fly.io** | `fly-deployment` |
| Stateful backend (SQLite, volumes) | **Fly.io** | `fly-deployment` |
| Docker containers | **Fly.io** | `fly-deployment` |
| Object storage / CDN | **Cloudflare R2** | `cloudflare-r2-d1` |
| Edge database (SQLite) | **Cloudflare D1** | `cloudflare-r2-d1` |
| Session/config caching | **Cloudflare KV** | `cloudflare-r2-d1` |
| Serverless functions | **Cloudflare Workers** | `cloudflare-r2-d1` |

---

## Quick Reference by Stack

### Full-Stack Next.js + Python API
```
Frontend (Next.js)     → Vercel       → vercel-deployment
Backend (FastAPI)      → Fly.io       → fly-deployment
File uploads           → Cloudflare R2 or Fly volume
```

### Edge-First Stack (Cloudflare)
```
Frontend (static/SPA)  → Cloudflare Pages
API (Workers)          → Cloudflare Workers  → cloudflare-r2-d1
Database               → Cloudflare D1       → cloudflare-r2-d1
Files                  → Cloudflare R2       → cloudflare-r2-d1
```

### Monorepo Pattern
```
apps/web (Next.js)     → Vercel       → vercel-deployment
apps/api (FastAPI)     → Fly.io       → fly-deployment
```

---

## Platform Strengths

### Vercel
- Zero-config Next.js deployment
- Preview deployments per PR
- Edge functions & middleware
- Automatic HTTPS & CDN

**Best for:** Next.js, React, static sites

### Fly.io
- Run any Docker container
- Persistent volumes (SQLite, file storage)
- Multiple regions with data locality
- WebSocket support

**Best for:** Python backends, stateful apps, containers

### Cloudflare
- Edge-first (runs in 300+ cities)
- No cold starts (Workers)
- Integrated storage (R2, D1, KV)
- Zero egress fees on R2

**Best for:** Low-latency APIs, edge computing, global scale

---

## Common Deployment Patterns

### Pattern 1: Vercel + Fly.io
```
User → Vercel (frontend) → Fly.io (API) → SQLite (volume)
```

Deploy commands:
```bash
# Frontend
vercel --prod

# Backend
fly deploy
```

### Pattern 2: Full Cloudflare
```
User → Pages (frontend) → Workers (API) → D1 (database) + R2 (files)
```

Deploy command:
```bash
wrangler deploy
```

### Pattern 3: Hybrid (Vercel + Cloudflare Storage)
```
User → Vercel (Next.js) → Cloudflare R2 (uploads) + external DB
```

---

## Troubleshooting Quick Links

| Issue | Check Skill |
|-------|-------------|
| Vercel deployment issues | `vercel-deployment` |
| Docker build fails | `fly-deployment` |
| Volume mount error | `fly-deployment` |
| D1 query timeout | `cloudflare-r2-d1` |
| R2 upload fails | `cloudflare-r2-d1` |

---

## Cost Comparison (Free Tiers)

| Platform | Free Tier Highlights |
|----------|---------------------|
| **Vercel** | 100GB bandwidth, serverless functions, preview deploys |
| **Fly.io** | 3 VMs (256MB), 3GB storage, 160GB bandwidth |
| **Cloudflare** | 100K Worker requests/day, 10GB R2, 5GB D1 |

---

## When to Use Each Skill

**Use `vercel-deployment` when:**
- Deploying Next.js or React apps
- Configuring vercel.json
- Setting environment variables
- Troubleshooting build errors

**Use `fly-deployment` when:**
- Writing Dockerfiles for Fly.io
- Configuring fly.toml
- Setting up volumes or persistent storage
- Deploying Python/FastAPI backends

**Use `cloudflare-r2-d1` when:**
- Storing files in R2
- Working with D1 SQLite database
- Caching with KV
- Writing Cloudflare Workers
