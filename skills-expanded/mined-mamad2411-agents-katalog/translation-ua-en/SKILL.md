---
name: translation-ua-en
description: Translate ArtStroy article drafts from Ukrainian to English while preserving MDX structure, frontmatter fields, code blocks, and component syntax. Includes cultural idiom adaptation for an international technical audience.
---

# Translation: Ukrainian → English

ArtStroy's author (AZANIR) writes first drafts in Ukrainian. The Translator produces the English publication version. The English text must read as native — not translated.

## When to Run

- When a `article-draft` issue is assigned to Translator with a UA draft attached
- The draft file is at `src/content/articles/{slug}/index.mdx` with Ukrainian body text

## What to Translate

**Translate:**
- Article body text (all prose paragraphs, headings, list items, blockquotes)
- `title` frontmatter field
- `description` frontmatter field
- Alt text in `<Image>` components if it is in Ukrainian
- Any inline comments visible to readers (e.g., captions in `<Figure>` components)

**Do NOT translate:**
- Code blocks (everything inside triple backticks or `<CodeBlock>` components — code is language-agnostic)
- URLs and slugs
- The slug (directory name) — already English
- `publishedTime`, `authors`, `cover`, `category` frontmatter fields
- MDX import statements (`import { ... } from '...'`)
- Component names and props: `<Component prop="value" />` — only translate string prop values if they are visible UI text
- `isDraft` value

## MDX Preservation Rules

These patterns must survive translation exactly:

```mdx
{/* This is an MDX comment — preserve exactly */}

import { SomeComponent } from './components/SomeComponent.tsx'
{/* ↑ preserve exactly */}

<SomeComponent
  title="This title IS user-facing — translate"
  internalId="do-not-translate"
  client:load
/>

```code block content — never translate```

<Image src={cover} alt="descriptive alt text — translate this" />
```

**Practical rule**: if a string would be rendered and read by a website visitor, translate it. If it is code, config, or infrastructure, leave it.

## Translation Quality Standards

### Register and Tone

ArtStroy's voice: direct, technical, confident, slightly informal (like a senior engineer explaining to a peer). Not academic. Not overly casual. Never corporate marketing tone.

Markers of ArtStroy's voice to replicate in English:
- Short declarative sentences for key points ("OWASP recommends X. This matters because Y.")
- "we" for the author+reader team ("Let's look at...", "We can see that...")
- Imperative in tutorials ("Run the command", "Open the file", not "The user should run...")
- No hedging language ("might", "could possibly") unless the original is genuinely uncertain

### Cultural Adaptation

Ukrainian technical writing has specific idioms that translate poorly literally:

| Ukrainian pattern | Literal (avoid) | Natural English equivalent |
|---|---|---|
| "Розглянемо ..." | "Let us consider..." | "Let's look at..." / "Here's how..." |
| "Варто зазначити" | "It is worth noting" | "Note that..." / "Importantly..." |
| "На практиці" | "In practice" | "In the real world" / "In production" |
| "Гарна практика" | "Good practice" | "Best practice" / "The right approach" |
| Parenthetical explanations "(тобто ...)" | "(that is...)" | Rewrite as a clause, not a parenthetical |

When an idiom or analogy relies on a Ukrainian cultural reference with no English equivalent, replace it with a functionally equivalent reference familiar to an international software engineering audience.

### Technical Terminology

Use standard English technical terms as they appear in:
- OWASP documentation (for security topics)
- MDN Web Docs (for web/browser APIs)
- Official tool documentation (for framework-specific terms)

Do not invent anglicisms from the Ukrainian if an established English term exists (e.g., "запит" → "request", not "query-request").

## Process

1. Read the full draft before translating — understand the article's argument arc
2. Translate section by section, not sentence by sentence (preserve flow)
3. After translating, re-read the English version from top to bottom as if reading a fresh article — fix any stiffness
4. Verify all MDX components and frontmatter are structurally identical to the original

## Output

The Translator edits the `index.mdx` file directly — overwrites the Ukrainian prose with the English translation while leaving all MDX structure intact.

After completing the translation:
- Comment on the issue: "Translation complete. English draft ready for Editor review."
- Assign the issue to Editor
- Add label `needs-editorial-review`

## Handoff to Editor

The Editor reviews both the original UA draft (accessible in git history or as a comment) and the English version for:
- Faithfulness to the original argument
- Natural English register
- Technical accuracy (the Translator is a language specialist, not necessarily a deep SME on every topic)

The Editor should flag any section where the translation may have changed the technical meaning, not just the wording.
