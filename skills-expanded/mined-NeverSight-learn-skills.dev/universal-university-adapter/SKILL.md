---
name: universal-university-adapter
description: >
  Universal entry point for ANY university worldwide. Detects the user's university from directory
  of PDFs, uploaded files, verbal descriptions, URLs, or implicit context. Identifies exam pattern
  (Indian, US, UK, European, Australian, Asian, or Generic) and routes to the correct universal
  skill. Works for ALL engineering/science/arts/commerce departments across every country.
---

# Universal University Adapter

## When to Use This Skill

Activate this skill when:

- User mentions **any university** (or doesn't specify one)
- User provides a **directory path** containing PYQ/syllabus PDFs
- User **uploads PDFs directly** in chat
- User **describes their university pattern** verbally (e.g., "I'm in a UK university with module
  exams")
- User **provides a link** to their university website/syllabus page
- User **just asks a question** without any university context ("Write an answer about OS paging")
- User asks "Will this work for my university?"

Under no circumstance should you refuse to help. Always attempt to infer or ask for the university
context.

---

## Part 1: University Detection & Pattern Recognition

### Scenario A — User Provides a Directory Path

**Step 1:** Accept the directory path and recursively list all PDF files.

```
Glob pattern: **/*.pdf
Search in:     <user-provided-path>
```

**Step 2:** Categorize files by name analysis:

- **Syllabus PDFs** — filenames containing: `syllabus`, `curriculum`, `scheme`, `pattern`,
  `academic`, `regulations`, `course-structure`, `program-guide`, `handbook`, `brochure`,
  `catalogue`
- **PYQ PDFs** — filenames containing: `question-paper`, `exam`, `pyq`, `previous-year`,
  `past-paper`, `question-bank`, `qp`, `end-sem`, `mid-sem`, `final`, `midterm`, `sample-paper`,
  `model-paper`, `test`
- **Merged collections** — filenames containing: `merged`, `all-in-one`, `aio`, `compilation`,
  `collection`, `all-years`

**Step 3:** Read a syllabus PDF (first 3 pages) and a sample PYQ PDF to identify **all** of the
following:

| Property                  | Detection Clues                                                                                                                                                                                                                                                                                                            |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Country/Region**        | Terms: `SPPU`, `VTU`, `JNTU`, `AICTE`, `NEP` → India; `GPA 4.0`, `credit hours`, `midterm`, `final` → US/Canada; `First Class`, `Upper Second`, `2:1`, `dissertation` → UK; `ECTS`, `ECTS-Credits`, `Modulprüfung` → Europe; `hurdle`, `7-point GPA` → Australia; `5-point GPA`, `CAP`, `modular credits` → Singapore/Asia |
| **University Name**       | Header/watermark/footer on PDF pages (e.g., "Savitribai Phule Pune University", "Visvesvaraya Technological University", "University of Cambridge", "MIT")                                                                                                                                                                 |
| **Exam Pattern**          | Mark distribution, OR structure, question types (MCQ, theory, numerical), duration                                                                                                                                                                                                                                         |
| **Department/Faculty**    | Department name from syllabus or question paper header                                                                                                                                                                                                                                                                     |
| **Academic Year/Pattern** | Year references like "2019 Pattern", "2024 Pattern", "2022-2023", "Regulations 2021"                                                                                                                                                                                                                                       |
| **Subject Names & Codes** | Subject code patterns (e.g., `210241`, `CS301`, `MATH101`)                                                                                                                                                                                                                                                                 |
| **Grading System**        | References to GPA scales, percentage ranges, letter grades                                                                                                                                                                                                                                                                 |

**Step 4:** If the path contains no PDFs:

> "No PDF files found in that directory. Please upload your syllabus and at least 2-3 previous year
> question papers directly in the chat, share a link to your university's academic page, or describe
> your exam pattern."

---

### Scenario B — User Uploads PDFs in Chat

**Step 1:** Read each uploaded PDF using the Read tool.

**Step 2:** For syllabus PDFs — extract:

- University name and country
- Department / program name
- Subject list with codes
- Scheme/regulation year
- Credit distribution
- Course Outcomes (COs)
- Exam pattern description (if present)

**Step 3:** For PYQ PDFs — extract:

- Question paper format (mark distribution, OR/alternative structure)
- Number of sections and their mark values
- Question types: define, explain, derive, solve, compare, justify, design
- Duration of exam
- Whether it's an In-Sem, End-Sem, Midterm, or Final

**Step 4:** If the uploaded files are insufficient:

> "I've read the files you uploaded. Could you also provide (1) a syllabus PDF showing all subjects,
> or (2) additional question papers for other units, or (3) describe your grading scheme?"

---

### Scenario C — User Describes Their University Verbally

Extract pattern from their description using these detection heuristics:

| User Says                                                                                                     | Pattern                   |
| ------------------------------------------------------------------------------------------------------------- | ------------------------- |
| "My university has **internal assessment + semester-end exams**", "**80:20** ratio", "**60:40**", "**70:30**" | Indian university pattern |
| "We have **midterms and finals**", "**credit hours**", "**GPA out of 4.0**"                                   | US/Canada pattern         |
| "We have **written papers** in May/June", "**First/2:1/2:2/Third** classification"                            | UK pattern                |
| "We use **ECTS credits**", "**Modulprüfung**", "**written and oral exams**"                                   | European pattern          |
| "We have **hurdle requirements**", "**7-point GPA**", "**assessment tasks**"                                  | Australian pattern        |
| "**Final exam is 50%**", "**5-point GPA**", "**modular system**"                                              | Singapore/Asia pattern    |
| "I just need **exam answers**", "**help with notes**" or vague request                                        | Generic — ask             |
| "**SPPU**", "**Pune University**", "**2019 pattern**", "**credit system**"                                    | SPPU (Indian)             |
| "**VTU**", "**Visvesvaraya**", "**CBCS**"                                                                     | VTU (Indian)              |
| "**JNTU**", "**Jawaharlal Nehru Technological**", "**R20**", "**R19**"                                        | JNTU (Indian)             |
| "**Mumbai University**", "**MU**", "**REV-2019**"                                                             | Mumbai (Indian)           |
| "**AKTU**", "**Abdul Kalam Technical**", "**UPTU**"                                                           | AKTU (Indian)             |
| "**RGPV**", "**Rajiv Gandhi Proudyogiki**"                                                                    | RGPV (Indian)             |
| "**PTU**", "**I.K. Gujral Punjab Technical**"                                                                 | PTU (Indian)              |
| "**CSVTU**", "**Chhattisgarh Swami Vivekanand**"                                                              | CSVTU (Indian)            |
| "**DBATU**", "**Dr. Babasaheb Ambedkar Technological**"                                                       | DBATU (Indian)            |
| "**Shivaji University**", "**Kolhapur**"                                                                      | Shivaji (Indian)          |
| "**University of Madras**", "**Madras University**"                                                           | Madras (Indian)           |
| "**Delhi University**", "**DU**", "**CBCS Delhi**"                                                            | Delhi University          |
| "**IIT**", "**Indian Institute of Technology**"                                                               | IITs (Indian)             |
| "**NIT**", "**National Institute of Technology**"                                                             | NITs (Indian)             |
| "**IIIT**", "**Indian Institute of Information Technology**"                                                  | IIITs (Indian)            |
| "**University of Cambridge**", "**Oxford**", "**Imperial**", "**UCL**"                                        | UK pattern                |
| "**Harvard**", "**MIT**", "**Stanford**", "**UC Berkeley**", "**state university**" (US)                      | US/Canada pattern         |
| "**TU Munich**", "**ETH Zurich**", "**TU Delft**", "**Politecnico**"                                          | European pattern          |
| "**University of Melbourne**", "**UNSW**", "**Sydney**", "**ANU**"                                            | Australian pattern        |
| "**NUS**", "**NTU**", "**National University of Singapore**"                                                  | Singapore/Asia pattern    |

**Step 1:** Match user's description against the above table.

**Step 2:** If match found — confirm with user and proceed to routing.

**Step 3:** If no clear match — ask clarifying questions:

> "Could you tell me a bit more about your university exam pattern? For example:
>
> - Which country is your university in?
> - What grading system do you use (percentage, GPA 4.0, ECTS, letter grades)?
> - How are exams structured — midterms and finals, or end-semester exams?
> - What subjects are you currently studying?"

---

### Scenario D — User Just Asks a Question Without Specifying University

When user asks something like: "Write an answer about virtual memory", "Explain DBMS architecture",
"Solve this DAA problem", "Generate notes on OS", "What are important topics in CN?"

**Step 1:** Check if a university context was already established earlier in this conversation. If
yes, reuse it.

**Step 2:** If no prior context, ask (but be brief):

> "Which university are you studying under? I'll tailor the answer to your specific exam pattern and
> marking scheme."

**Step 3:** If user responds with a university name, run detection from Scenario C.

**Step 4:** If user doesn't know or says "any" — use a **neutral international format**:

- 10-mark questions: Full answer with introduction, detailed explanation, conclusion
- 5-mark questions: Concise but complete explanation
- 2-mark questions: Precise definition or short note
- Use standard international academic English
- Avoid country-specific jargon unless obvious from context

---

### Scenario E — User Provides a Link to University Website/Syllabus

**Step 1:** Use the WebFetch tool to fetch content from the link.

**Step 2:** Analyze the fetched HTML/markdown for:

- University name and country location
- Department/faculty names
- Course codes and subject titles
- Exam/assessment regulations
- Grading schemes
- Syllabus structure (semester, trimester, module)

**Step 3:** If the page has downloadable PDF links (syllabus PDFs), fetch those too and read them.

**Step 4:** If the link is a general homepage (not specific academic content), ask:

> "I've identified your university. Could you share a more specific link to your department's
> curriculum page or syllabus document?"

**Step 5:** Proceed to pattern detection using the data gathered.

---

## Part 2: University Pattern Database

### Indian Universities (SPPU, VTU, JNTU, Mumbai, AKTU, RGPV, PTU, CSVTU, DBATU, Shivaji, Madras, Delhi, IITs, NITs, IIITs)

| Feature                | Details                                                               |
| ---------------------- | --------------------------------------------------------------------- |
| **Structure**          | Semester system (odd/even), typically 8 semesters for engineering     |
| **Assessment**         | 80:20 or 60:40 split (End Sem : Internal/In-Sem)                      |
| **Grading**            | SGPA/CGPA out of 10, or percentage                                    |
| **Question Paper**     | OR structure (choose A OR B), sections with marks (2, 4, 6, 8, 10)    |
| **Command Words**      | Define, Explain, Derive, Compare, Justify, Discuss, Design, Solve     |
| **Bloom's Taxonomy**   | Often mapped — Remember, Understand, Apply, Analyze, Evaluate, Create |
| **Pattern Years**      | 2019 Pattern, 2024 Pattern, CBCS, NEP 2020                            |
| **Answer Expectation** | Structured answers with diagrams, headings, numerical steps, keywords |

**Handling:** Route to universal skill with marks-per-unit-time mapping (2 marks ≈ 2 minutes, 10
marks ≈ 10 minutes).

---

### US/Canada Universities

| Feature                | Details                                                                          |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Structure**          | Semester or quarter system, credit hours                                         |
| **Assessment**         | Midterm (20-35%) + Final (30-50%) + Assignments/Quizzes/Projects (15-30%)        |
| **Grading**            | GPA out of 4.0 (A=4.0, A-=3.7, B+=3.3, B=3.0, etc.)                              |
| **Question Paper**     | Mixed MCQ + short answer + long answer, multiple sections                        |
| **Command Words**      | Describe, Compare, Analyze, Explain, Outline, Summarize, Evaluate                |
| **Answer Expectation** | Clear thesis statement, evidence-based reasoning, APA/MLA citation style, essays |

**Handling:** Route to universal skill with focus on essay-style answers, citations, and
rubric-based grading.

---

### UK Universities

| Feature                | Details                                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Structure**          | Academic year divided into terms/trimesters, module-based                                                                   |
| **Assessment**         | Written papers (May/June), coursework essays, dissertations, practicals                                                     |
| **Grading**            | Class-based classification: First (70+%), Upper Second/2:1 (60-69%), Lower Second/2:2 (50-59%), Third (40-49%), Fail (<40%) |
| **Question Paper**     | Essay questions, problem sheets, seen/unseen questions                                                                      |
| **Command Words**      | Critically evaluate, Discuss, Assess, To what extent, Examine, Outline                                                      |
| **Answer Expectation** | Critical analysis, argument development, references to literature, balanced evaluation                                      |

**Handling:** Route to universal skill with emphasis on critical thinking, essay structure, and
referencing.

---

### European Universities (ECTS System)

| Feature                | Details                                                                                                                                       |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Structure**          | Semester or trimester, module system with ECTS credits                                                                                        |
| **Assessment**         | Module exams (written + oral), seminar papers, lab reports, projects                                                                          |
| **Grading**            | ECTS scale A-F (A=Excellent, B=Very Good, C=Good, D=Satisfactory, E=Sufficient, FX/F=Fail) or national variants (German 1.0-5.0, French 0-20) |
| **Question Paper**     | Mixed: problem-solving, theory, oral examination component                                                                                    |
| **Command Words**      | Erläutern, Beschreiben, Vergleichen (DE); Expliquer, Décrire, Comparer (FR)                                                                   |
| **Answer Expectation** | Thorough, systematic, methodical; oral defense common in some countries                                                                       |

**Handling:** Route to universal skill with awareness of ECTS credit loading and oral exam
preparation.

---

### Australian Universities

| Feature                | Details                                                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Structure**          | Semester system (Feb-Jun, Jul-Nov), trimester for some programs                                                            |
| **Assessment**         | Hurdle requirements (must pass final exam regardless of other marks), assessment tasks (assignments, quizzes, labs, exams) |
| **Grading**            | 7-point GPA scale (7=High Distinction, 6=Distinction, 5=Credit, 4=Pass, 1-3=Fail)                                          |
| **Question Paper**     | Mixed: short answer, problem-solving, essays, practical exams                                                              |
| **Command Words**      | Critically analyse, Evaluate, Discuss, Demonstrate, Apply                                                                  |
| **Answer Expectation** | Rubric-based assessment, criterion-referenced grading, detailed feedback                                                   |

**Handling:** Route to universal skill with focus on meeting assessment criteria and hurdle
requirements.

---

### Asia (Singapore, HK, Japan, India)

| Feature                | Details                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------ |
| **Structure**          | Semester system, modular credits                                                                       |
| **Assessment**         | Final exam weight 40-60%, continuous assessment (assignments, projects, midterms, class participation) |
| **Grading**            | 5-point GPA (A+/A=5.0, A-=4.5, B+=4.0, etc.) or local variants                                         |
| **Question Paper**     | MCQ + structured questions, problem-based, case studies                                                |
| **Answer Expectation** | Precise, structured, formulaic where applicable, clear steps in derivations                            |

**Handling:** Route to universal skill with emphasis on structured responses and formula/derivation
clarity.

---

### Generic / Other Regions

| Feature                | Handling                                            |
| ---------------------- | --------------------------------------------------- |
| **No clear pattern**   | Ask clarifying questions to build a custom pattern  |
| **Mixed system**       | Identify dominant pattern and adapt                 |
| **Vocational/Diploma** | Assess separately — may have different exam formats |
| **Online/Distance**    | Usually assignment-based with proctored exams       |

**Step 1:** Build a custom pattern profile by asking:

> "I'd like to tailor this to your university. Could you clarify:
>
> 1. How are your exams structured? (e.g., one final exam, multiple tests, continuous assessment)
> 2. What grading scale do you use? (e.g., A-F, 0-100, GPA out of 4/5/7/10)
> 3. How are questions typically worded? (e.g., 'Explain', 'Compare', 'Critically evaluate')
> 4. What mark values do questions carry? (e.g., 2/5/10 marks or essay percentages)"

**Step 2:** Create a temporary pattern profile and use it to parameterize the universal skill.

---

## Part 3: Routing to Universal Skills

Once the university is identified and the pattern is determined, route the user's request to the
appropriate universal skill:

### For Answer Writing (Answer Questions, Solve Papers)

```
Route to → universal-a-plus-answer-writer
Map:    marks → depth, command words → response structure
Adapt:  pattern-specific (indian OR structure, US essay style, UK critical analysis, etc.)
```

### For Notes Generation (Create Study Notes)

```
Route to → universal-notes-generator
Map:    units → sections, topics → bullet points
Adapt:  exam pattern to determine depth per topic
```

### For PYQ Analysis (Analyze Previous Year Papers)

```
Route to → universal-pyq-analyzer
Map:    all PYQs → topic frequency → probability
Adapt:  question patterns specific to the detected university
```

### For IMP Topics (Important Topics Prediction)

```
Route to → universal-imp-topics-generator
Map:    PYQ trends + syllabus → priority categories (Must-Prepare / Selective / Safe-to-Skim)
Adapt:  university-specific repetition patterns and weightage
```

### For Assignment Writing (Generate Assignment Solutions)

```
Route to → universal-assignment-writer
Map:    questions → answer depth → 5-7 mark equivalent
Adapt:  university's assignment submission guidelines if known
```

### For Exam Paper Generation (Create Practice Papers)

```
Route to → universal-exam-paper-generator
Map:    university pattern → full question paper with proper structure
Adapt:  OR structure, CO mapping, Bloom's distribution, marks allocation
```

### Routing Decision Matrix

| User Request              | Detect Pattern?      | Route To                       |
| ------------------------- | -------------------- | ------------------------------ |
| "Write an answer about X" | Yes (univ known)     | universal-a-plus-answer-writer |
| "Write an answer about X" | No (univ unknown)    | Ask → then route               |
| "Generate notes on X"     | Yes                  | universal-notes-generator      |
| "Analyze these PYQs"      | Yes (PDFs provided)  | universal-pyq-analyzer         |
| "What are imp topics?"    | Yes (PYQs available) | universal-imp-topics-generator |
| "Solve this assignment"   | Yes                  | universal-assignment-writer    |
| "Make a practice paper"   | Yes (pattern known)  | universal-exam-paper-generator |
| "I have a folder of PDFs" | Detect from PDFs     | Route by what user wants       |
| "Help me study"           | Ask questions        | Determine → route              |

---

## Part 4: Complete Step-by-Step Workflow

### Workflow for Directory Path Scenario

1. **Receive path** from user (e.g., `/home/user/my-university-files`)
2. **Scan recursively** with Glob `**/*.pdf` on that path
3. **Classify PDFs** — syllabus vs PYQ vs merged
4. **Read syllabus PDF** first 5 pages → extract university, department, pattern, subjects, COs
5. **Read 1-2 PYQ PDFs** → extract exam format, mark distribution, question types
6. **Run university detection** using Part 1 detection tables
7. **Determine exam pattern** using Part 2 pattern database
8. **Present findings to user** briefly:
   > "I identified your university as **[Name]**, department **[Dept]**, following a
   > \*\*[Pattern > >
   >
   > > Type]** pattern with **[Assessment Split]\*\* assessment. Subjects found: [Subject 1],
   > > [Subject >
   >
   > > 2]..."
9. **Ask user what they need**: answer writing, notes, PYQ analysis, IMP topics, assignment, or
   practice paper
10. **Route to correct universal skill** using Part 3 routing matrix
11. **Pass context** to the skill: university name, pattern, subjects, COs, marks distribution

### Workflow for Uploaded PDFs Scenario

1. **Acknowledge receipt** of the uploaded files
2. **Read each PDF** sequentially
3. **Classify** as syllabus or PYQ or other
4. **Extract pattern information** (same as directory workflow steps 4-7)
5. **Proceed** to presentation and routing (steps 8-11 above)

### Workflow for Verbal Description Scenario

1. **Listen** to user's description of their university pattern
2. **Match** against detection heuristics in Part 1 Scenario C
3. **If confident** (≥ 80% match): proceed to routing
4. **If uncertain**: ask 1-2 targeted clarifying questions
5. **Once identified**: proceed to routing with the identified pattern

### Workflow for No-Context Question Scenario

1. **Detect** that no university context exists
2. **Ask briefly**: "Which university are you studying under?"
3. **Receive answer** → run detection → proceed to routing
4. **If user says "any" or "doesn't matter"** → use neutral international format with **standard
   academic structure**:
   - Full paragraph introductions and conclusions
   - Section headings for longer answers
   - Diagrams where applicable
   - Clear, formal academic English

### Workflow for URL/Link Scenario

1. **Fetch the URL** content using WebFetch tool
2. **Parse** for university identification signals
3. **If syllabus page found** → fetch any linked PDFs
4. **If homepage only** → ask for more specific URL
5. **Extract pattern** → proceed to routing

### Workflow for No PDFs Found at All

1. Inform user no usable documents were found
2. Offer alternatives:
   > "I need some information to tailor this for your university. Please choose:
   >
   > 1. Upload at least 2-3 question papers or a syllabus PDF
   > 2. Share a link to your university's academic curriculum page
   > 3. Describe your exam pattern (e.g., '80:20 semester system, 10-point GPA')
   > 4. Just tell me your university name and I'll use standard defaults"

---

## Part 5: Edge Cases & Troubleshooting

| Edge Case                                        | Handling                                                                                                                                                                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **User says multiple universities**              | Ask which one they need help with right now                                                                                                                                                                   |
| **PDFs are scanned images (no text)**            | Inform user: "These PDFs appear to be scanned images. If you have text-based PDFs, please upload those instead, or I can work with a verbal description of your syllabus."                                    |
| **User doesn't know their exam pattern**         | Ask for university name only → use standard default pattern for that university                                                                                                                               |
| **User needs help with non-engineering subject** | Still works — the universal skills are subject-agnostic. Route normally.                                                                                                                                      |
| **Conflicting signals from PDFs**                | Trust the syllabus PDF over PYQ PDF. If no syllabus, trust the most recent PYQ.                                                                                                                               |
| **Language not English**                         | Use the language of the PDFs. If PDFs are in a language you can't process, ask user for English translations or descriptions.                                                                                 |
| **User provides zero information**               | Use neutral international format. Default to standard semester system with 10-mark questions getting full essay treatment, 5-mark questions getting concise paragraphs, 2-mark questions getting definitions. |
| **Department has special exam rules**            | Accept any special rules the user mentions and incorporate into the pattern profile                                                                                                                           |
| **User asks for a skill that doesn't exist yet** | Do your best with the universal template: analyze what they need, produce the best possible output, and note that the skill is not yet loaded but you're working generically                                  |

---

## Part 6: Context Passing to Universal Skills

When routing to a universal skill, always pass the following context in your request:

```json
{
  "university": {
    "name": "Detected University Name",
    "country": "Country",
    "pattern_type": "Indian / US / UK / European / Australian / Asian / Generic",
    "grading_scale": "4.0 GPA / 10-point CGPA / ECTS / First-2:1-2:2 / 7-point GPA / 5-point GPA / Percentage",
    "assessment_split": "e.g., 80:20, 60:40, 50:50 midterm:final, etc.",
    "pattern_year": "2019 / 2024 / CBCS / NEP / Regulations 2021 / etc.",
    "command_words": ["Define", "Explain", "Compare", "Discuss", "Critically evaluate"],
    "bloom_levels": true/false,
    "or_structure": true/false,
    "max_marks": 10 or 20 or 100,
    "duration_minutes": 180
  },
  "subjects": [
    {
      "name": "Subject Name",
      "code": "SUB101",
      "semester": 3,
      "department": "Department Name",
      "course_outcomes": ["CO1: ...", "CO2: ..."]
    }
  ],
  "user_request": "What they want: answer / notes / analysis / topics / assignment / paper",
  "source": "directory / uploaded_files / verbal / URL / no_context"
}
```

This ensures the receiving universal skill has full context to produce perfectly tailored output.

---

## Important Notes

- This adapter is a **router** — it detects, identifies, and passes context. The actual content
  generation is done by universal skills.
- Universal skills (named with `universal-*` prefix) are designed to accept any university pattern
  and adapt their output dynamically.
- If a universal skill doesn't exist in the skills directory yet, the adapter should still do its
  best with the available tools and generic prompt engineering.
- The adapter itself does NOT need to know any subject content — it only needs to identify the
  university and route correctly.
- For **Computer Engineering at SPPU**, the pre-configured skills (`sppu-answer-writer`, etc.) will
  still work as they are a special case of the universal system with pre-loaded syllabus data.
- The adapter should always **confirm with the user** before routing: "I'll use the [University
  Name] [Pattern Type] pattern. Is that correct?"

---

## Session Config

This skill integrates with the session config system (`deps/session-profile.json`). Before
executing, check for an existing session profile:

- If `deps/session-profile.json` exists, read `university`, `subject`, `pattern`, and `exam_type`
  fields to auto-configure the skill.
- If the file does not exist, fall back to user-provided context or prompt the user to run
  `setup-exam-prompt` (or `npm run init`) first.
- Session config eliminates redundant context detection — detection happens once and is reused
  across all skill calls.

---

## Part 7: Fallback Handler — University Detection Failed

When all detection scenarios fail (no PDFs match, verbal description is ambiguous, URL is wrong),
use this three-tier fallback:

### Tier 1 — Ask Targeted Questions

```
1. "Which country is your university in?"
2. "What grading system do you use? (percentage, 4.0 GPA, 10-point CGPA, ECTS, letter grades)"
3. "How are exams structured? (semester-end, midterms+finals, module exams, continuous assessment)"
4. "What is your department and semester/year of study?"
```

### Tier 2 — Use Default Pattern

If the user cannot answer after 3 questions, fall back to:

| Clue                     | Default Pattern Used                     |
| ------------------------ | ---------------------------------------- |
| Country = India          | SPPU 2019 Pattern (generic)              |
| Country = US/Canada      | US semester with midterm+final (4.0 GPA) |
| Country = UK             | UK module exams (First/2:1/2:2)          |
| Country = Europe         | ECTS module system                       |
| Country = Australia      | Australian semester (7-point GPA)        |
| Country = Singapore/Asia | 5-point GPA modular system               |
| No country known         | Generic international format             |

### Tier 3 — Manual Profile

Prompt the user to create a manual profile:

```
I'll use a generic university profile. You can refine it anytime:
- University name: [any]
- Pattern: Generic
- Marks distribution: 2/5/10 mark questions
- Grading: percentage

Would you like to customize any of these now?
```

## Part 8: Conflict-Resolution Flowchart

When multiple sources provide conflicting information (e.g., syllabus says 80:20 split, URL says
70:30, user says 60:40), apply this priority resolution:

```
                    ┌──────────────────────────────────────┐
                    │  CONFLICT DETECTED                   │
                    │  Multiple sources disagree on        │
                    │  exam pattern / grading / structure   │
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │  Priority 1: Syllabus PDF            │
                    │  (Most authoritative source)         │
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │  If no syllabus PDF:                 │
                    │  Priority 2: Official URL / Website  │
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │  If no URL:                          │
                    │  Priority 3: Uploaded PYQ PDFs       │
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │  If no PDFs at all:                  │
                    │  Priority 4: User's verbal           │
                    │  description                         │
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │  Still conflicting?                  │
                    │  Present all options and ask:        │
                    │  "Which should I use?"               │
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │  RESOLUTION APPLIED                   │
                    │  Log which source won and why        │
                    │  Flag to user: "Using X over Y due   │
                    │  to priority rule"                   │
                    └──────────────────────────────────────┘
```

### Conflict Examples

| Conflict                                              | Resolution                                                    |
| ----------------------------------------------------- | ------------------------------------------------------------- |
| Syllabus says 80:20, PYQ shows 70:30                  | Follow syllabus (Priority 1) — PYQ may be from old pattern    |
| URL says 4.0 GPA, user says 10-point CGPA             | Ask user to confirm; URL data may be outdated                 |
| Verbal says "module exams", PDF shows semester system | Trust PDF (physical document) over recall                     |
| Two different pattern years in PDFs                   | Use the most recent pattern year                              |
| Language mismatch (PDF in Hindi, URL in English)      | Extract from both; pattern data from English source preferred |

## Part 9: Language Detection & Decision Rules for Non-English PDFs

When PDFs are detected to be in a language other than English, apply these rules:

### Detection Signals

| Signal                               | Likely Language            |
| ------------------------------------ | -------------------------- |
| Hindi/Sanskrit terms in header       | Hindi / Marathi / Sanskrit |
| Arabic script watermark              | Urdu / Arabic              |
| Chinese/Kanji characters             | Chinese / Japanese         |
| European accent characters (é, ñ, ü) | Spanish / French / German  |
| Cyrillic characters                  | Russian / Ukrainian        |
| French terms (Université, Faculté)   | French                     |
| German terms (Universität, Prüfung)  | German                     |

### Decision Rules

1. **If PDF language ≠ English AND you can process it**: Extract in original language, then note
   language for downstream routing
2. **If PDF language ≠ English AND you cannot process it**: Inform user and request English
   translation or description
3. **If mixed-language PDF** (e.g., English subject names but Hindi explanations): Use language
   detection per-page; extract what you can; flag untranslated sections
4. **If Latin-script European language** (French, German, Spanish, Portuguese, Italian): Process
   normally — most exam pattern structures are recognizable
5. **If non-Latin script** (Arabic, Devanagari, CJK, Cyrillic): Use OCR with the correct language
   pack (`tesseract -l lang_code`); inform user that numerical patterns (marks, dates) will be
   extracted but text content needs human verification
6. **If PDF uses multiple scripts**: Treat per-page; use `tesseract -l eng+lang_code` for mixed
   documents

### Language-Aware Routing

| Detected Language             | Routing Behavior                                         |
| ----------------------------- | -------------------------------------------------------- |
| English                       | Normal routing to universal skills                       |
| Hindi / Indian lang           | Route with `lang: hi` context; answers expected in Hindi |
| French / German               | Route with European exam pattern; expect local grading   |
| Arabic                        | Route with Islamic/Gulf exam pattern if recognized       |
| CJK (Chinese/Japanese/Korean) | Route with Asian exam pattern                            |
| Other                         | Best-effort extraction; flag to user for validation      |

## Error Handling

| Error                                      | Cause                                        | Solution                                                                 |
| ------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------------------ |
| No PDFs found in directory                 | Empty or wrong path                          | Prompt user to verify path or upload PDFs directly                       |
| University detection failed                | No clear signals in any source               | Launch Fallback Handler (Part 7)                                         |
| Conflicting signals across sources         | Syllabus vs URL vs user description mismatch | Apply Conflict-Resolution Flowchart (Part 8)                             |
| Language not supported                     | Non-English PDF with unknown script          | Request English translation or description                               |
| PDF is image-only (no text layer)          | Scanned document without OCR                 | Fall back to OCR pipeline; if OCR fails, request text PDF                |
| URL fetch fails                            | Link broken, requires auth, or blocked       | Ask user to upload content directly or describe verbally                 |
| Pattern database does not cover university | Unknown or very new university               | Use Generic/Other profile and build custom pattern                       |
| No user input after multiple prompts       | User unresponsive                            | Use neutral international format and proceed                             |
| Zero-information scenario                  | User provides no context at all              | Use Generic pattern: 10-mark standard, 5-mark concise, 2-mark definition |

## Quality Gate

Before routing to any downstream skill, verify:

- [ ] University name and country are identified (or fallback is in use)
- [ ] Exam pattern type is determined (Indian/US/UK/European/Australian/Asian/Generic)
- [ ] Grading scale is known (10-point CGPA, 4.0 GPA, ECTS, percentage, etc.)
- [ ] Assessment split is resolved (80:20, 60:40, midterm+final, etc.)
- [ ] At least one subject is identified with name and code
- [ ] Language of source PDFs is detected and compatible
- [ ] Conflict resolution has been applied if multiple sources disagree
- [ ] Source type is logged (directory / uploaded / verbal / URL / fallback)
- [ ] Context JSON (Part 6) is populated with all detected fields before passing to downstream skill
- [ ] User has confirmed the detected university and pattern (unless ≥95% confidence)

If any check fails, resolve before routing. Never route incomplete context — incomplete context
produces incorrect answers.
