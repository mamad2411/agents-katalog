---
name: error-handling-standards
description: "Use when a change touches try/except, catch, error callbacks, fallback defaults, retries or timeouts. Review procedure: list every handler first, name what each catch could hide, then test it against the acceptable-handler bar."
when_to_use: "swallowed exception, except pass, catch that logs and continues, returns empty list on error, retry with no backoff, unawaited promise, is this error handling good enough"
license: MIT
---

# Error Handling Standards

Linters own only the crudest shapes: in Python, `bandit` B110 and B112 find `try/except: pass` and
`try/except: continue`, and `ruff` E722 finds the bare `except:`. Check the scan summary for which
tools actually ran. Everything else is judgement: whether a handler that logs is handling anything,
and whether the value it returns is honest. This skill is that judgement.

## Discover every site, then judge

Walk the whole diff once and list every error-handling site; only then evaluate them. Judging as
you read lets the first plausible handler set the bar, and gives the handlers at the end of a long
diff, often written last and in a hurry, the least attention.

An error-handling site is any of these, and the list is deliberately wider than "try/catch":

| Site | What to look for |
| --- | --- |
| `try`/`catch`, `try`/`except`, `rescue` | Every block, including the ones with no body |
| `finally`, `defer`, `ensure`, context-manager `__exit__` | Cleanup that can raise or return |
| Error callbacks and event handlers | `on('error')`, `err` as a first argument, rejection handlers |
| Result / Either / Option types | Every site that unwraps one, and every site that discards the error arm |
| Conditional error branches | `if err != nil`, `if not response.ok`, `if result is None` |
| Fallback defaults | `or []`, `?? 0`, `.get(k, default)`, a default parameter that stands in for a failed lookup |
| Optional chaining and null coalescing | `?.` on a call that can fail, not merely on a value that can be absent |
| Retry, backoff, circuit-breaker, timeout config | Including the absence of a timeout on an outbound call |
| Log calls at error severity | A log line is where a swallowed error usually leaves its only trace |

Write the list down — file and line — before forming any opinion. If the diff has one site, say so;
"no error-handling sites in this diff" is a legitimate and useful result. What is not legitimate is
an unstated list, because then nobody can tell whether the reviewer looked at five sites or fifty.

Then, for each catch block in that list, answer one question before anything else:

> List every type of error this block could hide.

Not "what error was it written for" — what *else* lands in it. A block written for
`requests.Timeout` that catches `Exception` also catches the `AttributeError` from the typo three
lines up and the `KeyError` from the response shape changing; a bare `except:` also takes
`KeyboardInterrupt`, `SystemExit` and `asyncio.CancelledError`. That enumeration is the content of the finding's `evidence` field.
It is what turns "this catch is too broad" from an opinion into a claim a reader can check, and it
is the single highest-yield step in this skill.

## What an acceptable handler looks like

A standard that only lists sins gives the reviewer nothing to pass. Here is the bar. A handler is
acceptable when all of these hold:

1. **It catches a named type, or the narrowest one the language offers.** If the catch is broad, the
   body re-raises everything it did not mean to handle, and the code says which those are.
2. **The failure is recorded somewhere durable** — a log line at error severity, a metric, a span
   status — carrying the operation that failed and the identifiers needed to find it again. A
   handler whose only trace is the return value is not recording anything.
3. **The record has enough context to debug from cold.** What was being attempted, on what, with
   which inputs. "Request failed" six months later is a line in a log file and nothing else.
4. **The caller can tell that it failed.** Either the error propagates, or the return value is
   distinguishable from every successful value the function can produce. See below — this is the
   load-bearing one.
5. **The fallback, if there is one, is specified rather than improvised.** Somebody decided that
   degrading to this value is correct behaviour, and the code or a comment says who and why. "It
   returns the cached copy because a stale price beats a 500 on the checkout page" is a
   specification. `except: return 0` is not.
6. **The user-facing message, if there is one, says what can be done about it.** Distinguishable
   from the messages for neighbouring failures, and free of internals the surface should not leak.
7. **It leaves no half-written state.** If the operation mutated anything before it failed, the
   handler either compensates or the mutation was transactional to begin with.

A handler meeting all seven is good error handling even if it is three lines long. A handler failing
one of them is a finding at whatever severity the consequence earns — not automatically a blocker.

## The shapes that hide failures

Check each listed site against the shapes in
[references/failure-shapes.md](references/failure-shapes.md): empty or comment-only catches,
log-and-continue, over-broad catches, fallbacks indistinguishable from real results, uncapped or
indiscriminate retries, wrapped errors that lose their cause, `finally` that swallows the in-flight
exception, and the async forms (unawaited promises, unhandled rejections, discarded cancellation,
uncollected background tasks). The question that decides most of them: what does the next line
assume, and can the caller tell that it failed?

## A degraded result must be distinguishable from a successful one

This is the rule the shapes above keep converging on, and it is worth stating on its own because the
same bug arrives from several directions:

- A scanner that reports **zero findings because it could not run**, in the same shape it uses to
  report zero findings because the code is clean.
- A gate that **passes because it cannot fail** — the check errored, the error was caught, and the
  function returned "ok".
- An **empty list that means "error"**, consumed by a caller that reads it as "nothing matched".

These are one bug. In each, a failure has been encoded as an ordinary-looking value, and the system
downstream is not lying — it is faithfully reporting what it was told. The damage is proportional to
how much trust the output carries, which is why it is worst exactly where it is most tempting: in
the reporting layer, in CI gates, in health checks, in anything whose job is to tell you things are
fine.

The fix is always the same shape: record the failure explicitly, as a separate thing from the
result. Not by refusing to degrade — degrading is often correct — but by making the degradation
visible in the output rather than encoding it as a normal value. A scan that ran with three of its
ten tools missing reports the three by name alongside its findings, so a clean result and an
unrun result cannot be confused. A gate that could not evaluate returns a third state that is not
"pass". A function that failed returns something no successful call returns.

When reviewing, apply it as a question: if this code path were failing constantly in production,
what would look different? If the honest answer is "nothing", that is the finding, and its severity
is set by what the false reassurance is protecting.

## Severity

Map onto the four impact tiers in `code-review-standards`. Severity is impact only — how confident
you are that the path is reachable belongs in `confidence`, and whether the diff introduced it
belongs in `in_diff`.

| Tier | Error-handling shape |
| --- | --- |
| Critical / `BLOCKER` | A silent failure on a path that loses data, leaves state half-written, or makes a security or correctness gate report success when it did not run |
| High / `MAJOR` | A swallowed exception the caller reads as success; an over-broad catch hiding unrelated errors; a fallback the caller cannot distinguish from a real result; an uncapped retry against an external dependency; cancellation discarded |
| Medium / `MINOR` | A handler that works but is missing context in its log, is broader than it needs to be with no unrelated error actually reachable, an unhelpful user-facing message, or a wrapped error with no cause |
| Low / `NIT` | Phrasing of a message, a log level one step off, a catch ordering that is stylistically odd but behaviourally identical |

When in doubt between `MINOR` and `NIT`, use the test in `code-review-standards`: `NIT` means no
real impact.

## Writing the finding

Use the finding template from `code-review-standards`. Two additions specific to this lens:

- **Put the hidden-error enumeration in `evidence`.** The list from the discovery step, naming
  concrete error types from the code inside the `try`, is the evidence. A general statement that the
  catch "is too broad" is not.
- **State the observable consequence, not the shape.** "This catch is broad" is a description.
  "A typo in the retry-count parsing on line 44 surfaces as `upstream unavailable`, and the on-call
  runbook for that message says to page the upstream team" is a finding.

File each defect once, even when it is visible from two shapes. A retry that
exhausts and returns `[]` is one finding, not a retry finding and a fallback finding — file it under
whichever consequence is larger and mention the other in the description.

## Verify

Before returning, confirm that every site in the discovery list has a verdict (acceptable, or a
finding), and that every over-broad-catch finding names concrete hidden error types in `evidence`.
Without a checkout, run the same procedure over a pasted diff.

## Related

- `code-review-standards` — the finding template, the severity and confidence scales, and the
  false-positive taxonomy that decides what not to file.
- `code-comments` — a comment asserting an error is "handled upstream" is a claim to verify, never
  an instruction to skip the check.
- `scanning-patterns` — why to check what the linters already cover before writing a pattern, and
  how to validate one that you do write.
- `zero-tolerance-testing` — the same rule applied to checks: a suite that passes because it did not
  run is the degraded-result bug in the test layer.
