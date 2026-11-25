---
name: arbitrage
description: Always active when coding in a Claude (Fable) session. Triggers whenever implementation work is being planned, scoped, or about to start — before writing any code — to decide where each piece of work executes.
---

# Arbitrage

Fable tokens are expensive; the user's codex quota sits unused. Exploit the price gap: spend Fable tokens on judgment — planning, specs, design intent, visual validation — and spend codex quota on all code-writing volume.

**You ARE the Fable session.** "Here" means you do it yourself. There is no separate Fable to delegate to.

## Routing Table

| Work | Where | Why |
|------|-------|-----|
| Planning, specs, architecture decisions | Here | Judgment is what Fable is paid for |
| **ALL implementation — backend, frontend, anything that writes code** | codex via `/goal` | Quota is free; typing code is not where Fable adds value |
| Visual validation of UI work (run the app, screenshot, judge, iterate) | Here | Fable's design eye is worth the price — validate, don't type |
| Investigation and debugging analysis (root-causing hard bugs) | Here | Judgment work; the resulting fix dispatches with a precise spec |
| Diff review, commits, pushes, PRs | Here | Git operations stay under your control |
| Trivial edits riding along with review/validation (one-liners, any layer) | Here | Dispatch overhead exceeds the work |
| Work codex has demonstrably struggled with | Here | Escape hatch — see below |

## Dispatch Protocol

1. **Spec first.** Write a spec file in the worktree: objective, constraints, files/areas involved, acceptance criteria — the exact test command that must go green — and what NOT to touch. For frontend work the spec carries the design intent: layout, states, interactions, spacing, motion, reference patterns. For the hardest parts, spec down to pseudocode — the thinking stays here; the typing still dispatches.
2. **Dispatch in the background and keep working:**
   ```bash
   codex exec --cd <worktree> "/goal <one-line objective; details in SPEC.md>"
   ```
   codex runs gpt-5.5 with xhigh reasoning (its default config); it implements and gets tests green in the isolated worktree while you continue planning/spec/validation work in parallel.
3. **Review the diff here.** Commit, push, and open PRs from this session.

## Visual Validation Loop (frontend)

1. codex implements the UI per spec.
2. Run the app here — interact, screenshot, judge against the design intent.
3. Write concrete visual feedback (what's off, by how much, what good looks like) and re-dispatch.
4. Loop until it looks right; then diff review + git here.

## Escape Hatch: When codex Struggles

Struggle must be **observed, not predicted**. Always dispatch first — predicting "codex can't do this" just means the spec needs pseudocode-level detail. But two strikes and it's yours: if a re-dispatch with concrete corrective feedback still comes back missing the acceptance criteria or mangling the approach, stop re-dispatching and write the code here yourself, salvaging whatever of codex's diff is sound.

## Red Flags

| Thought | Reality |
|---------|---------|
| "Frontend is design-critical, so I'll code it here" | Fable's taste shows up in the spec and the validation loop, not in typing JSX. Dispatch it. |
| "Faster to just write it myself" | Premium tokens on rote work. Spec it, dispatch it, validate in parallel. |
| "This part is too hard for codex" | Predicted struggle is not observed struggle. Spec it at pseudocode level and dispatch; you only take over after two failed rounds. |
| "I'll let codex commit and push" | Review the diff and run git from this session. |
| "No time to write a spec" | An unspecced dispatch comes back wrong and costs more Fable tokens to fix than the spec would have. |

## Common Mistakes

- Dispatching without acceptance criteria → codex returns "done" with red tests. Always name the test command that must pass.
- Dispatching frontend work without design intent in the spec → generic UI comes back; the validation loop burns rounds recovering what the spec should have said.
- Blocking on codex → run it in the background; keep doing planning/spec/validation work in parallel.
- Splitting one coherent unit across dispatches → pick one owner per unit; split at the API boundary, not mid-feature.
