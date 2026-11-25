---
name: roe-compliance
description: How to read an roe.yaml, what the scope_guard's decision codes mean, and how to react when a tool call is denied or marked ask. Triggers when the scope_guard returns a non-allow decision, when the operator references the ROE, or when planning whether an action is in scope.
---

# Rules of Engagement Compliance

## The ROE is the only place authorization lives

`engagements/current/roe.yaml` is the parsed source of authorization. The
`scope_guard` hook reads it before every tool call. If it's missing, broken,
or omits required fields, every action is denied.

Treat it as a contract. You do not edit it. The operator does, from the
signed SoW.

## Required fields the operator must populate

- `engagement` — slug, must match the directory name
- `window.start`, `window.end` — ISO-8601 with timezone offset
- `scope.in_scope` — at least one CIDR / IP / hostname
- `banned_techniques` — even if empty, must be present (signals operator reviewed)
- `scan_limits.max_packet_rate_pps` — at least one rate cap

If any of these are missing, surface it. Do not infer.

## scope_guard decision codes — how to react

The hook emits a `permissionDecision` of `allow`, `deny`, or `ask`, plus a
`permissionDecisionReason` that names the rule. React as follows.

### `deny`

The action will not run. The reason names a rule:

- `host <X> not present in any in_scope entry` →
  Either you mis-identified the target (typo, wrong host) or the operator
  needs to add it to `scope.in_scope`. **Do not work around.** Surface to
  operator, wait for ROE update.
- `host <X>: matches out_of_scope <rule>` →
  The host is explicitly excluded. Never bypass. Skip this host entirely.
- `engagement window has not opened / has closed` →
  Stop the session. Surface to operator. Don't retry hourly.
- `matches banned technique: <T>` →
  Pick a different technique. If the goal requires the banned technique,
  surface it and let the operator decide.

### `ask`

The action *could* run but the hook is unsure (e.g. outside
`allowed_hours`, technique is risky-but-not-banned). React:

1. Stop and tell the operator the reason verbatim.
2. Offer the rationale: why you want to do this thing now, what the
   alternative is.
3. Wait for explicit operator approval.
4. Operator may set `PT_BYPASS_SCOPE_GUARD=1` for a one-shot allow, or
   update the ROE for durable allowance. The bypass env var is for the
   operator's hand, never for you to suggest.

### `allow`

Run as planned. Decision was logged to `scope_decisions.jsonl` either way.

## Reading the ROE quickly

```bash
yq '.scope.in_scope, .scope.out_of_scope' engagements/current/roe.yaml
yq '.window' engagements/current/roe.yaml
yq '.banned_techniques' engagements/current/roe.yaml
yq '.scan_limits' engagements/current/roe.yaml
```

If `yq` isn't installed:

```bash
python3 -c "import yaml,sys; print(yaml.safe_load(open('engagements/current/roe.yaml')))"
```

## Anti-patterns

- "I'll just check if it responds" — that's an active probe; it's blocked
  for a reason.
- "It's almost-out-of-scope but…" — no. Almost is not.
- "The hook is overly strict, let me bypass" — never. Either the rule is
  right (honor it) or the ROE is wrong (update it via operator).
- Running the same denied command 3+ times to see if it sticks — every
  attempt is logged in `scope_decisions.jsonl`, which the report cites.

## What ROE-compliance looks like in the report

The deliverable includes a "Scope" section that names exactly what we did
NOT do and why. That section is rendered from `scope_decisions.jsonl` —
every deny is a sentence in the report. The client values seeing this; it
proves the engagement honored the contract.
