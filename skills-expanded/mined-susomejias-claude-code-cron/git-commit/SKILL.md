---
name: git-commit
description: Use this skill when creating git commits with emoji conventional commit messages, staged-file awareness, and commit-splitting guidance for mixed changes.
---

# Git Commit Skill

Create clean, atomic commits using emoji conventional commit format, while preserving staging intent and warning about split opportunities.

## When to Use This Skill

- Creating a commit from current repo changes
- Preparing changes for PR with clean history
- Enforcing commit message consistency
- Deciding whether to split mixed changes before commit

## Workflow

### Step 1: Inspect Repository State

1. Check status and staged set first: `git status --short`
2. If staged files exist, treat staged files as commit scope
3. If no files are staged, inspect full working diff and stage only after agreeing on scope
4. Never auto-include unrelated unstaged files when staged files already exist

### Step 2: Analyze Commit Scope and Split Risk

1. Review effective diff:
   - Staged scope: `git diff --cached`
   - Unstaged scope: `git diff`
2. Detect split signals:
   - Different concerns in one diff (feature + fix + refactor)
   - Mixed commit types (`feat` with `docs`, etc.)
   - Unrelated file patterns (UI + DB + infra in one shot)
   - Large noisy changes that hide intent
3. If split is needed, suggest explicit smaller commit groups before committing

### Step 3: Build Commit Message

Use format:

`<emoji> <type>: <description>`

Rules:

- Use imperative mood (`add`, `fix`, `refactor`)
- Keep first line under 72 characters
- Keep one clear purpose per commit
- Do not add trailing signatures or Claude attribution

Core types:

- `✨ feat`: New feature
- `🐛 fix`: Bug fix
- `📝 docs`: Documentation
- `💄 style`: Formatting/style-only
- `♻️ refactor`: Internal restructuring
- `⚡ perf`: Performance improvement
- `✅ test`: Tests
- `🔧 chore`: Tooling/maintenance

For extended mapping, read `references/emoji-map.md`.

### Step 4: Execute Commit

1. Default commit:
   - `git commit -m "<emoji> <type>: <description>"`
2. If user requests hook skip:
   - `git commit --no-verify -m "<emoji> <type>: <description>"`
3. If user requests amend:
   - `git commit --amend`
   - Or `git commit --amend -m "<emoji> <type>: <description>"`
4. Keep Husky enabled by default unless user explicitly requests `--no-verify`

### Step 5: Confirm Result

1. Show resulting commit summary: `git log -1 --oneline`
2. Confirm committed file scope matches intended scope
3. If changes remain, propose follow-up split commits

## Guardrails

- Never add "Generated with Claude" or similar signatures to commit messages
- Prefer splitting unrelated work rather than forcing one large commit
- Respect staged intent as source of truth when staged files exist
