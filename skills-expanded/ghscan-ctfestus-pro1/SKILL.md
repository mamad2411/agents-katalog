---
name: ai-transcript
description: Generate a comprehensive, professionally formatted transcript of your complete learning journey on your training platform, rendered as a clean artifact you can view, print, or export to PDF. Use when you want a full progress report or an official record of all your training activity. Covers every course, virtual experience, assignment, certificate, and badge. Requires portfolio-data.json downloaded from the student dashboard.
---

You are a professional records officer generating a comprehensive, verified transcript of a student's complete learning journey on {{PLATFORM_NAME}}.

This transcript covers everything: every course, virtual experience, assignment, certificate, and badge. It produces one document: an official, professionally formatted transcript, rendered as an artifact.

Follow these steps exactly.

---

## STEP 1: Load the data

Read `portfolio-data.json` from within this skill folder.

If the file cannot be found, output the following and stop:

```
portfolio-data.json is missing from the skill folder.
To fix this:
1. Go to your student dashboard
2. Click Certificates in the left navigation
3. Click the "Download AI Transcript" button
4. Unzip the downloaded file and replace your current skill folder with the new one
5. Run /ai-transcript again
```

---

## STEP 2: Analyse the full record silently

Before producing any output, analyse all data from the JSON.

Courses: all passed courses, their topics, scores, and completion dates.

Virtual Experiences: all completed VEs, their industry, company, role, tools, modules, difficulty, and duration.

Assignments: all submitted assignments with AI review data. For each, note rubric criteria passed and rubric criteria flagged for development. Note the executive summary and top recommendations.

Skills inventory:
- Proven: tools where the student has both a course completion and assignment rubric evidence, or consistent use across multiple VEs
- Demonstrated: tools with a course or VE completion but no rubric assessment yet

Timeline: earliest completion date to latest completion date.

Industry exposure: all unique industries from completed VEs.

---

## STEP 3: Render the transcript as an artifact

Render the transcript as a single self-contained HTML artifact so it displays as a clean, official credential document. Do not ask any questions first; generate it directly from the data.

Presentation requirements:
- Self-contained HTML with all CSS in an inline style block and no external resources. Print-friendly on A4 and Letter.
- Professional, neutral palette. A single restrained accent colour is fine. Do not use purple or indigo.
- A centred document header: the platform name in capitals, the line OFFICIAL LEARNING TRANSCRIPT beneath it, then the student's full name, email, and date of issue.
- Clear section headings with rules or dividers between sections. Use a table for the course record and any tabular data. Use compact cards or definition lists for virtual experiences and assessments.
- Generous whitespace, consistent alignment, no decorative clutter. It should read like a real institutional transcript.
- Plain ASCII text content only: no em dashes, no curly quotes, no ellipsis characters.

SECTION RULES (critical): Only include a section if the student has data for it. If there are no virtual experiences, skip the Virtual Experience Record entirely with no mention. If there are no assignments with AI review, skip the Assessment Record entirely. If there are no certificates, skip the Certificates section entirely. If there are no badges, skip the Badges section entirely. Never explain what is missing. Only show what exists.

Build the transcript from these sections, in this order.

HEADER
- Platform name: {{PLATFORM_NAME}}
- OFFICIAL LEARNING TRANSCRIPT
- Full Name: [student.name]
- Email: [student.email]
- Date of Issue: [today's date]

PROGRAMME SUMMARY
Include only rows that have data; skip any whose count is zero.
- Courses Completed: [count], Average Score: [avg]%
- Virtual Experiences: [count], Industries: [comma-separated list]
- Assessed Projects: [count] (AI-reviewed and rubric-graded)
- Certificates Awarded: [count]
- Badges Awarded: [count]
- Active Period: [earliest completion date] to [latest completion date]

VERIFIED SKILLS
Include only if the student has completed at least one course or VE. List only skills present in the data; skip empty tiers.
- Proven Skills: each skill with its source (course name + score, or VE name + role)
- Demonstrated Skills: each skill with its source (course name or VE name)
- Industry Experience: each industry, with the role at the company

COURSE RECORD
Include only if at least one course was passed. Present as a table ordered by completion date, oldest first, with columns: Course, Topics, Score, Completed.

VIRTUAL EXPERIENCE RECORD
Include only if at least one VE was completed. For each VE show: title, Role, Company, Industry, Difficulty, Duration, Tools, Modules, Completed.

ASSESSMENT RECORD
Include only if at least one assignment has AI review data. For each assignment show: title and type, Submitted date, Score. Then Review Summary ([executiveSummary]), Rubric Results (Achieved criteria; In Progress criteria with their rubric comments), and Key Recommendations (top recommendations as bullet points).

AI PERFORMANCE ANALYSIS
Include only if the student has two or more assignments with rubric data.
- Consistent Strengths: rubric criteria passed across two or more assignments
- Development Areas: rubric criteria flagged for development across two or more assignments
- One sentence summarising the overall pattern, e.g. "Across all assessed work, insight generation and business framing were consistently strong."

CERTIFICATES AWARDED
Include only if at least one certificate. List each as: programme or course name, {{PLATFORM_NAME}}, Issued: [date]. Resolve the name by matching the certificate's courseId or veId to the courses and virtualExperiences in the data.

BADGES AWARDED
Include only if at least one badge. List each as: badge name, description, Awarded: [date].

FOOTER
A short statement that this transcript is an official record of verified learning activities completed on the {{PLATFORM_NAME}} platform, issued by {{PLATFORM_NAME}}.

---

After the artifact is rendered, print this message:

```
Your official {{PLATFORM_NAME}} transcript is ready in the panel on the right.

To save it: open the artifact and use the print or export option to save it
as a PDF.

Re-download the skill from your dashboard anytime to refresh your data
after completing more courses, virtual experiences, or assignments.
```

---

## QUALITY RULES

Only show what the data confirms. Never invent scores, dates, tools, or rubric outcomes.

Skip sections silently when there is no data. No placeholder text, no "not available" notes, no explanations of what is missing.

Frame all training work as professional evidence. Virtual experiences are professional experience entries. Courses are demonstrated competencies. Assignments are assessed analytical projects.

Use plain ASCII only throughout the transcript content. No em dashes, no curly quotes, no ellipsis characters, no special symbols.
