---
name: check-reliability
description: "Checks whether the code handles failure gracefully."
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  processing: [CRITICAL_THINKING_STANDARD, DECOMPOSITION_PROCEDURE]
  output: [CRITICAL_THINKING_STANDARD]
verification_spiral:
  tier: standard
  template_base: STANDARD_TIER_DEFAULT
  custom_dimensions:
    - name: "Primitive Coverage Completeness"
      threshold: ">= 4/5"
      standard_reference: "plugins/sulis/skills/codebase-assess/references/primitives.md INF-04 + DAT-05"
      scorer: generating_agent
      evidence_required: "Existing reliability patterns + INF-04 verbose-error + DAT-05 audit-logging hypothesis all have status"
related_skills:
  - relationship: depends_on
    skill: code-health
    notes: invoked as wired tier 4 (Survives) in code-health orchestrator
  - relationship: depends_on
    skill: _lib/baseline
  - relationship: depends_on
    skill: _lib/allowlist
  - relationship: depends_on
    skill: _lib/scope
  - relationship: depends_on
    skill: _lib/tools
  - relationship: depends_on
    skill: _lib/tools/semgrep
    notes: NEW — to be created — covers INF-04 verbose-error / debug-mode-in-prod
---

# Check Reliability

The "what happens when X fails?" check. Pattern-scans for three
high-confidence reliability issues:

1. **Missing timeout** — external calls (HTTP, subprocess, database)
   without an explicit time limit. By far the most common reliability
   bug. A request without a timeout will hang the calling process
   indefinitely when the upstream service stalls.
2. **Silent-except** — `try: ... except: pass` and
   `except Exception: pass`. Swallows errors invisibly; founder never
   learns something went wrong.
3. **Broad-except without re-raise** — `except Exception:` or naked
   `except:` that doesn't re-raise. Catches too much, hides bugs.

Pattern-based; designed for **low false-positive rate**, not exhaustive
coverage. For deep reliability analysis (chaos tests, data integrity,
distributed-systems patterns), use `sulis-security:codebase-assess`
(Armor pillar — 25 primitives, OODA-spiral).

## What this skill catches vs misses

| Catches (high confidence) | Misses (out of scope) |
|---|---|
| HTTP calls (requests/httpx) without `timeout=` | Async timeout primitives (asyncio.wait_for) — DETECTED differently |
| subprocess without `timeout=` | Custom timeout decorators (project-specific) |
| `try: ... except: pass` (silent swallow) | Errors logged but not re-raised when they should be |
| `except Exception:` without re-raise | Business-logic error-recovery decisions |
| | Chaos test coverage |
| | Distributed-system patterns (idempotency, retries, circuit breakers) |
| | Data integrity (flush/fsync) |

The misses category is what `sulis-security:codebase-assess` covers
(Armor pillar). Don't treat "check-reliability passed" as "fully
resilient."

## Two modes + three invocation modes

Same pattern as sibling tier-skills. Founder default + `--raw` operator
JSON. Scope auto-detects PR vs codebase (`--scope` / `--base-branch` /
`--pr-number` overrides).

## Allowlist

Per-project allowlist at `.checkup/{project}/check-reliability-allowlist.md`
for known-intentional patterns (a test that deliberately swallows
errors during teardown; a script that's meant to hang). Same format as
check-security: `signature: reason` (signatures contain `:`, so the
parser uses `rfind(': ')` for the reason separator).

Path-based allowlist pre-loaded:
- `tests/`, `__tests__/`, `_test.go`, `*.test.ts` — test code uses
  different reliability conventions
- `fixtures/`, `testdata/`, `mocks/` — intentional patterns
- `docs/examples/`, `node_modules/`, `.git/`, `vendor/`, `dist/`, `build/`

## When invoked

1. **Walk source files.** git ls-files filtered to Python / JS / TS / Go.
2. **Apply pattern catalogue.** Per file: regex + AST-lite pattern
   matching. Patterns are library-specific (different libraries have
   different timeout conventions).
3. **Apply allowlist.**
4. **Compare to baseline.** Same `.checkup/{project}/baseline.json`
   pattern; `tier_4_findings` sub-key.
5. **Present verdict.** Founder template:

   ```
   🛡 Reliability check — {scope}

   Verdict: {clear / missing timeouts / silent errors found}

   ⚠ External calls without time limits — 3
     • `apps/api/services/billing.py:42` — Stripe call won't time out
       if Stripe's API stalls. Add `timeout=30` (or similar).
     • `apps/api/services/email.py:78` — Sendgrid call won't time out.
       Add `timeout=10`.

   ⚠ Silent error swallowing — 1
     • `apps/api/utils/cache.py:33` — `except: pass` hides errors;
       founder won't see cache failures. Log the exception instead.

   Allowlisted: 0
   ```

## Gotchas

- **False positives in test code.** Tests intentionally use bare
  `except:` during teardown and intentionally skip timeouts because
  they run in-memory. Path allowlist skips `tests/`, `__tests__/`, etc.
  *Source: every static analysis tool's test-vs-prod problem.*

- **Async function timeouts look different.** `asyncio.wait_for(coro,
  timeout=N)` is the async timeout primitive, NOT a `timeout=` kwarg
  on the call itself. Pattern catalogue knows about `aiohttp` (uses
  `ClientSession.get(url, timeout=N)`) and detects `asyncio.wait_for`
  wrapping.
  *Source: author-experience — every "missing timeout" check that
  doesn't know about asyncio over-reports.*

- **Re-raising in except blocks is fine.** `try: ... except Exception:
  log.error(...); raise` is the canonical wrap pattern. Pattern
  catalogue scans the except body for `raise`, `raise X`, `reraise()`
  — if present, NOT flagged.
  *Source: idiomatic Python; documented in PEP 8 and Python docs.*

- **Founder might expect this to FIX missing timeouts.** Universal
  read-only audit ambiguity. This skill identifies; adding timeouts is
  a separate engineering action (deciding the right value per call
  site, handling timeout exceptions appropriately).
  *Source: cross-skill pattern from check-readability + check-tests +
  check-build + check-security.*

- **Tier 4 scope creep.** Reliability is enormous (chaos tests, data
  integrity, distributed systems). v1 sticks to timeouts + silent-
  except + broad-except. Anything more requires its own skill — don't
  let it grow.
  *Source: SEA's TDD tier 4 description; founder asks "is it resilient?"
  not "is it perfectly survivable?".*

## Vocabulary

- **reliability** — umbrella property: "does it handle failure?"
  (Disambiguates from code-health's tier-name use of the same word —
  same meaning, different layer.)
- **missing-timeout** — external call (HTTP / subprocess / DB) without
  an explicit time limit. The most common reliability bug across
  codebases.
- **silent-except** — `try: ... except: pass` or
  `except Exception: pass`. Swallows errors invisibly.
- **broad-except** — `except Exception:` or naked `except:` without
  re-raise. Catches too much; hides bugs.
- **observability-gap** — operation-shaped function with no logging.
  Deferred to v1.1 (too speculative for v1's low-FP target).
- **data-loss-risk** — writes without flush+fsync. Deferred to v1.1
  (too strict; many legitimate cases).

## When to invoke this skill

- Founder asks "is it resilient?", "what happens when X fails?",
  "could this hang?", "are errors being swallowed?"
- Before opening a PR — fast pass for the basics
- After dependency changes — catch newly-introduced unprotected calls
- Code-health invokes at tier 4

## When NOT to invoke this skill

- Founder wants **deep reliability audit** (chaos coverage, data
  integrity, distributed-systems patterns) — use
  `sulis-security:codebase-assess` (Armor pillar — 25 primitives,
  OODA-spiral)
- Founder asks "are the tests reliable?" — that's `check-tests` (tier 3)
- Founder asks "is the build reliable?" — that's `check-build` (tier 1)
- Founder wants the FIX — this skill reports; adding timeouts +
  proper error handling is separate engineering work
- Operator wants raw scanner output — use `--raw` mode or run
  `semgrep` / `bandit` / language-specific linters directly
