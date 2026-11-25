---
name: pdes-accessible-test-sessions
description: Plans how to bring disabled people and older users into a round of usability sessions, with an invitation that welcomes them, access needs asked in advance as an open question, their own assistive technology, consent in accessible formats and session adjustments. Use for "run pdes-accessible-test-sessions", "include disabled participants in my testing", "test with screen reader users", "accessible usability sessions", "ask participants about access needs", "usability testing with older users", "no disabled person has used this design", part of the Claude for Product Designers Pack by 90n.
---

# Accessible Test Sessions

## When To Use
The accessibility review passed on paper and no disabled person has ever used the design. Run this when you already have a round of sessions planned and want disabled people, and older users where they are in your audience, to be part of it. It answers: how do I invite them, what do I ask beforehand, and what do I change so they can take part as themselves?

## When Not To Use
This is not an audit and it never shows that a product meets a standard. To inspect a screen or flow against WCAG 2.2 at the design stage, use Accessibility Review, and do that first so the obvious barriers are fixed before anyone gives you their time.

## Inputs
- The tasks or script for this round, the session format (remote, their place, your office) and the dates
- The consent form you use today, and who your users are, including whether older people are among them
- What the design-stage review found and what has been fixed since
Use participant ids (P1, P2) and remove contact details before pasting anything about a person.
If you have none of this, I start from the flow under test and the session format, and mark the output as a first draft.

## Approach
Involving Users in Evaluating Web Accessibility (W3C Web Accessibility Initiative) with Running research sessions with disabled people (GOV.UK Service Manual). People use their own assistive technology with their own settings, because those are hard to recreate, and a few people never stand for everyone with a similar disability. Sessions sit beside a standards review; alone they cannot say a product is accessible. The failure this prevents: a borrowed screen reader on your laptop, a participant fighting unfamiliar settings, and a slide that says "blind users cannot check out" from one session.

## Workflow
1. Ask up to three questions: how many disabled or older participants will you add and which access needs do you want to cover, what is the session format, and has a design-stage review been done and its obvious barriers fixed.
2. Set the range. A few people, not one, across the needs you chose, with assistive technology skill that matches your real users. You set the numbers. Write the invitation line that says disabled people are welcome, and say where it will be posted.
3. Ask access needs in advance as one open question: "Is there anything we can do to make it easier for you to take part?" Keep only what runs the session. Never record a diagnosis.
4. Plan each setup around their own assistive technology and settings. If they cannot bring it, go to them or run the session remotely on their device. Allow extra time for setup.
5. Check consent: can each person use and understand the form? Offer the format they asked for. If a helper or interpreter attends, agree their role beforehand and speak to the participant, not to them.
6. Write the session adjustments and conduct notes: ask before helping and do not assume; ask which terms the person prefers; longer slots, fewer tasks, breaks.
7. Add the reporting note to every output: scope, methods and who took part, with findings stated per person and need.

## Output Format
```markdown
# Accessible Test Session Plan
**Flow under test:** [name, version] | **Format:** [remote / their place / office] | **Design-stage review done:** [date, barriers fixed]
## Who to invite
| Access need to cover | People | Assistive technology skill to match | Invitation line | Where posted |
|---|---|---|---|---|
| [need] | [n, set by you] | [as your users] | [welcome wording] | [channel] |
## Access needs question
"[open question text]" | Kept only for: [running the session] | Deleted: [when]
## Per participant setup
| Id | Their assistive technology and settings | Place | Consent format | Helper or interpreter role | Adjustments |
|---|---|---|---|---|---|
| [P1] | [as told by P1] | [place] | [format] | [role agreed] | [setup time, breaks, pace] |
## Conduct notes
- [ask before helping; preferred terms; speak to the participant]
## Reporting note
Scope: [flow]. Methods: [sessions plus the design-stage review]. Findings are stated per person and need; [n] of [N] participants is never read as a group.
## Decision
[Designer running the sessions] confirms each participant's setup and adjustments by [date]. Who may consent and how access needs data is kept: [named role] confirms by [date]; check with a qualified adviser.
```

## Done When
- The invitation welcomes disabled people, and the range of needs and numbers is the one you set
- Every participant has their own setup, consent format and adjustments written down before their session
- The reporting note and the adviser check are in the plan

## Quality Bar
- Access needs are asked openly and kept only to run the session; no diagnosis is recorded
- Nobody is described by their condition in anything shared; participant ids only
- Their own assistive technology comes first; any other setup is named as a fallback with what it cannot show
- Access needs may be sensitive personal data, and nothing here says what a law requires; check with a qualified adviser
- Disabled people take part themselves; Claude never simulates them, and sessions do not make a product conformant

## Next
Run pdes-usability-findings (Usability Test Findings) to write up what happened.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
