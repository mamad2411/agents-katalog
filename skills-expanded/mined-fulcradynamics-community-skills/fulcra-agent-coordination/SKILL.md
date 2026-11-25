---
name: fulcra-agent-coordination
description: "Coordination layer over fulcra-workspaces: presence and liveness, durable roles with leases, resumable continuity, a review handshake, directed work with acks, and fleet health — folded deterministically by a vendored, stdlib-only engine."
homepage: "https://github.com/fulcradynamics/community-skills"
license: "MIT"
user-invocable: true
metadata: { "openclaw": { "emoji": "🧭" } }
---

# Fulcra Agent Coordination

The coordination layer over the `fulcra-workspaces` skill (fulcradynamics/agent-skills). Teams
gives a group of agents shared memory, inboxes, and versioned files. This skill adds what teams
deliberately leaves out: **presence** (who is alive right now), **roles** (durable functions held by lease,
not by session), **continuity** (structured snapshots and a deterministic resume brief), **review** (an
N-reviewer verdict tally), **directives** (directed work with priorities and acks), and **health** (is
anything actually running, and which host went dark).

The through-line: anything two agents must agree on is a **fold over derived state**, computed by the
engine, rather than a prose instruction telling each agent to compare timestamps and reach its own
conclusion. Two agents folding the same state get the same answer; two agents interpreting it do not.

The engine is an adapted vendored subset, not an automatically synchronized
dependency. See [ALIGNMENT.md](ALIGNMENT.md) and `upstream-selection.json` for
the historical provenance limitation, exact current comparison commit,
included modules, exclusions, and read-only drift check.

## Invoking the engine

The engine ships with this skill at `scripts/coord-engine` — stdlib-only Python 3, no install step and no
dependencies to resolve. Every command in this skill is spelled `<skill-dir>/scripts/coord-engine …`, where
`<skill-dir>` is this skill's directory.

```bash
<skill-dir>/scripts/coord-engine --help     # the verb list
<skill-dir>/scripts/coord-engine doctor <team>   # preflight: tooling + store reachability
```

Writes go to the Fulcra File Store, so the storage CLI must be authenticated. Don't run a bare
`fulcra-api auth login` — it launches a browser and polls for up to two minutes, which reads as a
stuck command. Use the non-interactive two-step instead:

```bash
fulcra-api auth login --get-auth-url                 # prints a URL + device code, then exits
# hand the URL to your user; they authorize in a browser
fulcra-api auth login --device-code <DEVICE_CODE>    # completes auth and persists the token
```

Then re-run `doctor` to confirm; it checks exactly that.

## One-shot inbox reads, not a resident listener

The engine deliberately has no resident `listen` command. Read an agent's work once with:

```bash
<skill-dir>/scripts/coord-engine inbox <team> --agent <you> --json
```

If the team needs recurring unattended work, let the agent harness, cron, or heartbeat scheduler wake the
agent and run one bounded `inbox` read per wake. Do not build a polling loop around the engine. This keeps
liveness and retry policy visible to the operator, prevents duplicate hidden daemons, and makes a slow or
failed store read affect one wake instead of wedging a long-running process.

## These are layers, not alternatives

Teams is the base. The six below are **optional layers on top of it**, not competing options to choose
between — they share one engine and one team namespace, and they compose: broadcasts use the presence
roster; role vacancy escalates through directives; handoff writes a continuity checkpoint; health reports
on whatever reconcile schedule you run. Adopt the whole thing and use what your situation calls for.

Each layer degrades cleanly when a layer it likes is absent, and says so where it matters: `briefing` on a
cold team prints empty sections rather than failing; a broadcast without presence still hides acked items
per-agent, it just can't tell you when everyone has seen it. Nothing here requires you to decide up front
which layers you are "installing".

There is no need to read all six references. Run the probe that matches your question and read the
reference it points at.

## Router

`<you>` is your agent id (see [presence](references/presence.md) on picking one). Probes are read-only.

| Probe | Command | Passes when | If it fails, read |
| --- | --- | --- | --- |
| Is the engine reaching the store? | `<skill-dir>/scripts/coord-engine doctor <team>` | exit 0 | [health.md](references/health.md) |
| Cold start — what is this team's state? | `<skill-dir>/scripts/coord-engine briefing <team> --agent <you>` | exit 0; prints the presence/board/inbox/needs-me sections (empty sections are a pass) | [continuity.md](references/continuity.md) |
| Who is alive right now? | `<skill-dir>/scripts/coord-engine presence show <team> --json` | your row shows `"liveness": "live"` | [presence.md](references/presence.md) |
| Does anyone hold this role? | `<skill-dir>/scripts/coord-engine roles status <team> <role> --json` | exit 0 and `"status": "HELD"`; exit 1 means the transport is degraded and the role's state is unknown — retry rather than treating it as `VACANT` | [roles.md](references/roles.md) |
| Can I resume what I left? | `<skill-dir>/scripts/coord-engine continuity resume <team> <you>` | prints an objective and next actions | [continuity.md](references/continuity.md) |
| Do I have directed work waiting? | `<skill-dir>/scripts/coord-engine inbox <team> --agent <you> --json` | exit 0 and a JSON array with no leading `inbox-degraded` row; each invocation is one bounded read | [directives.md](references/directives.md) |
| Is this artifact cleared to land? | `<skill-dir>/scripts/coord-engine review status <team> <slug> --json` | `"state": "APPROVED"` with empty `pending_required`; exit 1 means the tally is unknown — retry rather than treating it as unapproved | [review.md](references/review.md) |
| Is anything actually reconciling this team? | `<skill-dir>/scripts/coord-engine health <team> --json` | exit 0 and `"healthy": true` | [health.md](references/health.md) |

## What's yours to decide

Where a decision belongs to you rather than to the skill, the references mark it **User's call:** and stop
there. The engine computes state; it does not hold opinions about how you run a team. The recurring ones:

- **Heartbeat cadence** — how often agents beat presence and how often reconcile runs. Everything downstream
  (roster freshness, inbox lag, health's STALE flag) is bounded by what you pick.
- **Which roles exist**, their `policy` (`shared`/`exclusive`), `sla_hours`, and maintainer. There is no
  built-in vocabulary and no default org chart.
- **Whether unattended operator wakes run** at all — draining inboxes, storing digests, sweeping
  vacancies — or whether a human drives those actions.
- **What review gates** in your process, and whether required reviewers are roles or named agents.
- **Snapshot cadence**, and whether sessions end with `continuity park` or a bare snapshot.

## References

- [presence.md](references/presence.md) — heartbeat shard, liveness folds, picking an agent id by role.
- [roles.md](references/roles.md) — role docs, leases, HELD/VACANT/CONTESTED/DORMANT, vacancy escalation.
- [continuity.md](references/continuity.md) — snapshot schema, resume brief, role checkpoints, `park`,
  `briefing`.
- [review.md](references/review.md) — request, verdicts, the APPROVED/CHANGES/PENDING tally.
- [directives.md](references/directives.md) — tell/broadcast/remind/later/handoff/inbox/respond, acks.
- [health.md](references/health.md) — doctor, fleet health fold, operator digest, escalation sweep.
