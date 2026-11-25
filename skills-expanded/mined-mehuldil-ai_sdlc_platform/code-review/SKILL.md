# /project:code-review

**Interactive Code Review & PR Validation**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:code-review AB#123
/project:code-review --pr=2456
/project:code-review --repo=backend --branch=feature/AB-123
```

## What This Does

1. **Loads PR** or branch against feature/story
2. **Runs automated checks** (linting, coverage, security)
3. **Reviews code** against design + story AC
4. **Identifies issues** (blocking, major, minor, suggestions)
5. **Comments on PR** with findings
6. **Tracks approval** workflow

## Interactive Flow

```
User: /project:code-review AB#123

Claude: 🔍 Code Review & PR Validation

✅ STORY LOADED:
  Story: Phone verification & OTP (AB#123)
  PR: #2456 (feature/AB-123-phone-otp)
  Files: 8 changed (6 modified, 2 new)

🚀 AUTOMATED CHECKS:

✓ Linting: PASSED (ESLint, 0 errors)
✓ Coverage: 85% (target: 80%) ✓
✓ Security Scan: 0 critical, 1 medium
✓ Type Check: PASSED (TypeScript strict mode)
✗ Performance: Slight regression (-2% on /api/signup)

⚠️ FINDINGS:

**BLOCKING ISSUES:**
  [1] Hardcoded API key in config.ts (line 34)
      Severity: CRITICAL
      Fix: Move to environment variables
      
  [2] Missing error test for invalid phone format (AC-02)
      Severity: BLOCKING
      Fix: Add test case for AC-02 edge case

**MAJOR ISSUES:**
  [1] N+1 query in getUserById (line 156)
      Severity: MAJOR
      Fix: Add database join to eliminate extra queries
      Impact: Will cause P95 latency spike at scale
      
  [2] Unhandled promise rejection (line 89)
      Severity: MAJOR
      Fix: Add .catch() or try/catch block

**MINOR ISSUES:**
  [1] Variable name not descriptive (tempPhone vs phoneNumber)
  [2] Missing JSDoc comment on public method

**SUGGESTIONS:**
  [1] Consider caching phone validation results (minor perf optimization)
  [2] Move constants to separate file for maintainability

REQUEST CHANGES FROM DEVELOPER?
  [1] Yes, comment on PR and request changes
  [2] Preview comments first
  [3] Approve with suggestions
  [4] Reject for now, ask developer to fix blocking issues

User: [1]

✓ Posted code review comments to PR #2456
✓ Requested changes (blocking + major issues)
✓ Marked PR as "Changes Requested"

WAIT FOR DEVELOPER FIX?
  [1] Yes, notify me when updated
  [2] Check back later manually
  [3] Done with review for now

User: [1]

[Developer pushes new commits fixing issues...]

✓ PR updated with new commits
✓ Re-running checks...
✓ Linting: PASSED
✓ Coverage: 87% ✓
✓ Blocking issues: RESOLVED
✓ Major issues: RESOLVED

READY FOR APPROVAL?
  [1] Yes, approve PR
  [2] Need developer to address one more thing
  [3] Request second reviewer

User: [1]

✓ Approved PR #2456
✓ Ready for merge
✓ Logged review to .sdlc/memory/code-review-AB#123.md

MERGE PR?
  [1] Yes, merge to main (squash commit)
  [2] Yes, merge to develop (merge commit)
  [3] Developer handles merge
  [4] Cancel

User: [3]

✓ Code review complete
✓ PR approved, awaiting developer merge
✓ Task moved to Code Review → Done
```

## CLI Mode

```bash
$ sdlc skill code-review AB#123
$ sdlc skill code-review --pr=2456 --auto-approve
$ sdlc skill code-review --repo=backend --branch=feature/AB-123
```

## Review Checklist

- Logic correctness (AC satisfied?)
- Code style (variant conventions)
- Performance (N+1 queries, memory leaks)
- Security (input validation, PII exposure)
- Testing (>80% coverage, all AC covered)
- Architecture alignment (design adherence)

## ADO Outcomes

- **PR Comment**: Posted with findings + links
- **Status Update**: Task moved to Code Review
- **Approval**: PR marked approved (Azure DevOps)
- **Metrics**: Coverage, performance delta tracked

## G6 Gate Clear Conditions

Gate G6 is CLEAR when:
- All blocking issues resolved
- Coverage >80%
- PR approved by minimum 2 reviewers
- All AC verified in code
- No security findings

## Next Commands

- `/project:test-design AB#123` - QA test design
- `/project:performance-testing AB#123` - Performance validation
- `/project:deployment AB#123` - Deployment prep

---

## Model & Token Budget
- **Model Tier:** Sonnet (code analysis)
- Input: ~2.5K tokens (PR diff + story)
- Output: ~2K tokens (review findings)

