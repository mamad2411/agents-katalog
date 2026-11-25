---
name: git-commit-message-delivery
description: Base primitive — safely pass multi-line commit messages containing
    shell-special characters to `git commit` without escaping failures, and
    verify commit contents with reliable path listing.
category: Git & Repository Management
---

# Git Commit Message Delivery Skill (v1) — Base Primitive

> **Skill ID:** `git-commit-message-delivery`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

When constructing a commit, the agent must deliver the message to `git commit`
without shell-escaping failures and verify the resulting commit contains the
expected files. This skill documents three delivery patterns with clear
selection criteria, plus the reliable verification technique.

### Message Delivery Problem

`git commit -m '...'` breaks when the message contains:

| Character | Why it breaks |
|-----------|---------------|
| `'` (single quote) | Closes the shell quoting — `it's` becomes `git commit -m 'it'` with trailing `s'` as garbage |
| `$` (dollar sign) | Triggers variable expansion — `$variable` is replaced by its value |
| `` ` `` (backtick) | Starts subshell execution |
| Newlines | Multi-line `-m` messages are fragile across shells |

### Verification Problem

`git show --stat` truncates long file paths to fit terminal width:

```
.../ai-agent-rules/git-operation-rules.md
```

A `grep` or `Select-String` on the stat output may miss matches because the
truncated path no longer matches the expected string. `--name-only` outputs
every file path in full with no truncation.

---

## 1. Delivery Pattern Reference

### 1.1 `-m` (Simple single-line messages)

Safe when the message is a single line with no `"`, `$`, or `` ` `` characters.

```bash
git commit -m "docs(rules): add widget lifecycle protocol"
```

**Limitations:**
- `'` is safe inside double-quoted `-m` in bash/zsh, but `'` inside `-m '...'` breaks
- `$` and `` ` `` must be escaped (`\$`, `` \` ``)
- Newlines require fragile `\n` concatenation
- **Forbidden for multi-line messages or any content that contains characters whose shell interaction is uncertain**

### 1.2 Heredoc → `-F` (Safe for all content)

**RECOMMENDED for multi-line or special-character messages.** Use a heredoc to
write the message to a temp file, then pass via `-F`:

```bash
cat > /tmp/commit_msg <<'EOF'
feat(api): add user registration endpoint

- Implements POST /api/v1/users with validation
- Adds email uniqueness check before insert
- Returns 201 with user ID on success
EOF

git commit -F /tmp/commit_msg
```

**Key details:**
- `<<'EOF'` (quoted delimiter) prevents ALL shell interpolation — `$`, `` ` ``, and `'` are passed verbatim
- Use a unique temp file path per invocation: `/tmp/commit_msg.$$` or `/tmp/commit_msg.$(date +%s)`
- `git commit -F` reads the file; no shell parsing of the message occurs
- Clean up: `rm -f /tmp/commit_msg` immediately after the commit succeeds

**Why not embed inside `-m` with `$()`?** `git commit -m "$(cat <<'EOF' ...)"` still
exposes the message to the shell's `-m` argument parsing; any characters that
interact with the outer double-quoting (`"`, `$`, `` ` ``) can still break.

### 1.3 `GIT_EDITOR` script (Reword / Amend)

When Git invokes the editor for `reword`, `amend`, or interactive rebase, delegate
message writing to a script that replaces `$1`:

```bash
cat > /tmp/commit_msg.sh <<'SCRIPT'
#!/bin/sh
cat > "$1" <<'MSG'
feat(api): add user registration

Implementation notes:
- Uses bcrypt for password hashing
- Rate-limited to 10 requests/min per IP
MSG
SCRIPT

chmod +x /tmp/commit_msg.sh
GIT_EDITOR=/tmp/commit_msg.sh git commit --amend
rm -f /tmp/commit_msg.sh
```

This is the canonical pattern used by
[`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) and
[`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md).

---

## 2. Verification Pattern

### 2.1 Reliable file listing — `--name-only`

After a commit, verify the file set with:

```bash
git show --name-only HEAD
```

This outputs every file path in full, one per line. Pipe to `grep` for targeted
checks:

```bash
git show --name-only HEAD | grep "git-operation-rules.md"
```

Use this for **programmatic path matching** — it never truncates.

### 2.2 Full diff inspection

When you need to verify both the file set AND the content:

```bash
git show HEAD          # full diff with paths
git show --stat HEAD   # summary with line counts
```

Use `--stat` only for human-readable summaries, never for programmatic path
matching.

### 2.3 Detecting stat truncation

If `--stat` output is the only data available, detect truncation by checking
for leading `...`:

```bash
git show --stat HEAD | grep '\.\.\./'
```

Any match indicates path truncation. Switch to `--name-only` for reliable
matching. The `.../` prefix signals Git clipped the path to fit terminal width.

---

## 3. When to Apply

Apply this skill whenever you need to:

- Construct a `git commit` command with a multi-line or special-character message
- Verify that a commit contains the expected file paths
- Debug a shell-escaping error in a commit-message command

Do NOT apply when:

- The commit message is a single short line with no special characters
  (`git commit -m "..."` is sufficient)
- You are inspecting commit *content* (diff hunks) rather than the file
  manifest — use `git show` or `git diff` directly

---

## 4. Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| `-m '...'` with `'` in message produces shell syntax error | Switch to heredoc → `-F` pattern (§1.2) |
| `git show --stat | grep <file>` misses known-committed files | Use `git show --name-only` instead (§2.1) |
| Temp file path collision in parallel shells | Use unique paths: include `$$` or `$(date +%s)` in the filename |
| Forgetting to remove temp file after commit | Add `rm -f <file>` as the next command after `git commit -F` succeeds |

---

## Prohibited Behaviors

- **Using `-m` for multi-line messages** — line breaks are fragile across shells
- **Using `-m '...'` when the message contains single quotes** — always switch to heredoc → `-F`
- **Relying on `--stat` output for programmatic path matching** — truncation makes it unreliable; use `--name-only`

---

## Related Skills

- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) — primary consumer; Step 10 references this skill's delivery and verification patterns
- [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) — consumer of the `GIT_EDITOR` pattern (§1.3)
- [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md) — consumer of the `GIT_EDITOR` pattern (§1.3)
