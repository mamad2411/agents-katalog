---
description: Evaluate a generated resume against the job description using the evaluator rubric
argument-hint: [resume prefix e.g. Google_SWE]
allowed-tools: Read, Write
---

> Allowed file operations: Read any file listed in the steps below. Write ONLY to `prompts/daily_feedback.json`. Do not create any new files or write to any other path under any circumstance.

Evaluate the resume `output/extras/$ARGUMENTS_Resume.txt` against the current job description.

Follow these steps exactly:

1. Read `output/extras/$ARGUMENTS_Resume.txt` — this is the plain-text extract of the resume, parsed from the LaTeX source by the backend before invoking this command; it contains Technical Skills, Experience, Projects, and Education in clean readable format with no binary artifacts
2. Read `output/extras/$ARGUMENTS_jd.txt` — this is the job description snapshot written by the backend specifically for this evaluation run; it is isolated per-job and guaranteed to match the JD used to generate this resume
3. Read `prompts/prompt_summary.txt` — this contains the condensed rule reference used during generation (use as the `system_prompt` / `user_constraints` context for the evaluator)
4. Read `prompts/evaluator_prompt.txt` — this contains the role, scoring categories, output schema, and rule_reference_map

5. Apply the full evaluation rubric from `prompts/evaluator_prompt.txt` to the resume text from step 1, using:
   - `output/$ARGUMENTS_jd.txt` content as the `job_description` input
   - `prompts/prompt_summary.txt` content as the `system_prompt` and `user_constraints` context
   - Set `resume_id` to `$ARGUMENTS`

6. Read `prompts/daily_feedback.json` if it exists:
   - If it exists and contains a valid JSON array, append the full evaluation result object to that array
   - If the file does not exist, is empty, or does not contain a valid JSON array, create a new array containing only the evaluation result object
   - Write the updated array back to `prompts/daily_feedback.json`

7. Output ONLY the following JSON object to stdout (nothing else — no markdown, no prose):
   `{"total_score": <number>}`
