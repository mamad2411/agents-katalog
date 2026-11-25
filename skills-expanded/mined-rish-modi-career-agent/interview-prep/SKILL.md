---
name: interview-prep
description: Behavioral interview prep, mock interviews, company research, and round-specific cheat-sheets. Selects from the project STAR files in $PERSONAL/career/star/ and orchestrates them into prep artifacts. For coding interviews, use coding-prep. For creating new STAR project files, use star-stories.
---

# Interview Prep

## Scope and boundaries
This skill **selects, sequences, and rehearses** behavioral material. It does not create the raw stories.

- Project STAR records live in `$PERSONAL/career/star/<slug>.md`, owned by the `star-stories` skill.
- Behavioral coverage audits, mock interviews, company research, and cheat-sheets are owned here.
- Coding interview prep is owned by `coding-prep`.

If a needed story is missing from `$PERSONAL/career/star/`, this skill does not write a new STAR file. It tells the user to run `/star-stories <project>` and resumes once the file exists.

## Inputs

`$PERSONAL` is the personal-docs sibling directory defined in `CLAUDE.md`. Resolve once at the start of the session.

**Always available:**
- `$PERSONAL/career/star/*.md` — project STAR records (source of truth for behavioral material).
- `$PERSONAL/career/impact-doc.md` — fallback when star/ is missing coverage; used to recommend which projects to STARify next.
- `$PERSONAL/career/goals.md` — read if exists; informs which competencies the user wants to emphasize.

**Per role (when relevant):**
- `$PERSONAL/applications/<company>/<role-slug>/role.md` — fit analysis and Job Description.
- `$PERSONAL/applications/<company>/<role-slug>/brief.md` — company brief from Mode 3.
- Prior round cheat-sheets in the same folder.

## The competency index

Several modes need a `competency → [(file, angle)]` map. Build it once per session by scanning `$PERSONAL/career/star/*.md`:
- Read each file's frontmatter `primary_competencies` array.
- Scan the body for `## Angle N:` headers (each angle is what gets recommended, not the whole file).
- Map each competency to the list of `(file, angle title)` pairs that support it.

This index is in-memory only. Not persisted. Rebuilt on each session because star/ files change.

Standard competency vocabulary (use these tags consistently across modes):
- leadership, influence-without-authority
- conflict (peer, manager, cross-team)
- ambiguity, defining-the-problem
- failure-and-recovery
- technical-depth, architecture
- leverage, multiplying-team-output
- mentorship, scaling-through-others
- difficult-tradeoff, scope-quality-time
- cross-functional-partnership
- driving-change-in-a-large-org
- data-judgment, product-influence
- on-call, production-incident
- agent-architecture, MCP, AI-product

If a star/ file uses a non-standard competency in its frontmatter, accept it but flag the drift in the audit output.

## Modes

### Mode 1: Behavioral coverage audit

**Triggered by:** "audit my stories", "do I have coverage for X", "where are my gaps".

**Read-only.** Does not write to star/, does not write to story-bank.json (deprecated).

Steps:
1. Build the competency index.
2. Report coverage in three buckets:
   - **Strong** (3+ projects support this competency)
   - **Thin** (1-2 projects)
   - **Gap** (0 projects)
3. For each Gap and Thin competency, look at `$PERSONAL/career/impact-doc.md` and recommend one specific project that would close the gap. Output as: "Run `/star-stories <project>` to add coverage on <competency>."
4. End with a one-line summary: "X competencies strong, Y thin, Z gaps."

Do not write a new file. Do not propose draft stories. The audit's job is to point at what's missing, not fill it.

### Mode 2: Mock interview

**Triggered by:** "mock interview", "let's practice", "run a mock for the Pinecone HM round".

**Setup:**
- Confirm company, role-slug, round type (recruiter / hiring manager / tech screen / onsite behavioral / system design framing / cross-team collab), interviewer role, and time budget.
- Confirm: strict mode (stay in character, feedback at end) or coaching mode (feedback after each answer).
- Build the competency index. Pre-load the role's `role.md` if it exists.

**During:**
- Ask one question at a time. Don't telegraph what's coming.
- For each answer, evaluate on:
  - **Structure:** STAR? easy to follow?
  - **Specificity:** real details, named systems, real numbers? or vague?
  - **Ownership:** I vs we; did the user's contribution come through?
  - **Outcome:** quantified impact?
  - **Length:** 2-4 min ideal. Flag rambling or under-delivery.
- After each answer (coaching mode) or at the end (strict mode), name the specific star/ file and angle that would have landed it better, e.g.: "[agentic-dev-team.md](../../career/star/agentic-dev-team.md) Angle 1 (technical depth) was a stronger fit than the one you used."
- If the user reaches for a project that has no star/ file, flag it: "I don't have a STAR file for that project. Run `/star-stories <project>` after this mock to capture it."

**End:**
- Overall assessment.
- Top 2 strengths and top 2 things to fix before the real interview.
- **Stories to rehearse** list: 3-5 `(file, angle)` pairs that the user should drill before the real round.
- Save the transcript and feedback to `$PERSONAL/applications/<company>/<role-slug>/interview-prep/mock-<round>-<YYYY-MM-DD>.md`.

### Mode 3: Company / role research

**Triggered by:** "research Pinecone", "build me a brief for this role", "what should I know before this interview".

When the user names a company and an upcoming interview:
1. Search: recent news (last 6 months), product launches, financial signals, leadership changes, engineering blog posts, glassdoor patterns.
2. Surface: known interview format, leadership principles or values they evaluate on, likely interviewers if named.
3. Generate likely questions based on the role + company patterns.
4. **New step:** Build the competency index. For each likely question pattern, recommend a specific `(file, angle)` pair from star/ that would land it. If no good match exists, flag it as a gap and suggest the project worth STARifying.

Don't dump search results. Synthesize. End with a one-page brief at `$PERSONAL/applications/<company>/<role-slug>/brief.md`.

The brief must include a **"Recommended stories for this loop"** section: 3-5 file pointers mapped to the round structure (recruiter, HM, tech screen, onsite, behavioral, system design).

### Mode 4: Cheat-sheet generation

**Triggered by:** "build me a cheat-sheet for the Pinecone HM call", "prep cheat-sheet for tomorrow's recruiter screen", or implicit ("I have the HM call tomorrow").

**Inputs:**
- Company, role-slug (required).
- Round type (required): recruiter / hiring-manager / tech-screen / onsite-behavioral / system-design / cross-team-collab.
- Interviewer name and time (optional; fill in `[FILL IN]` if missing and ask the user before the call).

**Reads:** role's `role.md` (must exist), `brief.md` (if exists), all star/ files via competency index, prior cheat-sheets in the same folder.

**Output:** `$PERSONAL/applications/<company>/<role-slug>/<round>-cheat-sheet.md` with this exact structure:

```markdown
# <Company> <Round> — Cheat Sheet

**Role:** <position>
**Interviewer:** <name or [FILL IN]>
**When:** <date>, <time or [FILL IN]>
**Stories ready:** <bulleted markdown links to the 3-5 star/ files most relevant to this round>

---

## Opening pitch (30 sec, round-tuned)
<Pitch text. Different for recruiter, HM, tech screen, etc.>

---

## Lead stories (rehearse in order)

### Lead 1: <Project Name> — Angle N (<competency>)
<One-sentence framing of the angle. What to land on. Link to the star/ file:angle.>

### Lead 2: <Project Name> — Angle N (<competency>)
<Same shape.>

### Lead 3: <Project Name> — Angle N (<competency>)
<Same shape.>

Backup stories: <links to 2-3 more star/ files that cover adjacent competencies, no angle pre-selected>

---

## Predicted questions and the angle to play

| Question | Story | Anti-pattern to avoid |
|---|---|---|
| <Likely question 1> | <project.md Angle N> | <what not to do> |
| (4-7 rows, drawn from the role's fit profile + brief if it exists) | | |

---

## Gap framing
<Address the 1-3 weakest fit signals or risks for this role, e.g. "On the Rust/Go gap" or "On the SDK shipping gap". Direct framing, no apology.>

---

## Level / comp framing (only if relevant to this round)
<For recruiter and HM rounds. Skip for tech screens.>

---

## Questions to ask the interviewer (pick N)
<Categorized: technical/scope, team/working-style, strategic, mutual-fit. 6-8 questions, user picks 3-4 in the room.>

---

## What to listen for (signal vs noise)
<Round-specific tells. 3-5 items.>

---

## Don't do these
<3-6 anti-patterns specific to this round and this role.>

---

## After the call
<3-item capture list for role.md Notes within 10 min of hanging up.>
```

**Round-specific adjustments to the template:**

- **Recruiter:** Heavy on logistics, comp framing, level disambiguation. Light on technical depth. Don't include the "Lead stories" deep dive; replace with "Project highlights to mention if asked."
- **Hiring manager:** Heavy on Lead stories, predicted questions, gap framing, level framing. This is the canonical shape.
- **Tech screen (coding):** Replace "Lead stories" with "Approach patterns to lean on" + "Communication checklist." Replace "Predicted questions" with "Problem-type predictions." Defer to `coding-prep` for the actual practice.
- **System design:** Replace "Lead stories" with "Architecture patterns I should reach for" (drawing on agentic-dev-team, doc-first-extraction, design-system-mcp). Add a "Trade-off vocabulary" section.
- **Onsite behavioral:** Heavy on Lead stories. Add a "Story rotation plan" that prevents recycling the same 2 stories across 4 interviewers. Cross-reference which stories were already used in earlier rounds (read prior cheat-sheets in the folder).
- **Cross-team collab:** Heavy on cross-functional-partnership and conflict angles. Lead with vendor-drawer-ab, supplier-payments-plus, doc-first-extraction Angle 4.

**If a cheat-sheet already exists at the target path, prompt:**
- **Overwrite** — regenerate from scratch.
- **Revise** — apply targeted updates while preserving structure.
- **Cancel** — print to terminal only.

## Output discipline
- Audit (Mode 1): terminal only, no file writes.
- Mock interview (Mode 2): transcript + feedback at `$PERSONAL/applications/<company>/<role-slug>/interview-prep/mock-<round>-<YYYY-MM-DD>.md`.
- Brief (Mode 3): `$PERSONAL/applications/<company>/<role-slug>/brief.md`.
- Cheat-sheet (Mode 4): `$PERSONAL/applications/<company>/<role-slug>/<round>-cheat-sheet.md`.
- Never write to `$PERSONAL/career/star/`. That's star-stories' territory.
- `story-bank.json` is deprecated. Existing files are ignored, not deleted. Do not create new ones.

## Anti-patterns
- Don't draft or rewrite STAR stories. If material is missing, point at star-stories. Don't duplicate its job.
- Don't grade mock answers generously. Weak is weak.
- Don't recycle the same 2 stories across an onsite. Use the rotation plan to enforce range.
- Don't generate a cheat-sheet without reading the role's `role.md`. The cheat-sheet's specificity comes from the fit analysis.
- Don't fabricate stories or metrics. If a star/ file lacks a metric, surface that, don't paper over it.
- **Never use em or en dashes (— –) in any output.** Use commas, periods, colons, or parentheses.
- Don't be vague in recommendations. "Use the Agentic Dev Team story" is weak. "Use [agentic-dev-team.md](../../career/star/agentic-dev-team.md) Angle 1 (technical depth)" is correct.
