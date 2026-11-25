---
name: line-check
description: Use after every Write, Edit, or MultiEdit AND before every Bash tool call to audit the line/command for contradictions, syntax errors, shell-mode/completeness traps, factual claims, and scope creep. Catches the class of bug where a partially-formed shell command drops PowerShell into a `>>` continuation prompt and never executes (unbalanced quotes, unclosed heredocs, missing flag args, PS-vs-bash mode confusion). Companion to karpathy-guidelines, operating at line granularity. Auto-triggers via PostToolUse hook on writes; pair with PreToolUse(Bash) hook for command pre-flight.
---

# Line-Check

Per-line audit pass run immediately after producing any written artifact (code, prose, config, commit message) AND before sending any shell command. Companion to `karpathy-guidelines`: where Karpathy operates on tasks ("think before coding", "surgical changes"), Line-Check operates on lines ("does THIS line contradict the line above it, the spec, reality, or the shell it is about to run in").

## Vivid Failure (the bug class this exists for)

Real session, real waste:

```
PS C:\Users\you\projects\demo> ssh remote-host "mkdir -p ~/.claude/projects/myproject && tar -xzf ~/memory.tgz -C
>>
```

What broke on this single line:
1. `tar -xzf ~/memory.tgz -C` — `-C` flag expects a target directory argument; nothing follows it.
2. The double-quoted SSH command argument was never closed (no trailing `"`).
3. PowerShell entered continuation mode (`>>`) waiting for the closing quote that never came.

Cost: command never executed, user typed a second corrupted version, then aborted. Tokens and minutes burned for a missing `<dir>` and a missing `"`.

**Line-Check exists to catch this class of error in one cheap pass before the line is sent.** Five checks, one of which is dedicated to exactly this trap.

## When to run

- **Always:** after a `Write`, `Edit`, or `MultiEdit` tool call (auto-triggered by PostToolUse hook).
- **Always:** before any `Bash` tool call (PreToolUse hook recommended — see Hook Setup section).
- **Always:** before posting a code block in chat the user might copy-paste.
- **Manual:** before claiming completion, before committing, when reviewing pasted spec.
- **Skip:** binary files, generated files, files >2000 lines (sample instead — see Long-File Mode).

## The Five Checks

For each changed/written line OR each command about to be sent, in order. Stop at the first hard failure; fix; restart from check 1.

### 1. Contradiction Check
Does this line contradict:
- An earlier line in the same file (e.g. function says `returns int`, body returns `str`)?
- A line elsewhere in the diff (e.g. caller passes `userId`, callee takes `user_id`)?
- The user's stated requirement (e.g. user said "no external deps", line imports `requests`)?
- A claim made in chat ("I'll use Postgres" → line uses SQLite)?

If yes → flag, propose fix, do not silently pick.

### 2. Syntax Check
- Does the line parse in its language? (mismatched brackets, missing colons, unterminated strings)
- Does it reference identifiers that exist? (typos in variable/function names, wrong imports)
- For prose: complete sentences, matching quotes, correct list syntax.
- For config (JSON/YAML/TOML): valid structure, correct types.

When uncertain → run a parser/linter or read surrounding context. Do not guess.

### 3. Shell-Mode & Completeness Check (*new — failure-class catcher*)

Specifically catches the bug class shown in the Vivid Failure above. Run on every shell command and every multi-line shell block.

**3a. Right shell?** Does the syntax match the shell that will execute it?
- `PS C:\…>` prompt → PowerShell. `cd /tmp && ls` is bash, NOT PS. PS uses `;` not `&&` for unconditional chain; `cd /tmp; ls`. PS env vars: `$env:NAME`, not `$NAME`. Forward path-quote rules differ.
- `$` / `#` prompt → bash/zsh. Heredocs `<<EOF`, expansions `$(...)`, `&&` chaining all valid.
- Mixed-shell paste (PS prompt with bash-isms, or vice versa) → flag immediately.

**3b. Quotes balanced?** For the line/block, count UNESCAPED:
- `"` count must be even.
- `'` count must be even.
- `` ` `` (backtick) count must be even (PS escape; bash command sub).

If any odd → line is incomplete; shell will hang in continuation. Name the missing closer.

**3c. Brackets balanced?** Count `()`, `{}`, `[]`, plus PS-specific `@()`, `@{}`, `$()`. If any unmatched → incomplete.

**3d. Heredocs closed?** If line opens `<<EOF` (or `<<MARKER`), block must contain a line that is `EOF` (or `MARKER`) with NO leading whitespace and NO trailing whitespace. `<<-EOF` allows leading tabs only.

**3e. Trailing-continuation?** If line ends with `\` (bash), `` ` `` (PS), `&&`, `||`, `|`, `,`, `(`, `{`, `[` — line is by definition incomplete; next line is required. Flag if you intended a single command.

**3f. Flag-args filled?** Common flags that REQUIRE a value:
- `tar -C <dir>`, `tar -f <file>`, `tar -T <list>`
- `cp -t <dir>`, `mv -t <dir>`
- `ssh -i <key>`, `ssh -p <port>`, `ssh -L <fwd>`
- `git -C <dir>`, `git checkout -b <name>`
- `docker run -v <vol>`, `docker run -p <port>`, `docker run --name <n>`
- `find -name <pat>`, `find -type <t>`, `find -exec <cmd>`
- `sed -e <expr>`, `sed -i <suffix>`
- `awk -F <sep>`, `awk -v <var>=<val>`
- `xargs -I <repl>`, `xargs -n <num>`
- `curl -o <file>`, `curl -H <hdr>`, `curl -d <data>`
- `kubectl -n <ns>`, `kubectl -f <file>`
- `npm -w <ws>` (note: `pnpm -r` / `--recursive` takes NO arg — do not flag it)

If a `-X` flag appears with the next token being another `-Y` flag, EOL, or a closing quote → likely missing arg. Name what should fill it.

**3g. Bash-on-Windows context?** WSL paths (`/home/...`), Git Bash quoting, Cygwin behavior — flag if line assumes one but session is in another.

If 3a–3g all clear, the command is structurally complete. Does NOT prove it does the right thing — only that it will execute instead of hang.

### 4. Fact Check
For lines making factual claims:
- API signatures: does this method/flag actually exist in the version we're using?
- File paths: does the path exist? (Use `Glob`/`Read` to verify before asserting.)
- Version numbers, dates, URLs: invented or sourced?
- Behavioral claims ("this returns null on miss"): documented or assumed?

If sourced from memory, mark uncertainty. If a hallucination risk exists, verify with `Read`/`Grep`/`WebFetch` before locking in.

### 5. Scope Check
Per Karpathy guideline #3 (Surgical Changes): every changed line must trace to the user's request.
- Did this line need to change for the requested task?
- Is it a drive-by refactor, a "while I'm here" cleanup, or a speculative abstraction?
- Did I add error handling for an impossible case? A config knob nobody asked for?

If a line fails scope check → revert it. Mention it separately if worth flagging, but do not bundle.

## The Pilot Pre-Send Checklist (shell commands)

Before sending ANY shell command — single line or block — stamp these 6 in order. Aviation pattern: short, fixed, run before every takeoff.

1. **Quotes paired?** `"`, `'`, `` ` `` all even count.
2. **Brackets paired?** `()`, `{}`, `[]`, `@()`, `@{}`.
3. **Heredocs closed?** `<<EOF` has matching bare `EOF`.
4. **No trailing-continuation by accident?** Line doesn't end in `\`, `` ` ``, `&&`, `||`, `|` unless next line follows.
5. **Flag-args filled?** Every `-X` that takes a value has one.
6. **Right shell?** Syntax matches PS / bash / zsh / cmd / fish at the prompt shown.

If all 6 stamp clean → send. If any fail → name the missing piece, fix, re-stamp from 1.

## Operating Procedure

After a write/edit completes, OR before a Bash call goes out:

1. **Re-read the diff or command.** Not the whole file — just changed lines / the command string.
2. **Walk each line** through the 5 checks. Most lines clear all 5 instantly; that is fine — speed comes from cheap passes, not from skipping.
3. **For shell commands, also stamp the 6-item Pilot Checklist.**
4. **Collect findings.** For each failure: `<file>:<line> — <check> — <issue> — <proposed fix>`.
5. **Fix immediately** if mechanical (typo, missing closer, missing flag arg, contradiction with earlier line). Use `Edit`.
6. **Surface for confirmation** if judgment-level (scope creep that might have been intended, factual claim you cannot verify, contradiction with possibly-misread context).
7. **Do not claim completion** until audit is clean OR every finding resolved/surfaced.

## Recursion Guard

The skill is invoked by hooks on Write/Edit/Bash. The skill's own auto-fixes use Write/Edit/Bash, which would re-trigger the hook → infinite loop.

**Rule:** if hook environment shows `LINE_CHECK_DEPTH=1` (set by the hook on first invocation), the skill DOES NOT auto-fix mechanically. It surfaces findings to the user instead. This caps recursion at depth 1.

For the simpler implementation: skill explicitly tracks "I just fixed something with Edit" → next PostToolUse trigger is acknowledged but no further auto-fix happens, only verification of the fix.

## Output Format

When findings exist, report as:

```
line-check findings (N):
  path/to/file.ts:42 — contradiction — return type `User` but body returns `User | null` — narrow return or widen signature?
  path/to/file.ts:58 — syntax — closing brace missing for `if` block — fixed in edit
  cmd:bash — shell-completeness — `-C` flag has no target dir AND closing `"` missing — fixed: `ssh remote-host "… -C ~/.claude/projects/myproject"`
  README.md:14 — fact — claims Node 18+ but package.json `engines` says 20+ — aligned to 20+
  src/auth.ts:91 — scope — added telemetry call, not in user request — reverted
```

When clean: silent. Do not announce a passing audit — it is the default.

## Long-File Mode

For diffs >200 changed lines:
- Audit changed regions only (not whole file).
- Group by file; report per-file counts.
- If a file has >50 findings, stop and ask the user — likely a mismatch between intent and implementation, not a per-line fixable problem.

## Compound-Language Lines

Lines where one language is embedded inside another are doubly-prone:
- SQL inside a Python triple-quoted string.
- Bash command inside `subprocess.run(["bash", "-c", "..."])`.
- Regex inside a JSON config string.
- Dockerfile `RUN` lines (bash inside Docker).
- PowerShell here-strings (`@'...'@`, `@"..."@`) embedding scripts (see also `publish-skill` skill which documents PS here-string parse traps in detail).
- `eval` / `exec` strings.

Run BOTH the host-language Syntax Check AND the inner-language Syntax Check + Shell-Mode Check. Most one-line bugs in this category are unbalanced quotes between the two layers.

## Hook Setup (companion)

Two hook entries make Line-Check auto-fire. Settings.json edits are blocked from agent self-mod — paste these into `~/.claude/settings.json` `"hooks"` block manually:

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit|MultiEdit",
    "hooks": [
      {
        "type": "command",
        "command": "python -c \"import json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PostToolUse','additionalContext':'[LINE-CHECK ACTIVE] File write/edit completed. Run line-check skill: re-read the diff and audit each changed line through the 5 checks (Contradiction, Syntax, Shell-Mode, Fact, Scope). Fix mechanical failures via Edit; surface judgment-level findings before claiming completion. Recursion guard: skip auto-fix if LINE_CHECK_DEPTH set. Format: <file>:<line> -- <check> -- <issue> -- <fix>. Silent on clean audits.'}}))\""
      }
    ]
  }
],
"PreToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python -c \"import json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','additionalContext':'[LINE-CHECK PRE-FLIGHT] Before sending this Bash command, run the 6-item Pilot Checklist from the line-check skill (quotes paired, brackets paired, heredocs closed, no accidental trailing continuation, flag-args filled, right shell). See ~/.claude/skills/line-check/SKILL.md section: The Pilot Pre-Send Checklist. If any item fails, fix the command BEFORE sending. Silent on clean.'}}))\""
      }
    ]
  }
]
```

## Interaction with Other Skills

- **karpathy-guidelines:** task-scope (think before coding, define success criteria). Line-Check is line-scope (verify the bytes you just wrote/are about to send). They stack — Karpathy gates *what* you do, Line-Check gates *what you ship*.
- **superpowers:verification-before-completion:** Line-Check feeds into it. Verification asks "did the whole change work"; Line-Check asks "is each line internally consistent and shell-safe". Run Line-Check first; verification afterwards.
- **publish-skill:** documents PS here-string parse traps — cross-link for compound-language line checking.
- **caveman mode:** Line-Check output stays terse. Drop articles in findings; keep file paths, line numbers, missing-token names exact.
- **simplify (oh-my-claudecode):** Scope check overlaps with simplify's reuse/efficiency review. Line-Check catches it earlier (immediately post-write); simplify catches it as a later pass.

## What Line-Check is NOT

- Not a linter replacement — does not catch every style issue. Run real linters when the project has them.
- Not a test replacement — does not prove behavior, only internal consistency. Run tests.
- Not a security audit — flags obvious leaks but does not replace a real security review.
- Not a typing system — catches obvious type contradictions, not deep flow analysis.
- Not a sandbox — does not pre-execute commands. Companion `validate.sh` (deferred v2) would add `bash -n` / `python -m py_compile` / `pwsh [scriptblock]::Create` real-parser checks.

It is a **fast self-review pass** that catches cheap, embarrassing, hallucination-class mistakes (and the continuation-prompt trap) before they reach the user.

## Anti-Patterns

- Running it once per file instead of once per write — defeats purpose; the next write may invalidate prior checks.
- Skipping because "the diff is small" or "the command is short" — small diffs hallucinate too; one-line shell commands are the most-hit by the continuation-prompt trap.
- Treating it as a replacement for thinking before coding — it is the safety net, not the plan.
- Auto-fixing scope-check failures without mentioning them — silently dropping changes the user might have wanted.
- Running it on the *whole file* every time — only changed regions. Cheap stays cheap.

## Roadmap (deferred — do NOT build until v1 fails to catch user pain)

- **v2:** Companion `validate.py` / `validate.sh` — stdlib-only validator that shells out to `bash -n`, `python -m py_compile`, `pwsh -Command "[scriptblock]::Create(...)"`, `tsc --noEmit` (warm), `cargo check` (slow — opt-in). Regex fallback per shell. Cap 100ms / per file; skip if exceeds.
- **v3:** MCP tool `linecheck.validate(text, lang)` — model calls explicitly, language-detected, returns structured findings.
- **v4:** Telemetry log → auto-promote most-common failure patterns to the cheat sheet. Opt-in.

Ship v1 first. Measure pain. Build v2+ only if v1 leaks.
