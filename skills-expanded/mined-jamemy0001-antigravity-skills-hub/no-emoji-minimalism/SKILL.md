---
name: no-emoji-minimalism
description: "Strictly enforces plain text typography and eliminates decorative emojis across source code, commit messages, technical documentation, and chat responses. Only allows strictly functional status badges (check/cross) and severity/rating levels. Trigger when writing code, drafting docs, formatting responses, or reviewing PRs."
category: "05 - Security & Code Quality"
tags:
  - agent-skill
  - clean-code
  - typography
  - code-quality
  - stage-5
aliases:
  - no-emoji
  - clean-typography
  - anti-slop
  - strict-minimalism
---

# No-Emoji Minimalism: Professional Engineering Typography & Code Hygiene

This skill eliminates decorative "AI slop" emojis across source code, git commits, documentation, and agent responses, restoring clean, publication-grade technical typography.

---

## 1. Core Philosophy: Why Decorative Emojis Are Prohibited

Modern LLMs are trained to be conversational and expressive, often defaulting to sprinkling decorative emojis across headings, bullet points, and code comments. In enterprise engineering and high-reliability systems:

1. **High Visual Noise (Cognitive Fatigue)**: Decorative icons disrupt reading flow and create unneeded visual clutter.
2. **Unprofessional Tone**: Top-tier software projects (Linux Kernel, Go, PostgreSQL, Google Style Guides) enforce clean, sober technical prose.
3. **CLI & Tooling Fragility**: Emoji width mismatches across terminals, monospaced editors, and CLI tools cause misaligned tables and broken git logs.
4. **Accessibility (Screen Readers)**: Screen readers read emojis literally (e.g. "rocket ship", "fire"), slowing down visually impaired engineers.

---

## 2. The 4 Absolute Prohibitions

```
┌────────────────────────────────────────────────────────────────────────┐
│                   THE 4 FORBIDDEN EMOJI ZONES                          │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Source Code     ──► ZERO emojis in code, comments, docstrings       │
│ 2. Git Commits     ──► ZERO emojis in commit messages & PR titles      │
│ 3. Headings        ──► ZERO emojis in H1-H6 markdown headers           │
│ 4. Bullet Points   ──► ZERO emojis replacing list hyphens or bullets   │
└────────────────────────────────────────────────────────────────────────┘
```

<!-- no-emoji-disable -->
### Zone 1: Source Code & Comments
- **NEVER** place emojis in variable names, function signatures, comments, docstrings, or logging strings (unless explicitly writing a test for Unicode emoji handling).
- ❌ **Wrong**:
  ```python
  # 🚀 Initialize database pool
  def connect_db(): ...
  ```
- ✅ **Correct**:
  ```python
  # Initialize database pool
  def connect_db(): ...
  ```

### Zone 2: Git Commits & PR Titles
- **NEVER** use Gitmoji or emoji prefixes in commit messages.
- Use strict, pure **Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
- ❌ **Wrong**: `feat(auth): 🔐 add jwt authentication logic`
- ✅ **Correct**: `feat(auth): add jwt authentication logic`

### Zone 3: Document Headings (H1 to H6)
- Rely on typographical scale, weights, and clean semantic titles. Never prefix headings with icons.
- ❌ **Wrong**: `## 🏗️ Architecture Overview`, `### 📦 Installation`
- ✅ **Correct**: `## Architecture Overview`, `### Installation`

### Zone 4: Bullet Points & List Items
- Use standard markdown list markers (`-`, `*`, or numbers `1.`). Never substitute list bullets with decorative emojis (`⚡`, `💡`, `👉`, `🔥`).
- ❌ **Wrong**:
  ```markdown
  - ⚡ 10x faster execution
  - 📦 Zero dependencies
  ```
- ✅ **Correct**:
  ```markdown
  - 10x faster execution
  - Zero dependencies
  ```
<!-- no-emoji-enable -->

---

## 3. The Strict Functional Whitelist (Only 2 Permitted Exceptions)

Emojis are permitted **only** when they convey non-decorative, machine-equivalent semantic state:

| Category | Permitted Markers | Valid Usage Example |
| :--- | :--- | :--- |
| **1. Verification & Test Status** | `[x]`, `[ ]`, `PASS`, `FAIL`, `[OK]`, or `✅` / `❌` / `⚠️` in matrix tables | `\| Test Suite \| Status \|`<br>`\| Auth Suite \| [PASS] ✅ \|`<br>`\| DB Suite   \| [FAIL] ❌ \|` |
| **2. Severity Triage & Scoring** | `🔴 Critical`, `🟡 Warning`, `🟢 Info`, or score stars `⭐⭐⭐⭐⭐` (or `5/5`) | `🔴 [Critical]: Memory leak in connection pool`<br>`Score: ⭐⭐⭐⭐⭐ (5.0 / 5.0)` |

Any emoji outside these two functional categories is strictly considered forbidden slop and must be removed.

---

## 4. Automated CLI Tooling (`scripts/lint_no_emoji.py`)

This skill includes an automated Python linter and auto-fixer:

```bash
# Check current directory for forbidden emojis
python3 Skills/no-emoji-minimalism/scripts/lint_no_emoji.py --check .

# Automatically strip forbidden emojis while preserving whitelisted status markers
python3 Skills/no-emoji-minimalism/scripts/lint_no_emoji.py --fix .

# Check only git staged files before committing
python3 Skills/no-emoji-minimalism/scripts/lint_no_emoji.py --staged

# Validate git commit message file
python3 Skills/no-emoji-minimalism/scripts/lint_no_emoji.py --commit-msg .git/COMMIT_EDITMSG
```

### Git Hooks Integration
- **Pre-Commit Hook** (`.git/hooks/pre-commit`):
  ```bash
  #!/usr/bin/env bash
  python3 Skills/no-emoji-minimalism/scripts/lint_no_emoji.py --staged || exit 1
  ```
- **Commit-Msg Hook** (`.git/hooks/commit-msg`):
  ```bash
  #!/usr/bin/env bash
  python3 Skills/no-emoji-minimalism/scripts/lint_no_emoji.py --commit-msg "$1" || exit 1
  ```

---

## 5. Summary Checklist Before Finalizing Any Output

- [ ] Does any heading contain an emoji icon? (Remove)
- [ ] Do bullet points use emoji decorations? (Replace with `-`)
- [ ] Does any source code or comment contain an emoji? (Remove)
- [ ] Does the commit message use emoji prefixes? (Use pure Conventional Commits)
- [ ] Are the only remaining emojis strictly within the functional whitelist (status or rating)?

---

## 🔗 Connected Skills

- [[Skills/document-design/SKILL|document-design]] — Production editorial document styling and Edward Tufte typography
- [[Skills/git-workflow/SKILL|git-workflow]] — Pure Conventional Commits and clean git branching
- [[Skills/tdd-workflow/SKILL|tdd-workflow]] — Clean test matrices with functional status indicators
- [[Skills/verification-before-completion/SKILL|verification-before-completion]] — Evidence-based verification without decorative noise
- [[Skills/review-security/SKILL|review-security]] — Code quality and security review hygiene

<!-- v1.1.0 synchronized: 2026-09-29 -->
