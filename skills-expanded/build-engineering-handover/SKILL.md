---
name: build-engineering-handover
description: Writes an Engineering Handover Note covering how to open and run the prototype, a map of screens to requirements, the decisions made and why, everything faked or hardcoded, known problems, and what you recommend keeping, rebuilding or throwing away. Use for "run build-engineering-handover", "hand my prototype to engineering", "write a handover note", "write a README for my prototype", "document the decisions I made while building", "what should engineers keep or rebuild", "engineers have forty questions about my prototype", "list everything I hardcoded", part of the Claude for Product Builders Pack by 90n.
---

# Engineering Handover Note

## When To Use
You send engineers a link and a "let me know what you think", and they have forty questions before they can start. Building the prototype forced decisions the spec never made, and they live in a chat thread. This skill answers: what exists, how do you open it, why is it this way, and what would you keep?

## When Not To Use
If the question is what production still needs, run Prototype vs Production Note. If you want an engineer's time and judgement, run Engineering Review Request, which points at this note. A prototype that tested nothing does not need a handover yet.

## Inputs
- The prototype: a link, the folder, or the Claude Design project, and what it was built with.
- The spec with its requirement ids, and the chat where you built it.
- Your own list of what is faked, hardcoded or broken, and where the sample data lives.
If you have none of this, I start from a walk through the screens in your own words and mark the output as a first draft.

## Approach
Four public conventions. The README sections from Make a README (https://www.makeareadme.com/). Decision records (https://adr.github.io/, original template at https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions). The spike rule from Extreme Programming (http://www.extremeprogramming.org/rules/spike.html): "Most spikes are not good enough to keep, so expect to throw it away." And Anthropic's tutorial on documenting decisions in the chat before a Claude Design hand-off to Claude Code (https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux). The failure this prevents: a senior engineer spending a day reverse-engineering a choice you made in ten seconds.

## Workflow
1. Ask at most three questions: where does the prototype live and what is it built with; where is the reasoning (the chat, the spec, your notes); which engineering role receives this note?
2. Write the README part: name, description, how to open or install it, how to use it, project status. Status reads "prototype". Test the opening steps on a machine that is not yours, or mark them untested.
3. Map every screen to the requirement id it covers and mark it works, faked or missing. A requirement with no screen goes in the map too.
4. Write one record per decision in the template's parts: title, context (the forces at play), decision ("We will..."), status, consequences. Pull each from the reasoning in the build chat. A record written from memory says so.
5. List everything faked or hardcoded, every known problem, and where the sample data is. Any key, password or real customer record found on the way stops the note: check with your engineering or security lead before it is shared.
6. Recommend keep, rebuild or throw away for each part, with one reason. Throwing away is the default for a spike. State that the choice is engineering's.
7. If it was built in Claude Design, say where the hand-off to Claude Code is. It carries the design and the names used, not a finished codebase.

## Output Format
```markdown
# Engineering Handover Note
**Name:** [prototype] | **Status:** prototype | **Built with:** [surface and tools] | **Written for:** [engineering role]
## How to open and use it
[Steps, in order] | **Tested on a second machine:** [yes / no]
## Screen and requirement map
| Screen | Requirement id | State |
|---|---|---|
| [screen] | [id] | [works / faked / missing] |
## Decisions
| Title | Context | Decision | Status | Consequences | Source |
|---|---|---|---|---|---|
| [title] | [forces at play] | We will [choice] | [status] | [what follows] | [build chat / from memory] |
## Faked, hardcoded and known problems
- [Item]: [faked / hardcoded / problem], [where it shows]
**Sample data:** [location, and confirmation that none of it is real customer data] | **Hand-off:** [where the Claude Design hand-off to Claude Code is, or "not used"]
## Builder's recommendation
| Part | Keep, rebuild or throw away | Reason |
|---|---|---|
| [part] | [recommendation] | [reason] |
## Decision
[Engineering lead, by role] chooses what is kept, rebuilt or thrown away, on a date they set. The table above is a recommendation only.
```

## Done When
- Someone who has never seen the prototype can open it from the note alone.
- Every screen and every requirement id appears in the map with a state.
- Each decision has a context, a consequence and a source, and the recommendation table states that engineering chooses.

## Quality Bar
- Decisions are recorded with reasons, never with blame. No engineer or designer is assessed.
- "Faked" is said plainly on every faked part. A reader should never find one by surprise.
- No estimate, no date and no claim that any part is ready for customers.
- The builder recommends; engineering decides what is kept, rebuilt or thrown away, and owns what ships.

## Next
Run build-review-request (Engineering Review Request) to ask an engineer one question about it, with this note attached.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
