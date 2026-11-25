---
name: network-troubleshooting
description: "OSI-first network device diagnosis with vendor commands."
version: 1.1.0
author: Dandi Suryadi, Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [network, troubleshooting, osi, diagnosis, cisco, mikrotik, huawei, aruba, arista, juniper, ruijie, fortinet]
    related_skills: [ntnroute, network-device-cli, network-change-management, network-security-audit]
---

# Network Troubleshooting

Diagnose a network device fault with the OSI ladder as the reasoning model and
live read-only evidence as the only thing that counts as proof.

This is a guided procedure, not an output parser. Vendors differ in syntax,
pagers, and error text — so the skill supplies the *order of thinking* plus
per-platform command hints, and you supply the interpretation from actual
output. Nothing here auto-verdicts from text patterns; that is your job.

## When to Use

- A device in the `ntn` inventory is unreachable, slow, or behaving oddly.
- "No internet", "can't ping", "link down", "duplex errors", "it flaps".
- You need real state before deciding on a change.
- You must distinguish device down / path down / your own session dying.
- You need to rule out a change as the cause.

Not for: changing configuration (→ `network-change-management`),
adding/removing devices (→ `ntnroute`), security assessment
(→ `network-security-audit`), or plain Linux servers.

## Core principles

1. **OSI layers, don't skip.** L1 → L2 → L3 → L4 → L7. Prove the lower layer is
   healthy before moving up. Exception: a sharply specific symptom (DNS
   timeout) may go straight to its layer.
2. **Read-only first.** Every diagnostic command is read-only. No `set`,
   `configure`, `no`, `undo`, `clear`, `reset`, `shutdown`, `reload`. Changes
   are `network-change-management`.
3. **One symptom = one hypothesis.** Each hypothesis needs a command that can
   falsify it, named before you run it. No "try restarting" without evidence.
4. **Absolute counters mean nothing.** Read counters twice with a real pause;
   only a **climbing** number is a fault. Record both numbers and the interval.
5. **Record findings.** What was checked, key output, conclusion, what was
   ruled out. Without notes the same checks get repeated.
6. **A falsified hypothesis is discarded.** Don't patch an old hypothesis to
   fit new evidence — write a new one.
7. **Unknown stays unknown.** If you cannot determine something, say so. An
   ambiguous reachability result is a result.

## Procedure

The full step-by-step is **`references/diagnosis-playbook.md`** — eight phases,
each with an exit condition. Read it before starting; the summary here is the
shape, not the detail.

### Phase 0 — Scope

Device, symptom in the observer's words, since when, what's affected, and
whether anything changed recently. One question, then work.

### Phase 1 — Is it there?

```bash
NTN_INTERNAL=1 ntn ping <ref>
```

Ping failure is one signal, not a verdict: device down, ICMP filtered, and
broken session all look identical. Get a second vantage point before
concluding. Reachability is a question, not an assumption.

### Phase 2 — Baseline

```bash
ntn sync <ref>
```

Exact OS and version, because they decide which diagnostic commands are valid.
If SSH is dead but ICMP answers, work from an upstream neighbour.

### Phase 3 — Read state

One batch per device, saved to a file, grouped by layer:

```bash
NTN_INTERNAL=1 ntn exec <ref> '<cmd>' '<cmd>' > /tmp/<host>-diag.txt
```

Command hints per platform: `references/vendor-commands.md`. Hints for confirmed
syntax only — a rejected command is not a fault, verify against official docs.

### Phase 4 — Climb or bisect

`references/osi-ladder.md` holds the symptom → layer map and the traps per
layer. Climb when you know nothing; bisect when the symptom is narrow (last
working point, first failing point).

When the symptom is routing-shaped — **adjacency up but routes missing, or
prefixes arriving from one side only** — go straight to
`references/routing-protocol-interop.md`. That file covers the failure modes
that produce no error at all: OSPF network-type mismatch (`FULL/BDR` on one
end, `not-reachable in topology Base` in the database, every route silently
discarded), RouterOS `passive` being a flag rather than a parameter, MTU and
authentication mismatches, and area/stub disagreement. It also carries the
warning that `rollback_gen` will inject `shutdown` into an interface that was
`up` — write routing rollbacks by hand.

### Phase 5 — Two readings

Every counter claim needs `reading, pause, reading`. Flat is fine; climbing at
X per N minutes is the finding.

### Phase 6 — Research, in order

Vendor docs for the exact release → vendor advisories and release notes (a
known bug in that version is a valid root cause) → community for leads only,
verified before it enters the report. `references/official-sources.md`.

### Phase 7 — Report and propose

Symptom, scope, checked layers with evidence, confirmed facts, hypothesis with
a confidence level, what you ruled out, remaining unknowns, the next cheapest
test, and the proposed fix. **Never apply anything** — that is
`network-change-management` with its approval gate and rollback.

## During an actual outage

Priority changes from "find the cause" to "restore service, then find the
cause". Note what you did and when, because a restart destroys evidence. If the
symptom began right after a change and a `check_point` exists, propose the
rollback through `network-change-management` instead of hand-fixing live.
Never change the interface carrying your own session.

## Cross-vendor practice

- Confirm vendor, OS/version, model, and role before choosing commands. Don't
  infer from notes about a different platform.
- The command tables are hints. Similar keywords do not guarantee identical
  behaviour across brands, and a release can change syntax.
- Prefer standard signals that exist everywhere: link state, counters,
  addressing, routes/neighbours, logs, end-to-end tests.
- Unfamiliar platform? Ask for safe read-only output or read the docs. Never
  run an unverified batch to "see what happens".
- `ntn` moves the bytes and preserves the transcript. It does not interpret.
  Interpretation is yours.

## Pitfalls

- **Never change the management path.** Identify the interface carrying your
  session before anything else; diagnosis does not authorize changes.
- **Verify platform syntax.** RouterOS has no `show` — every command starts
  with `/`. Huawei uses `display`. Juniper needs screen-length handled (the
  engine does it). Assuming Cisco shapes across brands wastes time and can be
  read as a fault that isn't there.
- **Ping is one signal.** ICMP may be filtered by policy.
- **`up/up` is not healthy.** Rising CRC/input errors are a physical fault with
  a green light.
- **Two readings or no claim.** Absolute counters are archaeology.
- **A bug in that exact release is a legitimate root cause.** Check release
  notes before theorising about your own config.
- **Ruled-out items belong in the report.** They stop the next person
  repeating your work.

## Verification

No bundled parser — verification is the evidence: raw output saved per device
and layer, read and interpreted manually, adapted to the confirmed platform.

What has actually been exercised:

- The eight-phase structure and its exit conditions are the rewritten
  procedure; the previously bundled `triage` parser (Cisco/MikroTik regex
  verdicts) is gone, so no output is auto-graded any more.
- The per-platform command hints in `references/vendor-commands.md` come from
  the previously working diagnostic battery plus vendor documentation. They
  have **not** been re-run end to end in this revision: the lab VMs
  (`192.168.200.0/24`, vmnet8) were powered off at the time of writing.
- The engine's `month_for` timestamp fix and the archive-pair naming are
  unit-tested independently of the lab.

Treat the command tables as "confirmed syntax, pending a full live pass". When
the lab is up, run Phases 1–5 on one RouterOS and one IOS device and record the
dated result here.