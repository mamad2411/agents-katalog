---
name: writing-clearly
description: "Rules for clear, concise writing. Apply when drafting or editing docs, READMEs, comments, commit bodies, or any user-facing prose."
---

# Writing Clearly and Concisely

> Adapted from [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)

## Overview

Write with clarity and force. This skill covers what to do (Strunk) and what not to do (AI patterns).

## When to Use This Skill

Use this skill whenever you write prose for humans:

- Documentation, README files, technical explanations
- Commit messages, pull request descriptions
- Error messages, UI copy, help text, comments
- Reports, summaries, or any explanation
- Editing to improve clarity

**If you're writing sentences for a human to read, use this skill.**

## Elements of Style

William Strunk Jr.'s *The Elements of Style* (1918) teaches you to write clearly and cut ruthlessly.

### Rules

**Elementary Rules of Usage (Grammar/Punctuation):**

1. Form possessive singular by adding 's
2. Use comma after each term in series except last
3. Enclose parenthetic expressions between commas
4. Comma before conjunction introducing co-ordinate clause
5. Don't join independent clauses by comma
6. Don't break sentences in two
7. Participial phrase at beginning refers to grammatical subject

**Elementary Principles of Composition:**

8. One paragraph per topic
9. Begin paragraph with topic sentence
10. **Use active voice**
11. **Put statements in positive form**
12. **Use definite, specific, concrete language**
13. **Omit needless words**
14. Avoid succession of loose sentences
15. Express co-ordinate ideas in similar form
16. **Keep related words together**
17. Keep to one tense in summaries
18. **Place emphatic words at end of sentence**

### The Most Important Rules (10-13, 16, 18)

- **Active voice**: "The team shipped the feature" not "The feature was shipped by the team"
- **Positive form**: "He forgot" not "He did not remember"
- **Specific language**: "It rained every day for a week" not "A period of unfavorable weather set in"
- **Omit needless words**: "The question as to whether" → "Whether". "He is a man who" → "He". "The reason why is that" → "Because"
- **Keep related words together**: Subject near verb, modifier near the word it modifies
- **Emphatic words at end**: "Humanity has barely noticed this loss" not "This loss has barely been noticed by humanity"

## AI Writing Patterns to Avoid

LLMs regress to statistical means, producing generic, puffy prose. Avoid:

- **Puffery:** pivotal, crucial, vital, testament, enduring legacy
- **Empty "-ing" phrases:** ensuring reliability, showcasing features, highlighting capabilities
- **Promotional adjectives:** groundbreaking, seamless, robust, cutting-edge
- **Overused AI vocabulary:** delve, leverage, multifaceted, foster, realm, tapestry
- **Formatting overuse:** excessive bullets, emoji decorations, bold on every other word

Be specific, not grandiose. Say what it actually does.

For the full catalog of AI writing tells (sentence structure, tone, composition patterns), use `/write-as-human`.

## Bottom Line

When writing for humans: use active voice, put statements in positive form, be specific, and omit needless words. If it sounds like marketing copy, rewrite it.
