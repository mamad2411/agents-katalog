---
name: 5-why
description: Performs 5-Why root-cause analysis (RCA) from the Toyota Production System, tracing a problem through five why-questions in dialog until the actual cause — not the symptom — is found. Use when the user says root cause, RCA, postmortem, incident, retrospective, recurring bug, "why does this keep happening", 5 whys or 5w, or reports a defect or failure that keeps coming back. Also handles the what-for variant for sharpening goals or OKRs. Not for complex social systems with circular causality (team dynamics, feedback loops) — label results as hypotheses there.
license: MIT
---

# 5-Why Method

Five "Why?" questions lead from an observation to its actual root cause.
The method comes from the Toyota Production System and is attributed to
Toyoda Sakichi. Its core discipline: never settle for the first plausible
explanation.

## Procedure

1. **Capture the observation.** Formulate the situation together with the
   user as a concrete, verifiable fact — not an interpretation.
   ("Printer returns error E-04 since Tuesday", not "IT is incompetent".)
2. **Ask five why-questions in dialog with the user.** One question per
   message, numbered (1st why … 5th why). Each question targets the previous
   answer, so every link in the chain connects to its predecessor. Never ask
   all five at once.
3. **Name the root cause** and derive a solution approach that addresses the
   cause itself — not the symptom.

## Rules for good why-questions

- Questions may be phrased positively or negatively. Next to "Why did this
  happen?", often more effective: "Why did the opposite NOT happen?"
- Five is a guideline, not law. The root cause may surface after 2–3
  questions; sometimes more are needed. Stopping early at the first plausible
  explanation is the real mistake this method guards against.
- Dead end? Step back 1–2 levels and rephrase the last question. A different
  question steers the chain toward a different insight.

## Limits

- The method fits linear-causal relationships: processes, technical systems,
  defects. On complex social systems (team dynamics, feedback loops) it loops
  or oversimplifies — there, present the result explicitly as a hypothesis,
  not a root cause.
- There is no single root cause. Different question chains yield different,
  equally usable causes.

## The what-for variant

Replacing "why" with "what for" flips the view from the rear-view mirror
(cause analysis) to the windshield (goal development). Use this variant when
the user wants to sharpen goals or OKRs: ask "What is this for?" instead of
"Why is this so?"

## Output format

Document the full chain when the analysis concludes:

```
Observation: <concrete, verifiable fact>
1st why: <answer>
2nd why: <answer>
3rd why: <answer>
4th why: <answer>
5th why: <answer>
Root cause: <…>
Solution approach: <addresses the cause, not the symptom>
```

Also include discarded partial chains from dead ends — they document which
paths were ruled out and why.

For deeper method guidance see `reference.md` in this folder; for worked
analysis chains see `examples.md`.
