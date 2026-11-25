---
name: intent-brief
description: Compile the smallest applicable domain, contract, constraint, and live-claim context before repository work or landing. Use at intake and when scope or governing content changes; ordinary ungoverned work remains direct.
---

# intent-brief

Compile a read-only working envelope. Domains are semantic clusters inferred from the request,
code, and referenced material; never infer domain membership mechanically from a directory.

## Compile

1. Identify the requested outcomes and intended paths or interfaces.
2. Select only semantic domains that materially apply. For an ordinary local edit, selecting no
   domain is correct.
3. Run `scripts/resolve-config.sh` once and retain the integration target. Use
   `scripts/brief-support.sh reach --paths ... [--domain <id>]...` at intake.
4. Read `rows <domain...>` and retain `digest <domain...>` when domains apply. Audits and
   observations are evidence and never enter this digest.
5. Proceed directly unless a critical boundary must first be adopted or useful parallel work
   requires `intent-coordinate`.

Posture is:

- `local` — no accepted binding record intersects;
- `bounded` — accepted contracts or constraints apply;
- `open` — defining material, verification, or additive governance changes;
- `gated` — accepted governance is removed or rewritten.

Contracts supply executable verification. Constraints always require semantic compliance review
and may additionally supply commands. `resolution: assisted` asks only for a consequential
unresolved meaning; routine compliance remains agent work. Read
[references/intent-interview.md](references/intent-interview.md) only for such a resolution.

## Lifetime and landing

A brief remains usable until its domain-governance digest changes or its semantic scope expands.
Use `observe <digest> <domain...>` for freshness. Git supplies causal order; no timestamp decides
freshness.

Before landing, recompute reach from the exact diff, review every emitted constraint against the
prospective tree, collect affected verifiers, and pass scopes, domains, checks, and reviewed
constraint ids to `intent-land`.

Use [references/intent-review.md](references/intent-review.md) only when an independent semantic
review is useful.
