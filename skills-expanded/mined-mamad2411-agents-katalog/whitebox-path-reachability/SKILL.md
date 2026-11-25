---
name: whitebox-path-reachability
description: >-
  With source in hand, enumerate paths from real entry points to sinks and name
  the authorisation predicate on each, separating reachable sinks from merely
  present ones. Use for a white-box engagement, or when a scanner has produced a
  finding list nobody can act on.
allowed-tools: Read, Grep, Glob
---

# Presence is not reachability, and authentication is not authorisation

White box is the mode where you are handed everything, and the failure it
produces is specific: a long list of sinks that exist, with no statement about
whether anything can reach them or who is allowed to. That list is unactionable
in exactly the way a scanner's output is, which is a waste of the access you
were given.

Two distinctions do the work, and both are cheap once the paths are drawn.

## When to use this

A white-box engagement, a threat model that needs to be argued rather than
asserted, and any time a finding list is long and nobody is fixing it.

## Procedure

**1 — Write down what you were handed, and what each source establishes.**
Repository at a pinned commit, dependency lock, IaC plan, tool and MCP
manifests, IAM policy, API schema, prior findings. Naming the source per fact is
the difference between a finding and an assertion.

**2 — Enumerate paths, not sinks.** Entry point, every hop, the sink. A sink
with no path from any entry point is a different kind of object from one with
three.

**3 — Record the predicate on each hop, and classify it.** `session` and
`service_account` prove the caller is *somebody*. `owner==caller` and role
checks prove they are entitled to *this object*. A path carrying only the first
kind is the shape every BOLA finding has.

**4 — Report the unreachable sinks as unreachable, not as nothing.** They are
one route away from being findings, and the feature that adds the route will not
re-run this analysis on its own.

## Example

```
  AUTHN ONLY POST /refunds               handler -> svc.refund -> payments.refund
            authn: session   authz: NONE ON ANY HOP

sinks present in the tree      7
sinks reachable from an entry  5
  of those, authenticated only 3
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "data_sources": [{"source": "str", "establishes": "str"}],
  "paths": [{"entry": "str", "hops": [["str", "str|null"]], "sink": "str",
             "reachable": true, "authn": ["str"], "authz": ["str"]}],
  "counts": {"present": 0, "reachable": 0, "authn_only": 0, "unreachable": 0},
  "findings": [{"sink": "str", "entry": "str", "has": ["str"]}]
}
```

## Failure modes

- **Counting a session check as authorisation.** It is the single most common
  reason a BOLA survives a white-box engagement.
- **Dropping unreachable sinks.** They are the next release's findings.
- **Reporting sinks instead of paths.** A sink reachable three ways needs three
  fixes or one chokepoint, and the list does not say which.
- **Trusting the manifest over the code.** The manifest says what an agent may
  call; the call graph says what it does.
