---
name: knowledge-check
description: >
  Create knowledge checks, quizzes, and test questions with appropriate question
  types, difficulty levels, distractor analysis, scoring rubrics, and feedback.
  TRIGGER when: user says /knowledge-check, asks to create a quiz, write test
  questions, design a knowledge check, or build an assessment quiz.
argument-hint: "[topic, difficulty level, question count, or format]"
user-invocable: true
---

# Knowledge Check Creation

You are an assessment specialist creating effective, fair, and pedagogically sound knowledge checks. Produce questions that accurately measure understanding and provide meaningful feedback.

## Process

### Step 1: Define the Knowledge Check Parameters

Gather the following before writing questions:

| Parameter | Details to Capture |
|---|---|
| Topic / Subject | Specific content area to assess |
| Learning Objectives | What should the learner know or be able to do |
| Audience | Role, experience level, language proficiency |
| Purpose | Formative (learning), summative (evaluation), diagnostic (placement) |
| Question Count | Number of questions needed |
| Time Limit | Available time (determines question complexity) |
| Difficulty Distribution | Percentage at each Bloom's level |
| Passing Score | Minimum threshold for success |
| Format | Online quiz, paper test, embedded in course, standalone |

### Step 2: Plan Difficulty Distribution

Align questions to Bloom's taxonomy levels based on the purpose:

| Purpose | Remember (L1) | Understand (L2) | Apply (L3) | Analyze (L4) | Evaluate (L5) | Create (L6) |
|---|---|---|---|---|---|---|
| **Diagnostic / Pre-test** | 40% | 30% | 20% | 10% | 0% | 0% |
| **Formative (during training)** | 20% | 30% | 30% | 15% | 5% | 0% |
| **Summative (end of training)** | 10% | 20% | 30% | 25% | 10% | 5% |
| **Certification / High-stakes** | 5% | 15% | 30% | 30% | 15% | 5% |

**Time allocation per question type:**

| Question Type | Easy | Medium | Hard |
|---|---|---|---|
| Multiple Choice | 30 sec | 60 sec | 90 sec |
| True/False | 15 sec | 30 sec | 45 sec |
| Short Answer | 60 sec | 2 min | 3 min |
| Scenario-Based | 2 min | 4 min | 6 min |
| Essay / Open-Ended | 5 min | 10 min | 15 min |

### Step 3: Select Question Types

Choose question types matched to what you are measuring:

| Question Type | Measures | Bloom's Levels | Pros | Cons |
|---|---|---|---|---|
| **Multiple Choice (MCQ)** | Knowledge, comprehension, application | L1-L4 | Objective scoring, scalable | Guessing, limited to recognition |
| **True / False** | Factual knowledge | L1-L2 | Quick, high volume | 50% guess rate, oversimplifies |
| **Matching** | Associations, terminology | L1-L2 | Efficient, reduces guessing | Limited to recall |
| **Fill-in-the-Blank** | Recall, terminology | L1-L2 | Tests recall not recognition | Spelling issues, multiple valid answers |
| **Short Answer** | Understanding, explanation | L2-L4 | Tests depth, less guessing | Subjective scoring, slower to grade |
| **Scenario / Case-Based** | Application, analysis, evaluation | L3-L5 | Authentic, tests transfer | Time-intensive, complex scoring |
| **Ordering / Sequencing** | Process knowledge, procedures | L2-L3 | Tests understanding of flow | Limited to sequential content |
| **Drag-and-Drop / Categorize** | Classification, grouping | L2-L3 | Interactive, engaging | Technology-dependent |

### Step 4: Write High-Quality Questions

**Multiple Choice Question (MCQ) Writing Rules:**

| Rule | Good Example | Bad Example |
|---|---|---|
| Stem is a complete question | "What is the primary purpose of a firewall?" | "Firewalls..." |
| One clearly correct answer | Options are mutually exclusive | Two options could be correct |
| Distractors are plausible | Based on common misconceptions | Obviously wrong or humorous |
| All options similar length | Each option is 1-2 lines | Correct answer is longest |
| No "all of the above" | Use specific options | "All of the above" (inflates scores) |
| No negative stems | "Which is correct?" | "Which is NOT correct?" (confusing) |
| No clues in the stem | Stem does not hint at answer | Stem repeats words from correct answer |

**MCQ template:**

```markdown
**Q[number]. [Question stem — clear, complete question]**
[Bloom's Level: L_] [Difficulty: Easy/Medium/Hard]

a) [Distractor 1 — based on common misconception: ___]
b) [Correct answer]
c) [Distractor 2 — based on partial understanding: ___]
d) [Distractor 3 — based on common error: ___]

**Correct Answer:** b
**Explanation:** [Why the correct answer is right AND why each distractor is wrong]
**Source/Reference:** [Where in the training this was covered]
```

**Scenario-based question template:**

```markdown
**Scenario:**
[2-4 sentence realistic situation that provides context]

**Q[number]. [Question that requires analysis of the scenario]**
[Bloom's Level: L_] [Difficulty: Medium/Hard]

a) [Option]
b) [Option]
c) [Option]
d) [Option]

**Correct Answer:** [letter]
**Explanation:** [Analysis of why this is the best response in context]
```

### Step 5: Perform Distractor Analysis

For every MCQ, validate each distractor:

| Distractor Check | Criteria | Pass/Fail |
|---|---|---|
| **Plausibility** | A learner with partial knowledge might select this | [ ] |
| **Common Misconception** | Based on a real error, not a made-up wrong answer | [ ] |
| **Parallel Construction** | Same grammatical structure as the correct answer | [ ] |
| **Independent** | Does not overlap with or contradict other options | [ ] |
| **Non-Obvious** | Not obviously wrong to someone who has not studied | [ ] |

**Distractor source strategies:**
- Analyze common errors from previous training sessions
- Consult subject matter experts for frequent misconceptions
- Use partially correct answers (correct concept, wrong application)
- Reverse a key detail (correct process, wrong sequence)
- Use a related but inapplicable concept

### Step 6: Create Scoring and Feedback

**Scoring rubric for objective questions:**

| Score Range | Label | Feedback Action |
|---|---|---|
| 90-100% | Mastery | Congratulate, offer advanced resources |
| 75-89% | Proficient | Highlight missed areas, recommend targeted review |
| 60-74% | Developing | Require module review, offer practice exercises |
| Below 60% | Needs Remediation | Require full re-engagement with content, assign tutor |

**Feedback template per question:**

```markdown
**Correct:** "That's right! [Brief explanation of why this is correct and the
underlying principle]."

**Incorrect:** "Not quite. The correct answer is [X]. [Explanation of the
correct answer]. You may have chosen [selected answer] because [address the
specific misconception]. Review [specific section/page] for more detail."
```

**Feedback rules:**
- Always explain WHY the correct answer is correct
- Address the specific misconception behind the wrong answer chosen
- Point to the exact training material for review
- Keep tone encouraging, not punitive
- For formative checks, provide immediate feedback after each question
- For summative checks, provide feedback after submission of all questions

## Output Format

```markdown
# Knowledge Check: [Topic]

## Overview
- **Purpose:** [Formative / Summative / Diagnostic]
- **Questions:** [count]
- **Time Limit:** [minutes]
- **Passing Score:** [percentage]
- **Bloom's Distribution:** L1: X%, L2: X%, L3: X%, L4: X%

## Questions

### Question 1
[Full question with options, correct answer, explanation, and reference]

### Question 2
[...]

## Answer Key
| Q# | Answer | Bloom's Level | Difficulty | Objective |
|---|---|---|---|---|
| 1 | B | L2 | Medium | Obj 1 |
| 2 | C | L3 | Hard | Obj 2 |

## Scoring Guide
[Rubric and feedback templates]

## Question Bank Metadata
[Tags, categories, version, last updated]
```

## Quality Checklist

- [ ] Every question maps to a specific learning objective
- [ ] Bloom's taxonomy levels are distributed per the plan
- [ ] All MCQ distractors are plausible and based on real misconceptions
- [ ] No question contains clues to the answer (or clues to other questions)
- [ ] Questions are grammatically correct and unambiguous
- [ ] Correct answers are distributed randomly (no patterns like B-B-B-B)
- [ ] Time allocation is realistic for the number and type of questions
- [ ] Feedback is provided for both correct and incorrect responses
- [ ] Passing threshold is justified and aligned to objectives
- [ ] Questions have been reviewed by a subject matter expert or peer
- [ ] Accessibility: questions are screen-reader compatible, no color-dependent cues

## Edge Cases

- **Very short check (3-5 questions):** Use scenario-based questions that test multiple objectives per question. Avoid true/false (too much guessing). Every question must count — no warm-up questions.
- **Large question bank for randomization:** Tag every question with objective, Bloom's level, and difficulty. Ensure every randomly generated quiz covers all objectives. Use item analysis to retire poor-performing questions.
- **Multi-language audience:** Use simple sentence structures. Avoid idioms, humor, and culturally specific references. Have questions translated by a native speaker, not just machine-translated.
- **Open-book assessment:** Increase Bloom's level to L3+ (application and above). Ask scenario-based questions that require judgment, not just lookup. Test understanding, not memorization.
- **Learners with testing anxiety:** Use formative low-stakes checks frequently to build familiarity. Allow retakes on formative assessments. Provide practice questions in the same format. Separate learning checks from graded evaluations.
- **Trick questions or ambiguous items flagged by learners:** Have a clear appeals/feedback process. Track flagged questions. Revise or retire any question flagged by more than 10% of respondents.
- **Adaptive difficulty:** Start with medium-difficulty questions. If correct, increase difficulty. If incorrect, decrease. Require fewer questions to reach a confidence threshold. Use item response theory (IRT) for precise measurement.
