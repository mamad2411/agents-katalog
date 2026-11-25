---
name: leeway-skill-lifecycle-governance
description: Governs how LeeWay skills emerge, combine, cool, transfer, deprecate, retire, and return without erasing reusable capability. Separates verified mastery from activation priority and preserves dormant skills inside the ambient capability field so cross-domain primitives remain reusable.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  mode: always-on-capability-governance
  stage: pre-capability-routing
  kernel: skills/leeway-universal-capability-kernel/SKILL.md
  compatibility: Agent Skills / GitHub Copilot / Codex / MCP / OpenCode / Hermes
---

# LeeWay Skill Lifecycle Governance

## Core law

A living skill system must change without developing amnesia.

Usage frequency is not the same as importance, mastery, transfer value, or future usefulness.

Keep separate:

- `MASTERY` — verified quality when the capability is actually used;
- `ACTIVATION_PRIORITY` — how much full runtime attention it deserves now;
- `TRANSFERABILITY` — how broadly its primitives/patterns can support other work;
- `CRITICALITY` — consequence of not having it;
- `RECENCY` — freshness of the underlying technology/knowledge;
- `EVIDENCE_QUALITY` — strength of support;
- `COMPATIBILITY` — whether the current runtime can execute it.

Never lower mastery merely because a skill has not been used recently.

## Lifecycle states

- `CORE_ALWAYS_ON` — constitutional LeeWay skills; never decay by inactivity.
- `ACTIVE` — currently focal/recently verified.
- `WARM` — valid and likely useful, but not focal.
- `DORMANT` — full activation is low priority; primitives/transfer patterns remain ambiently eligible.
- `CANDIDATE` — newly discovered capability under evaluation.
- `SANDBOXED` — candidate being tested in controlled conditions.
- `VERIFIED` — evidence supports use; not necessarily default.
- `PROMOTED` — approved into the governed registry/manifold.
- `DEPRECATED` — superseded; retained for compatibility/reference.
- `RETIRED` — not routable by default; provenance retained.
- `QUARANTINED` — unsafe, unverified, contradictory, compromised, or blocked by provenance/license.

## Cooling law

Cooling affects **full-load/runtime priority**, not ambient reusable knowledge.

A skill may move:

`ACTIVE → WARM → DORMANT`

because of low focal relevance, replacement quality, stale dependencies, or sustained non-use.

But:

`DORMANT != ABSENT`

A dormant skill may still contribute a primitive, analogy, safety pattern, diagnostic method, teaching device, failure mode, verifier, or transfer edge through `leeway-universal-capability-kernel`.

Do not decay these solely from non-use:

- constitutional governance;
- safety/security/recovery;
- critical infrastructure;
- compliance/legal authority;
- disaster/failover;
- Creator-pinned skills.

## Emerging-skill pipeline

New technology must earn authority:

`DISCOVER → SOURCE → PROVENANCE → COMPATIBILITY → SANDBOX → BENCHMARK → VERITAS → RECEIPT → PROMOTE`

Preserve when available:

- technology/project identity;
- source repository/spec/publication;
- license;
- version/commit/release;
- maintenance activity/recency;
- security/trust boundary;
- runtime dependencies;
- overlap and primitive relationships with existing skills;
- benchmark/acceptance criteria;
- failure modes;
- promotion decision and receipt.

Unverified emerging skills remain `CANDIDATE` or `SANDBOXED`.

## Composition law

Do not model a task as "one skill selected." Use the Universal Capability Kernel.

For substantive work:

1. Keep all promoted skill metadata/primitives eligible in the `AMBIENT_CAPABILITY_FIELD`.
2. Build a `TASK_CAPABILITY_WEAVE` from every materially useful cross-domain primitive/pattern.
3. Resolve prerequisites, complements, conflicts, supersession, verifiers, fallbacks, and transfer relationships.
4. Expand full instructions only where deeper skill detail is necessary.
5. Build the `FOCAL_EXECUTION_SET` for actual tools/workflows/runtimes.
6. Allow the wider weave to continue shaping reasoning, safety, creativity, explanation, and verification.
7. Preserve shared provenance and receipt boundaries.
8. Promote successful combinations only after evidence.

A task may involve hundreds of micro-capabilities without executing hundreds of external runtimes.

## Transfer relationships

Supported relationships include:

- `shares_primitive_with`
- `transfers_pattern_to`
- `analogous_failure_mode_to`
- `analogous_safety_pattern_to`
- `requires`
- `supports`
- `verifies`
- `criticizes`
- `fallback_for`
- `supersedes`
- `conflicts_with`
- `teaches`
- `explains`
- `humanizes`
- `quantum_accelerable`
- `classical_fallback`

Analogy can nominate a transfer. Veritas determines whether it deserves lasting authority.

## Capacity law

The registry may grow to hundreds or thousands of skills.

Do not load every full `SKILL.md` into the prompt merely to claim they are available. Preserve a compact capability index/manifold so all promoted skills remain eligible, then expand details according to evidence and task need.

Preferred model:

`large persistent capability manifold + broad lightweight task weave + bounded focal execution`

not:

`large library + artificially tiny intelligence`

and not:

`load every full document every turn`.

## Revalidation

Revalidate a skill when material dependencies, standards, APIs, hardware models, security posture, licenses, or upstream behavior change.

Staleness may lower execution confidence/priority. It does not erase historical receipts or reusable conceptual primitives unless those primitives themselves are disproven.

## Learning boundary

Only verified outcomes may alter mastery, lifecycle promotion, or authoritative transfer relationships.

Popularity, model confidence, star counts, download counts, and frequency of mention are discovery signals, not capability proof.
