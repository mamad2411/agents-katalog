---
name: github-issue-writer
description: 'Research the codebase, then create well-structured GitHub enhancement issues via gh CLI in Tom''s Cometline-style format. Use when the user asks to create a GitHub issue, write an issue, file an enhancement, says "next issue is about", "add an issue for", or wants help wanted labels on issues. Trigger phrases include "create github issue", "gh issue", "file a ticket", "make an issue".'
---

# GitHub Issue Writer

Researches the relevant code first, drafts a structured enhancement issue in the project's house style, and creates it with `gh issue create`. Optionally labels issues `help wanted` when the user asks.

## Thinking Process

### Step 1: Clarify intent (brief)

**Goal:** Know what to file before reading code.

**Key Questions to Ask:**
- What feature, bug, or design gap is this issue about?
- Which repo? (infer from workspace; default `owner/repo` from `gh repo view` if inside a git repo)
- Enhancement, bug, or question?
- Should the issue get `help wanted` (user will say explicitly)?

**Decision Point:** Proceed when you can state the issue in one sentence: "We need X because Y is missing today."

If the user already gave a clear topic (e.g. "next issue: Teams gateway like Discord"), skip questions and research.

### Step 2: Read the codebase (mandatory)

**Goal:** Ground the issue in real files and behavior, not assumptions.

**Actions:**
1. Search for keywords related to the topic (`grep`, file glob, read key modules).
2. Trace the data path: settings → runtime → API → UI (or whatever layers apply).
3. Note **what exists today** in a short table (file paths + one-line behavior).
4. Identify gaps, hard-coding, and natural extension points.

**Decision Point:** Do not draft the issue until you can cite at least 3 concrete file paths and describe current behavior accurately.

### Step 3: Check existing issues and style

**Goal:** Match house style and avoid duplicates.

**Actions:**
```bash
bash /Users/tomlord/workspace/personal-project/tomtom-skill/skills/github-issue-writer/scripts/list-recent-issues.sh [owner/repo] [limit]
```

Optionally view one reference issue:
```bash
gh issue view <number> --repo <owner/repo>
```

**Thinking Framework:**
- If a similar open issue exists, tell the user and offer to extend it instead of duplicating.
- Titles use conventional commits: `feat(scope): description` for enhancements, `fix(scope):` for bugs.

### Step 4: Draft the issue body

**Goal:** Produce a self-contained issue a contributor can implement without re-discovering context.

Use the section order in [references/issue-template.md](references/issue-template.md). Required sections:

| Section | Purpose |
|---------|---------|
| **Summary** | 2-4 sentences: what and why |
| **Problem** | User pain, wrong behavior, missing capability |
| **Current behavior** | Markdown table: Layer → Today (with file links) |
| **Proposed behavior** | Numbered subsections for design |
| **Implementation sketch** | File-level plan, not vague bullets |
| **Acceptance criteria** | `- [ ]` checkboxes, testable |
| **Out of scope** | Prevents scope creep |
| **Related issues** | `#N` links when relevant |
| **Related code** | Bullet list of paths |

**Style rules:**
- Link files as repo-relative paths: `` [`path/to/file.go`](path/to/file.go) ``
- Use a mermaid diagram only when flow/architecture clarifies a multi-component design.
- Prefer tables for "today vs proposed" comparisons.
- Write complete sentences; no telegraphic bullet chains in prose sections.
- For cross-repo monorepos, prefix paths with module (`cometmind/`, `cometline/`).

### Step 5: Create the issue

**Goal:** File on GitHub without manual copy-paste errors.

**Actions:**
```bash
gh issue create --repo <owner/repo> \
  --label enhancement \
  --title "feat(scope): short imperative description" \
  --body "$(cat <<'EOF'
<paste full markdown body>
EOF
)"
```

- Use `--label bug` for defects; `enhancement` for features.
- Use a heredoc (`<<'EOF'`) so backticks and `$` in the body are literal.
- Run the command yourself; do not tell the user to run it.

For bugs, title prefix `fix(scope):` instead of `feat`.

### Step 6: Optional labels and follow-up

If the user asked for `help wanted`, add it to selected issues:
```bash
gh issue edit <number> --repo <owner/repo> --add-label "help wanted"
```

**Good `help wanted` candidates:** bounded scope, clear acceptance criteria, tests specified, not security-critical core rewrites.

**Poor candidates:** large platform rewrites, auth/security sandboxes, unresearched designs.

Tell the user the issue URL and a one-paragraph summary of what you filed.

## Label guide

| Label | When |
|-------|------|
| `enhancement` | New feature or improvement (default for this skill) |
| `bug` | Incorrect behavior with repro |
| `help wanted` | User requested; issue is contributor-friendly |
| `good first issue` | Very small, UI-only or docs-only (ask user first) |

## Title format

```
feat(component): verb phrase in lowercase imperative
fix(component): ...
```

- **component** — module or area (`cometmind`, `cometline`, `comet-sdk`, or feature name)
- Keep under ~72 characters
- No trailing period

Examples from this workflow:
- `feat(cometmind): resolve context window per model instead of global 128k/256k setting`
- `feat(cometline): expose default SOUL.md and support custom personas with image + personal SOUL.md`
- `feat(cometmind): Microsoft Teams gateway with parity to Discord gateway`

## Scripts

```bash
# List recent issues for style reference
bash /Users/tomlord/workspace/personal-project/tomtom-skill/skills/github-issue-writer/scripts/list-recent-issues.sh [owner/repo] [limit]

# Show full body of a reference issue
bash /Users/tomlord/workspace/personal-project/tomtom-skill/skills/github-issue-writer/scripts/view-issue.sh <number> [owner/repo]
```

## Anti-patterns

- Filing an issue without reading source first
- Vague acceptance criteria ("works well", "is fast")
- Missing **Out of scope** (invites endless expansion)
- Duplicating an open issue instead of linking it
- Pasting code dumps without explaining current vs proposed behavior
- Asking the user to run `gh` when the agent can run it

## Present Results to User

After creating the issue, reply with:
1. Markdown link to the issue
2. One sentence on what problem it captures
3. Whether you added `help wanted` and why (if applicable)
4. Optional: offer cross-links to related issues