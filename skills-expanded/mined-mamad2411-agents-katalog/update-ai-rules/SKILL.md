---
name: update-ai-rules
description: Analyses an approved PR branch for rule-worthy changes and proposes new or updated AI rules across Cursor, Claude Code, and GitHub Copilot. Use when updating AI rules, checking rules for a branch, or deciding whether to update cursor/claude/copilot rules after a PR.
---

# Update AI Rules from Branch

Run on an approved PR branch **before merging into main** to identify changes worth capturing as new or updated AI rules across all three providers.

## Prerequisites

Read `project-context/SKILL.md` first — especially the architecture overview and intentional patterns. If the PR introduces a new node type, changes the mapper pattern, adds a new layer to the model hierarchy, or modifies the execution flow, those are strong signals for rule-worthy changes. The architecture context gives you the vocabulary to detect these structural shifts.

Also read `architecture.md` in the repo if it exists — it has deeper detail on the two-layer model design, node categories, and engine runtime that helps you distinguish between "new pattern worth documenting" and "existing pattern being followed."

---

## What counts as "rule-worthy"

Not every code change warrants a rule update. Use this checklist to decide:

| Change type | Rule-worthy? | Example |
|---|---|---|
| New architectural pattern introduced | Yes | New service layer abstraction, new file structure convention |
| New tech / library added | Yes | Added Zod for validation, switched from Jest to Vitest |
| New naming convention established | Yes | All event handlers now prefixed with `on`, all types suffixed with `Type` |
| Build/test/lint command changed | Yes | Changed from `npm test` to `pnpm test:unit` |
| New coding standard enforced | Yes | All API handlers must return typed responses |
| Constraint that AI should never violate | Yes | Never import from `../shared` in the `api` package |
| Bug fix that reveals a bad AI habit | Yes | AI kept suggesting `==` instead of `===`; add rule |
| New node type or mapper added | Yes | New node category means new storage model, engine model, and mapper — document the pattern |
| Change to the storage↔engine boundary | Yes | If the mapper contract changes, AI needs to know |
| New environment variable or config key | Maybe | Worth noting if it affects how AI suggests code |
| One-off fix with no broader pattern | No | Fixed a typo, corrected a variable name |
| Feature addition with no new conventions | No | New endpoint that follows existing patterns exactly |
| Formatting change handled by linter | No | Already enforced by ESLint/Prettier config |

---

## Rule locations and formats (reference)

### Cursor — `.cursor/rules/*.mdc`
```yaml
---
description: "When to apply this rule"
globs: "src/**/*.ts"       # optional path scoping
alwaysApply: false          # true = always injected; false = agent-decides
---
Rule content here.
```

### Claude Code — `.claude/rules/*.md`
```markdown
---
paths: ["src/**/*.ts"]   # optional — omit for unconditional rules
---
Rule content here.
```

### Copilot
- Repo-wide (always on): `.github/copilot-instructions.md` — plain Markdown
- Path-scoped: `.github/instructions/NAME.instructions.md` with `applyTo` frontmatter glob

---

## Steps

### Step 1 — Get the full branch diff
```bash
git diff main...HEAD --stat
git diff main...HEAD
git log main..HEAD --oneline
```
Use the triple-dot `main...HEAD` diff to see everything this branch adds compared to where it forked from main — the complete PR scope.

### Step 2 — Read existing rules and architecture context
```bash
find .cursor/rules -name "*.mdc" 2>/dev/null
find .claude/rules -name "*.md" 2>/dev/null
cat .github/copilot-instructions.md 2>/dev/null
find .github/instructions -name "*.instructions.md" 2>/dev/null
```
Read the content of all existing rule files. You need to know what's already documented before proposing additions.

Also read `project-context/SKILL.md` and `architecture.md` (if present) to understand the established patterns. This helps you:
- Recognize when a PR is extending an existing pattern (probably not rule-worthy) vs. establishing a new one (probably rule-worthy)
- Write rules that reference the correct architectural vocabulary (e.g. "storage model", "engine model", "mapper")
- Avoid proposing rules that contradict intentional design decisions

### Step 3 — Identify rule-worthy changes
Go through the diff and apply the checklist from above. For each rule-worthy change, note:
- What the new pattern/convention/constraint is
- Which files it applies to (all files, specific language, specific directory?)
- Whether it's a new rule or an update to an existing one
- Which providers already have a relevant rule (and whether it needs updating)

### Step 4 — Draft proposed rule updates
For each rule-worthy change, produce a proposal in this format:

```
### [Rule title]

**Why this is rule-worthy:** [One sentence explaining the pattern/convention from this PR]

**Scope:** [all files / `src/api/**` / TypeScript files / etc.]

**Proposed rule text:**
[The actual instruction text, written clearly for an AI agent to follow]

**Changes needed:**
- **Cursor** (`.cursor/rules/NAME.mdc`): [New file / Update existing — show full file content or diff]
- **Claude Code** (`.claude/rules/NAME.md`): [New file / Update existing — show full file content or diff]
- **Copilot** (`.github/copilot-instructions.md` or `.github/instructions/NAME.instructions.md`): [Append section / New file / Update — show content]
```

If a change only warrants updating one provider (e.g. updating Copilot review behaviour only), state that clearly and explain why the other providers don't need the update.

### Step 5 — Handle the "nothing to update" case
If no changes on the branch are rule-worthy, say so clearly:
```
No rule updates needed for this branch.

Changes reviewed:
- [brief list of what was looked at and why it wasn't rule-worthy]
```
Do not propose rules just to look thorough. False positives create noise and bloat the rule files.

### Step 6 — Ask for approval
Do NOT write any files. Present all proposals and ask:
```
## Proposed Rule Updates

[Proposals here]

---
Please review the proposals above:
- `approve all` — apply all proposed rule changes across all providers
- `approve [rule title]` — apply a specific rule
- `approve cursor` / `approve claude` / `approve copilot` — apply changes for one provider only
- `skip [rule title]` — skip a specific rule
- Edit any proposed rule text above before approving
```

### Step 7 — Apply approved changes
Write the approved rule files. For new files, use the correct format for each provider (see formats above). For updates to existing files, append or edit surgically — do not overwrite unrelated rules.

After writing all files, print a summary:
```
Rules updated:
- `.cursor/rules/NAME.md` — [created / updated]
- `.claude/rules/NAME.md` — [created / updated]
- `.github/copilot-instructions.md` — [updated: added section "[heading]"]
```

---

## Writing good rules

- **Be specific, not vague**: "Use `pnpm` not `npm`" not "Use the correct package manager"
- **Be negative when needed**: "Never import `lodash` — use native array methods instead"
- **Scope appropriately**: if a rule only applies to test files, use path scoping — don't pollute global rules
- **Keep each rule short**: one clear instruction per rule, not a paragraph
- **Avoid redundancy**: if the linter or TypeScript compiler already enforces it, don't add a rule for it
- **Think like a new team member**: would a capable AI developer get this wrong without being told?

---

## Rules
- Never write rule files without explicit user approval
- Never propose rules that duplicate what linters, type checkers, or existing tooling already enforces
- Aim for precision: a rule that's too broad is worse than no rule
- Always apply changes to all three providers unless there is a clear reason not to
