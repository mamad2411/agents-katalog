---
name: pwrl-review-sync-status
description: "Post review findings back to GitHub PR with comments, formal reviews, and labels. Final phase of pwrl-review orchestrator."
argument-hint: "[report artifact from pwrl-review-report]"
---

# pwrl-review-sync-status — GitHub PR Integration & Reporting

**Purpose:** Final phase of review workflow. Takes the report artifact from Phase 4 and synchronizes all review findings back to GitHub:
- Posts detailed review findings as PR comment
- Creates formal GitHub review (APPROVE or REQUEST_CHANGES)
- Updates PR labels based on verdict and quality scores
- Resolves review workflow by posting status to GitHub

## Interaction Method

- Minimal user interaction (status updates only)
- Display confirmation of GitHub updates posted
- If GitHub API fails, provide fallback: "Review findings saved locally. Manual GitHub posting may be needed."
- Ask one question if needed: "Post this review to GitHub? [yes/no]"

## Input: Report Artifact

Expects artifact from `pwrl-review-report` with:

```yaml
report_id: YYYY-MM-DD-UNN-report
created: ISO-8601-timestamp

# Executive Summary
verdict: APPROVED | REQUEST CHANGES | REJECTED
critical_issues: [count]
major_issues: [count]
minor_issues: [count]

# Quality Scores
overall_score: [0-100]%
code_quality_score: [0-100]%
security_score: [0-100]%
test_coverage_score: [0-100]%
documentation_score: [0-100]%

# Detailed findings organized by category
code_quality_findings: [list]
security_findings: [list]
test_coverage_findings: [list]
documentation_findings: [list]
integration_findings: [list]

# Sign-off
approved_by: [user/reviewer]
approval_date: ISO-8601-timestamp
```

Plus: PR number or branch reference from original input context

## Output: GitHub PR Updates

**Primary Output:**
- GitHub PR comment with formatted review findings and metrics
- Formal GitHub review (APPROVE or REQUEST_CHANGES action)
- PR labels updated (review-approved, review-changes-requested, security-concerns, coverage-low, etc.)

**Status Output:**
- Sync status logged: "Review findings posted to GitHub PR [#N]"
- All updates timestamp for audit trail

## Workflow

### Step 1: Validate Report Artifact & PR Context

1. Check report artifact has:
   - Valid `report_id`
   - Verdict (APPROVED/REQUEST_CHANGES/REJECTED)
   - All quality scores
   - Findings populated (even if empty lists)
   - Sign-off metadata

2. Resolve PR context:
   - Extract PR number from original input (argument or context)
   - Verify PR exists in GitHub
   - Get current PR metadata (title, description, base branch)

3. **If validation fails:**
   - Return error: "Report artifact invalid or PR context missing"
   - Optionally fall back to local file storage

### Step 2: Format Review for GitHub

**Comment Header:**
- Verdict prominently displayed (✅ APPROVED / ⚠️ REQUEST CHANGES / ❌ REJECTED)
- Link to full report artifact (if stored)
- Execution timestamp

**Quality Metrics Section:**
- Display as visual progress bars:
  ```
  📊 Code Quality:    ████████░░ 85%
  📊 Security:        ██████████ 100%
  📊 Test Coverage:   ███████░░░ 75%
  📊 Documentation:   █████████░ 90%
  ─────────────────────────────
  Overall Score:      ████████░░ 87%
  ```
- Critical / Major / Minor issue counts with emoji severity
- Pass/Fail status for each dimension

**Findings Section:**
- Group by severity (CRITICAL, MAJOR, MINOR)
- For each finding:
  - File:line reference (clickable)
  - Issue description
  - Category (Code Quality, Security, Tests, Docs, Integration)
  - Severity badge
- Limit to top 20 findings (full list in linked artifact if deep review)

**Action Items (for REQUEST CHANGES only):**
- Numbered list of top 3-5 fixes required
- Specific: not vague ("Remove unused variable" not "clean up")
- Actionable: includes file:line if applicable

**Next Steps:**
- For APPROVED: "Ready to merge ✅"
- For REQUEST CHANGES: "Please fix the above items and request re-review"
- For REJECTED: "Please discuss approach with team before resubmitting"

### Step 3: Post Comment to GitHub PR

1. **Construct comment** with formatted findings (Step 2)
2. **Post to PR** using GitHub API:
   ```
   POST /repos/{owner}/{repo}/issues/{issue_number}/comments
   {
     "body": "[formatted comment]"
   }
   ```
3. **Handle errors:**
   - If rate-limited: Retry after rate limit reset
   - If PR doesn't exist: Log error, save locally
   - If auth fails: Provide OAuth re-auth instructions

4. **Success:** Store comment ID for potential updates/edits later

### Step 4: Create Formal GitHub Review

**Review Action:** Based on verdict (see [review-verdict-mapping.md](references/review-verdict-mapping.md))

| Verdict | GitHub Action | Reason |
|---------|---|---|
| APPROVED | **APPROVE** | Code ready to merge |
| REQUEST CHANGES | **REQUEST_CHANGES** | Issues found, please fix |
| REJECTED | **REQUEST_CHANGES** (blocking) | Major blockers, discuss first |

1. **Post review** using GitHub API:
   ```
   POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
   {
     "body": "[summary of review]",
     "event": "APPROVE" | "REQUEST_CHANGES" | "COMMENT"
   }
   ```

2. **Review body:** Brief summary (2-3 lines) of key findings
   - APPROVED: "All checks passed. Code is ready to merge."
   - REQUEST CHANGES: "X critical/major issues require fixes before merge"
   - REJECTED: "Blocking issues found. Please discuss before resubmitting."

3. **Handle errors:**
   - If already reviewed: Skip (don't duplicate)
   - If auth fails: Fall back to comment only

### Step 5: Update PR Labels

**Label Assignment Rules:** (see [review-verdict-mapping.md](references/review-verdict-mapping.md))

**Auto-add labels:**
- `review-approved` (if APPROVED)
- `review-changes-requested` (if REQUEST CHANGES)
- `review-rejected` (if REJECTED)
- `security-concerns` (if security CRITICAL/MAJOR found)
- `coverage-low` (if coverage < threshold)
- `docs-incomplete` (if documentation issues found)
- `build-failing` (if integration check failed)

**Auto-remove old labels:**
- Remove `review-approved` if new review is REQUEST CHANGES/REJECTED
- Remove `review-changes-requested` if new review is APPROVED
- Remove `coverage-low` if new coverage meets threshold
- Keep: `security-concerns`, `docs-incomplete`, `build-failing` (must be manually cleared)

**Label persistence:**
- Save labels applied for audit trail
- Log removed labels for history
- Allow user override if needed

### Step 6: Post Status & Wrap Up

**Final Status Message:**
```
✅ Review posted to GitHub PR #{number}
   - Comment with findings: ✓
   - Formal review (APPROVE/REQUEST_CHANGES): ✓
   - Labels updated: ✓
   - Ready for merge? [Based on verdict]
```

**Completion Logging:**
- Log timestamp of all GitHub updates
- Store PR number and link for reference
- Record any GitHub API errors or retries
- Indicate local fallback if needed

**Next Action (by Verdict):**
- APPROVED: "PR is ready to merge"
- REQUEST CHANGES: "Author should fix issues and request re-review"
- REJECTED: "Team discussion recommended before resubmitting"

---

## Error Handling

| Error | Recovery Strategy |
|-------|-------------------|
| **PR not found** | Return error; confirm PR number with user |
| **Auth token invalid/expired** | Request OAuth re-auth; provide link to GitHub settings |
| **Rate limited** | Wait and retry; inform user of delay |
| **GitHub API unavailable** | Fall back to local artifact save; suggest manual posting |
| **Report artifact invalid** | Return error; return to pwrl-review-report |
| **Formatting fails** | Use plain text fallback; post unformatted findings |
| **Comment too large** | Truncate to 60KB limit; link to full artifact |
| **Label doesn't exist** | Create label with standard format or skip |
| **Already reviewed** | Skip formal review; post comment only (avoid duplicates) |

**Retry Policy:**
- Max 3 retries for transient errors (rate limit, timeout)
- Exponential backoff: 1s → 2s → 4s
- After 3 retries: Fall back to local save and inform user

---

## Testing Coverage

**Happy Path Tests:**
- ✅ APPROVED verdict → APPROVE action, correct labels
- ✅ REQUEST CHANGES verdict → REQUEST_CHANGES action, action items clear
- ✅ REJECTED verdict → REQUEST_CHANGES action, blocking issues noted
- ✅ Comment formatted correctly → Markdown renders properly
- ✅ Labels applied and old labels removed
- ✅ All 5 quality metrics shown correctly

**Edge Cases:**
- ✅ Very large findings list (truncate to top 20)
- ✅ No findings (empty lists, APPROVED with zero issues)
- ✅ All CRITICAL issues (REJECTED, clear escalation)
- ✅ Mixed findings (some pass, some fail)
- ✅ Security CRITICAL (triggers security label + warning)
- ✅ PR already has review (skip duplicate, post comment only)

**Error Cases:**
- ✅ GitHub rate limited (retry with backoff)
- ✅ Auth token expired (request re-auth)
- ✅ PR doesn't exist (error + local save)
- ✅ Comment too large (truncate to 60KB)
- ✅ Network timeout (retry and fallback)

**Output Validation:**
- ✅ Comment posted successfully
- ✅ GitHub review created (correct action)
- ✅ Labels match verdict + findings
- ✅ All updates timestamped
- ✅ Audit trail logged

---

## When to Use

- **Always:** As final phase of pwrl-review orchestrator (after Phase 4)
- **Manual trigger:** If GitHub sync was skipped and findings need posting
- **Retry scenario:** If initial sync failed, retry after resolving errors
- **PR updates:** When re-running review on same PR, updates existing comment + review

---

## Related Documentation

- [review-verdict-mapping.md](references/review-verdict-mapping.md) — Verdict → GitHub action & label mappings
- [github-pr-sync-protocol.md](references/github-pr-sync-protocol.md) — GitHub API details, OAuth, retry strategy
- [artifact-schemas.md](../pwrl-review/references/artifact-schemas.md) — Report artifact structure
- [verdict-criteria.md](../pwrl-review/references/verdict-criteria.md) — Verdict decision logic

---

## Dependencies

**GitHub Integration:**
- GitHub account with repo access
- GitHub OAuth token (PAT) with PR read/write permissions
- `gh` CLI or direct API access via library

**Artifacts:**
- Report artifact from Phase 4 (pwrl-review-report)
- PR number from original input context

**External Services:**
- GitHub API: `api.github.com` (rate limits: 60 req/hr unauthenticated, 5000 req/hr authenticated)
- Network connectivity for GitHub API calls

