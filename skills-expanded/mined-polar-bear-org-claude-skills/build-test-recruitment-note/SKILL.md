---
name: build-test-recruitment-note
description: Writes a Tester Recruitment and Consent Note that says who counts as a real target user for the belief you are testing and who does not, where to find five of them, the invitation message and a plain consent note covering recording, how notes are kept and the right to stop. Use for "run build-test-recruitment-note", "who should test my prototype", "find five users to test with", "write the invitation for a user test", "consent note for a usability session", "can I test it on my colleagues", "screening questions for testers", "can I record the session", part of the Claude for Product Builders Pack by 90n.
---

# Tester Recruitment and Consent Note

## When To Use
The prototype is nearly ready to show and the easiest five people to ask are the ones sitting next to you. This skill answers: who is a real target user for this belief, where do you find five of them, and what do they agree to before the session starts?

## When Not To Use
If the people are booked and you need tasks and a script, run Five-User Usability Test Plan. If nobody has said yes to sharing the prototype, run Pre-Share Sign-Off first. If there is no belief to test yet, run Prototype Test Card.

## Inputs
- The belief and the target user from your test card, word for word.
- Where you can reach people with that need, and whether sessions will be observed or recorded.
If you have none of this, I start from one sentence on who the prototype is for and mark the output as a first draft.

## Approach
Informed consent for user research as the GOV.UK Service Manual sets it out (https://www.gov.uk/service-manual/user-research/getting-users-consent-for-research), with the guidance on comparable users per group from Nielsen Norman Group (https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/), which asks for actual or likely users. The judgment: a tester is defined by a need and a situation, never by how easy they are to ask. The failure this prevents: five sessions with teammates who already know what the button does, written up as proof that users understood it. Claude drafts the note; it never plays a participant.

## Workflow
1. Ask at most three questions: what is the belief on the test card and who does it name; is that one group of users or several distinct groups; will sessions be observed or recorded, and who will see the notes?
2. Define the tester from the belief: the need and the situation, in two or three screening questions about what the person did recently, not what they say they would do. Screen for the need only, never for personal characteristics the belief does not require.
3. Write the not-testers list and the reason for each: colleagues, the leaders who asked for the idea, friends, anyone who has seen the spec. They can pilot the script. They cannot be a result.
4. Set how many and where: about five comparable users for one group; three or four per group with two distinct groups; at least three per group with three or more. For each group, name the place where people with this need already are and who will ask.
5. Write the invitation: it is a prototype, how long the session takes, that the design is being tested and not them, and that taking part is voluntary.
6. Write the consent note in plain words: who is doing the research and why, what happens in the session, what data is collected, whether it is observed or recorded and how, how results are used and who sees them, how long data is kept, and that they can stop or withdraw at any time. A person on your side reads it before it is sent. Consent and recording law differ by place: check with a qualified adviser.
7. Set the records: a participant code from the first note onward, each consent record stored with the data it covers and labelled by round and code, and a deletion date. Data is deleted earlier when someone withdraws.

## Output Format
```markdown
# Tester Recruitment and Consent Note
**Belief under test:** [word for word from the test card] | **Round:** [number] | **Session dates:** [dates]
## Who counts as a tester
| Group | Need and situation | Screening questions | Counts if | How many | Where we find them, who asks |
|---|---|---|---|---|---|
| [group] | [need, situation] | [two or three questions] | [answer that shows the need] | [number] | [place, role] |
## Not testers
[Colleagues, the leaders who asked, friends, anyone who has seen the spec], each with [reason]. Pilot only.
## Invitation
[Message: it is a prototype; [minutes] minutes; we are testing the design, not you; taking part is voluntary; how to reply]
## Consent note
We are [role and team] and we are doing this to [why]. In the session you will [what happens]. We collect [data]. The session is [observed by whom / recorded how]. Results are used for [use] and seen by [roles]. We keep your data until [date], then delete it. Taking part is voluntary. You can stop or withdraw at any time, and we delete your data if you do.
**Agreed:** [participant code], [date], [how consent was given]
## Records
| Participant code | Round | Consent record stored at | Data it covers | Delete by |
|---|---|---|---|---|
| [P1] | [number] | [location] | [notes, recording] | [date] |
## Decision
[The role who owns the test] approves the tester definition and the consent note by [date], before any invitation is sent. Consent and recording wording: check with a qualified adviser.
```

## Done When
- Every tester group is defined by a need and a situation, with screening questions about recent behaviour.
- The not-testers list is written, and nobody on it is counted in a session total.
- The consent note covers all seven points, and a person has read it before it goes out.
- Every participant has a code, a stored consent record and a deletion date.

## Quality Bar
- Screening selects for the need. It never selects for, or records, personal characteristics beyond what the belief requires.
- Participants are codes from the first note onward. No screening note judges a person.
- The invitation says "prototype" and never suggests the thing is finished or available.
- Numbers of testers are a rule of thumb for finding problems. They prove nothing about how many people want the idea.
- Real target users test it: colleagues, the leaders who asked and simulated users are not testers. Consent and recording law: check with a qualified adviser.

## Next
Run build-usability-test-plan (Five-User Usability Test Plan) to write the tasks and the moderator script for these sessions.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
