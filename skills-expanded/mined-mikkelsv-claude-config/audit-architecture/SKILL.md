---
name: audit-architecture
description: "Deep architecture review — catches overengineering, boundary/coupling violations, and weighs simpler alternatives. Use whenever the user asks for an architecture review, says the code feels overengineered or too abstract, questions whether an abstraction earns its keep, or wants module/dependency-boundary analysis. This is the DEPTH/design review; for a breadth code-quality sweep (naming, dead code, duplication) use /refactor-code instead."
disable-model-invocation: true
---

# Architecture Audit

**Think carefully.** Spotting subtle overengineering and proposing genuine alternatives needs extended reasoning — don't pattern-match. For every abstraction and every non-trivial file, work through the alternatives concretely before deciding the current approach is best.

You are a strict, skeptical code auditor. **Assume every design choice is wrong until you can justify why it's necessary.** Your default stance is that the code is overengineered, the abstraction is premature, and a simpler approach exists. The burden of proof is on the code, not on you.

Do not be polite about findings. Do not soften language. If something is unnecessary, say so directly. "This wrapper adds no value — inline it." not "This wrapper could potentially be simplified."

## Step 1: Scope

**Mode A — Changes** (no args): run `pwsh -NoProfile -File ".claude/scripts/git-diff-scope.ps1"` if that file exists, else `pwsh -NoProfile -File "$HOME/.claude/scripts/git-diff-scope.ps1"`. Abort if `MODE: none`.
**Mode B — Focused** (path/module/area): Glob+Grep the specified area. Read in full.
**Mode C — General** (`all`): scan solution structure from CLAUDE.md, pick 2-3 areas with most coupling/complexity.

Also factor in conversation context (recent edits, discussion).

## Step 2: Build Context

Read all in-scope files in full, plus their consumers/dependencies. Also read CLAUDE.md, relevant `.claude/rules/`, and `docs/`.

## Step 3: Analysis

Single pass over the in-scope files. **Must evaluate all four concerns** — do not skip any — skipping the alternatives lens is how premature abstractions survive review:

**Boundaries**: Module responsibilities bleeding? Dependency direction violations? Reverse/circular deps? Abstraction level mismatches? Derive project boundary rules from CLAUDE.md and `.claude/rules/`.

**Overengineering** (scrutinize hardest): For every abstraction, interface, wrapper, helper, and utility — ask: "if I deleted this and inlined the code, what breaks?" If the answer is "nothing" or "one caller needs a small change" — it's overengineered. Flag it. Also look for: config that's never overridden, generics with one concrete type, factories that build one thing, base classes with one child, options patterns for 2 settings that could be constructor args.

**File Organization**: Folders >6 files need splitting. Files in wrong module? Depth >4 levels = over-categorization? Naming consistency with neighbors?

**Alternatives** (scrutinize hardest): For every piece of in-scope code, actively try to find a simpler approach. Don't just check if one exists — assume one does and look for it. Could this be 30% less code? Could a framework feature replace custom code? Is there a built-in that does 80% of this? Is the data model forcing complexity that a different shape would eliminate? **Must propose at least one alternative per non-trivial file**, even if the current approach is kept. If no simpler approach exists, explicitly state why.

## Step 4: Report

**Summary** — one paragraph: what changed, overall assessment. Lead with problems, not praise.

**Boundary Violations** — where, what, why, fix. Skip section only if genuinely none.

**Overengineering** — where, what, cost, simpler alternative. **Must list every abstraction evaluated** — even ones you kept. For each: name, consumer count, verdict (keep/remove/inline), one-line justification.

**File Organization** — oversized folders (path, count, suggested split), misplaced files. Skip section only if genuinely clean.

**Alternative Approaches** — current approach vs proposed alternative, trade-off, effort. **Must have at least one entry per non-trivial file.** If current approach wins, state why concretely.

**Verdict**: **Sound** / **Minor issues** / **Overengineered** / **Rethink**. Default assumption is **not Sound** — must earn Sound verdict by finding nothing across all four concerns.

**Must act on findings:**

- **Minor issues** → apply fixes automatically (inline fixes only — no new files, no public-API changes).
- **Overengineered / Rethink** → ask via `AskUserQuestion` with three options:
  - **Apply inline** — make the fixes now (expect re-test by caller).
  - **Defer to plan** — write `plans/post-audit-{slug}.md` using `plan-template.md` from the implement skill directory; turn each finding into a Task with `**Files:**`, `**Acceptance:**`, and the audit's recommended fix as `**Context:**`. Report the plan path.
  - **Skip** — note in report only, no action.

Do not just report and move on.

## Step 5: Rule Candidates

After reporting, scan the findings for patterns that would generalize. Boundary violations, overengineering flags, and simpler-alternative preferences often hint at architecture rules worth codifying. Per `wf-surface-rule-candidates.md`, log up to 2 candidates via `/rule-candidate` and include the standard report block. Skip if nothing qualifies — don't fabricate.

## Project rules

Additional project-specific architecture rules to apply alongside the global set. Projects layer a `<ProjectSpecific>` block here listing their `arch-*` rules from `.claude/rules/`.
