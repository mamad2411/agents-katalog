---
name: adopt-shared-prompt-library
description: Builds a shared prompt library with one entry format, the way entries are proposed, tested, updated and retired, where the library lives and its review rhythm. Use for "run adopt-shared-prompt-library", "shared prompt library", "team prompt library", "prompt library template", "organise our AI prompts", "nobody owns the prompts in the shared folder", "how to share prompts across the team", "clean up our prompt folder", part of the Claude Guide for AI Adoption Pack by 90n.
---
# Shared Prompt Library
## When To Use
Good prompts live in private chats and the shared folder holds forty untested ones nobody owns. People cannot tell which entry still works, so they write their own again. The question this answers: what does an entry have to carry before anyone else can trust it, and who keeps it alive?

## When Not To Use
Not when one task needs one card at the point of use: that is the AI Job Aid, which holds no collection. Not to decide who looks after the library: the AI Champions Network sets that. With fewer than a handful of prompts worth sharing, one shared page is enough and a lifecycle is overhead.

## Inputs
- The prompts or skills people already share, pasted as they are, with the task each one is for.
- The place the team already opens every day, who could own the library, and how often the tool and the rules have changed lately.
- Your organisation's never-put-in list, so examples can be checked against it.
If you have none of this, I start from two or three prompts that worked on real work, and mark the output as a first draft.

## Approach
The lifecycle is capture, structure, reuse, improve: the first four practices of Knowledge-Centered Service, from the Consortium for Service Innovation's practices guide, with its idea of content health. I leave out that guide's practice on assessing contributors: this library assesses entries. Each entry also carries the judgement of how to ask: what the task is, what the context is, what a good result looks like. The failure this prevents is the prompt graveyard, a folder that grows every week and is trusted by no one, because nothing in it says who tested it, on what, or when.

## Workflow
1. Ask at most three questions: where do the prompts live today and who opens that place, which few have really worked on real work, and who will own the library.
2. Capture. An entry is written at the moment a prompt worked on real work, in the words of the task, by the person who used it. A prompt written "in case it is useful" enters as a draft and stays one until someone uses it.
3. Structure. Put every entry in one template: task, when to use it and when not, what to give it (context, source material, what good looks like), the prompt or skill, what to check, an example with sanitised material, owner, last tested on [date]. I check each example against your never-put-in list and flag anything that should not be there.
4. Reuse. Search before writing: a new prompt for a task that already has an entry becomes an edit or a link, never a duplicate. I sort your existing prompts by task and show the overlaps. Then improve, because reuse is review: whoever uses an entry and finds a problem flags it or fixes it, and the owner confirms. No separate review committee.
5. Set content health. Four states: draft, tested, needs review, retired. An entry with no owner or no test date is not "tested", whatever it looks like. You set the review rhythm, and a change in the tool or the rules sends the affected entries to "needs review".
6. Choose where it lives: one place the team already opens, such as Projects (redesigned, in beta on select plans) to keep the library with its files, or any shared folder. Then sort the starting inventory into states and name what is retired on day one.

## Output Format
```markdown
# Shared Prompt Library
**Lives in:** [one place the team already opens] · **Library owner:** [name] · **Review rhythm:** [you set it] · Draft status: [first draft / agreed on date]
## Entry format
| Field | What goes in |
|---|---|
| Task, when to use it and when not | [the task in the words of the people who do it, the situation it fits, the one it does not] |
| What to give it | [context, source material, what a good result looks like] |
| What to check | [facts against the source, numbers, names, what is missing] |
| The prompt or skill, with an example | [text or link], [example on sanitised material only] |
| Owner, last tested, state | [name or role], [date] on [type of work], [draft / tested / needs review / retired] |

## Lifecycle
| Step | What happens | Who | Rule |
|---|---|---|---|
| Propose | [written when it worked on real work] | [anyone] | [search first, link instead of duplicating] |
| Test | [a second person uses it on their own work] | [role] | [no owner or no test date means not tested] |
| Update | [flag it or fix it on use] | [user, then owner] | [the test date changes only after a real use] |
| Retire | [moved out of search, kept for reference] | [owner] | [trigger: unused, superseded, tool or rule changed] |

Early review when: [the tool changed / the rules changed / an entry gave a wrong result]. The library keeps no count of entries or contributions per person, and its size is not a goal.
## Starting inventory
| Existing prompt | Task | Overlaps with | State it enters with | Owner |
|---|---|---|---|---|
| [prompt] | [task] | [entry or none] | [draft / tested / retired] | [name or "none yet"] |

## Decision
[Library owner name] approves the entry format and the starting states by [date]; [sponsor or team lead name] confirms where the library lives and the review rhythm by [date].
```

## Done When
- Every entry in the starting inventory has a task, a state and an owner, or is marked "none yet" and held as a draft.
- No entry is called tested without a test date and the type of work it was tested on.
- Every example has been checked against the never-put-in list, and the lifecycle names who can retire an entry and what triggers it.

## Quality Bar
- One format for every entry. A library with three formats is three folders.
- "What to check" is filled for every entry: a prompt shared without its check passes on the risk with the shortcut.
- Fewer entries that work beat many that might. Retiring is maintenance, not loss.
- Every entry has an owner, a test date and a check a person runs; contributions are never counted per person.

## Next
Run adopt-local-adaptation-review (Local Adaptation Review) to handle the variations teams make to the agreed way.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).