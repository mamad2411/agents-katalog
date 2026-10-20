---
name: consolidate-into-sulis
description: "Folds a separate plugin into the Sulis plugin using the proven recipe."
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  processing: [CRITICAL_THINKING_STANDARD, DECOMPOSITION_PROCEDURE]
  output: [CRITICAL_THINKING_STANDARD]
verification_spiral:
  tier: heavy
  template_base: HEAVY_TIER_DEFAULT
  custom_dimensions:
    - name: "Recipe Self-Consistency"
      threshold: ">= 4/5"
      standard_reference: "this SKILL.md applied to the sulis-execution → sulis precedent commits (02c1e77..fa882b1) — every gate must map to a real commit move"
      principle_reference: "CRITICAL_THINKING_STANDARD BI-01 (counter-search: does the recipe cover what the precedent actually did?)"
      scorer: external_sub_agent
    - name: "Code-Health Gate Effectiveness"
      threshold: ">= 4/5"
      standard_reference: "Gate 0 baseline + Gate 6 verification must catch the kinds of regression a real consolidation produces (path drift, broken imports, ref rot, coverage drop)"
      principle_reference: "CRITICAL_THINKING_STANDARD AT-01 (adversarial: name the regression types and verify each is caught)"
      scorer: external_sub_agent
related_skills:
  - relationship: depends_on
    skill: ../add-skill
    notes: consolidate-into-sulis was authored via add-skill v0.7.0
  - relationship: related_to
    skill: ../add-agent
    notes: sibling meta-skill; both encode marketplace authoring/migration discipline
  - relationship: depends_on
    skill: ../code-health
    notes: invoked by Gate 0 (baseline) and Gate 6 (verification)
  - relationship: depends_on
    skill: ../../references/standards/CRITICAL_THINKING_STANDARD.md
    notes: cited at Gate 0 (inventory + plan) and Gate 6 (verification)
  - relationship: depends_on
    skill: ../../references/standards/DECOMPOSITION_PROCEDURE.md
    notes: cited at Gate 0 for primitive-level planning
  - relationship: depends_on
    skill: ../../references/standards/SPIRAL_TEMPLATES.md
    notes: VERIFICATION_REPORT.md template; HEAVY tier dimensions
  - relationship: depends_on
    skill: ../../references/standards/REFERENTIAL_INTEGRITY_STANDARD.md
    notes: cross-skill ref integrity is the highest-risk failure mode at Commit 4
---

# Consolidate Into Sulis

## Conclusion (Pyramid Principle — lead with the answer)

A runbook for folding a specialist plugin into the `sulis` plugin via the proven **5-commit recipe + 2 verification gates**. Mirrors the sulis-execution → sulis migration (commits `02c1e77` through `fa882b1`, ~50 files moved, 5 commits, 0-finding self-test) — codified so the four upcoming consolidations (sulis-context, sulis-security, sea, srd) follow the same shape without reinvention.

Verify the precedent at any time with `git log --oneline 02c1e77^..fa882b1` (5-commit chain) and `git log --stat 02c1e77^..fa882b1` (~50 files moved across the chain).

The output of running this skill is one merged consolidation:

1. The source plugin's contents under `plugins/sulis/` (history preserved via `git mv`)
2. The source plugin's directory marked `[DEPRECATED]` (no shim skills — directory stays as shell per sulis-concierge + sulis-execution precedent)
3. Every external reference updated (`plugins/{source}/` paths, `subagent_type` dispatches)
4. Every founder-visible incoming skill name passes the **tin test** (verb-noun or otherwise self-describing — bare verbs like `decompose` / `harden` / `probe` renamed)
5. `/sulis:code-health` clean on the migrated tree (or all regressions fixed forward)
6. Sulis metadata bumped (`plugin.json` + `CHANGELOG.md` + `marketplace.json`)
7. `VERIFICATION_REPORT.md` on disk for the consolidation run under `plugins/sulis/skills/consolidate-into-sulis/runs/{source-plugin}-{YYYY-MM-DD}/`

If you have not read `references/methodology.md`, read it once. It explains why each gate exists and what failure mode it prevents.

## What this is NOT

- **Not a one-off migration script.** Each consolidation is reviewable as 5 commits; the recipe doesn't auto-execute commits without operator verification between them.
- **Not a deprecation-shim creator.** Source plugins are marked DEPRECATED outright; no shim skills get written (per sulis-concierge precedent).
- **Not a rename-existing-sulis-skills pass.** The tin-test rename applies to incoming skills only — existing sulis plugin names (`retry`, `handoff`, etc.) are out of scope here.
- **Not a multi-plugin batch tool.** One source plugin per run. For the four-plugin Phase 3 plan, run the skill four times sequentially (sulis-context → sulis-security → sea → srd).

## The recipe — 5 commits + 2 verification gates

> **Step numbering note.** This recipe labels commits `step 1/5` through `step 5/5`. The sulis-execution precedent used a `step N/8` labelling (its plan had 8 logical sub-tasks, but the final three were bundled into the wrap-up commit). This recipe aligns step numbers to commit numbers for operator clarity.

| Step | Output | Pass criteria summary |
|---|---|---|
| **Gate 0** — Inventory + Plan + Baseline | `CONSOLIDATION_PLAN.md` + `code-health-baseline.json` | Plan covers all moves; baseline captured |
| Commit 1 — scripts + tests + CI | scripts/, tests/, CI workflow moved | `plugins/{source}/scripts/` empty; CI YAML updated |
| Commit 2 — skills (with tin-test rename) | skills/ moved, renames applied | `plugins/{source}/skills/` empty; founder-visible names pass tin test |
| Commit 3 — agents | agents/ moved, subagent_type sweep done | `plugins/{source}/agents/` empty; every dispatch updated |
| Commit 4 — references + external ref sweep | references/ moved, all repo-wide refs updated | `plugins/{source}/references/` empty; `git grep "plugins/{source}/"` returns no non-deprecated hits |
| Commit 5 — wrap-up | docs/ moved, DEPRECATED markers set, sulis bumps | source plugin marked DEPRECATED; `plugin.json` + `CHANGELOG.md` + `marketplace.json` updated |
| **Gate 6** — Code-health verification | `code-health-final.json` | No regression vs Gate 0 baseline (or fix-forward Commit 6 lands clean) |

Each gate has explicit pass criteria. Operator verifies between gates. Do not batch commits — atomic commits preserve reviewability + rollback.

## Preconditions

- Working tree clean (no uncommitted changes)
- On a feature branch (auto-create from `main` or `dev` if needed)
- `git`, `python3`, `jq` available on PATH
- Source plugin exists at `plugins/{source-plugin}/`
- Target is always `plugins/sulis/`

## Gate 0 — Inventory + Plan + Baseline (no commit)

**Standards:** BI-01..04 (counter-search), PG-01..04 + PD-01..06 (primitive decomposition of the work).

### Sub-step 0a — Inventory the source plugin

```bash
RUN_DIR=plugins/sulis/skills/consolidate-into-sulis/runs/{source-plugin}-$(date +%Y-%m-%d)
mkdir -p "$RUN_DIR"

python3 plugins/sulis/skills/consolidate-into-sulis/scripts/inventory.py \
  --marketplace-root . \
  --source-plugin {source-plugin-name} \
  > "$RUN_DIR/inventory.json"
```

Produces JSON with every file in the source plugin grouped by category (scripts, skills, agents, references, docs, CI workflows, manifest files, metadata files).

### Sub-step 0b — Detect collisions + tin-test failures

```bash
python3 plugins/sulis/skills/consolidate-into-sulis/scripts/detect_collisions.py \
  --marketplace-root . \
  --target-plugin sulis \
  --inventory-json "$RUN_DIR/inventory.json" \
  > "$RUN_DIR/collisions.md"
```

Produces Markdown listing:

- Direct name collisions (incoming skill / agent / reference with same name in sulis)
- Tin-test failures (incoming skills with bare verbs or internal-jargon acronyms — founder can't decode from name alone)
- CI workflow rename candidates

See `references/conflict-resolution.md` for the rename rubric.

### Sub-step 0c — Find external references

```bash
# inventory.json's `.agents` field is a sorted array of agent .md filenames
# (e.g., ["context-cartographer.md"]). The jq strips `.md` for the search.
AGENT_NAMES=$(jq -r '.agents | map(sub("\\.md$"; "")) | join(",")' "$RUN_DIR/inventory.json")

python3 plugins/sulis/skills/consolidate-into-sulis/scripts/find_external_refs.py \
  --marketplace-root . \
  --source-plugin {source-plugin-name} \
  --agent-names "$AGENT_NAMES" \
  > "$RUN_DIR/external-refs.md"
```

The script catches both absolute (`plugins/{source}/`) and relative (`../{source}/`, `../../{source}/`, etc.) path references. Verified during smoke-test against sulis-context: surfaces refs in `related_skills:` blocks (which use relative paths) as well as in CLAUDE.md and other absolute-path citations.

Produces Markdown listing every line in the marketplace that cites `plugins/{source-plugin}/` paths or dispatches the source plugin's agents via `subagent_type`. Every line needs updating during Commits 2-4.

See `references/external-ref-sweep.md` for the 12-category sweep checklist.

### Sub-step 0d — Capture code-health baseline

```bash
# Subprocess-only deterministic baseline (no Agent dispatch, no token cost).
# Important: discard stderr so the orchestrator's progress line
# ("code-health: tiers_walked=…") does not pollute the JSON stream.
python3 plugins/sulis/skills/code-health/scripts/orchestrator.py \
  --mode fast --raw --scope codebase --repo-root . \
  2>/dev/null > "$RUN_DIR/code-health-baseline.json"
```

If invoking the code-health skill via the Claude Skill tool instead of the
orchestrator directly, save its `--raw` output to the same path.

This is the pre-consolidation state. Gate 6 compares against this. See `references/code-health-gating.md` for the comparison rubric.

### Sub-step 0e — Write CONSOLIDATION_PLAN.md

Using `templates/CONSOLIDATION_PLAN.md.template`, produce a commit-by-commit plan at `$RUN_DIR/CONSOLIDATION_PLAN.md` covering:

- Inventory summary
- Direct collisions + resolution strategy
- Tin-test failures + rename mappings
- External ref sweep checklist
- Code-health baseline reference
- Per-commit checklist

**Pass criteria for Gate 0:**

- Inventory JSON produced; no errors
- Collisions Markdown produced; every collision has a resolution strategy in the plan
- External refs Markdown produced; every line categorised in the plan
- Code-health baseline captured at `$RUN_DIR/code-health-baseline.json`
- CONSOLIDATION_PLAN.md exists; all checklist sections complete (no TBD)

## Commit 1 — Scripts + tests + CI workflow

**Standards:** REFERENTIAL_INTEGRITY (paths cited from scripts must continue to resolve).

> **No-op handling.** If the source plugin has no scripts, tests, or CI workflows (verified by `find plugins/{source}/scripts -type f` returning empty AND `ls .github/workflows/{source}*.yml` returning no match), **skip this commit entirely** and resume at Commit 2. Document the skip in CONSOLIDATION_PLAN.md and VERIFICATION_REPORT.md. The recipe step-numbering preserves Commit 1 as a placeholder for the consolidation chain's audit trail.

```bash
# Move scripts (preserves git history)
git mv plugins/{source}/scripts/* plugins/sulis/scripts/

# Move CI workflow with rename (keep source qualifier)
git mv .github/workflows/{source}-tests.yml .github/workflows/sulis-{qualifier}-tests.yml
# Edit the workflow YAML to point at new paths (see CONSOLIDATION_PLAN.md)

# Verify source is empty of scripts
find plugins/{source}/scripts -type f
# Should return empty
```

**Edit pass.** Open every moved script + the CI YAML. Update any internal path that cited `plugins/{source}/`. Common categories (see `references/external-ref-sweep.md`):

- shebang and `sys.path.insert` lines
- cache paths
- dev fallback paths
- plugin install path lookups

```bash
git commit -m "chore(sulis): step 1/5 — move {source} scripts + tests + CI into sulis"
```

**Pass criteria:**

- `plugins/{source}/scripts/` directory does not exist (or is empty)
- New files exist at `plugins/sulis/scripts/`
- CI workflow at `.github/workflows/sulis-{qualifier}-tests.yml` references new paths
- Local test invocation works (`python3 plugins/sulis/scripts/tests/...` or equivalent — no broken imports)

## Commit 2 — Skills (with tin-test rename pass)

**Standards:** REFERENTIAL_INTEGRITY (skill refs to other skills must continue to resolve); tin-test rubric in `references/conflict-resolution.md`.

```bash
# Move each skill — applying rename if CONSOLIDATION_PLAN.md says so
git mv plugins/{source}/skills/{skill-name}/ plugins/sulis/skills/{new-or-same-name}/
# Repeat for each skill
```

**Edit pass.** For each moved skill, update:

- SKILL.md `description:` field (if name changed, the description text may need rewording — descriptions often cite the skill name)
- SKILL.md `related_skills:` paths (now under sulis)
- Any `cache path` references inside scripts
- Any `subagent_type:` references (likely deferred to Commit 3, but flag here)
- Internal cross-skill references (e.g., `see /sulis-context:discover` → `see /sulis:discover-context`)

```bash
git commit -m "chore(sulis): step 2/5 — move {N} {source} skills into sulis (with {M} tin-test renames)"
```

**Pass criteria:**

- `plugins/{source}/skills/` directory does not exist (or is empty)
- All renames in CONSOLIDATION_PLAN.md applied; no operator-vocab leak in founder-visible names
- `git grep "/{source}:" plugins/sulis/` returns no hits in moved skills
- No tin-test failures remain (re-run detect_collisions.py against the migrated tree to confirm)

## Commit 3 — Agents (with subagent_type sweep)

```bash
# Move agent files
git mv plugins/{source}/agents/{agent-name}.md plugins/sulis/agents/{agent-name}.md

# Repo-wide sweep for subagent_type references — use find_external_refs.py output
# Edit each cited file to update plugins/{source}/agents/{name} → plugins/sulis/agents/{name}
```

```bash
git commit -m "chore(sulis): step 3/5 — move {source} agents into sulis"
```

**Pass criteria:**

- `plugins/{source}/agents/` empty
- `git grep -E "subagent_type[=:].*{agent-name}"` returns no hits citing old plugin
- Agent dispatch from the Sulis agent still works (manual smoke test: invoke once to confirm)

## Commit 4 — References (with external ref sweep)

**This is the highest-risk commit** because cross-plugin references can be cited from anywhere — CLAUDE.md at the repo root, other plugins' references, the Sulis agent itself.

> **Move-then-sweep ordering (v0.1.2 — non-negotiable).** Move ALL source-plugin content (skills + agent + references + docs) **before** running the bulk sweep. If the sweep runs while content is still in the source plugin's directory, that directory is excluded from the sweep, and any self-references inside the about-to-move content survive untouched into the new location — requiring fix-forward commits. The sea consolidation surfaced this bug twice (engineering-architect.md had 24 unswept `/sea:*` refs; 5 references had 24 collective unswept refs) before this discipline was encoded.
>
> The right sequence:
>
> 1. Move ALL content (Commits 1, 2, 3 + the reference moves in Commit 4) — source plugin directory empty of active content
> 2. THEN run `bulk_rewrite.py` (see below)
> 3. THEN apply manual edits for non-deterministic patterns
> 4. THEN `git add -A` + commit

```bash
# Move reference files
git mv plugins/{source}/references/{ref-file}.md plugins/sulis/references/{ref-file}.md

# After Commit 1 + 2 + 3 + the reference moves above, ALL source-plugin
# content is in plugins/sulis/. The source plugin directory is empty of
# active content (only plugin.json + CHANGELOG + README + settings remain).
# NOW run the bulk sweep — it can scan everything without the
# excluded-source-plugin escape hatch protecting unswept self-references.

# Write the replacement table — one [old, new] pair per line in JSON
cat > /tmp/{source}-replacements.json <<'JSON'
[
  ["/{source}:{old-skill-name}", "/sulis:{new-skill-name}"],
  ["plugins/{source}/skills/{old-name}", "plugins/sulis/skills/{new-name}"],
  ["plugins/{source}/agents/", "plugins/sulis/agents/"],
  ["plugins/{source}/references/", "plugins/sulis/references/"],
  ...
]
JSON

# Run the bulk rewrite
python3 plugins/sulis/skills/consolidate-into-sulis/scripts/bulk_rewrite.py \
  --source-plugin {source} \
  --replacements-json /tmp/{source}-replacements.json

# Verify (no live source-plugin refs remain outside historical files)
git grep -nE "(plugins/{source}/|/{source}:[a-zA-Z])" -- \
  ':!plugins/{source}/' ':!**/CHANGELOG.md' ':!**/VERIFICATION_REPORT.md' \
  ':!plugins/sulis/skills/consolidate-into-sulis/' \
  ':!**/sulis.VERIFICATION_REPORT.md'
```

Categories of refs to expect (see `references/external-ref-sweep.md` for the full 12-category checklist):

1. Skill `description:` fields
2. Agent body cross-references
3. Reference docs citing other reference docs
4. SKILL.md `related_skills:` blocks
5. CLAUDE.md (root + per-plugin)
6. README.md (root + per-plugin)
7. CHANGELOG.md (when narrating prior commits, the path was correct then — leave historical narration alone)
8. Cache path patterns in scripts
9. Workflow YAML
10. Settings JSON
11. Template files
12. Test fixtures

```bash
git commit -m "chore(sulis): step 4/5 — move {source} references into sulis + external ref sweep"
```

**Pass criteria:**

- `plugins/{source}/references/` empty
- `git grep "plugins/{source}/" .` returns no non-historical hits anywhere in marketplace
- All references in find_external_refs.py output addressed

## Commit 5 — Wrap-up (docs + DEPRECATED + bumps)

```bash
# Move docs/ if present (with rename if collision)
git mv plugins/{source}/docs/{doc-file}.md plugins/sulis/docs/{prefix}-{doc-file}.md

# Mark source plugin DEPRECATED in:
# - plugins/{source}/.claude-plugin/plugin.json (add deprecated: true; description: "[DEPRECATED] ...")
# - plugins/{source}/CHANGELOG.md (add final entry naming the consolidation commit chain)
# - plugins/{source}/README.md (replace body with deprecation notice + pointer to sulis)
# - plugins/{source}/CLAUDE.md (replace body with deprecation notice)

# Bump sulis metadata:
# - plugins/sulis/.claude-plugin/plugin.json: version
# - plugins/sulis/CHANGELOG.md: new entry describing consolidation
# - .claude-plugin/marketplace.json: sulis version bump (and marketplace version)

# Update checkup allowlists if affected
```

```bash
git commit -m "feat(sulis): vX.Y.Z — {source} consolidated into sulis (step 5/5 — wrap-up)"
```

**Pass criteria:**

- Source plugin shows DEPRECATED status in all four files (plugin.json, CHANGELOG.md, README.md, CLAUDE.md)
- `plugins/sulis/.claude-plugin/plugin.json` version bumped
- `plugins/sulis/CHANGELOG.md` has new entry
- `.claude-plugin/marketplace.json` reflects new sulis version

## Gate 6 — Code-health verification

```bash
# Re-run code-health from a Claude session and save the --raw JSON:
#   /sulis:code-health --raw > "$RUN_DIR/code-health-final.json"

python3 plugins/sulis/skills/consolidate-into-sulis/scripts/compare_baseline.py \
  --baseline "$RUN_DIR/code-health-baseline.json" \
  --final    "$RUN_DIR/code-health-final.json" \
  > "$RUN_DIR/code-health-comparison.md"
```

Three outcomes:

- **PASS** — no regression. Consolidation done. Update `VERIFICATION_REPORT.md` with PASS verdict. Push branch.
- **NEW FINDINGS, regression-grade** — fix forward in Commit 6. Common patterns: broken imports, ref rot in docstrings, coverage drop because tests were moved but coverage config wasn't updated. Fix, commit, re-run Gate 6.
- **NEW FINDINGS, pre-existing** — findings that pre-date the consolidation (false attribution). Document in `VERIFICATION_REPORT.md`; do not gate on these.

See `references/code-health-gating.md` for the regression rubric.

**Pass criteria for Gate 6:**

- `code-health-final.json` exists
- Comparison to baseline shows no NEW findings, OR all NEW findings have a fix-forward commit
- `VERIFICATION_REPORT.md` updated with Gate 6 verdict and the comparison report

### Fix-forward vs rollback

If Gate 6 surfaces regressions, fix-forward (Commit 6) is the default. Rollback is the right call when fix-forward becomes expensive:

- **≤ 3 fix-forward commits** to reach NEW = 0 → fix-forward; document the patterns in VERIFICATION_REPORT.md
- **> 3 fix-forward commits** required → stop. The recipe missed something structural. Roll back to before Commit 1 (`git reset --hard {pre-consolidation-SHA}`), record the failure pattern in VERIFICATION_REPORT.md as a recipe-improvement signal, and either re-run after fixing the recipe or escalate to operator review

The rollback threshold is signal that this consolidation's plugin shape exposed a recipe gap. Treat the failure as data, not as a procedural defect — Phase 3's first four consolidations are explicitly the calibration set for recipe maturation.

## Publishing the consolidation

After Gate 6 passes:

1. Push the consolidation branch
2. Open a PR titled `consolidate(sulis): {source} → sulis (v{old}→{new})`
3. PR body: summary table from `CONSOLIDATION_PLAN.md` + Gate 6 verdict + link to `VERIFICATION_REPORT.md`
4. Standard PR review / merge to dev (per `repository-contract-standard.md` in srd plugin until consolidated)

## Gotchas

- **External ref rot is the silent killer.** A source plugin's reference is cited from CLAUDE.md at the repo root → moves silently → CLAUDE.md still points to old path. Mitigation: run `git grep "plugins/{source}/"` after every commit; should return zero non-historical hits by Commit 4. Grounded in sulis-execution precedent commit `5278a85` which had to update `plugins/srd/references/executor-loop-standard.md` after-the-fact.
- **CI workflow rename collision.** Naming the new workflow just `sulis-tests.yml` collides with the sulis plugin's own. Always keep the qualifier: `sulis-{source-qualifier}-tests.yml`. Mitigation: `detect_collisions.py` flags this; CONSOLIDATION_PLAN.md locks the name. Grounded in precedent commit `02c1e77` (`sulis-execution-tests.yml` → `sulis-executor-tests.yml`).
- **Subagent_type silent break.** Renaming an agent without updating `subagent_type:` references means Sulis dispatches to a nonexistent agent. Mitigation: `find_external_refs.py` emits every dispatch site; Commit 3 fixes them; manual test by invoking Sulis once afterwards. Grounded in precedent commit `99607e8` which moved executor + orchestrator agents.
- **Tin-test rename → description-field rewrite.** If a skill name changes from `decompose` to `plan-work`, the `description:` field in its SKILL.md likely also needs rewording — descriptions often cite the skill name and operation. Mitigation: Commit 2 edit pass includes description verification.
- **`git mv` then forgetting to edit the moved files.** Moving a script preserves history but doesn't update internal paths inside the moved file. Mitigation: every commit has an Edit pass after the `git mv` pass; pass criteria requires paths to resolve.
- **`git mv` stages renames, but post-rename Edits do NOT auto-stage.** After `git mv` + Edit pass, the moves are staged but the content changes are not. A naive `git commit` will land the rename without the edits, producing a slightly broken intermediate state that needs a follow-up "continuation" commit. Mitigation: run `git add -A` (or explicitly `git add <edited-files>`) **after** the Edit pass and **before** the `git commit`. Grounded in the sulis-context → sulis consolidation (Commit 2 split into `0e5c9ea` + `584d438` from this exact misstep).
- **Sweep ordering matters: move BEFORE sweep, not the reverse.** If `bulk_rewrite.py` runs while source-plugin content (agent, references) is still in the source directory, that directory is excluded from the sweep — and any self-references inside the about-to-move content survive untouched into the new location. The sea consolidation surfaced this bug twice (engineering-architect.md had 24 unswept `/sea:*` refs; 5 references had 24 collective unswept refs). Mitigation: move ALL source content (skills + agent + references + docs) before invoking `bulk_rewrite.py`. The script's source-plugin exclusion then becomes a no-op (the directory is empty of active content).
- **Code-health baseline drift.** If the founder ran `/sulis:code-health` weeks ago and saved a baseline somewhere global, Gate 0's fresh baseline supersedes — don't reuse stale baselines for regression detection. Mitigation: Gate 0 captures fresh baseline at consolidation start.
- **Atomic commits violated under pressure.** Mid-consolidation, an operator might be tempted to batch Commits 2-4 to "save time." Don't — atomic commits preserve reviewability and rollback. Mitigation: skill's pass criteria gate per-commit; do not advance until met.

## Vocabulary

- **Source plugin** — the plugin being folded into sulis (e.g., `sulis-context`, `sea`, `srd`). Always exactly one per consolidation run.
- **Tin test** — naming rubric for incoming founder-visible skills. Bare verbs (`decompose`, `harden`, `probe`) and internal-jargon acronyms (`srd-*`, `spec-*`) fail. Verb-noun (`plan-work`, `harden-codebase`) and clear nouns (`inbox`, `code-health`) pass.
- **External ref sweep** — repo-wide grep + edit pass for every path or `subagent_type` citing the source plugin. The highest-risk step in the recipe (Commit 4).
- **Qualifier rename** — when a name collides between source and target, suffix or prefix with a disambiguator (`status` → `wp-status`; `decompose` → `plan-work`). CI workflows always keep their source qualifier.
- **DEPRECATED shell** — the source plugin's directory after consolidation: contents moved away, but `.claude-plugin/plugin.json`, `README.md`, `CHANGELOG.md`, `CLAUDE.md` remain with `[DEPRECATED]` markers. No shim skills are written.
- **Code-health gate** — Gate 0 captures the baseline; Gate 6 verifies no regression. Both invoke `/sulis:code-health`; comparison via `compare_baseline.py`.
- **Run directory** — `plugins/sulis/skills/consolidate-into-sulis/runs/{source}-{date}/`. Holds inventory.json, collisions.md, external-refs.md, CONSOLIDATION_PLAN.md, code-health-baseline.json, code-health-final.json, code-health-comparison.md, VERIFICATION_REPORT.md for one consolidation.

## When to invoke this skill

- A specialist plugin (sulis-context, sulis-security, sea, srd) is ready to be folded into sulis as part of Phase 3 of the change-as-primitive build
- A future plugin migration follows the same recipe (any single-plugin → sulis fold-in)

## When NOT to invoke this skill

- The work is a partial move (only the agent, not the whole plugin) — use direct `git mv` + manual ref sweep instead
- The source plugin is multi-source (depends on or extends another plugin in non-trivial ways) — this recipe is single-source-plugin; refactor first
- The work is the inverse direction (split sulis into pieces) — that's a different operation; no skill exists yet
- Existing sulis plugin skill rename pass (`retry`, `handoff`) — out of scope; do as a separate focused commit
