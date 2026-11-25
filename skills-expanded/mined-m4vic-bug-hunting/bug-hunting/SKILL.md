---
name: bug-hunting
description: Bug bounty hunting and penetration testing skills for Claude, Codex, and other agentic AI tools.
---

# Bug Hunting — Router

This is the entry point only. It does not contain technique detail — it decides which domain guide to load, then gets out of the way. Loading this file should never cost more than a few hundred tokens.

## The core discipline

Real bug hunting is not "run the checklist for one vuln class." Nobody tells you what bug exists, or if one exists at all. The loop is:

1. **Map the surface completely** — every endpoint, param, auth state, response shape.
2. **Hypothesize widely** — for each input, ask "what could this become?" Don't commit to one guess. A URL-fetching param could be SSRF, or IDOR if that value doubles as a record key — keep both alive until evidence rules one out.
3. **Confirm, don't guess** — a finding is only real once you've proven it (differential response, out-of-band callback, reproduced twice). Report only what you proved.

## Step 0 — the operating workflow (mandatory, before any domain routing)

**Before picking a domain, load `methodology/workflow.md` and follow it.** This is not optional technique reference — it's the administrative discipline that separates a systematic hunter from someone with the same knowledge who doesn't organize it: a real per-target working folder (`scope.md`, `recon/`, `hypothesis-log.md`, `findings/`, `session-notes.md`), a hard gate that blocks exploitation until recon is actually marked complete, a running log of every hypothesis tried (so nothing gets re-tested or lost across a long session), and a resume record so a paused engagement doesn't restart from zero.

If resuming a target already worked on, `methodology/workflow.md` also tells you to read that target's `session-notes.md` and `hypothesis-log.md` first — before doing anything else.

## Step 1 — identify the target type

Read the target's shape (URLs, app type, what you were handed) and pick the matching domain guide. Load **only** that guide's `ROUTER.md` next — not its `references/`, not another domain.

| Target looks like | Load |
|---|---|
| A website, web app, traditional HTTP endpoints | `web/ROUTER.md` |
| A documented/undocumented API — REST, GraphQL, gRPC, WebSocket | `api/ROUTER.md` |
| An iOS or Android app (APK, IPA, mobile client) | `mobile/ROUTER.md` |
| Cloud infra, IAM, SSO/enterprise identity (Okta, Entra, SAML, VPN) | `cloud-identity/ROUTER.md` |
| An AI/LLM feature — chatbot, agent, RAG, tool-calling | `ai-llm/ROUTER.md` |
| You don't know yet — need to map the attack surface first | `recon/ROUTER.md` |

A single engagement often touches more than one — e.g. a web app backed by an API backed by an LLM feature. Load each relevant domain's `ROUTER.md` as you reach that part of the surface; don't front-load all of them.

## Step 2 — inside a domain guide

Each domain `ROUTER.md` is a signal table: observable thing about this endpoint → plausible vuln class(es) → how to confirm. It stays small on purpose. Only when it points you at a specific class and you're going deep on that one, pull the matching file from that domain's `references/`.

## Step 3 — always applies, regardless of domain

- `methodology/workflow.md` — the working-folder/hypothesis-log/resume discipline from Step 0. Referenced again here because it stays active for the whole engagement, not just at the start.
- `methodology/mindset.md` — the hunter's decision loop in more depth (recon-first, hypothesize-wide, confirm-strict), read once, not per-target.
- `methodology/reporting.md` — how to write up a confirmed finding so it gets paid, not closed — a finding only moves from the hypothesis log into `findings/` once it clears this bar.

## Scope discipline

Only test targets you are explicitly authorized to test — an in-scope bug-bounty program, your own systems, or a lab you control. Read the program's scope and rules before sending a single request. This applies regardless of which domain guide is loaded.
