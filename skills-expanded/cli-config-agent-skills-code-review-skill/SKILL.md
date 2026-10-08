---
name: code-review
description: Run a structured, holistic code review that combines static analysis with actionable human-readable feedback. Use this skill whenever the user asks to "review my code", "give me feedback on this PR", "do a code review", "check this diff", "look at my changes", or "review before merging". Also trigger when the user pastes code and asks "what do you think?" or "is this good?". This skill produces a prioritized, categorized review comment list — NOT just an analysis plan — so it is the right choice when the user wants immediate reviewer-style feedback rather than an execution plan. It bridges analyze-code (which produces implementation_plan.md) and refactor-code (which applies changes), sitting between them as the human-readable review layer.
---
 
# Code Review Skill
 
A structured code review workflow that mimics a senior engineer's pull-request review: it reads the code, identifies issues across multiple dimensions, and delivers clear, prioritized, actionable feedback — with optional one-click refactoring handoff.
 
**Do NOT use** for:
- Purely generating an execution plan → use `analyze-code` + `refactor-code`
- Broad architecture brainstorming → use `brainstorming-coding`
- Applying fixes directly without review → use `refactor-code`
 
---
 
## Review Workflow
 
```
1. SCOPE — Determine what to review
        ↓
2. READ — Load all relevant files / diffs
        ↓
3. ANALYZE — Inspect across all review dimensions
        ↓
4. WRITE — Produce structured review output
        ↓
5. OFFER — Ask if user wants to apply fixes (→ refactor-code)
```
 
---
 
### Step 1 — Determine Scope
 
**If the user provides files or paths:**
- Read each file in full.
 
**If the user asks to review git changes:**
```bash
git status
git diff HEAD          # unstaged + staged vs last commit
git diff --cached      # staged only
git log --oneline -5   # recent commits for context
```
Focus the review on changed lines, but read surrounding context to judge correctness.
 
**If the user pastes code inline:**
- Review it as-is. Ask for the filename / language if ambiguous.
 
**Scope bounding — large codebases:**
- If the user points at an entire repo or many files, do NOT try to read everything. Focus on entry points and changed/relevant files. If scope is still ambiguous, ask: "Which files or modules should I focus on?" A shallow review of 20 files is less useful than a deep review of 3.
- Aim to review no more than ~500–800 lines of code in a single pass. If the scope exceeds this, surface the most critical files first and note which areas were skipped.
 
---
 
### Step 2 — Understand Context
 
Before judging, understand:
- What is this code supposed to do?
- What language / framework / style conventions are in use?
- Is this a new feature, a bug fix, a refactor, or a hotfix?
- Are there existing tests?
 
Infer from the code itself if the user hasn't said. Don't ask unless truly ambiguous — reviewers read context, not questionnaires.
 
---
 
### Step 3 — Analyze Across Review Dimensions
 
Inspect the code against ALL of the following dimensions. Not every dimension will surface issues — skip gracefully.
 
The emoji labels (🔴 / 🟠 / 🟡) below indicate each dimension's **typical severity ceiling** — how severe an issue in this area tends to be. They are NOT a fixed mapping. A security finding could be 🟡 (informational) or a readability finding could be 🔴 (unreadable critical path). Always assign severity based on the actual impact of the specific issue, not the dimension it came from.
 
#### Correctness *(typical ceiling: 🔴 Critical)*
- Logic errors, off-by-one errors, wrong conditions
- Incorrect handling of edge cases (empty input, zero, null/None, overflow)
- Race conditions or missing synchronization in concurrent code
- Silent failures (errors swallowed, wrong return value)
 
#### Security *(typical ceiling: 🔴 Critical)*
- Injection vulnerabilities (SQL, shell, template)
- Missing input validation / sanitization
- Hardcoded secrets, tokens, passwords
- Improper authentication / authorization checks
- Unsafe deserialization or eval-like patterns
 
#### Error Handling *(typical ceiling: 🟠 Should Fix)*
- Missing try/catch where exceptions can propagate
- Catch-all handlers that hide real errors
- No logging on error paths
- Functions that return ambiguous sentinel values (None, -1, False)
 
#### Design & Structure *(typical ceiling: 🟠 Should Fix)*
- Single Responsibility violations (functions doing too many things)
- DRY violations — copy-paste duplication
- Deep nesting (> 3 levels is a smell)
- God objects / functions (too large, too many parameters)
- Unnecessary abstraction or premature generalization
- Missing separation of concerns (e.g., business logic in UI layer)
 
#### Readability & Naming *(typical ceiling: 🟡 Consider)*
- Unclear variable / function names (single letters, cryptic abbreviations)
- Functions named differently from what they do
- Magic numbers / magic strings without named constants
- Dead code, commented-out blocks, TODO bombs
 
#### Performance *(typical ceiling: 🟡 Consider)*
- O(n²) or worse algorithms where O(n log n) or O(n) is possible
- Unnecessary re-computation inside loops
- Missing indices on frequent lookups
- Memory leaks or unbounded growth
 
#### Testability & Tests *(typical ceiling: 🟡 Consider)*
- Is the code testable as-written? (pure functions, injected dependencies)
- Are new behaviors covered by tests?
- Are edge cases tested?
- Test quality: are assertions meaningful? Are tests brittle?
 
#### Documentation *(typical ceiling: 🟡 Consider)*
- Missing or stale docstrings / comments
- Comments that explain "what" instead of "why"
- Public API lacking type hints or parameter descriptions
 
---
 
### Step 4 — Write the Review
 
Output the review in this format (do NOT wrap the entire review in a code block — render it as live Markdown):
 
---
**## Code Review — [filename / PR title / "Inline Snippet"]**
 
**### Summary**
[2–4 sentences: overall quality, biggest risks, general impression]
 
---
 
**### 🔴 Critical — Must Fix**
 
**[C1] [Short issue title]** · `[file:line or function name]`
> [1–2 sentence description of the problem and why it matters]
 
    # ❌ Current
    <problematic code snippet>
 
    # ✅ Suggested fix
    <corrected code snippet>
 
[Repeat for each critical issue]
 
---
 
**### 🟠 Should Fix**
 
**[S1] [Short issue title]** · `[location]`
> [Description + suggested fix or direction]
 
[...]
 
---
 
**### 🟡 Consider**
 
**[N1] [Short issue title]** · `[location]`
> [Description — no fix required, just a nudge]
 
[...]
 
---
 
**### 🟢 Looks Good**
- [Specific pattern, choice, or section that was done well — see guidance below]
 
---
 
**### Next Steps**
- [ ] Fix [C1], [C2] before merging
- [ ] [S1] can be addressed in a follow-up PR
- [ ] [N1] worth discussing with the team
 
---
 
**Formatting rules:**
- Use inline code for identifiers, paths, and short snippets.
- Include a code block for every Critical issue — reviewers who see a problem must also see the fix.
- For Should Fix and Consider, a code block is optional (include when the fix isn't obvious).
- "Looks Good" is NOT optional — always acknowledge what works. Aim for 2–4 specific bullet points. Name the exact pattern, function, or section: "Good use of context managers in `load_data()`" not "Code is clean." Reviewers who only list problems are noise.
- Keep the language direct, not bureaucratic. Write as a senior engineer talking to a peer, not a linter dumping errors.
 
---
 
### Step 5 — Offer Refactor Handoff
 
After delivering the review, ask:
 
> "Want me to apply the Critical and Should Fix items? I can use the `refactor-code` workflow to implement them one by one with test verification."
 
If the user says yes:
1. Write the findings to `implementation_plan.md` using the same severity labels as the review output:
   - **Critical** → items from 🔴 Critical — Must Fix
   - **Moderate** → items from 🟠 Should Fix
   - **Minor** → items from 🟡 Consider (include only if user explicitly wants them applied)
2. Invoke the `refactor-code` skill
 
---
 
## Severity Calibration
 
| Label | Meaning | Action |
|---|---|---|
| 🔴 Critical | Bug, security hole, data loss risk | Block merge |
| 🟠 Should Fix | Design flaw or error-handling gap | Fix in this PR or immediately after |
| 🟡 Consider | Readability / performance / style | Worth discussing, not blocking |
| 🟢 Looks Good | Explicitly good work | Call it out — 2–4 specific items |
 
**Default to fewer, higher-quality comments.** A review with 3 Critical and 2 Should Fix is more useful than a wall of 20 minor nitpicks. If you have more than 5 items in any single severity bucket, consolidate or promote/demote based on actual impact.
 
---
 
## Tone & Style
 
- Write as a helpful senior engineer, not a linter.
- Explain the *why* behind every issue: "This creates a SQL injection vulnerability because..." not just "Don't do this."
- When unsure if something is a real issue vs. a style preference, label it Consider, not Critical.
- Never make comments about the developer — only about the code.
- Phrase suggestions as "Consider..." or "This could..." for non-critical items, not imperatives.
 
---
 
## Example Usage
 
**User:** "Can you review this Python file before I push?"
 
**Skill actions:**
1. Read the provided file
2. Infer: Python script, file I/O with error handling, data transformation
3. Find: uncaught `FileNotFoundError` (Critical), magic number `86400` (Consider), good use of context managers (Looks Good)
4. Write review with one Critical, zero Should Fix, one Consider, one Looks Good
5. Offer to apply the fix via `refactor-code`
 
---
 
**User:** "Review my git diff"
 
**Skill actions:**
1. Run `git diff HEAD`, identify changed files
2. Read each changed file for context
3. Review only the diff lines (with surrounding context)
4. Produce a review scoped to "what changed", not the entire codebase
5. Offer refactor handoff if Critical/Should Fix items exist
 