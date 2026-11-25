---
name: commit-message-conventions
description: >
  Write clear git commit messages using Conventional Commits (type, optional scope,
  subject/body/footer), emphasizing why the change exists rather than restating the
  diff. Use when drafting or reviewing a commit message, Conventional Commits, 提交信息,
  git commit -m, changelog-friendly subjects, or breaking-change footers.
---

# Commit Message Conventions

## Scope And Authorization

- **In scope:** repositories you contribute to; follow repo-specific commitlint if present.
- **Out of scope:** rewriting published shared history without team agreement; stuffing secrets into messages.
- Pair with `changelog-and-release-notes` for release automation and `code-quality-standards` for the code itself.

## When To Use

- Authoring commits or reviewing message quality in PRs.
- Enabling semantic-release / changelog generation.
- Tokens: Conventional Commits, type(scope), BREAKING CHANGE, 提交信息.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| PR review comments | `code-review-comments-style` |
| Changelog generation detail | `changelog-and-release-notes` |
| CODEOWNERS | `codeowners-review-routing` |
| Code quality of the change | `code-quality-standards` |

## Format

```text
<type>(<optional scope>): <short summary in imperative>

<optional body: why, context, trade-offs>

<optional footer(s):
Fixes #123
BREAKING CHANGE: description
>
```

### Common types

| Type | Use |
| --- | --- |
| `feat` | User-facing feature |
| `fix` | Bug fix |
| `docs` | Docs only |
| `style` | Formatting; no logic |
| `refactor` | Neither fix nor feat behavior |
| `perf` | Performance |
| `test` | Tests only |
| `build` | Build system / deps |
| `ci` | CI config |
| `chore` | Maintenance |
| `revert` | Revert prior commit |

## Subject Line Rules

1. Imperative mood: “add”, “fix”, not “added” / “fixes”.
2. ~50–72 chars when practical; no trailing period.
3. Explain **why** in body if subject cannot.
4. Scope optional: `fix(auth):`, `feat(api):`.

## Workflow

### 1. Check local rules

```bash
# commitlint / husky if present
ls commitlint.config.* .commitlintrc* 2>/dev/null
cat CONTRIBUTING.md 2>/dev/null | head
```

1. Org may ban `WIP` on main; use draft PRs instead.
2. Some repos require ticket IDs in footer or subject.

### 2. Summarize the change for a future reader

1. What problem existed?
2. What approach and why not alternatives (if non-obvious)?
3. Risks / follow-ups?

### 3. Write the message

**Good:**

```text
fix(payments): prevent double charge on vendor 500

Payment provider uses HTTP 500 for soft declines. We retried those
and double-charged (INC-1842). Retry only on 503 + network errors.

Fixes #8421
```

**Bad:**

```text
fix stuff
updated files
WIP
```

**Breaking change:**

```text
feat(api)!: remove legacy /v1/orders list shape

BREAKING CHANGE: clients must use cursor pagination on /v2/orders.
```

### 4. Atomic commits when helpful

1. One logical change per commit if history is used for bisect/revert.
2. Don’t mix massive formatting with logic (or mark `style` separately).

### 5. Verify

```bash
git log -1 --pretty=full
# commitlint if configured
npx commitlint --from HEAD~1 --to HEAD 2>/dev/null || true
```

1. No secrets, tokens, passwords in message.
2. Issue refs resolve.

### 6. Amend / fixup carefully

1. `--amend` only for unpushed or coordinated force-with-lease.
2. Prefer `fixup` + rebase for private branches.

### 7. Hand off

1. Document convention in CONTRIBUTING if missing.
2. Optional CI commitlint on PR titles if squash-merge uses PR title.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Subject | `fix(api): handle empty page token` | `fixed bug` |
| Body | Why + context | Paste of diff |
| Secrets | None | API keys in message |
| Breaking | `BREAKING CHANGE:` footer | Silent incompatible change |
| Types | Accurate `feat`/`fix` | Everything `chore` |

## Output Checklist

- [ ] Local commitlint/CONTRIBUTING consulted
- [ ] Type/scope accurate
- [ ] Subject imperative and concise
- [ ] Body explains why when needed
- [ ] Footers for issues/breaking changes
- [ ] No secrets in message
- [ ] Matches team squash/merge policy if any

## Rules

- Prefer why over what; history is for humans and changelogs.
- Never put credentials in commit messages (they live forever).
- Repo-local rules override this skill when stricter.
- Focus on **commit messages**; code quality and PR tone are siblings.
