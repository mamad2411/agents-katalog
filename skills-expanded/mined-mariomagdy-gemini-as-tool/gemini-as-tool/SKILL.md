---
name: gemini-as-tool
description: Use Google Gemini (3.x Pro and Flash) as a headless tool from Claude Code — a second opinion, a builder, or a judge — via a Google AI Pro OAuth subscription with no API key. Use when the user says "use Gemini", "ask Gemini", "get a second opinion", "have Gemini review/judge this", "cross-check with another model", or "orchestrate Gemini"; asks the literal question "how do I use Gemini from Claude Code?"; mentions Gemini 3 Pro/Flash, Antigravity, agy, or the Gemini CLI; or when you want to run Gemini headlessly or fan out prompts in parallel.
when-to-use: Reach for this for a second-model opinion, a builder→judge pipeline, or parallel Gemini calls from inside Claude Code. Trigger phrases — "use Gemini", "ask Gemini", "second opinion from Gemini", "have Gemini judge/review this", "cross-check with Gemini", "run this by another model", "orchestrate Gemini as a subagent".
---

# Gemini as a Tool (Google AI Pro subscription, no API key)

## Overview

A tested harness ships with this skill for calling subscription Gemini models headlessly:

```
python "$CLAUDE_PLUGIN_ROOT/skills/gemini-as-tool/gemini_tool.py" <ask|pipeline|parallel> ...
```

Use it. Do not rediscover the plumbing — the raw CLIs have traps (below).

## Quick reference

> **Locating the script.** When installed as a plugin, Claude Code sets `$CLAUDE_PLUGIN_ROOT`, so
> the harness is `$CLAUDE_PLUGIN_ROOT/skills/gemini-as-tool/gemini_tool.py`. If that variable is
> not set (e.g. a plain clone), the script is in this skill's own directory — run `python
> gemini_tool.py ...` from there. The commands below use the short form for brevity.

| Goal | Command |
|---|---|
| One answer (3.5 Flash) | `python gemini_tool.py ask "prompt"` |
| One answer (3.1 Pro) | `python gemini_tool.py ask "prompt" --model pro` |
| Builder→judge (Pro builds, Flash judges) | `python gemini_tool.py pipeline "build task"` |
| N prompts concurrently | `python gemini_tool.py parallel "p1" "p2" "p3"` |

(Python API: `from gemini_tool import ask`.)

Calls take 10–60s (agy startup ≈10s). Verified working 2026-06-04.

## Running a BUILD with Gemini (proven recipe, 2026-06-06)

A proven pattern for delegating a full build to Gemini:

1. **Brief as a FILE, not a prompt.** Write a detailed `BUILD_BRIEF_<name>.md` in the target
   repo/worktree (read-these-files-first list, file ownership + do-not-touch, blocking
   tsc/test gates, "write BUILD_REPORT_<name>.md as your completion signal"). The ask prompt
   is then just: *"Read `<abs path>\BUILD_BRIEF_<name>.md` and execute it fully, step by step.
   If you cannot edit files or run commands in this mode, say exactly that as your entire
   reply."* (The escape hatch catches permission failures honestly instead of a hallucinated
   success story.)
2. **Isolated git worktree** (`git worktree add _wt-<name> -b <branch>`) when any other agent
   touches the same repo.
3. **`--timeout 2700` is MANDATORY for builds.** The default 300s kills the run mid-build and
   surfaces as `agy run finished but conversation could not be located`. Launch in background:
   `python gemini_tool.py ask "<pointer prompt>" --timeout 2700`
4. **Completion signal** = the BUILD_REPORT file + commits on the branch (check `git log`),
   not the stdout text alone.
5. **Verify untrusted:** re-run the gates yourself (tsc + full suite), scope-audit with
   `git show <commit> --stat` against the ownership list, review the diff.
6. **Record the result** for your own tracking (what the model built, whether gates passed).

## Facts that prevent wasted effort

- **Gemini 3.5 Flash EXISTS** (GA since 2026-05) but is **Antigravity-only**. On `gemini` CLI, `gemini-3.5-flash` → 404. Do NOT conclude it doesn't exist and silently substitute an older model — that fails the user's request. The harness's `--model flash` = real 3.5 Flash via agy.
- **Raw `agy -p` prints NOTHING to stdout on Windows** (exit 0, empty pipe — antigravity-cli#115). It is not broken auth; the response is in `~/.gemini/antigravity-cli/brain/<conv-id>/.system_generated/logs/transcript.jsonl`. The harness handles this; don't pipe agy directly.
- **agy `--model` takes display labels** (`"Gemini 3.5 Flash (High)"`, `"Gemini 3.1 Pro (High)"`). Plain ids are silently ignored (falls back to default).
- **`gemini` CLI sunsets for this account 2026-06-18.** Don't build anything new on it; the harness's `--backend gemini-cli` is temporary.
- Auth is OAuth (your Google account, keyring) — never ask for or set an API key for this.

## Common mistakes

| Mistake | Fix |
|---|---|
| Probing model names against `gemini` CLI to find 3.5 Flash | It's not there. Use the harness (agy backend). |
| `agy -p ... \| <parse stdout>` | Empty by bug. Use the harness, or read transcript.jsonl. |
| Asking a model to self-identify to verify version | Unreliable. Trust the harness's model labels (verified). |
| Treating exit 55 / trust errors as auth failure | Workspace trust: `--skip-trust` (gemini) or run under your home directory (`%USERPROFILE%`) (agy). |
| Launching a build with the default timeout | 300s default kills builds → "conversation could not be located". Pass `--timeout 2700`. |

Details/ops notes: see `README.md` in this repo.
