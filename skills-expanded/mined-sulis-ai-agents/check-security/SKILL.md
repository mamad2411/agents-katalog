---
name: check-security
description: "Checks whether anything in the code could harm users or the business."
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  processing: [CRITICAL_THINKING_STANDARD, DECOMPOSITION_PROCEDURE]
  output: [CRITICAL_THINKING_STANDARD]
verification_spiral:
  tier: heavy
  template_base: HEAVY_TIER_DEFAULT
  custom_dimensions:
    - name: "Primitive Coverage Completeness"
      threshold: ">= 4/5"
      standard_reference: "plugins/sulis/skills/codebase-assess/references/primitives.md SEC/DAT/SC categories"
      scorer: generating_agent
      evidence_required: "Each of SEC-01..07 + DAT-01..05 + SC-01..04 (+ DAT-02 + INF-03 when --url) has a status: PASS / ADVISORY / CONCERN / CRITICAL / HYPOTHESIS / NOT_ASSESSED"
    - name: "Tool Degradation Verified"
      threshold: ">= 4/5"
      standard_reference: "plugins/sulis/_lib/tools/REFERENCE.md degradation policy"
      scorer: generating_agent
      evidence_required: "With Docker stopped AND native binary absent, each tool reports NOT_ASSESSED (never silent regex fallback)"
related_skills:
  - relationship: depends_on
    skill: code-health
    notes: invoked as wired tier 2 (Safe) in code-health orchestrator
  - relationship: depends_on
    skill: _lib/baseline
    notes: shared baseline-aware regression detection
  - relationship: depends_on
    skill: _lib/allowlist
    notes: shared per-project + per-skill allowlist loading
  - relationship: depends_on
    skill: _lib/scope
    notes: shared PR-vs-codebase scope auto-detection
  - relationship: depends_on
    skill: _lib/tools
    notes: shared tool-integration foundation (detection + degradation)
  - relationship: depends_on
    skill: _lib/tools/semgrep
    notes: NEW — to be created — covers SEC-01 / SEC-03..06 / DAT-03 / INF-04
  - relationship: depends_on
    skill: _lib/tools/gitleaks
    notes: NEW — to be created — covers SEC-07 (git history) / DAT-04 / INF-02
  - relationship: depends_on
    skill: _lib/tools/trivy
    notes: NEW — to be created — covers SC-01..04 / INF-01 base image
  - relationship: optional_input
    skill: _lib/tools/testssl
    notes: NEW — to be created — covers DAT-02 when --url provided
  - relationship: optional_input
    skill: _lib/tools/curl_probe
    notes: NEW — to be created — covers INF-03 when --url provided
  - relationship: supersedes
    skill: plugins/sulis/skills/codebase-assess
    notes: scheduled for Phase 5 retirement after Phase 4 cross-validation
---

# Check Security

The fast security pass. Scans for:

1. **Credential leaks** — hardcoded API keys, tokens, passwords matching
   high-confidence patterns (AWS, GitHub, Slack, Stripe, OpenAI, generic
   high-entropy strings near suspicious keywords)
2. **Dangerous code patterns** — `eval()` / `exec()` on user input,
   `subprocess(shell=True)` with formatted strings, SQL string
   concatenation patterns, `dangerouslySetInnerHTML` in React, etc.

Pattern-based; designed for **low false-positive rate**, not exhaustive
coverage. For deeper security analysis (25 primitives, OODA-spiral),
use `sulis-security:codebase-assess`.

## What this skill catches vs misses

| Catches (high confidence) | Misses (out of scope) |
|---|---|
| Hardcoded AWS / GitHub / Stripe / Slack / OpenAI keys | Auth-bypass logic errors |
| `eval(user_input)` patterns | Race conditions |
| Subprocess shell injection | Business-logic flaws |
| SQL string concatenation (heuristic) | Cross-tenant data leaks |
| React XSS via dangerouslySetInnerHTML | Missing rate-limiting |

The misses category is what `sulis-security:codebase-assess` is for. Don't
treat "check-security passed" as "fully secure."

## Two modes + three invocation modes

Standard sibling pattern: founder default / `--raw` operator JSON;
scan-only (default) / `--baseline-update` (capture current as new baseline) /
explicit invocation with --pr-number for remote PRs.

## Allowlist

Patterns inevitably produce some false positives. Two allowlists:

- **Path allowlist** — fixture directories, test data, doc examples are
  intentional. Pre-loaded with common fixture patterns.
- **Per-finding allowlist** — `.checkup/{project}/security-allowlist.md`
  for project-specific waivers (a "this is a public demo key, ignore it"
  per-finding override).

Allowlist additions require explicit founder action (never auto-add).

## When invoked

1. **Walk source files.** Skip fixture paths, test data, docs/, build
   artifacts, node_modules, .git, etc.
2. **Apply pattern catalogue.** Per file: regex-scan for known secret
   patterns; AST-scan (where supported) for dangerous-pattern matches.
3. **Apply allowlist** to each finding.
4. **Compare to baseline.** Same `.checkup/{project}/baseline.json`
   pattern as check-tests; `tier_2_findings` sub-key. Report newly-found
   security findings as regressions.
5. **Present verdict.** Founder template:

   ```
   🔒 Security check — {scope}

   Verdict: {clear / found credentials / found dangerous patterns}

   ⚠ Likely-leaked credentials — 1
     • `apps/api/src/config.py:42` — looks like an AWS access key.
       To investigate: rotate the key, then remove from git history.

   ⚠ Dangerous code patterns — 0

   Allowlisted (intentional patterns): 3
     • Test fixtures with sample keys (paths listed in --raw)
   ```

## Gotchas

- **Security false positives are scary.** A founder seeing
  "AWS key leaked" panics — even when it's a false positive. v1 scope
  kept narrow (high-confidence patterns only) to minimise FP rate.
  *Source: HD-013 + sulis-security tier 2 known issues.*

- **Test fixture credentials look like real leaks.** Fixture files
  (`tests/fixtures/`, `testdata/`, `mocks/`) often contain fake
  credentials for testing. Allowlist these paths by default.
  *Source: check-readability hit this exact pattern with `leaked_key.py`
  in the polyglot monorepo fixture.*

- **Pattern-based security is incomplete by design.** This skill
  catches low-hanging fruit. Sophisticated vulnerabilities (auth-bypass,
  race conditions, business-logic flaws) need a deeper tool —
  `sulis-security:codebase-assess` (25 primitives, OODA-spiral). Don't
  treat "check-security clear" as "fully secure."
  *Source: every static-analysis tool's perennial limitation.*

- **First-run has no baseline.** Same as check-tests / check-build.
  First run captures + says so explicitly.

- **Founder might expect this to FIX leaks.** Universal read-only
  ambiguity. This skill identifies; rotation + removal-from-history
  is separate engineering work.
  *Source: cross-skill pattern from sibling tier-skills.*

## Vocabulary

- **credential-leak** — a string matching a high-confidence credential
  pattern (AWS, GitHub, etc.) AND not on the allowlist.
- **dangerous-pattern** — code construct with known security risk
  (eval / exec / shell injection / SQL string concat / DOM-based XSS).
- **security-finding** — generic term for any finding from this skill.
- **high-entropy-string** — a string whose Shannon entropy is above
  a threshold (default 4.5 bits/char), typically indicating a key or
  token. Heuristic — used carefully because plain English text can
  occasionally trigger it.
- **secret-pattern** — a regex matching a specific known credential
  format (`^AKIA[0-9A-Z]{16}$`, `^ghp_[A-Za-z0-9]{36}$`, etc.).
  Opposite end of FP spectrum from entropy heuristics.

## When to invoke this skill

- Founder asks "is the code secure?", "any leaked credentials?",
  "did I expose anything sensitive?"
- Before opening a PR — fast pass for obvious issues
- After dependency changes — catch newly-added secrets
- Code-health invokes at tier 2 (foundational — safety before
  legibility)

## When NOT to invoke this skill

- Founder wants a **thorough security audit** — use
  `sulis-security:codebase-assess` (25 primitives, OODA-spiral,
  deeper coverage)
- Founder asks "is my auth logic correct?" — pattern-scanning can't
  verify business-logic correctness; this needs human review or
  `sulis-security:codebase-assess`
- Founder wants the FIX — this skill reports leaked secrets; rotating
  + removing-from-history is a separate engineering action
- Operator wants raw scanner output — use `--raw` mode or run more
  comprehensive tools (`semgrep`, `bandit`, `gitleaks`) directly
