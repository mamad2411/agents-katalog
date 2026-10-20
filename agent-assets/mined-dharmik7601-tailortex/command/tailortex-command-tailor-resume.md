---
description: Generate a tailored LaTeX resume for the current job description
argument-hint: [output-filename e.g. Google_SWE]
allowed-tools: Read, Write
---

> Allowed file operations: Read any file listed in the steps below. Write ONLY to `output/$ARGUMENTS_Resume.tex`. Do not create any other files.

Generate a tailored LaTeX resume. Output filename prefix: $ARGUMENTS

Follow these steps exactly:

1. Read `resumes/master_resume.tex` — split the content at `\begin{document}`. Store the preamble (everything before and including `\begin{document}`) and the body separately. Do not modify the preamble under any circumstance.

2. Read `job_description.txt` — this is the target role to tailor for.

3. Read `prompts/system_prompt.txt`, `prompts/user_constraints.txt` (if non-empty), and `prompts/additional_projects.txt` (if non-empty) — these are the generation rules, personal constraints, and project bank respectively. Apply all of them when generating the resume body.

4. Generate the tailored resume body by applying all rules from step 3 to the master resume body from step 1, targeting the job description from step 2. The system_prompt formatting_constraints define exact section and bullet counts that guarantee a one-page fit — follow them precisely and the output will fit one page without any post-generation adjustment.

5. Reassemble the full `.tex` file by prepending the original preamble from step 1 to the generated body. Write the complete file to `output/$ARGUMENTS_Resume.tex`.

6. Confirm `output/$ARGUMENTS_Resume.tex` exists. The backend will handle compilation, cleanup, and opening the PDF.