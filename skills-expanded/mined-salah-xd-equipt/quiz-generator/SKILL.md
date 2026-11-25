---
name: quiz-generator
description: "Generates quizzes and assessments with multiple choice, true/false, and short answer questions with answer keys."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Quiz Generator

## When to Use This Skill

Use this skill when you need to:
- Generate quizzes for courses, training programs, or certifications
- Create multiple question types — multiple choice, true/false, short answer
- Build answer keys with explanations for correct and incorrect responses
- Design assessments that test different cognitive levels

**DO NOT** use this skill for personality quizzes, lead-generation quizzes, or survey design. This is for knowledge assessment quizzes that verify learning.

---

## Core Principle

A GOOD QUIZ DOES NOT JUST TEST MEMORY — IT TESTS WHETHER THE LEARNER CAN APPLY WHAT THEY LEARNED. QUESTIONS SHOULD REQUIRE THINKING, NOT JUST RECALL.

---

## Phase 1: Quiz Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Subject** | "What topic does this quiz cover?" | No default — must be provided |
| **Source material** | "What content should questions be based on — a lesson, manual, module?" | No default — must be provided |
| **Number of questions** | "How many questions?" | 10 questions |
| **Question types** | "Multiple choice, true/false, short answer, or mix?" | Mix of all three |
| **Difficulty level** | "Beginner, intermediate, or advanced?" | Intermediate |
| **Passing score** | "What score is required to pass?" | 70% |

**GATE: Confirm subject and source material before generating questions.**

---

## Phase 2: Question Design

### Question Type Guidelines

**Multiple Choice (4 options):**
- One clearly correct answer
- Three plausible distractors (wrong answers that make sense)
- Avoid "all of the above" and "none of the above" — they weaken assessment
- Avoid negatives in the stem ("Which is NOT...") — rephrase positively when possible
- All options should be similar in length and structure

**True/False:**
- Statement must be unambiguously true or false — no "it depends" answers
- Avoid double negatives
- Test one concept per statement
- Balance approximately 50/50 true and false

**Short Answer:**
- Question should have a specific, defensible answer (not open to interpretation)
- Provide the expected answer length ("In 1-2 sentences...")
- Include grading criteria in the answer key

### Cognitive Level Distribution

| Level | % of Quiz | Question Style |
|-------|-----------|---------------|
| Remember/Recall | 20-30% | Definitions, facts, terminology |
| Understand | 20-30% | Explain concepts, compare ideas |
| Apply | 30-40% | Scenarios, problem-solving, "what would you do" |
| Analyze/Evaluate | 10-20% | Case studies, best approach, justify a decision |

---

## Phase 3: Quiz Template

### Quiz Format

```
## [Quiz Title]

**Subject:** [Topic]
**Questions:** [X]
**Time limit:** [X] minutes (optional)
**Passing score:** [X]%

---

### Question 1 (Multiple Choice)

What is the primary purpose of [concept]?

a) [Distractor — plausible but incorrect]
b) [Correct answer]
c) [Distractor — common misconception]
d) [Distractor — related but wrong]

---

### Question 2 (True/False)

[Statement about the topic.]

True / False

---

### Question 3 (Short Answer)

In 1-2 sentences, explain [concept or process].

---

### Question 4 (Scenario-Based Multiple Choice)

A client tells you [scenario]. Based on best practices, what should you do first?

a) [Option A]
b) [Option B]
c) [Option C]
d) [Option D]

---

[Continue for all questions...]
```

### Answer Key Format

```
## Answer Key — [Quiz Title]

### Question 1: **B**
[Explanation of why B is correct and why the other options are wrong.
This is the teaching moment — answer keys should educate, not just confirm.]

### Question 2: **False**
[Explanation: The statement is false because... The correct information is...]

### Question 3: **Sample Answer**
"[Model answer that would receive full credit.]"

**Grading criteria:**
- Must mention [key concept 1] (1 point)
- Must mention [key concept 2] (1 point)
- Accurate and clear explanation (1 point)

### Question 4: **C**
[Explanation with reasoning for why C is the best approach in this scenario.]
```

---

## Phase 4: Quiz Delivery & Analysis

### Delivery Options

| Format | Best For | Tools |
|--------|----------|-------|
| Paper / PDF | In-person training, printed handouts | Word, Google Docs |
| Online form | Self-paced learning, auto-scoring | Google Forms, Typeform |
| LMS integration | Courses with tracking and certification | Teachable, Thinkific, Kajabi |
| Live verbal | Workshops, quick pulse checks | No tools needed |

### Quiz Analysis

After administering, review:

| Metric | What It Tells You |
|--------|------------------|
| Overall pass rate | Is the quiz appropriately difficult? |
| Average score | Are learners grasping the material? |
| Question-level analysis | Which questions had the lowest correct rate? |
| Distractor analysis | Are wrong answers attracting responses evenly? |
| Time to complete | Is the quiz too long or too short? |

### Quiz Checklist

- [ ] Questions align with stated learning objectives
- [ ] Mix of question types and cognitive levels included
- [ ] Multiple choice distractors are plausible (not obviously wrong)
- [ ] No trick questions or ambiguous wording
- [ ] Answer key includes explanations, not just correct answers
- [ ] Passing score is appropriate for the difficulty level
- [ ] Quiz has been tested by someone who knows the material (to catch errors)
- [ ] Quiz has been tested by someone who does NOT know the material (to check clarity)

---

## Anti-Patterns

- **Trick questions** — questions designed to confuse rather than assess learning are unfair and uninformative.
- **Testing trivia instead of understanding** — "What year was X invented?" tests memory, not competence.
- **All recall questions** — if every question is "define this term," the quiz does not test real-world application.
- **Obvious wrong answers** — if three of four options are absurd, the quiz is not assessing anything.
- **No answer explanations** — a quiz without explanations in the answer key wastes a learning opportunity.
- **Too many questions** — quiz fatigue reduces accuracy after 15-20 questions. Keep it focused.

---

## Recovery

- **High failure rate:** Review the questions — are they too hard, ambiguous, or testing content not covered in the source material?
- **Everyone gets a perfect score:** The quiz is too easy. Add application and analysis questions that require deeper thinking.
- **One question has a very low correct rate:** Either the content was not taught well or the question is poorly written. Investigate both possibilities.
- **Learners complain about unfairness:** Review with fresh eyes. Remove any questions that could be interpreted multiple ways.
- **Need more questions for a question bank:** Write 3x the questions you need and rotate them across quiz versions to prevent answer sharing.
