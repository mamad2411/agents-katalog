---
name: modularity-review
description: >-
  Reviews and reduces structural complexity: shallow layers, leakage,
  public-surface size, reversed dependencies, over-abstraction,
  scattered error mapping, hard-to-test handlers or components, and
  architecture cosplay. Use when a file or module is a mess, hard to
  test, or the same change lands in many places; for a PR/diff
  structure review; or for a refactor that moves code across modules.
  Do not use to decide whether units should stay together or split —
  that is cohesion-locality. Do not use for ordinary bug fixes,
  formatting, naming-only cleanup, or local edits that do not affect
  structure.
metadata:
  targets: [claude, cursor, codex, agents]
---

# Modularity Review

This skill independently owns **complexity at the public surface**: depth, leakage, dependency direction, testable seams, and architecture cosplay. `cohesion-locality` owns boundary judgment; `module-structure` is an optional selector, not a prerequisite or a source of working rules for this skill.

## Goal

Reduce code complexity without architecture cosplay. Prefer a deep module: small, stable public surface, large hidden payoff, clear dependency direction. Prefer the smallest restructuring that materially improves understanding, change, and testing; consider broader designs when the task warrants them. The request's language is not a signal: the same code gets the same analysis in any language, and the reply uses the user's language.

## Principles and boundaries

Use these as defaults, adjusting depth and sequence to the user's task. Exploration may compare speculative architectures or broader changes; distinguish those ideas from evidence-backed recommendations for this codebase.

- Inspect relevant code, callers, and conventions to ground findings. When code is unavailable, offer conditional guidance and identify assumptions instead of claiming a verified defect.
- Prefer abstractions that hide meaningful knowledge or relieve coupling and testing pressure. Layers, interfaces, DI, and thin adapters are options whose value depends on their contract and cost, not on implementation count alone.
- Consider moving knowledge to its owner or removing a redundant facade before adding machinery. Prefer a local solution when it solves the problem; broader alternatives are useful when the evidence or requested exploration warrants them.

Respect user scope and applicable hard project rules. Review and design do not authorize implementation or unrelated documentation changes. Preserve behavior and public contracts unless their change is authorized. Existing implementation authorization remains valid when another analysis is needed; continue without requesting it again. Report evidence and validation honestly.

## Boundary input

Use established ownership, boundary conclusions, evidence, and constraints as input. When a split/join question or independent change axes leave ownership unclear enough to affect a recommendation, use `cohesion-locality` when available to examine that question. A one-sentence responsibility is a clue, not a completion gate. Pause only the recommendation that depends on the answer; continue unaffected analysis.

Bring the boundary result or remaining uncertainty back into the requested surface work, retaining the task's scope, contracts, and current mode. Include material boundary findings in the same report without forcing them into a surface-complexity score. Reuse inspected evidence; reconsider a boundary only when new evidence, a useful counterexample, or an exploratory alternative could change the judgment. If the same question remains unresolved without new information, state the limitation and proceed with supported work; ask when a consequential missing answer blocks progress.

When a companion is unavailable, complete supported analysis or conditional design exploration and identify the limitation without claiming to have used it. Treat unverified cuts as hypotheses. No return to the selector is needed.

## Core vocabulary

When terminology matters or you produce a report, use: module, public surface, implementation, depth, shallow module, seam, leakage, change amplification, architecture cosplay, recommendation strength. Definitions in `references/language.md`. Prefer the repo's own word when it has one.

**Responsibility**, **cohesion**, and **change axis** belong to cohesion-locality's boundary vocabulary.

## Orient the review

The main agent first reads the root and nearest applicable `AGENTS.md`, relevant architecture/ADR guidance, and applicable project-local `SKILL.md` files identified from their descriptions. Apply them during design as well as review; do not merely forward unread paths. If a project skill requires specialized review, the main assigns one dedicated fresh-context reviewer for that domain and scope, reusing an existing assignment if present. That reviewer reads the source rules itself, reports evidence, and does not delegate further.

Use the following questions as a starting point, not a fixed inspection sequence.

1. Inspect first: folder layout, naming, import direction, nearby similar features, test style, public exports, and existing error/validation conventions.
2. For relevant boundaries, consider: What does it own? What should it hide? What is its public surface? Who imports it? What does it import? Can it be tested without booting the whole app?
3. Read project context when a recommendation is broad or moves code across modules — see `references/decision-records.md`.

Judge complexity by whether future changes get harder: change amplification, cognitive load, unknown unknowns, obscurity. Load `references/red-flags.md` or `references/principles.md` by section — do not recite them. Brief boundary observations can remain in this review; use the boundary input guidance when a recommendation needs deeper ownership reasoning.

## Mode selection

| Mode | Use when | Output |
| --- | --- | --- |
| **A — Fast review** | Review a file, diff, PR, module, route, component, or small area. | Findings ordered by risk. No candidate cards. |
| **B — Friction scan** | Scan for shallow layers, leakage, reversed deps, or a top recommendation. | Candidate cards + top recommendation. |
| **C — Candidate deepening** | A candidate is chosen, or the user asks to design a public surface. | Owns/hides/surface + design comparison. |
| **D — Implementation** | The user asks the agent to actually refactor. | Smallest behavior-preserving change + validation. |

Default to the smallest mode that fits the requested deliverable: A/B for review, C for surface design, D only for implementation already requested in the conversation. A broad task can span B → C → D within that scope. A boundary result supplies input to the current mode; a keep-together decision can still support an authorized surface simplification.

### Review execution (Modes A/B)

When a manual review request leaves its scope unspecified, the main asks one concise scope question and waits before reviewing code or dispatching reviewers: uncommitted changes, the latest commit or a specified commit range/PR, or a named project/module (these are suggestions, not an exhaustive menu). Reuse any scope already clear from the current or prior conversation, including the parent's assignment; ask only for missing details. Resolve the repository/path and revisions from the answer: uncommitted includes staged and unstaged changes plus relevant untracked files; the latest commit means its diff from its parent; “recent commits” needs a count or range; project/module review covers the named area, not an assumed diff. Do not silently choose HEAD~1, the current repository, or the whole project when those choices are unresolved. Only the main asks; reviewers receive the resolved scope. A bare skill invocation with unclear design-versus-review intent needs a task clarification, not an automatic diff review. Design requests remain design requests.

Use parallel subagents when available and useful for independently inspectable areas or a consequential contract needing an independent read. Choose by responsibilities, coupling, and risk, rather than line count or a fixed reviewer quota; a focused review can stay with the main agent. Before delegating, read [Parallel review](references/review-report.md#parallel-review). Each reviewer reads this entrypoint and the complete core [principles](references/principles.md); read cohesion-locality in full when ownership judgment is needed and it is available. One main agent verifies and synthesizes results in the original mode. Delegated reviewers report to that main without spawning further reviewers. This mechanism does not automatically activate for Mode C design or Mode D implementation.

### Mode A: Fast modularity review

Inspect the code and report findings ordered by risk. A useful finding connects the following; adapt the format to the task:

- **Impact and confidence** — tie priority to an observed cost, demonstrated risk, or applicable contract. A possible future problem is an exploration hypothesis, not automatically a medium-severity defect. Keep confidence distinct from impact when evidence is incomplete.
- **File/line** if available.
- **Why it increases complexity** — name the mechanism (leakage, shallow module, reversed dependency, architecture cosplay) or the supported boundary issue.
- **Smallest useful fix** — behavior-preserving; prefer move-to-owner or delete facade.
- **What not to change** — only when there is a real over-refactor risk.

Concise findings are the default. Use another format when requested or when it materially improves the explanation; HTML is opt-in.

### Mode B: Architecture friction scan

Explore the area for surface/leakage/shallow friction, then produce a candidate report using `references/review-report.md`:

- Lead with the most useful conclusion, including when no material change is warranted.
- Usually a few worthwhile candidates, connecting: current friction (grounded in real code), why complexity increases, smallest useful fix, before/after sketch, testing impact, what not to change, and recommendation strength (Strong | Worth exploring | Speculative).

Markdown is the default. HTML is opt-in. If the request ends at a scan, present the recommendation. If it includes further design or implementation, continue within that scope; ask only when a consequential unresolved choice needs user input.

### Mode C: Candidate deepening design

Use after the user selects a candidate, after cohesion-locality has chosen a cut, or when asked to design a public surface. Useful elements, scaled to the decision:

1. What the module **owns**.
2. What it **hides**.
3. The **public surface**.
4. **Example caller code** — the smallest realistic call site.
5. The **tests that should survive** unchanged (the behavior contract).
6. What **not** to refactor.
7. **Materially different alternatives** when they clarify a nontrivial tradeoff; no quota.
8. **A recommendation**, with its reason and any consequential uncertainty.

Load `references/interface-design.md` for the comparison. Comparing designs is not a license to add interfaces — the minimal surface often wins.

### Mode D: Behavior-preserving implementation

- Make the **smallest behavior-preserving change** that realizes the chosen design.
- Do not silently change public APIs.
- Update imports carefully; do not move code without checking callers.
- Keep unrelated cleanup out of the change.
- Carry the "what not to change" guardrail through.
- Then validate.

Close with: what changed, why the structure is better, what checks were run, and remaining risk. For tiny changes, collapse this into a short paragraph.

## Validation

After edits, run project-required checks and validation relevant to the affected behavior and boundaries. Depending on the change, that may include behavior tests, typecheck, lint, or import checks. Inspect the final diff for unintended scope or contract changes. State which checks ran and any validation limits; availability alone is not a reason to run every tool.

## Reference loading

Use progressive disclosure. Reach for `rg` (or the Grep tool / `grep`); if the right section is not obvious, list headings first with `rg '^## ' references/*.md`, then read only the matching range. Do not recite references — apply them to the code at hand.

- `references/principles.md` — depth, information hiding, dependency direction, abstraction discipline. Not stay-together.
- `references/red-flags.md` — suspected surface/leakage/cosplay problems; skip change-axis ownership flags.
- `references/examples.md` — concrete restructurings when no nearby project pattern is enough.
- `references/language.md` — vocabulary for reports.
- `references/review-report.md` — Mode B candidate format.
- `references/interface-design.md` — Mode C design comparison.
- `references/decision-records.md` — project context before broad recommendations.
