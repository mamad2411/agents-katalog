---
name: remediation-engine
description: Secure code fixer — takes findings from other security skills (code-audit, vulnerability-scanner, etc.) and implements the actual code fixes safely, preserving functionality, for any language or stack. Use whenever the user asks to fix, patch, or remediate previously identified vulnerabilities directly in their codebase, not just describe the fix.
---

# Remediation Engine — Secure Code Fixer

The most important skill in the chain: don't just describe the vulnerability — **actually implement the fix** in the code.

## When to use this
- After another skill (`code-audit`, `vulnerability-scanner`, etc.) has identified vulnerabilities, and the user wants them actually fixed
- Direct request: "fix these vulnerabilities in the code"

## Mandatory Principles
1. **No functional regressions.** The code must behave the same way the user needs it to after the fix — minus the vulnerability.
2. **Minimal footprint.** Change only what's necessary to close the gap; don't perform an unrelated full refactor of the file.
3. **Clear patch.** Always show the code **before** and **after** for every change.
4. **Fix the root cause, not just the symptom.** For example, don't just suppress an error message — address why the information was leaking in the first place.
5. **Re-verify after every fix.** Confirm the change didn't introduce a new issue (a common trap: over-aggressive encoding to fix XSS can break legitimate content rendering — check the balance).

## Workflow
1. Gather the list of vulnerabilities to fix (from a prior scan's output, or directly described by the user).
2. Sort by severity: Critical first.
3. For each vulnerability:
   - Show the current (vulnerable) code clearly
   - Explain in one or two lines why it's unsafe
   - Provide the corrected code, complete and ready to apply
   - If the fix requires installing a new library (e.g., DOMPurify, bcrypt, helmet), state the install command
4. After all fixes, summarize:
   - Number of vulnerabilities fixed
   - Any vulnerabilities that need the user's decision (major architectural change, or a tradeoff between security and UX) and weren't auto-fixed
   - A recommendation to run a full re-scan (`vulnerability-scanner`) to confirm

## Common Fix Patterns

**SQL Injection → Parameterized Query**
```js
// Before (vulnerable)
db.query(`SELECT * FROM users WHERE id = ${userId}`);
// After (safe)
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

**Hardcoded Secret → Environment Variable**
```js
// Before
const apiKey = "sk-abc123...";
// After
const apiKey = process.env.API_KEY;
```

**Weak Hash → bcrypt**
```js
// Before
const hash = crypto.createHash('md5').update(password).digest('hex');
// After
const hash = await bcrypt.hash(password, 12);
```

**Missing Security Headers → helmet**
```js
// Before
app.use(express.json());
// After
const helmet = require('helmet');
app.use(helmet());
app.use(express.json());
```

## Rules
- If a fix touches sensitive business logic that the user's workflow may depend on, ask before applying it instead of assuming.
- Don't touch files or code sections unrelated to the vulnerability being fixed.
