---
name: markdown-discipline
description: Markdown writing discipline that strips AI-slop tells — no em dashes, no marketing fluff, no emoji bullets, no triple-cataloging, no soft closes. Use when writing or editing any markdown content (README, docs, briefs).
license: MIT
---

# Markdown discipline

Apply to docs, READMEs, briefs, and any markdown content. The goal: high-signal text that reads well as both a doc and as context for an LLM.

## Banned

- Emoji in any markdown (unless explicitly requested by the user)
- Marketing adjectives ("robust", "powerful", "comprehensive", "seamless", "world-class", "leverage" as verb)
- Welcome banners + celebration emoji + "Let's dive in!" energy
- Triple-cataloging ("fast, simple, and reliable")
- Antithesis pattern ("It's not X; it's Y")
- Soft closes ("Hope this helps!" / "Let me know if you have questions")
- Title Case headings
- Em dash overuse (sparingly, < 2 per page)
- Excessive bold (one bolded phrase per paragraph max)
- Block quotes used as warning callouts
- Multiple H1s per file
- Sentence fragments for emphasis

## Required

- Sentence case for headings
- One H1 per file
- Headings describe content, don't announce sections
- One sentence per bullet
- Max 2 nesting levels in lists
- Code fences specify language
- Inline code for filenames, identifiers, types
- Descriptive link text
- Tables only for comparison matrices

## Reading test

- Does the second half of a paragraph add new info? If no, cut.
- Are bullets in a list distinct or padded? If padded, cut.
- Does a heading describe what's below or announce a section? Describe.
- Would a comma work where an em dash is? Use it.

---

Full content + before/after examples at https://github.com/HermeticOrmus/markdown-discipline-skills.
