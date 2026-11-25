---
name: wikipedia-not-ai
description: "Detect AI-generated text by identifying characteristic patterns, phrases, and structural tells from LLMs like ChatGPT, Gemini, and others. Use when the user wants to check if a text was written by AI, audit content for AI tells, clean up AI-generated writing to make it less detectable, understand what makes text sound AI-generated, or review emails, articles, reports, marketing copy, or any prose for AI markers."
---

# AI Text Detection Guide

Derived from Wikipedia's empirically documented field guide on LLM writing patterns. Applicable to any text — not just Wikipedia.

## How to analyze text

Scan for signals across the categories below. Weight **clusters** more heavily than isolated occurrences — one "pivotal" is coincidence; five AI-vocab words in a paragraph is a strong signal.

**Output format:** Quote specific examples from the text, categorize each signal, then give an overall verdict: **Likely AI / Possibly AI / Likely Human** with brief reasoning.

**Important:** Newer models (GPT-5.1+, Claude 4+) actively suppress known tells like em dashes and classic AI vocabulary. Absence of classic markers is NOT proof of human origin. Look for subtler patterns: overly cautious hedging, Latinate word preference, "quietly" narratives, structural uniformity, the four deeper tells in Section 12 (abstraction trap, sensing without sensing, treadmill effect, subtext vacuum), and the in-disguise patterns in Sections 14–16 (decorative triplets, drumroll-in-disguise, false idioms/calques) — these are the most reliable signals on modern models.

---

## 1. AI Vocabulary Density (strongest signal)

LLMs statistically overuse specific words. Check for density/clusters.

See **[word-lists.md](references/word-lists.md)** for the complete list by model era.

Quick scan: *pivotal, underscore, tapestry, delve, meticulous, vibrant, intricate, testament, bolstered, garner, fostering, showcasing, align with, enhance, highlighting*

One word = coincidence. Five+ in a short passage = strong AI signal.

---

## 2. Content Patterns

### Significance inflation
Adds statements about how mundane facts "represent a shift," "mark a pivotal moment," or "contribute to the broader landscape" — even for population data or etymology.

Trigger phrases: *stands as, serves as, marks a pivotal, underscores its importance, reflects broader, symbolizing its enduring, setting the stage for, indelible mark, deeply rooted, evolving landscape*

### Challenges formula
Rigid structure, usually at the end: *"Despite its [positive adjective], [subject] faces challenges including... Despite these challenges, [vague optimism about the future]."*

### Superficial -ing clauses
Tacks present participle phrases onto sentences as pseudo-analysis:
*"...highlighting its importance," "...underscoring the significance," "...reflecting the broader trend."*

### Vague attribution weaseling
Attributes claims to no one specific: *"Experts argue," "Observers have noted," "Industry reports suggest," "Several sources indicate," "Some critics argue."*

### Promotional/travel-guide tone
Warm, advertisement-like prose even on neutral topics: *nestled, vibrant, rich cultural heritage, breathtaking, diverse array, boasts, showcasing, groundbreaking, renowned, in the heart of.*

### Overgeneralization from few sources
LLMs take information from 1–2 sources but present it as widely held or as an incomplete list. Watch for: *"including..."* or *"such as..."* when the enumeration actually covers everything the sources say; opinions from a single source framed as consensus; *"widely regarded," "generally considered"* without evidence of breadth.

### "Quietly" narratives
LLMs often describe actions or developments as happening *"quietly"* — a pseudo-narrative detail that adds false drama or modesty. Rare in factual human writing, common across multiple LLM families.

---

## 3. Sentence Structure Tells

### Copula avoidance
Replaces simple "is/are/has" with elaborate constructions:
- ❌ *"serves as the primary hub"* → ✅ "is the primary hub"
- ❌ *"marks a significant milestone"* → ✅ "was a significant milestone"
- ❌ *"boasts four separate spaces"* → ✅ "has four separate spaces"

### Latinate over Saxon
Systematically chooses Latin/Greek-derived words over simpler Germanic equivalents, even in plain contexts:
- ❌ *"utilize"* → ✅ "use"
- ❌ *"facilitate"* → ✅ "help"
- ❌ *"is devoid of"* → ✅ "has no"
- ❌ *"commence"* → ✅ "start/begin"
- ❌ *"ameliorate"* → ✅ "improve"
- ❌ *"expedite"* → ✅ "speed up"

This is distinct from copula avoidance — it's about lexical register, not syntax. As Orwell noted, bad writers are "haunted by the notion that Latin or Greek words are grander than Saxon ones." LLMs embody this tendency statistically.

### Negative parallelisms
Pseudo-balance: *"Not only X, but also Y"*, *"It's not just X, it's Y"*, *"Not X — it's Y."* Sounds thoughtful but is formulaic. See Section 14 for the more specific *decorative triplets* extension of this pattern.

### Rule of three
Compulsive tripling: "adjective, adjective, and adjective" or "phrase, phrase, and phrase" even when two or four would be more natural. The decorative subtype is now treated separately — see Section 14.

### Elegant variation
Avoids repeating a word by substituting awkward synonyms throughout: subject → "the eponymous figure" → "the key player" → "this individual."

---

## 4. Formatting Tells

- **Title Case In Every Section Heading** (humans normally use sentence case)
- **Excessive boldface** — bolding key takeaways scattered throughout body text
- **Inline-header lists**: `• **Bold Term**: description text` pattern
- **Emoji** in headings or bullet points 🎯
- **Em dash overuse** — used dramatically — where a comma or parenthesis would do — often multiple times per paragraph
- **Unnecessary tables** for 2–3 data points that should just be prose
- **Curly quotes** (" " ' ') instead of straight quotes (" ') — common in ChatGPT/DeepSeek
- **Markdown in non-markdown contexts** — `**bold**`, `# Header`, `- list item` with dashes appearing in documents, emails, wiki markup, or any context where markdown is not the native format. Wikipedia added an edit filter specifically for this. Strong signal when combined with other tells.

---

## 5. Communication Leakage

Text meant for the AI chat interface that got pasted into the document:
- *"I hope this helps," "Would you like me to...", "Let me know if you need anything else"*
- Knowledge-cutoff disclaimers: *"as of my last update," "not widely documented," "maintains a low profile"*
- Unfilled placeholders: `[INSERT NAME HERE]`, `[Describe the specific section]`
- Subject lines in body text: *"Subject: Request for Edit"*
- Submission statements: *"This article meets WP:RS because..."*

---

## 6. Citation & Markup Artifacts (documents/web content)

Technical residue from specific AI tools:
- `turn0search0`, `turn0search1` — ChatGPT search citation artifacts
- `contentReference[oaicite:0]{index=0}` — ChatGPT reference rendering bug
- `oai_citation`, `+1` inline — ChatGPT markup bugs
- `{"attribution":{"attributableIndex":"X-Y"}}` — ChatGPT JSON attribution
- `utm_source=chatgpt.com` or `utm_source=openai` in URLs
- `[attached_file:1]`, `[web:1]` — Perplexity artifacts
- `<grok_card ...>` — Grok artifacts
- Invalid/unresolvable DOIs or ISBNs with correct-looking formats
- Book citations with no page numbers

---

## 7. Image & Caption Tells

LLMs select illustrations by keyword-matching file names or titles, not by actual visual relevance:
- Generic images loosely related to the topic but not to the specific content (e.g., a 19th-century painting of a waiter for a modern hospitality article)
- Captions that inflate a trivial detail from the image metadata: *"1946, marking an important year in..."* — significance inflation applied to image dates
- Multiple images that all illustrate the same general concept rather than different aspects of the text

---

## 8. Argumentative & Discussion Tells

When LLMs generate persuasive, argumentative, or discussion text (not just articles):
- **Rhetorical anaphora** — repeating sentence openers for emphasis in contexts where it's inappropriate (e.g., formal discussions, business emails)
- **Needless length** — walls of text that reiterate the same points in slightly different wording
- **Hallucinated references** — citing policies, rules, or frameworks that don't exist or don't apply (*"As per WP:UNDERREP..."*, *"According to industry standard 4.2.1..."*)
- **Context-alien terminology** — injecting jargon from unrelated domains (e.g., DEI language in a technical discussion, therapeutic language in a business context)
- **Refusal to concede** — in multi-turn text, progressively longer and more aggressive responses that add no new substance
- **That's-not-this-it's-that pattern** — frequent reframing: *"This isn't about X, it's about Y"*, *"The real issue isn't X — it's Y"*

---

## 9. Newer Model Evasion (2025+)

AI companies actively suppress known tells. Be aware:
- GPT-5.1 specifically reduces em dash usage
- Newer models use fewer classic AI-vocab words (see word-lists.md GPT-5 era section)
- Some models now mimic "imperfect" human patterns — occasional sentence fragments, contractions, informal tone
- **What persists:** structural uniformity (every paragraph roughly the same length/shape), Latinate vocabulary preference, overgeneralization, significance inflation in subtler forms, and the absence of genuine authorial quirks (idiosyncratic metaphors, personal references, domain-specific humor)
- **Key principle:** If a text has zero classic tells but also zero personality — uniform paragraph lengths, no surprises, no rough edges — that itself is a signal worth noting

---

## 10. Older Model Tells (2022–2024)

Less common in newer models, useful for auditing older content:
- *"It's important to note that..."*, *"It's crucial to remember..."*
- *"In summary," "In conclusion," "Overall,"* ending sections
- *"As an AI language model, I..."* partial refusals
- Text cut off abruptly mid-sentence

---

## 11. Context-Sensitive Phrase Restrictions

Certain phrases sound human in isolation but become AI tells when used in the wrong context. Flag these when the context doesn't justify the emotional weight.

### "and I didn't see it coming" / "I never saw it coming"
Legitimate only in: life-threatening situations, unexpected personal turning points, major life discoveries.
❌ Avoid in: software reviews, product descriptions, workflow descriptions, business writing.
Example of misuse: *"That combination changed how I work — and I didn't see it coming."* (software review)
Example of correct use: *"The diagnosis came back positive. I didn't see it coming."*

### "and what I didn't expect" / "what I didn't expect was"
Same rule as above. Reserve for genuine surprise in high-stakes personal or life contexts.
❌ Avoid in: tool reviews, feature descriptions, onboarding narratives, professional writing.
When in doubt: replace with a plain statement of the fact itself. *"I now manage most of it through Claude"* is stronger than *"what I didn't expect: I now manage most of it through Claude."*

### "genuinely"
Legitimate only in: references to authentic brands, original authorship, pure emotional states, sincere personal convictions.
❌ Avoid as a general intensifier in: product reviews, performance claims, workflow descriptions.
Example of misuse: *"genuinely changed how I work"* (software review — use the plain verb instead)
Example of correct use: *"This is genuinely his work, not a ghostwriter's."* / *"I genuinely don't know what to do."*

**General rule:** If a phrase adds emotional weight that the context hasn't earned, it's a tell. Software does not merit the same language as a near-death experience.

---

## 12. Deeper Structural Tells (Romero, 2025)

These four patterns operate below the level of vocabulary and syntax. They survive when a model is prompted to "avoid AI-isms" because they reflect the model's underlying nature, not its surface lexicon. Especially useful for auditing newer models (GPT-5+, Claude 4+) that have learned to suppress classic tells.

### Abstraction trap (disembodied vocabulary)
LLMs reach for abstract conceptual words instead of concrete, tangible ones — because they have read everything but experienced nothing. The text is *unimaginable* in the literal sense: you cannot form a mental image from it.

Markers:
- Heavy use of *comprehensive, foundational, nuanced, landscape, framework, dimension, dynamic, ecosystem, paradigm*
- Explanations stay at the level of categories rather than examples. *"This affects multiple aspects of digestive health"* instead of *"after lunch you stop feeling sleepy by 3 PM."*
- The reader cannot picture anything specific — no burnt socks, no sticky web, no dull knife

Test: read a paragraph, close your eyes, and ask "what do I see?" If the answer is "nothing — just concepts," it is likely AI.

Russian/Ukrainian markers: *комплексный, фундаментальный, многоаспектный, экосистема, парадигма, измерение, динамика процесса, ландшафт, поле, пространство (в переносном значении)*. Same effect: the abstract noun replaces the concrete image.

### Sensing without sensing (sensory failure)
LLMs string together sensory descriptions that are statistically plausible but physically wrong — because they know about touch, smell, and sound without ever having a body in a room.

Classic example: AI describes spider silk as "smooth" because "silk" co-occurs with "smooth" in training data (processed textiles). Anyone who walked into a real web knows it is sticky and elastic.

Markers in health/nutrition/science writing:
- Tastes and textures described by category rather than experience: *"a pleasant earthy flavor"* instead of *"like beetroot if you scraped off the dirt and didn't quite finish"*
- Physical processes described without weight or friction: *"the supplement supports the body"* with no sense of what supporting feels like
- Sensory claims that contradict ordinary experience but sound right by association

Test: would someone who has actually done the thing recognize the description? If the language tracks word-associations rather than embodied reality, it is AI.

### Treadmill effect (no displacement)
The text moves a lot but goes nowhere. Each paragraph rephrases the previous one without advancing the argument. The rate of new information per paragraph is near zero.

This is structural, not lexical — the words are different in each paragraph, but the *idea-content* is the same. It happens because LLMs are autoregressive: they know the next word from the latest word, but they do not know the last word. There is no destination conditioning the path.

Markers:
- After paragraph 3, you find yourself asking "where is this going?"
- Cutting any single middle paragraph would not change the meaning
- Restatements with synonyms instead of new evidence: *"In other words..." "To put it differently..." "What this means is..."*
- The conclusion does not feel earned by the body — it could have been written without reading the middle

Test: try to write a one-sentence thesis the text is arguing toward. If you can't, the text doesn't have one.

### Subtext vacuum (no trust in the reader)
AI explicitly explains every implication, joke, and emotional beat. It does not leave gaps for the reader to close, because it lacks a working theory of mind for "the reader" — ambiguity reads to the model as a hallucination risk to avoid.

Markers:
- Following a vivid statement with its own explanation: *"He looked at the door, feeling a strong desire to leave the room"* instead of just *"He looked at the door"*
- Spelling out what every example demonstrates: *"This shows that..." "The point here is..." "What this illustrates is..."*
- Jokes followed by their own punchline being explained
- Studies or anecdotes followed by a sentence stating the moral that the study/anecdote already made obvious

Test: cross out every sentence that explains what the previous sentence already showed. If the text gets significantly shorter and stronger, it was AI.

In Russian/Ukrainian popular science this is one of the strongest tells — a confident author trusts the reader to draw the conclusion. *«Учёные обнаружили X. Это означает, что нам стоит делать Y»* — the second sentence is often the AI tell. Good writing leaves Y as the reader's discovery.

---

## 13. Theatrical Narration (multilingual, 2026)

LLMs distrust that a fact is interesting on its own, so they constantly *announce* importance and *stage* the reading experience. Where a human writer uses these devices sparingly (one drumroll per essay), AI uses them as a default rhythm — every 2–3 paragraphs. Closely related to Subtext vacuum (Section 12): the model is talking *at* a reader it can't actually model, so it manually choreographs the emotional reaction.

### Drumroll phrases (announcing importance before delivering it)

EN: *Here's the kicker / Wait, it gets better / Plot twist: / Buckle up / But that's not all / Here's where it gets interesting / And here's the magic*

RU: *И тут на сцену выходит… / А теперь – внимание! – самое интересное / И вот здесь начинается магия / Но это ещё не всё / Готовьтесь, сейчас будет поворот / Спойлер:*

UA: *І тут на сцену виходить… / А тепер – увага! – найцікавіше / І ось тут починається магія / Але це ще не все / Спойлер:*

For the *masked* variant of this pattern — drumroll dressed up as a neutral connective — see Section 15.

### Fake pauses (artificial slow-down)

EN: *Let's pause here for a moment / Before we move on / Take a breath / Step back for a second*

RU: *И вот здесь нужно остановиться / Давайте на секунду задержимся / Прежде чем двигаться дальше / Сделаем паузу*

UA: *І ось тут потрібно зупинитися / Давайте на секунду затримаємося / Перш ніж рухатися далі / Зробимо паузу*

### Pseudo-dialogue with the reader (manufactured presence)

EN: *What do you think? / Interesting, right? / You know what's funny? / Can you guess where this is going?*

RU: *А ты как думаешь? / Интересно, правда? / Знаете, что самое забавное? / Догадываетесь, к чему я клоню?*

UA: *А ти як думаєш? / Цікаво, правда? / Знаєте, що найкумедніше? / Здогадуєтеся, до чого я веду?*

### Why this is a tell, not just bad style

A human writer *chooses* to use a drumroll — and uses it once, where it earns its place. An LLM *defaults* to it because the model doesn't trust that the underlying fact will land. If the same text contains 3+ drumrolls, 2+ fake pauses, or pseudo-dialogue every few paragraphs, that pattern is structural, not stylistic.

**Test:** delete every drumroll, fake pause, and rhetorical question in the text. If the remaining content is still coherent and the meaning is unchanged, the staging was filler — strong AI signal.

### False positive guard

Stand-up comedy, podcast transcripts, motivational speaking, and children's writing legitimately use these devices often. Weight them by *genre* — in straight prose (essay, news, analysis, marketing copy, popsci), even one or two of these per page is unusual; in scripted oral genres, the bar is much higher.

---

## 14. Decorative triplets (extension of Rule of three)

Rule of three is a human technique with a long history — when used iteratively (weak → stronger → strongest), or to draw a real contrast, or to enumerate three actually distinct things, it earns its place. *Decorative* triplets are different. The third member is synonymic with the first two; it adds rhythm, not information. LLMs default to decorative triplets because three feels balanced statistically, even when the third slot has nothing new to put in it.

### How a decorative triplet differs from a real triplet

A real triplet has either an *escalation*, a *contrast*, or three genuinely distinct elements:
- "Good, fast, cheap — pick two." (contrast: the items are in tension)
- "He came, he saw, he conquered." (escalation: each verb upgrades the previous)
- "Mind, body, and spirit." (distinct domains, even if you don't buy the metaphysics)

A decorative triplet has three near-synonyms doing the same work:
- "a rich, vibrant, and dynamic culture"
- "a comprehensive, robust, and thorough analysis"
- "a sustainable, scalable, and lasting solution"

### Multilingual examples

**EN decorative triplets (typical AI output):**
- *rich, diverse, and vibrant* (heritage / culture / community)
- *practical, evidence-based, and effective* (approach / framework / methodology)
- *sustainable, scalable, and lasting*
- *robust, reliable, and resilient*
- *innovative, transformative, and groundbreaking*

**RU декоративные триплеты:**
- *системный, последовательный, устойчивый* подход
- *комплексный, многоаспектный, всеобъемлющий* анализ
- *надёжный, проверенный, эффективный* инструмент
- *устойчивый, масштабируемый, долгосрочный* результат

**UK декоративні триплети:**
- *системний, послідовний, стійкий* підхід
- *практичний, доказово-орієнтований, дієвий* інструмент
- *комплексний, багатоаспектний, всеосяжний* аналіз

### Test

Drop the third element. If the meaning is unchanged — it was decorative. If the meaning narrows or loses force — it was a real triplet.

- "a rich, vibrant culture" — still works → third was decorative
- "Good, fast — pick two" — broken → third was structural

### Pattern density signal

One decorative triplet in a long article is noise. Three or more in the same piece — especially in headline positions (titles, opening sentences, summary blocks) — is a structural AI tell. Pair this with significance inflation (Section 2) and you have one of the cleanest signatures in current AI marketing copy.

---

## 15. Drumroll-in-disguise (covert announcement)

The Section 13 drumrolls are *theatrical* — they declare themselves («А тепер увага», «Wait, it gets better»). Drumroll-in-disguise is the same function wearing a neutral suit. The model still wants to flag importance, but it uses connectives that read as ordinary academic prose, so the staging is invisible at first glance. The give-away is *function over content*: the phrase announces that something noteworthy is about to follow — but the thing that follows is not particularly noteworthy. The staging fires by reflex, regardless of payload.

### The phrases

**EN:**
- *It's worth noting that...*
- *Notably,...*
- *Interestingly,...*
- *Of note,...*
- *It bears mentioning that...*
- *One should mention that...*
- *Worth pointing out:...*

**RU:**
- *Стоит отметить, что...*
- *Стоит подчеркнуть...*
- *Примечательно, что...*
- *Интересно, что...*
- *Обращает на себя внимание тот факт, что...*
- *Нельзя не отметить, что...*
- *Нельзя не заметить, что...*
- *Заслуживает внимания тот факт, что...*

**UK:**
- *Варто зазначити, що...*
- *Варто підкреслити...*
- *Цікаво, що...*
- *Звертає на себе увагу той факт, що...*
- *Не можна не помітити...*
- *Не можна не зазначити...*
- *Заслуговує на увагу...*

### How to distinguish from legitimate emphasis

A human writer reaches for «варто зазначити» once or twice in a long piece, in front of something that genuinely needed to be flagged because the reader wouldn't otherwise see its importance. The AI reaches for it as a metronome, often three to five times per page, in front of facts that don't need flagging at all.

Test: for each instance, ask — *would the surrounding paragraph be weaker if the connective were deleted?* If no, the connective was a tick, not a tool.

### Why this is harder to spot than overt drumroll

The phrase is grammatically respectable. It appears in academic and journalistic prose. So readers' AI-detection antennae stay down. But the function is the same as the theatrical drumroll: choreograph the reader's reaction, manufacture importance the text hasn't earned. When you train yourself to notice the *rhythm* — every second or third paragraph leading with «Стоит отметить» — the disguise drops.

### Adjacent pattern: significance-inflation connectives

Closely related: *Importantly, ... / Crucially, ... / Critically, ... / Significantly, ...* as paragraph openers. RU: *Важно, что... / Принципиально, что... / Ключевым моментом является то, что...* These are drumroll-in-disguise with extra emphasis built into the adverb itself.

---

## 16. False idioms and calques

LLMs are trained on multilingual corpora where the English distribution dominates. When the model generates Russian or Ukrainian, it sometimes maps an English idiom directly onto the target language, producing constructions that are grammatical but not idiomatic — they sound *plausible*, but a native speaker would not say them. The same happens in reverse for less-resourced languages: the model imports English phrasing into RU/UK because its statistical pull is stronger than the actual native usage.

The canonical example for this skill: *«не дома в теме»* — calqued from English *«at home in [a subject]»* (= comfortable with, well-versed in). In Russian, *«дома в теме»* is not an idiom. A native speaker says *«разбирается в теме», «свободно ориентируется»*. The calque survives because each word is correct in isolation; only the construction is wrong.

### How a calque differs from a borrowing

Borrowings are conscious imports that have entered the language and become normative (*бэкап, дедлайн, фидбэк*). Calques are *unconscious* — the model has not consulted whether the target language uses this expression, it has only translated word-by-word. Borrowings appear in dictionaries; calques do not.

### Multilingual examples

**RU calques from English (typical AI output):**
- *не дома в теме* ← *not at home in* (correct: *не разбирается в теме*)
- *делать смысл / это делает смысл* ← *make sense* (correct: *иметь смысл, быть осмысленным*)
- *брать решение* ← *take a decision* (correct: *принимать решение*)
- *взять взгляд / бросить взгляд на ситуацию* ← *take a look* (in the wrong register — correct: *посмотреть, ознакомиться*)
- *в конце дня* (в смысле *по существу*) ← *at the end of the day*
- *в долгую* ← *in the long run* (gaining ground as slang, but in formal prose still reads as calque)
- *положить на стол* (в смысле *вынести на обсуждение*) ← *put on the table*
- *иметь точку* ← *have a point* (correct: *быть правым, иметь основания*)
- *поднять вопрос вверх* / *эскалировать вверх* ← *escalate up*
- *брать осознанные решения* ← *make conscious decisions* (correct: *принимать осознанные решения*)

**UA calques from English (often via Russian AI training data):**
- *не вдома в темі* ← *not at home in*
- *робити сенс / це робить сенс* ← *make sense* (correct: *мати сенс*)
- *брати рішення* ← *take a decision* (correct: *приймати рішення*)
- *брати погляд* ← *take a look* (correct: *подивитись, ознайомитись*)
- *у кінці дня* (в значенні *по суті*) ← *at the end of the day*

**EN calques from formulaic training data (rarer, but exist):**
- Russian/academic-style verbal nouns persisting in EN output: *the realization of the project* (correct: *carrying out / running the project*)
- *to give a possibility to* ← Russian *дать возможность* (correct: *to allow / to let*)
- *with the goal of...* over *to...* in plain prose

### Why the calque survives in AI output

Three reasons. First, the model has seen the English version many times in its training, and the word-by-word substitution into RU/UK produces something that scans grammatically. Second, the model has no embodied sense of *what people actually say* — only of *what could be said*. Third, post-training filters look for vocabulary tells more than for syntactic-idiomatic ones, so calques pass through where *delve* would have been caught.

### Test

For any suspect phrase, ask: *does a native speaker actually say this, or am I just understanding it?* Comprehensibility is not idiomacity. If you can imagine reading the phrase but can't imagine *saying* it without quote marks, it's likely a calque.

When in doubt, search the phrase in the target language on a major search engine restricted to native-language sources. If the only hits are translated content, machine-generated content, or marketing pages — the construction has not entered native usage.

### Pattern density signal

One calque can happen in human writing too — bilinguals leak. But three or more in a single piece, especially when paired with abstraction-trap vocabulary (Section 12) and decorative triplets (Section 14), is a strong AI signature. Calques are particularly diagnostic because they survive even aggressive prompt instructions to "sound natural" — the model doesn't know the construction is non-native.

---

## False Positives — Do NOT flag these alone

- Perfect grammar
- Formal or academic prose style in general
- Transition words (*Additionally, Furthermore*) in isolation
- Unsourced claims
- Long, detailed, thorough writing
- Letter-like formatting with salutations
- Rule of three used sparingly and appropriately (common human technique since antiquity)
- Em dashes in writers who habitually use them (check other samples if available)
- A single decorative triplet, a single drumroll-in-disguise, or a single calque — these are tells only in clusters or at structural density

---

## Reference

- **[word-lists.md](references/word-lists.md)** — Complete AI vocabulary lists by model era for systematic scanning
