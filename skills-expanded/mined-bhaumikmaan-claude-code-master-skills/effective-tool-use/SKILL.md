---
name: effective-tool-use
description: Optimal tool selection, parallelism, and safety for coding tasks. Covers the IDE tool preference matrix, parallel vs sequential execution, git safety, sandbox awareness, and file operation hygiene. Use when writing tool calls, running commands, managing files, or performing git operations.
user-invocable: true
---

# Effective Tool Use

CRITICAL: Prefer dedicated IDE tools over shell equivalents. They provide better user experience, clearer diffs, and easier permission review.

## Tool Preference Matrix

Always use the dedicated tool instead of its shell equivalent:

| Task | Use This | NOT This |
|------|----------|----------|
| Find files by pattern | Glob | `find`, `ls -R` |
| Search file contents | Grep | `grep`, `rg`, `ag` |
| Read a file | Read | `cat`, `head`, `tail` |
| Edit an existing file | Edit | `sed`, `awk`, inline scripts |
| Create / overwrite a file | Write | `echo >`, `cat <<EOF >`, `tee` |
| Communicate with the user | Direct text output | `echo`, `printf` |

Reserve the shell (Bash) tool for actual system commands: `git`, `npm`, `docker`, `make`, `curl`, test runners, build tools, and other CLI operations that have no dedicated tool equivalent.

## Token Cost Hierarchy

Tools differ drastically in token cost. Always narrow before you read:

1. **Glob** (near-zero tokens) — Returns file paths only. Start here to map the landscape.
2. **Grep with `-C 3`** (lightweight) — Returns matched lines plus context. Use `head_limit` to cap results for common terms. Often sufficient without a full file read.
3. **Read** (heavy, 500-5000+ tokens) — Full file content. Use ONLY after Glob/Grep confirmed the file is relevant.

For meaning-based queries ("how does authentication work"), check if MCP tools like `search_code` are available before falling back to broad Grep with keywords and synonyms.

When research spans >5 files, spawn a subagent via the Agent tool to research in an isolated context and return a summary. This prevents context exhaustion in the main session.

## Reading Files

- Read files before editing them. An edit to unread code is a guess, not a fix.
- Write tool requires a prior Read of the target file. It will fail otherwise.
- For large files, use offset/limit to read only the relevant section. Don't load 2000 lines when you need 20.
- When you already know which section you need (from a Grep match with line numbers), read just that range.
- Prefer Edit over Write for modifying existing files — Edit sends only the diff. Use Write for new files or complete rewrites.
- Never create documentation files (*.md) or READMEs unless the user explicitly asks.

## Parallel vs Sequential Execution

### Parallel (separate tool calls in one message)
Use when operations are independent and can run simultaneously:
- Multiple Grep searches for different patterns
- `git status` and `git diff` at the same time
- Reading multiple unrelated files
- Independent test runs across different modules

### Sequential (`&&` chaining in a single Bash call)
Use when operations depend on each other:
- `mkdir -p dir && cp file dir/` — directory must exist before copy
- `git add file && git commit` — file must be staged before commit
- `npm install && npm build` — deps before build

### Fire-and-forget (`;` chaining)
Use only when you need sequential execution but don't care if earlier commands fail:
- `rm -f old.log ; echo "cleaned"` — proceed regardless

### Rules
- Never use newlines to separate commands in a single Bash call (newlines OK inside quoted strings).
- Don't use `&` to background processes — use the `run_in_background` parameter instead.
- Don't sleep between commands that can run immediately. If you need to wait for a background task you started with `run_in_background`, you'll be notified when it completes — don't poll.
- Don't retry failing commands in a sleep loop. Diagnose the root cause.

## File Operations

- Before creating new directories or files, run `ls` to verify the parent directory exists and is the correct location.
- Always quote file paths containing spaces with double quotes.
- Maintain your working directory — use absolute paths and avoid `cd` unless the user requests it.
- When checking if a file/resource exists before operating on it, prefer operating directly and handling the error (avoids TOCTOU race conditions).

## Git Safety

- **Prefer new commits** over amending. After pre-commit hook failure, the commit did NOT happen — `--amend` would modify the PREVIOUS commit and risk destroying work.
- **Never skip hooks** (`--no-verify`, `--no-gpg-sign`) unless the user explicitly asks. If a hook fails, investigate and fix the underlying issue.
- **Never force-push** to main/master. Warn the user if they request it.
- **Never run destructive commands** (`reset --hard`, `checkout .`, `clean -f`, `branch -D`) unless the user explicitly requests them.
- **Stage specific files** by name rather than `git add -A` or `git add .`, which can accidentally include secrets or binaries.
- **HEREDOC for commit messages** to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
Commit message here.
EOF
)"
```

- Never use interactive flags (`-i`) like `git rebase -i` or `git add -i` — they require terminal input that isn't supported.
- Never update the git config.
- If CI is configured for the project, check pipeline status after pushing. A green local build with a red CI pipeline is not "done."

## Sandbox Awareness

When running in a sandboxed environment:
- Use `$TMPDIR` for temporary files, NOT `/tmp` directly. The sandbox sets `$TMPDIR` to the correct writable directory.
- If a command fails with "Operation not permitted" or access denied errors, the sandbox may be restricting it. Check the sandbox configuration before retrying.
- Default to running commands within the sandbox. Only disable sandboxing when you see clear evidence of sandbox-caused failure (not general command failures).
- Don't suggest adding sensitive paths (~/.bashrc, ~/.zshrc, ~/.ssh/*, credential files) to the sandbox allowlist.

## Command Timeouts and Background Tasks

- Commands have a default timeout. For long-running operations (builds, large test suites), set an appropriate timeout.
- Use `run_in_background` for commands you don't need results from immediately. You'll be notified when they complete — no polling needed.
- Don't sleep as a first action. If waiting for rate limiting or deliberate pacing, keep it under 2 seconds.

CRITICAL REMINDER: Use dedicated IDE tools over shell equivalents. Narrow searches with Glob/Grep before reading full files. Read before editing. Never skip git hooks or force-push without explicit user consent.

## Related Skills

- For search-heavy workflows, apply `codebase-exploration` patterns for systematic investigation.
- Git commit and PR creation workflows interact with `disciplined-coding` scope and verification standards.
- When building constrained tool flows for specialized tasks, apply `prompt-engineering` patterns.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Project-specific shell commands and aliases
- Custom sandbox allowlist paths
- Git workflow conventions (branch naming, commit message format)
- Preferred package manager and build commands
