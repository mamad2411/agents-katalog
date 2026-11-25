---
name: bootstrap-repo
description: Initialize or reset a repository README and agent workflow docs from a short project brief
type: execution
version: v0.5
argument-hint: "<project brief>"
---

# Bootstrap Repo

Invoke as `$bootstrap-repo`.

Initialize a repository with a useful `README.md` and the standard agent workflow docs. When invoked with `--reset-existing`, first archive stale implementation and documentation files from a non-empty stuck repo so the fresh start is not built on old code or old assumptions by accident.

## Process

1. **Parse the project brief and mode** from `$ARGUMENTS`:
   - Detect `--reset-existing`, `--in-place-reset`, or an explicit request to archive/reset the current codebase before bootstrap.
   - Extract the project name, purpose, setup instructions, run/test commands, and any constraints.
   - If the brief is missing or too thin to write a useful README, ask for the project name and one-sentence purpose. Ask for setup or run instructions only when the repository does not make them discoverable.

2. **Inspect the target repository:**
   - Read existing `README.md`, `CLAUDE.md`, `AGENTS.md`, package manifests, obvious build files, and directory names.
   - Preserve discovered commands and facts. Do not invent dependency managers, deployment targets, or product claims.

3. **Reset existing stale repo when explicitly requested:**
   - Only perform this step when reset mode is explicit. Never archive or move files during ordinary bootstrap.
   - Confirm the repo is non-empty and contains stale implementation, docs, research, specs, task files, design notes, or generated app structure. If it is already empty or freshly initialized, skip archival and note why.
   - Create `archive/YYYY-MM-DD-HHMMSS/` and move stale implementation and documentation files/directories there before writing fresh bootstrap docs.
   - Archive old docs by default, including `docs/`, `alignment/`, `research/`, `specs/`, `tasks/`, planning reports, implementation notes, design docs, old README content, and prior roadmap/todo/history files. These may remain useful as historical evidence in the archive, but they must not stay active as source-of-truth inputs.
   - Do not archive `.git/`, `.agents/`, `archive/`, `desk-flip-report.md`, root agent config files needed for the current session, or the newly written high-level concept artifact.
   - Preserve exactly one active concept seed, such as `concept.md` or `README.md` `## Concept`, derived from the bootstrap brief or `desk-flip-report.md`. Keep it high level: product name, target user, core problem, value proposition, non-goals, and open questions. Do not preserve old research/spec detail as active files.
   - Preserve a manifest at `archive/YYYY-MM-DD-HHMMSS/MANIFEST.md` listing every moved path, every intentionally preserved path, and the high-level concept source that justified the reset.
   - Prefer `git mv` for tracked paths so history remains understandable. Use ordinary moves only for untracked paths.
   - Do not delete old files outright. If a path cannot be moved safely, stop and report the blocker instead of partially resetting further.
   - After archival, the root should contain only the fresh-start sources of truth: git metadata, agent config, the archive directory, `desk-flip-report.md`, the high-level concept artifact, and any newly written bootstrap docs. Old docs/research/specs belong in the archive.

4. **Create or update `README.md`:**
   - If `README.md` is absent, empty, or placeholder-like, write a concise README with:
     - `# <Project Name>`
     - A short purpose summary.
     - `## Getting Started`
     - `## Development`
     - `## Notes`
   - If `README.md` already has substantial content, preserve it. Ask before replacing it; otherwise add a small bootstrap section only when it improves the file.
   - Use the project brief as the primary source and repository inspection as supporting evidence.

5. **Provision agent workflow docs:**
   - Run `$provision-agentic-config` for the same repository.
   - Confirm `CLAUDE.md` and `AGENTS.md` exist after provisioning.
   - Preserve unrelated existing content in both files.

6. **Verify the result:**
   - Check that `README.md`, `CLAUDE.md`, and `AGENTS.md` exist.
   - Confirm the corresponding workflow orchestration block appears exactly once in each of `CLAUDE.md` and `AGENTS.md`.
   - Report whether the monorepo safety block was included or skipped by `$provision-agentic-config`.
   - In reset mode, check that `archive/YYYY-MM-DD-HHMMSS/MANIFEST.md` exists and lists moved and preserved paths, and verify old docs/research/specs/tasks were archived rather than left active.

7. **Route research-first after product bootstrap:**
   - If this is a product, app, SaaS, dashboard, internal tool, marketplace, website, or other user-facing restart, rebuild market and lifecycle alignment from the high-level concept before UI requirements or prototypes.
   - Check `.agents/project.json.enabled_packs` when present. If `business-research` is not enabled, recommend `npx skillpacks install business-research` from the project shell, before `$customer-discovery`. If `customer-lifecycle` is not enabled, include `npx skillpacks install customer-lifecycle` before `$journey-map`.
   - When required packs are available, recommend `$customer-discovery <concept>` as the next command. After `$customer-discovery`, the intended sequence is `$competitive-analysis` -> `$journey-map` -> `$positioning` -> `$user-flow-map` -> `$ux-variations [specific-user-flow]` -> `$ui-interview [specific-ux-variation]` -> prototype work.
   - If current, accepted `research/icp.md`, `research/competitive-analysis.md`, and `research/journey-map.md` already exist from the fresh reset but positioning is missing, then recommend `$positioning <topic>`.
   - If positioning exists but a flow map is missing, recommend `$user-flow-map <topic>`.
   - If a flow map exists but UX variation branches are missing, recommend `$ux-variations [specific-user-flow]`.
   - If UX variation branches exist but no branch has an approved UI direction, recommend `$ui-interview [specific-ux-variation]`.
   - Recommend `$ui-interview --requirements-only <topic>` only when the user explicitly needs a fixed content/data/action contract before `$ux-variations --layout-mode <topic>`.
   - Only route directly to `$roadmap` or `$exec` when the project is non-UI/non-product work or already has accepted alignment artifacts and a consolidated prototype.
   - The intended product sequence after reset is: `$customer-discovery` -> `$competitive-analysis` -> `$journey-map` -> `$positioning` -> `$user-flow-map` -> `$ux-variations [specific-user-flow]` -> `$ui-interview [specific-ux-variation]` -> build variants/prototypes via `$exec` or the applicable prototype-building route -> `$uat --variant-evaluation` -> `$consolidate-prototypes` -> `$research-roadmap --post-prototype` -> `$spec-interview` or `$roadmap`.

## Output

```markdown
Bootstrapped repository
- README.md: [created | updated | preserved], source: [arguments | prompts | existing content]
- Reset archive: [created archive/YYYY-MM-DD-HHMMSS | skipped (<reason>)]
- Active concept seed: [concept.md | README.md ## Concept | other]
- CLAUDE.md: [created | updated | unchanged], corresponding workflow block appears once
- AGENTS.md: [created | updated | unchanged], corresponding workflow block appears once
- Monorepo safety block: [included (<heuristic>) | skipped]
- Verification: [commands/checks run]
- Recommended next command: [npx skillpacks install business-research | npx skillpacks install customer-lifecycle | npx skillpacks install product-design | $customer-discovery <concept> | $positioning <topic> | $user-flow-map <topic> | $ux-variations [specific-user-flow] | $ui-interview [specific-ux-variation] | $roadmap | $exec]
```

## Constraints

- Do not overwrite substantial existing `README.md` content without explicit user confirmation.
- Do not invent setup, test, deploy, or architecture details that are not in the brief or repository.
- Keep the README concise and useful for a new contributor.
- Do not modify files other than `README.md`, `CLAUDE.md`, and `AGENTS.md` unless the user explicitly asks or invokes reset mode.
- Reset mode may move stale files, including old docs/research/specs/tasks, into `archive/YYYY-MM-DD-HHMMSS/` and write that archive's `MANIFEST.md`; it may not delete files outright.
- In reset mode, do not preserve old docs as active files just because they were marked salvageable. Use them only as archived historical evidence; active research and requirements restart from the high-level concept.
- Do not create, modify, or suggest GitHub Actions workflows.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
