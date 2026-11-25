---
name: ux-design
description: UX design for a feature — user flows, screens and their states (empty, loading, error, success), accessibility requirements (WCAG keyboard, focus, contrast, ARIA) and design-system component references, as a ux-spec handed to develop. Use to design the user experience, flows, screens, wireframe specs or accessibility. Not the technical architecture (architecture), implementing it (develop), or the PRD (product).
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
---

# UX design (phase workflow)

Turn a feature (or PRD) into a **UX spec**: the user flows, the screens and their states, the
accessibility requirements, and the design-system components to reuse — handed to `develop`. This
is the *user* experience, distinct from `architecture` (the *technical* design). Outputs are
**specs and handoff docs, never pixels** — keep visual/brand design out of scope. (Design: ADR 0023 and
`docs/architecture/design-onboarding.md` in the agentic-forge repository — not shipped with the
plugin.)

## When to use

When the task is to design the user experience for a feature — flows, screens and states, or
accessibility. **Not** the technical architecture (`architecture`), building it (`develop`), or
the product requirements (`product`).

## Process

> **Deliver in isolation** — when a `<feature-slug>` is in play, write into the feature's
> shared documentation worktree rather than the checkout, and deliver the result as a pull
> request (see [doc-delivery](../../patterns/doc-delivery.md)). One worktree and one PR per
> **feature**, shared by every document phase — that is what lets the next phase read what
> this one wrote. Skip it for a one-off document outside a feature flow. A repo with no remote (or
> no `gh`) still commits — on `docs/<slug>`, reported as not pushed / no PR — never a failed phase.

> **Write where the repository keeps its features** — run
> `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" artifact-home --repo <worktree> --slug <feature-slug> --kind ux`.
> Its `feature_dir` is `<feature-dir>` below (`docs/sdlc/<feature-slug>` only when the repository
> keeps no feature folder for it), and `documents.<kind>` (`research`, `prd`, `design`, `plan`,
> `ux`) gives each document's `abs` path. **Never put a path on a command line yourself:** run
> the commands it prints (`documents.<kind>.commands.*.shell`) verbatim, and where a call below shows
> `<path>`, use that document's `arg` (absolute, already quoted). A document or ADR directory with
> `unsafe` set (a symlink, or something other than a regular file, at or on the way to its path) is
> never written: stop and report it. On `ambiguous`, ask when interactive; headless, take its pick
> and record it as an assumption naming the alternatives
> ([where a feature's documents go](../../patterns/handoff.md#where-a-features-documents-go)).

1. **Read the feature.** Load the feature description / `prd.md`; identify the actors and the jobs
   to be done.
2. **User flows.** Map the key flows (happy path plus the important branches) as step sequences —
   not screens-as-pictures.
3. **Screens and states.** For each screen, specify its states: **empty, loading, error, and
   the populated/success** state — the ones engineers forget. Describe content and behavior, not
   visual layout.
4. **Accessibility.** State concrete WCAG requirements: keyboard navigation and focus order,
   contrast, semantics/ARIA (e.g. live regions for async results), labels for inputs.
5. **Design system.** Reference the components/tokens to reuse (don't invent a visual language).
   When the spec is handed to engineering, load
   [references/design-handoff.md](references/design-handoff.md) — the per-component handoff
   template (tokens, variants, ALL states incl. focus/disabled/error, ARIA/keyboard) and the
   5-minute accessibility pass.
6. **Write the `ux-spec`** with valid YAML frontmatter: `type` (= `ux-spec`), `feature`, `status`,
   `review_decision: revise` until the loop exits, and the **list** fields `flows`, `screens`, `accessibility`, `design_system` (each a YAML list —
   not prose; quote any value containing a colon) — as `ux-spec.md` at `documents.ux.abs` (in
   `<feature-dir>/`), then validate it
   (the read-back below) — the input `develop` builds from.
   These fields are the whole schema: do not read `handoff.py` or `af.py` to learn them.
   Then **read the file back** — `documents.ux.commands.handoff_load.shell`, the printed form of `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type ux-spec` — and fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).
7. **Adversarial review (bounded).** Fork fresh `reviewer`s (via `Task`) on two lenses —
   **accessibility** (keyboard/focus order, contrast, ARIA/live-regions present and correct) and
   **flow/state completeness** (every screen has empty/loading/error/success; no dead-end flow) —
   verify each finding against the spec, then revise worst-first. These are exactly the states and
   a11y items engineers forget. **External reviewer lens (on by default, ADR 0057/0061):** when
   `external_reviewer.enabled` (settings), also run the external reviewer over the spec —
   `documents.ux.commands.external_review.shell`, the printed form of `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/external_review.py" --target <path> --repo <worktree> --kind ux`; codex critiques it as an independent-model lens over the same two concerns and its
   `findings` fold into the same worst-first revision. It **degrades gracefully** (absent/disabled
   codex is skipped, not a failure; **exit 3 is a failed lens**, not a skip — record it in the round and tell the user) and its findings are **advisory** (prompt-injectable) — verify
   before acting. **Persist each round** — one `review-<artifact>-<iteration>.md` per round in `<feature-dir>/` (`feature_abs`), aggregating **both** lenses; on `proceed` keep only the final round, on `escalate` keep them all (naming + lifecycle: [review-loop.md](../../patterns/review-loop.md)). **Exit criterion (the shared, tested rule):** each round, aggregate both lenses
   (plus the external one) to a single verdict and compute
   `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" review-decision --verdict <approve or changes> --iteration <n> --gate-green <yes if the ux-spec validates, else no>`
   (see [adversarial-review.md](../../patterns/adversarial-review.md), bounded by
   [review-loop.md](../../patterns/review-loop.md)) — `revise` (loop back and fix worst-first),
   `escalate` (still `changes` at N = 3 → **commit nothing; mark the feature PR a draft** (the merge gate already refuses a draft), set the artifact's `review_decision` to `escalate` (never touch its `status`, the repo's lifecycle field), surface the unresolved gaps and stop; that field is what makes "don't hand off" enforceable — the file is already on disk), or
   `proceed` (**commit this phase's artifact and push — opening or updating the feature PR per [doc-delivery](../../patterns/doc-delivery.md)**; `approve` **and** the spec validates → the spec is done). Don't hand off a spec with a
   dead-end flow or a screen missing its error state.

## Output

**A full ux-design run produces the finished spec: a validated `ux-spec`** — flows, screens +
states, accessibility requirements, and design-system references — that survived the bounded
adversarial loop to `proceed`, ready as the input `develop` builds from. No pixels or visual
mockups — specs only. A run whose loop `escalate`s (unresolved gaps at N = 3) surfaces them and
stops; it does **not** hand off an incomplete spec.

## Definition of done

- The adversarial loop exited on `proceed` (`review-decision`): `approve` **and** the `ux-spec`
  validates — not `escalate`.
- The key user flows and per-screen states (incl. empty + error) are specified.
- Concrete accessibility requirements are stated (keyboard, focus, contrast, ARIA).
- A bounded accessibility + flow-completeness review pass (plus the external-reviewer lens when
  enabled) was run before handoff.
- Output is a spec (a valid `ux-spec` artifact), not a visual/pixel mockup.
