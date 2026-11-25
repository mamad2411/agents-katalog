---
name: sync-ai-rules
description: Checks whether AI rule sets for Cursor, Claude Code, and GitHub Copilot are in sync, and proposes reconciliation when they are not. Use when syncing rules, checking rules across providers, or fixing out-of-sync AI rules.
---

# Sync AI Rules

Checks and reconciles AI rules across Cursor (`.cursor/rules/*.mdc`), Claude Code (`.claude/rules/*.md`), and GitHub Copilot (`.github/copilot-instructions.md` + `.github/instructions/*.instructions.md`).

---

## Prerequisites

Read `project-context/SKILL.md` if you haven't already — it has the project conventions and architecture context that helps you understand which rules are project-specific vs. general.

## Rule locations and formats

### Cursor — `.cursor/rules/*.mdc`
Each file is a Markdown file with optional YAML frontmatter:
```yaml
---
description: "Human-readable description of when to apply this rule"
globs: "src/**/*.ts"      # optional — restricts to matching files
alwaysApply: true          # if true, always injected; if false, agent decides based on description
---
# Rule content here
```
Modes: `alwaysApply: true` = always, `alwaysApply: false` + description = agent-decided, globs = file-scoped.

### Claude Code — `.claude/rules/*.md`
Plain Markdown files. Optional frontmatter for path-scoping:
```yaml
---
paths: ["src/**/*.ts", "tests/**"]
---
# Rule content here
```
Rules without `paths` apply unconditionally. File names are free-form.

### Copilot — `.github/copilot-instructions.md` + `.github/instructions/*.instructions.md`
- **Repo-wide**: `.github/copilot-instructions.md` — plain Markdown, no frontmatter, always applied.
- **Path-specific**: `.github/instructions/NAME.instructions.md` — frontmatter with `applyTo` glob:
```yaml
---
applyTo: "**/*.ts,**/*.tsx"
---
# Rule content here
```
Both types support an optional `excludeAgent: "code-review"` or `excludeAgent: "coding-agent"` field.

---

## Steps

### Step 1 — Discover all rule files
```bash
# Cursor rules
find .cursor/rules -name "*.mdc" 2>/dev/null | sort

# Claude Code rules
find .claude/rules -name "*.md" 2>/dev/null | sort

# Copilot rules
ls .github/copilot-instructions.md 2>/dev/null
find .github/instructions -name "*.instructions.md" 2>/dev/null | sort
```
Read the content of every file found. Strip YAML frontmatter before comparing content — only compare the actual rule text.

### Step 2 — Group rules by topic/scope
Cluster the rules you find into logical groups based on their content:
- **Always-on / global rules** (no file scoping): e.g. code style, naming conventions, commit format
- **Language/path-scoped rules**: e.g. TypeScript rules, test file rules, backend-only rules
- **Tool-specific rules**: anything that only makes sense for one provider (e.g. Copilot review behaviour via `excludeAgent`)

### Step 3 — Compare across providers
For each rule group, check if an equivalent rule exists in all three providers. Build a comparison table:

```
## 🔍 Rule Sync Status

| Rule / Topic | Cursor | Claude Code | Copilot | Status |
|---|---|---|---|---|
| [topic] | ✅ `.cursor/rules/NAME.mdc` | ✅ `.claude/rules/NAME.md` | ✅ `.github/copilot-instructions.md` | In sync |
| [topic] | ✅ `.cursor/rules/NAME.mdc` | ❌ Missing | ✅ `.github/instructions/NAME.instructions.md` | ⚠️ Out of sync |
| [topic] | ✅ `.cursor/rules/NAME.mdc` | ✅ `.claude/rules/NAME.md` | ✅ present | ⚠️ Content differs |
```

For each "⚠️ Out of sync" or "⚠️ Content differs" row, include:
- A summary of what differs (missing entirely, different wording, contradictory instructions, scope mismatch)
- The specific lines or sections that differ

### Step 4 — Propose reconciliation
For each out-of-sync rule, propose the canonical version and show the exact change needed for each affected provider. Use this format:

```
### ⚠️ [Topic name]

**Issue:** [Brief description — e.g. "Rule exists in Cursor and Copilot but is missing from Claude Code" or "Copilot says X but Cursor says Y"]

**Proposed canonical rule:**
[The clean, agreed-upon version of the rule text]

**Changes needed:**
- **Cursor** (`.cursor/rules/NAME.mdc`): [No change needed / Add / Update with diff]
- **Claude Code** (`.claude/rules/NAME.md`): [No change needed / Add / Update with diff]
- **Copilot** (`.github/copilot-instructions.md` or `.github/instructions/NAME.instructions.md`): [No change needed / Add / Update with diff]
```

### Step 5 — Ask for approval
Do NOT write any files yet. Present the full report and ask:
```
Ready to apply the above changes. Please review and confirm:
- `approve all` — apply all proposed changes across all providers
- `approve [topic]` — apply only the changes for a specific rule topic
- `approve cursor` / `approve claude` / `approve copilot` — apply changes for one provider only
- `skip [topic]` — skip a specific rule
- Edit any proposed rule above before approving
```

### Step 6 — Apply approved changes
For each approved change, read the current file content, apply the edit, and write the file back. When adding a new rule file for a provider, use the correct format for that provider (see formats above). When updating an existing file, make surgical edits — do not rewrite unrelated sections.

---

## Handling format differences
Some rules have no 1:1 equivalent across formats:
- **Cursor `alwaysApply: true`** → Claude Code: add rule without `paths` frontmatter → Copilot: add to `copilot-instructions.md`
- **Cursor glob-scoped rule** → Claude Code: add `paths` frontmatter → Copilot: create a `NAME.instructions.md` with matching `applyTo` glob
- **Copilot `excludeAgent: "code-review"`** → Note in the proposal that this is Copilot-specific and has no equivalent for the other providers; suggest keeping it as-is

---

## Rules
- Never write files without explicit user approval
- When the same instruction is worded differently across providers but means the same thing, flag it as a style difference (not a conflict) and let the user decide whether to harmonize the wording
- If a rule is intentionally provider-specific (e.g. Copilot review behaviour), mark it as intentional and exclude it from sync proposals
- Prefer editing existing files over creating new ones where a suitable file already exists
