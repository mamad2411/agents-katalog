---
name: code-author
description: Expert skill for writing high-quality code changes (CLs/PRs) following Google's Engineering Practices. Focuses on small changes, clear descriptions, and professional feedback handling.
version: 1.0.0
keywords: [google-eng-practices, code-author, cl-description, small-cls, software-engineering]
---

# code-author ✍️

> Keyword: author | Platforms: gemini,claude,codex

Expert AI Agent Skill for **Code Authoring** - Best practices for creating, describing, and refining code changes based on [Google's Engineering Practices](https://google.github.io/eng-practices/review/developer/).

## 🎯 Core Mandates (The Author's Rules)

- **Small CLs Only:** Keep changes focused on ONE thing. Small CLs are easier to review, faster to merge, and lower risk.
- **Clear Descriptions:** Always explain **WHAT** is changing and **WHY**. The "How" should be evident from the code, but the "Why" is critical context.
- **Risk Areas Identification:** Explicitly call out parts of the code where you are unsure or where there is a high risk of side effects.
- **No Refactor + Feature Mix:** Never mix refactoring with new features or bug fixes. These must be separate CLs.
- **Proactive Communication:** Address all reviewer comments, even if you disagree. Explain your reasoning clearly and professionally.
- **Self-Audit First:** Run the "Self-Audit Checklist" before sending a CL for review.

---

## 🛠 Authoring Workflows

### 1. Planning a Change (CL)
1. **Isolate the Task:** Can this be broken into smaller, independent steps?
2. **Draft the Description:** Start with a one-line summary. Add context on the problem being solved.
3. **Identify Risks:** Note any areas that need extra attention from the reviewer.

### 2. Writing the Code & Self-Audit
- **Tests First:** Ensure the change is covered by automated tests.
- **Style Consistency:** Follow [Google Java Style](https://google.github.io/styleguide/javaguide.html).
- **Self-Audit Checklist:**
    - [ ] **Diff Minimization:** Revert accidental changes (whitespace, commented-out code).
    - [ ] **Documentation Check:** Update README, JSDoc, or JavaDoc for new exports/logic.
    - [ ] **Test Alignment:** Ensure tests cover logic branches, not just the "happy path."
    - [ ] **Logic Validation:** Mentally trace the execution path for edge cases (null, empty, etc.).

### 3. Handling Reviewer Feedback
- **Be Grateful:** Reviewers are spending time to improve your code.
- **Don't Take it Personally:** The goal is to improve the code, not critique the author.
- **Resolve or Disagree:** Either apply the change or explain why the current approach is better. Never ignore a comment.

---

## 🔍 CL Description Template (Superpowers Edition)

```markdown
[Summary Line: Brief one-line description]

### 📝 Context & Intent
[Why is this change necessary? What problem does it solve?]

### 🛠 Key Changes
[Bullet points of the main code modifications]

### ⚠️ Risk Areas & Concerns
[Where should the reviewer focus? Any potential side effects or uncertainties?]

### ✅ Verification Results
[List tests run, coverage achieved, and manual verification steps]

[Related Issues: e.g., Fixes #123]
```

---

## 🌐 Knowledge Sources & Deep Dives

> **Directive:** Use `web_fetch` to find Google's specific guidance on "Small CLs" or "CL Descriptions" if a change feels too large or complex.

- **Developer's Guide:** [Google Eng Practices - Authoring](https://google.github.io/eng-practices/review/developer/) - The primary source.
- **Small CLs:** [Why Small CLs?](https://google.github.io/eng-practices/review/developer/small-cls.html) - Benefits and strategies.
- **CL Descriptions:** [How to write CL Descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) - Best practices.
- **Handling Feedback:** [Handling Reviewer Comments](https://google.github.io/eng-practices/review/developer/handling-comments.html) - Mindset and communication.

## Skill Interoperability

The **code-author** ✍️ skill ensures that work produced by other skills is packaged correctly:
- **java-expert** ☕ & **quarkus-expert** ⚡: Logic produced is split into reviewable CLs.
- **refactoring-expert** 🛠: Ensures refactors are isolated from feature changes.
