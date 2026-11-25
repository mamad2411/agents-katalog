---
name: pdes-design-system-change-record
description: Writes a Design System Change Record for one proposed change, with the problem, what already exists, the "can it be built from what exists" check, who is affected and a decision field left for the system owner. Use for "run pdes-design-system-change-record", "propose a design system change", "add a component to the design system", "new component proposal", "should this go in the library", "component variant request", "retire a component", "design system changelog", part of the Claude for Product Designers Pack by 90n.
---

# Design System Change Record

## When To Use
Your feature needs something the system does not have, and "I just added a variant" is how the system got two card patterns. Run it before anyone touches the library, for one new, modified or retired component, token or pattern. It answers: is this a real gap, who does it touch, and what does the system owner need in front of them to decide?

## When Not To Use
A product design choice for your own area (which flow, which layout) is not a system change: file it in Design Decision Log. If you want the system written down as it is today so Claude follows it, use Design System Rules File.

## Inputs
- The change: new, modified or retired, what it is called, and the screen where the need came up
- The closest things the system already has, with their variants and properties
- Who uses the thing being changed, and earlier change records if you have them (a Project keeps them between chats, or paste them in)
If you have none of this, I start from the screen and the need in two sentences, and mark the output as a first draft.

## Approach
This is the Architecture Decision Record (Nygard, 2011, cognitect.com/blog/2011/11/15/documenting-architecture-decisions) applied to one design system change: a short dated record of the context, the decision and its consequences, kept even when the answer is no. The judgment behind it is that a new component needs a job no existing one can do, so the record checks that before it argues for anything. The failure it prevents: a year from now someone asks why there are two card patterns, and the only answer is a shrug.

## Workflow
1. Ask three questions: what the change is and the problem it answers on which screen; what exists that is close and why it does not serve; who uses it today, who owns the system and by when they decide. If the team has no written change path, I use propose, check, decide, tell, land.
2. Check earlier records for this proposal or its opposite. If "what exists" was never checked, we check it together before going further. Then run the "can it be built from what exists" check in three forms. Can an existing component do it with a variant or a property change? Can two existing components composed do it? Is the difference a visual preference and not a different job? A yes to any turns the proposal into a variant, a composition or a decline, with the reasoning kept.
3. List each consumer (screens, products, the coded library) and mark the impact invisible, visible or breaking. A breaking change is announced before it lands, with a date.
4. Write the record down to the decision field and stop. The field reads "awaiting [system owner], due [date]" until a person fills it. One change per record; five bundled changes become five records.
5. Once the owner has decided, add the status and reason, one changelog line in the past tense, and the note to the team: what changed, who is affected, what to do, by when. If it lands differently, add a dated addendum.

## Output Format
```markdown
# Design System Change Record
**Title:** [component or pattern, and the change] | **Type:** [new / modified / retired] | **Date:** [date] | **Proposer:** [role]
**Problem:** [two sentences, with the screen or flow where it came up]
## What exists and why it does not serve
| Existing component or pattern | What it covers | Where it falls short |
|---|---|---|
| [name] | [job] | [gap, or "not checked"] |
## Can it be built from what exists
| Form of the check | Answer | Reasoning |
|---|---|---|
| A variant or property change on an existing component | [yes / no] | [why] |
| Two existing components composed | [yes / no] | [why] |
| A visual preference, not a different job | [yes / no] | [why] |
## Proposal
[New component, variant, composition or nothing to add, in the system's own names.]
## Affected
| Consumer | Impact | What they need to do | Told by |
|---|---|---|---|
| [screen, product or coded library] | [invisible / visible / breaking] | [action or none] | [date] |
## Changelog line and note to the team
[Drafted only after the decision. One past-tense line, then what changed, who is affected, what to do, by when.]
## Decision
Status: proposed, awaiting [system owner], due [date]. [System owner] accepts, changes or declines the change and writes the reason here; nobody else fills this field.
```

## Done When
- "What exists" names real components and none reads "not checked"
- All three forms of the check have an answer and a reason
- Every consumer has an impact mark, each breaking change has an announcement date, and the decision field names the system owner and a date

## Quality Bar
- The record is about the component, never about who added the last duplicate, and no count is kept of anyone's proposals
- Declined and deferred records are kept; a record is never edited to match what landed, it gets an addendum
- I know the system only through what you paste; the system owner checks "what exists" against the library, and a person lands the change
- Claude writes the record; the system owner decides, and the decision field stays blank until they do

## Next
Run pdes-ux-debt-register (UX Debt Register) for the issues that did not make this release.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
