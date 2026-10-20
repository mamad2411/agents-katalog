---
name: wikipedia-like-writing
description: Helps an AI assistant write, structure, and edit articles in the encyclopedic style of Wikipedia — neutral tone, lead section, summary style, inline citations, no peacock/weasel/persuasive language, and the stub→FA quality ladder. Also covers Simple English Wikipedia rules. MADE BY SQERSTERS
risk: safe
source: community
version: 1.0.0
license: MIT
---

# Wikipedia-like Writing

## Purpose

This skill teaches an AI assistant how to write and edit articles in the style of Wikipedia.

It is **not** a skill for writing actual Wikipedia articles — Wikipedia explicitly forbids LLMs from generating article content. It is for writing **encyclopedia-style content elsewhere** (a Miraheze wiki, a personal knowledge base, a project wiki, a fan wiki, internal docs) using the conventions Wikipedia has refined over two decades.

When this skill is active, the assistant must:

- Write in a **formal, impersonal, neutral** tone.
- Build articles around the **lead → body → appendices** structure.
- Treat every claim as if it needed an **inline citation** to a reliable source.
- Refuse purple prose, hype, hedging, and rhetorical questions.

---

## Core Rule

Before writing, ask in this order:

1. **What is the topic?** Is it a thing, a person, a concept, a fictional entity, an event?
2. **Is it notable?** Is there enough material from independent, reliable sources to justify a standalone article? If not, fold it into a parent topic.
3. **Who is the reader?** A non-specialist who arrived from a random link. The article must make sense to them.
4. **What quality tier am I targeting?** Stub, Start, C, B, Good, A, or Featured (see the quality ladder below).

If any of these is unclear, ask the user before writing.

---

## Article Structure

Every article (above stub size) follows this layout:

```
1. Lead section          (no heading — appears above the first ==Heading==)
2. Body                  (level-2 sections, level-3 subsections)
3. Standard appendices   (in this exact order):
   - Works               (for biographies/creators)
   - See also            (related internal links)
   - Notes / References  (citations, footnotes)
   - Further reading     (recommended sources NOT cited)
   - External links      (relevant websites NOT cited)
```

### Lead section rules

- **Stands alone** as a complete summary of the topic.
- **No more than ~400 words.**
- First sentence: short, declarative. Answers *"What is the subject?"* and *"Why is it notable?"*
- The article title appears in **bold** the first time it appears (and only the first time).
- Italicise the title if it would normally be italicised (books, films, ships, paintings).
- Avoid links inside the bolded title. Link surrounding words instead.
- Cover every major section of the body in proportion to its importance.
- The lead **summarises the body, never introduces new material.** Body first, lead second.

### First-sentence patterns

Good:

> **Amalie Emmy Noether** (23 March 1882 – 14 April 1935) was a German mathematician known for her contributions to abstract algebra and theoretical physics.

> An **electron** is a subatomic particle that carries a negative electric charge.

Bad:

- *"Computer architecture refers to the theory behind…"* — uses-vs-mentions error. The article is about the theory, not the words.
- *"A nuchal cord is when the umbilical cord becomes wrapped around the fetus's neck."* — `is when` is vague. Use `is a condition in which…`.

---

## Tone

The tone is **formal, impersonal, dispassionate.** Always.

### Forbidden

| Category | Examples |
|---|---|
| **First-person** | I, me, we, us, our |
| **Second-person** | you, your |
| **Peacock terms** | one of the most important, prestigious, influential, significant |
| **Weasel words** | some say, many believe, it is widely regarded as, critics say |
| **Persuasive style** | appeals to emotion, calls to action, advocacy |
| **News style** | bombast, pull quotes, headlinese, recentism |
| **Colloquial / poetic** | hyperbole, jargon (without explanation), unnecessary acronyms, contractions |
| **Punctuation** | exclamation marks, rhetorical questions (both only inside direct quotations) |

### Style examples

| News style | Persuasive style | Encyclopedic style |
|---|---|---|
| At a press conference on Monday evening, Sue Speaker announced that the investigation would officially be closed the next day. | The recently closed investigation demonstrates again why everyone should support restrictions on social media… | The investigation was closed. |

### Show, don't tell

Replace *"The Yankees are one of the greatest baseball teams in history"* with *"The New York Yankees have won 27 World Series championships — almost three times as many as any other team."*

The facts carry the weight. Adjectives don't.

---

## Two compatible style frames

Wikipedia articles tend to use one of two structures (often both):

1. **Summary style** — Broad topic with subsections that summarise sub-articles. Good for large, hierarchical subjects (`Association football`, `World War II`).
2. **Inverted pyramid** — Most important info first, decreasing in importance. Good for short biographies, single events, stub articles.

The lead is **always** inverted-pyramid. The body may follow either.

---

## Citations and verifiability

Every substantive statement needs a source.

- **Inline citations** required for: direct quotations, statistics, contentious claims about living people, and anything likely to be challenged.
- **Reliable sources**: books from reputable publishers, peer-reviewed journals, respected newspapers, sources with a fact-checking reputation.
- **Not reliable**: blogs, social media, user-generated content, personal websites, and Wikipedia/the wiki itself.
- **Primary sources** allowed sparingly, only for basic facts. They do not establish notability.
- **Three independent reliable sources** is the rough floor for notability.

When in doubt, cite. *"Be careful about deleting material that may be factual."*

---

## Provide context

Wikipedia readers come from anywhere and arrive via random links. Test every article with these questions:

- Does this make sense if the reader landed here from a random page?
- Could a layperson in another English-speaking country tell what this is about?
- If you printed page 1 only, would the reader know the topic?

State the obvious in the first one or two sentences. *"The Ford Thunderbird was a car…"* not *"The Ford Thunderbird was conceived as a response to the Chevrolet Corvette…"*

Avoid jargon. When jargon is needed, explain it inline or link to an article that does.

---

## The quality ladder

When asked to write an article or improve one, target a specific tier:

| Tier | Bar | What it means |
|---|---|---|
| **Stub** | A few sentences. Has a stub template, a category, at least one wikilink. | Enough context for someone else to expand it. |
| **Start** | Sectioned. Some sources (even questionable ones). Meets core content policies. | Past speedy-deletion danger. |
| **C** | Average. Some content gaps, some irrelevant material. | Workable but uneven. |
| **B** | Suitably referenced with inline citations. Reasonable coverage. Defined structure. Reasonably well-written. Supporting media. Understandable to a broad audience. | Comprehensive to a casual reader. |
| **Good** (GA) | All B-class criteria, plus: clear and concise prose, no original research, no copyvio/plagiarism, neutral, stable, illustrated where possible with proper licensing and captions. | Reviewed by an impartial editor. |
| **A** | Between GA and FA. | Rarely used outside large WikiProjects. |
| **Featured** (FA) | Professional standards of writing, presentation, sourcing. | Wikipedia's best work. |

When the user says "write a Wikipedia-style article", default to **B-class** unless they specify otherwise.

---

## Concrete writing checklist

Before finalising any article-style output, verify:

- [ ] First sentence defines the topic and answers *what* and *why notable*.
- [ ] Title appears in **bold** on first mention.
- [ ] Lead is ≤ 400 words and summarises every major section of the body.
- [ ] Body uses level-2 headings (`==`), no links in headings.
- [ ] Tone is formal, no first/second person, no peacock/weasel/persuasive language.
- [ ] No exclamation marks or rhetorical questions outside quotations.
- [ ] Inline citations for quotations, statistics, contentious claims, and BLP-sensitive content.
- [ ] Jargon is explained or linked.
- [ ] Major viewpoints represented fairly; fringe views not given undue weight.
- [ ] Standard appendices in the right order.
- [ ] Spelling and grammar are correct.
- [ ] Article is **on topic** — no irrelevant tangents.

---

## Common mistakes to refuse

When asked to do any of these, push back and offer the encyclopedic alternative instead:

- Promotional copy disguised as an article (*"a leading provider of…"*, *"trusted by thousands"*)
- Articles that exist only to define a single word (that's a dictionary, not an encyclopedia)
- Original research, personal essays, opinion pieces in article form
- Future speculation framed as fact
- Articles about non-notable subjects (your band, your project, your site) without independent coverage
- Copying source text verbatim — always paraphrase and cite

If the user asks for something Wikipedia-style for a real Wikipedia article, remind them that Wikipedia's policies forbid LLM-generated article content. Help them draft notes, find sources, or critique their own draft instead.

---

## Simple English mode

When the user asks for **Simple English** style (for the Simple English Wikipedia, ESL audiences, accessibility, or plain-language docs), apply these extra rules on top of everything above.

### Audience

Readers may have English as a second language, be young, or have learning difficulties. The **language** is simple. The **ideas** do not have to be.

### Vocabulary order

When picking a word, try in this order:

1. **Basic English (BE) 850** — the simplest tier.
2. **Basic English (BE) 1500** — slightly broader.
3. **VOA Special English Word Book** — broader still.
4. Anything else — only if the simpler word is unclear or wrong, and link or explain it inline.

### Method

1. Write the sentence as you'd say it to an ordinary person.
2. Check your words against the lists above.
3. Convert **passive → active voice**: *"The bird was eaten by the cat"* → *"The cat ate the bird."*
4. Use **past or present tense only**. Avoid future, conditional, perfect.
5. Use **subject-verb-object** sentences. One idea per sentence.
6. Avoid compound and compound-complex sentences. Split them.
7. No idioms, no contractions, no slang.

### Sentence-splitting recipes

- See `and / or / but / for / so / yet`? Split into two sentences.
- Missing subject in the second clause? Add the pronoun.
- Semicolon? Split.
- Multiple subordinate clauses? Reorder so the most important info comes first, start follow-up sentences with `This is…` / `This was…`.
- Mid-sentence dependent clause? Move it to its own sentence with the right pronoun.

### What not to do (Simple English)

- Don't use poor grammar — Simple English ≠ broken English.
- Don't use contractions (*can't*, *I've*, *hasn't*). Use the long form.
- Don't use the second person.
- Don't put links in headings.
- Don't copy the regular Wikipedia article verbatim and call it Simple. Rewrite it.

### Length expectation

A Simple English article is often **25–50% longer** than the equivalent regular article — short sentences need filler words to stay readable. Simple English is **not shorter English**.

---

## Sources

This skill is distilled from these Wikipedia guidance pages:

- [Help:Your first article](https://en.wikipedia.org/wiki/Help:Your_first_article)
- [Wikipedia:Writing better articles](https://en.wikipedia.org/wiki/Wikipedia:Writing_better_articles)
- [Wikipedia:How to write a featured article](https://en.wikipedia.org/wiki/Wikipedia:How_to_write_a_featured_article)
- [Wikipedia:How to write Simple English pages (Simple Wiki)](https://simple.wikipedia.org/wiki/Wikipedia:How_to_write_Simple_English_pages)

Content was rephrased and condensed for compliance with licensing restrictions. Source pages are CC BY-SA 4.0.
