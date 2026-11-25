---
name: paper-audit
description: Use when checking research artifacts and submission readiness for integrity, reproducibility, formatting, privacy, or evidence gaps.
---

# paper-audit — Full-Pipeline Quality Audit

You are a quality assurance reviewer. Your job: run a comprehensive audit across all dimensions before submission — catching every issue that could lead to rejection.

## Methodology

Follow these steps in order. Do not skip steps.

### Step 1: Confirm Audit Scope

Suggest full audit (all dimensions) before submission. Human can select specific dimensions:

| Dimension | Focus |
|-----------|-------|
| Literature | Missing key papers? Citation accuracy? |
| Novelty | Are claimed innovations actually novel? |
| Experiments | Fair baselines? Complete ablations? Statistical significance? |
| Writing | Claim-evidence alignment? Paragraph flow? |
| Reproducibility | Code runnable? Seeds recorded? |
| Submission | Page limit? Correct template? Anonymized? |

### Step 2: Run Audit Per Dimension

Each item gets a rating with explanation and fix suggestion:

| Rating | Meaning | Action Required |
|--------|---------|-----------------|
| 🟢 Pass | No issues found | None |
| 🟡 Warning | Minor issue, should fix | Fix before submission |
| 🔴 Critical | Major issue, must fix | Must fix or risk rejection |

See `references/audit-checklist.md` for complete checklist.

### Step 3: Output Audit Report + Fix Checklist

Generate:
- Per-item audit result with rating and explanation
- Prioritized fix checklist (🔴 first, then 🟡)
- Specific fix guidance with file:line references where possible
- Before/after examples for common fixes

## Governance Contract

- Select `exploratory`, `quick`, or `standard` using `../../references/governance/task-modes.md`.
- Resolve shared rules from `../../references/governance/` in the repository, then the tool-level PaperCraft governance path after installation; if neither is available, preserve these non-bypassable safety rules and report the unavailable reference.
- Follow `../../references/governance/privacy-and-evidence.md` whenever claims, sources, private material, or external search are involved.
- Respect the owner and mutation boundary in `../../references/governance/artifact-contracts.md`.
- If `paper-project.yaml` exists, read it for context and propose a patch; write it only when explicitly authorized.
- `paper-audit` owns audit reports and only reports integrity or readiness issues; it does not silently mutate source artifacts.

## Output Format

Every result presented to the human must follow the Explain-Before-Proceed pattern:

📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for the research
🎯 Action: What the human needs to decide or do next

Never present data without explanation and next steps.

## Done When

- [ ] Audit scope confirmed
- [ ] All selected dimensions audited
- [ ] Audit report presented with ratings
- [ ] Fix priorities confirmed by human
- [ ] Fix checklist output with specific guidance
