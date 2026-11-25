---
name: check-polish
description: "Checks whether the project feels finished and professional."
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  processing: [CRITICAL_THINKING_STANDARD]
  output: [CRITICAL_THINKING_STANDARD]
verification_spiral:
  tier: standard
  template_base: STANDARD_TIER_DEFAULT
  custom_dimensions:
    - name: "CQ-04 Canonical Ownership"
      threshold: ">= 4/5"
      standard_reference: "plugins/sulis/skills/codebase-assess/references/primitives.md CQ-04"
      scorer: generating_agent
      evidence_required: "Existing TD-001 + TD-002 patterns + this skill is the canonical CQ-04 owner; codebase-assess defers here post-Phase 5"
related_skills:
  - relationship: depends_on
    skill: code-health
    notes: invoked as wired tier 7 (Polished) in code-health orchestrator
  - relationship: depends_on
    skill: _lib/baseline
  - relationship: depends_on
    skill: _lib/allowlist
  - relationship: depends_on
    skill: _lib/scope
  - relationship: supersedes
    skill: plugins/sulis/skills/codebase-assess
    notes: CQ-04 ownership transfers here post-Phase 5
---

# Check Polish

The "does this feel professional?" check. v1 ships a narrow tier-7
focused on documentation completeness, tech-debt-marker density, and
basic file hygiene.

**Scope is narrower than SEA's original TDD tier-7 vision.** The
broader tier-7 concerns (performance budgets, accessibility standards,
UX consistency) require upstream design work — which performance
threshold? which a11y standard (WCAG 2.1 AA, AAA)? what UX system?
Deferred to a future version when the founder has answered those.

## What this skill catches vs misses

| Catches (advisory mostly) | Misses (deferred) |
|---|---|
| Plugin missing README.md | Performance budgets |
| Plugin missing CHANGELOG.md (if >1 version shipped) | Accessibility audits (WCAG) |
| Plugin missing LICENSE | UX consistency / design-system adherence |
| TODO/FIXME/HACK density >5% of comments | API documentation completeness |
| Trailing whitespace in source files | Translation / localisation completeness |
| Mixed line endings (CRLF + LF in same file) | SEO / metadata completeness |

For the deferred concerns: founder picks the standard first (which a11y
spec? which perf budget?), then a dedicated skill ships in a future
version.

## Two modes + per-plugin scope

Same as sibling tier-skills. Founder default / `--raw` operator JSON.

**Per-plugin scope.** Each `plugins/*/` directory is audited as a unit
(does it have README + CHANGELOG + LICENSE in the expected places?).
Per-file checks (trailing whitespace, line endings, TODO density) run
across all source files in scope.

## When invoked

1. **Walk source files + plugin directories.**
2. **Apply rule catalogue.** Documentation completeness per plugin;
   per-file hygiene rules across source files.
3. **Apply allowlist.** Per-project at
   `.checkup/{project}/check-polish-allowlist.md`.
4. **Compare to baseline** (`tier_7_findings` sub-key).
5. **Present verdict.**

   ```
   ✨ Polish check — {scope}

   Verdict: {clear / a few polish items / many polish items}

   📚 Documentation gaps — 2
     • Plugin `sulis-platform-sdk` has no README.md.
     • Plugin `sulis-builder` has no CHANGELOG.md but has shipped
       multiple versions.

   📝 Tech-debt density — 1
     • `plugins/sea/scripts/probe/runner.py` has 23 TODO markers
       across 89 comment lines (26%) — high concentration.

   🧹 File hygiene — 0
   ```

## Gotchas

- **Polish is opinionated; v1 scope is narrow.** SEA's TDD specified
  perf/a11y/UX. Those need upstream design work first. v1 ships the
  basics (docs + tech-debt + hygiene). Founders expecting perf/a11y
  reports won't find them here — documented in "What this skill
  catches vs misses."
  *Source: SEA TDD ADR-006 deferral.*

- **Tech-debt markers aren't bugs.** Some projects use TODO as
  intentional future-work tracking. v1 only flags HIGH density (>5%
  of comments). Below threshold = OK.
  *Source: every linter's known limit on TODO interpretation.*

- **Missing README on legacy plugins isn't a regression.** Pre-existing
  plugins without README ship as `concern` severity (not `high`) so
  founders don't see catastrophic failure on old work.
  *Source: HD-004 incomplete cleanup — same pattern.*

- **Line-ending mix is often legitimate** in cross-platform projects.
  v1: advisory only. Configure `.gitattributes` to fix at commit time.
  *Source: cross-platform development reality.*

- **Founder might expect this to FIX polish.** Universal read-only
  ambiguity. This skill identifies missing READMEs and tech-debt
  density; writing the README + cleaning TODOs is separate work.
  *Source: cross-skill pattern from all check-* siblings.*

## Vocabulary

- **polish** — umbrella property: "does the project feel professional
  and complete?"
- **docs-completeness** — has README + CHANGELOG + (where applicable)
  LICENSE + plugin.json keywords.
- **tech-debt-marker** — TODO / FIXME / HACK / XXX / TEMPORARY /
  WORKAROUND comment.
- **trailing-whitespace** — lines ending in spaces/tabs.
- **line-ending-mix** — files containing both CRLF and LF, or CRLF in
  a primarily-LF project.

## When to invoke this skill

- Founder asks "does this look professional?", "what's the codebase
  missing?", "is documentation complete?", "anything that looks
  amateurish?"
- Before open-sourcing or external review — polish pass
- Before onboarding a new contributor — make sure docs exist
- Code-health invokes at tier 7

## When NOT to invoke this skill

- Founder asks about **performance**, **accessibility**, or **UX
  consistency** — v1 doesn't cover these (deferred — need upstream
  design choice first)
- Founder asks "is my README good?" (quality, not presence) — that's
  a different check
- Founder wants the FIX — this skill identifies; writing READMEs +
  cleaning TODOs is separate engineering work
