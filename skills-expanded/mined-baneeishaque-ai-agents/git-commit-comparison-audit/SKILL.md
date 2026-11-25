---
name: git-commit-comparison-audit
description: Active instruction set for side-by-side comparative analysis between two commits via skill orchestration.
category: Git-Hygiene
---

# Git Commit Comparison Audit Skill (v1)

This skill mandates high-fidelity comparison of two Git commits. It **orchestrates** the `git_commit_details_audit` skill to retrieve individual commit data and then synthesizes a "Why vs. What" comparative report.

***

## 1. Environment & Dependencies

The agent MUST autonomously verify the availability of required tools:

- **Git**: Verified via `which git`.
- **Python 3**: Verified via `which python3`.
- **PowerShell**: Verified via `$PSVersionTable.PSVersion` (required for the equivalence-check primitive — §2.2).
- **Orchestrated Skill**: Verify existence of `.agents/skills/git-commit-details-audit/scripts/audit.py`.

### 1.1 PowerShell Mandate

The equivalence-check primitive (§2.2) is **PowerShell-first**. All quoting, escape correctness, and profile
initialization rules are governed by
[`script-management-rules.md`](../../../ai-agent-rules/script-management-rules.md). `-NoProfile` is **forbidden**.

***

## 2. Operational Logic: The Comparison Workflow

### 2.1 Automated Orchestration (Industrial Standard — Metadata + Reachability + Submodules)

The agent MUST use the `compare.py` orchestrator to guarantee standardized tabular formatting and automated
submodule depth.

```bash
# Execute the comparison orchestrator
python3 .agents/skills/git-commit-comparison-audit/scripts/compare.py <SHA1> <SHA2>
```

#### Detailed Command Explanation:
- `python3`: Invokes the interpreter.
- `compare.py`: The specialized orchestrator that calls the detail-audit script for each SHA.
- `<SHA1> <SHA2>`: The two commits to be compared.

#### Output Features:
- **Side-by-Side Metadata**: Comparative table of Author + AuthorDate, Committer + CommitDate (surfaced separately so rebases, cherry-picks, and filter-repo rewrites are visible), and Message.
- **Reachability Audit**: Divergence status for branches/tags across both commits.
- **Submodule Pointer Audit**: Detection of mismatched submodule pointers.
- **Recursive Submodule Depth**: If pointers differ, the orchestrator automatically performs a detail-audit *inside* the submodule for both target SHAs.
- **1. High-Fidelity Pointer Comparison**: Tabular summary of parent commits vs. submodule SHAs and their functional significance.
- **2. Recursive History Audit Results**: Orchestrated audit of the submodule's internal history between the two pointers.
- **3. High-Level Impact: "Why vs. What"**: Pedagogical synthesis of the technical delta and historical rationale.

### 2.2 Content Equivalence Check (Depth Primitive)

When the comparative metadata table from §2.1 shows two commits with **different SHAs but identical author identity
and dates** — the canonical signature of a rewrite-mirror, cherry-pick, or filter-repo run — the agent MUST run the
PowerShell equivalence-check primitive to determine whether the two commits are **content-equivalent** or
**semantically divergent**.

```powershell
pwsh-preview -File .agents/skills/git-commit-comparison-audit/scripts/equivalence-check.ps1 `
    -Sha1 <SHA1> -Sha2 <SHA2> [-RepoPath <path>]
```

Fallback when `pwsh-preview` is unavailable:

```powershell
pwsh -File .agents/skills/git-commit-comparison-audit/scripts/equivalence-check.ps1 -Sha1 <SHA1> -Sha2 <SHA2>
```

> **Do not pass `-NoProfile`** — see §1.1.

#### What the primitive checks (five depth analyses)

| # | Analysis | Command | What it proves |
| :--- | :--- | :--- | :--- |
| 1 | **Patch-ID** | `git show <sha> \| git patch-id --stable` | Content fingerprint independent of SHA, parent, author, committer, and dates. Equality means the *diff against the parent* is identical on both sides. |
| 2 | **Tree SHA** | `git rev-parse <sha>^{tree}` | Exact byte-level tree identity. Equality means every file at that commit has identical content and mode on both sides. |
| 3 | **Tree diff** | `git diff --stat <sha1> <sha2>` | File-level delta — only emitted when trees differ. Quantifies the divergence. |
| 4 | **Subjects & bodies** | `git log -1 --format='%s%n%n%b'` | Message-level delta — the typical (and only) divergence in a reword-rebase mirror where trees + patch-id are identical. |
| 5 | **Refinement check** | line-by-line normalisation (`lower-case` + `_ -> -`) over `git diff --unified=0` | Detects deterministic kebab-case rewrites. Triggers only when trees differ and emits a verdict of REFINED when every `-`/`+` line pair matches after normalisation. |

#### Interpretation matrix

| Patch-ID | Tree SHA | Refinement | Verdict | Action |
| :--- | :--- | :--- | :--- | :--- |
| **=** | **=** | n/a | **CONTENT-EQUIVALENT** — pure rewrite-mirror (typically a reword) | Safe force-push after full pairwise audit completes |
| **=** | **≠** | n/a | **PATCH-EQUIVALENT BUT TREES DIFFER** — different parents producing the same diff (e.g., cherry-pick across disjoint histories) | Inspect ancestry; treat as equivalent *only* on the diff axis |
| **≠** | **=** | n/a | (rare) Trees match but patches differ — usually means one side has empty diff because the parent itself was rewritten | Inspect parents individually |
| **≠** | **≠** | **MATCH** (every line-pair equal under `lower-case` + `_ -> -`) | **REFINED EQUIVALENT** — intentional kebab-case normalisation; local is the refined form | Keep local form; safe to force-push |
| **≠** | **≠** | **NO MATCH** | **DIVERGENT** — true semantic delta | Cherry-pick / rebase / merge reconciliation required |

> The refinement check is intentionally conservative: it triggers only when the count of removed and added lines is
> equal AND every pair matches after normalisation. Mixed deltas (one normalisation + one semantic change) fall
> through to **DIVERGENT** and require human review.

> This primitive is the **SSOT** for content-equivalence determination. Other skills (notably
> [`git-divergence-audit`](../git-divergence-audit/SKILL.md)) MUST reference this section instead of duplicating
> the patch-id / tree-SHA logic.

### 2.3 Sequence-Aware Pair Walker (Branch-vs-Branch Audit)

When auditing **two diverged branches** (typical post-rewrite scenario), the agent MUST use the sequence-aware
walker rather than calling `equivalence-check.ps1` manually for each pair.

```powershell
pwsh-preview -File .agents/skills/git-commit-comparison-audit/scripts/pair-walker.ps1 `
    -LocalBranch <local_branch> -RemoteBranch <remote_branch> [-StartIndex <N>] [-MaxPairs <M>]
```

#### What the walker does

1. Enumerates both branches in oldest-first order (`git log --reverse`).
2. For each positional pair `(local[i], remote[j])`, invokes the §2.2 equivalence-check primitive.
3. Advances both indexes by 1 on any non-DIVERGENT verdict (CONTENT-EQUIVALENT, PATCH-EQUIVALENT, REFINED EQUIVALENT).
4. On DIVERGENT, runs the **split-equivalence probe** before stopping (see below).
5. Stops on the first true DIVERGENT and prints the full equivalence-check output for that pair.

#### Split-Equivalence Probe (sixth verdict category)

A common rewrite pattern is to **split** a single legacy commit into two atomic commits per a project rule
(e.g., the Generated/Custom `.gitignore` split mandated by
[`git-gitignore-handling-rules.md`](../../../ai-agent-rules/git-gitignore-handling-rules.md) §2). Such splits
appear as DIVERGENT to a single-pair check because the local commit only carries one half of the original tree.

When the equivalence-check returns DIVERGENT, the walker tests two hypotheses by comparing **trees**:

| Hypothesis | Test | Action on success |
| :--- | :--- | :--- |
| **A. Local was split** | `tree(local[i+1]) ≡ tree(remote[j])`? | Advance local by 2, remote by 1 |
| **B. Remote was split** | `tree(remote[j+1]) ≡ tree(local[i])`? | Advance local by 1, remote by 2 |

Tree equivalence here uses the same two-tier comparison from §2.2:

- Tree-SHA identical → **SPLIT EQUIVALENT**
- Trees differ but every line-pair matches under kebab-normalisation → **SPLIT REFINED EQUIVALENT**

#### Updated interpretation matrix (six verdicts)

| Verdict | Trigger | Action |
| :--- | :--- | :--- |
| **CONTENT-EQUIVALENT** | `patch-id ≡` AND `tree ≡` | Advance both by 1 |
| **PATCH-EQUIVALENT BUT TREES DIFFER** | `patch-id ≡` AND `tree ≠` | Advance both by 1; ancestry note required |
| **REFINED EQUIVALENT** | `tree ≠` AND every line pair normalises (kebab) | Advance both by 1 |
| **SPLIT EQUIVALENT** | DIVERGENT pair, but `tree(local[i+1]) ≡ tree(remote[j])` (or symmetric) | Advance the split side by 2, the other by 1 |
| **SPLIT REFINED EQUIVALENT** | DIVERGENT pair, but `tree(local[i+1])` matches `tree(remote[j])` after kebab-normalisation (or symmetric) | Advance the split side by 2, the other by 1 |
| **DIVERGENT** | None of the above succeed | Walker stops; human review required |

> The split probe inspects only the *adjacent* commit on each side. If a split spans more than 2 commits (rare),
> the walker will still stop at DIVERGENT and the human operator can extend the probe manually.

***

## 3. Pedagogical Narrative Mandate

Every comparison report MUST follow the **"Why vs. What"** standard, utilizing the auto-generated summary from `compare.py`:

1. **The What**: The technical delta (e.g., "SHA1 points to functional rules, SHA2 is a legacy snapshot"). This is pre-populated by the orchestrator but should be refined by the agent for clarity.
2. **The Why**: The historical rationale (e.g., "Commit 64f0f89 was preserved in the 2026-04-04 backup branches during the industrialization rebase"). This MUST be provided by the agent using context from the current session.

***

## 4. Traceability & Related Conversations

- **Session Log**: Results from this skill should be linked to the relevant industrial walkthrough.
- **Rules Mapping**: All comparative findings MUST comply with the **[Git Operation Rules](../../../ai-agent-rules/git-operation-rules.md)**.

***

## 5. Post-Audit Verification Checklist

- [ ] Are both SHAs independently audited using the detail-audit script?
- [ ] Does the report include a side-by-side metadata table (Author + Committer)?
- [ ] When SHAs differ but identity matches, was the §2.2 equivalence-check primitive run and a verdict recorded?
- [ ] For branch-vs-branch audits, was the §2.3 sequence-aware walker used (with split-probe enabled)?
- [ ] Is the submodule pointer shift clearly identified and analyzed?
- [ ] Does the "Why vs. What" narrative explain the divergence between versions?
