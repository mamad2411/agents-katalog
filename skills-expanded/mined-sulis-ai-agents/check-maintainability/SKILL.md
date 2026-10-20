---
name: check-maintainability
description: "Checks whether the code will be easy to change later."
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
      standard_reference: "plugins/sulis/skills/codebase-assess/references/primitives.md CQ-05"
      scorer: generating_agent
      evidence_required: "Existing dead-code detection + CQ-05 review-practices hypothesis both have status"
related_skills:
  - relationship: depends_on
    skill: code-health
    notes: invoked as wired tier 6 (Evolves) in code-health orchestrator
  - relationship: depends_on
    skill: _lib/baseline
  - relationship: depends_on
    skill: _lib/allowlist
  - relationship: depends_on
    skill: _lib/scope
---

# Check Maintainability

The "can we change this later without breaking things?" check. v1 focuses
on **dead code detection** — symbols defined but never referenced.

Dead code accumulates silently. Each unused function is a place a future
contributor might modify thinking it's still in use, or a place a
refactor breaks something invisibly. Spotting it early is cheap; fixing
late is expensive.

## What this skill catches vs misses

| Catches (advisory) | Misses (out of scope) |
|---|---|
| Functions / classes never referenced elsewhere | Migration completion (deprecated API still used?) |
| Top-level imports never used | Surface drift (CLI ↔ SDK ↔ MCP) |
| Constants never read | Test quality beyond coverage |
| Module-level functions referenced only by themselves | Cyclomatic complexity hotspots |

**FP philosophy: advisory-default.** Dead-code detection has inherent
false positives (dynamic dispatch via `getattr()`, plugin systems, test
introspection, public API surface). ALL findings ship at `advisory`
severity — the founder reviews each before acting. No `high`/`concern`
verdicts.

## Two modes + three invocation modes

Same as sibling tier-skills. Founder default / `--raw` operator JSON.
Scope auto-detects PR vs codebase.

## When invoked

1. **Build reference graph.** Walk Python source files; record every
   defined symbol (function, class, top-level const, top-level import).
   For each defined symbol, count references in other files.
2. **Apply exemptions.** Skip dunder names, `__all__` exports,
   `if __name__ == "__main__":` blocks, `conftest.py` fixtures, plugin
   convention-loaded functions.
3. **Apply per-project allowlist** at
   `.checkup/{project}/check-maintainability-allowlist.md`.
4. **Compare to baseline** (`tier_6_findings` sub-key).
5. **Present verdict.** Founder template:

   ```
   📦 Maintainability check — {scope}

   Verdict: {clear / some dead code worth reviewing}

   ℹ Dead code (advisory) — 4 items
     • `apps/api/utils/legacy.py:42` — function `format_old_date` has
       no detected references. Consider removing if confirmed unused.
     • `apps/api/services/billing.py:7` — import `from datetime import
       timedelta` has no detected references. Likely safe to remove.
   ```

## Gotchas

- **Dynamic dispatch is invisible to static analysis.** `getattr(mod,
  name)`, `globals()[name]`, plugin-registration systems all reference
  functions by string. The scan will flag them as "unused" — false
  positive. Founder MUST review each finding before deleting.
  *Source: vulture / ts-prune universal limitation.*

- **Test introspection patterns hide usage.** pytest finds tests by
  name convention; fixtures by `@pytest.fixture`. The scan skips
  `tests/` and `conftest.py` to avoid auditing test infrastructure for
  "dead" code.
  *Source: pytest discovery convention.*

- **Plugin/skill systems load by convention.** Claude Code skills are
  loaded by SKILL.md discovery; agents by agent.md. Functions
  referenced from those files aren't visible to AST scan. v1 special-
  cases the marketplace's own `plugins/` tree.
  *Source: this marketplace's own discovery model.*

- **Public API surface looks unused if you're the library.** A function
  exported via `__all__` may have zero internal callers but many
  external ones. Scan skips `__all__` exports.
  *Source: Python packaging convention.*

- **Founder might expect this to DELETE dead code.** Universal read-
  only ambiguity. This skill identifies; deleting is separate
  engineering work (verify external usage, run tests, ship the diff).
  *Source: cross-skill pattern from check-readability / check-tests /
  check-build / check-security / check-reliability.*

## Vocabulary

- **maintainability** — umbrella property: "can we change this later
  without breaking things?" (Disambiguates from code-health's tier-
  name use of the same word.)
- **dead-code** — a symbol with no detected references elsewhere in
  the codebase.
- **unused-symbol** — singular noun for an individual finding
  (function / class / variable / import).
- **reference-graph** — the static-analysis graph of symbol-to-callers
  used to detect dead code.
- **advisory-severity** — the FP-philosophy lock: ALL findings ship as
  advisories; founder reviews before acting.

## When to invoke this skill

- Founder asks "any dead code?", "is the codebase getting bloated?",
  "anything I can delete?"
- After a refactor — catch orphaned helpers
- Code-health invokes at tier 6

## When NOT to invoke this skill

- Founder wants **deep code-quality analysis** (cyclomatic complexity
  hotspots, duplication, coupling metrics) — use
  `sulis-security:codebase-assess` (Code Quality category: CQ-01..05)
- Founder asks about test coverage / quality — that's a separate
  concern; v1 doesn't address
- Founder asks "are my APIs consistent?" / "is my SDK in sync with my
  CLI?" — surface-parity not covered; deferred to v1.1
- Founder wants the DELETION — this skill suggests; deletion is
  separate engineering work
