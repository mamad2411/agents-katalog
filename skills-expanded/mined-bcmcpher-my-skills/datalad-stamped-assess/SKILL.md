---
name: datalad-stamped-assess
description: >
  Assess a DataLad research object against the STAMPED principles (Self-containment, Tracking,
  Actionability, Modularity, Portability, Ephemerality, Distributability) and optionally plan
  improvements. Trigger on "assess STAMPED", "STAMPED checklist", "STAMPED compliance",
  "check reproducibility", "how reproducible is this dataset", "grade this dataset", or
  /datalad-stamped-assess. Read-only — never modifies the dataset. Add --plan for remediation
  steps. Does NOT create or save datasets (use datalad-init / datalad-save).
argument-hint: '[dataset-path] [--plan]'
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Bash, Glob, Grep
---

# Skill: datalad-stamped-assess

Score a research object against the **STAMPED** checklist and, on request, produce a
remediation plan mapped to this plugin's `datalad-*` skills. STAMPED generalizes YODA: YODA is
the Self-containment + Modularity core, and this assessment covers all seven principles. The
full checklist backbone and DataLad evidence map live in
`${CLAUDE_PLUGIN_ROOT}/../references/stamped-principles.md` — **load it before scoring.**

Grading is a **spectrum, not pass/fail**. Grade each principle as ✓ satisfied / ◐ partial /
✗ unmet, and cite the concrete evidence (or its absence) behind every grade.

## Steps

1. **Resolve the target** — read `$ARGUMENTS`. Treat a leading non-flag token as the dataset
   path; if none, use the current working directory. Detect `--plan` anywhere in the args.
   Show the resolved absolute path. Confirm it is a DataLad dataset (`.datalad/` present) or at
   least a git repository; if neither, tell the user there is nothing to assess and stop.

2. **Gather evidence (read-only probes only).** Never write, save, or run pipelines. Prefer
   `datalad`/`git` porcelain; if `datalad` is not installed, fall back to git-only probes and
   note the reduced confidence. Collect:
   - **S** — `.datalad/` presence; `.gitmodules` (inputs linked as subdatasets vs copied);
     registered URLs (`git annex whereis` / `datalad status --annex`); a top-level `README`.
   - **T** — `git log --oneline` depth; git-annex backend; `datalad run`/`download-url`
     provenance in commit messages (`git log --oneline --grep '\[DATALAD RUNCMD\]'`), and
     `git annex whereis --json <path> | jq '.whereis | length'` for how many repositories
     hold a given file. There is no `datalad log` command — see `/datalad-log`.
   - **A** — runnable instructions: `README`, `Makefile`, `Snakefile`, `*.sh` in `code/`;
     presence of replayable `datalad run` commits.
   - **M** — `inputs/` / `code/` / `outputs/` separation; subdatasets and their boundaries.
   - **P** — env specs: `Dockerfile`, `environment.yml`, `pyproject.toml`, `requirements.txt`,
     `.datalad/environments/`; registered containers (`datalad containers-list`); scan
     provenance for absolute host paths.
   - **E** — whether runs reference a registered container image (rebuilt per run) vs assuming
     ambient tools.
   - **D** — configured siblings/remotes (`datalad siblings` / `git remote -v`); any DOI badge
     in README; `LICENSE` / `.reuse/` with a resolvable SPDX identifier.

3. **Score against the checklist backbone** in `references/stamped-principles.md` — walk S.1–D.3,
   marking each item satisfied / partial / unmet from the evidence in step 2. Respect the
   RFC-2119 weight (MUST gaps are more severe than SHOULD/MAY).

4. **Emit the readout** — a per-principle table, plus the item-level detail for anything not
   fully satisfied:

   | Principle | Grade | Satisfied | Gaps |
   |-----------|-------|-----------|------|
   | S Self-containment | ◐ | inputs are subdatasets | no top-level README |
   | … | | | |

   Lead with a one-line overall summary (e.g. "strong on S/T/M, weak on P/E/D"). Cite evidence
   for every grade; never assert a gap you did not probe for.

5. **Plan-to-improve** — when `--plan` is present, or the user asks how to improve, output an
   **ordered** remediation list (most severe MUST gaps first). Map each step to a concrete
   existing skill, e.g.:
   - Provenance missing (T/A) → re-run analysis via `/datalad-run` (or `/datalad-container-run`).
   - No environment spec (P/E) → add a `Dockerfile`/`environment.yml` and register a container
     for `/datalad-container-run`.
   - Inputs copied rather than linked (S/M) → `/datalad-clone` the source into `inputs/`.
   - No license (S/D) → add a `LICENSE` with an SPDX id (or REUSE `.reuse/dep5`).
   - Not distributable (D) → `/datalad-push` to a sibling, or `/datalad-export` to Zenodo/Figshare.
   Each step names the principle(s) it advances and the skill to run — but this skill itself
   makes no changes.

## Constraints

- **Read-only.** Never run `datalad create`/`save`/`run`/`push`, never edit files. Assessment
  must not mutate the research object.
- Grade on a **spectrum**; STAMPED principles are not pass/fail gates.
- **Cite evidence** for every grade — including the probe that found nothing.
- Degrade gracefully when `datalad` is absent: use git-only probes and say so.
- Always load `${CLAUDE_PLUGIN_ROOT}/../references/stamped-principles.md` for the authoritative
  checklist and DataLad evidence map before scoring.
