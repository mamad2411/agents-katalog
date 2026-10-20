---
name: ask-a-coworker-for-help
domain: communication
locale: [generic]
interface: mixed
difficulty: basic
est_time: 15min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

Ask a coworker for help in a way that is specific, respectful of their time, and easy for them to answer without taking ownership of your whole problem.

## Preconditions

- A work problem you cannot efficiently solve alone.
- Evidence that you tried reasonable first steps: docs, search, logs, prior examples, or a quick experiment.
- A sense of the coworker's role, workload, and whether they are the right person.

## Steps

1. **Define the exact help needed.** Decide whether you need a pointer, review, decision, debug session, context, approval, or introduction. → *Expect:* your ask has a shape smaller than "help me."
2. **Show what you tried.** Gather links, error messages, options considered, and the point where you got stuck. → *Expect:* the coworker can start from your work instead of repeating it.
3. **Choose the right channel.** Use chat for quick pointers, a ticket or doc comment for trackable work, and a meeting only when live back-and-forth is needed. [BRANCH: quick question | deeper help] ask in chat for quick context; send a short agenda for deeper help. → *Expect:* the medium fits the effort.
4. **Write the ask with constraints.** Include context, the specific question, deadline, and what answer format would help. → *Expect:* they can answer yes, no, or with a pointer.
5. **Respect their time.** Offer a bounded option: "Could you spend 10 minutes pointing me to the right owner?" or "If you are not the right person, who should I ask?" → *Expect:* the request does not silently claim their afternoon.
6. **Offer reciprocity or cleanup.** Say you will document the answer, take the next step, or return the favor on something you can help with. → *Expect:* the exchange feels collaborative, not extractive.
7. **Use the help well.** Listen, take notes, confirm next actions, and do the follow-through yourself. ⚠️ *Irreversible:* forwarding blame or exposing a coworker's informal advice can damage trust, so ask before quoting them in a wider thread. → *Expect:* the coworker sees their help turned into progress.
8. **Thank and close the loop.** Send a quick thanks and, later, the result: "Your pointer to the cache key fixed it." → *Expect:* they know the time was useful.

## Decision points

- If the issue is urgent production risk → follow the incident or escalation process, not only a friendly ask.
- If the coworker is overloaded → ask for a pointer or a better owner instead of a full session.
- If you need emotional support rather than technical help → name that separately and choose someone appropriate.
- If the answer affects ownership → document it in the shared system after confirming.

## Failure modes & recovery

- **F1 Ask is too broad:** detect no response or "what do you need?" → rewrite with the specific question and desired outcome.
- **F2 You skipped basics:** detect the coworker pointing to obvious docs → read them, summarize what you learned, and ask the remaining question.
- **F3 Help becomes handoff:** detect them doing the whole task → take back ownership and ask for review instead.
- **F4 You forget thanks:** detect the issue is solved but the helper heard nothing → send the outcome and appreciation now.

## Verification

The coworker received a specific bounded ask, saw what you already tried, and got a thank-you or outcome update after helping.

## Variations

- Remote teams: include links, screenshots, timezone, and async-friendly context.
- New job: ask for pointers and norms, and document what you learn for the next new person.
- Cross-functional ask: explain acronyms and business context before the technical request.

## Safety & privacy

Low risk, but workplace trust matters. Do not share credentials, confidential customer data, private personnel details, or informal advice outside its intended context.
