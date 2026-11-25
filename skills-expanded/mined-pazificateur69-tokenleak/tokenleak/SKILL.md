---
name: tokenleak
description: Token-lean working rules for coding agents. Cuts the context you re-pay on every later call (oversized file reads, unbounded test/build/install output, re-reads, serial round-trips, whole-file rewrites, recap prose) without trading away correctness. Use on any coding task that reads files, runs shell commands, tests, builds, git or searches a codebase, and whenever the user wants to save tokens, cut cost, stay under usage limits, or audit where their tokens went ("token leaks", "context tax", "why did this session cost so much").
license: MIT
---

# tokenleak

Every tool result you pull into context is re-sent on **every later call** until compaction. A 6k-token log read at call 5 of a 60-call session is paid ~55 more times. Every extra round-trip re-sends the whole context. Output costs ~5x input and joins the context too. So let in only what the next decision needs. Correctness first: a leak is cheaper than a wrong fix.

## Rules

1. **Locate, then read.** Don't know a file's size? Check it (`wc -l`) along with your first search. Search (`grep -n`, `rg -n`, Grep), then read only the region you need (offset/limit, `sed -n 'A,Bp'`). Read a whole file only if it is short (under ~300 lines) or you truly need all of it.
2. **Compute, don't read.** For questions about data (counts, totals, filters, lookups in big data files, CSV, JSON, logs), run a short script or one-liner that prints only the answer. Never pull the data itself into context.
3. **Bound every command.** Never let tests, builds, installs or logs stream into context unbounded.
   - Quiet or failures-only modes: `pytest -q -x`, `vitest run --reporter=dot`, `go test ./... 2>&1 | grep -v '^ok'`, `cargo test -q`, `npm ci --silent`, `make -s`.
   - Long jobs: `L="${TMPDIR:-/tmp}/out.log"; cmd > "$L" 2>&1; echo "exit=$?"; tail -n 40 "$L"`. Need more? `grep -n -m 20 -E 'error|FAIL|panic' "$L"` on the saved log. Never re-run a job just to see more of its output.
   - Iterate on the one failing test, not the whole suite. Run the full suite once at the end, quietly.
4. **Never re-read what you have.** A file you read or wrote is still in context. Re-read only after compaction or after something else changed it.
5. **Batch independent calls.** Reads and searches that don't depend on each other go in one turn (parallel tool calls), and shell steps that need no judgment in between go in one command (`wc -l a b; grep -n x a | head`). Each extra round-trip re-sends everything.
6. **Diffs over files.** `git status -s`, `git diff --stat` then `git diff -- <path>`, `git log --oneline -n 15`, `git show --stat <sha>`.
7. **Edit, don't rewrite.** Targeted edits only. Never rewrite a whole file to change a few lines, and never paste back into chat code that is already on disk.
8. **Narrow searches and fetches.** Scope by path and file type, cap results (`-m`, `head_limit`, `| head -n 30`, `-l` for names only). Pick fields from APIs and JSON (`--json a,b`, `jq '.items[] | {id,name}'`, `per_page`). Ask a web fetch a precise question instead of dumping the page.
9. **Delegate wide exploration.** If an answer means opening 10+ files and you only need the conclusion, hand it to a subagent if your agent has them. Only its summary enters your context.
10. **Answer lean.** Lead with the result. No step-by-step recap, no restating the diff, no closing summary of what the user can already see, no filler.

## Never save tokens by

- truncating so hard you miss the real error (widen with `grep`/`sed -n` on the saved log instead);
- skipping a read you need to edit correctly, or guessing file contents;
- skipping verification. Run the tests, quietly.

## Audit

When asked to audit tokens or find leaks, run `python3 scripts/tokenleak.py` from this skill's directory (Python 3.8+, no dependencies, local and read-only). Use `--current` for the session you are in, `--here` for the current project, `--since 30d` for a wider window, and `--compare <date>` to compare before and after a date. Report the leak score, the top 3 leak kinds, and the matching rule above. Then run `python3 scripts/tokenleak.py suggest` from the project folder: it turns this project's recurring leaks (its noisy test/build commands, its big files) into rules. Offer to add them to the project's `CLAUDE.md` or `AGENTS.md`; do not edit those files without the user's go-ahead.

If the report has a `context window` section, it replayed the user's own sessions with an earlier auto-compact and found it cheaper: in long sessions on a 1M-token window, everything stays in context (thinking included) and is re-sent on every call. Explain the trade-off (more compactions, each taking ~20-30 s; short sessions gain nothing) and offer to set it: `python3 scripts/tokenleak.py compact` shows the replay table, and `compact --apply` writes the recommended `autoCompactWindow` to `~/.claude/settings.json` with a backup (or point to `/config` → Auto-compact window). Never apply it without the user's go-ahead.
