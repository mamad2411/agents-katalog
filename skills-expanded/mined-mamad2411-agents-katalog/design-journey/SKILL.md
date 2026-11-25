---
name: design-journey
description: Use when the user wants to build, design, review, debug, or understand a Boom journey — the workflow graph behind an initiative that controls which template is sent, how long to wait, when the AI converses, follow-up rounds, branching by customer attributes, calling an external endpoint, or scheduling. Triggers on "build a journey", "follow-up rounds", "workflow", "why didn't the second message send", "branch by plan/attribute", "call our API from the journey", "re-engage after timeout".
---

# Design a Journey

A journey is the versioned workflow graph that runs each participant through an initiative: nodes emit **signals**, edges route on them. You can author a journey end-to-end through the MCP — create a draft, add and connect nodes, set the trigger, validate, and publish — or review and debug an existing one. Journeys can also be edited in Boom's visual builder; the MCP and the builder operate on the same graph, so you can hand off in either direction.

Your job with this skill: *build or debug the graph precisely*, then either publish it or give the user an exact node-by-node spec they can finish in the builder.

## Tools used

| Tool | Purpose | Scope |
|---|---|---|
| `journeys_list` / `journeys_get` / `journeys_get_definition` | Read a journey's versions and its full node + edge definition | read |
| `journeys_authoring_catalog` | The machine-readable node-kind catalog (kinds, inputs, output signals) — read this before building | read |
| `journeys_condition_catalog` / `journeys_event_catalog` | Valid DECISION predicate terms and dispatchable/reserved event names | read |
| `journeys_message_channels` / `journeys_message_templates` | Sending channel ids and approved template ids for SEND_MESSAGE | read |
| `journeys_email_templates` | What a SEND_EMAIL node needs: the PUBLISHED email templates, the org's email readiness, and the From / Reply-To senders (email has no `channelId`) | read |
| `journeys_message_variables` | The exact variable paths a SEND_MESSAGE template binding can reference for a journey (`customer.*`, `person.<key>`, and run-produced values) — read this before binding placeholders | read |
| `journeys_create_draft` / `journeys_create_draft_from_published` | Start a new editable draft (blank or copied from the live version) | write |
| `journeys_add_node` / `journeys_update_node` / `journeys_delete_node` | Add, edit, or remove a node | write |
| `journeys_connect_nodes` / `journeys_disconnect_nodes` | Wire (or unwire) an edge on a specific signal handle | write |
| `journeys_set_trigger` | Set how people enter (manual / segment / cdp_event); segment triggers can't be wired from here, see step 4 below | write |
| `journeys_update_draft` | Replace the whole draft definition at once | write |
| `journeys_validate` | Check a draft against the publish rules without going live | read |
| `journeys_publish` | Publish the draft — **this goes live to real customers**; confirm first | write |
| `drafts_list` / `drafts_get` / `drafts_count` / `drafts_decide` | Review sends held for approval (`delivery: "draft"`), size a bulk decide, and approve or reject them. **Approving sends real messages**; see "Hold sends for approval" | read / write |
| `initiatives_get` | The initiative the journey belongs to | read |

Tool names follow `domain_action`; if a call fails with `tool_not_found`, list available tools and match by that pattern.

## Node kinds and the signals they emit

| Kind | Group | Purpose | Key inputs | Emits |
|---|---|---|---|---|
| `ENTRY` | trigger | How people enroll | `triggerType: manual \| segment \| cdp_event`; `segmentId` / `eventName`; optional frequency cap `maxEnrollments` + `enrollmentWindow` | `SENT` |
| `SEND_MESSAGE` | action | Send a WhatsApp template | `templateId` **and** `channelId` (both required to publish), `templateBindings` (see "Bind your variables"), optional `delivery: immediate \| draft` (see "Hold sends for approval") | `SENT`; `SKIPPED` (optional: Smart Sending's cap refused the send); `REJECTED` (only with `delivery: "draft"`, optional) |
| `SEND_EMAIL` | action | Send a PUBLISHED email template (outbound only) | `templateId` (required to publish), optional `bindings`, `fromSenderIdOverride` / `replyToSenderIdOverride`, optional `delivery: immediate \| draft` | `SENT`; `SKIPPED` (optional: Smart Sending's cap); `REJECTED` (only with `delivery: "draft"`, optional) |
| `WAIT_FOR_REPLY` | action | Passive wait for the first reply (no AI) | `maxTimeout` | `REPLIED`, `TIMEOUT` |
| `MANAGE_CONVERSATION` | action | The AI-led conversation | `mode: AGENT \| ESCALATE`, optional `goal` (instructions for this step only; AGENT-mode only, see "Step goals"), optional `inactivityTimeout` (any value up to `24h`, under `30m` allowed but flagged; AGENT-mode only, and gated by the `journey-inactivity-timeout` flag — without it the node falls back to a single 7-day wait) | `CLOSED`, `STALE` — a configured `inactivityTimeout` *closes* the conversation, so it routes `CLOSED`; there is no separate inactivity handle |
| `CONVERSATION_BLOCK` | action | **Legacy** combined wait + AI conversation | `mode`, `maxTimeout`, `goal` | `CLOSED`, `TIMEOUT`, `STALE` |
| `DELAY` | logic | Wait | `mode: duration` (`2d`) \| `until_date` (ISO instant) \| `until_weekday` (weekdays + time window + IANA timezone) | `SENT` |
| `DECISION` | logic | Two-way branch | `logic: AND \| OR` + conditions: person attribute predicate, event occurred, custom-object match, or a runtime value | `YES`, `NO` |
| `CASE` | logic | Multi-way switch on one person attribute (≤10 branches) | `selectionPath` + `branches[]`; a wired **default** is mandatory | `case:<branchId>` + `case:default` |
| `HTTP_REQUEST` | action | Call an external endpoint (your API / a webhook) | `method`, `url` (supports `{{variable}}`), `headers`, `body`, `credentialId`, `timeoutMs` (≤30s), `maxAttempts` (≤5) | `SUCCESS`, `FAILED` |
| `DISPATCH_EVENT` | action | Record a CDP event for the person | `eventName`, static or bound `properties` | `SENT` |
| `EXIT` | terminal | End the journey | optional `outcome` label; optional `nextInitiativeId` to chain into another initiative | — |

For new journeys, prefer **`WAIT_FOR_REPLY` + `MANAGE_CONVERSATION`** over the legacy `CONVERSATION_BLOCK` — the split gives you separate handles for "never replied" (`TIMEOUT`) vs "replied then the AI closed the conversation" (`CLOSED`), which most follow-up logic needs.

**`SEND_EMAIL` has no reply of its own**, so its successor may not be `WAIT_FOR_REPLY`, `MANAGE_CONVERSATION` or `CONVERSATION_BLOCK` (`SEND_EMAIL_INVALID_SUCCESSOR`). Follow it with a `DELAY`, an `EXIT`, or another send/logic node. Publish refuses it unless its template is PUBLISHED and a From address resolves: `readiness.verified` and `readiness.hasSender` in `journeys_email_templates`, or a `fromSenderIdOverride` that is `usableAsFrom`. Templates are authored with `email_templates_create` / `email_templates_update`, not the WhatsApp `templates_*` tools; see [`email-templates`](../email-templates/SKILL.md).

Routing rule: an edge fires when its `sourceHandle` equals the signal the node emitted. **Every required signal must have exactly one outgoing edge**, which is the #1 publish error. Two handles are optional: `SKIPPED` and `REJECTED` on a send node. Left unwired, the run ends quietly there.

## Step goals

A `MANAGE_CONVERSATION` in `mode: AGENT` can carry a `goal`: instructions the agent follows **during this step only**, on top of the initiative's objective. The initiative objective says what the whole conversation is for; the step goal says what to do first at this point in the journey.

- **Write it as one concrete instruction.** Good: `"Confirma la dirección de entrega antes de responder cualquier otra cosa."` Bad: restating the objective, or a paragraph of tone rules (those belong on the initiative).
- **It narrows the objective, it never adds a second one.** If the step needs a different job, that is a second initiative (see "One objective per initiative").
- **Set it** with `journeys_add_node` (in the node's `inputs`) or `journeys_update_node` with `inputs: { "goal": "..." }`, which merges into the existing config. **Read it back** with `journeys_get_definition`. Clear it by sending an empty string.
- **ESCALATE ignores it**: a human handoff has no agent to instruct. The stored value is kept, so switching back to AGENT restores it.
- **It reaches new runs only.** Runs are pinned to the version they enrolled on, so editing a goal means `journeys_create_draft_from_published`, edit, publish, and only people who enroll after that get the new instructions.
- Different steps can carry different goals: a first `MANAGE_CONVERSATION` that collects an address and a later one, after a `DELAY`, that confirms delivery.

## Authoring workflow (MCP)

1. **Learn the graph.** Call `journeys_authoring_catalog` for the node kinds and their inputs; `journeys_message_channels` / `journeys_message_templates` for the ids a SEND_MESSAGE needs; `journeys_email_templates` for a SEND_EMAIL's; `journeys_message_variables` for the paths a template binding can reference; `journeys_condition_catalog` for DECISION predicate terms; `journeys_event_catalog` for valid event names.
2. **Open a draft.** `journeys_create_draft` for a blank one, or `journeys_create_draft_from_published` to iterate on the live version. Only a DRAFT is editable; a PUBLISHED version is frozen.
3. **Build the nodes.** `journeys_add_node` per node, `journeys_connect_nodes` per edge (name the `sourceHandle` — the signal the edge routes on). Positions are optional; the server auto-lays-out the graph.
4. **Set the trigger** with `journeys_set_trigger`. `manual` and `cdp_event` work fully from here. **`segment` does not**: it validates `segmentId` as the segment's internal id, and the public segment surface (`cdp-and-segments`) only exposes `slug`, so passing one fails `not_found`. Wire a segment trigger in the Boom app instead, everything else about the journey can still be built and published from here.
5. **Bind template variables** on every SEND_MESSAGE (see below), the most common thing to forget.
6. **Validate** with `journeys_validate` and fix every `error` (warnings are advisory).
7. **Publish** with `journeys_publish` once validation is clean. **Publishing starts real outreach, get explicit confirmation from the user first.** Publishing a new version supersedes the previous one; versions are immutable. This works on any journey, whatever its steps send, so you can take a whole flow live from here. One shortcut: `initiatives_launch` (see `launch-initiative`) publishes the current draft for you, on a WhatsApp or an email initiative, so you can skip this call in that case.

You can also assemble the whole definition and send it in one `journeys_update_draft` call instead of node-by-node — useful when you already have the full graph designed.

## Bind your variables (the most common miss)

A SEND_MESSAGE references an approved template that has placeholders (`{{1}}`, `{{2}}`, a name, a link). The node will not fill them in unless you set **`templateBindings`** — a map from each template placeholder to the value it should carry (a participant attribute, or a value produced earlier in the flow). **Adding the SEND_MESSAGE node is not enough: set `templateBindings` for every placeholder in the template**, or the message sends with empty or literal `{{1}}` values. Confirm the template's placeholders with `journeys_message_templates`, then bind each one.

**Use the right path.** A binding value is a dot-path, and it must be one the send-time resolver can reach. Call **`journeys_message_variables`** for the exact set this journey offers, then copy a returned `path` verbatim. The paths fall into three families:

| Family | What it is | Example |
|---|---|---|
| `customer.<field>` | Built-in contact fields | `customer.name`, `customer.phoneNumber` |
| `person.<key>` | **Custom person attributes** (from people upsert / your CDP) | `person.bank`, `person.plan` |
| run-produced values | Answers extracted in the conversation, or event/segment data carried into the run | copy the exact `path` from `journeys_message_variables` |

So a binding is **not** always `person.*` — built-in fields are `customer.*`, and extracted/event/segment data has its own paths that `journeys_message_variables` returns.

> ⚠️ A custom person attribute is `person.<key>` (e.g. `person.bank`) — **not** `attributes.bank` and **not** `customer.attributes.bank`. `attributes.<key>` is the DECISION/CASE **condition** syntax (from `journeys_condition_catalog`); it does not resolve in a message binding and the message will arrive blank. `journeys_validate` now rejects such a binding before publish.

## Publish-time validation

`journeys_validate` checks dozens of rules; the ones that trip people up most:

- Exactly **one ENTRY**, at least **one EXIT**; unique node ids; every edge references existing nodes; every node named.
- One out-edge per `(node, signal)` — a handle may wire to **at most one** node (no fan-out), and no required signal may be left unwired (`SKIPPED` and `REJECTED` on a send node are the optional ones). `WAIT_FOR_REPLY` needs both `REPLIED` and `TIMEOUT`; `MANAGE_CONVERSATION` needs `CLOSED`; `DECISION` needs both `YES` and `NO`; `CASE` needs every branch **plus** `case:default`; `HTTP_REQUEST` needs both `SUCCESS` and `FAILED`.
- `SEND_MESSAGE`: `templateId` and `channelId` both set — there is no silent fallback number.
- Timeouts and durations use the `30m` / `24h` / `3d` format; DELAY `until_date` must be in the future; DELAY timezones must be valid IANA zones.
- Foot-gun warnings: a `DISPATCH_EVENT` emitting the same event the ENTRY listens to (self-trigger loop), or an event that both enrolls and cancels the run.

Drafts can be incomplete; only **publish** requires a clean validation.

## Hold sends for approval (drafts)

A `SEND_MESSAGE` or `SEND_EMAIL` node with `delivery: "draft"` renders the send exactly as it would go out, stores it as a draft, and parks the run until a person approves or rejects it. In the builder this is the node's **Delivery** section, **Draft for approval**.

**Suggest it** when the user wants to see real messages before they go out: a first launch to a new audience, a personalized email they want to proofread per person, or a regulated or high-stakes send. Don't suggest it for sends that must go out on time, or for large always-on flows where nobody will be reviewing.

**Set it** with `journeys_add_node` or `journeys_update_node` with `inputs: { "delivery": "draft" }`. Omit it (or send `"immediate"`) for a normal send. Runs are pinned to the version they enrolled on, so this reaches new runs only after you publish.

**What happens next:**
- **Approve** sends the stored content, exactly as drafted, and the run continues on `SENT`. If Smart Sending's cap refuses the approved send, it routes `SKIPPED`.
- **Reject** sends nothing and emits `REJECTED`. Wire it if the flow should do something else (a different message, an `EXIT` with an outcome label like `rejected`). Left unwired, the run ends quietly.
- Content is frozen when the draft is created. If the template changes afterwards, the draft still carries the old content (the Drafts tab warns "Template edited since drafted").
- Do Not Contact, the template's status, the sender and a stopped journey are checked again when the draft is approved. Stopping the journey cancels its waiting drafts.
- Drafts don't expire. A run waits until someone decides.

**Limits:**
- WhatsApp only in template mode. A `mode: "free_text"` send can't be drafted, and neither can SMS, Instagram or Messenger.
- Not on a Transactional initiative's journey (`transactional_draft_delivery`): a notification has to go out when its event fires.
- On a parallel-runs journey, a drafted WhatsApp send can't keep the legacy business-hours gate (`sendImmediately: false`); publish refuses any windowed send there (`PARALLEL_RUNS_WINDOWED_SEND`). Use a preceding `DELAY` for timing.
- While a draft waits, the person keeps their one active run in this journey, so enrolling them again returns `ACTIVE_RUN_EXISTS` (except on a parallel-runs journey).
- The run-ended webhook reports a rejected run as `reason: completed`. Read the step's `emittedSignal` to tell them apart.

**Review them** on the initiative's **Drafts** tab in the Boom app, or over MCP: `drafts_list` returns pending drafts (filter by `initiativeId`, `workflowId`, `nodeId`, `channel`, `status`, plus `templateId` / `templateUpdatedAt` / `odd`, below) with a `preview` of what each person will receive, plus `asOf` (the server time of the read). `drafts_get` returns one draft by id, including who decided it and why. `drafts_count` counts the pending drafts a filter matches; pass the list's `asOf` as `createdTo`. `drafts_decide` takes `ids`, or a `filter` plus `asOf` (the value `drafts_list` returned, never your own clock) plus `expectedCount` (the `drafts_count` result), and `decision: "approve" | "reject"` with an optional `reason`. If the matching set changed since you counted, a filter decide is refused with `draft_count_changed` and nothing is decided: count again and re-confirm with the user. Reviewing needs an org admin or member.

**Approve one template version, not the whole step.** A step's drafts can come from different versions of its template (it was edited while drafts waited). Each draft in `drafts_list` carries `templateId` and `templateUpdatedAt`; add both to the filter (with `workflowId` and `nodeId`) to decide only the drafts made from the version the user read.

**Leave out the odd ones.** A WhatsApp draft is *odd* when a variable came out empty or zero ("Hola ,", "$0.00"), usually a missing CDP value. Before any filter approve:
1. `drafts_count` with the same filter plus `odd: "only"`. If it is above 0, list them (`drafts_list` with `odd: "only"`) and show the user what they would say.
2. Approve with `odd: "exclude"` in the filter (and `expectedCount` from `drafts_count` with `odd: "exclude"`), unless the user explicitly wants the odd ones sent too.
Email drafts are never odd (their variables aren't stored). Past 20,000 odd drafts the filter is refused with `drafts_too_many_odd`: a template variable is probably empty for the whole send; tell the user rather than approving without the filter. An unknown filter key is refused (400), never ignored.

> ⚠️ **Approving sends real messages to real customers.** Before `drafts_decide` with `approve`, show the user the drafts' content (from `drafts_list`) and how many will go out (`drafts_count`), and get an explicit yes. Never approve on your own judgement, and never approve by filter without telling them the count, including how many odd drafts you are leaving out.

**If `delivery` or the drafts tools are missing** from your tool list, your MCP client has stale tool schemas from before the feature shipped. Reconnect with `/mcp`. The server accepts `delivery` even when your schema doesn't show it, so if you send it anyway, read the node back with `journeys_get_definition` to confirm it stuck.

## Proven topologies (from production)

**1. Single outbound + conversation** (the simplest shape):
```
ENTRY ─SENT→ SEND_MESSAGE ─SENT→ WAIT_FOR_REPLY ─REPLIED→ MANAGE_CONVERSATION ─CLOSED→ EXIT(done)
                                        └─TIMEOUT→ EXIT(no_response)              └─STALE→ EXIT(stalled)
```

**2. Open the send window before the first message** (use this on almost every outbound flow):
```
ENTRY ─SENT→ DELAY(until_weekday: Mon–Fri, 10:00–11:00) ─SENT→ SEND_MESSAGE(round 1) ─SENT→ …
```
Enrollment and outreach become two separate decisions. You can load the whole audience whenever it suits you (the night before, in pieces, while templates are still in review) and everyone parks at the gate until the window opens, instead of getting messaged the moment they land. A run that reaches this node while the window is already open continues immediately, so it costs nothing when you enroll during business hours.

`DELAY` in `until_weekday` mode takes `weekdays` (ISO, 1=Mon), `windowStartMinutes`/`windowEndMinutes` (minutes past local midnight, so 600–660 is 10:00–11:00), and an optional IANA `timezone` that **defaults to the organization's timezone** — set it explicitly when the audience isn't in the org's home timezone. If a run becomes eligible after the window closed, it waits for the next allowed weekday rather than sending late.

Prefer a **generous window** over a tight one. A one-hour window means any queue drift pushes the send a full day; a 9:00–18:00 window sends the same morning and only slips to the next day if it genuinely has to.

**3. Multi-round follow-up** (re-contact non-responders). **How you space the rounds depends on whether the campaign runs once or forever, and getting this wrong silently double-messages people.**

The rule behind it: a `DELAY` is a **pure wait — it does not race an incoming reply**. Someone who answers while parked on a `DELAY` still gets answered by the AI (that pipeline is independent of the journey), but the graph never learns about it, so the next round fires anyway. Only `WAIT_FOR_REPLY` and `MANAGE_CONVERSATION` listen.

*One-time campaigns* (research, win-back, a single cohort) — put the **whole gap inside `WAIT_FOR_REPLY`** so every hour between rounds is connected to an agent block:
```
… SEND_MESSAGE(r1) ─SENT→ WAIT_FOR_REPLY(6h) ─TIMEOUT→ SEND_MESSAGE(r2) ─SENT→ WAIT_FOR_REPLY(20h) ─TIMEOUT→ SEND_MESSAGE(r3) → …
                                  └─REPLIED→ MANAGE_CONVERSATION ─CLOSED→ EXIT
```
Size each timeout to the real clock gap you want: a 10:00 opener, a 16:00 nudge and a next-day-noon last touch is `6h` then `20h`. No `DELAY` between rounds at all.

*Recurring campaigns* — you can't do that, because you need a `DELAY` to place the next send in an acceptable window (an audience that hits round 2 on a Friday evening should not be messaged on Saturday). So give `WAIT_FOR_REPLY` **enough time to actually catch a reply, six to eight hours minimum**, and only then hand off to the `DELAY` that carries the run into the next window:
```
… SEND_MESSAGE(r1) ─SENT→ WAIT_FOR_REPLY(8h) ─TIMEOUT→ DELAY(until_weekday, next window) ─SENT→ SEND_MESSAGE(r2) → …
                                  └─REPLIED→ MANAGE_CONVERSATION ─CLOSED→ EXIT
```
The residual risk is real but bounded: someone replying during that `DELAY` gets a follow-up they didn't need. Shrinking the `DELAY` doesn't fix it, lengthening the `WAIT_FOR_REPLY` does.

Each round needs its own approved follow-up template.

**4. Attribute-personalized opener** (branch before sending):
```
ENTRY ─SENT→ CASE(attributes.plan) ─case:pro→ SEND_MESSAGE(template_pro) ─┐
                       ├─case:basic→ SEND_MESSAGE(template_basic) ────────┼→ WAIT_FOR_REPLY → …
                       └─case:default→ SEND_MESSAGE(template_generic) ────┘
```
Use CASE for a **small** fork on a single attribute (plan, language, party size). For anything bigger, don't cram multiple goals into one journey — see "One objective per initiative".

**5. Always-on, segment-triggered**:
```
ENTRY(segment: "churned last month", maxEnrollments 1 per 90d) ─SENT→ …
```
People entering the segment enroll automatically; the frequency cap prevents re-contacting the same person too often. Pair with `isRecurring` + `reportCadence` on the initiative.

An `ENTRY` can also be `cdp_event`-triggered, which lets your own system decide the moment someone starts. **Know the tradeoff before you reach for it on a list you already have:** an event-triggered enrollment carries only the event's own `properties`, and it never fills in the per-participant context that enrolling from a list does, so any field you were counting on won't be there unless you put it in the event payload yourself. When the audience arrives as a spreadsheet, uploading it through the CSV flow (or `initiatives_participants_add`) is the better choice, because that path carries the columns through. Reach for the event trigger when the *timing* genuinely belongs to your system, not as a way to stage a list. Pattern 2 already gives you staging without giving up per-participant data.

**6. Call an external system, then hand off** (chaining):
```
… MANAGE_CONVERSATION ─CLOSED→ HTTP_REQUEST(POST the collected data to your API) ─SUCCESS→ DISPATCH_EVENT(done) ─SENT→ EXIT(nextInitiativeId: next)
                                                                                  └─FAILED→ EXIT(needs_review)
```
`HTTP_REQUEST` posts to your endpoint (authenticated with a stored credential) and its response is available to later nodes; `EXIT.nextInitiativeId` chains the person into a follow-on initiative. This is how you keep each initiative focused on one job and pass the baton between them.

## One objective per initiative

An initiative's conversation is run by the AI toward the **single objective** you set on the initiative. Journeys are great at *routing* (branch, wait, call an API, hand off), but a journey should not try to make one conversation accomplish two different goals — the agent handles a focused objective far better than a split one. When a flow really has two jobs (e.g. "collect the documents" and then, later, "resolve what was wrong with them"), model them as **two initiatives chained by an event or an `EXIT.nextInitiativeId`**, not one journey with a mode switch.

A step `goal` on `MANAGE_CONVERSATION` is not a way around this. It focuses one step *within* the objective ("ask for the address first"); it does not give the conversation a second job.

To keep a person out of two conflicting initiatives at once, two mechanisms help: a `DECISION` guard right before an action (re-check the person's current status; exit if they've moved on), and journey-level `cancelOnEvents` (cancel an in-flight run when a status event arrives). Pick whichever fits — the guard is explicit and easy to reason about.

## Design review checklist

Before publishing (or handing over a spec), verify:
1. Every `WAIT_FOR_REPLY` / `MANAGE_CONVERSATION` / `DECISION` / `CASE` / `HTTP_REQUEST` has **all** its signals wired (the TIMEOUT / FAILED paths are the ones people forget).
2. Every `SEND_MESSAGE` names an **APPROVED** template and a channel id, and **binds every template placeholder** (`templateBindings`). Check the approval status yourself before you save — a clean `journeys_validate` is not a promise that every template is ready to send.
3. Follow-up templates exist for every round (round 2..N need their own approved template).
4. DELAY windows respect the audience's waking hours, and the `timezone` is right — it falls back to the **organization's** timezone, which is not always the audience's. Set it explicitly when they differ.
5. Segment-triggered ENTRY has a frequency cap unless the user explicitly wants unlimited re-enrollment.
6. Each `MANAGE_CONVERSATION` `goal`, if set, is one step-specific instruction that fits inside the initiative objective, not a second objective.
7. A send with `delivery: "draft"` is one the user asked to review, it isn't on a Transactional journey, and its `REJECTED` path goes where the user expects (unwired ends the run).
8. EXIT `outcome` labels are meaningful (`recovered`, `no_response`) — they show up in analysis.

## Debugging a live journey

`journeys_get_definition` returns the full graph; `initiatives_get` shows the published version pointer. Typical diagnoses:
- **"Second message never sent"** → the `TIMEOUT` edge is missing on the wait node, or the follow-up template is not APPROVED.
- **"Message arrived with blank / `{{1}}` values"** → `templateBindings` is missing on the SEND_MESSAGE node, **or** a binding uses a path the resolver can't reach (e.g. `attributes.bank` / `customer.attributes.bank` instead of `person.bank`). Check each binding against `journeys_message_variables`; `journeys_validate` flags an unresolvable path.
- **"Some people got nothing"** → a CASE value with no matching branch falling to an unwired default, or Do Not Contact suppression (expected, server-side).
- **"The run is stuck at a send step"** → the node may be `delivery: "draft"` with a draft waiting. Check `drafts_list` for a PENDING draft on that `nodeId`.
- **"Person enrolled twice"** → segment-triggered ENTRY without `maxEnrollments` / `enrollmentWindow`.

See [`CONTEXT.md`](../../CONTEXT.md) for the domain model. Template authoring: [`whatsapp-templates`](../whatsapp-templates/SKILL.md), [`email-templates`](../email-templates/SKILL.md). Segments: [`cdp-and-segments`](../cdp-and-segments/SKILL.md).
