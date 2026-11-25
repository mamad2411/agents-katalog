---
name: git-commit-details-audit
description: Industrial protocol for retrieving and analyzing high-fidelity commit metadata, hunks, and pedagogical explanations across the repository and its submodules.
category: Git-Hygiene
---

# Git Commit Details Audit Skill (v1)

This skill mandates the retrieval and deep analysis of commit metadata, changed files, and code hunks. It ensures 100% fidelity to the repository's **Atomic History Mandate** by providing standardized, pedagogical explanations for every modification.

***

## 1. Environment & Dependencies

The agent MUST autonomously verify the availability of required tools before executing an audit:

- **Git**: Verified via `which git`.
- **Python 3**: Verified via `which python3` (required for the industrial audit engine).
- **PAGER**: All Git commands MUST be prepended with `PAGER=cat` to prevent terminal hangs.

***

## 2. Operational Logic: The Audit Workflow

### 2.1 Automated Audit (Industrial Standard)

The agent MUST prioritize the use of the Python-backed audit engine to guarantee standardized formatting and cross-repository auto-discovery.

```bash
# Execute the audit engine from the skill's scripts directory
python3 .agents/skills/git-commit-details-audit/scripts/audit.py <COMMIT_SHA>
```

#### Detailed Command Explanation:
- `python3`: Invokes the Python 3 interpreter to run the audit logic.
- `audit.py`: The specialized engine that iterates through the main repository and all submodules to resolve the SHA.
- `<COMMIT_SHA>`: The 40-character (full) or unique short SHA of the commit to be audited.

#### Output Features:
- **Metadata**: Author + AuthorDate **and** Committer + CommitDate (separate identities — required for forensic audits where author ≠ committer such as rebases, cherry-picks, or filter-repo runs), plus the full pedagogical Commit Message.
- **Advanced Reference Tracking**: Tabular identification of all branches (local/remote) and tags containing the SHA, along with their current Tips and Divergence Status.
- **Changed Files Inventory**: High-level modification status codes.
- **Hunk Exposure**: Full diff analysis with "Why vs. What" narrative context.

### 2.2 Manual Fallback (Hunk Isolation)

If the audit engine is unavailable, the agent MUST orchestrate the **[Git Commit Metadata Extraction](../git-commit-metadata-extraction/SKILL.md)** primitive. 

1. Execute the `git_commit_metadata_extraction` primitive on the `<COMMIT_SHA>` to obtain the zero-omission metadata and exact file classifications.
2. After retrieving the core metadata, extract the full diff hunks for analysis:

```bash
# Extract full diff hunks
PAGER=cat git show -p <COMMIT_SHA>
```

*Do not attempt to write custom bash commands to extract metadata; rely entirely on the primitive to ensure fidelity.*

***

## 3. Pedagogical Narrative Mandate (Crucial)

Every audit report presented to the user MUST follow the **"Why vs. What"** standard. The agent is BLOCKED from merely restating the code changes in the diff.

1. **High-Level Impact**: Summarize *why* the commit exists and what architectural goal it accomplishes.
2. **Hunk Analysis**: For each modified file, explain the rationale behind specific logic shifts (e.g., "Hardening the regex to avoid catastrophic backtracking").
3. **Deep Technical Breakdown Table**: If the commit contains more than 3 hunks or complex logic, the agent MUST include a table in the following format:

| Line Range | Logic Modification | Pedagogical Rationale |
| :--- | :--- | :--- |
| `L123-145` | Implementation of `try-catch` wrapper | Defensive hardening against missing submodule pointers. |

***

## 4. Traceability & Related Conversations

- **Session Log**: Results from this skill should be linked to the relevant industrial walkthrough in `docs/walkthroughs/`.
- **Rules Mapping**: All audit findings MUST comply with the **[Git Operation Rules](../../../ai-agent-rules/git-operation-rules.md)**.
- **Related Skills**: Uses **[Git Commit Metadata Extraction](../git-commit-metadata-extraction/SKILL.md)** as its fallback primitive.

***

## 5. Post-Audit Verification Checklist

- [ ] Does the output match the requested "Commit Details" template?
- [ ] Are all SHAs cross-referenced between repositories (main vs. submodule)?
- [ ] Does the "Why vs. What" narrative avoid redundant "fluff"?
- [ ] Is the Markdown output 100% lint-compliant?

## 6. Message-vs-Diff Direction Audit

A commit's narrative (message verbs like "from X to Y", "align with Z", "update to W") can be the **inverse** of what the diff actually did. Reading the message alone leads to dropping the wrong commit or panic-reverting in the wrong direction.

**Trap example** (sanitized — session 2026-05-30):

Commit message:
> `chore(submodules): align <name> with personal fork — update from URL-A to URL-B`

Actual `.gitmodules` diff:

```diff
- url = URL-A
+ url = URL-B
```

Reading the message direction in isolation suggests `URL-A` was the prior canonical and `URL-B` the new (correct) destination. The diff confirms the change *direction* — but the message's narrative ("align with personal fork") can be **inverted** vs the author's later intent (the "personal fork" turned out to be the wrong target).

**Audit recipe**:

1. Read the `-`/`+` lines FIRST. Extract the concrete URL/SHA/identifier on each side.
2. Read the commit message. For every English noun phrase (e.g., "personal fork", "upstream", "main", "canonical"), mechanically map it to one of the concrete identifiers from step 1.
3. If the mapping is ambiguous (the message names something that doesn't appear in the diff), STOP and surface to the user before acting.
4. If the mapping inverts ("update **to** X" but diff shows `+X` on the OLD side), the message is reversed-direction. The commit may still be the right one to drop/revert — but proceed only after confirming the *diff* matches the desired revert.

## 7. Composition by Higher-Level Skills

| Composer | Role |
|---|---|
| [`git-submodule-misconfiguration-audit-and-revert`](../git-submodule-misconfiguration-audit-and-revert/SKILL.md) | Phase 3 — applies §6 (Message-vs-Diff Direction Audit) to the URL-changing commit before authorizing the drop. |
