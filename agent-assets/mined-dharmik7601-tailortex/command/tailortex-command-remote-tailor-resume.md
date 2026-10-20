---
description: Generate a tailored LaTeX resume from a job description passed directly as an argument
argument-hint: [CompanyName ||| Full job description text]
allowed-tools: Read, Write, Bash
---

> Allowed file operations: Read any file listed in the steps below. Write ONLY to `output/$COMPANY_Resume.tex` and `C:\Users\Dharmik\Desktop\Resumes\`. Do not create any other files.

Generate a tailored LaTeX resume from an inline job description. 

Follow these steps exactly:

1. Parse $ARGUMENTS by splitting on the first occurrence of `|||`. The text before `|||` (trimmed) is the COMPANY_NAME. The text after `|||` (trimmed) is the JOB_DESCRIPTION. If `|||` is not found, stop and print: "Error: arguments must be in the format: CompanyName ||| job description text"

2. Read `resumes/master_resume.tex` — split the content at `\begin{document}`. Store the preamble (everything before and including `\begin{document}`) and the body separately. Do not modify the preamble under any circumstance.

3. Read `prompts/system_prompt.txt`, `prompts/user_constraints.txt` (if non-empty), and `prompts/additional_projects.txt` (if non-empty) — these are the generation rules, personal constraints, and project bank respectively. Apply all of them when generating the resume body.

4. Generate the tailored resume body by applying all rules from step 3 to the master resume body from step 2, targeting the JOB_DESCRIPTION from step 1. The system_prompt formatting_constraints define exact section and bullet counts that guarantee a one-page fit — follow them precisely and the output will fit one page without any post-generation adjustment.

5. Reassemble the full `.tex` file by prepending the original preamble from step 2 to the generated body. Write the complete file to `output/$COMPANY_NAME_Resume.tex`.

6. Compile using the local script:
   `python local/compile.py --tex output/$COMPANY_NAME_Resume.tex --prefix $COMPANY_NAME --output output --type resume`

   If the script exits with a non-zero return code AND no PDF was produced at `output/$COMPANY_NAME_Resume.pdf`:
   - Read `output/$COMPANY_NAME_Resume.tex` and scan for common LaTeX errors:
     - Unescaped special characters: `&` → `\&`, `%` → `\%`, `$` → `\$`, `#` → `\#`
     - Unescaped underscores outside math mode: `_` → `\_`
     - Mismatched braces `{` / `}`
   - Apply all detected fixes to `output/$COMPANY_NAME_Resume.tex`
   - Retry the compile command once:
     `python local/compile.py --tex output/$COMPANY_NAME_Resume.tex --prefix $COMPANY_NAME --output output --type resume`
   - If it fails again, stop and print the exact error. Do not retry more than once.

   If the script exits with a non-zero return code BUT the PDF exists at `output/$COMPANY_NAME_Resume.pdf`, treat it as a warnings-only compile and continue — do not retry.

7. Clean up any auxiliary files not already removed by compile.py:
   `if exist output\$COMPANY_NAME_Resume.aux del output\$COMPANY_NAME_Resume.aux`
   `if exist output\$COMPANY_NAME_Resume.log del output\$COMPANY_NAME_Resume.log`
   `if exist output\$COMPANY_NAME_Resume.out del output\$COMPANY_NAME_Resume.out`

8. Confirm `output/$COMPANY_NAME_Resume.pdf` exists. If it does not exist at this point, stop and print: "Compilation failed — PDF not found at output/$COMPANY_NAME_Resume.pdf"

9. Copy both output files to the desktop folder:
   `copy output\$COMPANY_NAME_Resume.tex "G:\Other computers\My Laptop\Documents\Resume\Custom\Remote Generated\$COMPANY_NAME_Resume.tex"`
   `copy output\$COMPANY_NAME_Resume.pdf "G:\Other computers\My Laptop\Documents\Resume\Custom\Remote Generated\$COMPANY_NAME_Resume.pdf"`