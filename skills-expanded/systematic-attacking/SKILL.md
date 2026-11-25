---
name: systematic-attacking
audience: specialist
description: Use for ALL authorized offensive-security / bug-bounty work — the single method to find, chain, prove, dedup, and package the highest-value (High/Critical) findings across every domain (web/SaaS, smart-contract/DeFi, infra/cloud, LLM/AI, mobile, binary/firmware). Enforces two iron laws before any offensive action or submission: never act outside authorized verified scope, and no finding without a reproduced, negative-controlled, intrinsic-impact proof.
status: authored
---

# Systematic Attacking

## Overview

Offensive work fails in two characteristic ways: it strays **outside authorized scope**
(the act of testing is itself potentially harmful), and it **submits claims that were never
really proven** — reachability dressed as impact, a pile of lows dressed as a high, a known
composite dressed as novel. This skill is the one method that blocks both failures.

**This is the only offensive _lifecycle_ skill.** It alone owns scope, severity, lead→finding promotion, and submission authority. `systematic-bug-hunting` is a subordinate, zero-authority bench-craft layer nested inside Phases 2–5: it generates candidates, holds no scope or severity, and refuses to start without a Phase 0 scope lock. Experimental / novel-vector work is a *phase* inside it
(Phase 3b), not a sibling skill — a second file would duplicate this safety lifecycle, and the
looser copy would become the bypass path. `systematic-debugging` guards the *fix*; this skill
guards the *claim* — and adds a scope law because attacking, unlike debugging, can hurt a real
system.

**Violating the letter of this process is violating the spirit of it.** An empty gate is a
skipped gate; a skipped gate is lab noise, not a finding.

## When a packet contradicts this skill

**Say so; do not resolve it silently.** The dispatching packet still wins — that is the design.
But if a packet instruction contradicts this skill, emit a `## PACKET OVERRODE SKILL` section in
your response naming both sides.

This is not hypothetical. H2 below states that a primitive **carries capability, not severity**,
and that an inert primitive is *labelled*, never deleted. For five consecutive audits Chrono's
Phase-3 packets instead demanded an impact-bar verdict per idea. Lanes obeyed the packet, killed
their own primitives, and the Chaining phase starved for want of a pool — silently, because nothing
made the contradiction visible.

No gate is added here. A reporting duty is enough: the failure was invisibility, not permissiveness.

## The Two Iron Laws

Two co-equal laws. Neither is negotiable, and neither substitutes for the other.

```
IRON LAW 1 (safety): NO OFFENSIVE ACTION OUTSIDE AUTHORIZED, VERIFIED SCOPE.
IRON LAW 2 (rigor):  NO FINDING WITHOUT A REPRODUCED, NEGATIVE-CONTROLLED,
                     INTRINSIC-IMPACT PROOF.
```

- **Law 1** is enforced at Phase 0 and is cross-cutting: an ambiguous scope STOPS; every hop
  stays inside the in-scope allowlist; a genuine refusal is **terminal** and is never re-shopped
  to a looser lane. Any live / mutating / credential-using action waits for the operator gate.
- **Law 2** is enforced at Phases 5–6: a runnable PoC against the real oracle, causal negative
  controls at link *and* chain level, the G1–G4 impact bar, and a different-family reproduction —
  before anything is called a finding or scored.

## Vocabulary — one definition, never redefined downstream

Every reference doc and specialist uses **these** words. Do not redefine "finding" anywhere.

**Promotion points have one home: `shared/modes/bounty.md` § "Evidence vocabulary — the
pipeline's type system".** That mode is the promotion home — it owns *when* each token is promoted
and what proof each transition demands (its state-token table and the Law 2 gate), and it already
names this section as naming "the same tokens." So the glosses below are denotational
only; for a token's **promotion point** read the mode, not here — exactly as this skill already
defers the phase list one section down. A restated criterion is what split `candidate` two ways; one
home ends it.

- **primitive** — a bounded attacker capability or environmental fact (from a lead, a validated
  finding used as an inner link, public/known behavior, or config). Carries **capability, not
  severity.**
- **lead** — "there may be exploitable impact here." No CVSS, **never submitted.**
- **candidate** — a composed attempt under evaluation; the mode owns the bar it must clear.
- **finding** — the verified type. **Only findings carry CVSS and may be submitted** (this skill
  owns severity and submission authority; the mode owns the candidate→finding gate).

**Finding definition (offensive-impact only, per operator):** a proven, reproducible claim of
**intrinsic** impact — loss of user/platform funds · RCE / attacker-controlled execution · direct
damage to users or services · cross-tenant data compromise at material scale · privileged /
control-plane takeover · a realized malicious capability. **Reachability, disclosure,
"could-lead-to" are NOT findings.** They are, at most, leads.

## The lifecycle — owned by the MODE, not by this skill

**`shared/modes/bounty.md` owns the phase list.** This skill previously restated Phases 0-8
verbatim, which made three documents claim authority over one process — and a restated process
loses to whichever copy is most recent, which is always the packet. What follows is what this
skill uniquely owns; for phase definitions, gates and owners, read the mode.

**This skill's job is METHOD**: how to discover primitives, how to compose them, and what
evidence survives review. It is target-agnostic. Target-class specifics live in their own
checklists (`cross-chain-bridge-audit`, `cosmos-sdk-audit-checklist`,
`vulnhunter-solana`, `known-advisory-backport-check`); campaign process lives in the
mode; this lane's task lives in the packet.

## Phase numbering — read campaign phases from the mode; two other numberings are different objects

`shared/modes/bounty.md` owns the campaign phase list and is its **only** authority. Do not read a
campaign phase number from this skill or from a specialist brief — read it from the mode. As of this
writing the mode defines **eight** campaign phases, **0 through 7** (verify:
`grep -cE "^## Phase [0-9]" shared/modes/bounty.md` returns `8`). **Phase 0 is ADMISSION** — the
campaign's entry gate and its stop condition. A mapping that starts the campaign at Phase 1 silently
deletes ADMISSION, and that omission once let a campaign run 38 lanes. The eight headers, by name —
for what each one *does* (its gate, owner, and procedure) read the mode; this is a locator, not a copy:

| Campaign phase — owned by `shared/modes/bounty.md` (read there for contents) |
|---|
| Phase 0 — ADMISSION |
| Phase 1 — RESEARCH |
| Phase 2 — PLANNING |
| Phase 3 — HUNT |
| Phase 4 — CHAINING |
| Phase 5 — VERIFY |
| Phase 6 — PACKAGE & OPERATOR-GATE |
| Phase 7 — TEARDOWN |

**`S0`–`S7` are NOT a parallel numbering of these campaign phases.** They are a *different object*: a
single lane's internal verification-contract stages (`required_phase_ids` in a task packet, enforced
by `scripts/python/verification_contract.py`) — one lane proving its own claim, not the cross-lane
campaign. The mode says so directly: see `shared/modes/bounty.md` § "Phase 5 — VERIFY", which
names the two things mistaken for this phase and rejects both — a lane's own `S5` (its internal
`S0-S7`, proving its own claim, required) and a Phase 3 deliverable review (does the artifact hold
up, not does it reproduce elsewhere).

So a lane's `S5` and campaign Phase 5 are not the same event. Lining `S0`–`S7` up in a column beside
the campaign phases is exactly what made "Phase 5" ambiguous; keep them apart.

**This skill numbers its own method sections separately, and that numbering is not the campaign's.**
The Quick checklist, the safety-rail table, and the verification-contract binding below refer to
Phases **0–8** — a finer-grained view of the *method* than the mode's eight campaign phases (for
instance it splits the mode's single VERIFY phase into separate PoC, impact-bar, and skeptic stages).
When *this skill* says "Phase 3" it means its own hunting stage; when *the mode* says "Phase 3" it
means campaign HUNT. They are close but not guaranteed identical, so resolve any specific number
against the mode rather than assuming a bare "Phase N" means the same stage in both.

**When a packet and a document disagree on a phase number, the packet wins and you report the
conflict.** Do not silently renumber, and do not assume "Phase 3" in a brief means the same stage as
"Phase 3" in the mode.


## Domain branching (Phase 3) — route, never copy

The skill is **target-agnostic**. In Phase 3 the hypothesis lane selects the domain checklist set
for the target and **routes into** the domain reference — it never copies domain content into this
skill or into chain-strike-v2. The verification back-end (Phases 4–8) is identical across domains.

| Domain | Route into (capability card) | Per-domain checklists / references (reference, never copy) |
|---|---|---|
| **web / SaaS** (+ **infra / cloud**) | `shared/capabilities/bounty/web-api-saas.md` | web + infra/cloud pattern sets in chain-strike-v2 §9–10; the card's fresh/no-auth DAST profile (authed-session + mobile are `needs_tool`) |
| **smart-contract / DeFi** | `shared/capabilities/bounty/smart-contract-web3.md` | `evm-audit-flow`, `cosmos-sdk-audit-checklist`, `cross-chain-bridge-audit`, `known-advisory-backport-check`; DeFi patterns in chain-strike-v2 §9 |
| **LLM / AI** | `shared/capabilities/bounty/ai-llm-system.md` | LLM/AI patterns in chain-strike-v2 §9; live-endpoint probing is `needs_tool` (offline transcript analysis is the live scope) |
| **mobile** | *(no dedicated card — profile of web-api-saas)* | mobile pattern set in chain-strike-v2 §9; mobile targets are `needs_tool` per the web card |
| **binary / firmware** | `shared/capabilities/bounty/binary-firmware.md` | `sandbox-provision-discipline`; card is `needs_tool` (radare2 static only) |

The card paths above are the full, maintainer-internal cards. A public checkout ships the public
versions under the same file names in `shared/capabilities/public/bounty/`.

**Cross-domain pivots** — where the shortest path to critical usually lives — are handled in
chain-strike-v2 §10 (web SSRF→cloud IMDS→ATO; LLM injection→MCP→cloud action; mobile deeplink→web
OAuth→ATO). Inventory primitives from *every* domain the target touches.

## Safety rails → phase gates (nothing floats free)

Every rail is enforced at a named gate; none is advisory prose.

| Rail | Enforced at |
|---|---|
| authorized-scope-only · `scope_gate` · `exact_target_allowlist` | Phase 0 |
| global refusal invariant (no unauthorized-attack help; a refusal is terminal, never re-shopped to a looser lane) | Phase 0 + cross-cutting |
| operator gate before any live / mutating / credential-using action | Phase 0 (target-engage) + Phase 5 |
| `no_self_inflicted` (+ self-inflicted detector) | Phase 0 boundary + Phase 5 |
| link/chain causal negative control + `poc_reproduction` | Phase 5 |
| impact bar G1–G4 + `cross_family_reproduction` + `cvss_v4` | Phase 6 |
| prior-art / dedup (finding **and** composite) | Phase 1, refreshed pre-submit |
| final Submit = per-report operator "go" | Phase 8 (the skill stops here) |

## Bounty verification-contract binding (submission-grade by construction)

Each hard gate emits **exactly one** verification-contract field, so the skill's output *is* a
filled contract. An **empty field means a skipped gate** — the mechanical line between a finding
and lab noise.

- **Phase 0** → `scope_gate`, `exact_target_allowlist`, `no_self_inflicted` (boundary)
- **Phase 5** → `poc_reproduction`, `negative_control`, `no_self_inflicted` (verified)
- **Phase 6** → `cvss_v4`, `cross_family_reproduction`, G1–G4

## Anti-patterns (do NOT PROMOTE any chain exhibiting these — banking is unaffected)

Inherited from chain-strike v1: **forced chains** · **theoretical chains** · **duplicate-root-cause**.
Added (each blocks a characteristic false-submit): **severity laundering** (naming lows/mediums ≠ a
high) · **chain padding** (endpoint occurs without the link) · **privilege laundering** (hidden
admin/root/victim capability) · **scope laundering** (out-of-scope hop bridges the path — Law 1 +
legal) · **assumption laundering** (lab config presented as real target state) · **same-effect
double-counting** · **circular dependency** · **unreliable / race-only chain** (probability
ignored) · **model mismatch** (harness omits a prod guard/oracle/identity/OS behavior) · **duplicate
composition** · **downstream-known chain** · **unsafe proof** (validation would exceed scope, harm
bystanders, move real funds, persist, or destroy prod). The full definitions live in
chain-strike-v2 §12.

<a id="primitive-pool"></a>
## The primitive pool — how specialists coordinate

There is **no live peer-to-peer channel** between running specialist CLIs. All coordination is
**Chrono-brokered** (specialist → Chrono → specialist). The Chaining phase's primitive pool is
therefore a **Chrono-owned shared findings ledger**: each specialist writes typed primitives to it
via their outbox, Chrono aggregates, and the chaining owner (`exploit-developer`) runs
chain-strike-v2 over the pool. No new comms machinery is required or assumed.

## Quick checklist

- [ ] Phase 0: in-scope allowlist + forbidden set written; ambiguous scope STOPPED; operator target-engage obtained.
- [ ] Phase 1: prior-art + composite dedup run *before* effort (`dedup-prior-art-check`: a separately provisioned prior-art service, or manual Solodit / GitHub-advisory searches); refreshed pre-submit.
- [ ] Phase 3: leads/primitives only from both lanes; 3b held to the same bar as 3a.
- [ ] Phase 4: typed graph + impact-first bidirectional search; shortest reliable path; **no CVSS / no severity arithmetic**.
- [ ] Phase 5: runnable PoC vs the real oracle; five link controls + chain-level control pass; operator gate cleared for any live action.
- [ ] Phase 6: G1–G4 pass; different-family reproduction; CVSS v4 scored **once** from the terminus.
- [ ] Phase 7: skeptic verified soundness (oracle real, harness faithful, result stable, prior-art honest).
- [ ] Phase 8: de-AI'd, form-fit, handed to operator; **final Submit left to the operator**.
- [ ] Domain content **routed into** bounty/* cards + checklists, never copied here.
- [ ] Every hard gate emitted its one contract field; no empty field.
