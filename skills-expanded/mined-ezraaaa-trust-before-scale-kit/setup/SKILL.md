---
name: setup
description: "Set up trust before scale in a project: copy scripts, config, eval cases and ADR draft, then wire the checks into its gate. Use to adopt, install or set up the workflow."
---

# Set up trust before scale in this project

The plugin is installed per machine but acts only where `.agents/trust-before-scale.json` (falling back to `.claude/trust-before-scale.json`) exists.

1. **Pick the profile.** `acme-mobile` and `acme-flutter` are invented stack examples; anything else is `generic`. Read
   `<plugin-root>/profiles/<profile>/NOTES.md` first. For private profiles use
   `--profile-dir <path>` or `TBS_PROFILE_DIR`; the flag takes precedence.
2. **Branch first** (never on `main` or the base branch): `git switch -c chore/trust-before-scale origin/<base>`.
3. **Copy the kit:** `node <plugin-root>/bin/tbs-init <profile>` from the repo root. It writes
   `scripts/tbs/` (including `VERSION`), `.agents/trust-before-scale.json` (falling back to `.claude/trust-before-scale.json`), `evals/`, and `docs/trust-before-scale/`
   (including `enforcers.md`). Existing project files are kept; `VERSION` always records the kit version.
4. **Prove it runs here:**
   - `node --test scripts/tbs/tbs.test.mjs`: the kit's tests.
   - `node scripts/tbs/feature-map.mjs --list`: the discovered screens. Empty or missing sources fail with a
     hint to fix `featureMap.sources`.
   - `node scripts/tbs/feature-map.mjs --init`: the starting map, every screen in `notMappedYet`.
   - `node scripts/tbs/skill-eval.mjs routine --dry-run`: the eval plan. Seeds that no longer apply (the code moved)
     are marked `STALE` and fail the dry run; rewrite them against the suite base before the first real run.
     An empty suite also fails: add 3–8 seeds from real failures.
5. **The generic profile** needs the config filled from the project's own rules: its gate commands and exit marker,
   its high-risk paths for the lane's block-list, where its screens are declared, and 3–8 seeds taken from failures
   the project has really had (CLAUDE.md "do not" rules, settled decisions, review findings that repeat).
6. **Wire the checks into the project's gate** (its verify script, CI, or the routine's gate list):
   `node scripts/tbs/feature-map.mjs && node scripts/tbs/skill-eval.mjs --check`, and into the release:
   `node scripts/tbs/skill-eval.mjs --check --fresh`. Run the first real eval
   (`node scripts/tbs/skill-eval.mjs routine`) before adding `--check`, or the gate goes red at once.
7. **Put the ADR draft to the owner** (`docs/trust-before-scale/ADR-draft.md`), each decision with a recommendation.
   The self-merge lane stays off until decision 4 is accepted.
8. Open one PR with all of it, through the project's normal routine. Nothing here bypasses it.

Screen entries may link to a verification journey with `verify`, a repo-relative file path, and list
`preconditions` as strings for auth, data, role and flags. A missing journey fails the map check; `--init`
leaves both fields out. Point entries at your project’s verification journeys when available.

For an installed project, `node <plugin-root>/bin/tbs-init --update` needs no profile. It replaces
shared scripts and the brief template, reports `updated`/`unchanged` per file and the old → new version,
and preserves config, evals, NOTES, ADR, the enforcer table and the feature map. Commit through the project's routine.

Resolve `<plugin-root>` to the installed plugin directory before running commands; see docs/harnesses.md in the kit checkout.
