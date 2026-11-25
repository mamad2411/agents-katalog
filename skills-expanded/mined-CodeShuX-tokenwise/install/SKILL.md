---
description: Install TokenWise routing rules into the user's Claude Code config (CLAUDE.md and settings.json). Probes the user's Claude Code build for known routing bugs first, shows diffs, backs up originals, asks for per-file confirmation. Supports --guided (default), --manual (print copy-paste only), and --dry-run (preview without writing). Use when the user says "install tokenwise", "set up tokenwise", or runs /tokenwise:install.
---

# /tokenwise:install — Configure model routing

You are the TokenWise installer. Walk the user through Phase 1 (Detect) and Phase 2 (Configure) of the TokenWise lifecycle.

## Parse $ARGUMENTS

`$ARGUMENTS` may contain:
- `--guided` — force guided mode (default if not detected as power user)
- `--manual` — print copy-paste blocks, exit without writing
- `--dry-run` — show all proposed changes without writing OR printing copy-paste

If empty or contains `--guided`, run guided mode. If `--manual`, run manual mode. If `--dry-run`, run guided flow but skip every write step — print "DRY RUN: would write to <file>" instead.

## Phase 1 — Detect

Print a header:
```
TokenWise Install — Phase 1: Detect
====================================
```

Do these checks (use Read and Bash tools):

1. **Read existing configs:**
   - `~/.claude/CLAUDE.md` (global) — note "missing" if absent
   - `./CLAUDE.md` (project, if cwd is a git repo) — note "missing" if absent
   - `~/.claude/settings.json` — note "missing" if absent

2. **Claude Code version:** run `claude --version` via Bash. Record output.

3. **Subagent routing probe (Anthropic Issue #47488 regression test):**
   - Spawn a probe Task at Haiku tier: `Task(description: "probe", subagent_type: "general-purpose", model: "haiku", prompt: "Return only the string TOKENWISE_PROBE_OK")`
   - If the response contains `TOKENWISE_PROBE_OK`, routing works. If not, mark probe as FAILED.
   - Note: if your Task tool doesn't support `model:`, or you have no Task tool available at all in this session, mark as "routing probe: unverifiable on this build" and proceed the same way — this is not a FAILED result and doesn't block install.

4. **Env-var probe (Anthropic Issue #36381):**
   - Run `bash -c 'CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80 env | grep CLAUDE_AUTOCOMPACT'`
   - If output contains the override, env vars are honored. Note as "env-var probe: OK".

5. **Inventory existing skills/hooks** by listing `~/.claude/plugins/cache/*/` directories — note any that look like routing or token-tracking tools.

Print a detection summary table:

```
File                          Status
~/.claude/CLAUDE.md           [exists | missing]
./CLAUDE.md                   [exists | missing | n/a]
~/.claude/settings.json       [exists | missing]

Probe                         Status
Routing (Issue #47488)        [OK | FAILED | unverifiable]
Env-var (Issue #36381)        [OK | FAILED]

Existing plugins detected:    <list or "none">
Claude Code version:          <output of claude --version>
```

**If routing probe FAILED** and not in `--manual` mode, refuse to proceed and tell the user:
> Your Claude Code build (v<version>) appears affected by Anthropic Issue #47488 — subagent model routing is not honored. TokenWise needs working routing to function. Options:
> 1. Update Claude Code: `claude update`
> 2. Run `/tokenwise:install --manual` to install routing rules via prompt-level instructions only (works even with broken SDK routing)
> 3. Pin to a known-good Claude Code version

**Otherwise continue to Phase 2.**

## Phase 2 — Configure

### Determine target file

If only one of `~/.claude/CLAUDE.md` or `./CLAUDE.md` exists, use that one.
If both exist, ask the user: "Which CLAUDE.md should I modify? [1] global (~/.claude/CLAUDE.md) [2] project (./CLAUDE.md). [1/2]"
If neither exists, ask: "No CLAUDE.md found. Create one at: [1] global [2] project. [1/2]"

### Compose the routing block

This is the TokenWise routing block. It is inserted between `<!-- BEGIN TokenWise -->` and `<!-- END TokenWise -->` markers. If the target file already contains these markers, replace everything between them in place. Otherwise, append the whole block to the end of the file, preceded by one blank line — don't try to find a "natural" insertion point among existing headings.

```markdown
<!-- BEGIN TokenWise — routing rules. Managed by /tokenwise:install. Do not edit by hand. -->
## Model routing (TokenWise)

When delegating work via the Task tool, classify the task by TYPE and route it
automatically. All four tiers are equal, direct destinations — none of them
needs a confirmation prompt:

- **Mechanical → Haiku** (5× cheaper than Opus) — one-right-answer work: file reads,
  grep, format, rename, simple edits, doc lookups. No judgment calls.
- **Execution → Sonnet** (~1.67× cheaper than Opus) — bounded implementation: refactor,
  test writing, or bug-fix scoped to 1-2 files, scoped research and code exploration.
  A plan scoped to one file or module is execution prep, not Planning — it goes here too.
- **Review → Opus** — judgment over existing work: code review, security review,
  root-cause analysis, auditing outputs, choosing between already-stated options.
- **Planning → Fable** (2× Opus) — large planning only: system-wide architecture,
  multi-file or cross-cutting design, migration strategy, decomposing ambiguous
  requirements into a work plan.

Classification rules, in order:
1. Trivial floor: description <100 chars AND no file context → run inline, no subagent.
2. User override `# tokenwise: <haiku|sonnet|opus|fable>` in CLAUDE.md context wins.
3. Verb is find/grep/rename/format/read/list with a clear target → Mechanical.
4. Verb is implement/refactor/fix/test/explore, scoped to ≤2 named files or one module
   → Execution. Planning questions with the same tight scope also go here.
5. Verb is review/audit/evaluate/diagnose over existing code or given options → Review.
6. Design/architecture/planning work spanning 3+ files, crossing systems, or starting
   from ambiguous requirements → Planning.
When two types fit, prefer the cheaper lane — a misroute costs one cheap
reclassification (below), so under-routing is cheap and over-routing isn't.

Safety caps:
- Subagents NEVER self-escalate or re-route. A subagent that discovers it was
  misclassified (wrong type, or right type but insufficient capability) stops
  and returns to the parent with an `escalation_reason`. The parent
  reclassifies directly to the correct lane — any lane, one hop, e.g. Sonnet →
  Fable with no detour through Opus — and re-spawns once. If the re-spawned
  task bounces again, the parent finishes it inline.
- Max spawn depth = 2 (parent → subagent → one more). Haiku never spawns subagents.
- Subagent context >30k tokens: use the next more capable model within a lane
  (Haiku → Sonnet, Sonnet → Opus). This bump stops at Opus — it compensates for
  context volume, which Opus fully handles. Fable is reached by task type
  (Planning) only, never by input size.

After every routed Task, append one NDJSON line to `.tokenwise/log.ndjson` in the current project root (create the directory if missing). Schema:
{"ts": "ISO8601", "task_class": "mechanical|execution|review|planning",
 "task_summary": "<first 80 chars, redact secrets>",
 "model_used": "haiku-4-5|sonnet-4-6|opus-4-7|fable-5", "model_baseline": "opus-4-7",
 "input_tokens": N, "output_tokens": N,
 "cost_actual_usd": N, "cost_baseline_usd": N, "savings_usd": N,
 "escalated": bool,
 "escalation_reason": null|"needs-mechanical"|"needs-execution"|"needs-review"|"needs-planning"|"ambiguous-spec"|"insufficient-capability",
 "duration_ms": N}

`cost_baseline_usd` is this task's own `input_tokens`/`output_tokens` re-priced at Opus's
rate — not a separate estimate. This is what makes every report reproducible from its own
numbers: sum the input/output columns across all tiers, re-price that sum at Opus rate, and
you get the baseline back exactly. `savings_usd = cost_baseline_usd - cost_actual_usd`.

Note: `savings_usd` for a Planning (Fable) line will be negative (Fable costs more than
the Opus baseline). That's expected — log it as-is, don't clamp to zero.

Pricing (Aug 2026, per 1M tokens, input/output):
- Fable 5:     $10 / $50
- Opus 4.7:    $5 / $25
- Sonnet 4.6:  $3 / $15
- Haiku 4.5:   $1 / $5
<!-- END TokenWise -->
```

### Compose the settings.json patch (only if env-var probe passed)

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "80"
  }
}
```

(Merge into existing `env` object if present. If the existing `env` object has other keys, keep them — only add/update the two TokenWise keys above.)

### Guided mode flow

For each file to modify:

1. Print a unified diff of the proposed change. When diffing `settings.json`,
   elide the value of any pre-existing `env` key that looks like a secret
   (name contains `KEY`, `TOKEN`, `SECRET`, or the value itself matches a
   common credential shape) — show `"<redacted — existing value unchanged>"`
   in its place. Never print a real secret value into a diff, even one you
   are not modifying.
2. Ask `[Y/n] Apply this change?`
3. If Y:
   - Compute timestamp: `date +%Y%m%d-%H%M%S`
   - Back up: `cp <file> <file>.tokenwise-backup-<ts>` (or create empty marker if file is missing)
   - Write the modified file
   - Read it back, verify the marker is present
4. If n: skip

After all writes, print:
```
Install complete.

Files modified:
  <list>

Backups saved to:
  <list>

Next steps:
  1. Restart Claude Code so routing rules load
  2. Use Claude Code normally — every routed Task is logged automatically
  3. Run /tokenwise:report after a few tasks to see savings

Heads-up: large planning tasks route to Fable 5 automatically ($10/$50 per 1M
tokens, 2× Opus). There is no per-task prompt — run /tokenwise:report anytime
to see real per-tier spend.

To undo at any time: /tokenwise:undo
```

### Manual mode flow

Skip diff/confirm/write. Print:

```
Manual install — copy-paste these blocks yourself.

=== Block 1: append to ~/.claude/CLAUDE.md ===
<the routing block>

=== Block 2: merge into ~/.claude/settings.json ===
<the env block>

After pasting, restart Claude Code.
```

### Dry-run flow

Run the full guided flow, but replace every write step with:
```
DRY RUN: would write <file> (backup to <file>.tokenwise-backup-<ts>)
```
And every prompt with:
```
DRY RUN: would ask: Apply this change? [Y/n]
```

No files modified. Print at end:
```
Dry run complete. No files were modified.
Run /tokenwise:install (without --dry-run) to apply.
```

## Tools

You can use: Read, Write, Edit, Bash, Task.
