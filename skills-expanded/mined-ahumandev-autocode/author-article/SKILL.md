---
name: author-article
description: Use `author-article` to get Professional Article/Report Format when reviewing/writing user content as articles/reports.
---

# Professional Article/Report Format

Follow these instructions before reviewing/writing professional articles/reports

## Editorial Rules

- Use full human-readable sentences by default
- Reduce long sentences > 40 words to smaller sentences (except in quoted text)
- Fix spelling and grammar mistakes (except in quoted text)
- Use British English by default in articles (unless different language requested)
- Merge repetitions
- Group long text into paragraphs. One paragraph = one argument or point.
- Start paragraphs with a statement or fact. Follow with explanation and examples.
- Keep article on introduction topic.
- Capitalize title words. Except prepositions < 4 chars (in, on, at, to, by, of, up), conjunctions (and, but, for, or, not, so, yet), and articles (a, an, the).
- NEVER modify quoted text even if it contains errors
- NEVER change the meaning of the text, unless the user explicitly asked to do so

## Style Rules

- Add introduction if missing. State article topic, but not main argument or point. Trigger curiosity. Do not offend groups or people strongly opposed to main argument.
- Write articles in third person
- Replace arrogant, offensive, or divisive tone. Replace sarcasm and rhetorical questions with objective statements.
- Write diplomatically. Do not offend people groups.
- Use professional tone. Explain academic and technical words in basic layman terms for non-Christians.
- Allow "I think", "We believe", and "It's possible" only for unproven opinion.
- Replace em dashes (—) and en dashes (–) with short sentences and periods. Except quoted text.
- In Old Testament verses only, replace `the Lord` with `the LORD`. New Testament verses may use `the Lord`.
- Use basic English. Explain complex academic terms for non-English speakers and laymen.
- Conclusion only summarizes main argument, point, or purpose. No explanation or evidence. Link each conclusion statement to supporting main-content section.

## Credibility Rules

- Rephrase confusing explanations, contradictions or fallacies
- Honestly say when statement is unproven opinion.
- Check Bible verse quotes and references. Fix wrong quotes. Replace wrong references with correct scripture. Example: `Jesus said love your enemies (Genesis 1:1)` is wrong. Genesis 1:1 does not say this.
- Add known evidence, such as Bible scripture or Markdown links to external sites.
- Remove contradictions against the author's own content
- Article must not contradict itself. Explain or note conflicts. Warn user.
- Check reasoning errors and fallacies. Rephrase arguments without logic errors; keep intended message.
- For controversial statements, add typical critique and defence.
- Add evidence to weak arguments. Rephrase if no evidence exists.
- Check external links. Find and fix broken site links, or remove them.

## Formatting Rules

- First line after frontmatter is main title. Use one H1 only.
- Keep H2 headers as short as possible, but still unique.
- Ensure logical header hierarchy (no skipped levels).
- Large sections (> 25 lines) should be subdivided into smaller subsections.
- Use numerical points if the article mentions a specific sequence or priority.
- Use bullet points only to list items.
- Convert `--` double hyphens in quoted text to em dashes.
- Format quotes: `> Quoted text — Source`. Put spaces around em dash. Source: Bible verse, author, book, or external link.
- For Bible quote source, include book abbreviation: `John 3:16 (ESV)`. Omit book abbreviation for inline Bible references.
- Separate verses from different books with `;`: `Genesis 1; Exodus 1:1; Leviticus 1`.
- Separate same-book, different-chapter verses with `, `, for example: `Genesis 1:1, 2:1, 3:1`.
- Separate same-book, same-chapter verses with `,` and no spaces: `Genesis 1:1-3,5-7,11,13`. Number without `:` means verse in prior chapter. Example: `Genesis 1:1,3` means Genesis 1:1 and Genesis 1:3.
- Provide full bible book names, not abbreviated (e.g., `Genesis` instead of `Gen`).
- NEVER md link bible verse references to online sources.

## Markdown Rules

- Convert underscore headers `-------------` to hashed prefix headers `##`
- Content should be Markdown linter compliant
- Code samples must be displayed in md code blocks specifying the correct language attribute
- Link online sites or external MD files when content uses an external source.
- Double spaces before EOL allowed. They make Markdown line breaks.
- Ensure that Markdown links within the same document to anchors/headers are valid.
- Fragments are preserved, for example `path/page.md#anchor`
- Store images beside Markdown, unless linked externally.
- Name images `{page}.{descriptor}.{ext}`. Avoid duplicate names, such as `church.church.jpg`.
- Provide alt text for accessibility
- Use Mermaid for complex relationships, integrations, or architecture.
- Strikethrough text as Markdown strikethrough: ~~strikethrough~~
- Inline math formulas as Markdown inline math: $E = mc^2$
- Block math formulas as Markdown block math: $$ ... $$
- Links to online sources as Markdown links: [source name](url)
- Public logos, icons, illustrations as Markdown images: ![alt text](url)

## Layout Rules

Default md layout (unless different layout was requested):
```
---
description: [Description]
keywords: [Keywords]
---

# [Title]

[Introduction]

## [Content Sections]

### [Optional Sub-Sections]

#### [Optional Sub-Sub-Sections...]

## Conclusion

[Conclusion Content]
```

- Conclusion summarize solution to introduction problem. Do not repeat problem.
- Conclusion summarize every article section in 1 sentence.
- Conclusion inline md links to article anchors with details.

## Frontmatter Rules

- Add frontmatter by default, unless user says otherwise.
- Description is SEO meta tag. Max 160 chars. Complement introduction: state article topic, hide main argument and solution, trigger curiosity. Do not offend groups or viewpoints. Do not start with verb. State article problem.
- Set `keywords` to useful CSV keywords from main points. Use unique keywords. Avoid common or generic words.
