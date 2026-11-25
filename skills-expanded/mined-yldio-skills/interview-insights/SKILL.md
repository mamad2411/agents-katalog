---
name: interview-insights
description: Turns a client interview or discovery call transcript into a list of every problem and need raised, each attributed to the person who said it, with a second pass for anything missed and a list of unclear comments. Use after a client interview when you have the transcript or recording.
---

# Extract Client Problems and Needs From Interviews

## When to use

After a client interview or discovery call, when you have the transcript and need
the problems raised captured and attributed before the detail fades.

## You need

- The interview transcript, or an audio file the tool can transcribe. Claude
  cannot watch video, so transcribe a video recording first.
- The attendees' names and roles, if the transcript does not show them.
- Written authorisation from the client to process the recording with an AI tool.
  Do not start without it.

## Role

You are analysing a recorded client interview. Members of the client team attended
the meeting.

## Steps

1. Analyse the full interview.
2. Identify who from the client team attended the meeting. If the transcript does
   not show names, ask the user rather than guessing.
3. Find every problem and need that was mentioned.
4. Review all the feedback given in the meeting and assess whether it holds
   together. Say where two points contradict each other or where a claim is not
   supported by anything else in the interview.
5. After the first pass, review the whole interview again and look for anything
   important you did not find the first time.
6. Do not guess. If an idea or comment is unclear, do not interpret it; list it in
   the final section.

## Output

Generate all the content in the chat.

1. Attendees: name and role for each person from the client team.
2. Problems and needs: a bullet list, each item attributed to the person who
   raised it.
3. Sense check: anything that contradicts or does not hold together, with who
   said it.
4. Unclear: ideas or comments that are not clear, so they can be analysed later.

## Before it goes out

- Go back to the recording and check attendees are named correctly.
- Every problem and need is attributed to the right person.
- Nothing significant is missing.
- Each item in the "Unclear" list genuinely needs follow-up rather than a closer
  listen.

This output is a draft, never a deliverable on its own.
