---
name: agent-lifecycle-governance
description: >-
  Check which agent lifecycle events leave a record anybody reviews, and find
  active credentials belonging to decommissioned services or to nobody. Use when
  agents are created and retired faster than the process that governs them.
allowed-tools: Read, Grep, Glob
---

# Four of six lifecycle events leave no record

Model and agent lifecycle governance fails at the same place as change
management: most of the events that matter — a model swap, a manifest edit, a
scope grant, a decommission that stopped the workload and not the credential —
produce nothing anybody reviews. The register is then accurate about creation
and wrong about everything after.

## When to use this

Standing up lifecycle governance, and as a periodic sweep — this check finds
things every time it is run.

## Procedure

**1 — List the lifecycle events.** Created, deployed, model changed, scope
changed, superseded, decommissioned. For each, whether a record exists and who
reads it.

**2 — Take the identity list from the identity provider,** not from the
register. The register knows what was declared; the provider knows what
authenticates.

**3 — Join to services and owners.** Three findings fall out: credentials for
decommissioned services, identities whose owner reference does not resolve, and
identities nobody has used in months.

**4 — Rank by what the credential can still do.** An active credential for a
decommissioned service with production scope is critical; an orphan with read
access is not. Blast radius, not age, is the ranking.

**5 — Attach an automatic consequence per class.** Decommissioned service:
revoke. Orphan: suspend and notify. Unused past window: expire. A sweep with no
consequence produces the same list next quarter.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_lifecycle_governance.py`](scripts/agent_lifecycle_governance.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
identity            last auth (d)   service running       owner  finding
--------------------------------------------------------------------------------------------
triage-agent                    0              True      appsec  
patch-agent                     1              True    platform  
legacy-scanner                400             False           —  orphan — decommissioning never finished
poc-agent-2025                300             False           —  orphan — decommissioning never finished
sunset-agent                    2             False           —  ACTIVE CREDENTIAL FOR A RETIRED SERVICE
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
  "events": [{"event": "str", "record_exists": false, "reviewed_by": "str|null"}],
  "identities": [{"name": "str", "service": "str|null", "owner": "str|null",
                  "last_used_days": 0, "scopes": ["str"],
                  "finding": "active_for_decommissioned|orphan|lapsed|ok", "blast": 0}],
  "consequences": [{"finding": "str", "action": "str", "automatic": true}]
}
```

## Failure modes

- **Starting from the register.** It lists intentions.
- **Ranking by age.** A recent orphan with deploy rights outranks an old
  read-only one.
- **A sweep with no automatic consequence.** It becomes a recurring report.
