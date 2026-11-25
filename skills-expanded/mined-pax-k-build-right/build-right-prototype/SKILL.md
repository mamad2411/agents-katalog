---
name: build-right-prototype
description: Answer one unresolved logic or UI design question with disposable executable evidence. Use for explicit prototype, spike, proof-of-concept, interaction experiment, state-model experiment, or design-experiment requests where observed behavior can reduce uncertainty before production feature planning.
---

# Build Right Prototype

Use this cross-cutting companion to answer one design question. A prototype is
evidence, not product code, customer validation, or permission to implement.

## Required Reading

- Read `references/logic.md` for state, transition, data-shape, or behavioral
  contract questions.
- Read `references/ui.md` for layout, hierarchy, or interaction questions.
- Use `assets/templates/prototype-evidence.md` for the retained evidence packet.
- Read the target repository's instructions, product authority, execution
  rules, and Git state before creating anything.

## Workflow

1. State exactly one prototype question and one observable success signal.
2. Classify the mode as `logic` or `ui`; stop if the question mixes unresolved
   concerns that cannot be observed together.
3. Inspect repository conventions and `git status --short`. Record unrelated
   work and do not touch it.
4. Create the prototype in a disposable temporary directory or detached
   temporary worktree. Never edit the main worktree by default. If neither safe
   isolation option is possible, stop and ask.
5. Make the prototype runnable with one documented Bun-native command such as
   `bun run prototype` or `bun index.ts`.
6. Run syntax, type, or build smoke verification appropriate to the prototype,
   plus the smallest assertion that proves the question's success signal.
7. Observe the result. Separate what was demonstrated from what remains
   assumed.
8. Write `docs/evidence/prototypes/<slug>.md` in the target repository using
   the evidence template. This retained packet is the only default main
   worktree edit.
9. Route any production implementation through
   `$build-right-feature-planning`. Never copy, move, or promote prototype code
   directly into production.

## Safety Contract

- Use fake, local, or read-only data. Never call a production mutation path.
- Do not use live credentials unless the user explicitly authorizes a bounded,
  non-mutating proof and repository policy allows it.
- Do not automatically commit, push, merge, publish, deploy, clean up, delete,
  or promote.
- Do not automatically abort or resolve an existing Git operation.
- Leave disposal or cleanup as an explicit user choice and report the temporary
  path or worktree.
- Label the finding `prototype-evidence` when observed and
  `prototype-assumption` when it remains inferred.

## Handoff

Prototype evidence may feed `$build-right-preflight` or
`$build-right-feature-planning`. It never upgrades itself to customer evidence
or product truth.

## User-Visible Status Badge

End every final response with exactly one status badge block:

```text
✅ [DONE] Status: DONE
Decision: <answer to the prototype question>
Next action: <planning handoff or none>
Needs user input: <none | concise ask>
Blocked by: <none | blocker>
```

Use `🟢 [GREEN] Status: ALL GREEN` while proof is safe to continue,
`🟡 [YELLOW] Status: NEEDS INPUT` for a required user decision,
`🟠 [ORANGE] Status: NEEDS WORK` for AI-owned proof gaps,
`🔵 [BLUE] Status: WAITING EXTERNAL` for external evidence, and
`🔴 [RED] Status: BLOCKED` for unsafe isolation, failed verification, or
conflicting evidence.
