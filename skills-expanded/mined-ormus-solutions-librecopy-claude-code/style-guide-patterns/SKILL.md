---
name: "style-guide-patterns"
description: "Style rule patterns: the 10-rule principle, do and don't pairs, terminology governance, voice and tone documentation, specific inclusive language rules, reading level enforcement, and anti-patterns. Use when writing the rules of a style guide."
---

# Style Guide Patterns

## The 10-Rule Principle

A style guide with 100 rules is a style guide no one reads. A style guide with 10 high-impact rules, automated by Vale, will actually be followed.

Before writing any rule, answer: "Is this in the base guide already (Google, Microsoft)?" If yes, do not duplicate it. Link to it. Write only the rules where you differ or extend.

The 10 most impactful rules for most technical teams:
1. Person (second vs. third)
2. Tense (present vs. future)
3. Voice (active vs. passive)
4. Core terminology (3-5 terms your team consistently gets wrong)
5. Code formatting (inline vs. block, language hints)
6. Heading case (title case vs. sentence case)
7. Inclusive language (team-specific banned terms)
8. Tone by context (at minimum: tutorial vs. reference)
9. Numbers (numeral vs. spelled out)
10. Contractions (always/never/context-dependent)

## The Do/Don't Pair Pattern

Every rule needs a concrete example from your domain. Abstract rules are ignored:

```markdown
# Bad rule: too abstract
Use active voice.

# Good rule: with domain-specific example
Use active voice.

Do: "The SDK throws `AuthenticationError` when the token expires."
Don't: "An `AuthenticationError` is thrown when the token has expired."

Why: Active voice identifies the actor (the SDK), which is what developers
need to know when debugging.

Automated: `.vale/styles/Custom/ActiveVoice.yml` (error level)
```

## Terminology Governance Pattern

A terminology decision needs three things to stick:

1. **The rule** (what to use)
2. **The rationale** (why -- without this, people relitigate it forever)
3. **Automation** (Vale substitution rule -- without this, it will be ignored)

```yaml
# .vale/styles/Custom/Terminology.yml
extends: substitution
message: "Use '%s' instead of '%s'"
level: warning
action:
  name: replace
swap:
  "(?i)login": "sign in"
  "(?i)log in": "sign in"
  "(?i)whitelist": "allowlist"
  "(?i)blacklist": "blocklist"
  "(?i)sanity check": "quick check"
```

The `(?i)` makes the pattern case-insensitive. Test with `vale sync && vale docs/`.

## Voice vs. Tone Documentation Pattern

Most style guides document voice OR tone, not both. Document both explicitly:

```markdown
## Voice (Never Changes)

Our voice is: **clear, direct, technically honest**.

- Clear: We eliminate ambiguity before it reaches the reader.
- Direct: We say what we mean without hedging or softening.
- Technically honest: We acknowledge limitations, tradeoffs, and failures.

## Tone (Varies by Context)

The same voice sounds different depending on context:

| Situation | Tone Adjustment | Example |
|-----------|----------------|---------|
| Tutorial | Encouraging | "You've connected to the database. Let's add your first query." |
| Error message | Empathetic + actionable | "Your API key has expired. Generate a new one in your dashboard." |
| API reference | Neutral, precise | "Returns 404 if the resource does not exist." |
| Breaking change | Direct, solution-focused | "This method is removed in v3. Use `client.connect()` instead." |
| Security advisory | Urgent, no softening | "Update immediately. Versions 2.0–2.3 are vulnerable." |
```

## Inclusive Language Rule Specificity

"Be inclusive" is not enforceable. Specific term substitutions are:

```markdown
## Inclusive Language

These are not suggestions -- they are required replacements with automated enforcement.

| Avoid | Use | Automated |
|-------|-----|-----------|
| blacklist / whitelist | blocklist / allowlist | Yes (Vale substitution) |
| master / slave | primary / replica | Yes (Vale existence) |
| sanity check | quick check, confidence check | Yes (Vale substitution) |
| guys (plural) | everyone, folks, team | Yes (Vale existence) |
| dummy (value) | example, placeholder | Yes (Vale substitution) |
| he/she (generic) | they | Yes (Vale substitution) |

For words without automated enforcement, add to PR review checklist.
```

## Reading Level Enforcement

Vale's built-in readability rules:

```ini
# .vale.ini addition for reading level
[*.md]
BasedOnStyles = Vale, Google, Custom
Vale.Readability = YES    # Flesch-Kincaid score
```

Or use a custom rule:
```yaml
# .vale/styles/Custom/ReadingLevel.yml
extends: script
message: "Reading level (grade %s) exceeds target (%s) for audience: end-user"
level: warning
script: |
  local grade = flesch_kincaid(doc)
  local target = 8  -- Grade 8 for end-user docs
  return grade > target, grade, target
```

## Anti-Patterns

### The Rules-Without-Examples Guide
```
# Bad: principle without example
Use the active voice in all documentation.

# Good: principle + example pair
Use active voice.
Do: "The function returns the user object."
Don't: "The user object is returned by the function."
Why: Active voice reveals the subject, which matters in technical explanation.
```

### The 100-Rule Guide
A guide with 100 rules signals the author wanted to demonstrate thoroughness rather than change behavior. Rules beyond the top 10 will not be read. Provide a "quick reference" of 10 rules + link to the base guide for comprehensive coverage.

### Unenforced Rules
A rule without automation is a rule that relies entirely on reviewer memory. For every rule, decide:
- Can Vale enforce this? → Write a Vale rule.
- Can a PR template remind reviewers? → Add to PR checklist.
- Relies only on writer training? → Prioritize Vale automation.

### The Style Guide That Never Ships
Waiting for a perfect guide before sharing it means no guide ever ships. Start with 5 rules and a Vale config. Add rules as you encounter real inconsistencies in code review.

## References
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/)
- [Vale prose linter](https://vale.sh/) and [Vale Hub](https://vale.sh/hub/) (pre-built styles)
- [Readability Formulas](https://readabilityformulas.com/)
