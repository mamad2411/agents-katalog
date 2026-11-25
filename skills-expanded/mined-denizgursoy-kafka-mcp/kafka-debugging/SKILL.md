---
name: kafka-debugging
description: Use when debugging a Kafka cluster through the kafka-mcp server — finding a message by id, key or field; measuring consumer lag and when a backlog clears; unblocking a stuck consumer; replaying messages since a moment; adding partitions; creating, reconfiguring or deleting a topic; producing a message; repairing many messages produced in the wrong shape; purging old messages or abandoned consumer groups; comparing two clusters; checking cluster health; finding why a group keeps rebalancing or one partition lags; diagnosing a schema change; or explaining an authorization error. Use for requests like "find the message for order 12345", "is there lag on orders", "the consumer is stuck", "which pod owns this partition", "reprocess everything since 9 this morning", "add partitions", "we need a dead letter topic", "cut retention on orders", "send a corrected message", "these messages came in wrapped in payload", "fix every message where", "reproduce this in preprod", "delete this topic", "delete the test data but keep the topic", "remove the old consumer groups", "are these two environments the same", "producers fail with NOT_ENOUGH_REPLICAS", "is the cluster healthy", "the consumer keeps rebalancing", "one partition always lags", "producer gets 409 incompatible schema", "is this schema change safe", "the disk is filling up", or "TOPIC_AUTHORIZATION_FAILED". Routes to the guide for the scenario, so read this before calling the tools.
---

# Kafka debugging

One guide per scenario. Read the guide for the scenario before calling
any Kafka tool: each one exists because the obvious sequence of calls gets the answer
wrong in a specific way.

## Read through MCP or local files

When `skill_reference` is available, read this skill from the copy built into
the server, so the guidance matches the running release. No local skill
installation or filesystem access is needed:

```json
{"items":[{"skill":"kafka-debugging"}]}
```

Then read the chosen guide with the same tool, for example:

```json
{"items":[{"skill":"kafka-debugging","file":"references/check-lag.md"}]}
```

The optional `file` defaults to `SKILL.md`. Each result contains the full
Markdown and a sorted `files` catalog. Names are exact and case-sensitive,
relative to the skill root. Resolve links inside a guide relative to that
guide: `replay-messages.md` inside `references/check-lag.md` means
`references/replay-messages.md`. Do not send `..` path segments.

If the endpoint withholds `skill_reference`, use the installed local skill
files instead. Reading a guide does not make its tools available: still check
`server_config` before promising a change.

## Pick the guide

| The user is asking | Guide |
| ------------------ | ----- |
| Where a message is, by id, key or a field condition | [find-message](references/find-message.md) |
| Whether consumers are behind, how fast, when it clears | [check-lag](references/check-lag.md) |
| Why a consumer is stuck, and how to get it moving | [skip-poison-message](references/skip-poison-message.md) |
| Whether to add partitions, and doing it safely | [scale-partitions](references/scale-partitions.md) |
| For a new topic, with a partition count and retention chosen on purpose | [create-topic](references/create-topic.md) |
| To write a message: repaired, reproduced elsewhere, or seeded | [produce-message](references/produce-message.md) |
| To fix many messages produced in the wrong shape and write them again | [repair-messages](references/repair-messages.md) |
| What differs between two clusters, or to create what one is missing | [compare-clusters](references/compare-clusters.md) |
| To remove a topic and everything in it | [delete-topic](references/delete-topic.md) |
| To reprocess messages since a moment, or from the start | [replay-messages](references/replay-messages.md) |
| To change retention, cleanup policy or message size on a topic | [tune-topic-config](references/tune-topic-config.md) |
| Whether brokers and partitions are healthy, or why producers get NOT_ENOUGH_REPLICAS | [cluster-health](references/cluster-health.md) |
| To delete old messages but keep the topic, or remove abandoned groups | [purge-messages](references/purge-messages.md) |
| Why a client is refused with an authorization error | [authorization-error](references/authorization-error.md) |
| Why a group keeps rebalancing, or members keep leaving | [unstable-consumer-group](references/unstable-consumer-group.md) |
| Why one partition lags while the others keep up | [partition-skew](references/partition-skew.md) |
| Whether a schema change is safe, or why producers or consumers broke on one | [schema-error](references/schema-error.md) |

## When "the consumer is behind" is ambiguous

Three of these guides answer the same opening complaint, and picking between
them by wording is guesswork. Call `consumer_lag` first and let `status` decide:

| `status` | What it means | Where to go |
| -------- | ------------- | ----------- |
| `caught_up` | There is no lag | Answer and stop |
| `draining` | Working, just slower than the user hoped | [check-lag](references/check-lag.md) for the ETA |
| `growing` | Consumers cannot keep up at all | [scale-partitions](references/scale-partitions.md) |
| `stalled` | Members present, consuming nothing | [skip-poison-message](references/skip-poison-message.md), which checks `open_transactions` first |
| `no_active_consumers` | Nobody is running | Say so: starting a consumer is the fix |

Before reading `status`, check three things that override it:

- any partition with **`offset_expired`**: retention deleted the group's
  position, and the fix is where it resumes → [replay-messages](references/replay-messages.md)
- lag concentrated on **one partition** → [partition-skew](references/partition-skew.md)
- a **state other than `Stable`** that keeps returning →
  [unstable-consumer-group](references/unstable-consumer-group.md)

Adding partitions to a `stalled` group, or skipping a message from a `growing`
one, is the common way this goes wrong. One destroys data for a capacity
problem; the other adds capacity to a consumer that is not consuming.

## Rules that apply to every guide

**One endpoint targets one cluster.** Several endpoints may target the same
cluster with different paths, purposes and permissions. Every tool is bound to
the cluster and policy of the endpoint it was called on. No tool takes a cluster
parameter, except `copy_message`, `produce_message` and `transform_messages`,
which choose a destination, `compare_clusters`, which names the cluster to compare against, and
`list_clusters`, which reports the roster. A destination must be one this
endpoint lists in its `destinations` (reported by `server_config`); a cluster
another endpoint may write to is not thereby writable from this one.

**Check `server_config` before promising a change.** A read-only endpoint does
not expose `add_partitions`, `alter_topic_config`, `commit_offset`,
`create_topic`, `delete_consumer_group`, `delete_records` or `delete_topic` at
all, and any
endpoint may withhold individual tools through its configuration, so there is no
refusal to discover and no preview to fall back on. Its `tools` list is what
this endpoint actually has. Find out at the start, not after the user has
already stopped their consumers.

**Never guess a topic.** If the user did not name one, call `list_topics` and
ask when several are plausible. Answering confidently about the wrong topic is
worse than one more question.

**Report partition and offset with any message.** That triple is what
identifies a message for every follow-up call; content alone does not.

**Read `format` before trusting a value.** Avro, Protobuf and JSON Schema
messages are shown decoded to JSON, with `schema_id` saying which schema; a
`decode_error` means the server could not decode it, and base64 there is not
the message's real content. Never write JSON back into a schema-encoded topic
without `value_schema` — see [produce-message](references/produce-message.md).

**Every target is an `items` array.** The tools that operate on a named topic,
partition, offset or group take it only inside `items` — there is no
single-target form, so one operation is an array of length one and several are
the same call with more entries. Never make one call per topic when one call
can carry them all. The exceptions are tools whose one call is already a scan
or a filter: `search_messages` and `transform_messages` take `topic` at the top
level, `produce_message` can take an `upload` instead of `items`, and
`list_consumer_groups` takes an optional `topic` filter. Check a tool's schema
rather than assuming.

Responses match: results stay in input order, each with `index` and either
`result` or `error`, so one item failing never hides the rest. Read the item's
own result rather than assuming the call succeeded or failed as a whole.

A write batch is never atomic: preview it first, explain every valid change, and
set the one top-level `confirm` only after the user approves the whole set.

**Files live on the user's machine.** `download` and `upload` never store
anything on the server. Over stdio the file is saved or read at once and the
response gives its `path`; tell the user where it is. Over HTTP the response
carries a `command` (`curl`): run it on the user's machine, in the directory
they want the file in, and report what it printed. The link in it expires
after ten minutes and is a secret until then; run an upload command once,
because running it again sends the file again.

**Say what was not measured.** An incomplete scan, an unsampled rate, a
partition returning an error — each is a different answer from "nothing there",
and reporting it as absence is how these investigations produce confident wrong
conclusions.
