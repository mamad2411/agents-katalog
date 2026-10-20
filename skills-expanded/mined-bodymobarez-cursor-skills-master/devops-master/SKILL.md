---
name: devops-master
description: Master hub for DevOps, infra & deployment. Use for Docker, Kubernetes, Terraform, CI/CD, Cloudflare, and deployment. Bundles 20 specialized skills (in skills/<name>/GUIDE.md). Use this for any devops task.
---

# DevOps, infra & deployment — Master Hub

Use for Docker, Kubernetes, Terraform, CI/CD, Cloudflare, and deployment.

## How to use this hub

This single skill bundles **all 20 devops skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **adding-docker** — Dockerize an application with a production-ready Dockerfile, docker-compose setup, and .dockerignore.  
  → `skills/adding-docker/GUIDE.md`
- **blastum-ansible** — Infrastructure automation with Ansible. Use for server provisioning, configuration management, application deployment, and multi-host orchestration.  
  → `skills/blastum-ansible/GUIDE.md`
- **blastum-docker** — Dockerfile authoring, Docker Compose configuration, and containerization best practices. Use when creating Dockerfiles, optimizing builds, configuring Compose files, or implementing containerizatio...  
  → `skills/blastum-docker/GUIDE.md`
- **blastum-docker-cli** — Comprehensive Docker CLI reference for agent control and orchestration. Use when executing Docker commands, building orchestration scripts, managing containers/images/networks/volumes, remote Docke...  
  → `skills/blastum-docker-cli/GUIDE.md`
- **blastum-mac-container-virtualization** — Complete guide to using Apple's native container tool for virtualization on macOS with Tailscale networking and multi-language containerization.  
  → `skills/blastum-mac-container-virtualization/GUIDE.md`
- **cloudflare-cloudflare** — Comprehensive Cloudflare platform skill covering Workers, Pages, storage (KV, D1, R2), AI (Workers AI, Vectorize, Agents SDK), feature flags (Flagship), networking (Tunnel, Spectrum), security (WAF...  
  → `skills/cloudflare-cloudflare/GUIDE.md`
- **cloudflare-cloudflare-email-service** — Send and receive transactional emails with Cloudflare Email Service (Email Sending + Email Routing). Use when building email sending (Workers binding or REST API), email routing, Agents SDK email h...  
  → `skills/cloudflare-cloudflare-email-service/GUIDE.md`
- **cloudflare-durable-objects** — Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing RPC methods, SQLite storage, alarms, WebSockets,...  
  → `skills/cloudflare-durable-objects/GUIDE.md`
- **cloudflare-sandbox-sdk** — Build sandboxed applications for secure code execution. Load when building AI code execution, code interpreters, CI/CD systems, interactive dev environments, or executing untrusted code. Covers San...  
  → `skills/cloudflare-sandbox-sdk/GUIDE.md`
- **cloudflare-web-perf** — Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (LCP, INP, CLS) and supplementary metrics (FCP, TBT, Speed Index), identifies render-blocking resources, network depende...  
  → `skills/cloudflare-web-perf/GUIDE.md`
- **cloudflare-workers-best-practices** — Reviews and authors Cloudflare Workers code against production best practices. Load when writing new Workers, reviewing Worker code, configuring wrangler.jsonc, or checking for common Workers anti-...  
  → `skills/cloudflare-workers-best-practices/GUIDE.md`
- **cloudflare-wrangler** — Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets Store. Load before runni...  
  → `skills/cloudflare-wrangler/GUIDE.md`
- **cursor-skills-devops** — DevOps rules for Cursor — Docker, Kubernetes, CI/CD, monitoring, and cloud deployment. Use for infrastructure and DevOps tasks.  
  → `skills/cursor-skills-devops/GUIDE.md`
- **incident-response** — Handle production incidents — triage, mitigate, communicate, and write postmortems.  
  → `skills/incident-response/GUIDE.md`
- **kubernetes-deploying** — Deploy applications to Kubernetes — Deployments, Services, Ingress, ConfigMaps, Secrets, health checks, and scaling.  
  → `skills/kubernetes-deploying/GUIDE.md`
- **setting-up-ci** — Set up a GitHub Actions CI/CD pipeline with linting, testing, type-checking, and deployment steps.  
  → `skills/setting-up-ci/GUIDE.md`
- **setting-up-terraform** — Set up Terraform infrastructure-as-code for cloud resources, including provider configuration, modules, state management, and CI integration.  
  → `skills/setting-up-terraform/GUIDE.md`
- **vercel-deploy-to-vercel** — Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this live", or "create a preview deployment".  
  → `skills/vercel-deploy-to-vercel/GUIDE.md`
- **vercel-vercel-cli-with-tokens** — Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tokens rather than interactive login — e.g. "deploy to vercel", "set up vercel",...  
  → `skills/vercel-vercel-cli-with-tokens/GUIDE.md`
- **vercel-vercel-optimize** — Use for Vercel cost and performance optimization on deployed projects, especially Next.js, SvelteKit, Nuxt, and limited Astro apps. Collect Vercel metrics, usage, project config, and code scan resu...  
  → `skills/vercel-vercel-optimize/GUIDE.md`

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
