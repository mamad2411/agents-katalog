---
name: code-review-standards
description: Code review mindset, severity levels, comment format, approval criteria, handling disagreements
globs: ["**/*.cs", "**/*.ts"]
alwaysApply: false
---

# Code Review Standards

How to review code: mindset, severity levels, comment quality, approval criteria.

## Code Reviewer Mindset

**ALWAYS**:
- **Assume good intent** (author did their best)
- **Ask questions** (don't assume you understand)
- **Suggest, don't demand** (except for security/critical issues)
- **Praise good code** (point out what works well)
- **Focus on logic and safety** (not style — let linters handle that)
- **Consider the context** (why this approach was chosen)
- **Be specific** (show the problem AND the fix)
- **Engage in dialogue** (not lectures)

**NEVER**:
- Approve code you don't understand
- Comment on style (use formatters/linters)
- Make personal criticism
- Demand changes without explanation
- Ignore tests (read them, they document intent)
- Bikeshed (argue about non-critical details)
- Approve without testing (run the code locally if unsure)
- Hoard reviews (unblock people quickly)

---

## Severity Levels

Every comment should have a level:

### 🔴 Critical (MUST fix before merge)
- Security vulnerability
- Data loss risk
- Breaks existing tests
- Memory leak
- SQL injection / XSS risk
- Hardcoded secret

**Example:**
```
🔴 CRITICAL: Line 47 has SQL injection risk.

Code: query = $"SELECT * FROM Users WHERE name = '{userName}'";

This allows SQL injection. Fix:
query = "SELECT * FROM Users WHERE name = @name";
using (var cmd = new SqlCommand(query, connection)) {
  cmd.Parameters.AddWithValue("@name", userName);
  // ...
}
```

### 🟠 High (Should fix before merge)
- Performance bottleneck (N+1, memory allocation)
- Missing error handling
- Race condition
- Inconsistent with codebase patterns
- Insufficient test coverage (< 70%)

**Example:**
```
🟠 HIGH: This loads users in a loop (N+1).

Current: for (var id in userIds) { user = await db.Users.FirstAsync(...); }

Better: var users = await db.Users.Where(u => userIds.Contains(u.Id)).ToListAsync();

Impact: Reduces DB calls from 100 to 1 for 100 users.
```

### 🟡 Medium (Consider fixing)
- Code clarity could improve
- Better error message possible
- Missing comment for complex logic
- Slightly inefficient (but not critical)

**Example:**
```
🟡 MEDIUM: This method is doing too much (validation + parsing + caching).

Consider: Split into ValidateInput(), ParseJson(), CacheResult().

Not blocking, but would make testing easier.
```

### 🔵 Low (Nice to have)
- Style suggestion (if linter didn't catch it)
- Naming could be clearer
- Comment could explain more
- Suggestion for future optimization

**Example:**
```
🔵 LOW: Method name "Process()" is vague.

Better: "ValidateAndPersistUser()" is clearer about intent.

Not urgent, but consider for clarity.
```

---

## Comment Format Template

```
[SEVERITY]: [Title]

[Explanation of issue]

[Why it matters]

[Example of current code (3-5 lines)]

[Suggested fix (3-5 lines) OR request for clarification]

[Reference: link to docs/pattern/ticket if relevant]
```

### ✅ GOOD Comment

```
🟠 HIGH: Missing null check on _logger.

Current (line 34):
  public void LogError(string message) {
    _logger.LogError(message); // What if _logger is null?
  }

Issue: If logger not injected, this throws NullReferenceException.

Fix:
  public void LogError(string message) {
    _logger?.LogError(message) ?? Console.WriteLine(message);
  }

Reference: Dependency injection should be verified at startup.
```

### ❌ BAD Comment

```
"This is wrong" 
(No severity, no context, no fix)

OR

"Use dependency injection here"
(Vague, assumes understanding)

OR

"CRITICAL!!!!" 
(Excessive, no actual issue explained)

OR

"You should have used LINQ instead"
(No concrete suggestion or example)
```

---

## Approval Levels

| Level | Meaning | Action |
|-------|---------|--------|
| ✅ **Approve** | Code is ready to merge | Can merge immediately |
| 🟡 **Request Changes** | Issues found, must fix before merge | Author must respond to each comment |
| 🔵 **Comment** | Feedback, not blocking | Author can merge with or without addressing |
| 🚫 **Reject** | Do not merge under any circumstances | Must resolve all issues before re-requesting review |

---

## Approval Criteria

**Can approve when:**
- [ ] Tests passing (CI green)
- [ ] Coverage not decreased
- [ ] No Critical/High issues outstanding
- [ ] Code follows project patterns
- [ ] Description explains what/why
- [ ] Security/performance reviewed

**Cannot approve when:**
- [ ] Tests failing
- [ ] Coverage decreased
- [ ] Critical security issue
- [ ] Code review incomplete
- [ ] Unresolved comments from previous reviewer

---

## Handling Disagreements

**When you disagree with an approach:**

1. **Ask first** (don't assume): "Why did you choose this approach?"
2. **Understand context** (they may have good reasons)
3. **Propose alternative** with trade-offs clearly explained
4. **Escalate if needed** (code review meeting or thread)
5. **Respect the decision** (once made, commit to it)

### ✅ GOOD Disagreement

```
Reviewer: "Why not use async/await here instead of .Result?"

Author: "Good question. I used .Result because this method is synchronous.
         Changing to async would require refactoring 15 call sites."

Reviewer: "Ah, that explains it. Let's add a TODO to refactor to async in next sprint?"

Author: "Done, added ticket #987."
```

### ❌ BAD Disagreement

```
Reviewer: "This is wrong. Use async/await."

Author: "It works fine as is."

Reviewer: "No, it's bad practice."

[Argument with no resolution]
```

---

## What NOT to Comment On

**Don't comment on:**
- Style (use formatters/linters)
- Naming conventions (use linters)
- Comment grammar (if the meaning is clear)
- Whitespace (use formatters)
- Personal preferences (unless it affects readability)

**Only comment on:**
- Logic correctness
- Security/performance
- Test quality
- API design
- Patterns/consistency
- Error handling

---

## Review Speed Expectations

| Task | Target | Reason |
|------|--------|--------|
| Comment on PR | < 24 hours | Unblock authors quickly |
| Major revision needed | 1-2 days max | Don't leave people waiting |
| Final re-review | Same day | Momentum matters |
| Merge (all approved) | < 1 hour | Get changes in quickly |

---

## Self-Review Before Requesting Review

Authors should review their own code first:

- [ ] Read diff line-by-line
- [ ] Check: Does it do what I intend?
- [ ] Run tests locally (all passing?)
- [ ] Check for obvious issues (TODOs, debug code, secrets)
- [ ] Verify description is clear
- [ ] Think: Would I approve this?

If you find issues: Fix them, then request review.

---

## Common Review Issues & Fixes

| Issue | How to Handle |
|-------|---------------|
| **Author disputes comment** | Explain reasoning, offer to discuss, defer if unsure |
| **Multiple reviewers disagree** | Get consensus in comment thread, escalate if needed |
| **Review comment ignored** | Ping author, request response |
| **Conflict resolution needed** | Code review meeting or decision by senior dev |
| **Author blocks on review** | Timebox discussion, make decision, document it |

---

## Code Review Checklist (For Each PR)

- [ ] Understand what the PR does (description clear)
- [ ] Tests: exist, passing, coverage sufficient
- [ ] Security: no vulnerabilities, secrets managed
- [ ] Performance: no N+1, no blocking operations
- [ ] Patterns: consistent with codebase
- [ ] Error handling: all error paths handled
- [ ] Documentation: updated if needed
- [ ] Comments: explain WHY, not WHAT

---

## Positive Feedback Matters

❤️ When you approve: say WHY

```
✅ Approved!

Great work on this PR. I particularly liked:
- The thorough test coverage (92%)
- The clear error messages
- The refactoring to reduce complexity

This is ready to merge.
```

vs.

```
✅ Approved.
```

The first one reinforces what's working well.

---

## Summary

**Good reviewers:**
1. Understand the code before commenting
2. Explain the severity and reasoning
3. Suggest fixes, not just problems
4. Approve quickly when ready
5. Unblock people efficiently

**Good reviews are:**
- **Clear** (anyone can understand the feedback)
- **Actionable** (author knows exactly what to fix)
- **Kind** (assumes good intent)
- **Fast** (doesn't waste time)
- **Thorough** (catches real issues)
