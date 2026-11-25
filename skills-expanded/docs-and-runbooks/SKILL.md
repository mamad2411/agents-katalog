---
name: docs-and-runbooks
description: Documentation that survives — READMEs that get someone running, ADRs that preserve decisions, runbooks that work at 2 a.m., and onboarding docs that scale the team. Use when writing or updating any project documentation, setting up a new repo, documenting operations or deploy procedures, capturing a decision, or when the user says "document this", "write a README", "runbook", "onboarding", "ADR", or "nobody knows how this works".
---

# Docs and Runbooks

Documentation has exactly one quality metric: **does the reader succeed at their task without asking anyone?** Docs are not written for completeness; they're written for four specific readers — the newcomer cloning the repo, the operator during an incident, the maintainer questioning an old decision, and (now, always) the AI model that reads your docs before touching your code. Write for those four; delete everything else.

## The prime rule: docs live where they can't be missed, and die when stale

- Docs live **in the repo, next to what they describe**, updated **in the same PR** as the change that staled them — a doc update is part of "done", not a follow-up ticket that never comes (same-PR rule; reviewers enforce it).
- A wrong doc is worse than no doc: the reader trusts it, acts on it, and fails confused. When you find a stale doc, fixing or deleting it *is* the task — never route around it silently.
- Don't document what the code already says (that's the what-comment sin at file scale, code-quality). Document what code *can't* say: how to run it, why it's shaped this way, what to do when it breaks.

## The four documents that matter

### 1. README — clone to running, measured in minutes
The README's job is one thing: a competent stranger goes from `git clone` to a running system without asking anyone. Contents in order: one paragraph of what this is → prerequisites → the exact copy-pasteable commands to run it → how to run the tests → where to find dev credentials/seed logins → the 3 gotchas that burn everyone. **Test it the only way that counts: fresh machine (or fresh clone + clean env), follow your own instructions literally.** Every place you improvise, the doc is broken. If setup takes 20 manual steps, the fix is scripting the steps (`make dev`, `docker compose up`), not documenting them harder.

### 2. ADRs — decisions with their why attached
Five lines per non-obvious decision: **context → options considered → decision → consequences accepted** (architecture-design). The trigger for writing one: any decision where a smart person's first reaction later would be "why on earth is it like this?" — because without the ADR, they'll "fix" it and relearn the reason in production (dependency-discipline's ledger; Chesterton's Fence from legacy-code-changes). ADRs are append-only history: a reversed decision gets a new ADR pointing at the old one, so the trail of *why* survives.

### 3. Runbooks — written calm, read panicked
For each alert and each recurring operational task, a runbook the on-call person can follow **at 2 a.m. with degraded judgment**:
- Structure: symptom ("payments error rate alert fired") → impact check (how bad? who's affected? — the 4 incident questions, observability-readiness) → diagnostic steps as exact commands, copy-pasteable, with expected output shown → decision fork ("if X → restart worker; if Y → escalate") → escalation contact and rollback procedure (deployment-safety).
- No prose paragraphs; numbered steps. No "check the usual suspects"; the *list* of suspects with the command for each.
- A runbook is verified the same way a README is: someone follows it literally during a calm-hours drill. Every incident that used a runbook improves it; every incident that lacked one creates one (root-cause-debugging's closing-the-loop rule).

### 4. The bus-factor page — one page that survives you
Where prod runs, how to deploy, where secrets/backups live, how to restore, which third parties matter and where the accounts are, who to call. This page is the difference between "founder on vacation" and "company on pause" (release-readiness Gate 7). Keep it findable, current, and boring.

## Writing rules (all four docs)

- **Commands over descriptions**: `docker compose logs backend | grep "OTP"` beats "check the backend logs for the OTP". Exact, copy-pasteable, with expected output where surprise is possible.
- Lead with the common case; ugly details after. The reader doing the normal thing shouldn't wade through the disaster appendix.
- State *versions and assumptions* ("assumes Docker 24+, ports 3000/8000 free") — unstated assumptions are where instructions break.
- Screenshots rot faster than text; prefer text + exact labels ("Settings → API Keys → Create") over images, except where the UI is genuinely the content.
- One source of truth per fact: the README links to the runbook rather than restating it. Duplicated docs drift into contradiction, and the reader can't tell which copy lies.

## Docs as AI leverage — the newest reason to bother

Your project-instructions file (CLAUDE.md / AGENTS.md) is documentation with a direct behavioral payoff: every convention written there is a correction you stop making per-task, for every AI model that touches the repo (ai-build-quality Law 2). The same holds in reverse — READMEs, ADRs, and runbooks are exactly what an AI assistant reads to operate your system safely. Documentation quality is now, literally, a multiplier on your AI tooling. Keep it curated: bloated instruction files get skimmed by models just like by humans.
