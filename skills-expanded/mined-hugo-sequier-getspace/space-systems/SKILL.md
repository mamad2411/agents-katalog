---
name: space-systems
description: Run recurring work through Space Systems, reading and applying verdicts first, putting new ideas and lessons in the system's lab, and reviewing systems at their cadence. Use before recurring work such as posts, outreach, SEO or a dev lane, for "what works for X?", "log this lesson", "test this idea", "review the X system", "promote this lesson" or "this no longer works".
---

# Systems and the lab

A system is work the person repeats, such as X posting, cold email, an SEO routine or a development lane, with a goal metric, a target, a health status and a playbook document. Its lab holds hypotheses and lessons under test. Only verdicts reach recall: entries promoted to Validated (label `works`, a rule or tactic) or Invalidated (label `does_not_work`, an anti-pattern). This skill reads and applies verdicts, records their use, adds lab entries, and reviews systems. It never saves an untested idea as memory, and it never promotes on its own judgement.

## Before you start

- Read the connected guide once: the `memory_guide` prompt or the `space://memory/guide` resource, and resolve the Space with `workspace_info`.
- Send the returned `agent_id` on every content call.
- Use the live tool schema for field names and bounds.

## Before recurring work: apply the verdicts

1. Find the system: `list_systems` returns every system with its goal, status and lab statistics, and every lab entry. Match the work to a system by name or goal; if none fits, ask rather than guessing.
2. Read its verdicts: `list_verdicts` with `query.system_id`, or `query.domain` when the work spans systems (domains: Copy & hooks, Social, Outreach & sales, SEO/GEO, Product & positioning, Dev & engineering, Agents & automation, Video, Ops & business). `get_context` also returns verdicts, each with a `verdict` object, when the topic matches.
3. Apply them. A `works` verdict is a rule or tactic to follow; a `does_not_work` verdict is an anti-pattern to avoid. Read `apply` and `applies_to`: a verdict from one channel or project is a hypothesis elsewhere until measured there.
4. When a verdict shaped the output, call `record_verdict_use` with `used_in` naming the output, such as "X post on the 4 November launch" or "Predella cohort 6 first emails". Record it once per output, after the output exists. This is what the system's reuse share counts.

Testing entries are ideas, not rules: you may read them to avoid duplicating one, but do not present them as what works.

## When something is learned: add it to the lab

Put a new hypothesis, a one-off result or an unmeasured lesson in the lab with `add_lab_entry`, not in memory:

- `name`: the hypothesis or lesson in one plain sentence that stands on its own, at most 280 characters.
- `system_id` and `domain`: the system that tests it and the closest domain.
- `evidence`: `untested` for an idea, `suggestive` for a result too small or confounded to rely on, `measured` for a result against the system's metric with a comparison, `owner_call` when the person decides it as a rule.
- `why`: the evidence and numbers; `apply`: how to use it; `applies_to`: where it may transfer; `source`: where the evidence is (a review, a dataset, a session, a post), required for promotion.

Read `list_systems` first and update an existing entry rather than adding a duplicate. When new evidence arrives for a testing entry, call `update_lab_entry` with all its fields and a `note` saying what changed, such as "Cohort 5: 3.1x median on 12 posts".

## Review a system

At the system's `review_cadence`, or when the person asks:

1. Read the system and its entries with `list_systems`, and the latest numbers from its `source_of_truth`.
2. Update the system with `update_system`: `current_value`, `status` (healthy, needs_attention, broken, not_measured, paused), `last_review` as today's date and `next_decision`. Send every field, keeping the ones that did not change.
3. Go through the testing entries. Propose which can become verdicts and why, which stay in testing, and which to retire. Report the system's `reuse_share` against the 30% target, and the verdicts never used.
4. Promote or demote only what the evidence supports, as below. When the person reviews with you, apply their calls.

## Promote and demote

`promote_lab_entry` with `verdict="validated"` (it works) or `verdict="invalidated"` (it does not work) makes the entry a verdict that recall returns. The person and their agents can both promote. Promote only on evidence: the evidence is `measured` or `owner_call`, the `source` is named and the system is active, otherwise the call is refused with what is missing. A measured comparison against the system's metric, or the person's explicit decision, is evidence. Your own opinion of an idea is not.

`demote_lab_entry` with `status="testing"` retries an entry, and `status="retired"` stops it. A verdict leaves recall at once and its history stays. Demote when new evidence contradicts a verdict, and say why in `note`. A verdict cannot be edited: move it back to testing, update it, then promote it again.

## Report the result

Name the system, what you did (verdicts applied with their labels, uses recorded, entries added or updated, promotions and demotions with their evidence), and the system's reuse share after the change. Report a refused promotion with the reason the server gave.

## Call shapes

Every tool below is an MCP tool. A client that surfaces MCP tools calls them as written. A client that reaches MCP through a code runtime, such as Prime Agent, discovers them with `mcp.list_tools("<server>")` and calls `mcp.call_tool("<server>", "<tool>", {…})`.

| Tool | Arguments | Returns |
|---|---|---|
| `list_systems` | `space_id` | `systems` (each with `stats`: `entries`, `testing`, `works`, `does_not_work`, `retired`, `verdicts`, `reused_30d`, `reuse_share`), `entries` newest first, `domains` |
| `list_verdicts` | `space_id`, optional `query` with `system_id` or `domain` | `systems` with their stats, `verdicts` with `label`, `evidence_label`, `system_name`, `reused_30d` and `url` |
| `create_system` | `space_id`, `command_id`, `data` | The system |
| `update_system` | `space_id`, `system_id`, `expected_revision`, `command_id`, `data` with every field | The system |
| `add_lab_entry` | `space_id`, `command_id`, `data` | The entry, in testing |
| `update_lab_entry` | `space_id`, `entry_id`, `expected_revision`, `command_id`, `data` with every field | The entry |
| `promote_lab_entry` | `space_id`, `entry_id`, `request`: `command_id`, `expected_revision`, `verdict`, optional `note` | The entry as a verdict |
| `demote_lab_entry` | `space_id`, `entry_id`, `request`: `command_id`, `expected_revision`, `status` (`testing` or `retired`), optional `note` | The entry |
| `record_verdict_use` | `space_id`, `entry_id`, `request`: `command_id`, `expected_revision`, `used_in` (1-500 characters) | The entry with `uses` and `last_used` |

System `data`: `name` (1-200, required), `description` (up to 10000), `status` (default `not_measured`), `goal_metric`, `current_value`, `counter_metric`, `source_of_truth`, `next_decision` (each up to 2000), `goal_target` (up to 500), `review_cadence` (`weekly`, `per_cohort`, `monthly`, `quarterly` or null), `last_review` (ISO date or null), `playbook_id` (a document's ID or null).

Lab entry `data`: `name` (1-280), `system_id`, `domain`, `evidence` (default `untested`), `why` and `apply` (up to 4000 each), `applies_to` and `source` (up to 1000 each), `captured` (ISO date or null), `note` (up to 2000, what this revision changed). Status, uses and the verdict change only through promotion, demotion and recorded uses.

`expected_revision` is the entry's or system's current `revision`, from `list_systems` or the last response.

## Boundaries

- Do not save an idea, a hypothesis or an unmeasured lesson with `remember`; add it to the lab.
- Do not promote on your own judgement, on a single anecdote, or with an invented source.
- Do not present a testing entry as a rule.
- Do not record a use for a verdict you only read.
- Do not create a system the person did not ask for; propose it.
- Do not archive an entry to hide a result; retire it with a note.

## Failures and retries

Reuse the same `command_id` and payload after an uncertain write; a retried promotion lands on the same verdict. A changed payload needs a fresh command ID. On a revision conflict, read the entry again with `list_systems` and rebuild the change from it. A refused promotion names what is missing: report it, or set the evidence and source if the person supplies them. A promotion needs the memory provider; if it is unavailable, the entry stays in testing and you report that.
