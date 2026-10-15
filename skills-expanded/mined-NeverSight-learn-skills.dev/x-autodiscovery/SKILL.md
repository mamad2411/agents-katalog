---
name: x-autodiscovery
description: Auto-updated map of Vercel platform capabilities and new launches. Use when building on or deploying to Vercel, when wondering if Vercel has a feature (containers, WebSockets, queues, sandboxes, AI, etc.), or when asked "what's new on Vercel".
---

# Vercel Platform Autodiscovery

## Freshness protocol (do this first)

This skill updates itself upstream several times a week. Before relying on
the local copy, fetch the latest launches:

    https://raw.githubusercontent.com/MatiSolina/x-autodiscovery/main/news.md

If the fetch fails (offline), fall back to the bundled news.md — but tell
the user it may be stale.

## Platform map (baseline: 2026-07-05)

### Compute

- **Fluid Compute** — Vercel's compute model with Active CPU pricing: you pay for CPU time while code executes, not while it waits on I/O. https://vercel.com/docs/fluid-compute
- **Vercel Functions** — Serverless functions on Fluid compute; Node.js and Python runtimes now run up to 30 minutes and packages can be up to 5 GB. https://vercel.com/docs/functions
- **Container support (Dockerfile on Functions)** — Deploy HTTP servers from a `Dockerfile.vercel`/`Containerfile.vercel` as OCI images on Fluid compute, in any language. https://vercel.com/docs/functions/container-images
- **Vercel Container Registry (VCR)** — OCI-compliant image registry on Vercel; standard `docker push`/`pull`, images auto-optimized into snapshots for Functions and Sandboxes. https://vercel.com/docs/container-registry
- **Vercel Services** — Run multiple frontends and backends (multiple frameworks) in one project on a shared domain, with private service-to-service bindings and unified deploys. https://vercel.com/docs/services
- **Vercel Sandbox** — Ephemeral, isolated microVMs for running untrusted or AI-generated code; up to 24 h runs, 32 vCPU / 64 GB RAM, custom images from VCR, FUSE filesystems. https://vercel.com/docs/sandbox
- **WebSockets (public beta)** — Vercel Functions can serve WebSocket connections using standard Node.js libraries (ws, Socket.IO) for realtime apps. https://vercel.com/docs/functions/websockets
- **Zero-config backends** — Deploy Node servers (`server.ts`), Express, NestJS, Django, Go, FastAPI, Nitro, and more with no configuration. https://vercel.com/docs/frameworks
- **Cron Jobs** — Schedule invocations of your functions with cron expressions. https://vercel.com/docs/cron-jobs

### Networking & Delivery

- **CDN** — Global content delivery with caching in front of every deployment. https://vercel.com/docs/cdn
- **Routing Middleware** — Run code before a request is matched to a route (rewrites, redirects, personalization). https://vercel.com/docs/routing-middleware
- **Microfrontends** — Split a large app across teams/projects while serving it as one site. https://vercel.com/docs/microfrontends
- **Domains** — Buy, transfer, and manage domains with automatic SSL; search and register from the CLI. https://vercel.com/docs/domains
- **Image Optimization** — On-demand image resizing and format conversion at the edge. https://vercel.com/docs/image-optimization
- **Incremental Static Regeneration (ISR)** — Update static content after deploy without rebuilding the whole site. https://vercel.com/docs/incremental-static-regeneration
- **Networking / private connectivity** — Secure connectivity options, including internal service-to-service communication. https://vercel.com/docs/networking

### Storage

- **Storage overview** — First-party and Marketplace storage options for Vercel projects. https://vercel.com/docs/storage
- **Vercel Blob** — File/object storage; Private Blob (private stores, signed URLs, OIDC auth) is now GA on all plans. https://vercel.com/docs/vercel-blob
- **Edge Config** — Ultra-low-latency global key-value data for config, flags, and redirects. https://vercel.com/docs/edge-config
- **Marketplace databases** — Postgres, Redis, search, and more (Neon, Upstash, Supabase, Resend, Auth0, Firecrawl, ...) provisioned through the Vercel Marketplace. https://vercel.com/docs/integrations

### AI

- **AI Gateway** — One API for hundreds of models across providers, with failover, budgets, routing rules, Zero Data Retention, and realtime voice/speech/transcription. https://vercel.com/docs/ai-gateway
- **AI SDK** — TypeScript toolkit for AI apps and agents (v7: agent harness integrations, tool approvals, durable WorkflowAgent, multimodal APIs). https://vercel.com/docs/ai-sdk
- **eve** — Open-source agent framework where an agent is a directory of files, with durable execution, sandboxed compute, approvals, subagents, and evals built in. https://vercel.com/docs/eve
- **Vercel Agent** — AI teammate that reviews code, investigates incidents, and takes approved actions from your dashboard. https://vercel.com/docs/agent
- **Vercel MCP** — Official MCP server to manage Vercel projects, deployments, and Agent Runs from AI assistants. https://vercel.com/docs/mcp
- **Vercel Connect** — Scoped, short-lived tokens for agents and apps to access external services (Slack, GitHub, Salesforce, custom APIs) without long-lived secrets. https://vercel.com/docs/connect

### Workflows & Queues

- **Workflows** — Durable, crash-safe workflow execution with the Workflow SDK (`"use workflow"`), observability, and trace viewer. https://vercel.com/docs/workflows
- **Queues** — Reliable background message processing with the Queues SDK; supports up to 7-day message TTL. https://vercel.com/docs/queues

### Security

- **Vercel Firewall / WAF** — Platform-wide DDoS protection plus custom WAF rules (including natural-language rule creation); firewall-mitigated traffic is free. https://vercel.com/docs/vercel-firewall
- **Bot Management** — Classify and control automated traffic. https://vercel.com/docs/bot-management
- **BotID** — Invisible CAPTCHA-style bot detection for high-value routes. https://vercel.com/docs/botid
- **Deployment Protection** — Password, SSO, and trusted-source protection for previews and production. https://vercel.com/docs/deployment-protection
- **Vercel Passport (public beta)** — Gate deployments behind your own identity provider (Okta, Auth0, any OIDC). https://vercel.com/docs/passport
- **DDoS Mitigation** — Automatic L3/L4/L7 DDoS defense on every deployment. https://vercel.com/docs/security/ddos-mitigation
- **RBAC** — Role-based access control for team members and resources. https://vercel.com/docs/rbac

### Developer Experience

- **Vercel CLI** — Deploy, develop, and manage everything from the terminal (dry-run deploys, native curl syntax, metrics/analytics queries, firewall and flags management). https://vercel.com/docs/cli
- **REST API & Vercel SDK** — Programmatic control of the whole platform. https://vercel.com/docs/rest-api
- **Observability** — Logs, traces, metrics, monitoring, and anomaly alerts across functions, workflows, and agents. https://vercel.com/docs/observability
- **Vercel Flags** — Platform-native feature flags (GA) with targeting, segments, progressive rollouts, and the Flags SDK. https://vercel.com/docs/flags
- **Rolling Releases** — Gradually shift traffic to a new deployment with automatic monitoring. https://vercel.com/docs/rolling-releases
- **Instant Rollback** — Revert production to a previous deployment in seconds. https://vercel.com/docs/instant-rollback
- **Vercel Toolbar** — In-browser toolbar for comments, flags overrides, and draft mode on previews. https://vercel.com/docs/vercel-toolbar
- **Speed Insights** — Real-user Core Web Vitals, queryable from the CLI. https://vercel.com/docs/speed-insights
- **Web Analytics** — Privacy-friendly, first-party analytics, queryable from the CLI. https://vercel.com/docs/analytics
- **Vercel Drop** — Instantly share files and prototypes as deployments. https://vercel.com/docs/drop
- **Checks** — Run quality checks (tests, Lighthouse, etc.) against every deployment. https://vercel.com/docs/checks
- **Git integration** — Automatic preview deployments for every push to GitHub, GitLab, or Bitbucket. https://vercel.com/docs/git

## Latest launches

See news.md (or the fetched fresh copy) for dated entries, newest first.
