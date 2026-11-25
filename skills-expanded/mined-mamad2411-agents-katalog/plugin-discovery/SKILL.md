---
name: plugin-discovery
description: "Search GitHub (and optionally npm) for external Claude Code components suitable for dotclaude vendoring. ONLY for discovering components to add to dotclaude's claudekit/ directory — do NOT invoke for general GitHub searches, npm lookups, dependency audits, or non-dotclaude research. Invoke only when called from /preset-wizard or when the user explicitly asks to find external Claude Code plugins/skills for dotclaude."
---

# plugin-discovery

Find external Claude Code components (agents, skills, commands, hooks) that can be
vendored into `claudekit/` to fill gaps in a preset. Follow phases in order.

**Rules:**
- Only recommend repos with substantial star counts (≥ 50 minimum; prefer ≥ 500).
- Always warn clearly when no high-quality results are found — never fabricate suggestions.
- Never add a submodule without explicit user approval.
- Requires dotclaude present locally (handled by `/dotclaude-setup` before this skill is called).

---

## Input Context

This skill is called with context from `/preset-wizard` or manually. Collect:

- **Gap**: what requirement claudekit couldn't cover (e.g., "no Python testing skill", "no k8s deployment agent")
- **User stack**: languages, frameworks, tools from the preset elicitation
- **User role**: who the preset is for

If called manually without context, ask the user for the gap and stack before searching.

---

## Phase 1 — Search

### Step 1a — GitHub search (automatic)

Use `mgrep --web` to search GitHub. Run multiple targeted queries to maximise recall:

```
mgrep --web "claude code <stack-keyword> skill site:github.com"
mgrep --web "claude-code <use-case-keyword> agent site:github.com"
mgrep --web "everything-claude-code <stack-keyword> site:github.com"
mgrep --web "claude code plugin <gap-keyword> site:github.com"
```

Also search by GitHub topic tags:
```
mgrep --web "topic:claude-code site:github.com"
mgrep --web "topic:claude-code-plugin site:github.com"
```

Collect repo candidates: URL, name, description, star count (if visible), last updated.

### Step 1b — npm search (user opt-in only)

After presenting GitHub results, ask:
> "Would you also like me to search npm for Claude Code packages? (This may surface less-vetted packages.)"

If yes, search:
```
mgrep --web "npm claude-code-plugin site:npmjs.com"
mgrep --web "npm @claudekit site:npmjs.com"
```

---

## Phase 2 — Evaluate

For each candidate repo, assess:

| Criterion | Threshold | Weight |
|---|---|---|
| Star count | ≥ 50 required; ≥ 500 preferred | High |
| Last commit | Within 12 months | High |
| License | MIT or Apache-2.0 | Required |
| Has Claude Code component structure | `agents/`, `skills/`, `commands/`, `hooks/`, or `rules/` folders | Required |
| Matches user's stack / use case | Relevant keywords in README or component names | Medium |

**Claudekit overlap check — run for each candidate:**

Before scoring, check if a similar component already exists in `claudekit/`.
The layout is source-grouped, so scan across every source folder:

```bash
# `*` expands to claudekit/everything-claude-code, claudekit/anthropic-skills, claudekit/dotclaude/<sub>, claudekit/private
ls -d claudekit/*/skills/* claudekit/*/agents/*.md claudekit/*/commands/*.md claudekit/*/hooks/*.* 2>/dev/null | grep -i "<keyword>"
```

If a similar component is found:
1. Read its sidecar (`SOURCE.yaml` for folder components, `<name>.source.yaml` for file components)
2. Check `categories.coverage` and sidecar `notes` — does the existing component already cover the gap? Or is it language-specific (and the candidate is a cross-language upgrade)?
3. Surface in Phase 3 proposal:
   - If existing covers the gap: `"Note: similar component already vendored at claudekit/<source>/<type>/<name>. Sidecar says: <coverage + notes summary>. Consider this before adding a new upstream source."`
   - If existing is js-only and candidate is cross-language: `"Note: claudekit already has <name> (js-only) under <source>. This candidate would be a cross-language upgrade — worth vendoring alongside or as a replacement."`

**Disqualify** any repo that:
- Has < 50 stars
- Has no commit in the last 12 months
- Has no compatible license
- Has no recognisable Claude Code component structure

**Quality warning — trigger when:**
- Zero qualifying candidates are found after all searches
- The only qualifying candidates are generic (no stack match)

Warning text to display:
> ⚠ No well-maintained external alternatives were found for "[gap]". Options:
> - Build a custom component (use `/preset-wizard` to scaffold it)
> - Proceed without coverage for this requirement
> - Try a broader search manually on github.com/topics/claude-code

---

## Phase 3 — Propose

Present qualifying candidates ranked by stars (descending):

```
## External Plugin Candidates for: <gap>

| Rank | Repo | Stars | Last Updated | Relevant components |
|------|------|-------|--------------|---------------------|
| 1 | github.com/... | ⭐ 1.2k | 2026-03 | skills/typescript-tdd, agents/code-reviewer |
| 2 | github.com/... | ⭐ 340  | 2025-11 | commands/test-runner |
```

For each candidate, note:
- Which specific components match the gap
- Any concerns (older activity, broad scope, dependency count)

Ask the user:
> "Which repo(s) would you like to add as an upstream source? Reply with rank numbers, or 'none'."

If the user selects none, or all candidates were disqualified, end here and report the gap as unresolved.

---

## Phase 4 — Vendor

For each repo the user selects, execute the following. **Confirm each step with the user before running.**

### Step 4a — Confirm the alias

Propose an alias for `upstream/<alias>/` and `dependencies.yaml`:
- Derive from the repo name (kebab-case, short)
- Example: `github.com/foo/claude-skills` → alias `foo-claude-skills`

Ask: **"Use alias `<alias>`? Or specify a different name."**

### Step 4b — Add as git submodule

```bash
git submodule add <repo-url> upstream/<alias>
git -C upstream/<alias> rev-parse HEAD
```

Record the HEAD commit SHA for Step 4c.

### Step 4c — Update dependencies.yaml

Add a new entry under `sources:`:

```yaml
  <alias>:
    name: <alias>
    description: <one-line description from README>
    repo: <repo-url>
    local_path: upstream/<alias>
    pinned_commit: <HEAD-SHA from Step 4b>
    ref: main
    role: sync_source
    license: <MIT|Apache-2.0>
```

### Step 4d — Vendor specific components via dotclaude-component-picker

Invoke the `dotclaude-component-picker` skill to pick the specific components needed.
Pass the alias as the upstream source and the component names identified in Phase 3.

The component-picker handles the full 8-step pipeline:
browse → evaluate → cross-reference scan → vendor → sidecar → preset → install → verify.

---

## Phase 5 — Report

After vendoring is complete:

- List all newly available components in `claudekit/` (type + name)
- Confirm they are ready to reference in a preset
- If any components were skipped or failed during component-picker, note them
- Return to `/preset-wizard` context if this was called from there:
  > "Discovery complete. The following components are now available for your preset: [list]"

If the gap remains unresolved (no suitable external source found, or user declined all candidates):
> "No external components were added. The gap '[gap]' will need a custom component or can be left uncovered in this preset."
