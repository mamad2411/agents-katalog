---
name: specdd
description: Spec-driven development orchestrator that turns vague, top-of-mind feature requests into production-grade specifications before any code is written. ALWAYS use this skill whenever the user describes a feature, change, capability, screen, flow, or new component in plain language — even if they don't explicitly ask for a spec. Triggers on phrases like "build me", "make me", "add a feature", "I want to", "help me create", "implement", "let's build", "I need a", "can you make", "create a screen/page/component", or any new-feature request that lacks complete requirements (missing user stories, acceptance criteria, edge cases, error/empty/loading states, accessibility, or non-functional requirements). Interviews the user to fill gaps, applies UX/UI common sense, produces a structured spec + plan + tasks, then implements against the spec. Use this BEFORE writing any code for non-trivial features. Skip only for true one-liners (rename a variable, fix a typo, answer a research question) or work that is purely investigative.
---

# specdd — Spec-Driven Development

## What this skill does

User requests for features are incomplete by design — the user gives you the top-of-mind 30%, not the full spec. Coding from that ships things that compile but miss the actual intent, skip the boring-but-critical states (loading, empty, error, edge), and feel unpolished.

specdd inverts that: you produce a spec the user agrees with **before** writing code. The spec captures intent, the user, the UX, edge cases, and non-functional requirements. The user keeps creative control; you stop guessing.

Not waterfall. The spec is small, agent-readable, revisable. Goal is alignment, not bureaucracy.

## When to use

Use it for any feature, screen, flow, component, API, change, or capability — even a one-line request.

Skip for: one-liners (rename, typo), pure Q&A or research, bugs with clear repro, or continuing in-progress work that already has a spec.

If unsure, use it. Under-use is the more common mistake.

## Scale ceremony to scope

| Scope | Signal | Artifacts |
|---|---|---|
| **Quick** | Single component, <30 min, no new surface area | Inline mini-spec (5–8 bullets) in chat. No files. |
| **Feature** | New UI / flow, 1–4 hours | `spec.md` + `plan.md` inline or as files. Skip tasks. |
| **Project** | Multi-day, multiple files/services | `spec.md` + `plan.md` + `tasks.md` as files in `specs/<feature-name>/`. |

User can override: "just a quick one" or "do this properly".

## The workflow

```
1. TRIAGE     →  scope, scale, skip-or-not
2. INTERVIEW  →  fill gaps the user didn't think to mention
3. SPEC       →  what & why (user-facing, no tech)
4. PLAN       →  how (tech approach, files, decisions)
5. TASKS      →  ordered, testable work units (Project scope only)
6. BUILD & VERIFY → implement against spec; run production-grade checklist before "done"
```

You don't ask permission to follow this workflow — it's the default. You DO surface the spec and plan for confirmation before building.

## Phase 1 — Triage

1. **Skip check:** one-liner, question, research? → abandon skill.
2. **Scope:** Quick / Feature / Project.
3. **Existing spec?** Read `specs/` first if it exists.
4. **Surface:** chat-only or filesystem-capable? Affects whether spec lives in chat or in a file.

State triage briefly: *"Treating this as a Feature — drafting a spec, then we'll build."*

## Phase 2 — Interview

Heart of the skill. Ask the **few** right questions to fill gaps — not a 20-question form.

**Rules:**
- 3–5 questions per round max. Prefer 1–2.
- Use tappable options when available — much easier than typing.
- Don't ask what you can reasonably infer or read from the codebase.
- State assumptions inline: *"Assuming X — flag if wrong."*
- For Quick scope, skip the interview; just state assumptions.

Cover the gaps the user **didn't already address**, in priority order:

1. **WHO** — user, technical level, device/context
2. **WHAT** — core story ("As a X, I want Y, so that Z")
3. **WHY** — the underlying problem (often reveals a better solution)
4. **DONE** — acceptance criteria, smallest version that ships
5. **EDGE** — empty / error / loading / offline / unauthorized / slow-network
6. **OUT** — what is explicitly NOT in scope
7. **NON-FUNCTIONAL** — perf, a11y, security/privacy, observability, i18n

See `references/interview-playbook.md` for question templates by request type.

## Phase 3 — Spec

Use `references/spec-template.md`. The spec is **user-facing and tech-free** — no frameworks, libraries, file names, or function names. If you're writing `useState` or `POST /api/`, you're in the Plan.

Show spec to user. Wait for explicit "looks good" / "ship it". Revisions are normal — expect 1–3 rounds for non-trivial features.

## Phase 4 — Plan

Use `references/plan-template.md`. Covers stack choices, file-level breakdown, key decisions with one-line rationale, alternatives considered, risks. Under 2 minutes to read. If longer, split the feature.

## Phase 5 — Tasks (Project scope only)

Use `references/tasks-template.md`. Each task: independently completable in one agent turn, has an observable "done" signal, has explicit dependencies.

For Quick or Feature scope, the agent's todo list is enough — skip the file.

## Phase 6 — Build & verify

Implement against the spec. While building:

- If the spec is wrong or incomplete, **stop and revise the spec**, don't silently deviate.
- Don't add scope the spec didn't ask for. ("I also added X" is a smell.)

Before declaring done, run the checklist in `references/production-checklist.md` — empty/error/loading states, a11y, keyboard, mobile, edge inputs, observability. Report what you verified and what you didn't: *"Verified items 1–15, skipped i18n (single-locale), didn't test screen-reader behavior end-to-end."*

---

## Common-sense gates

Push back **before** building, not after. UX defaults this skill assumes:

- **Names a solution, not a problem.** Ask what they're trying to do. ("Add a modal" may mean "let users edit X without losing context".)
- **Custom version of a solved problem.** Surface the standard pattern. ("Custom date picker? Native handles a11y, locales, keyboard for free.")
- **Scope creep in one sentence.** If a single sentence implies three features, name them; ask which is the MVP.
- **Conflicting requirements.** *"Fast AND comprehensive AND simple"* — surface the trade-off, let the user pick.
- **Destructive actions without safeguards.** Delete / overwrite / bulk-edit / send need confirmation patterns. Don't ship without one.
- **Auth/permission gaps.** If a feature touches user data, ask who can see/edit/delete it.

**Five-states rule.** Every screen / component / feature has these. If the spec doesn't address all five, it's incomplete:
1. **Loading** — what shows while data fetches
2. **Empty** — what shows with no data (the first thing new users see — must have a primary action)
3. **Error** — what shows on failure (with a recovery path; "Something went wrong" alone is not acceptable)
4. **Partial** — what shows when some-but-not-all data arrived
5. **Ideal** — the loaded / happy state everyone draws first

**Other defaults baked in.** State them when relevant; the user can override:
- Feedback within 100ms of any action; skeleton (not spinner) for loads >300ms
- Optimistic updates with rollback (defer optimism for server-assigned IDs)
- Confirmation scales with destruction: undo toast → modal → type-the-name
- Errors are actionable (what happened, why if knowable, what to do now)
- Keyboard reachable; visible focus; `Esc` closes; `Enter` submits
- Mobile usable at 360px; touch targets ≥44×44px
- Forms validate on blur, errors inline at the field, submit shows progress
- Respect `prefers-reduced-motion`; animations short (150–250ms) and ease-out

---

## Anti-patterns

- **Spec theatre.** Producing a long spec to look thorough. Specs scale with scope.
- **Firehose interview.** A 12-question form makes users bounce. Ask 2–3, infer the rest, surface assumptions.
- **Pre-coding the spec.** "Use React Query with optimistic updates" is plan, not spec.
- **Silent drift.** When implementation reveals a flaw, update the spec — don't quietly diverge.
- **Skipping verify.** The difference between "done" and "delightful" is the checklist.

## Worked examples

- `references/examples/example-quick-feature.md` — Quick scope, inline only
- `references/examples/example-feature-spec.md` — Feature scope with spec + plan
- `references/examples/example-project.md` — Project scope with files

Read the relevant example if unsure what the output should look like at a given scope.
