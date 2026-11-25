---
name: migrate-aplwin-to-dyalog
description: Orchestrate evidence-based migrations from APL+Win (APL2000) workspaces or text exports to Dyalog APL using Dyalog's official migration tool first, followed by static compatibility review and differential or golden-output tests. Use for APL+Win `.w3` workspace migration planning, exported `.apl*` source conversion, APL+Win/Dyalog dialect compatibility analysis, migration fixture authoring, and behavioral-equivalence reports. Do not use for unrelated APL dialects or unverified direct LLM translation.
---

# Migrate APL+Win to Dyalog

Treat migration as a reproducible verification workflow. Preserve source artifacts and distinguish conversion evidence from harness self-tests.

## Workflow

1. Confirm the source is APL+Win. Look for `.w3`, `⎕WI`, `⎕WSELF`, double-quoted text, or APL+Win control structures. Stop and identify the actual dialect if evidence conflicts.
2. Create an isolated migration workspace. Never edit the source workspace, its export, or client code in place. Record hashes or a source revision.
3. Read [migration-workflow.md](references/migration-workflow.md). Use the official `Dyalog/migration` export and converter before proposing manual translations.
4. Pin the official tool revision in the run configuration. Reject an unexpected checkout revision rather than silently changing the baseline.
5. Run static review on the converted directory. Link each critical/high finding to a focused fixture or an approved exception.
6. Read [fixture-design.md](references/fixture-design.md). Prefer live differential execution. If APL+Win cannot be automated, capture reviewed golden observations and execute Dyalog live.
7. Compare return value, normalized type, shape, rank, nesting, empty prototype, error behavior, selected globals, and declared side effects. Use tolerance only when the fixture explicitly permits it.
8. Emit JSON and Markdown reports. State the evidence level: `live-differential`, `golden-vs-live`, or `frozen-selftest`.
9. Do not claim migration acceptance from source inspection or a frozen self-test. Require passing runtime evidence and manual review of GUI, files, external calls, and component-file behavior.

## Harness use

The skill is self-contained. Locate this `SKILL.md`, then run its sibling wrapper:

```text
python scripts/run_harness.py selftest
python scripts/run_harness.py review --source <converted-source-directory>
python scripts/run_harness.py run --config <config.json>
```

For a real run, begin from `config/example.real.json`. Keep `migration.backend` set to `official-dyalog`. Use `frozen` only for harness development and tests.

If the skill is installed globally, do not assume the current working directory is the skill directory. Resolve all bundled scripts and examples relative to this file.

## Patch discipline

- Patch only a copy of converted output.
- Make one behavior-motivated change at a time.
- Add a failing focused fixture before a manual compatibility patch when practical.
- Re-run the entire suite after every patch.
- Record unresolved differences; do not hide them with broad tolerances, text-only comparisons, or deleted observations.
