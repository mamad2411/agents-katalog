---
name: hunter-report
description: >-
  Render the delivered Hunter artifact — the Field Notebook made permanent — in
  the fixed brand section order (cover, coverage map, finds, unpromoted signs,
  dark surfaces, method) with coverage always preceding findings. Emits both
  markdown and JSON and requires they agree. Produces the per-Find template
  including a ready-to-paste fix prompt another coding agent can act on. Load
  whenever about to write, render, assemble, or deliver a hunt report, a VERDICT,
  a findings document, or a fix prompt, or when the operator asks to "write up the
  hunt", "generate the report", "produce the fix prompt", or "deliver the finds".
  Runs after hunter-triage. Assumes hunter-doctrine is loaded.
---

# Hunter Report

The report outlives the hunt. It is the one surface a human reads without
re-running anything, so it must be self-justifying: every verdict expandable to
its artifact, every claim carrying a pointer, coverage stated before findings so
the reader learns what was *looked at* before what was *found*.

## Inputs

- `TRIAGE.json` from hunter-triage — deduplicated, severity-anchored, ranked Finds.
- The surface map from hunter-recon — the coverage denominator and per-surface
  state (cold / find / dark).
- `SIGNS.json` — leads that failed promotion, with the failed checkbox.
- Hunt metadata — hunt id, target, ISO-8601 start, duration, cost, oracle/skill
  versions, seeds.
- Any assumptions logged by hunter-ask unattended mode.

## Outputs

Two artifacts that MUST agree (see reconciliation below):

- `report.md` — the human artifact, sections in fixed order.
- `report.json` — the machine contract consumed by CI and the TUI.

### Fixed section order (brand §12 — non-negotiable)

```
1. Cover          target · hunt id · ISO timestamp · duration · cost · verdict + coverage fraction
2. Coverage map   every surface, state (cold ·/ find ●/ dark ?), BEFORE any finding
3. Finds          per-Find template below, ordered by evidence strength (default) then rank
4. Signs not promoted   each lead + which promotion box failed
5. Dark surfaces  every unprobed surface + why it was not reached
6. Method         probe inventory · oracle versions · skill versions · seeds
```

Section 2 precedes section 3 deliberately. Reversing it manufactures the illusion
of thoroughness and is a brand anti-pattern. Section 4 is mandatory even when
empty (`0 signs unpromoted`): publishing rejected leads is the reader's only
evidence the verification ladder actually rejects things.

Default Find ordering is **evidence strength, not severity** (brand §3): a
CRITICAL with one artifact sorts below a MAJOR with a twice-confirmed replay. The
`rank_score` from triage is offered as an alternate "by priority" view, never the
default.

## report.json schema

```json
{
  "hunt_id": "hunt/2026-08-07T14-02Z",
  "target": "acme-web",
  "started": "2026-08-07T14:02:11Z",
  "duration": "4m 12s",
  "cost_usd": 0.38,
  "verdict": "FAIL",
  "coverage": { "probed": 41, "denominator": 78, "cold": 40, "find_surfaces": 1, "dark": 37 },
  "assumptions": [],
  "finds": [ { "...": "per-Find object below" } ],
  "signs_unpromoted": [
    { "sign_id": "0f2c", "observation": "...", "failed_box": "reproduced_twice", "note": "observed 1/3, non-reproducible" }
  ],
  "dark_surfaces": [
    { "surface": "GET /admin/export", "reason": "no credential provided; escalated via hunter-ask, defaulted skip" }
  ],
  "method": {
    "probes": ["http-fuzz@1.4", "authz-matrix@0.9"],
    "oracles": ["status-oracle@2.1"],
    "skills": ["hunter-doctrine@1.0", "hunter-triage@1.0", "hunter-report@1.0"],
    "seeds": [ 42 ]
  }
}
```

Verdict comes from the closed set (hunter-doctrine): `PASS`,
`PASS (LIMITED COVERAGE)`, `PASS WITH ISSUES`, `FAIL`, `NOT-COVERED`. Never
`VERIFICATION-PENDING` — it may not appear in a delivered report. The verdict is
never rendered without its coverage fraction beside it. Compute it:

- Any Find at all → `FAIL`.
- Only ADVISORY/MINOR Finds, blocking criteria clean → `PASS WITH ISSUES`.
- No Finds, `dark > 0` → `PASS (LIMITED COVERAGE)`, dark list mandatory.
- No Finds, `dark == 0`, full planned coverage → `PASS` (rarest; run the
  zero-find protocol from hunter-doctrine and attach `zero_find_review`).
- An axis never exercised → `NOT-COVERED` for that axis with its reason.

## Per-Find object (JSON) and template (markdown)

Every Find object:

```json
{
  "find_id": "A31",
  "severity": "MAJOR",
  "severity_anchor": "core-flow-blocked",
  "confirmations": "2/2",
  "class": "http-5xx",
  "observation": "POST /session returns 500 on valid credentials",
  "conditions": "logged-out; valid seeded user alice@acme; empty session cookie",
  "reproduction": ["curl -i -X POST https://acme-web.test/session -d '{...}'", "observe HTTP/1.1 500"],
  "evidence": ["trail/A31/response.http", "trail/A31/stderr.log", "trail/A31/A44/response.http"],
  "expected": { "behaviour": "302 to /dashboard with Set-Cookie session", "authority": "implicit-correctness: valid credentials must authenticate" },
  "locus": "auth/SessionService.java:88 (suspected — NullPointer top frame)",
  "trails": ["A31", "A44"],
  "fix_prompt": "…string, schema below…"
}
```

The markdown per-Find template renders the same fields with evidence pointers as
monospace links, verdict-adjacent-to-evidence, and the fix prompt in a fenced
block ready to copy.

## The ready-to-paste fix prompt

This is the highest-leverage part of the report: a self-contained prompt another
coding agent can act on with no access to the hunt. It MUST contain, in order:

1. **Observation** — what the system did, in one line, with confirmation count.
2. **Reproduction** — exact steps/inputs/env to see it again.
3. **Evidence pointers** — the durable artifact ids to open.
4. **Expected behaviour + its authority** — what it should do and the source of
   that expectation (implicit correctness, a quoted spec line with location, or a
   recorded baseline).
5. **Suspected locus** — file/line if known, labelled *suspected*; omit if unknown
   rather than guess.
6. **The anti-suppression instruction** — an explicit line: *the fix must make the
   real system behave correctly and must not weaken, mock, skip, or gate around
   the detection; see hunter-anti-mock. A patch that only silences the probe is a
   rejection.*

Never fabricate a locus, a spec citation, or an expected value. If the authority
is implicit correctness, say so — do not manufacture a spec line.

## Worked example — one Find entry (markdown)

```
### ● A31 · MAJOR · core-flow-blocked · 2/2

login: POST /session returns 500 on valid credentials — 2/2 · trail/A31

Conditions   logged-out; seeded user alice@acme; empty session cookie
Class        http-5xx   ·   Blast radius 3/78   ·   Trails A31, A44

Reproduction
  curl -i -X POST https://acme-web.test/session \
    -H 'content-type: application/json' \
    -d '{"email":"alice@acme","password":"correct-horse"}'
  observe: HTTP/1.1 500 Internal Server Error

Evidence     trail/A31/response.http · trail/A31/stderr.log · trail/A44/response.http

Expected     302 to /dashboard with Set-Cookie: session=…
Authority    implicit correctness — valid credentials must authenticate
Locus        auth/SessionService.java:88 (suspected — NullPointer top frame)

Fix prompt (copy verbatim):
> POST /session returns HTTP 500 on valid credentials, reproduced 2/2.
> Reproduce: curl -i -X POST https://acme-web.test/session -H 'content-type:
> application/json' -d '{"email":"alice@acme","password":"correct-horse"}';
> observe HTTP 500. Evidence: trail/A31/response.http, trail/A31/stderr.log,
> trail/A44/response.http (same NullPointer at auth/SessionService.java:88 via a
> second surface). Expected: 302 to /dashboard with a Set-Cookie session header;
> authority is implicit correctness — valid credentials must authenticate.
> Suspected locus: auth/SessionService.java:88, NullPointer top frame.
> Fix the real system so valid credentials authenticate. Do not mock the session
> service, add a test-mode branch, broaden a try/except, or otherwise suppress the
> 500 so the probe passes — see hunter-anti-mock. A patch that only silences the
> probe is a rejection.
```

The verdict glyph `●` and severity sit **after** the evidence line, never before
it. Every pointer is a real artifact id written to the run directory.

## Markdown / JSON reconciliation — required

The two emissions are one truth in two renderings. Before delivery, verify they
agree on every load-bearing value:

- Same verdict and same coverage fraction on the cover and in JSON.
- Same set of `find_id`s, same severities, same confirmation counts.
- Same `dark_surfaces` list length as `coverage.dark`.
- Every markdown evidence pointer exists in the corresponding JSON `evidence`
  array and points to a file that exists on disk.
- Same fix-prompt text (byte-for-byte) in markdown fenced block and JSON
  `fix_prompt`.

If they disagree, the report is not shippable — fix the generator, do not
hand-edit one side. Emit a reconciliation line in Method:
`reconciled: md/json agree on 4/4 finds · 37/37 dark · verdict FAIL`.

## Handoff

`report.json` is the CI/TUI contract; exit-code mapping (brand §11) is the
caller's job, driven by `verdict` (`FAIL` → exit 1; any could-not-run condition is
not a report at all). `report.md` is the delivered human artifact. Reject-with-
reason from hunter-ask post-hunt triage feeds the Range, not this report.

## Self-check before delivery

- [ ] Sections in the fixed order; coverage (2) precedes finds (3)
- [ ] Section 4 present even if empty
- [ ] Verdict from the closed set, beside its coverage fraction, no VERIFICATION-PENDING
- [ ] Every Find sorted by evidence strength by default
- [ ] Every fix prompt carries all six parts including the anti-suppression line
- [ ] No fabricated locus, spec citation, or expected value
- [ ] Cold and dark distinct; dark list matches coverage.dark
- [ ] md and json reconciled on verdict, finds, dark, and fix-prompt text
- [ ] Zero-find hunts carry zero_find_review, never a bare success state
