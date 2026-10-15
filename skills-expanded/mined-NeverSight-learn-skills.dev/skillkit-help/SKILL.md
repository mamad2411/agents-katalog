---
name: skillkit-help
description: >
  Pre-build orientation for skill creators. Answers "what are skills?",
  "should I make one?", and "is my skill good enough?" before you start building.
  Use for: understand skills, decide skills vs subagents, validate an existing skill.
  When ready to actually build, invoke /skillkit directly instead.
category: core
---

## Routing

Detect which path the user needs and jump directly to it.

| User says | Route |
|-----------|-------|
| "what are skills", "how do skills work", "explain", "understand", "not sure", "should I" | → Path A |
| "validate", "check", "review my skill", "is this good" | → Path B |
| "ready to build", "let's create", "make a skill" | Tell them: "You're ready — invoke `/skillkit` directly to start building." |
| Ambiguous | Ask: "Do you want to (A) understand how skills work, (B) validate an existing skill, or are you ready to build (invoke `/skillkit`)?" |

---

## Path A: Understand How Skills Work

**Goal:** Build a mental model of skills — what they are, when to use them, and whether you actually need one — before starting to build.

**Step 1 — Why skills exist**

Load and read in full: `knowledge/foundation/01-why-skills-exist.md`

Summarize for the user: skills are reusable prompt-time instructions that extend your agent's behavior for specific tasks. They live in `~/.claude/skills/` and are invoked via `/skill-name`.

**Step 2 — Skills vs subagents**

Load and read: `knowledge/foundation/02-skills-vs-subagents-comparison.md`

Explain the difference with a concrete example:
- Skill: "When I type `/review-pr`, load these code review instructions"
- Subagent: "Spin up a separate agent with browser tools to scrape and summarize a URL"

**Step 3 — Decision framework**

Load and read: `knowledge/foundation/03-skills-vs-subagents-decision-tree.md`

Walk the user through the decision tree for their specific use case.

**Step 4 — Platform constraints**

Load and read: `knowledge/foundation/06-platform-constraints.md`

Cover the key rules: frontmatter requirements, size limits, trigger conditions.

**Step 5 — Hand off to the builder**

Tell the user: "You now have enough context to start building. Invoke `/skillkit` — it will guide you through the full creation workflow."

---

## Path B: Validate an Existing Skill

**Goal:** Check an existing skill for quality issues before sharing or publishing.

**Step 1 — Load validation standards**

Load and read in full: `knowledge/application/12-testing-and-validation.md`

**Step 2 — Run the checklist**

Ask the user to share their `SKILL.md` content or path. Then check:

- [ ] Frontmatter: `name`, `description`, `category` all present
- [ ] Description has a clear trigger (when to invoke it)
- [ ] At least one concrete usage example in description or body
- [ ] No hardcoded secrets, API keys, or PII
- [ ] SKILL.md is under 500 lines (if over, recommend splitting)
- [ ] Sections are clearly delimited with `##` headings
- [ ] Invoke in Claude Code: does it fire correctly?

Report findings: pass/fail per item, specific fix for each failure.

