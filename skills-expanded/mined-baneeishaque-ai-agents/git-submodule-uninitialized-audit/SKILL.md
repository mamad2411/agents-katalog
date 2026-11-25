---
name: git-submodule-uninitialized-audit
description: Recursive audit of uninitialized submodules (top-level + nested) with per-pointer reachability classification, delegating dead-upstream diagnostics to the dead-upstream audit skill.
category: Git & Repository Management
---

# Git Submodule Uninitialized Audit Skill (v1)

This skill provides a deterministic, **recursive** audit of every submodule pointer in a parent repository (and inside
each already-initialized submodule), classifying each as **Initialized**, **Uninitialized-Reachable**,
**Uninitialized-Unreachable**, or **Orphan-Gitlink** (recorded in tree but missing from `.gitmodules`). The skill is
strictly diagnostic — it never mutates the working tree, never runs `git submodule update`, and never opens network
write operations. Remediation belongs to the handler skill
([git-submodule-uninitialized-handler](../git-submodule-uninitialized-handler/SKILL.md)).

***

## 1. Environment & Dependencies

Before execution, the agent **MUST** verify the industrial environment.

1. **Verify Git** (`>= 2.30`):

    ```bash
    git --version
    ```

2. **Verify `curl` + `python3`** (used by the delegated dead-upstream probe):

    ```bash
    curl --version | head -1
    python3 --version
    ```

3. **Position at parent repo root**:

    ```bash
    git rev-parse --show-toplevel
    ```

    All subsequent commands assume the working directory is the value above.

***

## 2. Phase 1: Recursive Pointer Enumeration

Enumerate every gitlink reachable from the parent — both top-level and nested — exactly once.

1. **Top-level pointers** (status of every entry in parent's `.gitmodules`):

    ```bash
    PAGER=cat git submodule status
    ```

    Status leading character meanings:

    | Prefix | Meaning |
    | :--- | :--- |
    | ` ` (space) | Initialized, working tree matches recorded SHA. |
    | `+` | Initialized, working tree at a different SHA than recorded. |
    | `-` | **Uninitialized** — no `.git` directory present. |
    | `U` | Merge conflict in the submodule. |

2. **Recursive pointers** (top-level + every level of nesting):

    ```bash
    PAGER=cat git submodule status --recursive
    ```

    * `--recursive` — descends into each initialized submodule's own `.gitmodules` and reports its children.
    * Lines beginning with `-` at any depth are the audit's primary subject.

3. **Orphan-gitlink scan** (run inside every submodule that has its own `.gitmodules` — they may declare
   sibling pointers in the tree but omit them from `.gitmodules`):

    ```bash
    PAGER=cat git submodule foreach --quiet --recursive '
        if [ -f .gitmodules ]; then
            tree_paths=$(git ls-tree -r HEAD | awk "\$2==\"commit\"{print \$4}" | sort)
            cfg_paths=$(git config --file .gitmodules --get-regexp "\.path$" | awk "{print \$2}" | sort)
            orphans=$(comm -23 <(echo "$tree_paths") <(echo "$cfg_paths"))
            if [ -n "$orphans" ]; then
                echo "ORPHAN in $displaypath:"
                echo "$orphans" | sed "s/^/  /"
            fi
        fi
    '
    ```

    * `git ls-tree -r HEAD | awk '$2=="commit"'` — extracts every gitlink path from the working commit's tree.
    * `comm -23` — set difference: paths in tree but not registered in `.gitmodules`.
    * The `displaypath` env-var is supplied by `submodule foreach` and reports the path relative to the parent root.

***

## 3. Phase 2: Per-Pointer Classification

For each pointer surfaced in Phase 1, assign exactly one verdict.

| Verdict | Detection | Required Next Action |
| :--- | :--- | :--- |
| **Initialized** | Status line starts with ` ` or `+`. | None (audit-only). |
| **Uninitialized-Reachable** | Status line starts with `-` **AND** upstream URL returns HTTP `200` (Phase 3). | Hand off to handler skill. |
| **Uninitialized-Unreachable** | Status line starts with `-` **AND** upstream URL returns 4xx/5xx. | Delegate to [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md). |
| **Orphan-Gitlink** | Path appears in §2.3 orphan scan. | Delegate to [`git-submodule-orphan-gitlink-recovery`](../git-submodule-orphan-gitlink-recovery/SKILL.md) (handler skill orchestrates this). |
| **Conflict** | Status line starts with `U`. | Out of scope — instruct user to resolve merge first. |

***

## 4. Phase 3: Reachability Probe

For every pointer flagged in §3 as `Uninitialized-*`, resolve the upstream URL and probe HTTP reachability **without
cloning**.

1. **Resolve URL for a top-level pointer**:

    ```bash
    git config --file .gitmodules --get "submodule.<name>.url"
    ```

2. **Resolve URL for a nested pointer** (run from inside the parent of the nested):

    ```bash
    git -C <parent-submodule-path> config --file .gitmodules --get "submodule.<name>.url"
    ```

3. **HTTP probe** (no auth required for public repos; `-L` follows redirects):

    ```bash
    code=$(curl -sI -o /dev/null -w "%{http_code}" -L --max-time 8 "${url%.git}")
    echo "$code  $url"
    ```

    * `-sI` — silent HEAD request.
    * `-o /dev/null -w "%{http_code}"` — suppress body, print only the final status code.
    * `--max-time 8` — bounded wait so a hung host cannot stall the audit.
    * `${url%.git}` — strip trailing `.git` for the HEAD probe (GitHub's `.git` suffix returns 301 → final URL).

4. **HTTP code → verdict**:

    | Code | Verdict | Notes |
    | :--- | :--- | :--- |
    | `200` | Reachable | Public repo accessible to anonymous client. |
    | `301`, `302` | Reachable (after redirect) | `-L` already followed; final code applies. |
    | `401`, `403` | Unreachable (auth) | May still be cloneable with `gh auth` — note for handler. |
    | `404` | Unreachable (deleted/private) | Hand to dead-upstream audit. |
    | `5xx` | Inconclusive | Retry once, then mark as Unreachable if persistent. |

5. **For every Unreachable verdict**: delegate to
   [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md) §4 (SHA-based fork/mirror search)
   to determine whether the SHA exists anywhere on GitHub. The audit consumes that skill's verdict matrix and propagates
   it into this skill's report.

***

## 5. Phase 4: Audit Report

Render a single, deterministic markdown table summarizing every pointer in dependency order (parent → nested).

### 5.1 Report Template

```markdown
# Submodule Initialization Audit — <repo-name>

**Generated**: <YYYY-MM-DD>
**Parent root**: `<absolute-or-relative-path>`
**Total pointers (recursive)**: <N>
**Initialized**: <I>  |  **Uninit-Reachable**: <R>  |  **Uninit-Unreachable**: <U>  |  **Orphan**: <O>  |  **Conflict**: <C>

| # | Path (recursive) | Status | URL | HTTP | Verdict | Delegated To |
| :- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `<path>` | `-` | `<url>` | `200` | Uninit-Reachable | handler skill |
| 2 | `<sub>/<nested>` | `-` | `<url>` | `404` | Uninit-Unreachable | dead-upstream audit |
| 3 | `<sub>/<orphan>` | (tree-only) | (none) | n/a | Orphan-Gitlink | orphan-gitlink recovery |
```

### 5.2 Report Hygiene

- **Stable Ordering**: sort by `Path (recursive)` lexicographically so re-runs produce diffable output.
- **Absolute Paths Forbidden** (per
  [Markdown Generation Rules §4.2.9](../../../ai-agent-rules/markdown-generation-rules.md#429-redaction--pii-neutralization)):
  use repo-relative paths only.
- **Token Hygiene**: never embed any token, even prefix, in the report.
- **Save Location**: when persisted, write to
  `.agents/skills/git-submodule-uninitialized-audit/docs/audit-<YYYY-MM-DD>-<repo>.md`.

***

## 6. Operational Safety

- **Read-Only Mandate**: This skill MUST NOT execute `git submodule update`, `git submodule init`, `git fetch`,
  `git clone`, or any command that mutates `.git/config`, `.git/modules/`, or the working tree. Mutation belongs to
  the handler skill.
- **No Auto-Remediation**: Even when a verdict is unambiguous (e.g., obvious orphan), the audit report only
  **recommends** a delegate skill — it never invokes one.
- **Bounded Network**: Every outbound probe MUST set `--max-time 8` to keep the audit's wall-clock time predictable
  for repos with many submodules.
- **Concurrency Forbidden**: Probes MUST be serial. Parallel HEAD requests against the same host (typically
  `github.com`) trigger rate-limiting that pollutes the verdict.
- **Recursive Submodule Mandate** (per
  [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md)): every documented
  pointer-walk command in this skill uses `--recursive`; non-recursive variants are **FORBIDDEN**.

***

## 7. Composition Rationale

This skill is a **diagnostic composer** that reuses one base primitive plus its own enumeration logic:

```text
                        ┌─ git-submodule-dead-upstream-audit  (per dead URL → SHA search verdict) ┐
git-submodule-          │                                                                          │
uninitialized-audit ────┤                                                                          ├─→ classified report
                        └─ owns: recursive enumeration (§2) + HTTP reachability probe (§4)        ─┘
```

* **SHA-search primitive**: reused verbatim from
  [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md) §4 whenever an HTTP probe
  returns 4xx/5xx.
* **New primitive owned here**: recursive enumeration with three-axis classification (status / URL reachability /
  orphan-presence).

Inlining the SHA-search logic into this skill is **FORBIDDEN** by the Layered Composition Mandate.

***

## 8. Related Skills

- [Git Submodule Dead Upstream Audit](../git-submodule-dead-upstream-audit/SKILL.md) — invoked for every Unreachable
  pointer.
- [Git Submodule Uninitialized Handler](../git-submodule-uninitialized-handler/SKILL.md) — consumer of this skill's
  report; performs the actual init / update / orphan-recovery work.
- [Git Submodule Orphan Gitlink Recovery](../git-submodule-orphan-gitlink-recovery/SKILL.md) — referenced for any
  Orphan-Gitlink verdict; orchestrated by the handler.
- [Git Repository Status](../git-repository-status/SKILL.md) — broader repo-state audit that this skill complements.

## Composition by Higher-Level Skills

| Composer | Role | Reuses From This Skill |
| :--- | :--- | :--- |
| [`git-submodule-uninitialized-handler`](../git-submodule-uninitialized-handler/SKILL.md) | Drives every uninitialized pointer to a fully-initialized state. | Consumes the §5 audit report verbatim; routes each verdict to the appropriate remediation phase without re-enumerating. |

***

## 9. Traceability

- Origin session: **AI Suite Submodule Audit** (May 2026) — formalizes the recursive enumeration + reachability
  matrix used to surface the `gudastudio_skills` nested uninitialized pair and the `ljt-520_openclaw-backup` orphans.
- Standard authority: [Skill Factory](../skill-factory/SKILL.md) §2.0 (Layered Composition).
- Compatibility: macOS, Linux, Windows (Git Bash / Zsh).
