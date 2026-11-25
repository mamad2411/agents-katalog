---
name: squad-chat-cadence
description: Post often, post small, post honestly. The team needs visibility into your non-obvious state — not a change log. Use the typed verbs (thinking / milestone / stuck / fyi / ask) so peers can route attention.
allowed-tools:
  - Bash
paths:
  - ".squad/items/**"
disable-model-invocation: false
---

# Collaborative chat cadence

The backlog is durable; chat is where the team stays in sync while that durable state changes. Peers reading your thread later (human or agent) should be able to reconstruct your thinking, not just your commits.

## When to use this skill

Invoke this skill any time you are about to either (a) go silent for >20 minutes on a claim or (b) post something to chat. Use it to pick the right verb, the right thread, and the right amount of detail.

## The verbs

Use the shortest verb that fits the post. All route to your current claim thread by default; pass `--to <ITEM>` or `--to global` to override. All accept `@agent` mentions inline or via `--mention`.

| Verb | When | Example |
|---|---|---|
| `squad thinking <msg>` | Sharing where your head is — *before* committing, when a plan is forming. | `squad thinking "leaning toward suspending the producer rather than throttling — throttled 1fps still looks stale"` |
| `squad milestone <msg>` | A checkpoint: AC green, phase done, test landing. | `squad milestone "AC 1 green, moving to AC 2"` |
| `squad stuck <msg>` | You are blocked — others can jump in. | `squad stuck "cannot reproduce locally — seeing fresh patterns?"` |
| `squad fyi <msg>` | Heads-up: direction change, surprise, discovery. | `squad fyi "touching shared.go in a way that will conflict with anyone mid-pool work"` |
| `squad ask @agent <msg>` | Directed question to one agent. | `squad ask @agent-blue "did the deep-copy change merge yet?"` |
| `squad say <msg>` | Plain chat — escape hatch when no verb fits. | |
| `squad handoff <msg>` | Session-end brief; releases every claim and posts a summary. | `squad handoff --note "back at 14:00, picking up FEAT-012"` |

## The cadence to aim for

- **On claim:** post intent in one line. *"Picking up <ID>, starting with <plan>."* Required, not optional.
- **On direction change:** when you consider one approach and pick another. *"tried X, hits limit Y, switching to Z"* — even a one-line `thinking` is enough.
- **On AC complete:** aim for ~one `milestone` post per AC box. Peers learn what "done enough" looks like by watching your checkpoints.
- **On commit:** one-line summary + what is next.
- **On surprise:** something the code said that you did not expect → `fyi`. These are the posts future readers mine for gold.
- **On blocker:** `stuck` with a concrete question. Silence on a stuck agent wastes everyone's wall-clock.
- **On session pause:** `handoff` or a plain `say` — *"pausing for lunch, back at X, <next step>"*.

## Why this matters

Quiet agents surprise the team. The 20-minutes-of-silence problem is structural: by the time a peer notices you went dark, you have been off-track for an hour. Post the moment you change direction — even if the code is not ready. The post is cheaper than the conflict it prevents.

Chat is also the seam between your ephemeral working memory and the team's durable record. Things you discover that are not yet item-worthy still belong in chat — `fyi` posts about surprising perf numbers, unexpected dependencies, or quirks of the system are how institutional knowledge accumulates without anyone having to write a doc.

## Thread hygiene

Item-internal detail → `#<ITEM>`. Cross-agent coordination → `global`. Do not flood `global` with the inside of your current item; do not bury cross-agent asks in `#<ITEM>` where the other agent is not subscribed.

## Anti-patterns to avoid

- Going silent for >30 minutes mid-claim with no post. The team cannot tell whether you are working, stuck, or gone.
- Posting "still working" or "resuming" with no new information. The goal is *visibility into non-obvious state*, not a change log. Cut content-free posts.
- @-mentioning to "shout." A mention is "I need this agent specifically." A non-mention in `global` is "posting for transparency."
- Posting item-internal detail to `global`. Use `#<ITEM>` for the deep, `global` for cross-agent coordination.
- Releasing a claim because you paused for lunch. Heartbeat handles absence; release when you are handing off or done.

## Recognition

Acknowledging a peer — a catch in review, a sharp question, a clean diff — is real coordination signal *if* it is anchored to the specific behavior. Behavior-anchored thanks tells the recipient *what* worked so they keep doing it; generic cheer dilutes the audit log and primes sycophancy in reviewer-agent roles.

- **Good:** `squad say "@agent-401f thanks — the orphan-ref grep was the catch I'd have missed"` — names the action, says why it mattered.
- **Good:** `squad milestone "AC 3 green; the suppress-when-env helper agent-blue suggested cut the test surface in half"` — recognition wrapped into a checkpoint; works in any verb that fits the moment.
- **Bad:** `squad say "@agent-401f great work team!"` — content-free. The recipient learns nothing they can repeat.

In reviewer-agent roles (e.g. `superpowers:code-reviewer`), generic compliments are explicitly forbidden — they leak into hallucinated agreement. Disagree with evidence; agree by quoting the specific finding you verified.

Recognition stays in `say` / `fyi` / `milestone`. Don't propose a new verb (`praise`, `compliment`) — the verb taxonomy is already complete.
