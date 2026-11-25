---
name: loud-errors
description: "Use when an error is swallowed, vague, or loses its cause — an empty catch, `except: pass`, log-and-continue, `throw new Error(\"something went wrong\")`. Makes each failure say what operation failed, with which inputs, and what the caller should do. Use when reviewing AI-generated code or debugging a failure that left no trace."
---

# Loud Errors

## The failure mode this fixes

The worst error is the one you can't see. Code that swallows failures — `catch {}`, `except: pass`, an error logged at `debug` and then execution continues as if nothing happened — turns a clean crash into a silent corruption that surfaces hours later, somewhere else, with no trace back to the cause. The second-worst is the error that *is* loud but says nothing: `throw new Error("something went wrong")` tells the on-call engineer at 3am exactly nothing.

Agents are especially prone to both. They're optimizing for "make the happy path run," so they wrap risky calls in a `try` that quietly eats the failure, or they emit a generic message to satisfy a linter. The result is code that *looks* defensive and is actually blind.

This skill does the opposite of defensive-by-swallowing: it makes failures **loud** (they stop the wrong thing from continuing) and **specific** (they carry enough context to diagnose without a debugger).

## When to Use This Skill

- You see an empty or near-empty catch: `catch (e) {}`, `except: pass`, `catch { return null }`, `rescue nil`
- An error is logged and then execution continues as if it succeeded
- A thrown/raised error is generic: `"something went wrong"`, `"error"`, `"failed"`, a bare re-throw with no context
- A caught exception is replaced by a new one that drops the original cause
- You're reviewing AI-generated code and want to find where failures will be invisible
- A real incident left no useful trace and you're hunting for where the signal got eaten

**Don't use when:** the swallow is *deliberate and correct* — a genuinely optional operation (best-effort cache warm, telemetry that must never break the request), a documented retry/fallback, or a control-flow exception in a language that uses them idiomatically. In those cases the rule is not "make it loud," it's "make the *intent to swallow* explicit" (see step 4). Don't turn an intentional fallback into a crash.

## Instructions

### 1. Find where failures disappear

Scan the target scope for the swallow patterns:
- **Empty / nullifying catches** — `catch {}`, `except: pass`, `catch { return null }`, `.catch(() => {})`
- **Log-and-continue** — the error is logged but the function proceeds as if it succeeded, returning a default or partial result
- **Swallowed at the boundary** — a top-level handler that catches everything and returns `200 OK` / a generic page
- **Cause-dropping** — `catch (e) { throw new Error("failed") }` that discards `e`
- **Vague throws** — messages with no operation, no inputs, no actionable next step

### 2. Decide the right response for each (don't reflexively re-throw)

For each swallowed failure, classify the *intended* behavior:
- **Must fail** — the operation can't meaningfully continue → let it propagate, or throw with context. Most swallows are secretly this.
- **Must fail here, differently** — translate to a domain error the caller understands (`PaymentDeclined`, not a raw `StripeError`), but **keep the original as the cause** (`throw new X(..., { cause: e })`, `raise X from e`).
- **Genuinely optional** — the failure truly doesn't affect the result → keep swallowing, but make it explicit (step 4).

### 3. Make the message specific and actionable

A good error answers three questions without a debugger:
- **What operation failed?** ("charging card", not "error")
- **With what inputs / identifiers?** (the order id, the user id, the file path — **never** secrets, tokens, raw PII)
- **What should happen next?** (is it retryable? a bad input? a bug?)

> Bad: `throw new Error("failed")`
> Good: `throw new Error(\`charge failed for order \${orderId}: gateway rejected (retryable)\`, { cause: err })`

Preserve the original cause every time you wrap. A new error that drops the stack trace is just a different way of swallowing.

**Report once, at the boundary that owns the response.** Intermediate layers add context by wrapping with `cause` — they don't log. A failure that appears five times in the logs as it bubbles up is noise the on-call engineer has to dedupe by hand; loud means *visible once with full context*, not echoed at every layer.

### 4. Make any *intentional* swallow explicit

If a failure really should be ignored, it must say so on purpose — so the next reader (and the next agent) knows it's a decision, not an accident:
- Catch the **specific** type you mean to ignore, not the catch-all
- Leave a one-line "why" (`// best-effort; a cold cache is fine`)
- Still record it where it can be seen (debug log / metric), just don't fail the caller

### 5. Fail fast at the boundary

Validate and reject bad inputs at the edge (where the request, file, or message enters) — the closer the error surfaces to its cause, the cheaper it is to diagnose.

### 6. Verify the failure is now visible

For at least the highest-risk path, confirm the new behavior: trigger (or reason through) the failure and check that it surfaces with its context — a test that asserts the error is thrown with the right message/cause is the proof. If conventions are recorded in `CONTEXT.md` (error-handling style: exceptions vs result types vs error returns), match them rather than imposing a new pattern.

## Output format

```
SWALLOWED / VAGUE FAILURES
  - <location> @ <file:line> — pattern: <empty catch / log-and-continue / cause-dropped / vague throw>
    intended: <must-fail | translate-with-cause | genuinely-optional>
    fix: <propagate | specific message + cause | explicit intentional swallow>

PROPOSED MESSAGES (before -> after)
  - "failed"  ->  "charge failed for order {orderId}: gateway rejected (retryable)"

INTENTIONAL SWALLOWS (kept, now explicit)
  - <location> — why it's safe to ignore: <reason>

PROOF
  <a test asserting the error surfaces with its context, or the path you verified>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| `catch (e) {}` / `except: pass` | The failure becomes invisible; corruption surfaces later, elsewhere, untraceable. |
| Catch-all that swallows everything | You meant to ignore one thing and silenced a hundred — including the bug you'll spend a day hunting. |
| `throw new Error("failed")` | Loud but useless. No operation, no input, no next step — the on-call engineer learns nothing. |
| Wrapping that drops the cause | A new error with no `cause`/original stack is just swallowing with extra steps. |
| Logging secrets/PII into the message | An error you can't paste into a ticket is a new problem, not a fix. Identifiers, never secrets. |
| Making an intentional fallback crash | Best-effort work (cache, telemetry) must *not* fail the request. Make the swallow explicit, don't remove it. |
| Catch-log-rethrow at every layer | The same failure shows up five times in the logs. Wrap with `cause` as it bubbles; log once, at the boundary. |

## Mental Model

> A swallowed error is a bug you've agreed not to find out about. Make failures loud enough to notice and specific enough to fix — and if you really must ignore one, say so on purpose.
