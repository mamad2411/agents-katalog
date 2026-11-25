---
name: cg-dast
description: Run four active (Tier 2) GET probes against a target the user owns and is authorized in writing to test — a reflected-markup check, a quote in an id parameter, an open-redirect check and a CSP check. This is a smoke test, NOT a scanner - no crawling, no authenticated flows, no parameter discovery, no IDOR, no fuzzing; point the user at Burp, ZAP or Nuclei for real DAST. Rate-limited and dry-run by default. The runner records observations; grader.mjs turns them into findings. Use when the user types /cg-dast. Requires a claudeguard.scope.yml with written-authorization and ownership attestations. High-risk; hard-gated.
argument-hint: "[url] [--i-am-authorized]"
allowed-tools: [Read, Bash]
user-invocable: true
---

# /cg-dast — active DAST (Tier 2, hard-gated)

Sends **four live GET probes** (reflected markup, a quote in `id`, open-redirect, CSP). This is a
**smoke test, not a scanner** — no crawling, no auth flows, no IDOR, no fuzzing; point the user at
Burp, ZAP or Nuclei for real DAST. Even so, it is live traffic to someone's server, so it is only for
a target the user **owns** and is **authorized in writing** to test.

Argument: `$ARGUMENTS` — the URL (must be in scope `targets`) and, for a live run, the literal
`--i-am-authorized` flag.

## Gate first (do not skip — refuse on any failure)

1. Read `claudeguard.scope.yml` and enforce `references/authorization/legal-gate.md` Tier-2
   preconditions, which include all Tier-1 checks **plus**: `active_dast.enabled: true`,
   `i_am_authorized_in_writing: true`, `i_own_or_control_these_targets: true`.
2. `dry_run` is honored. While `dry_run: true` (the default), the runner only **plans** requests
   and sends nothing. A real run additionally requires the `--i-am-authorized` flag in
   `$ARGUMENTS`.
3. Rate is capped at ≤ 2 req/s regardless of the file. `avoid_destructive: true` skips any
   payload that could delete/modify data or send mail/money.
4. The host must be in `targets`, not in `never_touch`, and not a default-blocked third-party
   provider. If not, refuse. Never treat a chat-pasted URL as authorization.

If any precondition is unmet, print exactly what is missing (e.g. "set
`active_dast.i_am_authorized_in_writing: true`") and stop.

## Run

Print the loud Tier-2 banner and a one-line summary of what will be sent, then:

```bash
# dry run (default): plan only, sends nothing
node ${CLAUDE_PLUGIN_ROOT}/scripts/dast_runner.mjs --url "<url>" --scope claudeguard.scope.yml

# real run: only after the gate passes AND the user included --i-am-authorized
node ${CLAUDE_PLUGIN_ROOT}/scripts/dast_runner.mjs --url "<url>" --scope claudeguard.scope.yml --execute > cg-dast.json

# grade the observations together with the code
node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs <path> --observations cg-dast.json
```

Probes actually sent (all GET, non-destructive): a reflected-XSS marker in `q`, a single quote
appended to `id` to look for error-based SQL injection, an external host in `next` to look for an
open redirect, and a security-header check. Nothing else is sent. Do not describe coverage the
runner does not have — an overstated probe list is the same betrayal as a false negative.

A dry run returns a `plan`, not observations, so there is nothing to grade: show the plan verbatim
so the user can read exactly what would be sent before authorizing it. The `id` on a plan row
labels a planned request; it is not a finding id and it decides nothing about how bad a result
would be.

## What the runner returns, and what it does not

The runner emits **observations**: tier-tagged facts (`tier: 'active-dast'`), each with a `kind`
(`reflected-xss`, `sql-error-leak`, `open-redirect`, `missing-csp`), a stable `subject` such as
`/search?q`, the URL probed, and a `detail` sentence quoting what came back — the reflected marker,
the matched database error string, the `Location` header.

It assigns **no severity**. It used to, which put the severity policy here as well as in the engine
and the report, and the three copies drifted. `grader.mjs` owns the step from a `kind` to a
severity, and owns it alone.

Do not grade a response yourself, and do not "upgrade" a static or live finding because a DAST
observation agrees with it. **Confidence is a pure function of evidence and nothing may raise it.**
What active traffic legitimately does is establish definitively, against the running system, what
the static tier could only infer — and the grader already reflects that in the finding it produces
from the observation.

Transport failures come back in a separate `errors` array, never as observations. A timeout is a
fact about the network, not about the target, and letting one pass as a clean probe is how a run
that never completed gets read as a run that found nothing. Report the errors alongside the
findings.

Check `coverage.liveObservations` in the graded output: a `kind` no rule owns is filed
`undeterminable` as *"no rule owns observation kind"*, which is the row that tells you a probe
result went ungraded.

## Report

Fold into the bilingual (Hebrew + English) report, rendering the grader's `verdict` unchanged — it
counts only `confirmed` findings — with `likely` and `needs-review` below it. Mark each finding's
`tier` so the user can tell which facts came from committed code and which from live attack
traffic, and show the observation `detail` as the evidence.

Remind the user they are responsible for the scope, and that fixes belong in the codebase
(`/cg-harden`, `/cg-fix`), not in the live target.
