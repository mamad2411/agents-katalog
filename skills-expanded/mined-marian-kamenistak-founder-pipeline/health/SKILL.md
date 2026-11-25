---
name: health
description: "Use when the user says /health, /doctor, \"health check\", \"audit CLAUDE.md\", \"fix CLAUDE.md\", \"context bloat\", or wants a Claude project's setup audited: settings, hooks, MCP, CLAUDE.md size and consistency, duplicates, broken references, memory hygiene. Works on one project or every project under a named directory. `/founder-pipeline:founder` calls it at P1.S1 before the pipeline writes anything."
user-invocable: true
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, Agent
argument-hint: "[project path, or a parent directory to scan; empty = current project (cwd)]"
---

# Claude Project Health Check

Two layers, both required:

- **L0 harness** — the runtime that executes every session (settings, hooks, MCP, updates). Broken here, nothing else matters.
- **L1–L5 content** — the context loaded into every conversation (CLAUDE.md chain, references, memory).

## Input

- `$ARGUMENTS` empty — audit the current project. Walk up from cwd to the nearest project-root CLAUDE.md (the one whose parent directory does NOT itself contain a CLAUDE.md).
- `$ARGUMENTS` a path — audit that project.
- `$ARGUMENTS` a parent directory (or the word `all` plus a directory) — audit every CLAUDE.md underneath it. There is no default scan root: if the user says "all" without naming a directory, ask which one rather than guessing. Nothing in this skill assumes a particular folder layout, naming scheme, or where a user keeps their projects.

## Step 1 — Run the sweep

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/health/checks.sh" "<project-dir>"
```

This is the measurement. Do not re-invent it with ad-hoc greps — results must be comparable run to run. Read `checks.sh` before extending it. It is also the one place to adapt this skill to a project's own conventions: the L2 rule strings and the L1 line limits are constants at the top of the script.

It emits: L0 harness, L0b runtime, L1 line counts, L2 invariant-rule placement, L3 unresolved paths, L4 memory index, L5 systemic prompt.

## Step 2 — Adjudicate

The script measures; you judge. Rules:

### L0 Harness

`claude doctor` output is authoritative for install state. Escalate to BROKEN: failed auto-updates, missing hook scripts, invalid JSON, statusLine pointing at a missing file. Report as NOTE (not a defect): env vars with deliberate trade-offs — e.g. `DISABLE_TELEMETRY=1` disables feature-flag evaluation and therefore any feature gated behind it. That is a privacy choice, not a fault; state the trade-off and let the owner decide.

### L0b Runtime

Config being valid does not mean the harness is *behaving*. This layer catches hooks that run but never finish — invisible in `claude doctor`, invisible in a process monitor under their own name, and capable of taking the machine down within hours.

**`hook RUNAWAY` — BROKEN, always.** Hooks are sub-second by design. Seconds of CPU time or 30+ minutes of wall time means the hook is stuck or spinning. Do not dismiss it as "still working". Read the script it names, find the loop, fix the script — killing the process only clears today's copy.

**`hook PILEUP` — BROKEN.** Four or more concurrent instances of one hook script means each session-stop leaves a copy behind. The count grows through the day; that is why the machine is fine in the morning and frozen by mid-afternoon.

**`self-exec LOOP` — BROKEN, fix immediately.** A wrapper script whose `exec` line resolves to its own path spins forever, silently, at 100% of a core. The trap: a wrapper written to wrap a binary, then installed *at that binary's path*, so the target it names is now itself.

> Documented case, and the reason this check exists. A CLI tool was installed into a virtualenv as a pip console script. Someone then replaced that script, at the same path, with a hand-written shell wrapper that re-exec'd the same path to force a different CPU architecture — so the wrapper exec'd itself, forever. A session-stop hook called that wrapper, so **every stopped session pinned one core permanently**. Measured on a 10-core laptop after ~2 hours of uptime: 44,370 CPU-seconds burned, load average 19.6/24.6/31.8, wired memory climbing ~185 MB/min until it reached 12 GB of 16 GB, 13.6 GB of swap, and 90+ processes stuck in uninterruptible paging wait — including the window server and the file manager. The symptom as reported: "the machine freezes, I restart it twice a day." Nothing in `claude doctor` showed it. Fix: exec the *interpreter and module*, never the wrapper's own path — `exec <python> -m <module> "$@"` rather than `exec <the same path this script lives at>`.

The fix pattern is general: a re-exec wrapper must either target the interpreter plus module, or live at a different path from the thing it wraps. Editing the script terminates the running loops on their next exec cycle — no kill needed.

**`machine: ... <-- PRESSURE`** — report as context, not as a Claude-project defect, *unless* a RUNAWAY, PILEUP or self-exec LOOP is also present. Then it is the downstream symptom and the same finding, not a second one. Thresholds: load > 1.5× cores, wired > 50% of RAM, swap > 4 GB. High wired memory with no runaway hook is a different problem and outside this skill — say so rather than guessing.

Note: wired memory does not drain once leaked. After fixing the cause, one reboot is still needed to reclaim it — tell the owner that explicitly so the persisting slowness doesn't read as a failed fix.

### L1 Size

Each CLAUDE.md < 200 lines. Auto-loaded chain (global + project root) < 400 lines. A nested CLAUDE.md only loads when working in its subtree — count it against that subtree's chain, not the root's. Both limits are the script's defaults; a project with a genuinely larger loaded chain should change them at the top of `checks.sh` and say why, not quietly ignore the finding.

### L2 Invariant rules

A project's invariant rules — the standing instructions every session must load — must appear **exactly once in any loaded chain**, at the highest level that covers them. `checks.sh` ships with two defaults, matched by a distinctive substring each. Edit `L2_RULES` in the script to match the rules your projects actually declare.

> Do not make any changes until you have 95% confidence in what you need to build. Ask me follow-up questions until you reach that confidence.

> State your assumptions out loud. If the request is ambiguous, ask. If a simpler approach exists, push back. Stop when you are confused, name what is unclear, do not just pick one interpretation and run.

**Absent from the chain = BROKEN. Repeated inside one chain = DRIFT (duplication).** Do not "fix" a nested file by pasting the rule into it — the parent already loads. If N project roots carry identical copies, the fix is hoisting to the user's global agent instructions, if they keep any, not N edits.

(The first of the two is the rule `/founder-pipeline:founder` calls the Golden Rule and expects present at P1.S1. If a project has no CLAUDE.md at all, that is the finding — creating a minimal one is the founder run's job, not this skill's.)

### L3 Unresolved paths

Script output is **candidates, not findings**. Verify each before reporting: resolve it yourself, check whether it's a URL route, a shorthand for a path named nearby, or prose about a file that used to exist. Report only what you confirmed missing. Never edit a CLAUDE.md off an unverified L3 line.

### L4 Memory

Index matches files both ways. Valid frontmatter (name, description, type). No memory restating CLAUDE.md. Flag memories naming files/flags that no longer exist.

### L5 Systemic

Before filing a broken shared reference, grep the sibling projects. **If it appears in more than one project, it is one finding at the source, not one per project.** Fix the source or update all references in a single pass.

### Content checks the script cannot make

- **Single source of truth:** same rule, price, headline, or positioning line must exist in exactly one canonical place. Cross-check CLAUDE.md, mission/positioning docs, deck configs, pricing docs, web copy.
- **No contradictions:** conflicting prices, dates, partner tiers, people roles across assets.
- **No ambiguity:** vague instructions with multiple readings — rewrite to a specific number/name/date/action.
- **Stale content:** references to prices, partners, people, or features that have changed.
- **Index not inline:** flag inline blocks >20 lines that belong in a reference file; if a section is used <20% of sessions, it belongs in a skill.
- **Orphan rules:** scan recent memory and edits for "from now on…", "always…", "we decided…" not yet codified. Route each: project-wide rule → CLAUDE.md; multi-step procedure → skill; static reference → reference file; preference/context → memory.

## Step 3 — Report

```
## Claude Health Report: [project]
Date: [today]

### BROKEN (fix now)
- [issue + path + fix]

### DRIFT (fix when convenient)
- [issue + path]

### NOTE (deliberate trade-off, no action)
- [setting + consequence]

### CLEAN
- [X/Y checks passed]

### Context budget
- Chain: [N] lines (~[M] tokens) | Memory: [N] files (~[M] tokens)
- Verdict: [trim / healthy / restructure]
```

## Step 4 — Fix

Fix without asking (reversible, single correct answer):
- Missing invariant rule at the chain root
- Removing a duplicate copy from a nested file whose parent already carries it
- Orphaned memory file → add an index entry; dead index entry → remove
- Ambiguous wording with exactly one defensible resolution

Ask the owner first (judgment call — the 95%-confidence rule applies to this skill too):
- Any confirmed-broken reference to a **canonical source** (pricing, contacts, mission). Deleting the pointer and recreating the target are opposite fixes; you cannot tell which is right.
- Extracting inline content to reference files, or restructuring a CLAUDE.md
- Hoisting a rule to the user's global agent instructions (affects every project, not just this one)
- Resolving a contradiction between two sources (which is canonical?)
- Persisting an orphan rule (CLAUDE.md vs skill vs reference vs memory)
- Anything touching the user's global harness settings

## Red flags

| Thought | Reality |
|---|---|
| "Nested file lacks the invariant rule, I'll add it" | The parent loads. You just created duplication. |
| "L3 says missing, I'll delete the line" | L3 emits candidates. Verify, then ask if it's canonical. |
| "Same broken ref in 12 projects, 12 findings" | One finding at the source. |
| "`claude doctor` is a separate command" | It is L0 of this skill. Run it. |
| "I'll just grep instead of running checks.sh" | Then runs aren't comparable and you'll miss L0 entirely. |
