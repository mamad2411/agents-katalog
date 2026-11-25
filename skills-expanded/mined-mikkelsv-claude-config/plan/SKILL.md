---
name: plan
description: "Collaborative feature planning through discovery, external research, and architecture scrutiny — produces a structured task plan in plans/ that feeds /implement. Use whenever the user describes a new feature, says \"I want to build X\", \"let's plan Y\", or \"how should we approach Z\", or when work spans 3+ files or has design decisions. This is design and discovery — not execution (/implement) and not read-only research (/study)."
---

# Feature Planning

**Think carefully** — reason through trade-offs, edge cases, and failure modes before recommending. Act as a skeptical senior engineer, not an eager assistant: **do not default to agreement**, and assume the first approach (yours or the user's) isn't the best until you've looked for a simpler one.

- Find what's wrong with a proposed architecture before validating it. Name the pattern being reinvented (e.g. a repository over EF's `DbSet`).
- Surface a simpler idiomatic alternative in the project's own stack, unasked — establish the stack first.
- Question whether the feature needs to exist if the motivation is unclear.

## Input

> $ARGUMENTS

If empty, ask what to plan.

## Phase 1 — Understand

Read the input. Two passes — project context (always), then codebase exploration (delegated to `/study`).

### Phase 1.1 — Project Context

1. **`CLAUDE.md`** at the project root — architecture, conventions, stack
2. **`.claude/rules/`** — project-specific rules that constrain how things are done
3. **`docs/`** if it exists — deeper architecture documentation
4. **`plans/`** — check for overlapping or related plans

### Phase 1.2 — Codebase Exploration via /study

`/study` is the source of truth for "how to explore an area" — parallel sonnet agents + optional external research, synthesized into session.

**Fresh-session heuristic** (no substantive prior tool use, no prior file reads in this area, no prior discussion of the topic): invoke `/study <topic>` automatically.

**Non-fresh session**: ask via `AskUserQuestion` — **Study first** (Recommended if topic unfamiliar) / **I have context, skip study** / **Let's discuss**. If **Study first**, invoke `/study`; otherwise proceed with a focused direct read (`Glob`/`Grep` + targeted `Read`).

**Skip entirely** for trivial work (single-file fix, rename, config tweak).

Present the synthesis at the start of Phase 1.5.

## Phase 1.5 — External Research

Per `wf-verify-api-before-using`, research before drafting when the feature involves:

- A **third-party library, framework, or service**, or an **API surface you'd otherwise guess at** (signatures, config keys, lifecycle hooks, version breaks)
- A **pattern with competing approaches** (auth, real-time sync, caching, background jobs) — confirm the current idiom
- A **specific library/version** the user named — confirm it exists, check the changelog and known issues
- An **anti-pattern alternative** you're about to recommend — confirm the framework still recommends it

Use `WebSearch` + `WebFetch` on primary docs, cross-check 2 sources, confirm the project's package version supports it, and note the source of each non-obvious claim. Skip for pure UI tweaks, internal refactors, or features fully explained by the project's code. **If uncertain whether to research, research.** Surface what you learned at the start of Phase 2.

## Phase 2 — Discovery

Use `AskUserQuestion` to clarify the feature. Prefer clickable options with 2-3 choices plus a "Let's discuss" escape hatch. Ask 2-4 questions per round, usually 2-3 rounds total.

Draw from these dimensions as needed: **Functional** (what, inputs/outputs, edge cases), **Philosophy** (problem being solved, fit with app vision), **Technical** (where in architecture, DB changes, perf), **Future** (design for now vs leave door open).

**Must include at least one critical/skeptical question per round** — e.g. "Why build this instead of [existing feature/library]?", "This duplicates [pattern] — intentional?", "What if we just don't build this?"

### Architecture scrutiny

When the user proposes or implies an architectural choice, **must evaluate against idiomatic patterns** before accepting. Flag violations directly — do not hedge.

Apply both the global `arch-*` rules in `~/.claude/rules/` (auto-loaded — covering common .NET / EF Core / DI anti-patterns) and the project-specific `arch-*` rules in `.claude/rules/`. Project specifics override generic guidance where they overlap.

If the user's plan hits any flagged anti-pattern, **must** raise it in Phase 2 and propose the idiomatic alternative as the recommended option — even if they seemed set on the original approach.

Make one option your recommendation (often "don't build it this way"), flag conflicts with existing patterns directly, raise unmentioned edge cases, and agree only after scrutiny — saying why.

### Design agreement (features with a UI surface)

Skip this subsection if the feature has no UI surface at all — record that plainly in Phase 3's `## UI Contract` rather than omitting the section.

Before drafting, spawn `design-scout` (`subagent_type: "design-scout"` — **never** `general-purpose`, which has every tool and would silently erase the read-only restriction). Hand it the feature brief; it returns a constraint inventory plus candidate decisions triaged into **design-system-determined** / **existing-component-precedent** / **genuinely-open**. It has no `AskUserQuestion` and never decides anything — **only the genuinely-open bucket becomes a question you ask here**, with options grounded in the tokens and components it cited.

Reach agreement on **structure**, never inferred from surrounding code: where the feature lives (new page / panel in existing chrome / modal / inline), the primary interaction model, the information hierarchy, and the scale of the change ("adds a panel" vs "restructures the sidebar").

**The instrument is a concrete artifact, not a questionnaire.** Draw one ASCII mockup and ask "is this what you pictured?" via `AskUserQuestion`. Default to **one** mockup; use the `preview` field to offer 2–3 alternatives only where the genuinely-open bucket surfaces a real fork worth the user's time. This instrument **replaces** a battery of detail questions rather than supplementing one: **detail-level UI — spacing, hover, empty/loading/error/disabled/overflow states — is out of scope here.**

The agreed mockup becomes Phase 3's `## UI Contract` verbatim — the artifact itself, not a paragraph describing it. It is a structural agreement, not a spec: an implementing agent settles undecided detail within it rather than treating silence as a blocker.

**An undecided design question never stops the implementation loop.** If one surfaces mid-run, the agent makes the recommended call and continues, logging it to `Decisions & Review Items` as an in-flight decision (rejected alternative + rough cost-to-change). Escalation is reserved for architectural shape via `wf-think-clearly-on-architecture`. So **this subsection's agreement is the only place design gets settled.**

## Phase 2.5 — Scope Check

**Default: one plan per shippable feature, regardless of task count.** Milestone tasks (Phase 3) bound unattended work on top of an undetected regression; a single plan keeps one continuous context.

**Split only when the user identifies distinct shippable increments** — never from task or area count alone. If they do:

1. Propose the increments with names, order, and dependencies via `AskUserQuestion`.
2. Create a **managing plan** in the plans directory using `managing-plan-template.md` from the implement skill directory.
3. Create a separate **task plan** for each phase (using `plan-template.md` as usual).
4. The managing plan links to each phase's task plan by path.

Managing plan format: `## Phases` with `### Phase N: {name}` entries listing `**Plan:**`, `**Summary:**`, and `**Dependencies:**`. See the template for the full structure.

`/implement` detects the managing plan automatically and chains phases sequentially.

## Phase 3 — Draft

Create a plan file in `plans/` at the project root. Read `plan-template.md` from the implement skill directory for the task format.

Include sections: **Context** (before tasks), **Design Decisions** (before tasks), **UI Contract** (before tasks; required whenever the feature has a UI surface, per "Design agreement" above — write "None." if it doesn't, since an absent section can't be distinguished from an unasked question), **Future Considerations** (after tasks), **Decisions & Review Items** (empty, for implementation).

Task guidelines:

- Atomic and independently testable
- First task = smallest vertical slice (end-to-end)
- DB/model changes early (others depend on them)
- One component/page per UI task
- Last task = polish and cleanup
- Populate `**Dependencies:**` and `**Parallel group:**` (Phase 3.5)
- Populate `**Verify:**` per acceptance criterion — see below
- Populate `**Test:**` per the tier ladder — see below
- Mark milestone tasks by appending ` — **milestone**` to the heading — see below
- Check each task is cold-executable — see below

### The `**Verify:**` field

One entry per `**Acceptance:**` criterion, naming the instrument that settles it — never prose a verifier has to interpret. Preference order:

1. **A named test the project already exposes** — the general case.
2. **A state probe read** — whatever inspection surface the app offers.
3. **A standing scenario** — one of the project's durable end-to-end scenarios.
4. **A direct command dispatch** — the narrow case. Dispatch reach is often partial, so never assume a given command is reachable just because it exists.
5. **`human: <what to look at>`** — first-class, not a fallback of last resort. Pixels need a displayed pane; an honest escalation beats a silent pass.

**Wall rule:** a criterion needing an instrument that doesn't exist yet gets a task that builds it — never weaken the criterion to fit current tooling.

`/verify` reports `can't-tell` as distinct from `pass` — a criterion it can't settle is never counted as met.

### The `**Test:**` field

States which per-task gate `/implement` runs for this task — distinct from `**Verify:**` above, which names the instrument for each acceptance criterion. `**Test:**` names the tier.

- **Default: `/test gate`** — build plus every tier needing no preview server. Write "existing tests sufficient" or name the new unit test; don't request a browser tier you don't need.
- **Name a browser-tier check only when the task needs one** — a standing scenario, a task-written scenario, the integration suite, or `human: <what to look at>`. Naming one runs exactly that check, not the full stack.
- **Prefer a task-specific scenario over the project's generic standing scenarios.**
- **`human: <what to look at>` is first-class, and the expected value for a task implementing UI** — no tier verifies visual conformance to an agreed mockup.
- Per `wf-repro-test-first`: for a bug fix or new behavior, say "write first" and name the expected red before the fix.

Milestone tasks and the plan's last task always add the full suite regardless of what's written here.

### Milestone marking

Append ` — **milestone**` to a task's heading — e.g. `### Task 7: {short description} — **milestone**`. `/implement` detects this literal marker and runs the full suite **in addition to** whatever this task's `Test:` field names, never instead of it. `/verify` is not part of a milestone gate — it runs once, after every task is committed.

Place tighter around rendering-heavy or state-shape work (often only the browser suite reaches it); looser around docs, prose, and refactor tasks.

A milestone doubles as a re-grounding point: before running the gate, `/implement` re-reads the plan file and its `## UI Contract`.

### Cold-executable tasks

Plan-time check, applied per task before Phase 3.5: **could this task be handed to a fresh agent with only the plan file** — no memory of this conversation, no memory of an earlier task? `Context:` / `Files:` / `Acceptance:` must name actual paths, functions, and decided values — never "as discussed" or "per the approach above." State what the agent should **verify against the live repo** (grep for X, confirm Y exists), not only what was decided — decisions drift before the task runs.

A task that fails this check gets rewritten now, not flagged for later.

## Phase 3.5 — Parallel Analysis

Skip if <4 tasks or clearly sequential. Find task pairs with no dependency and disjoint `**Files:**` lists. Disqualify tasks sharing infrastructure (DI registration, shared CSS, migrations). Present proposed groups via `AskUserQuestion` — user approves, adjusts, or declines. Tag approved groups with letters (A, B, C); others get `—`.

## Phase 4 — Present

Show: feature summary, plan location, task count, open questions/risks, and the `## UI Contract` mockup if the plan has one — restated here for convenience, but the file remains the source of truth. Ask if adjustments needed; loop until the user has no more.

When the adjustment loop closes, **auto-run** `/plan-optimizer` for any plan with **3+ tasks**, or when a managing plan was created in Phase 2.5 — invoke the `plan-optimizer` skill with the plan path directly, no prompt. For very small features (1-2 focused tasks, single area), skip it — Phase 2's discovery already covered them.

## Project rules

Additional project-specific planning rules — anti-pattern lists, architecture principles, naming conventions. Projects layer a `<ProjectSpecific>` block here pointing at their relevant `.claude/rules/` entries.
