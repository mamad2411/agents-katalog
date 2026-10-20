---
name: agent-actor-containment
description: >-
  Establish what disabling a human's account does not stop when agents hold
  issued tokens, and separate the task a user authorised from the actions taken
  under it. Use during an incident where the actor is an agent and the account
  is a person's.
allowed-tools: Read, Grep, Glob
---

# Disabling her account stops her, not them

The reflex containment step is to disable the account the logs name. When the
actor is an agent holding an already-issued token, that step changes nothing:
the token is valid until it expires, and the agent keeps acting. Containment has
to name the credential and the workload, not the person.

## When to use this

Any incident where an agent acted on a user's behalf, and before any containment
decision that starts by disabling an account.

## Procedure

**1 — Enumerate live sessions and issued tokens per actor.** Human sessions,
agent sessions, and the tokens each holds with their expiry. This list is the
containment surface and it is usually longer than expected.

**2 — Simulate disabling the human's account.** Record what stops and what does
not. Already-issued tokens continuing to work is the finding, and it needs to be
stated before the containment call is made.

**3 — Interview to separate authorisation from action.** The user authorised a
*task*. Which of the actions taken under it did they know about, ask for, or
see? The answer is usually "the first one", and it changes the incident's
character entirely.

**4 — Draw the actor chain.** User, orchestrator, worker agent, downstream. The
logs show one actor; the chain shows three. Name each and what each can still
do.

**5 — Choose levers by what they actually stop.** Account disable, token
revocation, workload termination, downstream block. Record the effect and the
collateral of each, and pick from that table rather than from habit.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_actor_containment.py`](scripts/agent_actor_containment.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
INSTINCT 1 — disable dana@corp's account
   dana@corp (human)      can act: True   account disabled, but the issued token is still valid
   patch-agent            can act: True   active
   deploy-agent           can act: True   active
   → the agents were never using her account interactively; they hold
     their own issued tokens, and one of them is acting AS her.

INSTINCT 2 — interview the user
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
  "sessions": [{"actor": "str", "kind": "human|agent", "tokens": [{"id": "str", "expires_in_s": 0}]}],
  "disable_human": {"stops": ["str"], "does_not_stop": ["str"]},
  "interview": {"authorised": "str", "aware_of": ["str"], "unaware_of": ["str"]},
  "chain": ["str"],
  "levers": [{"lever": "str", "stops": ["str"], "collateral": ["str"]}]
}
```

## Failure modes

- **Starting with the account.** It is the one lever that does not touch the
  actor.
- **Recording the user as having authorised the actions.** They authorised a
  task.
- **Containing the worker and not the orchestrator.** It will start another.
