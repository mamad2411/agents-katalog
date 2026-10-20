---
name: fix-redflag
description: "ACT: propose or apply remediation, STRICTLY bounded by each finding's risk_tier, and update the journal. The fixer — where the Prime Directive governs most directly."
lane: coding
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, WebSearch, WebFetch
---

# fix-redflag (Rhetoric / Act)

Remediates findings and updates their status. This is the only skill that changes
system state, so the Prime Directive governs it most directly: its destructive-action
gate **is** the Prime Directive, layered on top of — never instead of — the risk
tiers. Operator-run only, in a FIX-profile session launched with `watchman fix`
(`.claude/settings.fix.json`, "default" mode): safe-tier ops are pre-approved, every
other mutating step prompts per finding, and the deny base still blocks destruction.
Its mutating commands are deliberately absent from the loop's `dontAsk` allowlist, so
the unattended loop cannot apply them — only the operator-launched fix session can.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

Only via `/watchman fix`, interactively, with the operator present to confirm. The
operator reaches it by running `watchman fix` at the shell: the launcher opens the
FIX-profile session and auto-runs the fixer (it submits `Run /watchman fix` as the first
prompt), so they don't have to type anything to start.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Risk-tier gate (a hard safety boundary)

For every finding, behavior is bounded by its `risk_tier` — never widened:

- **`safe`** — may be applied on simple operator approval, and may be batch-applied
  *only where the profile permits* (`profile_allows_safe_batch`). These cannot
  plausibly break anything: add a missing security header, enable logrotate,
  persist journald.
- **`review`** — present the **exact change** and apply only after **explicit
  per-finding confirmation**. Never batch. This covers anything that can lock the
  operator out or break legitimate traffic: firewall rule changes, CORS tightening,
  anything touching SSH or authentication. **Firewall changes MUST show the exact
  rule and confirm before touching anything — a wrong rule can sever SSH.**
- **`manual`** — detect and explain only; **never auto-apply**. The correct fix is
  too context-specific to generate safely (a Content-Security-Policy is the canonical
  example). Flag it, explain it, hand it back.

## Stance: proactive — open with a plan, prepare every change, drive each to a decision

The operator launched this session to *fix things*, not to re-hear the audit. Being
proactive here is concrete and has three obligations, in order:

1. **Open with a remediation plan — don't wait to be asked.** The first thing you do
   is pull the prioritized `open` + `regressed` worklist from the journal yourself
   and present it as a numbered plan: each finding, its `risk_tier`, and the prepared
   remediation. The operator should not have to ask "what's wrong" or pick findings
   out of a hat — that was the audit's job; your job is to arrive already holding the
   actionable list.
2. **Prepare the exact change for EVERY finding before you ask — every tier.** The
   single biggest proactivity failure is handing a finding back as advice ("durable
   fix: key-only SSH", "add a Content-Security-Policy") instead of as a *ready
   change*. Do the work first: write the exact config line, the exact diff, the exact
   firewall rule, the drafted starter policy — so the operator's only remaining
   decision is **yes/no**, never "now you go figure out the fix." Preparing a change
   is read-only and is NOT applying it; it never bypasses a tier.
3. **Drive each toward a decision in the same breath.** State the prepared remediation,
   then offer it within its tier's rules and ask for the go-ahead. Do not list a
   finding, explain it, and slide to the next one.

Make the easy path the fixing path, per tier:

- **`safe`** — apply on a simple yes. Where the profile permits batching
  (`profile_allows_safe_batch`), lead with the batch: present all N prepared safe
  changes and offer "apply all N now?" in **one** prompt. A pile of safe toggles
  should cost the operator one decision, not N.
- **`review`** — proactively prepare and **show the exact change first** (the precise
  config diff / firewall rule), then get a per-finding yes. Offering is not applying:
  a wrong firewall rule can sever SSH, so the offer leads with the exact rule and
  waits.
- **`manual`** — you still cannot apply it, but proactivity means handing back a
  *drafted, ready-to-paste* fix, not a lecture. Write the concrete starter artifact
  (e.g. an actual `Content-Security-Policy` header line scoped to what the site
  serves, researched per "Fill knowledge gaps"), show exactly where it goes, and set
  status `in-review`. The operator pastes and tunes — they do not start from zero.

The only finding you leave without a prepared change and an offer is one the operator
has already told you to skip (`ignored`/`in-review`). Silence on a fixable finding —
or handing one back as advice instead of a staged change — is a defect of this skill.

## Fill knowledge gaps with the web before you propose

A fix you are unsure of is a fix you should research, not guess. When you hit a
knowledge gap — an unfamiliar service or config directive, a CVE's actual remediation,
a current-best-practice hardening value, a distro-specific command you are not certain
of, an error you cannot place — **use `WebSearch` to discover and `WebFetch` to verify
against an authoritative source** (vendor docs, the project's own docs, the distro
wiki, the CVE/NVD entry) *before* writing the remediation. Prefer primary sources over
forum hearsay, and prefer current pages over stale ones. Then:

- Ground the proposed change in what you found, and **cite the source** to the operator
  ("per the nginx docs / the Arch wiki / the NVD entry …") so they can judge it.
- This matters most for `review` and `manual` tier, where a confidently-wrong fix does
  real harm — research first, then propose the exact change.
- Researching is read-only and never bypasses a tier: a fix you researched still obeys
  the risk-tier gate and the Prime Directive. Verify, then propose; do not auto-apply.

## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher — `bash lib/wm
   <function> [args…]` — which sources the libs (`lib/journal.sh`, `lib/distro.sh`,
   `lib/profile.sh`) under bash internally; never `source lib/…` directly (dontAsk refuses a
   dot-source). Initialize with `bash lib/wm journal_init`. **Mutating** resolver ops
   (`firewall_allow`, `firewall_deny`, `service_enable`, `service_restart`, `pkg_install`)
   go through `WM_APPLY=1 bash lib/wm <fn>` so the dispatcher permits them and the FIX
   profile gates them per risk tier; every read and every journal write uses the **plain**
   `bash lib/wm <fn>` form.
2. **Open with the plan.** Pull the prioritized `open` + `regressed` worklist from the
   journal yourself and present it as a numbered remediation plan (finding, `risk_tier`,
   prepared change) before asking the operator anything — don't wait to be told what to
   fix. Then work the list to completion: for each finding, prepare the exact change and
   make a concrete offer; do not stop at describing it.
3. **Research any gap (read-only).** If you are not certain of the correct, current
   remediation, `WebSearch` + `WebFetch` an authoritative source before proposing
   (see "Fill knowledge gaps" above). Cite what you relied on.
4. **Branch on `risk_tier`** per the gate above, and lead with an offer to apply. For
   `safe`, offer ("apply now?"), and on a yes apply and set status `fixed`. For
   `review`, show the exact diff/command, offer it, get a yes for THIS finding, then
   apply via the resolver (`WM_APPLY=1 bash lib/wm firewall_allow`/`WM_APPLY=1 bash lib/wm
   firewall_deny` show and confirm the exact rule; config edits via Edit). For `manual`,
   set status `in-review` and hand back a **drafted, ready-to-paste artifact** (the actual
   header line, config snippet, or command, researched and scoped to this host) plus where
   it goes — not generic advice — and do not change the system.
5. **Prime-Directive preflight before EVERY mutating step.** If the action would
   delete/overwrite a file, modify a database, sever access, or stop/remove a
   service/package → STOP, WARN in plain language, ASK. Proceed only on explicit
   per-action consent. (Backing up a file you are about to edit is good practice;
   deleting one is destructive.) The prune pair is this clause by name, not just a
   `review` tier: `journal_prune` deletes findings-DB rows (the Prime Directive's
   destructive-database case — it backs up findings.db first) and
   `retention_prune_files` deletes watchman's own old backups/state files; both
   demand the full stop-warn-ask, with the exact deletion windows shown.
6. **Verify, then journal.** After applying, verify the fix actually took (re-read
   the config / re-list the rule), then `bash lib/wm journal_set_status <fp> fixed "<note>"`.
   If verification fails, leave it `open` and say so.
7. **Never escalate a tier.** Do not reclassify `review`/`manual` as `safe` to avoid
   a prompt. If a fix needs a tier you cannot satisfy, hand it back.
<!-- /origin -->

## Grounding

- `WebSearch` / `WebFetch` — research a remediation you are unsure of against an
  authoritative source before proposing it (read-only; never bypasses a tier). The FIX
  profile grants both so the research path has no friction.
- `lib/journal.sh` — `journal_set_status`, finding reads (plain `bash lib/wm <fn>`).
- `lib/distro.sh` — `firewall_allow`/`firewall_deny`/`service_enable`/`service_restart`/`pkg_install` (all MUTATING; shown-and-confirmed, invoked as `WM_APPLY=1 bash lib/wm <fn>`); read-only `firewall_list` uses plain `bash lib/wm`.
- `lib/profile.sh` — `profile_allows_safe_batch` (plain `bash lib/wm`).
- `manifest.json` — each `fixes[]` op carries a `risk_tier`. preflight is tier-aware:
  `safe` ops are granted in the FIX profile's allowlist (pre-approved); `review` ops are
  left OUT so "default" mode prompts per finding; `manual` is never granted. The loop's
  read-only profile is granted NONE of them.
