---
name: wayfinder
description: Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.
disable-model-invocation: true
argument-hint: "[loose idea, or map identifier or URL]"
license: MIT
---

A loose idea has arrived, too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets** (questions whose resolution is a decision, not slices of a build to execute) one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting: it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic: engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the first working version can be built. Decisions that only matter once it runs belong to the implementation, not the map. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its **Notes**, carrying execution into the map itself, but absent that, produce decisions, not deliverables.

## Asking questions

Before the first user decision or confirmation, load and follow the `grilling` skill through the host's skill mechanism in the main conversation if it is not already loaded. Apply its **Asking questions** rules to every user question here, including naming the destination, the smallest-version check, the clear-route handoff, and the final choice after challenging an answer. Keep the live exchange in the main conversation; subagents return facts or candidate answers for it. Record a human decision or resolve a HITL ticket only after the user answers.

## Refer by name

Every map and ticket is an issue, so it has a **name**: its title. In everything the human reads (narration, the map's Decisions-so-far), refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish; a name wraps its link, but they ride _inside_ the name, never stand in for it.

## The Map

The map is a single issue on this repo's issue tracker, labelled `wayfinder:map`, the canonical artifact. Its tickets are child issues of the map.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place, its ticket, so the map never restates it, only gists it and links.

**Where the map, its child tickets, blocking, frontier queries, claims, and resolutions physically live is tracker-specific.** Read `docs/agents/issue-tracker.md`. If it is missing, tell the user to run `/setup-supermatt-skills` in Claude linked installs or Cursor, `/supermatt:setup-supermatt-skills` from the Claude plugin, `$setup-supermatt-skills` in Codex, or `/skill:setup-supermatt-skills` in OMP, then stop. Consult the tracker doc's "Wayfinding operations" section for how _this_ repo expresses them.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed: they are open child issues, found by query.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index: one sentence per ticket resolved on the route, at most 30 words (out-of-scope closures go under Out of scope): the decision alone, enough to judge relevance; its reasons and detail stay in the ticket -->

- [<closed ticket title>](link): <the answer's gist: one sentence, at most 30 words>

## Added so far

<!-- one line per kind: every field, state, command, file, and concept the decisions so far add to the destination, so the map's growth is visible at a glance -->

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination or not needed to reach it; closed, never graduates -->
```

### Tickets

Each ticket is a **child issue** of the map; the tracker's issue id is its identity. Its body is the question, sized to fit one agent session inside the [smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone):

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label, one of `research`, `prototype`, `grilling`, `task` (see [Ticket Types](#ticket-types)).

A **claim** belongs to a unique session ID (the host's session ID or a generated UUID), not just a developer. Obtain it through the tracker's Claim operation before any work. Assignment and unconditional file writes are not exclusive acquisition.

**Single-coordinator protocol:** unless the tracker provides documented exclusive acquisition, record one live coordinator's session ID in the map's Notes (the charting session by default). All sessions request claims from that coordinator; never elect a second coordinator themselves. The coordinator serializes eligibility recheck, ownership write, readback, and grant, keeping at most one owner per ticket. A worker starts only after a grant naming its ticket and session ID; an unproven or failed claim starts no work. If the coordinator is absent or unreachable, stop and ask the user to designate one. Release an interrupted claim or replace a coordinator only after the user confirms the prior worker or coordinator has stopped; outstanding ticket ownership survives coordinator replacement.

Blocking uses the tracker's **native** dependency relationship: essential because it renders the frontier _visually_ in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker that lacks native blocking falls back to a body convention. A ticket is **unblocked** when every blocker satisfies the configured tracker's completion rule. On Linear, verify the `completed` state type of every linked blocker, including read-only blockers outside the configured project. Canceled, active, unknown, or unreadable blockers keep the ticket blocked. In every tracker, the **frontier** is the open, unblocked, unclaimed children, the edge of the known.

The answer isn't part of the body; it's recorded on resolution (see [Work through the map](#work-through-the-map)). Assets created while resolving a ticket are linked from the issue, not pasted in.

## Ticket Types

Every ticket is either **HITL** (human in the loop, worked _with_ a human who speaks for themselves) or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved through the `research` skill using the delegation fallbacks under Invocation. Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to. For a logic or UI question, load and follow the `prototype` skill through the host's skill mechanism; make any other artifact (an outline, a rough take, a stub) yourself. In planning mode, override prototype's real-code fold-in step: preserve the throwaway artifact and record the decision, but defer implementation until handoff. Links the artifact as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation. The default case. Always load and follow the `grilling` and `domain-modeling` skills, each through the host's skill mechanism.
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made: nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that _does_ rather than decides, and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war**: the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets, one at a time, until the way to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination: everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now, _not_ whether you can answer it now.

- **Ticket when** the question is already sharp, even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope**: it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

"Not needed" is a full answer too. When a ticket resolves to "the destination is reached without this", close it the same way, with that reason on its Out of scope line.

Out-of-scope work never graduates (the frontier stops at the destination), so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination (mis-scoped in while charting, or exposed by a resolution), **close it** (a closed ticket is unambiguously off the frontier) and leave one line in the **Out of scope** section: the gist plus why it's out of scope, linking the closed ticket. It stays out of **Decisions so far**, which records the route actually walked; a scope boundary isn't a step on it.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session**, with the exception of research tickets.

For the research workers and answer challenges below, use native subagents up to the host's available capacity and queue the remaining work. If subagents are unavailable, use sequential fresh sessions where possible; otherwise research or challenge the answer yourself and report the lack of independent context. Keep concurrent research in separate worktrees and leave tracker resolution to the coordinating session.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Load and follow the `grilling` and `domain-modeling` skills, each through the host's skill mechanism, to pin down what this map is finding its way to: the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Name the smallest version.** State the smallest thing that delivers the destination's goal, often an existing tool plus a prompt or a doc. Ask the user whether building it first would teach more than planning it. If it would, stop: the effort starts as that build, not as a map.
3. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** (the way to the destination is already clear, the whole journey small enough for one session), you don't need a map. Stop and ask the user how they'd like to proceed.
4. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
5. **Create the tickets you can specify now** as child issues of the map, then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Wiring sorts them into the frontier and the blocked; everything you can't yet specify stays in the fog: the **Not yet specified** section.
6. **Fire the research subagents.** Give each research worker a unique session ID and obtain its Claim for an unblocked, unclaimed `research` ticket before dispatch. Leave blocked tickets pending. For each granted ticket, spin up a subagent with that session ID and grant, loading and following the `research` skill through the host's skill mechanism to resolve it in parallel, each in its own git worktree, capturing its findings on a throwaway `research/<name>` branch with a context pointer from the ticket. As each subagent reports back, serialize its tracker and map updates in this coordinating session's own checkout, not the subagent's worktree, by applying **Work through the map, steps 5-7**: classify the answer, record an in-scope resolution and its **Added so far** changes, prune unnecessary tickets and fog, and graduate newly specifiable fog through create-then-wire. An out-of-scope answer uses step 5's Close path only, never Resolve or an entry in **Decisions so far** or **Added so far**. Requery the frontier after those updates, then claim and dispatch newly unblocked research tickets. Bookkeeping may close unneeded tickets of other types, but charting never works or hand-resolves them.
7. Stop: charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with a map (URL or number). A ticket is **optional**: without one, you pick the next decision, not the user.

For HITL tickets, keep proposed glossary and ADR changes in context until step 4 confirms the answer, overriding `domain-modeling`'s inline-write rule. Ticket claims, throwaway prototype artifacts, and prerequisite Task work can proceed before confirmation.

1. Load the **map**: the low-res view, not every ticket body.
2. Choose the named ticket, or the first frontier ticket when none is named. Before requesting its Claim, verify that it is an open, unblocked, unclaimed child of this map. If it fails any check, report its blocker, existing claim, closed state, or different parent and stop. Otherwise request the tracker's Claim for this session ID; the coordinator rechecks eligibility inside its serialized grant procedure. Start work only after exclusive acquisition is proven or the coordinator grants this ticket to this session.
3. Resolve it the way its type says (the `wayfinder:<type>` label, or the `Type:` line on a local tracker) ([Ticket Types](#ticket-types)), and load and follow each skill named by the `## Notes` block through the host's skill mechanism. Load a conditional Notes skill when the work first meets its condition, even mid-resolution. **Zoom as needed**: fetch the full body of any related or closed ticket on demand.
4. **Challenge a HITL answer.** For a HITL ticket, once the grilling frontier is empty, and before asking the user to confirm anything, dispatch a subagent with the drafted answer and the map's Destination, told to argue for the smallest answer that still reaches the destination. Then put the drafted answer and any smaller answer it found to the user in one question. Their pick is the shared understanding grilling waits for. For an AFK ticket, record the completed investigation or work directly in step 5; no user confirmation is required.
5. Classify the answer before recording it. If this ticket is not needed to reach the destination, use the tracker's **Close** operation with the reason and link it under **Out of scope**; do not add it to **Decisions so far** or **Added so far**. Otherwise apply any confirmed glossary and ADR changes, then run the tracker's **Resolve** operation (it records the answer, takes the ticket off the frontier, and appends a context pointer to the map's Decisions-so-far), then add what the answer adds to **Added so far**. The pointer is one sentence of at most 30 words after the link: the decision alone. Reasons, rejected options and the text changed go in the ticket's answer, never in the map. Commit the repository files the resolution changed (such as `GLOSSARY.md` or an ADR), and only those, in one commit named after the ticket. Do not ask first.
6. **Prune.** Close every open ticket and clear every **Not yet specified** patch this answer made unneeded, each with an **Out of scope** line saying why.
7. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. Rule any other ticket beyond the destination out of scope rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.
8. **Hand off when the way is clear.** When no open tickets remain and **Not yet specified** is empty, the map is done. When the destination is something to build, tell the user to run `/to-spec <map>` in Claude linked installs or Cursor, `/supermatt:to-spec <map>` from the Claude plugin, `$to-spec <map>` in Codex, or `/skill:to-spec <map>` in OMP, which collapses its decisions into a buildable plan; otherwise tell them the destination is reached.

The user may run granted tickets in parallel. Serialize claim grants through the recorded coordinator wherever the tracker lacks exclusive acquisition; concurrent sessions never turn assignment or a plain file write into a lock.
