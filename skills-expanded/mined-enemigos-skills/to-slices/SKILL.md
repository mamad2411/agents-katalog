---
name: to-slices
description: Turns the current conversation into a plan file of vertical slices that agents can build in parallel. Use when asked to plan, lay down or write up a plan before code is written.
disable-model-invocation: true
---

Turn what the conversation already decided into a plan file that a person skims and an agent builds from. Synthesize. Don't interview the user.

A plan says what to build and what was decided. It leaves how to the agent that builds each slice, because building turns up things no plan predicts.

## Steps

1. **Gather.** Pull the decisions, rules and open questions from the conversation and the issue. Explore the code only far enough to know which layers the change crosses. When the code contradicts a decision, keep the decision and mark it `NEEDS CLARIFICATION` with what you found. Done when every claim in the plan traces to a source.
2. **Size it.** When the change is one slice with an obvious approach, say so and stop. It doesn't need a plan.
3. **Slice** the work by the rules in Slices.
4. **Draft** into the template below. Only the intro and Slices are in every plan. Rabbit holes, No-gos and Flow stay only when they pass their test in Cut.
5. **Cut.** Go through the draft line by line with the tests in Cut and delete what fails. Done when no line fails.
6. **Check** the draft against Voice and rewrite every line that breaks a rule. When a `humanize` skill is loaded, run it on the intro and the rabbit holes, the parts a person reads. It may reword or delete, but it adds nothing, uses no idioms and leaves headings, labels and markers alone. When a skill for writing to agents is loaded, run it on the slices. When neither is loaded, the Cut and Voice rules are the whole check.
7. **Self-review.** Fix what fails and check again until all of these hold.
   - No section is there because the template has it.
   - A slice's name, text and checks each say something the other two don't.
   - Every slice ends in a check someone can run or see.
   - Every slice could go to an agent that has read only this file.
   - No slice stops partway through its behavior, like an endpoint whose screen is in another slice.
   - No file paths or code names beyond the exception in Detail.
   - No "TBD", "handle edge cases" or "etc.".
   - Skim test. Reading only the title and the `Start with` line tells a person what gets built and what to do next.
   - Every sentence has one idea and reads smoothly out loud.
   - No "as mentioned", "see below" or "above". Each slice stands alone.
8. **Save** to `docs/<topic>-plan.md` unless the user names a path, and add its row under "In-flight specs" in `docs/README.md`. Reply with the path and the slices that can start now.

## Template

    # <What the user will be able to do>

    <Up to 3 short sentences. Say what the feature is, the way you would tell a teammate who hasn't heard of it. Cover who does what and what the user sees. Leave out why it's needed.>

    ## Slices

    Start with: <the slices that have no blocker>.

    Take any slice whose blockers are done. Check a box when its check passes. When building proves a decision here wrong, change this file.

    <Mermaid flowchart of the slices, one arrow from each blocker to the slice it blocks. Only when the `Blocked by` lines don't make the order plain, like a chain or a diamond.>

    ### <What works when this slice is done>

    Blocked by: <slice names, or "nothing">

    <Up to 2 sentences on what the name leaves out. Skip them when the name says it all.>

    - [ ] <check someone can run or see>

    ## Rabbit holes
    - <the risk or question>. <the decision that closes it>.

    ## No-gos
    - <what this doesn't do>. <where it lives instead, when it has a home>.

    ## Flow

    <details>
    <summary><the path from entry point to outcome></summary>

    <Mermaid diagram of the user's path. Only when the change adds or changes one.>

    </details>

    Linear [<ID>](<url>)

Mark a point that is undecided, or decided too loosely to build from, inline as `NEEDS CLARIFICATION (<who>)` on the slice or rabbit hole it blocks.

The user is whoever the change is for. For internal work that's a teammate or an operator.

Rabbit holes and No-gos are Shape Up terms. Every rabbit hole names the risk first, so a reader sees why each decision exists. A decision with no risk behind it isn't a rabbit hole. Put it in the slice it shapes.

Flow sits in a collapsed `<details>` block, because the slices already say what gets built. Keep a blank line after `<summary>` and before `</details>`, or GitHub won't render the Mermaid.

## Cut

A template invites filling, and a filled section reads as bloat. Never write a bullet to fill a section. Being true, or being in the conversation, doesn't earn a line its place. A section has to pass its own test first, and then each line in it gets this test. Delete it, then ask whether the agent that takes the slice would build something different, or a person skimming would come back with a question. When the answer is no, it stays deleted.

Two kinds of line fail most.

- **Redundant.** The title, a slice name or another section already says it. The intro is exempt, because it describes the whole feature in one place.
- **Obvious.** The builder would do it unprompted, like regenerating the API contracts, or the reader would assume it. What Slices and Checks ask for is never obvious, so a check that guards reused code stays.

Each optional section has its own test.

- **Rabbit holes** stays for a spot where a builder could lose days or build the wrong thing, with the decision that stops it. A fact, a rule or a decision nobody would get wrong isn't one. A plan with none is fine.
- **No-gos** stays for an option that was really on the table and turned down, like polling, and for work a builder would be tempted to do on the way. A scope edge listed for completeness isn't one, even when the conversation names it.
- **Flow** stays when the change adds or changes a user's path and the slice graph doesn't already show it.

In every list, put first the bullet that would cost the most if it were missed. Cut whole lines. Never shorten a sentence by packing more into it, because a dense sentence is harder to read than a long one.

## Slices

A slice is one behavior, built through every layer that behavior touches, like schema, API, web and mobile. Finishing one gives a person something to see or run. Finishing all of them is the feature.

- Cut by behavior, not by layer. "A client removes an account from its page" is a slice. "Add the endpoint" isn't.
- Size a slice for one agent in one session.
- Slices aren't steps. Name each one in a few words for what works when it's done, and leave out numbers. Order comes only from `Blocked by`, so two slices that don't block each other can be built at the same time.
- Add a blocker only when the slice can't be built or checked until the other one is done.
- Slices are built apart, but they don't have to ship apart. When one would do harm live without another, like signing without its refusals, say so in that slice's text.
- When the conversation settled on a change that clears the way for other slices, like splitting a function two paths will share, make it its own slice. It blocks the slices that need it.
- One mechanical change across the whole codebase, like a rename, can't be cut thin. Plan it as three kinds of slice. Add the new form, move the callers over in batches, then remove the old form.
- Read "Web/Mobile Parity" and the migration rules in `CLAUDE.md` each time instead of working from memory, because the rules change. A slice that changes a parity-tracked web screen includes its mobile twin or says why mobile isn't needed. A slice known to need a schema change says how it stays safe between rollout and migrate.

## Checks

Give a slice the fewest checks that prove it. One is often enough.

- When a slice adds logic with clear inputs and outputs, its check names the test written first and seen failing, like "Every refusal code has a test, written before the rule."
- When a slice changes code that already has tests, its check is those tests passing unchanged.
- When a slice is UI, its check is a screenshot plus one test that the screen opens.

## Detail

Leave out file paths, function names and code. They go stale as soon as building starts, and the agent that takes a slice finds them faster than a plan can list them.

Name one only when it is the decision, like a route another team will call, a legal template the text must match or a table several slices share.

## Voice

- Join clauses with a word like "and", "so", "but" or "because", or start a new sentence. Keep colons for code, labels like `Blocked by:` and the line before a list.
- Write slice names and checks as plain sentences. Leave out commit prefixes like `feat:` or `refactor(api):`.
- Write rabbit holes as short bullets, one per risk. Leave out tables.
- Use the word the user sees, not the internal one. Write "monthly deposit" even if the code calls it a draft.
- Write for a teammate whose first language isn't English. Keep one idea in each sentence, and put the subject first.
- Give a definition or a side note its own sentence. Don't tuck it into the middle of another one.
- Use common words and say things literally. Leave out idioms.
- Define a business word a teammate might not know, the first time it appears.
- Give an example only when the idea fails without it.
- Use only hyphens and straight quotes. Use checkboxes in Slices only.
