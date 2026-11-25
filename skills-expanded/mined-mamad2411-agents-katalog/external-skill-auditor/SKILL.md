---
name: external-skill-auditor
description: >-
  Audit third-party Agent Skills before install or repo promotion. Use when
  evaluating external skill sources, hooks, scripts, provenance, credentials,
  network behavior, or destructive commands. NOT for creating skills, code
  review, or appsec scans.
argument-hint: "<mode> [source-or-path]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# External Skill Auditor

Audit third-party Agent Skills as trust-bearing assets before installing them
globally or promoting them into this repository.

**Scope:** External skill import review only. NOT for creating skills
(`skill-creator`), normal code review (`honest-review`), dependency/appsec
scanning (`security-scanner`), or broad skill discovery (`discover-skills`).

## Dispatch

| `$ARGUMENTS` | Mode | Action |
|---|---|---|
| Empty | `menu` | Show audit modes, required evidence, and outcome categories |
| `triage <source>` | `triage` | Classify source reputation, registry signal, install syntax, and dedupe risk |
| `inspect <path>` | `inspect` | Review local staged skill files for frontmatter, hooks, scripts, and command risk |
| `commands <path>` | `commands` | Extract and classify shell commands, package-manager calls, and network operations |
| `provenance <source>` | `provenance` | Check source URL, owner, license, commit/hash, and registry/source-list consistency |
| `decision <source-or-path>` | `decision` | Produce install-now / inspect / keep-global / build-local / avoid recommendation |
| `scan <path>` | `scan` | Run the local static scanner and interpret its JSON output |
| Natural language about external skills, registries, hooks, scripts, or importing | Auto-detect the closest mode |

## Outcome Categories

| Category | Meaning |
|---|---|
| `install now` | Reputable source, clear gap, no risky executable surface after inspection |
| `inspect then install` | Useful candidate with unresolved scripts, hooks, credentials, or provenance questions |
| `keep global only` | Useful personally, but duplicate or too operational for repo promotion |
| `build locally` | Concept is valuable but external options are weak, stale, or too broad |
| `avoid/duplicate` | Unsafe, untrusted, source-conflicted, stale, or redundant with repo skills |

## Canonical Vocabulary

Use these canonical terms exactly in audit reports.

| Term | Meaning |
|---|---|
| **source-list** | Read-only `npx skills add <source> --list` result used before install |
| **executable surface** | Hook, script, command substitution, shell snippet, binary, or package script |
| **source conflict** | Registry metadata and source-list/install behavior disagree |
| **provenance** | Source owner, URL, license, commit, content hash, and access date |
| **credential behavior** | How a skill reads, stores, transmits, or asks for secrets and tokens |
| **promotion** | Moving an external skill into this repo's tracked catalog or docs |
| **outcome category** | One of `install now`, `inspect then install`, `keep global only`, `build locally`, or `avoid/duplicate` |

## Classification Gate

Classify the request before auditing:

1. If the user asks to create or improve a skill, route to `skill-creator`.
2. If the user asks for normal code review, route to `honest-review`.
3. If the user asks for app vulnerability or dependency scanning, route to `security-scanner`.
4. If the user asks for broad skill discovery, route to `discover-skills`.
5. Otherwise, choose the closest mode from the dispatch table.

## Audit Workflow

1. Capture the intended source and install command exactly.
2. Run only source-list or read-only inspection first, such as:
   ```bash
   npx skills add <source> --list
   ```
3. Read the candidate `SKILL.md` and all referenced files before installing.
4. Inspect hooks, scripts, allowed tools, command substitutions, shell snippets,
   network calls, env access, credential storage, and filesystem writes.
5. Check dedupe against repo-owned and globally installed skills.
6. Decide with one of the outcome categories and include the evidence boundary.

For local staged skill directories, run:

```bash
uv run python skills/external-skill-auditor/scripts/audit_external_skill.py <skill-dir>
```

Treat the script output as a first-pass signal only. Human review still decides
whether commands are intentional, documented, and acceptable for the skill's
purpose.

## Progressive Disclosure

- Start with this `SKILL.md` for routing, outcome categories, and hard rules.
- Read `references/import-checklist.md` when making any install, promotion, or avoid decision.
- Run `scripts/audit_external_skill.py` only for local staged skill directories.
- Do not load unrelated code-review, appsec, or skill-authoring guidance unless the classification gate redirects.

## Import Checklist

Use `references/import-checklist.md` for the full gate. Minimum checks:

- Source owner, URL, license, install count, and current source-list behavior.
- Resolved commit SHA and content hash before repo promotion.
- Frontmatter validity and description fit for this repo.
- `hooks`, `allowed-tools`, scripts, and executable files.
- Commands that mutate git, install packages, write home directories, or call APIs.
- Credential/env var handling, network egress, telemetry, and data upload behavior.
- Duplicate concepts already covered by repo skills.

## Critical Rules

1. Require `npx skills add <source> --list` evidence before any install decision.
2. Inspect hooks, scripts, binaries, and command substitutions before approving promotion.
3. Block source conflicts where registry metadata and source-list behavior disagree.
4. Redact secret values while reporting credential-handling issues.
5. Refuse to run candidate scripts during audit except syntax/static checks in a staging path.
6. Downgrade unknown community sources unless install count, recency, and code inspection compensate.
7. Record evidence date because registry counts and source contents drift.
8. Classify every candidate into exactly one outcome category.

## Reference File Index

| File | Read When |
|---|---|
| `references/import-checklist.md` | Running any audit, decision, or repo-promotion review |

| Script | Run When |
|---|---|
| `scripts/audit_external_skill.py` | Static first-pass scan of a local external skill directory |

## Output Shape

```markdown
## External Skill Audit

- Candidate:
- Source:
- Intended install command:
- Outcome:
- Confidence:
- Trust blockers:

### Evidence
- Source/provenance:
- Registry/source-list:
- Dedupe:
- Executable surfaces:
- Credential/network behavior:
- Script scan:

### Required Follow-up
- ...
```

## Validation Contract

Before declaring this skill complete after edits:

```bash
uv run wagents validate
uv run wagents eval validate
uv run python audit.py skills/external-skill-auditor
uv run wagents package external-skill-auditor --dry-run
uv run python skills/external-skill-auditor/scripts/audit_external_skill.py skills/external-skill-auditor
```

Completion criteria:

- Skill and eval validation pass.
- Audit score is A or all remaining findings are explicitly accepted.
- Package dry-run passes.
- Static scanner returns JSON without executing candidate scripts.
- Smoke review covers source triage, local scan, hook/script risk, and negative-control routing.
