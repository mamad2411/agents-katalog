---
name: no-swallow
description: "MANDATORY before declaring code \"done\", \"ready\", or ending a turn after writing or editing anything with a try/catch, except, or error path. Use whenever you wrapped something in a handler and left the body empty — `except: pass`, `except Exception: pass`, `catch (e) {}`, `catch {}`, `.catch(() => {})`, `.catch(() => null)`, an empty `if err != nil {}` in Go. Forces you to handle the error, log it, re-raise it, or return a real fallback instead of silently swallowing it. Triggers on \"just catch it for now\", \"ignore the error\", \"swallow it\", \"catch and move on\", \"wrap it in a try so it doesn't crash\", \"empty catch\", \"best-effort\", \"I'll handle it later\"."
---

# No Swallow

**A caught error you do nothing with is a bug that hides itself.**

`except: pass` and `catch (e) {}` don't make the failure go away — they make it invisible. The operation still failed; you just deleted the evidence. The next person debugging a wrong result, a missing row, a half-written file has no log line, no stack trace, no signal at all. The model reaches for the empty handler constantly to make a red squiggle or a crash disappear.

## The rule

> **Never swallow a caught error.** Every `except`/`catch` does ONE of four real things: handle it, log it, re-raise it, or return a real fallback. An empty body is not one of them.

## What counts as swallowing

- **Python:** `except: pass`, `except SomeError: pass`, or a multi-line `except` whose body is only `pass` / `...` / `continue` / `break`. Bare `except:` (catch-all) is worse — it swallows everything, including bugs you didn't anticipate.
- **JS/TS:** `catch (e) {}`, `catch {}`, `catch (e) { }`; promise `.catch(() => {})`, `.catch(() => null)`, `.catch(() => undefined)`, `.catch(function(){})`.
- **Java / Kotlin / C# / C++ / Swift:** an empty `catch (...) {}`; Swift bare `catch {}`.
- **Go:** `if err != nil {` immediately followed by `}` — the error is checked and then thrown away.

## What is NOT swallowing (don't change these)

- An `except`/`catch` that **logs** (`logger.error`, `console.error`, `print`), **re-raises** (`raise`, `throw`, `rethrow`), **returns** a value, **sets a variable / error state** (`setError(e)`), or **calls a real handler** (`.catch(handleError)`, `.catch(err => setError(err))`).
- `except ... : raise` / `catch (e) { throw e }` — re-raising is handling.
- `except ImportError:` with a real **fallback import** in the body — that's a deliberate compatibility path doing work.
- Swift `try?` (optional-try) — that's a language idiom for "give me nil on failure," not an empty handler. Never flagged.

The gate already knows the difference — a body that logs, raises, returns, assigns, or calls anything meaningful passes untouched.

## Step 1 — Find every handler you added this turn

Re-read your diff for the `try`/`except`/`catch`/`if err != nil` you wrote. For each, ask: **if this fires, what actually happens?** If the answer is "nothing," it's a swallow.

## Step 2 — Pick one of the four real outcomes

- **Handle it** — do the actual recovery (retry, use a default, fall back to another path) and make that explicit.
- **Log it** — at minimum, record it with the project's logger at the right level (`logger.error(e)`, `console.error(e)`), so the failure is visible.
- **Re-raise it** — if this layer can't deal with it, `raise` / `throw` so a layer that can does.
- **Return a real fallback** — return a sensible default *and* (usually) log why, so the caller isn't silently handed a wrong value.

`pass` is none of these. A comment explaining why you're ignoring it is still not handling it.

## Step 3 — Genuinely intentional swallows are allowed, but only out loud

Sometimes a best-effort cleanup *should* be swallowed (closing a socket that may already be closed, deleting a temp file that may already be gone). That's a decision — declare it:

```
NO-SWALLOW: INTENTIONAL — best-effort temp-file cleanup; failure is irrelevant here
NO-SWALLOW: INTENTIONAL — optional cache warm; a miss is fine, real path re-fetches
```

The Stop hook scans code you edited this turn for swallowed handlers and blocks the turn unless each is handled or you've recorded that line.

## Avoiding false alarms

The gate is deliberately conservative and **fails open** — error swallowing is harder to detect than a stray `console.log`, so when a body is ambiguous it passes. It only flags a handler whose body is genuinely empty (or comments only) with nothing that logs, raises, returns, or acts. `try?`, fallback imports, and any real statement in the body are safe.

## Kill switch

False positive (the gate misread a handler that does real work): `touch .no-swallow-off` in the project root, or `export NO_SWALLOW_GATE=off`.

## Pairs with

- **`no-stub`** — an empty handler is a stub of error handling; this is the same bar for the failure path.
- **`no-debug`** — strip the debug print, but keep (and promote) the real error log; a swallowed error is the opposite mistake.
- **`verify-before-done`** — once errors surface instead of hiding, run the code and prove the real path holds.
