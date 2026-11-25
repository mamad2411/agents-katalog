---
name: reach-message-checklist
description: Checks the message you wrote against six checks in order, with a pass or a flag per check, the line each flag refers to and the reason, and no replacement wording. Use for "run reach-message-checklist", "message checklist", "check my message", "does this sound like a pitch", "review my cold email", "is this message too salesy", "check before I send", "flags only", part of the Claude Guide for Outreach Pack by 90n.
---

# Message Checklist

## When To Use
You wrote it yourself and cannot tell whether it reads as warm or as one more pitch. This is the second look before you send. It answers: does each line pass, and where exactly does it slip?

## When Not To Use
If you want spelling and grammar fixed, use Grammar Check; this skill does not touch grammar. If you have no message yet, start with Talking Points. If you want it rewritten, this is the wrong skill by design.

## Inputs
- Your message, exactly as you would send it.
- The one reason you chose, and whether you have any history with the person.
- The sources behind any fact you mention, your length limit if you have one, and your Writing Voice Guide if you have one.
If you have none of this, I start from the message alone and mark the checks that need a source or a reason as "cannot check".

## Approach
A pre-send checklist with flags only, described generically: six checks in a fixed order, each a pass or a flag pointing at a line. The wording signs come from two public pages: the plain language guide on Digital.gov (shorter words, active voice, written for its reader) and Wikipedia's "Signs of AI writing". The judgement is in flagging without fixing, because the moment a reviewer offers better wording the message stops being yours. The failure it prevents: "I came across your profile and was really impressed", deleted on sight.

## Workflow
1. Ask at most three questions: the reason you chose, whether you know this person at all, and your length limit (if you have none, I say how long it is and you decide).
2. Number the lines of your message so every flag can point to one.
3. Run the six checks in order. One reason, and only one. About them before you: the first lines concern them or the reason, not your background. One fact they will recognise: true, and sourced or from your history. At most one ask, easy to decline. Length within your limit. Nothing that reads as a template: stock openers, flattery, false familiarity, passive padding, patterns from your AI-tell checklist.
4. For each check, write pass or flag, the line number, and why in one sentence.
5. Flag separately any fact about the reader that has no source, or that is private.
6. Stop there. No replacement wording, no "try saying". You rewrite, and run it again if you want.

## Output Format
```markdown
# Message Checklist Flags
Person: [name] | Reason: [reason] | History: [your words, or "none"] | Length: [count] against your limit [limit, or "none set"]
## Checks
| # | Check | Pass or flag | Line | Why |
|---|---|---|---|---|
| 1 | One reason, only one | [ ] | [line no.] | [one sentence] |
| 2 | About them before you | [ ] | [ ] | [ ] |
| 3 | One fact they will recognise, sourced | [ ] | [ ] | [ ] |
| 4 | At most one ask, easy to decline | [ ] | [ ] | [ ] |
| 5 | Length within your limit | [ ] | [ ] | [ ] |
| 6 | Nothing that reads as a template | [ ] | [ ] | [ ] |
## Facts with no source, or private
- [line no.]: [the fact, and the problem]
## Decision
[Your name] decides which flags to act on and rewrites those lines personally, by [date].
```

## Done When
- All six checks have a pass or a flag, and every flag names a line.
- Every fact about the reader is sourced or flagged.
- No line of the output suggests replacement wording.
- Grammar is not commented on.

## Quality Bar
- A flag is specific to a line; "feels a bit salesy" with no line is not a flag.
- A pass is earned; a check that cannot be made says "cannot check" and why.
- Your informal style is not a flag.
- Only the message is judged, never the person receiving it.
- Flags only; you rewrite your own message and you send it.

## Next
Run reach-grammar-check (Grammar Check) to clean the grammar without changing your words.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
