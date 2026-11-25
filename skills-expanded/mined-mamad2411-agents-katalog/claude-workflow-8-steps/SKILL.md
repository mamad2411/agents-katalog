---
name: claude-workflow-8-steps
description: The "Stop using Claude one prompt at a time" workflow from @ai.am.claude (10-slide carousel, slide 2 missing from the upload) - raw material, find the signal, turn analysis into action, create the deliverable, critique version one, structure the prompt, review and refine, use it - with each slide's example prompt quoted and a runnable chain. Use when someone wants a repeatable multi-step way to work with Claude instead of a single prompt, or wants the eight prompts to paste.
---

# Claude workflow, 8 steps

Source: @ai.am.claude, "Stop using Claude one prompt at a time. Build a workflow instead. One task. Multiple steps. Better result." Slides 1, 3 to 10 of 10 were uploaded; **slide 2 was not**, so anything it said is unknown. The example prompts below are quoted from the slides; the "why" column is mine.

| Step | Slide | Instruction | Example prompt (quoted) | Why it helps [Likely] |
|---|---|---|---|---|
| 01 | 3 | Give Claude the raw material (notes, documents, emails, data, ideas), then say what you want to achieve | "I'm going to give you raw information. First analyze it. Don't create the final output yet." | Stops it writing before it has read |
| 02 | 4 | Find the signal: key information, patterns, gaps, risks, contradictions, open questions | "Analyze this first. What matters most, what is missing, and what requires my attention?" | Surfaces gaps while they are cheap to fix |
| 03 | 5 | Turn analysis into action: tasks, owners, priorities, deadlines, next steps | "Turn your analysis into an actionable plan. Prioritize the next steps and flag anything that requires a decision." | Separates thinking from deciding |
| 04 | 6 | Create the deliverable: email, report, presentation, checklist, meeting agenda | "Using the approved action plan, create a concise follow-up email for the team." | The deliverable is built from an approved plan, not from scratch |
| 05 | 7 | Do not accept version one: critique, point out what is unclear, missing or repetitive, suggest, refine | "Critique this output before I use it. What is unclear, missing, repetitive or potentially misleading? Then improve it based on your critique." | A second pass catches what the first missed |
| 06 | 8 | Structure the prompt: goal, context, requirements, format, examples, constraints | "Create a step-by-step plan to... Goal: ... Context: ... Requirements: ... Format: ... Examples: ... Constraints: ..." | Removes guessing about what "good" means |
| 07 | 9 | Review and refine: check accuracy, clarity, shorter or more professional | "Review this text and suggest improvements. Make it clearer, more professional and concise. Highlight what could be added, removed or rephrased." | Edits are visible, so you can reject them |
| 08 | 10 | Turn ideas into action: final version, right format, practical output, next steps | "Using the refined version, create a final document/presentation/report in [format]. Make it ready to use, with clear structure and key takeaways. Also suggest next steps." | Ends with something usable |

## Weaknesses to know

- A model critiquing its own output shares its blind spots. For anything with facts, numbers or legal weight, step 07's "check for accuracy" is not verification; check against the sources yourself. [Certain]
- Step 04 sends text to a team. Treat it as a draft; a person approves before it is sent.
- The carousel gives no evidence that this beats one well-written prompt. It is a sensible habit, not a measured result. [Likely]

Use `/claude-workflow` to run it on a real input. Related: `hallucination-guardrails-6`.
