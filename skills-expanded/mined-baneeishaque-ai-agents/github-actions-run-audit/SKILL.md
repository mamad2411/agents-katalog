---
name: github-actions-run-audit
description: Composer skill — audit GitHub Actions workflow runs end-to-end via the `gh` CLI. Owns observation primitives (`run list`, `run view`, `run download`) and composes the bases `github-repo-commit-fetch` (verify committed artifact) and `github-actions-workflow-dispatch` (optional trigger-then-audit). Captures the "did the scheduled / triggered workflow run, succeed, and commit the fresh artifact?" question as reusable, scripted protocol.
category: GitHub-Automation
---

# GitHub Actions Run Audit Skill (v1)

> **Skill ID:** `github-actions-run-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../skill-factory/SKILL.md))

## 1. When to Apply

Apply this skill whenever the agent needs to answer ANY of:

- "Did the scheduled workflow `<X>` run on time? What was its conclusion?"
- "I just made a change — did the periodic backup capture it yet?"
- "Trigger workflow `<X>` and tell me when it's done."
- "Download the artifacts from run `<id>` so I can inspect them locally."
- "What does the workflow run history look like for the last N runs?"

**Anti-trigger:** For authoring NEW workflows, see
[`github-workflow-creation`](../github-workflow-creation/SKILL.md). For pure
write-only dispatch with no audit, use
[`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md)
directly.

## 2. Critical Pre-Flight: Identify the Workflow-Owning Repo

> ⛔ **Most common mistake.** Workflows often live in a DIFFERENT repo from
> the application code they serve. Today's working example:
>
> - Application code: `baneeishaque/Account-Ledger-Server-PHP`
> - Workflow that backs it up: `baneeishaque/Account-Ledger-Server`
>
> An agent that audits the wrong repo will see stale / failed / nonexistent
> runs and reach the wrong conclusion. **Always confirm the workflow-owning
> repo first**, ideally by reading the workflow YAML in the suspected repo
> via `fetch-file-at-ref.py --path .github/workflows/<name>.yml --ref HEAD`.
>

## 3. Why a composer skill (not one mega-skill)

Per the [Layered Composition Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md):

| Concern | Owned by | Why |
| --- | --- | --- |
| Read repo data (commits, files at refs) | Base [`github-repo-commit-fetch`](../github-repo-commit-fetch/SKILL.md) | Useful outside Actions (PR review, archaeology, supply-chain audit) |
| Trigger workflows | Base [`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md) | Useful in deploy CLIs, manual-deploy automation |
| Observe runs + download artifacts | **This composer** | Actions-specific; meaningless outside the Actions domain |

## 4. Required Inputs

- `gh` CLI installed and authenticated. Falls back to
  [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md).
- Both base skills' scripts available at their canonical paths.
- Python 3.10+ via `mise` per workspace convention.

## 5. Operational Logic

### 5.1 Script catalogue (this skill)

| Script | Purpose | Required args | Output |
| --- | --- | --- | --- |
| [`scripts/audit-run.py`](scripts/audit-run.py) | Observation only: list the N most recent runs of `<workflow>`, or inspect one `<run-id>` (status, conclusion, timestamps, jobs). Emits JSON. | `--repo` + (`--workflow` OR `--run-id`) | JSON document |
| [`scripts/download-artifacts.py`](scripts/download-artifacts.py) | Download all (or named) artifacts of one workflow run to a local directory via `gh run download`. | `--repo`, `--run-id`, `--dir` | Files written to `--dir`, summary on stdout |

### 5.2 Base-script composition (full audit pipeline)

```bash
DISPATCH_DIR=.agents/skills/github-actions-workflow-dispatch/scripts
SCRIPTS_DIR=.agents/skills/github-actions-run-audit/scripts
FETCH_DIR=.agents/skills/github-repo-commit-fetch/scripts

REPO=owner/workflow-owning-repo
WF=database-backup.yml

# Step 1 — (optional) trigger the workflow now and wait for completion.
python3 "$DISPATCH_DIR"/trigger-workflow.py --repo $REPO --workflow "$WF" --wait 300

# Step 2 — audit the latest run's status.
python3 "$SCRIPTS_DIR"/audit-run.py --repo $REPO --workflow "$WF" --limit 1

# Step 3 — confirm the workflow committed a fresh artifact.
python3 "$FETCH_DIR"/list-commits.py --repo $REPO --limit 1

# Step 4 — inspect what file that commit touched.
SHA=$(python3 "$FETCH_DIR"/list-commits.py --repo $REPO --limit 1 \
      | python3 -c 'import json,sys;print(json.load(sys.stdin)[0]["short"])')
python3 "$FETCH_DIR"/commit-details.py --repo $REPO --sha $SHA --files-only

# Step 5 — fetch the committed artifact and verify it contains expected content.
python3 "$FETCH_DIR"/fetch-file-at-ref.py --repo $REPO --ref $SHA \
    --path db_backups/foo.sql --out /tmp/backup.sql
grep -c "ENGINE=InnoDB" /tmp/backup.sql

# (Alternative to step 5: if the workflow uploads artifacts instead of committing,
#  download them via:)
# python3 "$SCRIPTS_DIR"/download-artifacts.py --repo $REPO --run-id $RUN_ID --dir /tmp/artifacts/
```

### 5.3 Composition Rationale

This composer chains base scripts via **relative paths anchored at the
caller's repo root**, never inlining base logic. The full path resolution
pattern is:

```text
.agents/skills/<base-skill>/scripts/<script>.py
```

Anchoring on the repo root keeps the composition portable across machines
and survives skill renames at the composer layer.

## 6. Related Skills

| Skill | Relationship |
| --- | --- |
| [`github-repo-commit-fetch`](../github-repo-commit-fetch/SKILL.md) | **Base** — provides all read-only repo data primitives. |
| [`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md) | **Base** — provides the write-side trigger primitive. |
| [`github-workflow-creation`](../github-workflow-creation/SKILL.md) | Sibling — authoring side. After authoring a new workflow, use this skill to verify it runs. |
| [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md) | Fallback — REST equivalent of every `gh` call here. |
| [`github-secrets-bulk-set`](../github-secrets-bulk-set/SKILL.md) | Sibling — secrets-management for the workflows being audited. |
| [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) | Co-skill — redirect audit JSON to `scratch/` for later diff. |
| [`mise-tool-management`](../mise-tool-management/SKILL.md) | Co-skill — Python interpreter pinning. |

## 7. Prohibited Behaviors

- Auditing the wrong repo (see §2). Always confirm the workflow-owning repo
  first.
- Triggering workflows without explicit user authorization (delegated to
  [`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md)
  §7).
- Reimplementing `list-commits` / `commit-details` / `fetch-file-at-ref`
  inline — call the base scripts. Inlining duplicates the base's SSOT and
  silently diverges bug fixes.
- Concluding "the workflow is broken" from one failed run — check
  `--limit 5` or `--limit 10` to see whether the failure is recent or
  endemic.
- Downloading artifacts to the repo working tree without a `scratch/`
  gitignore guard — use [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md).
