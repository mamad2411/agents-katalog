---
name: demo-strategy
description: "Plan a demo that maps every feature shown to a named buyer pain, lands one wow moment, and is tailored to the people in the room. Use before a product demo or technical walkthrough. Triggers on: plan the demo, demo strategy, tailor the demo, demo prep, demo flow."
---

# Demo Strategy

## Purpose
Turn discovery into a demo plan that shows *only* what maps to a named pain, lands one
memorable wow moment, and speaks to each role in the room — ending in a concrete
demo flow you can run from.

## Inputs
- The pains discovered so far (and whose pain each is)
- Who will be in the room and their role / what they care about
- The product capabilities available to show
- The deal's current stage and what this demo needs to advance

## Method
1. **Discovery-driven selection.** List every feature you're tempted to show. Beside
   each, write the *named* pain it answers and the person who voiced it. If a feature
   has no named pain next to it, cut it. A demo is not a feature tour — it's proof you
   listened. Default to showing fewer things, deeper.
2. **Tell-show-tell each segment.** For every feature that survives the cut, structure
   it in three beats:
   - **Tell:** restate the pain in their words ("You said reps lose 2 hours a day
     re-typing call notes into the CRM…").
   - **Show:** the smallest live path that proves you solve it. No menu tours, no
     "and you can also…". One clean path to the payoff.
   - **Tell:** the "so what." (see next step.)
3. **"So what / why it matters" line per feature.** Every feature shown gets one
   sentence that converts capability into outcome, in business terms:
   `Because <feature>, you <outcome that maps to the pain> — which means <impact on
   their metric / their day>.` If you can't write this line, you don't yet know why to
   show the feature.
4. **Plan one wow moment.** Pick a single beat to land as the demo's peak — the thing
   they'll repeat to whoever wasn't in the room. It should hit the most expensive or
   most emotional pain, be live (not a slide), and feel effortless. Sequence the demo
   so this moment arrives after you've earned trust but before attention fades — not
   the very first thing, not buried at the end.
5. **Tailor to the audience in the room.** Map what each role needs to see:
   - **End user / champion:** does it make their day easier? Show the daily workflow.
   - **Economic buyer:** does it move a number they own? Lead with outcome, keep it short.
   - **Technical evaluator:** does it fit / integrate / secure? Be ready to go deeper.
   Order segments so each person hears their pain answered. If the room is mixed, open
   with the economic buyer's outcome, then go deep for the user/technical seats.
6. **Output the demo flow.** Produce a per-segment plan: `pain → feature → outcome`,
   tagged with which audience segment it's for, and the wow moment marked.

**Demo flow template:**
```
Demo: <account> — <date> — advancing to <next stage>
Room: <names + roles>
Wow moment: <the one beat they'll repeat>

For <segment / role>:
- Pain:    <named pain, their words>
- Feature: <smallest live path that proves the solve>
- Outcome: Because <feature>, you <outcome> — which means <impact>.

[repeat per segment, wow moment marked ★]

Close: <single next-step ask>
```

**Cut rule:** if a feature has no named pain, no owner in the room, and no "so what"
line, it does not go in the demo.

## Tool binding
This skill works from discovery notes alone. It gets sharper when connected to your
stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the discovered pains and the
room directly instead of asking the user to reconstruct them:
- `ontology_resolve("deal", id, expand=["pain_points","value_drivers","stakeholders","products"])`
  — `pain_points` gives the named, transcript-derived pains to map features against;
  `value_drivers` gives the outcomes for your "so what" lines; `stakeholders` tells you
  who's in the room and what each cares about; `products` scopes what you can show.
- `search_transcripts(...)` to quote the buyer's exact words for each "tell" beat.
Doris already extracts pains, value drivers, and stakeholders per deal — prefer those
over re-deriving from raw notes.

### With a CRM / CI / email MCP
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) or a transcript file → source
  the discovered pains and what each attendee said.
- CRM MCP (Salesforce/HubSpot) → pull the contact roles and deal stage to size the room
  and tailor segments.

### With nothing connected
Ask the user for two things: the pains they discovered (and whose pain each is) and who
will be in the room with their roles. Then map features to pains yourself, write a
"so what" line per feature, pick the wow moment, and output the tailored demo flow
(`pain → feature → outcome` per segment) as a copy-paste block.

## Works without Doris
Fully functional from discovery notes — Doris only removes the reconstruction step and
supplies evidence-backed pains, value drivers, and the stakeholder list.

## Common mistakes
- Feature tour: showing capabilities with no named pain behind them.
- No "so what" — demoing *what* it does without *why it matters* to them.
- One-size demo that ignores the roles actually in the room.
- No wow moment, or burying it where no one's paying attention.
- Showing the long path when the shortest live path proves the point.
