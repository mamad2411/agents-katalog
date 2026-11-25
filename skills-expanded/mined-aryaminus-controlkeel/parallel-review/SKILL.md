---
name: parallel-review
description: "DEPRECATED for inline use — this is now a CLI composite (`controlkeel review --parallel`). Kept callable only for explicitly requested comprehensive security+quality orchestration; otherwise invoke security-review + deep-code-quality-review separately or via that CLI."
when_to_use: "Do NOT invoke via skills when possible — use `controlkeel review --parallel` (CLI). Invoke this skill only when explicitly asked for comprehensive security+quality orchestration."

argument-hint: "[PR, branch, or diff]"
disable-model-invocation: true
deprecated: true
prefer_cli: "controlkeel review --parallel"
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: review
  ck_mcp_tools: [ck_validate, ck_finding, ck_git_diff, ck_review_submit, ck_route, ck_delegate]
  related_skills: [security-review, deep-code-quality-review]
---

# Parallel Review

Run `security-review` and `deep-code-quality-review` concurrently, synthesize into one prioritized report.

## Do NOT use when
- Only security OR quality review needed (use the specific skill directly)
- During normal coding
- For single-file changes where sequential review is fast enough

## Workflow

1. Run `ck_git_diff` to gather the diff. Run `ck_validate` for automated findings.
2. Launch both reviews (via `ck_delegate` or sequential invocation):
   - **Security**: `security-review` skill — OWASP, injection, auth, secrets, deps
   - **Quality**: `deep-code-quality-review` skill — abstraction, file size, spaghetti, layering
   Both record findings independently via `ck_finding`.
3. Synthesize:
   - Deduplicate: same code path flagged by both → one finding, higher severity
   - Prioritize: critical > high > medium > low; security > quality > reviewability
   - Weight overlaps: flagged by both = higher confidence
   - Resolve disagreements with your own judgment
4. Submit via `ck_review_submit` (review_type: `diff`) with combined findings.
5. **Wait for approval** before merge/deploy.

## Rules

- Both reviews must complete — do not skip one
- Blocked finding from either = merge blocked
- Deduplicate, do not double-count

## Output

- Combined findings (deduplicated, prioritized)
- `ck_review_submit` diff review
- Clear verdict: merge / merge with warnings / blocked
