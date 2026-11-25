---
name: litig-deposition-prep
version: 1.0.0
description: Prepare for a deposition by building an examination outline, key-topic map, exhibit set, and either witness prep or a taking-the-depo strategy.
author: matrixx0070
tags: [litigation, discovery, depositions, witness-prep, trial]
capabilities: []
---

## When to use
Reach for this when you are getting ready for a deposition and need a structured outline, a topic-and-exhibit map, or a plan to prepare your own witness. Use it whether you are taking the deposition or defending one. It helps you sequence topics, tie exhibits to questions, and flag areas that need attorney sign-off.

**Not for:** subpoena mechanics (see litig-subpoena-triage), privilege logging (see litig-privilege-log-review), or drafting briefs (see litig-brief-section-drafter).

## Method
1. Fix your role. Taking the depo means fact extraction and locking in admissions; defending means preparing and protecting your witness.
2. **Decision point:** If taking, build a topic outline funneling from background to key disputed facts. If defending, build a witness-prep checklist (tell the truth, answer only what is asked, pause before answering, do not guess).
3. Map every disputed fact to the documents that prove it; assign each exhibit a marking sequence.
4. Draft open-ended questions for discovery topics and closed leading questions to pin admissions.
5. **Decision point:** If the witness is an expert, add Daubert-adjacent questions on methodology and basis; if a fact witness, focus on personal knowledge and foundation.
6. ATTORNEY-ESCALATION gate: Route the outline, prep script, and any advice to the witness to a supervising attorney for review before the deposition.

## Example
> Defending a former employee in a wrongful-termination suit. You build a prep checklist, review the three performance memos likely to be marked, and rehearse the "I don't recall" versus guessing distinction. You flag one memo as arguably privileged and route it to the supervising attorney before the session.

## Pitfalls
- **Over-coaching:** Preparing a witness on substance is proper; scripting answers or telling them what to say can constitute improper coaching or obstruction.
- **Unmarked exhibits:** Failing to pre-mark and sequence exhibits wastes record time and creates confusion on the transcript.
- **Asking one question too many:** When taking, stop once you have the admission; the extra question invites explanation.
- **Ignoring objections-to-form:** Sloppy compound or leading questions draw objections that can spoil an answer at trial.

## Output format
```
DEPOSITION PREP — [Witness] — [Taking/Defending]
Objective: [locked admissions OR protection goals]
Topics:
  1. [Topic] -> Exhibits: [Ex. #] Questions: [key Qs]
Exhibits: [# | description | source Bates]
Risk areas / privilege flags: [...]
Attorney review: [name | date | status]
```

## Reference
Under FRCP 30, a deposition is generally limited to one day of 7 hours absent stipulation or court order (30(d)(1)); many states mirror this but vary. Objections must be stated concisely and non-suggestively; a deponent may be instructed not to answer only to preserve a privilege, enforce a court limitation, or present a 30(d)(3) motion. Errors in transcription may be corrected via the 30(e) errata process, typically within 30 days of the transcript's availability. For 30(b)(6) organizational depositions, the noticing party must describe topics with reasonable particularity and the entity must prepare a witness to testify on the organization's behalf. Deadlines and 7-hour rules vary by jurisdiction; confirm local rules and any standing order. This is general litigation practice, not legal advice.
