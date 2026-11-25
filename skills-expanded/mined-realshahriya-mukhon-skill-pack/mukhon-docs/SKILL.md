---
name: mukhon-docs
description: Canonical MUKHON (মুখন) Platform architecture, product requirements, system flows, design system, technical stack, database schemas, roadmap, and security invariants. Use whenever designing, implementing, reviewing, or debugging any part of the MUKHON codebase.
license: MIT
---

# MUKHON (মুখন) Sovereign Platform Documentation Skill

This skill connects the AI assistant directly to MUKHON's canonical documentation located in `/doc/` (and symlinked at `/.agents/doc/`).

Whenever you are tasked with creating, refactoring, styling, or auditing code in MUKHON, consult the authoritative document matching your task:

---

## 1. Document Routing Directory

| If you are working on... | Consult Document | Key Topics & Invariants |
| :--- | :--- | :--- |
| **Product features, user requirements, verification tiers, personas** | [`/doc/PRD.md`](doc/PRD.md) | 6-Tier Trust Hierarchy, "Social Media First" vision, target personas, functional requirements (FR-01 to FR-12), regulatory compliance. |
| **Workflows, user journeys, sequence diagrams, state machines** | [`/doc/FLOW.md`](doc/FLOW.md) | NID e-KYC flow, Adda feed lifecycle, Reels 0ms playback & 3-dot HUD drawer, SafePay 4-digit OTP escrow, Mini-App IPC bridge. |
| **Styling, CSS variables, typography, layouts, components, reels HUD** | [`/doc/UI.md`](doc/UI.md) | Sovereign Dark tokens, Hind Siliguri / Inter fonts, 6+1 TrustBadges, `MukhonPlayer`, `ReelsView`, `CreatePostModal`, mobile viewport lock. |
| **API endpoints, Fastify server, Next.js AppRouter, runtime failover** | [`/doc/TRD.md`](doc/TRD.md) | Monorepo stack, Dual-Mode In-Memory/Postgres engine, multi-path `.env` discovery, 401 session resiliency, REST & WebSocket schemas. |
| **Database tables, SQL migrations, double-entry ledger, blind indexing** | [`/doc/DB.md`](doc/DB.md) | PostgreSQL 15 DDL, ENUMs, double-entry ledger ($\sum \text{Debit} = \sum \text{Credit}$), `nid_blind_index`, text-handle relational casting. |
| **Project milestones, sprint tasks, feature rollout, risk mitigations** | [`/doc/PLAN.md`](doc/PLAN.md) | 18-week roadmap, Sprints 1 to 9 deliverables, risk matrix, Definition of Done (DoD). |
| **Security hardening, threat models, escrow locks, OWASP, anti-fraud** | [`/doc/SECURITY.md`](doc/SECURITY.md) | Zero-trust model, zero raw PII storage, SafePay row locks (`SELECT ... FOR UPDATE`), constant-time OTP check, 3-strike dispute lock. |

---

## 2. Universal Invariant Quick Checklist

Before finalizing any changes, verify:
1. **Zero Tailwind Dependency:** Use semantic Vanilla CSS with design tokens.
2. **Double-Entry Ledger:** Never mutate wallet balances without balanced debit/credit records in `ledger_entries`.
3. **Session Resiliency:** Never log the user out on network drops or 5xx server errors; only explicit 401 Unauthorized invalidates local session.
4. **Zero Raw PII Storage:** Raw NID numbers must never be stored; use HMAC-SHA256 blind indexing.
5. **Clean TypeScript Build:** Monorepo must pass `npm run typecheck` cleanly with 0 errors.
6. **No Auto-Commit:** Never run `git commit` or `git push` without an explicit direct user command.
