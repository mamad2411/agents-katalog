---
name: no-debug
description: MANDATORY before declaring code "done", "ready", or ending a turn after writing or debugging a function/handler/module. Use whenever you added a debug print while working something out — console.log, debugger, pdb.set_trace(), breakpoint(), binding.pry, byebug, dd()/var_dump()/print_r(), dbg!(), a "print('here')" or "console.log('DEBUG', x)". Forces you to strip the debug noise before shipping, and to reach for a real logger when you actually need persistent logs. Triggers on "let me add a log to see", "just debugging", "temporary print", "I'll remove this later", "console.log to check", "drop a breakpoint".
---

# No Debug

**A `console.log("here")` is how you debugged it, not how it ships.**

The prints, breakpoints, and dumps you scatter while working something out are scaffolding for *you*. Left in, they leak internals to stdout, slow hot paths, clutter logs, and tell the next reader "this was never cleaned up." The model adds them constantly and forgets them just as often.

## The rule

> **Strip debug noise before "done."** Every debug print, breakpoint, and dump you added to work the problem out comes back out — or becomes a real log line, deliberately.

## What counts as debug noise

- **JS/TS:** `console.log(` / `console.debug(` / `console.trace(` / `console.dir(`, `debugger;`
- **Python:** `pdb.set_trace()`, `breakpoint()`, `import pdb` / `import ipdb`, `ipdb.set_trace()`, and a `print(...)` whose content is a debug marker (`print("DEBUG", x)`, `print("here")`)
- **Ruby:** `binding.pry`, `binding.irb`, `byebug`
- **PHP/Laravel:** `var_dump(`, `print_r(`, `dd(`, `dump(`, `error_log(`
- **Go:** a leftover `fmt.Println(` / `fmt.Printf(` that's clearly a debug trace (`DEBUG`/`here`/`XXX`)
- **Rust:** `dbg!(`, a debug-ish `eprintln!(`
- **Java/Kotlin:** a debug-ish `System.out.println(`

## What is NOT debug noise (don't strip these)

- `console.error(` / `console.warn(` — that's legitimate error/warn reporting
- A real logger: `logger.info(...)`, `log.warn(...)`, `logging.getLogger(...)`, `winston`, `pino`, `slog`, `Log.d(...)`
- A genuine CLI/script `print(...)` that's part of the program's output (prompts, results, `--help` text)

The gate already knows the difference — it leaves `console.error`/`console.warn`, real loggers, commented-out lines, and bare CLI prints alone.

## Step 1 — When you finish debugging, sweep what you added

Every print/breakpoint you dropped to watch a value go through is now answered. Re-read your own diff for this turn and find them.

## Step 2 — Decide: delete, or promote to a real log

- **You added it to see one value once?** Delete it. It did its job.
- **You actually want this logged in production?** Don't ship `console.log` — use the project's logger at the right level (`logger.info` / `log.warn` / `console.error` for genuine errors). A real logger is filterable, levelled, and routable; a stray `console.log` is none of those.

## Step 3 — Intentional prints are allowed, but only out loud

A CLI tool, a build script, a one-off utility — these legitimately print to stdout. That's fine, but make it a *decision*, not a leftover. Declare it:

```
NO-DEBUG: INTENTIONAL — CLI entrypoint; prints results to stdout by design
NO-DEBUG: INTENTIONAL — migration script; progress output is the UX
```

The Stop hook scans code you edited this turn for debug markers and blocks the turn unless it's clean or you've recorded that line.

## Avoiding false alarms

The gate is conservative by design: it never flags `console.error`/`console.warn`, never flags a recognised logger, never flags a commented-out line, and only flags an ambiguous `print` / `fmt.Println` / `System.out.println` when the line also carries debug-ish content (`DEBUG`, `here`, `===`, an emoji). A bare `print("Enter name:")` in a CLI passes untouched.

## Kill switch

False positive (a CLI that prints by design, a print the gate misread): `touch .no-debug-off` in the project root, or `export NO_DEBUG_GATE=off`.

## Pairs with

- **`no-stub`** — the same gate for half-written code; debug-free *and* stub-free is the bar.
- **`secret-guard`** — a `console.log(token)` is also how secrets leak; strip the log, keep the secret out.
- **`verify-before-done`** — once the noise is gone, prove the real code still runs.
