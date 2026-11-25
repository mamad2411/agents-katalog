---
name: writing-skills
description: Use when creating a new skill for the Shipworthy plugin, or when a recurring failure mode needs to be codified into a reusable guide. Covers TDD-for-documentation, CSO (Claude Search Optimization), adversarial testing, and the full skill lifecycle.
invoke_when: Use when creating a new skill for the Shipworthy plugin, or when a recurring failure mode needs to be codified into a reusable guide.
---

# Writing Skills

This is the meta-skill: the skill for writing skills. It treats skill authorship with the same rigor as software engineering — because skills ARE production code. They run on every session, shape every output, and compound in effect over time. A sloppy skill causes more damage than a sloppy function because it corrupts behavior across every future interaction.

## 1. Skills Are Tests for Behavior

Just like code tests verify that software behaves correctly, skills verify that the AI follows correct processes. A test asserts "given input X, the output must be Y." A skill asserts "given situation X, the AI must behave like Y."

This is not a metaphor. Skills are literally executable specifications for AI behavior. They are loaded into context, parsed for rules, and enforced during generation. If a skill is vague, the AI will interpret it loosely — the same way a developer interprets a vague test as "anything goes." If a skill is specific, the AI will follow it precisely — the same way a developer follows a well-written test that leaves no room for misinterpretation.

The consequences of treating skills casually are severe:

- **Untested behavior drifts.** Without a skill, the AI will handle the same situation differently across sessions. One session it adds error handling; the next it does not. One session it writes tests first; the next it writes code first and "plans to add tests later."
- **Rationalizations fill the vacuum.** When there is no explicit rule, the AI will rationalize whatever is most convenient. "The user seems to want speed, so I'll skip the security check." Skills close this gap by making the expected behavior explicit.
- **Compounding errors.** A missed skill in session 1 produces code that session 2 builds on top of. By session 5, the architectural debt is load-bearing and expensive to fix.

Write skills the same way you write tests: identify the failure first, then write the fix. Never write a skill because "it seems like a good idea." Write it because you have evidence of a specific failure that the skill will prevent.

## 2. TDD for Skills

The TDD loop for skills mirrors the TDD loop for code: RED (document the failure), GREEN (write the minimal fix), REFACTOR (close loopholes and harden).

### RED: Document the Failure

Before writing a single line of skill content, document what goes wrong WITHOUT this skill. Be specific. Use concrete examples.

**What to capture:**
- What mistake does the AI make?
- What does the user have to correct repeatedly?
- What quality issue keeps appearing?
- In which sessions or task types does this failure occur?

**Failure Evidence Template:**

```markdown
## Failure Evidence

**Observed behavior:** [What the AI actually did]
**Expected behavior:** [What it should have done]
**Frequency:** [How often — every session? Only on large tasks? Only for Builder-tier?]
**Impact:** [What goes wrong downstream — broken code? Wasted time? Security hole?]
**Root cause:** [Why does the AI do this? Missing context? Competing priorities? Ambiguity?]

### Example 1
- User asked: "Add authentication to the API"
- AI did: Added JWT middleware but skipped token refresh, rate limiting, and logout
- Should have: Followed the security-first-development skill's auth checklist

### Example 2
- User asked: "Fix the login bug"
- AI did: Changed the code without writing a regression test first
- Should have: Followed TDD — write failing test, then fix
```

The RED phase is complete when you can show someone the failure evidence and they immediately understand why a skill is needed. If you cannot produce concrete examples, you do not have enough evidence to write a skill yet. Go collect more data.

### GREEN: Write the Minimal Skill

Write just enough guidance to prevent the documented failures. Nothing more. Every additional rule is a maintenance burden and a potential source of confusion.

**Minimum Viable Skill Checklist:**

- [ ] Frontmatter has `name`, `description` (starts with "Use when..."), and `invoke_when` (starts with "Use when...")
- [ ] Description is purely about triggering conditions — no workflow summary
- [ ] Rules directly address the documented failures (each rule maps to at least one failure)
- [ ] Rules are specific and testable — you could verify compliance by reading the AI's output
- [ ] No rules for things the AI already does correctly (do not over-specify)
- [ ] Verification steps describe how to confirm the skill was followed
- [ ] The skill fits in under 500 lines (if longer, it probably covers too many concerns)

The GREEN phase is complete when the skill, if followed, would have prevented every failure documented in the RED phase. Test this by mentally replaying each failure scenario with the skill loaded.

### REFACTOR: Close Loopholes

Review the skill for weaknesses that an AI might exploit (not maliciously, but through optimization pressure — the AI wants to be helpful and fast, which sometimes conflicts with being thorough).

**Refactoring checklist:**
- Rationalizations that could bypass the skill — add them to a rationalization table with counters
- Edge cases where the guidance is ambiguous — make them explicit
- Overly broad rules that would cause false positives — narrow them
- Missing decision points — add decision trees or numbered steps for complex processes
- Verify the skill does not conflict with other skills — check `shipworthy:using-shipworthy` for priority rules

## 3. CSO: Claude Search Optimization

CSO is the practice of writing skill metadata so that AI agents reliably find and trigger the right skill at the right time. This is the skill equivalent of SEO — except instead of optimizing for search engines, you are optimizing for AI context matching.

The AI sees skill frontmatter (name, description, invoke_when) during routing. It uses these fields to decide which skills to load for the current task. If the frontmatter is poorly written, the skill will not be loaded when it should be (false negative) or will be loaded when it should not be (false positive). Both are costly.

### Rules for CSO

**The `description` field must start with "Use when..."** This forces the author to think about triggering conditions, not workflow summaries. The description is a trigger, not an abstract.

- Good: `Use when writing auth logic, API endpoints, database queries, or user input handling.`
- Bad: `Security practices for web development including input validation and OWASP compliance.`

**Never summarize the workflow in the description.** That is what the body of the skill is for. The description's only job is to help the AI decide "should I load this skill for the current task?"

**The `invoke_when` field must match the description.** It is the extended trigger — same purpose, slightly more detail allowed. Both fields should answer the same question: "Under what circumstances should this skill activate?"

**Use concrete verbs in present participle form.** Writing, creating, debugging, reviewing, deploying, migrating, refactoring. These are action-oriented and match how users describe tasks.

- Good: `Use when writing database migrations, altering schemas, or renaming columns.`
- Bad: `Use when working on database stuff.`

**Include common synonyms.** The AI may encounter different terminology for the same concept. Include both forms:
- "auth" AND "authentication"
- "DB" AND "database"
- "deps" AND "dependencies"
- "CI" AND "continuous integration"
- "k8s" AND "Kubernetes"

**Respect the character budget.** The total frontmatter (name + description + invoke_when) should stay under 1024 characters. This keeps context overhead low when the AI is scanning many skills.

**The self-test.** After writing the frontmatter, ask yourself: "If an AI read ONLY the description, would it know when to invoke this skill?" If the answer is no, rewrite it. The description must be self-sufficient as a trigger.

**Avoid negations in triggers.** Do not write "Use when NOT doing X." The AI is better at matching positive conditions than negative ones. Instead, write the positive trigger for the skill that SHOULD handle X.

## 4. Skill File Structure

### Directory Conventions

```
skills/[category]/[skill-name]/
├── SKILL.md           # The skill itself (required)
└── [supporting].md    # Heavy reference material (optional)
```

**Categories** group skills by domain: `core`, `meta`, `quality`, `security`, `architecture`, `operations`, `planning`, `collaboration`, `frontend`, `debugging`, `documentation`. Use an existing category when possible. Creating a new category requires justification — it should contain at least 3 skills.

**Skill names** use kebab-case and should be descriptive enough to identify the skill without reading it: `test-driven-development`, `security-first-development`, `zero-downtime-migrations`. Avoid generic names like `best-practices` or `guidelines`.

### Supporting Files

Add supporting files only when the SKILL.md would exceed 500 lines due to reference material (large tables, extensive examples, checklists). The SKILL.md should be self-contained for the common case; supporting files handle the long tail.

**Naming conventions for supporting files:**
- `examples.md` — before/after examples, templates
- `reference.md` — tables, lookup data, standards references
- `checklist.md` — detailed checklists too long for the main skill

### Cross-Referencing

Use `shipworthy:skill-name` syntax to reference other skills. Example: "For security considerations, see `shipworthy:security-first-development`."

Never use `@import` or similar inclusion mechanisms. Each skill must be independently loadable. Importing creates dependency chains that bloat context and create fragile coupling.

### Frontmatter Format

All three fields are required:

```yaml
---
name: skill-name
description: Use when [triggering conditions]. [Brief expansion of when this activates.]
invoke_when: Use when [triggering conditions with slightly more detail than description].
---
```

The `name` must match the directory name. The `description` and `invoke_when` must both start with "Use when" per CSO rules.

## 5. Rules for Good Skills

### Description Says WHEN, Not HOW

The description field exists for routing. It tells the AI "activate this skill when you encounter these conditions." It does NOT summarize the skill's workflow. If the description says "Covers input validation, OWASP compliance, and secrets management," the AI has to guess whether the current task matches. If it says "Use when writing auth logic, API endpoints, or user input handling," the match is obvious.

### Rules Are Specific and Testable

Every rule must be verifiable by examining the AI's output. "Write good code" is not a rule because no one can agree on what it means. "Every exported function must have a JSDoc comment with @param and @returns" is a rule because you can check it mechanically.

- Before: `Handle errors properly`
- After: `Wrap all async operations in try/catch. Log the error with structured context (operation name, input parameters, timestamp). Return a typed error response — never throw raw strings or expose stack traces to the client.`

### Address Rationalizations Explicitly

The AI will look for reasons to skip or partially follow a skill, especially under time pressure or when the user seems to want speed. Anticipate these rationalizations and counter them directly in the skill.

- Before: `Always write tests`
- After: `Always write tests. "The change is too small for tests" is not valid — small changes break production too. "I'll add tests later" is not valid — later never comes. The ONLY valid skip is when architecture.md explicitly marks a module as prototype-only.`

### One Skill, One Concern

A skill should address exactly one behavioral domain. If you find yourself writing a skill that covers both "error handling" and "logging," split it into two skills. Cross-reference them with `shipworthy:skill-name`.

Why? Because a combined skill will be loaded in situations where only half of it applies, wasting context. And when it needs updating, you risk breaking the half that was working fine.

### Skills Are Prescriptive

Tell the AI what to DO, not what to think about. Skills are not essays or philosophical musings. They are instructions.

- Before: `Consider whether the API response might break existing consumers.`
- After: `Before modifying any API response shape: 1) List all current consumers. 2) Check if the change is additive-only. 3) If removing or renaming a field, add a deprecation header and keep the old field for 2 versions.`

### Include Before/After Examples

For every non-obvious rule, show what the AI output looks like WITHOUT the rule (before) and WITH the rule (after). Concrete examples eliminate ambiguity more effectively than any amount of abstract description.

### Anti-Patterns in Rules

Watch for these patterns that indicate a rule needs rewriting:
- **"Should" or "consider"** — these are suggestions, not rules. Replace with "must" or imperative verbs.
- **"When appropriate"** — appropriate according to whom? Specify the conditions.
- **"Best practices"** — which practices? List them explicitly.
- **"Properly"** — define what proper means in measurable terms.

### Process Flow for Complex Skills

If a skill involves more than 3 steps, describe the process as either numbered steps or a decision tree. Do not rely on prose paragraphs to convey sequence — the AI will lose track of ordering.

```
1. Check if architecture.md defines constraints for this module
2. IF constraints exist → validate the proposed change against each constraint
3. IF no constraints → proceed but flag for architecture review
4. Write the implementation
5. Run verification against the constraints from step 2
```

## 6. Adversarial Testing

Before submitting a skill, pressure-test it by trying to break it. The AI is not adversarial, but it IS an optimizer — it will find the path of least resistance. Your job is to make sure the path of least resistance IS the correct behavior.

### Evasion Testing

**Try to make the AI skip the skill entirely.** Frame a task in a way that might not trigger the skill's `invoke_when`. If you succeed, the trigger conditions are too narrow — widen them.

Example: If your skill triggers on "writing database migrations," try asking "can you rename this column?" The AI might not recognize that as a migration task. Add "altering schemas, renaming or removing columns" to the trigger.

### Partial Compliance Testing

**Try to make the AI follow only part of the skill.** Give it a task where following the full skill feels like overkill. If the AI skips steps, either the steps genuinely are overkill for that case (add a size-based exception) or the skill needs stronger language about mandatory steps.

### Edge Case Testing

**Test the boundaries:**
- Tiny tasks: Does the skill add disproportionate overhead to a one-line change?
- Huge tasks: Does the skill scale, or does it become unmanageable for 50-file refactors?
- Ambiguous tasks: When the triggering condition is unclear, does the skill have a default behavior?

### Rationalization Table

Build a table of every excuse the AI might use to skip or partially follow the skill, paired with a counter-argument. Include this table in the skill itself.

```markdown
| Rationalization | Counter |
|---|---|
| "This is a quick fix, no need for the full process" | Quick fixes cause the majority of production incidents. Follow the process. |
| "The user seems to be in a hurry" | Shipping broken code wastes more time than following the process. |
| "This case is different because..." | If it truly is different, document why. Otherwise, follow the process. |
```

### Cross-Tier Testing

Test the skill's behavior at each user tier:
- **Builder tier:** Does the skill stay invisible and not overwhelm non-technical users?
- **Maker tier:** Does the skill provide the right level of guidance without being patronizing?
- **Engineer tier:** Does the skill provide enough detail for experienced developers?

### Cross-Size Testing

Test across task sizes:
- **Quick Fix:** Does the skill add appropriate (minimal) overhead?
- **Feature:** Does the skill provide sufficient guidance for multi-file changes?
- **Project:** Does the skill scale to multi-day, multi-session work?

## 7. Skill Anti-Patterns

These are the most common mistakes when writing skills. If you recognize any of these in your draft, fix them before submitting.

### Over-Specification

Writing rules for things the AI already does correctly. Every rule has a maintenance cost and a context cost. If the AI consistently writes type-safe code without being told, do not add a rule saying "write type-safe code." You are spending context budget on zero behavioral change.

**How to detect:** Remove the rule and test. If the AI's behavior does not change, the rule is over-specifying.

### Under-Specification

Writing vague rules that can be interpreted multiple ways. "Handle errors gracefully" means different things to different models, different sessions, and different task types. The AI will pick whatever interpretation is most convenient.

**How to detect:** Show the rule to someone unfamiliar with the project. If they ask "what does that mean exactly?" the rule is under-specified.

### Process Theater

Adding ceremony without substance. Steps that exist to look thorough but do not change outcomes. "Step 1: Consider the implications. Step 2: Think about edge cases. Step 3: Proceed." These steps are unverifiable and therefore unenforceable.

**How to detect:** For each step, ask "how would I verify this was done?" If the answer is "I can't," the step is theater.

### Context Bloat

Skills that load too much information into every session. A 2000-line skill with extensive reference tables will consume context budget even when only 10% of it is relevant. Move reference material to supporting files and keep the SKILL.md focused on rules and decision logic.

**How to detect:** If the skill is over 500 lines, it is probably bloated. If more than half the content is reference material, move it to a supporting file.

### Dependency Chains

Skills that require 5 other skills to function. "See `shipworthy:X` for step 1, `shipworthy:Y` for step 2, `shipworthy:Z` for the verification." This means the skill cannot be understood or followed in isolation.

**How to detect:** Can someone follow this skill without reading any other skill? If not, inline the critical parts and cross-reference the rest.

### Kitchen Sink

One skill trying to cover multiple unrelated concerns. "This skill covers error handling, logging, monitoring, and alerting." These are four separate behavioral domains that change independently and trigger in different situations.

**How to detect:** Does the skill have sections that are irrelevant to some of its trigger conditions? If "creating API endpoints" triggers the skill but the logging section only applies to background jobs, the skill covers too many concerns.

## 8. Skill Lifecycle

Skills are living documents. They are born, they evolve, and sometimes they need to be retired.

### Draft

A new skill starts as a draft. It has failure evidence (RED phase), minimal rules (GREEN phase), and has been adversarially tested (REFACTOR phase). Drafts go through review before merge.

### Review

Another person (or a fresh AI session) reviews the skill for:
- CSO compliance — will the AI find this skill when it should?
- Rule quality — are rules specific, testable, and prescriptive?
- Anti-patterns — does the skill avoid the seven anti-patterns listed above?
- Conflict check — does this skill contradict or duplicate any existing skill?

### Merge

The skill is added to the skills directory and becomes active in all sessions. Monitor its first week of use for false positives (skill activates when it should not) and false negatives (skill does not activate when it should).

### Monitor

Track the skill's effectiveness through the retrospective loop (`shipworthy:retrospective`). Signals that a skill needs attention:
- Users frequently correct AI behavior in the skill's domain — the skill is not working
- The AI loads the skill but ignores specific rules — those rules need strengthening
- The skill triggers on irrelevant tasks — the invoke_when is too broad
- The skill never triggers — the invoke_when is too narrow or the domain is rare

### Iterate

Update the skill based on monitoring data. Add new rules for newly discovered failure modes. Remove rules that are no longer needed (the AI's base behavior improved, or the project evolved). Tighten or loosen triggers based on false positive/negative rates.

### Deprecate

A skill should be deprecated when:
- The failure mode it addresses no longer occurs (base model improved)
- The domain it covers is now handled by a better, more comprehensive skill
- The project has moved away from the technology the skill addresses

Deprecation process:
1. Add `deprecated: true` to the frontmatter
2. Add a note at the top explaining why and what replaces it
3. Keep the file for one release cycle (so existing references do not break)
4. Remove the file in the next release

## 9. Rationalization Pressure Test

This section applies the adversarial testing framework to the writing-skills skill itself. Every skill should include a rationalization table. Here is ours.

| Rationalization | Counter |
|---|---|
| "This failure mode is too rare to codify" | Rare failures in production cause the most damage precisely because nobody prepared for them. If it happened once, it will happen again. |
| "The existing skills already cover this" | Check. Actually read the existing skills. If they cover the failure mode, extend them with the new case. If they do not — and they usually do not cover it as specifically as you think — create a new skill. |
| "This skill would be too specific" | Specific skills are more effective than vague ones. A skill that says "when writing database migrations, always use expand-contract" prevents more failures than "handle schema changes carefully." Specificity is a feature, not a bug. |
| "I can just add this to an existing skill" | One skill, one concern. Adding unrelated guidance to an existing skill bloats it, makes it harder to maintain, and causes it to trigger in irrelevant contexts. If the new guidance addresses a different failure mode, it deserves its own skill. |
| "Nobody will read a 3000-word meta-skill" | The AI will. And the AI is the primary consumer. Human authors will read the sections relevant to their current task. The length is justified by the breadth of the topic. |
| "I already know how to write skills" | Then this skill will be fast to follow. Expertise does not exempt you from process — it makes the process faster. Skip the reading, not the steps. |
