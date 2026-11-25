---
name: zero-trust
description: "Covers Zero Trust architecture per NIST SP 800-207: the seven tenets, PDP/PEP placement, identity-centric vs network-centric approaches, the CISA Zero Trust Maturity Model, and a pragmatic adoption order. Use when the user asks what zero trust actually means, how to plan or assess a ZTA program, replace VPN with ZTNA, assess maturity, or cut through zero-trust vendor claims."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Zero Trust Architecture (ZTA)

Zero Trust is a strategy, not a product. The core move: **stop trusting the network location**. A packet from inside the LAN gets no more trust than one from the internet; every request is authenticated, authorized, and encrypted per-session against dynamic policy. "Never trust, always verify" is the slogan; the substance is in where you put the decision and enforcement.

Canonical source: **NIST SP 800-207** (the ZTA reference, stable since 2020): fetch `https://csrc.nist.gov/pubs/sp/800/207/final`. Maturity model: **CISA Zero Trust Maturity Model v2.0** (April 2023, current as of 2026): fetch `https://www.cisa.gov/zero-trust-maturity-model`. Verify both are still current before citing in a deliverable.

## The seven tenets (NIST 800-207)

These are the test for "is this actually zero trust", not vendor marketing.

1. All data sources and compute services are **resources**.
2. All communication is **secured regardless of network location** (no implicit trust from the LAN).
3. Access is granted **per-session**, least-privilege, just-enough.
4. Access is determined by **dynamic policy**: identity, device posture, behavioral/environmental attributes, not a static ACL.
5. The enterprise **monitors and measures integrity/posture** of all owned + associated assets; no asset is inherently trusted.
6. Authentication and authorization are **strictly enforced before access**, and continually re-evaluated.
7. The enterprise **collects telemetry** on assets/traffic and uses it to improve posture (logging + continuous reassessment).

If a design grants standing trust to anything because of where it sits, it fails tenet 2.

## PDP / PEP: where the decision lives, where it's enforced

The whole architecture reduces to two logical components and one rule: **separate the decision from the enforcement.**

- **Policy Decision Point (PDP)**: the brain. Splits into **Policy Engine** (grants/denies using policy + signals: identity provider, device/posture, threat intel, SIEM) and **Policy Administrator** (issues/revokes the session credential/token).
- **Policy Enforcement Point (PEP)**: the gate. Sits inline between subject and resource; opens, monitors, and **terminates** the connection on the PDP's verdict. Re-checks continuously, not just at handshake.
- **Enforce at the PEP closest to the resource.** The further the PEP is from what it protects, the larger the implicit-trust zone behind it. A single perimeter PEP is just a firewall with extra steps.

Map this to your stack: PEP = identity-aware proxy / service mesh sidecar / SASE/ZTNA gateway / host agent; PDP = IdP + posture engine + policy service.

## Identity-centric vs network-centric

Two implementation approaches: pick deliberately, most mature programs converge on identity-centric.

- **Identity-centric**: the user/workload identity + device posture is the primary policy input; enforcement via identity-aware proxies, ZTNA, app-layer gates. Works across cloud/remote/BYOD; doesn't depend on owning the network. **Default choice today.**
- **Network-centric (microsegmentation)**: SDN/microsegmentation/NAC carve the network into per-workload segments; enforcement at network controls. Strong for east-west containment and OT/legacy that can't speak modern auth. See `load_skill network-segmentation`.
- They compose: identity decides _who/what_, segmentation shrinks the _blast radius_ when identity is bypassed. Don't treat segmentation alone as zero trust: without per-session auth it's tenet-2 noncompliant.

## CISA Zero Trust Maturity Model v2.0 (the assessment lens)

Use it to score current state and target state per pillar: same Current/Target gap method as `load_skill nist-csf`.

- **Five pillars**: Identity, Devices, Networks, Applications & Workloads, Data.
- **Three cross-cutting capabilities** woven through all pillars: Visibility & Analytics, Automation & Orchestration, Governance.
- **Four maturity stages**: Traditional → Initial → Advanced → Optimal. (v2.0 added the "Initial" stage; "five-stage" or no-governance answers are stale.)
- Score each pillar's functions across the stages; the gap to your target stage is the roadmap.

## Pragmatic adoption order (don't boil the ocean)

ZTA is a multi-year migration of an existing estate, never a greenfield rebuild. Sequence by leverage:

1. **Inventory first**: you can't protect resources you can't enumerate (tenet 1/5). Asset + identity + data-flow inventory. Cross-link `load_skill recon-footprint` for discovering the real attack surface.
2. **Fix identity**: strong phishing-resistant MFA (FIDO2/passkeys), kill standing privileged access, SSO everywhere. Highest ROI; most breaches are credential-driven.
3. **Device posture**: feed device health/compliance into the PDP as an access signal.
4. **Protect one high-value app**: front it with a PEP (identity-aware proxy/ZTNA), remove its network reachability. Prove the pattern, then repeat. Don't try to cover everything at once.
5. **Microsegment east-west** for the crown jewels: limit lateral movement (`load_skill network-segmentation`).
6. **Classify + protect data**: the innermost pillar; hardest, do it where it matters most.
7. **Continuous monitoring + automation**: feed telemetry back into dynamic policy (tenet 7). This is what separates "Advanced" from "Optimal".

## Rules

- A "zero trust" claim with a standing-trusted network zone is not zero trust: check it against tenet 2.
- PEP placement is the architecture decision that matters most; push it to the resource.
- Don't sell ZTA as a tool purchase. The vendor sells a PEP/PDP; the strategy is yours.
- Maturity-model scores are for direction, not a grade to max out: target the stage the risk justifies, per pillar.
