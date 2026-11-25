---
name: simple-understanding-quiz
description: "Create short retrieval questions to identify knowledge gaps and check understanding of a topic."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["active-recall", "retrieval-practice", "diagnostic-quiz", "learning", "education", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Test Understanding with Interactive Diagnostic Quizzes (AI Skill)

## Overview
Reading a summary or textbook chapter creates a cognitive illusion called the **Illusion of Competence**: because the text makes sense while reading it, your brain assumes it has mastered the concept. Without active retrieval, over 70% of new information is forgotten within 48 hours.

The **Interactive Diagnostic Quiz Protocol** commands the AI to generate a **3-tier active recall test** (Direct Mechanism $\rightarrow$ Real-World Application $\rightarrow$ Tricky Misconception Trap) to measure and reinforce retention.

---

## The 3-Tier Diagnostic Quiz Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 The 3-Tier Diagnostic Quiz                  │
│                                                             │
│  [ QUESTION 1: Core Mechanism ] ──► Direct conceptual test  │
│                 │                                           │
│  [ QUESTION 2: Scenario Problem]──► Apply concept in context│
│                 │                                           │
│  [ QUESTION 3: The Trap / Edge] ──► Common misconception    │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Diagnostic Quiz Prompt Templates

### Pattern 1: The 3-Question Active Recall Drill
Use immediately after studying any technical, medical, or business topic:

```markdown
I just studied [TOPIC: e.g. Git Rebase vs. Merge / The Federal Reserve Interest Rate Mechanism].

Generate an interactive 3-question Multiple Choice Quiz to test my true comprehension:
1. **Question 1 (Core Mechanism)**: Test the fundamental rule.
2. **Question 2 (Applied Scenario)**: Give me a concrete real-world situation to resolve.
3. **Question 3 (The Misconception Trap)**: A tricky edge-case question targeting the most common beginner mistake.

Rules:
- Provide 4 options (A, B, C, D) per question.
- Do NOT reveal the answers yet.
- Tell me to reply with my choices (e.g. "A, C, B"), and you will grade my answers with detailed explanations.
```

---

### Pattern 2: The Flashcard Socratic Examiner
Use for one-by-one interactive quizzing:

```markdown
Act as my strict oral exam proctor for [SUBJECT].
- Ask me **one single question at a time**.
- Wait for my answer.
- If I am correct: give brief praise and ask the next harder question.
- If I am wrong: explain the flaw in my reasoning and give me a similar question to retry.
```

---

## Real-World Case Study

### Scenario: Testing Understanding of SQL Indexes

#### AI-Generated Diagnostic Quiz Output
> **Question 1 (Mechanism)**: When you create a B-Tree index on a column in PostgreSQL, what is the primary operational trade-off?
> - A) Read queries become slower, write queries become faster.
> - B) Read queries become faster, write operations incur higher CPU/disk overhead.
> - C) Storage space decreases because data is compressed.
> - D) Null values are automatically deleted from the table.
>
> **Question 2 (Scenario)**: You have a table with 10M rows and query `SELECT * FROM users WHERE status = 'active'` (where 95% of users are active). Will a standard B-Tree index on `status` improve query speed? Why or why not?
> - A) Yes, indexes always speed up queries regardless of data distribution.
> - B) No, because the query planner will perform a sequential table scan when selectivity is low ($>90\%$).
> - C) Yes, but only if you use a clustered index.
> - D) No, because PostgreSQL does not allow indexes on string columns.

**User Replies**: *"1: B, 2: B"*

**AI Evaluation**: *"100% correct! You correctly identified that indexes impose a write penalty, and that the query planner skips indexes when filtering on low-cardinality/high-density columns (low selectivity)."*

---

## Summary Best Practices
- **Never ask for questions with answers included**: If the answer is visible at the bottom of the message, your brain will skim it and skip active retrieval.
- **Answer without looking at notes**: The mental effort of struggling to retrieve a memory is what cements long-term neural retention.
