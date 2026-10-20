---
name: slack-workflow
description: Wire delivery events into Slack without creating a channel nobody reads — channel taxonomy with owners, a suppression policy applied before any integration is built, Block Kit messages that lead with the ask, incident channel protocol, least-privilege bot scopes, and an alert-fatigue audit that measures the action rate instead of asserting noise. Use when connecting a tracker, pipeline or alerting system to Slack, before granting a bot token, or when a channel has become unreadable. Not for Slack app development, not for deciding what to build, not for reading channel history out of curiosity.
argument-hint: "[--design] [--audit] [--incident] [--channel \"#alerts-api\"] [--dry-run]"
user-invocable: true
agent: foundry-pmo:slack-operator
model: sonnet
effort: medium
metadata:
  foundry.vertical: management
  foundry.io: "handoff.v1 + risk.v1 -> Slack configuration + handoff.v1"
license: Apache-2.0
---

# Slack workflow

Attention is the budget. Every automated message spends some whether or not it was worth reading,
so the default answer to "should this post to Slack" is **no** and the message carries the burden
of proof.

`--dry-run` is the default for anything that writes. A posted message is not undoable in any
meaningful sense: people have read it, and deleting it leaves a visible gap.

## Step 0 — Preflight

```bash
curl -sS -H "Authorization: Bearer $SLACK_BOT_TOKEN" https://slack.com/api/auth.test
```

**Slack returns HTTP 200 even when the call failed.** Parse the `ok` field; on `false`, report the
`error` string verbatim (`not_in_channel`, `channel_not_found`, `missing_scope`, `ratelimited`).
Checking the exit status of `curl` proves nothing here, and this is the single most common way an
integration reports success while posting nothing.

Request the narrowest scopes that do the job: `chat:write` to post, `channels:read` to resolve
names, `reactions:write` to acknowledge. `channels:history` reads everything people said and is
requested only for a stated, time-boxed audit — say when it can be removed.

## Step 1 — `--design`

Decide the suppression policy **before** building any integration. Retrofitting it means asking a
team to tolerate noise while you tune, and they will mute the channel first.

An event earns a message only if all three hold:

1. **A human can act on it.** If the action is "nothing", it belongs in a dashboard.
2. **The right human sees it.** Posting to a channel the owner does not watch is theatre.
3. **It is not derivable from the previous message.** A recovery after a self-healing alert is
   noise; a state change nobody expected is not.

Channel taxonomy, each channel with a named owner:

| Prefix | Holds | Automated posts |
|---|---|---|
| `#team-<name>` | a standing team's conversation | none |
| `#proj-<name>` | one project, archived when it ships | milestones only |
| `#alerts-<service>` | machine-generated, actionable | yes — each links a runbook |
| `#deploys` | one line per deployment | yes |
| `#inc-<date>-<slug>` | one incident | yes |
| `#help-<topic>` | questions, with an owning rota | none |

Two rules do most of the work:

- **Alerts and discussion never share a channel.** Discussion buries alerts; alerts interrupt
  discussion. This split repairs more unreadable channels than any threshold tuning.
- **A channel with no owner gets archived**, not renamed or merged. Search still reaches archived
  content, so nothing is lost and the sidebar gets shorter.

Every `#alerts-*` message links a runbook. An alert nobody knows how to act on is noise wearing a
severity label — get the runbook written by `foundry-core:runbook-author` first, then wire the
alert.

## Step 2 — Message design

Block Kit, scanned rather than read.

```json
{
  "blocks": [
    { "type": "section", "text": { "type": "mrkdwn",
      "text": "*Checkout latency above budget* — p95 1.9s against a 1.2s budget.\n*Needed:* on-call to confirm whether to roll back build 4471." } },
    { "type": "context", "elements": [ { "type": "mrkdwn",
      "text": "service `checkout` · prod · breaching for 12m · <https://example.invalid/runbook/checkout-latency|runbook> · <https://example.invalid/dash/checkout|dashboard>" } ] }
  ]
}
```

- **The ask goes first**, before the context. Burying it guarantees it is missed.
- `context` carries metadata, never the ask.
- **Link artifacts; never paste them.** A log, a diff or a 400-line report makes the channel
  unusable for everyone who comes after.
- **Reply in the thread** of the originating message for updates on the same event. A new
  top-level message per update is the most common cause of an unreadable incident channel.
- `@channel` requires a stated justification — it wakes people. `@here` is narrower, not softer.

## Step 3 — `--audit`

Do not assert that a channel is noisy. Measure it over 30 days, with `channels:history` granted
for this purpose only:

| Metric | Reading |
|---|---|
| action rate | replies + reactions + threads ÷ messages. Below ~10% the channel is scrolled past, not read |
| duplication rate | messages differing only by id or timestamp — an alert firing per item that should batch |
| out-of-hours rate | non-incident messages outside working hours — attention spent with no way to act |

Then cut, in this order: suppress recoveries of self-healing alerts, batch per-item notifications
into a digest, delete alerts whose runbook says "no action", and only then tune thresholds.
Tuning thresholds first treats the symptom and leaves the volume roughly where it was.

Emit each surviving problem as `finding.v1` with the measured rate as evidence.

## Step 4 — `--incident`

Open `#inc-YYYYMMDD-<slug>` per incident, never a standing `#incidents`. A dedicated channel gives
the timeline a boundary and makes postmortem evidence gathering trivial.

Within the first minutes, **pin** three things: the current commander, the current status, and
customer impact in one sentence. Update the pin instead of posting status again. Everything else
goes in threads.

Archive after the postmortem is published and link it in the pin. The postmortem itself belongs to
`foundry-quality:sre-planner` — this skill only carries it to people.

## Step 5 — Rate limits and verification

Slack's chat-posting tier allows roughly one message per second per channel with short bursts.
A loop posting per item will be throttled, and will have deserved it — batch instead. Honour
`Retry-After` on `ratelimited`.

Before reporting success: confirm each message's `ok: true` and its `ts`, and confirm no token,
customer identifier or file content appears in any posted text.

## Refusals

- Posting to a channel not confirmed by name. A channel id resolved by fuzzy match is unconfirmed.
- Posting credentials, customer data, or the contents of a file not read in full.
- Joining a channel silently on `not_in_channel` — report it and give the invite command; joining
  is a visible act with social meaning.
- Reading channel history outside a stated, scoped audit.

## Privacy

Workspace retention, export policy and Discovery API access decide how long these messages live
and who reads them later. A bot posting customer identifiers into a channel with indefinite
retention has created a data-protection question. When personal data could appear in an automated
message, emit `finding.v1` and route the analysis to `foundry-legal:privacy-engineer`.

## Progressive disclosure

- `references/block-kit.md` — message patterns for alert, deploy, incident and digest.
- `references/scopes.md` — the scope table, what each grants, and how to ask for less.
- `references/alert-fatigue.md` — the audit queries and the suppression order.
