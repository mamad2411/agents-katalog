---
name: skill-inventory
description: Inventory downstream repository Claude and Codex skill installs from a control-repo manifest, classify managed local skill-copy drift against canonical agentic-skills sources, and produce report-only Markdown or JSON guidance without refreshing, deleting, or mutating downstream repos.
type: ops
version: v0.0
argument-hint: "[--manifest <path>] [--repo <path>] [--format markdown|json]"
---

# Skill Inventory

Invoke as `$skill-inventory`.

Use this skill from a control repository that manages downstream repositories and needs to know whether copied local skill roots are current, stale, pinned, unmanaged, or missing their canonical source.

## V1 Contract

Report-only — do not modify tracked files.

- Do not run `scripts/pack.sh refresh`.
- Do not run delete, cleanup, remove, prune, or reinstall commands.
- Do not edit `.claude/skills/**`, `.codex/skills/**`, `.agents/project.json`, or any file inside downstream repositories.
- Do not add an apply route in v1. Suggest exact follow-up commands only after the inventory report shows what is needed.
- Only write control-repo artifacts: `tasks/skill-inventory.md`, `alignment/skill-inventory-{topic}.html`, task notes, prompt history, and normal shipping docs.

## Process

1. Read repo instructions first: `AGENTS.md`, `CLAUDE.md`, or the local equivalent.
2. Capture the visible `$skill-inventory` invocation under `prompts/skill-inventory/` before substantive work, following the repo prompt-history convention.
3. Resolve downstream repos from a manifest before scanning. Default manifest search order:
   - `tasks/downstream-repos.md`
   - `tasks/fleet-queue.md`
   - `tasks/repo-seeding.md`
4. Require a Markdown table column named `Local Path` or `Path` for local checkout paths. Remote-only `owner/repo` cells are not scannable; ask for a local path instead of guessing.
5. Run the bundled scanner from this skill directory. Default output is the durable Markdown report:

   ```bash
   bash scripts/skill-inventory.sh --out tasks/skill-inventory.md --format markdown
   ```

   Useful variants:

   ```bash
   bash scripts/skill-inventory.sh --manifest tasks/downstream-repos.md --out tasks/skill-inventory.md
   bash scripts/skill-inventory.sh --repo ../downstream-app --out -
   bash scripts/skill-inventory.sh --format json --out -
   ```

6. The scanner sources the control repo's canonical `scripts/skill-links.sh` and uses `skill_install_status` for status classification. Do not reimplement the drift semantics manually.
7. Review the report and build `alignment/skill-inventory-{topic}.html` using `ALIGNMENT-PAGE.md` when producing a durable report. The page must render the report, evidence, assumptions, action hints, and approval gates without context loss.
8. End with:
   - **Next work:** the most specific inventory follow-up, usually adding missing local paths or reviewing stale rows.
   - **Recommended next command:** usually `$skill-inventory --manifest <path>` to rerun after manifest fixes, or `$project-fleet --status` when no inventory remediation is needed.

## Status Categories

Use the exact categories emitted by `skill_install_status`:

- `ok`: managed copy matches the canonical source content.
- `stale`: canonical source content changed since the managed copy was installed.
- `unknown`: marker exists but lacks `source_sha`; refresh is needed later to enable deterministic tracking.
- `missing-source`: marker points to a source directory that no longer exists.
- `pinned`: symlinked install, usually to `archive/<version>`, intentionally frozen.
- `not-managed`: skill directory is not an agentic-skills managed install.

## Report Expectations

`tasks/skill-inventory.md` should include:

- control repo, manifest path, generated timestamp, and report-only notice;
- repo-level totals across Claude and Codex skill roots;
- per-agent rows for `.claude/skills/*` and `.codex/skills/*`;
- installed and canonical version fields when available;
- source path evidence for managed or pinned installs;
- action hints for `stale`, `unknown`, and `missing-source`, including exact suggested follow-ups such as `scripts/pack.sh refresh`;
- a clear statement that the scan did not run refresh, delete, cleanup, install, or other mutation commands.

If no local paths are found, the scanner must fail non-destructively and print a manifest template with a `Local Path` column.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/skill-inventory-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
