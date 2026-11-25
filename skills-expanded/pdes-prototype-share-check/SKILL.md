---
name: pdes-prototype-share-check
description: Prepare a prototype share check with eight checks a person runs before a prototype leaves the team, the list of what is faked, the words to say when showing it and who owns what ships. Use for "run pdes-prototype-share-check", "prototype share check", "before I share this prototype", "is this prototype safe to send", "checklist before sharing a prototype", "who can open this prototype link", "what to say when showing a prototype", "label this as a prototype", part of the Claude for Product Designers Pack by 90n.
---

# Prototype Share Check

## When To Use
A prototype is about to go to users or a stakeholder, and it looks finished enough to be mistaken for the product. The link is one paste away from a channel you do not control, and you have not looked at what the sample data says, who can open it or what you will say first.

## When Not To Use
Not a full accessibility pass: for the design-stage check against WCAG 2.2, use Accessibility Review. If the prototype stays inside the team that made it, a spoken "this is rough" is enough.

## Inputs
- What the prototype is for, who will see it (by role), when, and how it is shared (link, file, screen share) from which tool
- What you know is faked (data, logins, calculations, screens that lead nowhere), where its content came from, and whether anything was pasted from a real system
If you have none of this, I start from one sentence on what you are sharing and with whom, and mark the output as a first draft.

## Approach
This list is the skill's own design, not a published standard. It rests on three public points. Anthropic describes Claude Design as a tool for ideation, collaboration and buy-in, with the build handed to engineering (post of 24 Jul 2026). Its help article says a design starts private and the owner sets view, comment or edit (support.claude.com/en/articles/14604416-get-started-with-claude-design). The GOV.UK Service Manual's testing for accessibility page says rough prototypes still get a contrast check (gov.uk/service-manual/helping-people-to-use-your-service/testing-for-accessibility). I prepare the list and the words; I cannot see what your link exposes, so you run every check with the prototype open. The failure this prevents: a stakeholder forwards the link, a sales call demos it as the product, and the sample account on screen two belongs to a real customer.

## Workflow
1. I ask up to three questions. Who will see it, and how does it reach them? What in it is faked? Where did the names, numbers and text in it come from?
2. I write the eight checks for this prototype, each with how to look and the fix if the answer is no: the "prototype" label visible on every screen; faked parts listed; data invented; no keys, passwords or tokens; link access matching the audience; contrast looked at; a keyboard pass through the main path; opening words written. I draft the faked list from what you told me and mark the gaps for you to fill with the prototype open.
3. I word the access check for your tool. In Claude Design, that is the sharing setting (private, view, comment or edit); elsewhere, whoever can open the link. Anything about keys, tokens or where it is hosted ends with "check with your engineering or security lead".
4. I describe the quick look at contrast and keyboard: text against its background on the main screens, then tab through the main path with no mouse. It is a look, not an audit, and duties under accessibility law end with "check with a qualified adviser".
5. I write the opening words in four parts: what this is, what is faked, what feedback is wanted, what it does not promise. Then the last line naming who owns what ships, by role.
6. You run each check and answer yes, no or not applicable. A "no" is fixed or the share waits.

## Output Format
```markdown
# Prototype Share Check
**Prototype** [name], going to [audience, by role] via [link, file or screen share]
## Checks (run by [role] on [date], with the prototype open)
| # | Check | How to look | Yes / No / N/A | Fix |
|---|---|---|---|---|
| 1 | "Prototype" label visible on every screen | [placeholder] | [ ] | [placeholder] |
| 2 | Faked parts listed below | [placeholder] | [ ] | [placeholder] |
| 3 | Data invented; no real names, accounts or customer data | [placeholder] | [ ] | [placeholder] |
| 4 | No keys, passwords or tokens (check with your engineering or security lead) | [placeholder] | [ ] | [placeholder] |
| 5 | Link access (private, view, comment, edit) matches the audience | [placeholder] | [ ] | [placeholder] |
| 6 | Contrast looked at on the main screens | [placeholder] | [ ] | [placeholder] |
| 7 | Keyboard pass through the main path | [placeholder] | [ ] | [placeholder] |
| 8 | Opening words written | [placeholder] | [ ] | [placeholder] |
## What is faked
| Part | What a viewer might assume | What is true |
|---|---|---|
| [placeholder] | [placeholder] | [placeholder] |
## Opening words
- What this is: [placeholder]
- What is faked: [placeholder]
- Feedback wanted: [placeholder]
- What it does not promise: [placeholder]
## Decision
[Designer, by role] decides whether the prototype goes to [audience] on [date], once every check is answered and each "no" is fixed. [Engineering lead, by role] owns what ships; [product manager, by role] owns scope and dates.
```

## Done When
- All eight checks have an answer written by a person, with the date and their role, and every "no" has a fix done or the share is on hold
- The faked list was read against the prototype screen by screen
- The opening words fit in under a minute of speaking and name what is not promised

## Quality Bar
- No real customer or participant data stays in a prototype that leaves the team
- The contrast and keyboard look is recorded as a look; it is not a conformance claim
- Security questions are routed to a named role, not answered from the chat
- A person runs every check with the prototype open; a clean list does not make the prototype tested, accessible or ready to ship.

## Next
Run pdes-design-quality-bar (Design Quality Bar) to check the work against a written standard.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
