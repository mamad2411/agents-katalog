---
name: prompt-logging-hook-setup
description: Use when setting up, repairing, verifying, or troubleshooting a UserPromptSubmit prompt logging hook in a target repository, including trusted mode checks, hooks.json command wiring, git user name prompt-prefix logging, and per-user prompt log file names.
---

# Prompt Logging Hook Setup

Use this skill when the user wants to install a UserPromptSubmit prompt logging hook from scratch, repair a broken setup, check why the hook is not firing, or verify that prompt logs are being written correctly for a target repository.

## Workflow

1. Inspect the hook files in the repository being diagnosed before proposing changes:
   - `.codex/config.toml`
   - `.codex/hooks.json`
   - the referenced script under `.codex/hooks/`
2. Verify whether the repository being inspected must be opened in trusted mode for `.codex` to load.
3. Check the hook command carefully:
   - confirm the event name
   - confirm the script path resolves from the repo root
   - confirm the script reads JSON from stdin and handles invalid payloads safely
4. Verify the log schema:
   - `git_user_name` should come from `git config user.name`
   - `prompt_prefix` should match that Git user name
   - `prompt_raw` should preserve the unprefixed user input
   - `prompt` should contain the visible prefixed form
5. Verify where output is written and whether the parent directory is created.
   - prompt logs should be per Git user: `logs/{sanitized-git-user-name}-prompt-log.jsonl`
6. If the user wants a diagnosis, run `scripts/validate_hook_setup.py <repo_path>` first.
7. If the user wants a fix, prefer the smallest repair:
   - enable `codex_hooks`
   - fix malformed `hooks.json`
   - fix the command path
   - add Git user name prefix logging
   - fix log path creation
   - repair the standard prompt log hook with `scripts/install_or_repair_hook.py <repo_path>`
   - document trusted mode requirements when the repo still looks structurally correct

## What Good Prompt Logging Hook Setups Usually Include

- `codex_hooks = true` in `.codex/config.toml`
- a valid `.codex/hooks.json`
- a hook script that accepts stdin JSON and exits safely on malformed payloads
- a hook script that reads Git `user.name` and stores it as `git_user_name` and `prompt_prefix`
- a per-user log path inside the target repository, such as `logs/{sanitized-git-user-name}-prompt-log.jsonl`
- a short troubleshooting note explaining trusted mode

## Troubleshooting Priorities

- If no hook runs at all, first suspect trusted mode or `.codex/config.toml`.
- If the hook is registered but no log file appears, inspect the command path and write target.
- If the script runs but log lines are missing prefix fields, inspect the Git user lookup and log schema.
- If the structure is correct but runtime behavior still fails, explicitly tell the user to reopen the repository being repaired in trusted mode because that cannot be repaired by editing files inside the repository alone.
- If the user asks for documentation, keep it short and operational rather than explanatory.

## Resources

- Use `scripts/validate_hook_setup.py` for a fast structural check.
- Use `scripts/install_or_repair_hook.py` to write the standard prompt hook files into a target repository.
- Read `references/troubleshooting.md` when you need a more explicit diagnosis checklist.
