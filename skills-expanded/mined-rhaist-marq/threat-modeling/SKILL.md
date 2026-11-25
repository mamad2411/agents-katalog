---
name: threat-modeling
description: "Covers threat modeling: the data-flow-diagram method, STRIDE, attack trees, PASTA, LINDDUN (privacy), when to model, turning threats into requirements and tests, and a worked mini-example. Use when the user asks to threat model a system, feature, API or architecture, wants a STRIDE analysis or DFD, needs privacy threat analysis, or asks how to fold threat modeling into design reviews."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Threat Modeling

Threat modeling is structured paranoia applied at **design time**: find the flaws before they're built, when fixing them costs a sentence in a doc instead of a release. Four questions drive every method (Shostack's frame): **What are we building? What can go wrong? What are we going to do about it? Did we do a good job?** Everything below is machinery for answering #2 systematically instead of by gut.

## When to model (and when not to)

- **Model when**: new system/feature touching a trust boundary, new data flow, handling sensitive/regulated data, a new external integration, or a major architecture change. Tie it into the **design review** so it's a gate, not a one-off offsite.
- **Don't** model every trivial change: reserve it for trust-boundary-crossing or high-blast-radius work.
- **Re-model** when the architecture or data flow changes; a threat model is a living artifact, not a PDF you file once.
- It's the design-phase input to the secure SDLC: `load_skill appsec-sdlc`.

## The data-flow-diagram (DFD) method: the workhorse

Most practical approach; STRIDE rides on top of it.

1. **Decompose** the system into: **external entities** (users, third-party APIs), **processes** (services), **data stores** (DBs, queues, buckets), **data flows** (arrows between them).
2. **Draw trust boundaries**: lines where privilege/control changes hands (internet↔DMZ, app↔DB, tenant A↔tenant B, user space↔kernel). **Threats cluster on the boundary crossings**; that's where to spend your attention.
3. Walk each element/flow and ask "what can go wrong here." STRIDE gives you the checklist.

## STRIDE: the default per-element checklist

Microsoft's classification; apply each letter to each DFD element. Each maps to the security property it violates.

| Threat                     | Violates        | Example                                   |
| -------------------------- | --------------- | ----------------------------------------- |
| **S**poofing               | Authentication  | Forged token, impersonated service        |
| **T**ampering              | Integrity       | Modified request/data in transit or store |
| **R**epudiation            | Non-repudiation | "I never did that": no audit trail        |
| **I**nformation disclosure | Confidentiality | Leaked PII, verbose errors, IDOR          |
| **D**enial of service      | Availability    | Resource exhaustion, lockout              |
| **E**levation of privilege | Authorization   | User→admin, container escape              |

These map directly to attacker techniques in the rest of the library: spoofing/EoP → auth/JWT flaws; info disclosure → IDOR; tampering/injection → SQLi, SSRF.

## The other methods: when STRIDE isn't the right tool

- **Attack trees**: goal at the root ("steal customer data"), refine into AND/OR sub-goals down to leaf techniques. Best for **deep-diving one critical asset** or red-team planning; complements STRIDE rather than replacing it.
- **PASTA** (Process for Attack Simulation and Threat Analysis): a 7-stage, **risk- and business-centric** method (define objectives → tech scope → app decomposition → threat analysis → vuln analysis → attack modeling → risk & impact). Heavyweight; use when threats must tie explicitly to **business impact** and you have a mature program. Output feeds `load_skill risk-assessment`.
- **LINDDUN**: the **privacy** counterpart to STRIDE; same DFD-driven approach, privacy threat categories: **L**inking, **I**dentifying, **N**on-repudiation, **D**etecting, **D**ata disclosure, **U**nawareness, **N**on-compliance. Use it (alongside STRIDE) whenever you process personal data: GDPR/HIPAA/CCPA scope. Has lightweight (Go) and exhaustive (Pro/Maestro) variants: `https://linddun.org`. Pairs with `load_skill privacy-eu`.

**Practical sequencing**: start with **STRIDE on a DFD** (covers most teams), add **LINDDUN** when personal data is involved, reach for **attack trees** on the crown-jewel asset, graduate to **PASTA** as the program matures and needs business-impact linkage. Don't adopt PASTA as a first move; it stalls immature teams.

## Turn threats into requirements and tests (the step teams skip)

A threat that doesn't produce an artifact was theater. For each accepted threat:

- Write a **security requirement** (ideally as an ASVS item: `load_skill appsec-sdlc`) or an **abuse/misuse case**.
- Decide the response: **mitigate** (add a control), **eliminate** (remove the feature/flow), **transfer** (offload), or **accept** (document, owner + sign-off).
- Create a **test** that proves the mitigation; it feeds DAST/integration suites and the pentest scope. The unmitigated/accepted ones become the target list for network / web testing.

## Worked mini-example: file-upload avatar feature

DFD: _Browser_ → (internet ‖ DMZ boundary) → _Upload service_ → _Object store_; thumbnail _Worker_ reads the store.

STRIDE walk on the upload flow:

- **S**: can an unauthenticated user upload? → require auth on the endpoint.
- **T**: can the file be a polyglot / malicious payload? → validate content-type + magic bytes, re-encode the image, strip metadata.
- **R**: is the upload attributed? → log uploader id + hash (audit trail).
- **I**: can I fetch _another_ user's avatar by guessing the URL? (IDOR) → authorize per-object access; unguessable ids.
- **D**: can a 10 GB upload or a decompression bomb exhaust the worker? → size limits, timeouts, resource caps.
- **E**: can the worker be made to fetch an internal URL (SSRF via image fetch) or execute the upload? → no server-side fetch of user URLs; sandbox the worker; store outside webroot, never execute uploads. (SSRF, path traversal)

LINDDUN overlay (personal data; the image may reveal identity/location): strip EXIF GPS (**Identifying/Detecting**), set retention + deletion (**Non-compliance**), tell the user what's stored (**Unawareness**).

Output: 6+ requirements, each with a test, before a line of code is written. That is the entire value: fix-in-design, not fix-in-prod.

## Rules

- Threats cluster on trust boundaries: draw them first, spend attention there.
- A threat with no requirement/test/accept-decision is wasted effort; every threat exits to an artifact.
- STRIDE for breadth, LINDDUN for privacy, attack trees for depth, PASTA for business-impact linkage: sequence, don't pick one forever.
- Make it a design-review gate and re-run on architecture change; a stale model is a false sense of safety.
