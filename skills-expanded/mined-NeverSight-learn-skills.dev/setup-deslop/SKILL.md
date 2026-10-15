---
name: setup-deslop
description: One-time per-repo setup for the deslop pipeline, normally invoked by /deslop as step 0 (skipped if STACK.md already exists). Interviews the user about their stack (auth, payments, backend style, database, secrets, ops); detecting what it can from the repo first; and generates a STACK.md house overlay that the audit skills read. Triggered automatically by /deslop on first use in a repo; invoke directly when the user's stack has changed (switched auth provider, payment processor, framework, database) and STACK.md needs regenerating.
---

# Setup Deslop

Generate this project's `STACK.md`: the house overlay that tells the stack-agnostic audit what each category means *here*. Run once per repo (or once per org, if you share a stack). After this, `/map-the-surface`, `/plug-the-holes`, and `/launch-gate` know how to read your codebase.

The audit categories are universal; only their *instantiation* is yours. This skill captures that instantiation once so the audit never has to guess. The thinking behind it (the five questions every mapping answers) is in [references/MAPPING-PATTERN.md](./references/MAPPING-PATTERN.md). The blank it fills is [references/STACK-TEMPLATE.md](./references/STACK-TEMPLATE.md).

## Process

### 1. Detect first, ask second
Before interviewing, read what the repo already tells you: `package.json`/lockfile, framework config, `schema`/migration files, env-var names (names only, never values). Form a *hypothesis* of the stack and present it: *"Looks like an RPC-style backend with a managed auth provider, a single document store, an LLM API for AI features, secrets in env vars. Sound right?"* Confirming a good guess is faster and kinder than a blank interrogation.

### 2. Interview: the five questions, plus housekeeping
Work through the five mapping questions (see MAPPING-PATTERN). Ask in plain language, grouped, confirming detections rather than re-asking them. Cover:

- **Surface.** How does untrusted input reach the backend? What's the unit I enumerate (routes, server functions, resolvers, actions)?
- **Not-public mechanism.** How do you mark something server-only / admin-only? Where do debug/seed/admin routes tend to hide?
- **Identity.** What proves who the caller is, and what's the *safe* way a handler reads it? (So I can spot identity trusted from args/body, the classic Hole.)
- **Tenant & authz.** What's a tenant here (org/team/user)? What field keys a row to it? Is there one shared scoping seam, or is it re-done per handler? *(If there's no seam, recommending one is part of the output.)*
- **Money & cost.** Which calls hit a paid API per request? What's the payment processor and how are its webhooks verified? Any rate-limit/entitlement layer?
- **Secrets.** Where do secrets live? What's the client/server env convention, so I know what ships to the browser?
- **Data stores.** One database or several? (Two doing the same job is mixed-stack slop to flag.)
- **Ops.** Backups + tested restore? Prod/dev separation? Rollback? Error tracking + logging on money/identity paths?

Keep it to a handful of grouped exchanges, not 20 separate questions. If the user is unsure on one, mark it **Unknown** in `STACK.md`. An honest unknown is a finding the audit will resolve, not a blocker here.

### 3. Recommend the scoping seam
If the interview reveals no single place tenant scoping is enforced (per-handler copy-paste, or worse, missing), propose the seam appropriate to the stack: a `requireTenant`-style wrapper, a scoped data-access layer, or database row-level security. This is the highest-leverage line in the whole overlay; it's where closing Holes and removing slop become the same edit.

### 4. Write STACK.md
Fill [references/STACK-TEMPLATE.md](./references/STACK-TEMPLATE.md) from the answers and write it to the repo root (or `.deslop/STACK.md`). One concrete sentence per category: what the auditor should enumerate, where the seam is, what the tell is for that category's Hole. Note any **Unknown**s explicitly.

### 5. Confirm and hand off
Show the user the generated `STACK.md`, let them correct it, then point them at `/map-the-surface` to begin.

**Org shortcut:** if a team always ships the same stack, they keep one canonical `STACK.md` and copy it into each repo instead of re-interviewing. `/setup-deslop` then becomes "confirm this still matches."
