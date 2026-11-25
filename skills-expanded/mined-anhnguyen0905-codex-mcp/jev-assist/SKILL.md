---
name: jev-assist
description: Opt-in Jev decision assistance, off unless a TypeSafe key and CODEX_FLOW_JEV_MODE are set, shadow-mode-first.
---

# Jev Assist (opt-in appendix)

**Helpers**: required — none; optional — jev-client.mjs (scripts/jev-client.mjs; off/missing key is a silent no-op).

## Shared rules

- Opt in by loading this skill. `off` or a missing `TYPESAFE_API_KEY` is a silent no-op, never a hard error.
- Shadow mode only logs comparisons; Jev never overrides exclusions, changes review-feedback's severity levels, the 3-round cap, or the `codex_continue` escalation rule, or automates an approval.
- Before every call, perform the security-category pre-check. Never send content involving auth/session,
  user input, database queries, file paths, external API calls, crypto, payments, or secrets/env to Jev at all.
- Claude remains responsible for every final decision. Enforce mode ships inert — every point defaults to `shadow`/`off`, and loading this skill never enables it.

## Fast-path: Jev-assisted lane routing

Apply after the fast-path gate has read the task and confirmed that no absolute exclusion applies. Only when
`getJevMode()` (via `node scripts/jev-client.mjs ask ...`) is not `off`, call `askJev` with a Choice question
`lane` whose criteria are `analysis`, `small-change`, and `full-flow`, plus Noul questions `is_security_sensitive`
and `is_ambiguous`; set `state` to the task description. Jev is only a tie-breaker for genuinely non-excluded,
non-obviously-security-sensitive tasks.

- Absolute exclusions — security-sensitive, spans components/contracts, ambiguous, user-requested full-flow — always win.
- `lane.confidence < 0.6` means ignore Jev's suggestion and use Claude's normal reasoning.
- In `shadow` mode, after Claude's gate decision, run:

```text
node scripts/jev-client.mjs log --point fast-path-lane --jev '<jevAnswer>' --claude '<claudeDecision>'
```

- Continue with Claude's decision unchanged. Enforce mode is defined for completeness but ships inert.

## Skill selection: Jev-assisted relevance scoring

Apply after Claude checks every candidate for exclusion and scope. If clear and `getJevMode()` is not `off`, make
one batched `askJev` call scoring every cleared candidate (fan-out), 0–3, with `state` equal to the requirements;
never make one call per candidate.

- In shadow mode, run:

```text
node scripts/jev-client.mjs log --point skill-relevance --jev '<jevAnswer>' --claude '<claudeOrder>'
```

- Enforce mode is inert: Score 0 with confidence above 0.8 goes last.
- Never bypass full `SKILL.md` reading or the `LOAD`/`VET`/`AUTHOR` gate; Claude owns the final verdict.

## Dual review: Jev-assisted finding triage

Apply for each raw Claude or Codex finding before verification, after the security-category pre-check above. Include
only findings that pass it; never batch the full diff/context and filter afterward. For each included finding `<n>`,
add Score question `severity_<n>` with the 0–3 rubric and Noul questions `is_duplicate_<n>` and `is_in_scope_<n>`.
Claude may make one batched `askJev` call (fan-out), with `state` containing only included findings:

```text
node scripts/jev-client.mjs ask --point review-triage --json '<json>'
```

Jev is non-blocking when unavailable or disabled. It is additive metadata only. In shadow mode, after Claude's own
verified severity/duplicate/in-scope verdict for each finding, run:

```text
node scripts/jev-client.mjs log --point review-triage --jev '<jevAnswer>' --claude '<claudeVerdict>'
```

In enforce mode, annotate `pre-triaged` only when Jev severity confidence is greater than 0.85 and agrees with one
reviewer's initial severity. CRITICAL/HIGH findings still use the full 3-round verify+continue loop unchanged.

## Dual review: Jev-assisted root-cause classification

Apply when a finding needs implementation-bug-versus-plan-drift classification and passes the security pre-check.
When no security category is at stake, call `askJev` with a Choice question `root_cause` whose choices are
`implementation_bug`, `plan_drift`, and `ambiguous`, as advisory input for Phase 5 step 6. Claude makes the final
call and runs the existing plan-drift transaction unchanged.

## Improvement gate: Jev-assisted improvement prioritization

Apply to each pending improvement after Claude confirms its description does not quote code in a security category.
Skip Jev entirely for descriptions that fail that check; never call-then-filter. Eligible descriptions may be sent in
`state` for an optional Jev Score question (0–3, “worth a new task”), used only to order the summary presented via
AskUserQuestion. The user still approves or declines every item manually. In shadow mode, run:

```text
node scripts/jev-client.mjs log --point improvement-priority --jev '<jevAnswer>' --claude '<claudeVerdict>'
```

No approval, task creation, or ledger status changes are automated.
