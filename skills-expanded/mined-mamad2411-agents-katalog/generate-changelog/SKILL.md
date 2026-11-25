---
name: generate-changelog
description: Generate a well-formatted changelog from git history, tailored to a specific audience. Trigger when the user asks to generate a changelog, release notes, or says things like "what changed since last release", "write release notes", "summarize recent commits", "/generate-changelog", "create a changelog entry", or "what's new in this version". Also trigger when the user mentions shipping a release and needs to communicate changes.
---

# Generate Changelog

Read git history and produce a polished, audience-appropriate changelog. Goes beyond listing commits — groups changes by impact, writes human-readable descriptions, and formats for the target audience.

## Trigger Examples

- "/generate-changelog"
- "Generate release notes for v2.3.0"
- "What changed since last release?"
- "Write a changelog for the last two weeks"
- "Summarize commits since the v1.5 tag"
- "I need release notes for the product team"

## Inputs

- **Range** (optional, default: last tag to HEAD) — one of:
  - A git ref range: `v1.2.0..HEAD`, `abc123..def456`
  - A time range: "last week", "since March 1"
  - A count: "last 50 commits"
  - If no range given, auto-detect from latest git tag to HEAD
- **Audience** (optional, default: `developer`) — one of:
  - `developer` — Technical, includes breaking changes, migration notes, API changes
  - `product` — Feature-focused, business impact, no implementation details
  - `executive` — High-level summary, metrics-oriented, 5 sentences max
  - `user` — End-user facing, "what's new" style, plain language
- **Format** (optional, default: `markdown`) — one of:
  - `markdown` — Standard changelog format
  - `slack` — Formatted for Slack posting (mrkdwn)
  - `github` — GitHub Release body format with collapsible sections
- **Project name** (optional) — used in the header; inferred from git remote or directory name if omitted

---

## Workflow

### Step 1: Read Git History

```bash
# Get commits in the specified range
git log --pretty=format:"%H|%s|%b|%an|%ad" --date=short [range]

# Get the latest tag if no range specified
git describe --tags --abbrev=0

# Get files changed per commit for context
git log --pretty=format:"%H" [range] | while read hash; do
  echo "=== $hash ==="
  git diff-tree --no-commit-id --name-only -r $hash
done
```

### Step 2: Classify Each Commit

Parse each commit and classify it into categories. Use both the commit message and the files changed for context:

| Category | Conventional Commit Prefix | Description |
|----------|---------------------------|-------------|
| ✨ Features | `feat:` | New functionality |
| 🐛 Bug Fixes | `fix:` | Defect corrections |
| 💥 Breaking Changes | `feat!:`, `fix!:`, `BREAKING CHANGE` | Changes requiring migration |
| ⚡ Performance | `perf:` | Speed or efficiency improvements |
| 🔒 Security | `security:`, CVE references | Vulnerability fixes |
| 🏗️ Infrastructure | `chore:`, `ci:`, `build:` | Build, CI, dependency updates |
| 📖 Documentation | `docs:` | Documentation changes |
| 🧪 Testing | `test:` | Test additions or fixes |
| ♻️ Refactoring | `refactor:` | Code changes that don't add features or fix bugs |
| 🎨 Styling | `style:` | Formatting, white-space, etc. |

**If commits don't follow conventional commit format:**
- Infer category from the files changed and commit message content
- A commit touching `src/api/` with message "add user search" → Feature
- A commit touching `tests/` with message "add missing tests" → Testing
- A commit touching `.github/workflows/` → Infrastructure
- Flag ambiguous commits and use best judgment

### Step 3: Rewrite for Audience

Transform raw commit messages into human-readable descriptions based on the audience:

**Developer audience:**
- Keep technical detail
- Note breaking changes with migration instructions
- Include file paths and API signatures where relevant
- Mention PR numbers and authors

**Product audience:**
- Lead with user impact: "Users can now search by email address" not "Add email field to user search query"
- Group by feature area, not commit type
- Skip infrastructure, refactoring, and test changes
- Quantify impact where possible

**Executive audience:**
- 3-5 bullet points maximum
- Focus on business outcomes: "Reduced page load time by 40%" not "Optimize database queries"
- Mention risk items (breaking changes, security fixes)

**User audience:**
- Plain language, no jargon
- Frame as benefits: "Find what you need faster with improved search" not "Implement full-text search with PostgreSQL tsvector"
- Group into "New", "Improved", "Fixed"

### Step 4: Generate Output

#### Markdown Format (developer)

```markdown
# [Project Name] Changelog

## [version] — [date]

### 💥 Breaking Changes
- **[scope]:** [description] — [migration note]

### ✨ Features
- **[scope]:** [description] ([#PR](link)) — @author

### 🐛 Bug Fixes
- **[scope]:** [description] ([#PR](link))

### ⚡ Performance
- [description]

### 🔒 Security
- [description]

### 🏗️ Internal
- [description]

---

**Full diff:** [`v1.2.0...v1.3.0`](link)
**Contributors:** @author1, @author2, @author3
```

#### Slack Format

```
:rocket: *[Project Name] v1.3.0* is out!

*What's New*
• [Feature description]
• [Feature description]

*Fixes*
• [Bug fix description]

*Breaking Changes*
:warning: [Description + migration note]

_Full release notes:_ <link|here>
```

#### GitHub Release Format

```markdown
## What's Changed

### ✨ Features
- [description] by @author in #PR

### 🐛 Bug Fixes
- [description] by @author in #PR

<details>
<summary>🏗️ Internal Changes</summary>

- [description]
- [description]

</details>

**Full Changelog**: https://github.com/org/repo/compare/v1.2.0...v1.3.0
```

### Step 5: Deliver

- Write the changelog to a file in `/mnt/user-data/outputs/`
- Also display a summary in chat
- If audience is `slack`, offer to copy as plain text for pasting
- If `github` format, note that it's ready to paste into a GitHub Release

---

## Notes for Claude

- **Don't just list commits.** The whole point is to transform raw git history into something a human wants to read. Merge related commits, drop noise, rewrite for clarity.
- **Breaking changes are sacred.** Never bury or skip breaking changes regardless of audience. Even the executive summary should flag them.
- **Infer when possible.** If commits don't use conventional format, make your best inference from file paths and message content. Don't refuse to categorize.
- **Be honest about gaps.** If the git history is mostly "fix stuff" and "wip", note that the changelog is best-effort and suggest adopting conventional commits.
- **Stats are nice.** If the range is large, include a stats line: "X commits, Y contributors, Z files changed" — it adds context.
- **Security fixes first.** If there are security fixes, always list them prominently regardless of audience.
