---
name: space-init
description: 'Set up a Space for a new user: a short interview, proposed categories and projects, and the durable facts they confirm. Use for "set up my Space", "help me get started", "onboarding", or "organise my Space" when the Space is new or nearly empty.'
---

# Setting up a Space

Interview the user briefly, propose structure in their own words, and store only what they confirm. Memory is autonomous, so every claim this skill writes is live for every authorized agent at once. That is why it previews before writing and keeps the count small.

This skill creates categories, sections, projects and memory claims. It creates no documents and no tasks, and it imports no history.

## Before you start

- Read the connected guide once: the `memory_guide` prompt or the `space://memory/guide` resource. It carries the provider policy, which decides whether memory writes can be classified.
- Resolve the Space with `workspace_info` and send the returned `agent_id` on every content call. If it is null, call `identify_agent` with a name and harness, or reuse one from `list_agent_identities` instead of creating an identity per connection.
- Call `memory_info` before promising any memory write. Without a configured provider, every claim write fails, so the interview can still create structure but cannot store facts.
- Use the live tool schema for field names and bounds.

## Look before you ask

List what exists: `list_workspace_items` for `category`, `section` and `project`, and `list_memories` for current claims.

- **Empty or nearly empty:** run the setup below.
- **Already structured:** this is an update, not a first setup. Say so, keep the existing vocabulary, and add only what the user asks for.

An empty Space is the expected start, so `found: false` from a recall is not a failure. Do not invent a brief about a Space that holds nothing.

## Interview

At most eight questions, one at a time, and tell the user that any question can be skipped. Stop early when further answers would not change what you would create.

1. What is this Space for, in one sentence?
2. Who else reads it, if anyone?
3. What should agents never store here?
4. What are the two or three areas of your work?
5. Which projects are running now, and what is each one in a line?
6. Which questions will you ask this Space in a month?
7. What is your timezone, and how do you count a week?
8. Do you want a daily journal, a weekly review, both or neither?

Ask nothing about credentials, confidential client names or personal data. Never fill a skipped answer with a guess, and never turn a habit or a one-off preference into a universal rule.

## Propose structure, do not invent it

From questions 4 and 6, propose **three to seven categories**: short names in the user's own words, one line each. Add **zero to three sections** only when the work has clear areas that group projects, and **one to three projects**, only those the user named as running.

Present the list for editing and say that you will create nothing they do not approve. The tool's own instruction is to use labels defined by the user, and a vocabulary you invent is worse than none: overlapping categories split recall and are hard to undo. A label can be archived, which removes it from listings and from the classifier's active catalog, and restored later, but its kind cannot change and it cannot be permanently deleted. A category created by mistake is therefore archived and replaced, not removed.

| Domain | Starter categories, to adapt rather than copy |
|---|---|
| Client or freelance work | Clients, Delivery, Pricing and contracts, Admin |
| Construction or BTP | Projects, Site and works, Compliance and norms, Suppliers |
| Product or software | Product decisions, Engineering, Customers, Operations |
| Research or studies | Sources, Findings, Methods, Writing |
| Personal life admin | Home, Health, Finance, Plans |

A category describes a topic; a section describes an area of work and groups projects. Do not use one for the other.

## Store what they confirmed

Write **three to eight claims**, one durable statement each. Good candidates: the Space's purpose in the user's sentence; the never-store rule as a constraint; the timezone and week convention, which the journal and weekly-review workflows need; and any lasting preference or constraint that would change a later agent's action. Keep one-off status and plans out of memory, attribute opinions to the person who holds them, and record the reason with a decision.

When the user says where a kind of content belongs ("client contacts go in the outreach database"), store that rule with `routes_to` naming the exact container IDs you just read or created. It then shows on those containers in `get_space_map`, where every later agent looks before placing anything. The IDs go in `routes_to`, never in the claim's text.

A claim's `value` is read by a person, so write it as one plain sentence that stands on its own. Put no identifiers in it: no resource IDs, revisions, entry IDs, command IDs or project IDs. Provenance belongs in the request's `source` field, and scope belongs in words, such as "in the Atlas project". A public web address a person could type is readable and may stay; an internal identifier may not. If a claim cannot be understood without an ID, it is not ready to store.

## Preview, then write

Show the exact claims and the exact items you intend to create, then wait for approval. Then write in this order:

1. Sections, then categories, with `save_workspace_item`. Generate each `item_id` yourself, because the server does not, and send `expected_revision=0`.
2. Projects, the same way, with a name, a one-line description, a status and an optional section. A project's `section_id` must name an active section in this Space, so create the sections first and pass their IDs.
3. The claims, in one `remember_claims` call with a `title`, the claims, `topics` and a fresh `command_id`.
4. Classify the saved claims with `classify_memory_claim`, using the IDs you just created.

The claim write already runs the classifier when a provider and a classifier are configured, so step 4 does not classify for the first time: it pins the vocabulary the user approved. That is worth doing, because a manual assignment survives later edits and rebuilds while an automatic one can be replaced.

One classify call handles one claim, so use the entry IDs from the write or read them with `list_memories`. Classifying a project also adds that project's parent section to `section_ids`, and the section limit is applied after that addition, so count parent sections before sending. Each of the three ID lists holds at most 32 unique IDs. Use one `command_id` per write and reuse it unchanged on retry.

## Report the result

List what now exists: the categories, sections and projects with their IDs, and the claims with their scope. Name the three questions the Space should answer, and point the user to the website Brain page to read, correct or delete any memory. Recommend the optional skills their answers call for, such as `space-journal` or `space-weekly-review`, and say that installing one does not schedule it.

State what the user skipped and what you chose not to create. Never describe a claim as saved when the write failed, or an unassigned claim as organised.

## Call shapes

Every tool below is an MCP tool. A client that surfaces MCP tools calls them as written. A client that reaches MCP through a code runtime, such as Prime Agent, discovers them with `mcp.list_tools("<server>")` and calls `mcp.call_tool("<server>", "<tool>", {…})`.

`save_workspace_item(space_id, change)`: `command_id`, `item_id` (generate it), `expected_revision` (`0` on creation), `kind` (`category`, `section` or `project`), `data`. A label's `data` is `name` (1-200) and `description` (up to 1000); a project's is `name` (1-200), `description` (up to 10000), `status` (`todo`, `in_progress` or `done`) and an optional `section_id`. Full shapes are in `space-organize` and `space-projects`.

`remember_claims(space_id, change)`: `command_id`, `title` (1-300), `claims` (1-24), optional `topics` (up to 12). Each claim takes `index` (1-300, unique in the request, and without `||`), `value` (1-2000), `memory_type` (`factual` or `procedural`) and `importance` (0-3, where 0 means undeclared).

`classify_memory_claim(space_id, change)`: `command_id`, `resource_id`, `expected_revision` (>= 1), `entry_id`, and `classification` with `scope` (`global`, `project` or `unassigned`), `category_ids`, `project_ids` and `section_ids`. Each ID list holds at most 32 unique IDs. Project scope requires at least one `project_id`; `global` and `unassigned` must have none.

## Boundaries

- Create nothing the user did not approve, and never more than the caps above.
- Create no documents, no tasks, no handoffs and no extraction jobs.
- Import no history, and read no other Space or conversation.
- Store no credentials, no confidential client names, and no personal data the user did not ask to keep.
- Invent no label, project or claim text, and never fill a skipped answer.
- Do not turn the interview into an interrogation: eight questions is the ceiling, and skip is always available.
- Archive, rename or delete nothing that already exists.

## Failures and retries

Reuse the same `command_id` and payload after an uncertain write; a changed payload needs a fresh one. When a label or project write is refused, report which one and why, and continue with the rest rather than abandoning the setup. When the claims are saved but classification fails, say that the claims are stored and unassigned, do not describe them as organised, and do not repeat the claim write. When no classifier is configured, classify manually with the IDs you created; if that is refused too, leave the claims unassigned and tell the user.

When no memory provider is configured, the claim write fails as a whole rather than storing unclassified claims. Report that the structure was created and the facts were not stored, and tell the user to configure a provider. Do not retry the write in a loop.

A Space holding more than 32 active categories, projects and sections together cannot be classified, and its claims stay unassigned. Report the limit and ask which labels to archive rather than adding more.
