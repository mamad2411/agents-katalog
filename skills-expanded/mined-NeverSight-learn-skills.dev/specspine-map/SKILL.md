---
name: specspine-map
description: Map observed brownfield repository architecture into a linked Markdown SpecSpine. Use bounded mode by default for surveys, architectural questions, selected subsystems, local refresh, and drift. Use exhaustive mode only when the operator explicitly asks to recurse until the requested scope is saturated; it coordinates branch-affine producers when available or runs sequentially. Do not invent intended architecture, perform general integrity audits, implement changes, or claim code/spec conformance.
---

# SpecSpine Map

Select one execution mode before project discovery:

- Use **bounded mode** unless the operator explicitly requests exhaustive,
  recursive mapping through terminal depth or saturation. Repository size,
  whole-project scope, or the word “deep” alone does not authorize exhaustive
  orchestration.
- Use **exhaustive mode** only for explicit intent such as “continue until
  saturated”, “fully map every useful branch”, or an unambiguous equivalent.

## Resources

- Read [references/bounded-mode.md](references/bounded-mode.md) completely for
  both modes. It is the sole mapping operation contract.
- Read [references/spec-semantics.md](references/spec-semantics.md) before
  classifying claims or recording code/spec disagreement.
- Read [references/spec-format.md](references/spec-format.md) before creating,
  editing, or restructuring specifications.
- Read [references/mapping-method.md](references/mapping-method.md) before a
  substantial survey, refresh, or restructuring.
- Start new files from `assets/templates/` and omit empty sections.

## Bounded mode

Perform exactly one bounded mapping operation and stop at its reported
continuation or terminal refusal. Do not load exhaustive orchestration
instructions, create a frontier ledger, or start producers.

## Exhaustive mode

Explicit exhaustive intent approves repeated documentation writes and final
navigation normalization. It does not authorize changing accepted intent or
choosing among materially different canonical owners.

Before discovery, inspect callable capabilities already exposed by the
environment. Do not probe capability by starting a subagent.

- If a subagent-creation mechanism is exposed, read
  [references/orchestration.md](references/orchestration.md) completely and
  follow it as the sole parallel protocol.
- If no such mechanism is exposed, do not read that reference. Follow the
  sequential protocol below. Unrelated async or wait tools do not count.

### Sequential exhaustive protocol

1. Resolve repository and Spine roots, existing intent, and one evidence
   baseline. Create a unique temporary run root outside the Spine with
   `mktemp -d`, then initialize:
   `python3 <map-skill-root>/scripts/frontier.py init
   <run-root>/frontier.json --scope <operator-scope> --root-question
   <root-question>`. Resolve `<map-skill-root>` as this `SKILL.md` directory.
   Resume an explicitly supplied preserved ledger after auditing it without
   `--final`. Reconcile it with the live Spine and rerun the checker. Delete no
   prior staging files; treat them as untrusted and unpublishable. Run
   `frontier.py resume --compact <ledger>` to release stale non-root owners;
   preserve only the active root. Create fresh staging if needed, reassign each
   branch to a new producer or `local`, and restart recorded questions. If
   reconciliation is ambiguous, mark the branch `blocked` and request direction.
2. Apply one bounded mapping operation at a time directly to the live Spine.
   Record every observed independent branch in the frontier before continuing.
   Before processing a queued branch locally, assign it with `--owner local`.
   Continue same-boundary and ready adjacent branches until each reaches the
   bounded protocol's terminal refusal. A refusal closes only its exact branch.
3. Before a coherent write, reserve every exact destination with
   `frontier.py reserve --compact <ledger> <branch-id> --path <path>`, adding
   `--replace-existing <path>` only for an approved replacement. After writing,
   record each changed path with `frontier.py publish --compact <ledger> <branch-id>
   --path <path>`; repeat `--path` per file. Then run
   `python3 <map-skill-root>/scripts/check_spine.py <spine-root> --json`;
   resolve errors before
   continuing. Execute and inspect each state mutation, write, and check
   separately; never chain them in one shell or continue after a nonzero exit,
   an `error` object, or nonempty checker JSON. Do not create producer staging
   when no producer exists.
4. Mark branches `locally_saturated` only with exact refusal reasons and
   `complete` only after their children complete. Repeat scope-level discovery
   after the ready queue drains and record it with `frontier.py discovery-pass
   --compact <ledger> --evidence <signals-checked>`. Before normalization require
   `python3 <map-skill-root>/scripts/frontier.py audit
   <run-root>/frontier.json --final` to print `[]`.
   Never end an exhaustive turn merely to report progress. A final response is
   permitted only after that clean final audit or when only concrete `blocked`
   branches remain and operator input is required.
5. Normalize navigation once and rerun the checker. Require
   `finalize_run.py <ledger> <spine-root>` to return `status: finalized`, then
   remove only the exact run root with `find <run-root> -depth -delete`. On
   interruption, preserve it and report the ledger path.
6. Report scope, changes, relationships, unresolved drift, limitations, and
   exact terminal reasons. Include the literal phrase `no useful node` and
   recommend `$specspine-doctor` in a new session. Never invoke Doctor during
   exhaustive Map. If only `blocked` branches remain, stop without claiming
   saturation, preserve the run root, and report each exact unblock condition.
