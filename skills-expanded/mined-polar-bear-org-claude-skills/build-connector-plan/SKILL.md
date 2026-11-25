---
name: build-connector-plan
description: Decides whether a prototype needs live tool data at all and writes a Connector Plan with each connector page checked, reads allowed and writes kept off, personal data flagged, who turns each connector on and one first-run question you can check by hand. Use for "run build-connector-plan", "should my prototype read real tickets", "connect the prototype to our analytics", "what could Claude change in our tools", "which connector actions should stay off", "do I need live data for this prototype", "who has to turn the connector on", part of the Claude for Product Builders Pack by 90n.
---

# Connector Plan

## When To Use
The prototype would be far more convincing reading real tickets or analytics, and you do not know what that would let Claude change. Run this before anything is connected. It answers: does the belief need live data at all, and if it does, what is the least the prototype may read?

## When Not To Use
If invented data will do, write a Sample Data Plan and connect nothing. If your question is who can open the prototype once it is shared, that is Access and Sharing Check; this plan covers what the prototype can read and change in other tools.

## Inputs
- The belief on your test card and the screen that would use live data
- The tools in question, by the names you use (your ticket tool, your analytics tool)
- Your Claude plan, and who can turn connectors on where you work
If you have none of this, I start from the one tool you most want to connect and mark the output as a first draft.

## Approach
Connectors are checked one by one on Anthropic's official directory (claude.com/connectors), read alongside the artifacts help page (support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them), and held to least privilege as the NIST glossary defines it (csrc.nist.gov/glossary/term/least_privilege): the minimum access the task needs. Convincing is not a reason to connect. The failure it prevents: a connector added so a prototype could read threads, which could also send messages as you, noticed on the day it does. Security points: check with your engineering or security lead.

## Workflow
1. Ask up to three questions: which belief and which screen would use live data, which tools, and who can turn a connector on for you?
2. Ask the first question first: does the belief need live data at all? If sample data tests it, the plan ends there and says so.
3. For each tool, open its page in the directory and copy what the page states it can read and what it can change. "Not found" and "the page does not say" are valid entries; never assume. Re-open the page yourself, since pages change.
4. Apply least privilege: only what this one prototype needs, and reads only. Writes stay off: send, share, delete, edit.
5. Record how an artifact uses a connection, as the help page states it. An artifact can read from and write to connected apps on paid plans; the first time, Claude asks which apps and tools to approve, and single tools can be turned off; each person who opens a shared artifact uses their own connection; an owner can turn this off for the whole organisation.
6. Flag every connector that exposes personal data (contacts, messages, transcripts), and name the role who turns each one on. That data stays out of the context file, the sample data and any shared screen.
7. Write one first-run question per connector whose answer you can check by hand in the tool itself. If the two answers differ, the connector stays off until someone explains why.

## Output Format
```markdown
# Connector Plan
Prototype: [name] | Belief tested: [from the test card] | Pages checked on: [date] | Plan: [plan]
## Is live data needed
[Yes / no]. [If no: sample data tests this belief, nothing is connected, and the plan ends here.]
## Connectors
| Tool | Page found? | Reads, as the page states | Changes, as the page states | The one read this prototype needs | Kept off | Personal data? |
|---|---|---|---|---|---|---|
| [your ticket tool] | [yes, date / not found] | [as stated / the page does not say] | [as stated / the page does not say] | [read] | [send, share, delete, edit] | [yes / no] |
## Who turns it on
| Connector | Turned on by (role) | Tools approved at first use | Tools turned off | Date |
|---|---|---|---|---|
| [connector] | [role] | [list] | [list] | [date] |
## First-run check
| Connector | Question asked | Answer in the prototype | Answer checked by hand in the tool | Match? |
|---|---|---|---|---|
| [connector] | [question] | [from run, or not yet run] | [from the tool] | [yes / no] |
## Decision
[Engineering or security lead, by role] says yes or no to each read-only connector by [date]; [builder, by role] runs each first-run check before a tester opens the prototype.
```

## Done When
- The live data question is answered in one line, with the reason
- Every tool is matched to a page or marked "not found", and every connector lists what is kept off
- Personal data connectors are flagged and each has a named role
- Each connector has a first-run question with an answer checked by hand

## Quality Bar
- Nothing is claimed about a connector beyond what its page states on the date checked. No write is turned on for a prototype, not even once to "see if it works".
- Testers who open a shared artifact use their own connection: say so in the plan, and say what they would see.
- Personal data reached through a connector never lands in the context file, the sample data or a shared screen.
- Reads only, and nothing live is connected until a named person has turned it on; security points: check with your engineering or security lead.

## Next
Run build-ai-prototype-check (AI Prototype Input Check) if the prototype has an AI feature inside.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
