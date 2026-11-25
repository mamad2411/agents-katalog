---
name: sveltekit-security-stinger
description: Evidence-backed, read-only security audit of Svelte 4/5 and SvelteKit 2 apps, any stack. Versions vs advisories, load leaks, actions, remote functions, hooks, XSS, CSRF, adapters.
license: AGPL-3.0-or-later
compatibility: Claude Code 2.1 or newer, Cursor 2.4 or newer, Codex, Cowork. Scanner needs Python 3.11 or newer (standard library only); ripgrep recommended.
metadata:
  author: Legion Code Inc.
  hive-drone: sveltekit-security-wasp-drone
  pair-drone: sveltekit-security-wasp-drone
  domain: sveltekit security audit
  version: 1.0.0
  research-window: 2026-03-30 to 2026-09-30
---

# SvelteKit Security Stinger

Designed and built by Legion Code Inc.

## Where this skill's files are

Every path below (`guides/`, `references/`, `scripts/`) is relative to the folder that contains this `SKILL.md`. In Claude Code that folder is `${CLAUDE_SKILL_DIR}`. If that text was not replaced with a real path, find the folder yourself (Glob for `**/sveltekit-security-stinger/SKILL.md`) and use it as the skill directory in every command.

## Purpose

Audit a Svelte or SvelteKit codebase for security problems the way an attacker would approach it, and report each one with evidence a founder can act on. The skill is framework-deep and stack-agnostic: it works on any SvelteKit 2 app (any database, auth library, or host) and on plain Svelte + Vite SPAs. It produces contract-shaped findings for the Audit My Code run: installed versions matched against every published advisory for svelte, @sveltejs/kit, devalue and the official adapters, plus manual-review findings across the server and client boundary, form actions, `+server` endpoints, remote functions, hooks and the authorization model, XSS sinks, CSP, cookies, adapters, prerendering, and patterns common in AI-written Svelte code. It never changes the audited repository.

## When to use

- The Audit My Code orchestrator dispatches `sveltekit-security-wasp-drone` because `intake.json.stacks` lists `svelte` or `sveltekit`
- "Security audit this SvelteKit app", "are my form actions protected", "do my remote functions check auth", "is my load function leaking data"
- "Which SvelteKit or Svelte advisories affect us", "is our devalue version safe"
- Reviewing a Svelte + Vite SPA for secrets in the bundle and XSS sinks

## When not to use

- The repository's own stack-specific gate (SvelteKit with Neon, WorkOS, Stripe, Vercel, Doppler, GoHighLevel) before a commit: `security-stinger`, which also remediates
- Secrets in git history, generic dependency triage, webhook signature checks, database row-level security: `security-wasp-drone` generic pass (`security-stinger`, armed report-only)
- React or Next.js code: `react-security-stinger` or `nextjs-security-stinger`; back ends in other languages: `polyglot-security-stinger`
- Fixing the findings: this skill is report-only; remediation planning belongs to the `mario` tier
- A live, external scan of a deployed site with no source: `web-security-posture-stinger`

## Procedure

1. Read the run contract (`audit-my-code-stinger/references/audit-contract.md`) and `intake.json`. Your scope is the stack paths for `svelte` and `sveltekit`.
2. Follow [guides/00-scoping-and-version-check.md](guides/00-scoping-and-version-check.md): classify each path, check advisory freshness, run `scripts/sveltekit_audit_scan.py`, review its version findings, and build the reading list.
3. Follow [guides/01-server-client-boundary-and-load-exposure.md](guides/01-server-client-boundary-and-load-exposure.md): public env names, universal loads, server load returns, remote queries, shared state.
4. Follow [guides/02-actions-endpoints-remote-functions.md](guides/02-actions-endpoints-remote-functions.md): build the endpoint table and check authorization, object ownership, validation, and CSRF for every surface.
5. Follow [guides/03-hooks-and-authorization-model.md](guides/03-hooks-and-authorization-model.md): write the auth model, check identity, `handle` coverage (including remote functions), layout-only and client-only guards, server fetch, errors, redirects.
6. Follow [guides/04-xss-csp-and-cookies.md](guides/04-xss-csp-and-cookies.md): every HTML sink, markdown pipeline, template-pattern advisory input, CSP, cookies, token storage.
7. Follow [guides/05-config-adapters-and-prerender.md](guides/05-config-adapters-and-prerender.md): adapter and host, prerender, adapter-node headers, Vercel ISR, platform env, service worker.
8. Follow [guides/06-writing-findings.md](guides/06-writing-findings.md): write `findings-sveltekit-security-wasp-drone.jsonl`, `metrics-sveltekit-security-wasp-drone.json`, and the notes file in `02-security/`, validate them, and return the verdict, counts by severity, and every coverage cap.

Throughout: no finding without evidence; `possible` never above `medium`; redact secrets to the first 4 characters plus `****`; never run installs, builds, or servers in the audited repository.

## References map

| Path | Load when |
| --- | --- |
| [references/REFERENCE.md](references/REFERENCE.md) | Start of every run: file map, scanner interface and outputs, finding example |
| [references/check-catalog.md](references/check-catalog.md) | Guides 01 to 05: each check's detection, confirmation, severity, code pair, refs |
| [references/detection-patterns.md](references/detection-patterns.md) | Before each guide's manual read: tested ripgrep commands |
| [references/advisory-table.md](references/advisory-table.md) | Guide 00, and explaining a version finding |
| [references/severity-guide.md](references/severity-guide.md) | Assigning severity and confidence; guide 06 |
| [references/research/distilled-sveltekit-security.md](references/research/distilled-sveltekit-security.md) | Verifying a claim, resolving a conflict, checking a thin spot |
| Source research archive (not shipped with the plugin) | Source-repository only; the shipped distillation summarizes it, do not require it |
| [scripts/sveltekit_audit_scan.py](scripts/sveltekit_audit_scan.py) | Once per run in guide 00 |
| [scripts/advisories.json](scripts/advisories.json) | Data for the scanner; refresh when older than 30 days |

## Related drones and stingers

- [sveltekit-security-wasp-drone](../../agents/sveltekit-security-wasp-drone.md) - The paired agent in this pack; the orchestrator dispatches it with this skill.
- [audit-my-code-stinger](../audit-my-code-stinger) - The run orchestrator and the contract this skill writes against.
- `security-stinger` (core) - Stack-specific Ship Gate security pass for SvelteKit with Neon, WorkOS, Stripe, Vercel, Doppler; the generic security pass in Audit My Code runs it report-only beside this skill.
- `react-security-stinger`, `nextjs-security-stinger`, `polyglot-security-stinger` (this pack) - Framework-deep passes for other stacks in a monorepo.
- `svelte-stinger` in `web-development-tools` (confirm installed) - Svelte 5 and SvelteKit 2 language and runtime details when a finding's fix needs them.
- `dependency-audit-stinger` (core) - Lockfile and supply-chain work beyond framework advisories.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [audit-my-code-stinger](../audit-my-code-stinger) - Audit My Code orchestrator, tiers, routing, and the shared output contract.
  - `security-stinger` - Generic and stack-specific security pass; first gate of the Ship Gate in development work.
  - `svelte-stinger` - Svelte 5 runes, SvelteKit 2 load functions, form actions, and remote functions.

<!--
Ship Gate removed: research-only stinger, produces no committable code.
-->

---

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.
