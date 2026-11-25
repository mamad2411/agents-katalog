---
name: github-repo-name-conflict-check
description: >-
  Check whether candidate repository names are free under a GitHub owner
  account via authenticated per-name lookups (200 = taken, 404 = available)
  with optional full owner-repo enumeration for count sanity. Read-only;
  used by transfer destination checks and repo-creation pre-flights.
category: GitHub
---

# GitHub Repo Name Conflict Check Skill (v1)

> **Skill ID:** `github-repo-name-conflict-check`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../../../skill-factory/SKILL.md))

## Description

Checks each candidate repository name against a GitHub owner account
(`<owner>/<name>`) with an **authenticated** lookup and classifies it as
`TAKEN` (HTTP 200), `AVAILABLE` (HTTP 404), or `UNKNOWN` (any other response).
Because the lookup runs with the owner's token, private repositories are
visible and can never be misreported as available.

## Composition Rationale

This skill is a base primitive: the 200/404 classification is the atomic
verdict every conflict workflow needs, but each workflow frames it differently
(transfer destinations, new-repo pre-flights). Extraction keeps the
authenticated-lookup semantics — and the private-repo visibility guarantee —
in one script. Known composers:

- [`github-repo-transfer-destination-conflict-check`](../../transfer/github-repo-transfer-destination-conflict-check/SKILL.md)
  — shells out to `scripts/check-name-conflicts.py` with the destination owner
  and the transfer repo list; consumes the per-name verdicts to gate the
  transfer initiation stage.

## Related Skills

- [`gh-repo-create`](../../../gh-repo-create/SKILL.md) — repo creation; this
  skill is its name-availability pre-flight reference.
- [`github-rest-api-fallback`](../../../github-rest-api-fallback/SKILL.md) —
  REST fallback patterns for environments without the `gh` CLI.
- [`github-repo-state-fingerprint`](../github-repo-state-fingerprint/SKILL.md)
  — sibling Batch-1 engine for post-change state verification.

## 1. When to Apply

Use this skill whenever repository-name availability under a GitHub owner
account must be established **before** a naming decision:

- Pre-flight for creating a new repository (name must be free).
- Pre-flight for a repository **transfer** destination (no name collision under
  the destination owner — the destination owner receives `<repo>` names).
- Auditing which of a candidate list is already taken under an account.

**Anti-trigger:** If the name is checked for any other purpose than
owner-scoped availability (e.g., trademark screening), this skill does not
apply. If you only need the owner's repo inventory (not per-name verdicts),
the `--enumerate` mode alone may suffice.

## 2. Why an Authenticated Per-Name Lookup (Not a Listing Shortcut)

| Option | Verdict | Reason |
| --- | --- | --- |
| Manual check in the GitHub web UI | ❌ | not automatable; no machine-readable record |
| Public listing (`gh repo list <owner> --limit N`, public API) | ❌ | **blind to private repos** — a same-named private repo reads as free (observed on a 960-repo account) |
| Creating the repo/transfer and catching the error | ❌ | mutates state; destructive probe |
| Authenticated `GET /repos/<owner>/<name>` per candidate | ✅ | precise per-name verdict including private repos; read-only |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../../../ai-agent-rules/scripting-language-selection-rules.md).

## 3. Required Inputs & Environment

| Requirement | Minimum | Notes |
| --- | --- | --- |
| `gh` CLI | authenticated for the owner account | `gh auth status` must show the owner login |
| Owner token | `--token-user <login>` when ambient auth is not the owner | resolved via `gh auth token --user <login>`; required for private-visible verdicts |
| Candidate names | `--repos` and/or `--repos-file` | file takes one name per line; `#` comments and blanks skipped |
| Python | 3.12+ | pure stdlib; no pip dependencies |

## 4. Operational Logic

### 4.1 CLI contract

```bash
python3 scripts/check-name-conflicts.py --owner <owner> --repos a,b,c [--token-user <login>] [--enumerate]
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--owner <login>` | required | account the names are checked under |
| `--repos <csv>` | — | comma-separated candidate names |
| `--repos-file <path>` | — | one candidate name per line |
| `--token-user <login>` | ambient auth | run lookups with this account's token |
| `--enumerate` | off | also paginate the owner's full repo list (includes private) and report `enumerated_total` |

### 4.2 Output contract

One JSON object per candidate, then a summary object — all on stdout;
diagnostics on stderr. Exit `0` = all available, `1` = any taken/unknown,
`2` = usage error.

```json
{"repo": "new-repo", "owner": "<owner>", "status": "AVAILABLE", "http_status": 404, "in_enumeration": false}
{"owner": "<owner>", "checked": 1, "taken": [], "available": ["new-repo"], "unknown": [], "counts": {"TAKEN": 0, "AVAILABLE": 1, "UNKNOWN": 0}}
```

### 4.3 End-to-end example

```bash
SCRIPTS=.agents/skills/github/repo/github-repo-name-conflict-check/scripts
python3 "$SCRIPTS"/check-name-conflicts.py \
    --owner <owner> --repos new-a,new-b --token-user <login> --enumerate
```

## 5. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`github-repo-transfer-destination-conflict-check`](../../transfer/github-repo-transfer-destination-conflict-check/SKILL.md) | Shells out to `scripts/check-name-conflicts.py` with the destination owner and the transfer repo list; consumes the per-name verdicts (exit 1 blocks initiation) and folds them into its pre-transfer gate report. |

## 6. Prohibited Behaviors

- Running availability lookups without the owner's token when private-repo
  visibility matters — public listing is blind to private repos.
- Mutating anything — this skill is strictly read-only (no creation, rename, or
  delete probes).
- Treating `UNKNOWN` as `AVAILABLE` — unknown is a blocker, not a pass.
- Reimplementing the 200/404 classification in composers — shell out to
  `check-name-conflicts.py`.

## 7. Change History

| Timestamp | Summary of Changes | Rationale |
| --- | --- | --- |
| [2026-09-30 15:35] | Initial skill v1 created | Extraction of the authenticated per-name conflict check used before repo transfers (public-listing blindness observed on a 960-repo account) |

## 8. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

## 9. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.
