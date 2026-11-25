---
name: artifact-evaluation-prep
description: Prepare a research artifact package for conference artifact evaluation, reproducibility review, badges, supplementary material, or post-acceptance artifact release. Use this skill whenever the user needs install instructions, reviewer-facing reproduction commands, Docker or environment checks, data/checkpoint packaging, hardware/runtime estimates, anonymized or public artifact metadata, artifact evaluation forms, or a claim-to-artifact reproducibility audit for ML/AI venues.
argument-hint: "[project-dir] [--venue <venue>] [--mode audit|package|instructions|smoke-test]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Artifact Evaluation Prep

Prepare a paper's code, data, checkpoints, scripts, and instructions so an external artifact reviewer can reproduce the paper-facing claims with minimal ambiguity.

Use this skill when:

- a venue requires or offers artifact evaluation, reproducibility badges, or artifact appendices
- the user needs reviewer-facing install, quickstart, demo, or reproduction instructions
- a camera-ready or accepted paper needs an artifact package handoff
- code, data, checkpoints, models, Docker images, or external services must be packaged
- runtime, hardware, random seeds, expected outputs, or troubleshooting notes need to be made explicit
- claims in the paper need to be mapped to runnable scripts or released artifacts

Do not use this skill as a general code-release skill. Use `release-code` for public repository hygiene, licensing, CITATION files, tags, and GitHub releases. Use this skill for reviewer-facing artifact execution and claim reproduction.

Pair this skill with:

- `camera-ready-finalizer` to recover accepted-paper obligations and final claim/evidence state
- `release-code` to prepare public repository hygiene after artifact obligations are clear
- `reproducibility-audit` when environment, data, or execution drift needs a broader audit
- `run-experiment` for generating or testing reproduction commands
- `figure-results-review` when artifact outputs must match paper figures or tables
- `citation-audit` when artifact metadata cites datasets, code, or prior artifacts
- `research-project-memory` when artifact status, blockers, and reviewer-facing instructions should persist

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── artifact-audit.md
    ├── memory-writeback.md
    ├── package-manifest.md
    ├── report-template.md
    └── reviewer-instructions.md
```

## Progressive Loading

- Always read `references/artifact-audit.md`, `references/package-manifest.md`, and `references/reviewer-instructions.md`.
- Read `references/report-template.md` before writing a saved artifact evaluation report.
- Read `references/memory-writeback.md` when the project has `memory/`, component `.agent/` folders, or the user asks for persistent state.
- If venue rules matter, verify current official artifact evaluation instructions before asserting deadlines, badge names, anonymity rules, upload fields, page limits, or required formats.

## Core Principles

- Artifact evaluation is a reviewer workflow, not just a code dump.
- The artifact must reproduce the paper's important claims at an acceptable cost, or clearly document what it cannot reproduce.
- Prefer one reliable quickstart and one complete reproduction path over many fragile commands.
- Every command should state expected runtime, hardware, input, output, and success criteria.
- Package only redistributable data, checkpoints, and dependencies; document restricted assets precisely.
- Keep anonymity, licensing, and external-service assumptions explicit.
- Treat smoke tests as required. An untested instruction file is not an artifact package.

## Step 1 - Recover Evaluation Context

Collect:

- venue and artifact evaluation track, if known
- official artifact instructions, badge criteria, anonymity policy, and upload mechanism
- accepted or submitted paper, appendix, supplementary material, and checklist
- code repository, commit hash, branches, and worktrees
- datasets, checkpoints, pretrained models, generated outputs, and external dependencies
- hardware expectations: CPU/GPU type, memory, disk, runtime, network access
- paper claims, figures, tables, and experiments that the artifact should support
- constraints: private data, license limits, large files, cloud dependencies, nondeterminism, or reviewer time budget

If no venue is specified, produce a venue-agnostic artifact package but mark venue-specific fields as unresolved.

## Step 2 - Map Claims to Artifact Paths

For each paper-facing claim or result, record:

- claim or result ID
- paper location
- script, notebook, config, or command that supports it
- input data or checkpoint
- expected output file, metric, table, or figure
- approximate runtime and hardware
- deterministic tolerance or expected variance
- reviewer priority: quickstart, core, optional, or not reproducible in package

Do not imply full reproducibility if only a smoke test or cached output is provided.

## Step 3 - Build the Artifact Manifest

Read `references/package-manifest.md`.

Create or update a manifest that lists:

- repository URL or archive path
- exact commit, tag, or checksum
- directory layout
- environment files and Docker images
- data and checkpoint locations
- reproduction scripts and configs
- expected generated outputs
- license and citation metadata
- known limitations and unsupported claims

Prefer small, stable names such as `ARTIFACT.md`, `REPRODUCE.md`, or `docs/artifact_evaluation.md` unless the venue requires a specific filename.

## Step 4 - Write Reviewer Instructions

Read `references/reviewer-instructions.md`.

Provide:

- setup commands
- quick smoke test under a short runtime budget
- core reproduction commands for main paper claims
- expected outputs and how to compare them with the paper
- troubleshooting for common failures
- hardware, storage, network, and time requirements
- contact policy or anonymous support channel if allowed
- limitations and optional extended runs

Instructions should be copy-pasteable and should not require the reviewer to infer hidden paths or environment variables.

## Step 5 - Smoke Test the Artifact

When allowed by the user and environment, run at least:

- environment creation or dependency resolution
- import or CLI sanity check
- quickstart command
- one representative data/checkpoint load
- one expected-output comparison

If commands are too expensive, record the exact reason and create a minimal substitute test.

## Step 6 - Handle Packaging Risks

Audit:

- anonymization vs public release state
- licenses for code, data, pretrained weights, and third-party assets
- large-file strategy and checksums
- private paths, credentials, API keys, and machine-specific assumptions
- random seeds and nondeterminism
- version pinning and dependency conflicts
- reviewer time budget and failure recovery

Route public release issues to `release-code`; route environment drift to `reproducibility-audit` if available.

## Step 7 - Write the Artifact Evaluation Report

Read `references/report-template.md`.

If saving to a project and no path is given, use:

```text
docs/submission/artifact_evaluation_prep_YYYY-MM-DD.md
```

The report must include:

- readiness decision
- blocking issues
- claim-to-artifact map
- package manifest summary
- smoke-test status
- reviewer instruction status
- risks, limitations, and reviewer-facing caveats
- handoff to release, camera-ready, or memory

## Step 8 - Write Back to Project Memory

Read `references/memory-writeback.md` when memory exists.

Update artifact status, reproduction commands, blockers, claim support, release actions, and final handoff notes without copying full command logs into memory.

## Final Sanity Check

Before finalizing:

- every important paper claim is either reproducible, smoke-tested, cached with explanation, or explicitly out of scope
- quickstart instructions have expected outputs and runtime
- hardware, data, checkpoints, licenses, and anonymity state are clear
- package paths and links are stable
- reviewer-facing failure modes are documented
- public-release and camera-ready obligations are routed
- project memory records artifact readiness and open blockers
