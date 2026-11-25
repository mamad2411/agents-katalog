---
name: course-project
description: "Use when someone asks to build a whole course to run later: syllabus, lessons, assignments and tests. A lesson now belongs to tutor or teach, a schedule to study-plan."
---

# Course project

Some goals need a full course package to run later: elementary map reading, high-school civics, university statistics, professional safety training, or a self-directed language course. Build a syllabus, lesson plan, assignments, tests, and teacher instructions at the learner's level. If the assistant has projects or custom instructions, store the files there. Otherwise deliver the files and a pasted instruction block the learner can reuse in any chat. Sequence prerequisites and check learning honestly.

Paths like `references/…`, `templates/…` and `examples/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../tutor/SKILL.md`) and are installed as their own skills too. If a file is missing from your copy, work from this file and the router's core rules.

## 0. When to offer it

- When the learner asks for a complete course package to run later: syllabus, lessons, assignments and tests.
- When the learner wants reusable teacher instructions and assessments across sessions.
- Offer it in one line; don't push. Some people prefer to keep learning in their usual chats, and `teach` works there too.

## 1. Learn the learner (briefly)

Use what they've told you and `references/first-session.md`: purpose (career, project, curiosity), the competence statement ("You'll be able to ___ without help"), prior knowledge (a short warm-up check), hours per week, deadline, what helps them learn, and tools they use. Don't gate the build on every answer.

## 2. Research the course like a curriculum committee

1. **Level-matched curricula.** Use at least three relevant public curricula, syllabi, course pages or practitioner guides when available. For a child, use age-appropriate learning objectives; for high school, course standards; for university or professional learning, published syllabi and field standards. Record author or institution, date, level and topic sequence. If sources are unavailable, use supplied materials, label the draft provisional and do not invent a benchmark.
2. **Discipline standards,** where one exists. Examples: ACM/IEEE-CS/AAAI *Computer Science Curricula 2023* (computing); IEEE Computer Society *SWEBOK* (software engineering); American Chemical Society Committee on Professional Training guidelines (chemistry); *Vision and Change* (undergraduate biology); ABET criteria (engineering programs); ACTFL Proficiency Guidelines (languages); the AAMC content outline (MCAT). Verify the current version before citing.
3. **Synthesize.** Common objectives form the core; others are options. Put prerequisites first and adjust examples to the learner's purpose, age and prior knowledge. Explain any deviation from the benchmarks.
4. **Primary resources:** one main text (open texts such as OpenStax or LibreTexts when they fit; check licenses), primary sources where the field values them, and one to three verified videos per unit at most (`find-media`).
5. **Be honest about the benchmark.** Name the sources and level used. The package does not grant academic credit or a professional credential.

If your platform can run research subagents, fan the syllabus search out and verify the results; otherwise search sequentially. Never invent a syllabus, course number or standard.

## 3. Write the course files

Produce four files the learner keeps (as files or documents they can download):

1. **Syllabus** (`course-syllabus.md`): title; who it's for; competence statement and course outcomes; benchmark sources with dates; units in order, each with objectives, readings, activities, assignment and assessment; schedule against their real hours; grading scale and weights; bonus policy (`assess` §5); the course's AI policy ("your teacher won't hand you answers to assigned work"; `assignment`).
2. **Lesson plan** (`lesson-plan.md`): for every unit, lesson by lesson: target, hook question, minimum teaching, the worked example, the visual to render (`references/visual-teaching.md`), practice items, the check, and the spaced review items from earlier units.
3. **Gradebook and progress** (`templates/gradebook.md`): starts empty except the plan.
4. **Project instructions** (`templates/course-project-prompt.md` filled in): the teacher.

Before delivering, check the files against each other: every syllabus objective appears in the lesson plan and is assessed at least once.

## 4. The project instructions

Fill in `templates/course-project-prompt.md`. It tells the assistant running the course to:
- Be the teacher of this course at the chosen level, with demanding but appropriate checks for this learner.
- Follow the lesson plan in order, one lesson per session unless the learner asks to move faster, and keep their place.
- Open each session with retrieval of what's due; teach with Myelinate's session loop; render visuals when concepts have shape; close with the learner's own recall.
- Set the assignments in the plan, coach them without giving answers, and grade them and the tests against written keys and rubrics.
- Keep the gradebook current: use file writing if they want it; otherwise end each session with an updated progress block the learner can save and paste next time.
- Use Myelinate if it's installed; otherwise follow the method in these instructions.

Keep the instructions specific and short enough to read in a few minutes; the syllabus and lesson plan carry the detail.

## 5. Set up the course anywhere

1. If the assistant supports projects, spaces or custom instructions, create one and add the filled teacher instructions, syllabus, lesson plan and gradebook. Check what that host actually remembers before relying on it.
2. If the host lacks those features, give the learner the four files or Markdown blocks. At the start of each new chat they paste the teacher instructions and current gradebook, then say "Begin the next lesson."
3. If the assistant can write files, save the gradebook with permission. Otherwise return a complete replacement block at each close. The learner keeps the source of truth.

Claude Projects are one possible host, not a requirement. If giving host-specific steps, verify the current interface first.

## 6. Running and revising the course

Each session in the chosen host runs as `teach` §5 describes. Every few units, review the gradebook with the learner and revise: speed up where they're strong, add practice where they're not, and update the files. When the course ends, give a final cumulative exam (`assess`), a capstone that meets the competence statement, and an honest summary of what they can now do.

## Anti-patterns

A syllabus from imagination instead of research · citing a standard you didn't check · a lesson plan that skips prerequisites · claiming credit or accreditation · instructions so long nobody reads them · no gradebook · files that disagree with each other.
