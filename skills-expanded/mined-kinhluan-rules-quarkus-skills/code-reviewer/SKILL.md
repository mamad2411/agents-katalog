---
name: code-reviewer
description: Expert skill for conducting high-quality code reviews following Google's Engineering Practices. Focuses on speed, standards, and mentorship.
version: 1.0.0
keywords: [google-eng-practices, code-reviewer, lgtm, mentoring, software-engineering]
---

# code-reviewer 🔍

> Keyword: reviewer | Platforms: gemini,claude,codex

Expert AI Agent Skill for **Code Reviewing** - Standards and practices for reviewing code effectively based on [Google's Engineering Practices](https://google.github.io/eng-practices/review/reviewer/).

## 🎯 Core Mandates (The Reviewer's Rules)

- **Preflight Check:** Always check if the code compiles and passes basic linting *before* starting the deep review. If it fails, reject immediately with the error logs.
- **The Standard for Approval:** Approve a CL if it is a net improvement, even if it's not perfect. Don't block for minor preferences.
- **Speed is Critical:** Respond to code reviews within one business day.
- **Mentorship Mindset:** Explain **WHY** you're requesting a change. Aim to teach the author.
- **7 Pillars of Review:** Conduct a holistic review based on:
    1.  **Correctness:** Does the logic actually work?
    2.  **Readability:** Is it easy to understand for future maintainers?
    3.  **Maintainability:** Does it avoid technical debt and duplication?
    4.  **Efficiency:** Are there obvious performance bottlenecks?
    5.  **Security:** Does it introduce vulnerabilities (logging secrets, SQL injection)?
    6.  **Edge Cases:** Does it handle `null`, empty inputs, and failures?
    7.  **Testability:** Is the logic covered by unit tests that actually fail when logic is broken?

---

## 🛠 Reviewing Workflows

### 1. Preflight & High-Level View
- Check compilation (`mvn compile`, `bazel build`).
- Review the CL description. Is the intent clear? Are the "Risk Areas" called out?
- Look for major architectural flaws first. Stop and discuss before nitpicking.

### 2. Deep Dive & Adversarial Logic Tracing
Use these "Adversarial" techniques to find hidden bugs:
- **The "What-If" Tracing:** "Assume line X returns `null` or an empty list. Trace the execution path. Does it fail gracefully?"
- **The "Boundary" Analysis:** "Check all comparison operators (>, <, ==). Verify if 'off-by-one' errors are possible."
- **The "Inversion" Check:** "Can you find a sequence of inputs that would enter an infinite loop or cause a race condition?"

### 3. Writing Constructive Feedback
- **Be Professional:** Focus on the code, not the person.
- **Distinguish Requirements from Suggestions:** Prefix minor suggestions with `Nit:`.
- **Explain Reasoning:** Instead of "Do this," say "Do this because it improves [Pillar X] by Y."

---

## 🔍 Comment Template Examples

- **Nitpick (Readability):** `Nit: This variable name could be more descriptive (e.g., 'userName' instead of 'un').`
- **Requirement (Correctness):** `Must fix: This loop is O(n^2), but could be O(n) using a Map. This will block the Event Loop in production.`
- **Adversarial Question:** `What happens if 'userService.find()' returns null here? It looks like line 45 would throw a NullPointerException.`
- **Security Nit:** `Nit: Logging the raw request body might leak sensitive customer data. Consider masking sensitive fields.`

---

## 🌐 Knowledge Sources & Deep Dives

> **Directive:** Use `web_fetch` to find Google's specific guidance on "Standards," "Speed," or "Constructive Feedback" during a code review.

- **Reviewer's Guide:** [Google Eng Practices - Reviewing](https://google.github.io/eng-practices/review/reviewer/) - The primary source.
- **Automated Checklists:** [7 Pillars of Reviewing](https://skills.sh/google-gemini/gemini-cli/code-reviewer) - Holistic review categories.
- **Superpowers for Reviewing:** [Requesting Code Review](https://skills.sh/obra/superpowers/requesting-code-review) - Structuring requests and responses.
- **Approval Standards:** [What is the standard?](https://google.github.io/eng-practices/review/reviewer/standard.html) - When to say LGTM.
- **Review Speed:** [The Speed of Code Reviews](https://google.github.io/eng-practices/review/reviewer/speed.html) - Why it matters.

## Skill Interoperability

The **code-reviewer** 🔍 skill acts as a quality gate for other skills:
- **java-expert** ☕ & **quarkus-expert** ⚡: Logic is reviewed against framework best practices.
- **refactoring-expert** 🛠: Refactoring changes are checked for behavior preservation and metrics.
- **code-author** ✍️: Works in tandem to ensure a smooth feedback loop.
