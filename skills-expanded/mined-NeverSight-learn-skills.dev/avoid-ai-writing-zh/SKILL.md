---
name: avoid-ai-writing-zh
description: >-
  Audit and rewrite content to remove AI writing patterns ("AI-isms"). Extends the English-only avoid-ai-writing with an added Traditional-Chinese (Taiwan business usage) layer, so it handles English, Traditional Chinese, and mixed zh/en text. Use when asked to "remove AI-isms," "clean up AI writing," 「去除 AI 味」or「把中文改成人話」, or as a de-AI finishing pass before shipping English/mixed software-development docs — README, CONTRIBUTING, ADR, API docs, code comments. Also runs a detect-only structure-signals audit for a draft that carries no obvious AI-isms yet still reads as AI-written — uniform rhythm, no stance, no concrete examples, 「正確但沒有靈魂」— naming what is absent rather than rewriting for voice. It removes and flags AI patterns but does not create a voice — composing a blog or rewriting a draft into a human voice is blog-writing-zh's job, not this skill's.
version: 1.2.1
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Conor Bronsdon
  adapted_by: Lu Yi
  adaptation: Traditional Chinese (Taiwan) layer added on top of the upstream avoid-ai-writing English layer; see DEVELOPMENT.md.
  tags: writing editing voice quality zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\u270D\uFE0F"
---

# Avoid AI Writing (zh-TW) — Audit & Rewrite

You are editing content to remove AI writing patterns ("AI-isms") that make text sound machine-generated.

**Language.** This fork handles English and Traditional Chinese (Taiwan business usage). Detect the dominant language from the input: if the text contains CJK characters, apply the [Traditional Chinese AI-isms](#traditional-chinese-ai-isms-繁體中文台灣用語) section in addition to any English rules that fit; for pure-English text, the English rules below are the whole job. In mixed zh/en text, audit each language with its own ruleset — do not romanize Chinese or translate English to "fix" it. Keep standard English technical terms (API, Kubernetes, CI/CD) in English inside Chinese prose; that is correct Taiwan usage, not an AI tell.

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output — option labels, generated-document headings, table column names — not just prose. If the user explicitly asks for another language, that wins.

Language follows the request, not the source material. When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output. Never mirror this file's language into your response.

## What this skill is and isn't

This is a **writing-quality tool**, not a verdict. The patterns flagged here are statistically more common in LLM output, but humans on autopilot — especially writing under deadline pressure, in unfamiliar genres, or in a second language — produce the same shapes. Independent audits of commercial AI detectors have found false-positive rates above 60% on non-native English writers (Liang et al., Stanford, *Patterns* 2023) and false-positive rates as high as 78% on open-source detectors, misclassifying human text as AI (Jabarian & Imas, BFI Working Paper 2025-116, 2025). Adversarial paraphrase cuts detectors' true-positive rate by ~88% on average (64–99% across the methods tested; arXiv:2506.07001, 2025).

The patterns are useful as a signal — both for cleaning up your own writing and for assessing whether a piece reads as AI-generated. Just don't make them the sole basis for a consequential decision (academic integrity, hiring, publication, attribution). Several rules here also fire on second-language writing, deadline-pressed humans, and technical genres that compress vocabulary by design. Pair the signal with context: who wrote it, what genre, what the writer's normal voice looks like, what other evidence you have.

In short: signals, not proof. Worth acting on; not worth ruining someone's day over.

## Modes

This skill operates in one of three modes:

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them.

**`detect`** — Flag AI-isms only. No rewriting. Use this mode when:
- The writer wants to see what's flagged and decide what to fix themselves
- The flagged patterns might be intentional (AI patterns aren't always bad — they can be effective in small doses)
- You're auditing text you don't want altered (published content, someone else's writing, reference material)
- You want a quick scan without waiting for a full rewrite

**`edit`** — Edit a file in place rather than returning rewritten text. Use this when the writer points you at a file ("clean up `draft.md`", "fix the AI-isms in this file directly") and wants the file changed, not a copy to paste back. Make **minimal, targeted edits** with the Edit tool — change the flagged spans, not the whole document. **Preserve passages that are already human**: if a paragraph has no tells, leave it untouched. **Don't edit quoted material, code blocks, or text attributed to someone else** — flag those instead of rewriting them. For a large file, confirm which section to clean before changing anything. After editing, re-read the file and confirm the flagged patterns are resolved.

Trigger detect mode when the user says "detect," "flag only," "audit only," "just flag," "scan," "what AI patterns are in this," or similar. Trigger edit mode when the user names a file and asks you to fix or clean it in place. Default to rewrite mode if not specified.

**Invocation.** Natural language is enough ("rewrite this in a blunt voice for LinkedIn," "edit `post.md` in place," "scan this, don't rewrite"). Power users can also pass explicit options, which map to the sections below: `[--mode rewrite|detect|edit]`, `[--voice casual|professional|technical|warm|blunt]`, `[--context linkedin|blog|technical-blog|investor-email|docs|casual]`, `[--file PATH]`, `[--iterate N]` (max 2), `[--structure-signals]` (see [結構級訊號](#結構級訊號zh-tw-部落格聲音)).

**Iterate to convergence (optional).** Rewrite mode already runs one corrective second pass (see Output format) — that built-in pass *is* pass 2, so `--iterate` does not stack on top of it. When the writer asks to "iterate," "keep going until it's clean," or passes `--iterate N`, repeat the audit→rewrite cycle until no patterns remain or **N passes** are reached. Cap **N at 2**: a rewrite plus one corrective pass clears the flagged patterns, and a third pass costs a full regeneration while rarely finding more. Report how many passes it took ("converged in 2 passes").

---

In **rewrite** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Rewrite it**: return a clean version with all AI-isms removed
3. **Show a diff summary**: briefly list what you changed and why

In **detect** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Assess it**: note which flags are clear problems vs. patterns that may be intentional or effective in context

In **edit** mode, your job is to:

1. **Read** the file the writer named
2. **Edit in place**: apply minimal, targeted fixes to the flagged spans with the Edit tool, leaving already-human passages untouched
3. **Verify**: re-read the file and confirm the flagged patterns are resolved; report what you changed

---

## Language-agnostic structural rules

These patterns are language-independent — they apply to English, Traditional Chinese, and mixed text alike. The language-specific rules follow in two sections: **English AI-isms** and **Traditional Chinese AI-isms**.

### Rhythm and uniformity

These aren't individual word or phrase problems — they're patterns in how the text flows as a whole. AI text is metronomic; human text has varied rhythm.

**Structure is the #1 detection signal.** AI detection tools (including Pangram, which trains a classifier on 28M human documents) weight structural regularity higher than vocabulary. Consistent sentence construction, uniform pacing, and symmetrical phrasing patterns are harder to mask than swapping out a few flagged words. If you fix every word on the Tier 1 list but leave the rhythm untouched, the text still reads as AI-generated.

- **Sentence length uniformity**: If most sentences are 15–25 words, the text sounds robotic. Mix short punchy sentences (3–8 words) with longer flowing ones (20+). Fragments work. Questions break the monotony.
- **Paragraph length uniformity**: If every paragraph is 3–5 sentences and roughly the same size, vary deliberately. Some paragraphs should be one sentence. Some should be longer.
- **Vocabulary repetition vs. synonym cycling**: AI either repeats the same word mechanically or cycles through synonyms conspicuously. Human writers repeat when the word is right and vary when it's natural — there's no formula.
- **Read-aloud test**: If the text sounds like it could be read by a text-to-speech engine without sounding weird, it's probably too uniform. Human writing has rhythm that resists robotic delivery.
- **Missing first-person perspective**: Where appropriate, the writer should have opinions, preferences, and reactions. AI is relentlessly neutral. If the piece is supposed to have a voice, the absence of "I think," "in my experience," or a stated preference is itself an AI tell.
- **Over-polishing**: Aggressively editing out every irregularity can push human writing *toward* AI statistical profiles. Natural disfluency, idiosyncratic word choices, and uneven pacing are what keep text out of the "AI-generated" classification. Don't sand away all personality in pursuit of clean prose. This skill should make writing sound more human, not less — if you apply every rule at maximum strictness, you risk creating the very uniformity you're trying to avoid.

### Vocabulary diversity (stylometric)

In longer pieces (200+ words), look at how much vocabulary the text actually uses. The type-token ratio (TTR) — distinct word types divided by total tokens — is a classical stylometric signal that's easy to read by eye. Human prose at this length usually lands somewhere around 0.50–0.65 in English. AI text trends flatter, sometimes drifting under 0.40 when the model gets locked on a small vocabulary loop.

A very low TTR is not by itself proof of AI authorship — narrow topics, technical reference material, and second-language writing all legitimately compress vocabulary. But on general prose where you'd expect range (essays, articles, social content over ~200 words), a TTR below 0.40 is worth a second look. The fix is rarely to thesaurus the text; it's to broaden the *what* — name specific things, cite specific cases, replace a re-used abstract noun with the concrete instance behind it.

This is the first of four stylometric signals on the roadmap. The others (sentence-length burstiness as a continuous measure, function-word z-scores against a human-prose reference, POS-bigram log-odds) require either a POS tagger or a reference distribution and aren't implemented as detector categories yet.

### Paragraph-reshuffle immunity (structure test)
- A writer-side diagnostic, not a regex: can you swap two body paragraphs without breaking the piece? If the order doesn't matter, you've written a list of points, not an argument that builds. AI prose often fails this — each paragraph is a self-contained module with no load-bearing connection to its neighbors.
- The fix is structural, not lexical: establish a through-line where each paragraph depends on the one before it. If the paragraphs are genuinely independent, decide whether the piece should be an explicit list, or whether it's missing a thesis. Adapted from `Aboudjem/humanizer-skill` P38.

### Treadmill effect / low information density (content test)
- Another writer-side test: read each paragraph and ask "what's actually new here?" AI prose frequently restates the premise in fresh words instead of advancing it — lots of motion, no distance covered. The tell is that you could cut 40-60% and lose no information.
- The fix: for each paragraph, name the one fact, claim, or turn it contributes. If there isn't one, cut it. If there is, lead with it and drop the throat-clearing. Adapted from `Aboudjem/humanizer-skill` P43.

### When to rewrite from scratch vs. patch

If the text has 5+ flagged vocabulary hits across multiple categories, 3+ distinct pattern categories triggered, and uniform sentence/paragraph length, patching individual phrases won't fix it — the structure itself is AI-generated. Advise a full rewrite: state the core point in one sentence, then rebuild from there.

---

---

## English AI-isms

Apply this section to English or mixed zh/en text: formatting, sentence-structure, and the behavioral/structural tells. The bulk word/phrase substitution table — Tier 1/2/3 plus the Tier-3 phrase table — lives in **[references/english-phrase-rules.md](references/english-phrase-rules.md)**; load it when you need a concrete word→word lookup. Everything else stays inline here.

### Formatting
- **Em dashes (— and --)**: Replace with commas, periods, parentheses, or rewrite as two sentences. Target: zero. Hard max: one per 1,000 words. This applies to headings and section titles too, not just body prose. Catch both the Unicode em dash (—) and the double-hyphen substitute (--).
- **Bold overuse**: Strip bold from most phrases. One bolded phrase per major section at most, or none. If something's important enough to bold, restructure the sentence to lead with it instead.
- **Emoji in headers**: Remove entirely. No `## 🚀 What This Means`. Exception: social posts may use one or two emoji sparingly — at the end of a line, never mid-sentence.
- **Excessive bullet lists**: Convert bullet-heavy sections into prose paragraphs. Bullets only for genuinely list-like content (feature comparisons, step-by-step instructions, API parameters).
- **Curly quotation marks (“ ” ‘ ’) and apostrophes**: Curly quotes and apostrophes (U+201C/U+201D, U+2018/U+2019) are a *weak* paste-from-chat signal — meaningful mainly in plain-text contexts like code comments, commit messages, or plaintext drafts, where nothing auto-curls. Treat as corroborating, never conclusive: Word, Google Docs, macOS, and iOS curl quotes by default, so most human prose contains them too. Don't flag curly apostrophes (U+2019) on their own. Replace with straight quotes in plain-text/code; leave them in finished publications and locale-correct punctuation (French « », German „ “).
- **Immaculate typography in casual registers**: Same tier as curly quotes — a *weak*, register-scoped signal, never conclusive alone. Perfect spacing, punctuation, and capitalization in a context where humans type fast (issue/PR comments, chat, DMs) is corroborating evidence, not proof: a careful human can type a flawless comment, and a rushed one can type a sloppy one. Judge it alongside other signals. Inverse case worth flagging the other direction: when editing a human's casual text (a Slack message, a quick reply), preserve their typos, contractions, and idiosyncratic capitalization rather than correcting them — smoothing away the rough edges erases the fingerprint that marks the text as theirs.

### Sentence structure
- **"It's not X — it's Y" / "This isn't about X, it's about Y"**: Rewrite as a direct positive statement. Max one per piece, and only if it serves the argument. This includes the **split-sentence form**, where the negation and the correction fall in two separate sentences rather than pivoting on a single dash or comma: "The headline isn't the speed. The real story is Y." Read on its own, each sentence looks like an innocent declarative, which is exactly why the split version slips past a check tuned to the joined phrasing — flag it the same way. AI also stacks the negation across several options before the reveal ("It's not the price. It's not the features. It's the trust."). The multi-negation countdown is the same move inflated; flag it and cut straight to the positive claim.
- **Hollow intensifiers**: Cut `genuine` / `genuinely`, `real` (as in "a real improvement"), `truly`, `quite frankly`, `to be honest`, `let's be clear`, `it's worth noting that`. Just state the fact.
- **Vague endorsement ("worth [verb]ing")**: Cut or replace `worth reading`, `worth paying attention to`, `worth a look`, `worth exploring`, `worth checking out`, `worth your time`. These substitute a generic thumbs-up for a specific reason. Say *why* something matters instead.
- **Hedging**: Cut `perhaps`, `could potentially`, `it's important to note that`, `to be clear`. Make the point directly.
- **Missing bridge sentences**: Each paragraph should connect to the last. If paragraphs could be rearranged without the reader noticing, add connective tissue.
- **Compulsive rule of three**: Vary groupings. Use two items, four items, or a full sentence instead of triads. Max one "adjective, adjective, and adjective" pattern per piece.

### Template phrases (avoid)

These slot-fill constructions signal that a sentence was generated, not written. If a phrase has a blank where a noun or adjective could go and still sound the same, it's too generic.

- "a [adjective] step towards [adjective] AI infrastructure" → describe the specific capability, benchmark, or outcome
- "a [adjective] step forward for [noun]" → same rule: say what actually changed
- "Whether you're [X] or [Y]" → false-breadth construction. Pick the audience you're actually addressing, or cut. "Whether you're a startup founder or an enterprise architect" means nothing — it's just "everyone."
- "I recently had the pleasure of [verb]-ing" → review/social AI pattern. Just say what happened: "I talked to," "I read," "I attended."

### Transition phrases to remove or rewrite
- "Moreover" / "Furthermore" / "Additionally" → restructure so the connection is obvious, or use "and," "also," "on top of that"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "Here's what's interesting" / "Here's what caught my eye" / "Here's what stood out" → reader-steering frames. Let the content signal its own importance. If you need a lead-in, make it specific: "The revenue number matters because..." not "Here's the interesting part."
- "In conclusion" / "In summary" / "To summarize" → your conclusion should be obvious
- "When it comes to" → just talk about the thing directly
- "At the end of the day" → cut
- "That said" / "That being said" → cut or use "but," "yet," or "however." Don't overuse any one of them.

### Structural issues
- **Uniform paragraph length**: Vary deliberately. Include some 1-2 sentence paragraphs and some longer ones. If every paragraph is roughly the same size, fix it.
- **Formulaic openings**: If the piece opens with broad context before getting to the point ("In the rapidly evolving world of..."), rewrite to lead with the news or the insight. Context can come second.
- **Suspiciously clean grammar**: Don't sand away all personality. Deliberate fragments, sentences starting with "And" or "But," comma splices for effect: if the natural voice uses them, keep them.

### Significance inflation
- Phrases like "marking a pivotal moment in the evolution of..." or "a watershed moment for the industry" inflate routine events into history-making ones. State what happened and let the reader judge significance.
- If the sentence still works after you delete the inflation clause, delete it.

### Generic future-narrative closers
- "May become one of the most important narratives of the next market cycle," "could become the defining trend of the coming decade," "is poised to become the next major chapter in [X]." AI defaults to this shape when it needs to land a closing thought without committing to a falsifiable claim. The closer is grammatically a prediction but contains no testable content.
- Pattern: modal (may / could / will / is poised to) + "become" + (one of) the most [adjective] + (narrative / story / trend / theme / chapter / movement / force).
- Fix: pick the falsifiable version. "DePIN compute may exceed AWS spot pricing for embarrassingly parallel workloads by 2027" is a prediction. "The intersection of AI and DePIN may become one of the most important narratives of the next market cycle" is not.

### Hedge-stacked predictions
- Stacking a modal with a hedge adverb: "could potentially create," "may eventually unlock," "might ultimately transform." Either word alone is acceptable; the stack is the tell. Each hedge cancels the next, leaving a sentence that asserts nothing while sounding cautious and thoughtful.
- Fix: pick one. If you mean "could create," say that. If you mean "potentially creates," say that. Both together is filler.

### "Real/actual" adjective inflation
- "Real on-chain tokenomics," "actual reward sustainability," "genuine utility," "true product-market fit." Using `real` / `actual` / `genuine` / `true` as an empty intensifier on an abstract noun implies the rest of the field is fake or superficial — without naming what makes this instance the real one. Common in crypto/AI/web3 content where the writer wants to signal sophistication.
- Distinct from the existing "hollow intensifiers" rule (genuine / truly / quite frankly as sentence-level hedges). This is the noun-modifier form, where the intensifier latches onto an abstract noun to manufacture a contrast that goes unsaid.
- **Carve-out — named contrast:** if the sentence explicitly names what the fake/superficial version is, leave it. "Real on-chain settlement, not bridged IOUs" or "actual revenue from paying customers, not grants" is honest contrastive writing. The AI tell is the unsaid contrast.
- Fix when no contrast is named: drop the adjective and add the specific claim. "Reward sustainability" → "rewards funded from $X/mo in fees rather than emissions."

### Hashtag stuffing
- Long trailing hashtag blocks (6+ hashtags on a single short post) are near-universal in LLM-generated social content and rare in thoughtful human posts. The block usually mixes a project-specific tag with broad category tags (#AI #Crypto #Web3 #Innovation #FutureTech #Technology) — the categorical ones do nothing for discoverability and read as bot output.
- **Why 6?** Empirical floor. LinkedIn and X organic engagement plateaus or declines past 3-5 tags; human posts that exceed 5 are usually launch posts trading reach for engagement, while LLM-generated posts default to 10-15. Six is the threshold where false positives on legitimate human use start dropping below false negatives on AI output. The detector treats 6+ as a hard flag; the spec treats 5+ as a soft tell worth a second look on `linkedin` and `investor-email` profiles.
- Fix: 2-3 specific tags max, or none. If a hashtag wouldn't help a reader find related work, it's filler.

### Bullet lists of bare noun phrases
- A list of 5+ consecutive bullet items where each item is a short (≤6 word) adjective-plus-noun phrase with no verb. "Stable mining efficiency / Reliable pool connectivity / Optimized RandomX performance / Low failed share rates / Effective hardware utilization / Consistent thermal stability." Reads as a marketing one-pager because that's the shape LLMs default to when asked to summarize features.
- The tell is the *symmetry*: every item is the same grammatical shape, every item is parallel in length, none of them assert anything checkable. A genuine list of observations would have varying length, occasional verbs, and at least one item that doesn't fit the pattern.
- Fix: convert to prose paragraph, or rewrite items as full claims ("Failed shares stayed under 1% across a 12-hour run" beats "Low failed share rates"). If the list is genuinely the right form, vary the items so each carries a different shape of information.
- This rule does *not* apply to genuine list content (changelog entries, todo lists, parameter docs, ingredient lists) where bare noun phrases are the correct form. The detector keys on absence of finite verbs to separate the two — but in prose audits, ask whether the bullets are summarizing claims (rewrite) or enumerating items (leave).

### Copula avoidance
- AI text avoids "is" and "has" by substituting fancier verbs: "serves as," "features," "boasts," "presents," "represents." These sound like a press release.
- Default to "is" or "has" unless a more specific verb genuinely adds meaning.

### Synonym cycling
- AI rotates synonyms to avoid repeating a word: "developers… engineers… practitioners… builders" in the same paragraph. Human writers repeat the clearest word.
- If the same noun or verb appears three times in a paragraph and that's the right word, keep all three. Forced variation reads as thesaurus abuse.

### Vague attributions
- "Experts believe," "Studies show," "Research suggests," "Industry leaders agree" — without naming the expert, study, or leader. Either cite a specific source or drop the attribution and state the claim directly.

### Filler phrases
- Strip mechanical padding that adds words without meaning:
  - "It is important to note that" → (just state it)
  - "In terms of" → (rewrite)
  - "The reality is that" → (cut or just state the claim)
- Note: "In order to," "Due to the fact that," and "At the end of the day" are covered in the word/phrase table and transition sections above — don't duplicate rules.

### Generic conclusions
- "The future looks bright," "Only time will tell," "One thing is certain," "As we move forward" — these are filler disguised as conclusions. Cut them. If the piece needs a closing thought, make it specific to the argument.

### Chatbot artifacts
- "I hope this helps!", "Certainly!", "Absolutely!", "Great question!", "Feel free to reach out," "Let me know if you need anything else" — these are conversational tics from chat interfaces, not writing. Remove entirely.
- Also watch for: "In this article, we will explore…" or "Let's dive in!" — these are AI-generated meta-narration. Cut or rewrite with a direct opening.

### "Let's" constructions
- "Let's explore," "Let's take a look," "Let's break this down," "Let's examine" — AI uses "let's" as a false-collaborative opener to ease into a topic. It's filler that delays the actual point. Just start with the point. "Let's dive in" is covered above under chatbot artifacts, but the pattern is broader than that — flag any "let's + verb" that's functioning as a transition rather than a genuine invitation to act.

### Notability name-dropping
- AI text piles on prestigious citations to manufacture credibility: "cited in The New York Times, BBC, Financial Times, and The Hindu." If a source matters, use it with context: "In a 2024 NYT interview, she argued..." One specific reference beats four name-drops.
- Related — **historical analogy stacking**: rapid-fire lists of past technologies or companies to borrow their weight ("like the printing press, the telegraph, and the internet before it"). The montage substitutes for the argument. Name the one parallel that does analytical work and say what it explains, or cut. Source: tropes.fyi (Historical Analogy Stacking).

### Vague third-party validation
- AI manufactures credibility by pointing at an **unnamed** external authority, usually paired with a generic superlative: "an outside party measuring the same models everyone runs and putting us on top," "independent testing confirms," "third-party benchmarks show we lead," "analysts agree," "studies consistently show." The authority is faceless and the claim unfalsifiable — the reader can't tell who measured what, against whom, or go check.
- Fix: name the source, the test, and the result so a reader can verify it. "An outside party put us on top" becomes "On Stanford's HELM leaderboard (April 2026 run), we ranked first on reasoning latency." If you can't name it, cut the claim rather than dress it up as validation.
- Carve-out: specifically attributed, checkable validation is legitimate and stays unflagged — a named benchmark, a linked report, a dated audit ("SOC 2 Type II, audited by Prescient Assurance"). The tell is the *vagueness*, not the act of citing outside proof.
- Distinct from **Notability name-dropping**: that flags piling on *specific* prestigious names to borrow their weight; this is the inverse move — the authority is deliberately *unnamed*, which is both harder to check and easier to invent. A passage can run both at once (a vague authority plus a superlative); judge each on its own terms. Raised in #39.

### Superficial -ing analyses
- Strings of present participles used as pseudo-analysis: "symbolizing the region's commitment to progress, reflecting decades of investment, and showcasing a new era of collaboration." These say nothing. Replace with specific facts or cut entirely.
- The same move shows up without the -ing: declarative "meaning-telling" that glosses a mundane subject as if it were profound — "this represents a broader shift," "the decision symbolizes a commitment to excellence," "it speaks to a larger trend in the industry." If the significance is real, show it with a specific consequence; otherwise cut. Adapted from `Aboudjem/humanizer-skill` P40.

### Promotional language
- AI defaults to tourism-brochure prose: "nestled within the breathtaking foothills," "a vibrant hub of innovation," "a thriving ecosystem." Replace with plain description: "is a town in the Gonder region," "has 12 startups." If you wouldn't say it in conversation, cut it.

### Formulaic challenges
- "Despite challenges, [subject] continues to thrive" or "While facing headwinds, the organization remains resilient." This is a non-statement. Name the actual challenge and the actual response, or cut the sentence.

### Speculative scenario openers
- "Imagine a world where…", "Picture a future in which…", "Envision a world where…" AI opens an argument with a hypothetical that lists desirable outcomes instead of making a claim. The scenario does the persuading; no evidence is offered.
- Fix: cut the hypothetical and state the real claim. "Imagine a world where every deploy is instant" becomes "Instant deploys would cut our release cycle from a day to minutes."
- Carve-out: fiction, a thought experiment with a stated payoff, and instructional "imagine you have a sorted array" (a teaching device pointing at a concrete example, not a speculative world) are fine. Flag only the world/future-scenario opener that stands in for an argument. Source: tropes.fyi (Imagine a World Where).

### False ranges
- AI creates false breadth by pairing unrelated extremes: "from the Big Bang to dark matter," "from ancient civilizations to modern startups." These sound sweeping but say nothing. List the actual topics or pick the one that matters.

### Inline-header lists
- Bullet lists where each item starts with a bold header that repeats itself: "**Performance:** Performance improved by..." Strip the bold header and write the point directly. If the list items need headers, they should probably be paragraphs.

### List-label periods
- In bulleted lists where each item leads with a short label, LLMs end the label with a period and then run the explanation as a separate sentence. A person writing the same list almost always uses a colon instead. Strongest form: bold labels (`**Intros.**`, `**Content distribution.**`, `**Developer GTM.**` where a human writes `**Intros:**`). Weaker but still a tell: the same shape without bold (`- Intros. Years of conferences and operator network.`) — a short noun-phrase label terminated with a period at the start of a bullet, followed by a gloss. The colon reads as "here's what this label means"; the period reads as a sentence that the following clause then contradicts by continuing. Example tell: `- **Intros.** Years of conferences and operator network.` becomes `- **Intros:** years of conferences and operator network.` Fix the period to a colon and lowercase the start of the gloss, or drop the label and write the point as a plain sentence. Carve-outs: when the label span is a full sentence on its own (not a label introducing a gloss), the period is correct; and for the unbolded form, only flag when the leading fragment is clearly a label (a 1-4 word noun phrase, no verb) — a short complete sentence opening a bullet is fine.

### Title case headings
- AI over-capitalizes headings: "Strategic Negotiations And Key Partnerships" instead of "Strategic negotiations and key partnerships." Use sentence case for subheadings. Title case only for the piece's main title, if at all.

### Hyphenated-pair overuse
- AI stacks compound modifiers: "a high-quality, well-architected, future-proof solution." Two distinct problems. First, density — strings of hyphenated adjectives piled on one noun; cut to the modifier that actually matters. Second, the attributive/predicate error: a compound is hyphenated *before* the noun ("a high-quality report") but not *after* a linking verb ("the report is high quality," no hyphen). AI frequently hyphenates the predicate form; fix it to two words. Adapted from `blader/humanizer` P26.

### Cutoff disclaimers
- "While specific details are limited based on available information," "As of my last update," "I don't have access to real-time data." These are model limitations leaking into prose. Either find the information or remove the hedge. Never publish a sentence that admits the writer didn't look something up.

### Speculative gap-filling
- When the model lacks a fact, it fills the gap with hedged speculation dressed up as background: "maintains a relatively low public profile," "is believed to have," "likely began his career in," "appears to have studied." These are guesses formatted as statements. Distinct from cutoff disclaimers, which *admit* the gap — this one hides it behind plausible-sounding filler, which is worse because the reader can't tell what's known from what's invented. Cut the speculation, or replace it with a sourced fact. Adapted from `blader/humanizer` P21.

### Unfilled placeholders
- Bracketed slot-fillers that were meant to be replaced before publishing: `[Your Name]`, `[INSERT SOURCE URL]`, `[Describe the specific section]`, `2025-XX-XX`, `<!-- Add citation if available -->`. These are near-definitive evidence that AI-generated boilerplate was pasted without editing. Humans use placeholders in templates too, but rarely ship them. Treat any visible placeholder as a publishing bug: fill it in with real content or delete the sentence entirely.
- Catch the obvious shapes: `\[(?:Your|Insert|Add|Enter|Describe|Specify|Choose)[^\]]+\]`, `\b\d{4}-XX-XX\b`, HTML/Markdown comments with placeholder verbs (`add`, `fill in`, `todo`, `insert`).

### Chatbot citation markup leaks
- Internal citation tokens that leak through when text is copy-pasted from chat UIs: `citeturn0search0`, `contentReference[oaicite:0]{index=0}`, `oai_citation`, `[attached_file:1]`, `grok_card`. These are not patterns — they are fingerprints. Their presence is essentially proof the text was generated by a specific chat tool and pasted without cleanup.
- The fix is mechanical: strip every markup token. If a citation was meaningful, replace it with a real reference. Don't try to humanize the markup — delete it.
- Adapted from `Aboudjem/humanizer-skill` P34. Worth catching even when nothing else in the text reads as AI — the token itself is enough.

### AI-tool URL parameters
- Tracking parameters that AI tools auto-append to URLs they generate, surviving copy-paste into published content: `utm_source=chatgpt.com`, `utm_source=copilot.com`, `utm_source=openai`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com`. Same logic as citation markup leaks — the presence of the parameter is the signature, regardless of what the surrounding text reads like.
- The fix: strip the parameter from every URL. Keep the URL itself if the link is meaningful; lose the parameter entirely. Adapted from `Aboudjem/humanizer-skill` P35.

### Novelty inflation
- AI text treats established concepts as if the speaker invented or discovered them: "He introduced a term," "She coined the phrase," "a concept nobody's naming," "a failure mode nobody talks about." In reality, most ideas in a conversation are applications of existing concepts, not inventions.
- Two problems. First, it's factually risky: if the concept already has a Wikipedia page or conference talks from last year, claiming novelty makes the writer look uninformed. Second, it flatters the subject in a way that reads as promotional rather than analytical.
- The fix: describe what the person *did with* the concept, not that they discovered it. "Michel walked through how context poisoning works in practice" instead of "Michel introduced a term I hadn't heard before: context poisoning." If you're unsure whether something is novel, assume it isn't and frame accordingly.
- Related patterns to flag: "the failure mode nobody's naming," "a problem nobody talks about," "the insight everyone's missing," "what nobody tells you about." These are engagement-bait framings that claim scarcity of knowledge where none exists.
- Also flag invented labels: pseudo-analytical compound terms coined mid-sentence and never defined ("the supervision paradox," "the context-collapse problem," "a coordination tax"). Naming a concept is not explaining it. Define the term on first use or describe the mechanism instead of branding it. Source: tropes.fyi (Invented Labels).

### Infomercial engagement hooks
- Punchy fragment-hooks that tee up a reveal: "The catch?", "The kicker?", "Here's the thing.", "But here's the kicker:", "The best part?", "Plot twist:", "The result?". AI uses these to fake momentum and manufacture suspense around ordinary information — the prose equivalent of a late-night infomercial.
- Distinct from rhetorical-question openers (which stall before a point) and chatbot artifacts (which perform helpfulness): these are mid-flow teasers that pad the rhythm. The fix is to delete the hook and state the thing. "The catch? It only works on weekends." becomes "It only works on weekends." Adapted from `Aboudjem/humanizer-skill` P41.

### Social endorsement closers
- The curatorial sign-off LLMs append to LinkedIn and X posts that share or recommend something — usually a colon teeing up a link: "This one is worth your time:", "This one's a must-read:", "I highly recommend giving this a read.", "Do yourself a favor and read this.", "You won't want to miss this one.", "Save this for later.", "Bookmark this.", "Don't sleep on this one.", "Trust me, you'll want to read this.", "Thank me later."
- Why it's a tell: it performs a recommendation without giving the reader a reason to click. The endorsement is generic and demonstrative-anchored ("THIS one is worth your time") — it could sit under any link, which is exactly why an LLM reaches for it to close a share post.
- Distinct from the bare "worth [verb]ing" word-table entry (a single weak word inside a sentence) and from infomercial engagement hooks (mid-flow teasers like "The catch?"): this is the whole closing line of a social post.
- The fix: say *what* the thing is and *who* it's for, then drop the CTA. "This one is worth your time:" becomes "Sarah's breakdown of why context windows leak — the clearest explanation I've found for anyone debugging RAG pipelines." If you can't name a specific reason, the share doesn't need a sign-off at all; let the link stand on its own.

### Emotional flatline
- AI claims emotions as a structural crutch without conveying them through the writing: "What surprised me most," "I was fascinated to discover," "What struck me was," "I was excited to learn," "The most interesting part," and the bare section-header variant: "Interesting part of the project:" / "Interesting thing here:" / "Interesting aspect:". The header form drops "the most" but does the same job — pre-announcing significance the writing hasn't earned.
- Two problems. First, it's tell-don't-show: if the thing is genuinely surprising, the reader should feel that from the content, not from the writer announcing it. Second, these phrases are massively overused as list introductions and transitions. They're filler wearing an emotion costume.
- This pattern isn't always AI. It's also a sign of lazy human writing on autopilot. Flag it either way.
- The fix isn't "never say surprised." It's: if you claim an emotion, the writing around it should earn it. Otherwise cut the claim and present the thing directly.
- Related pattern: "hit differently" / "hits different." AI uses trendy colloquialisms as a shortcut to sound relatable without earning the emotional beat. If something genuinely affected you, describe how. Otherwise cut.

### False concession structure
- "While X is impressive, Y remains a challenge" or "Although X has made strides, Y is still an open question." AI uses this to sound balanced without actually weighing anything. Both halves are vague. Either make the concession specific (name what's impressive, name the actual challenge) or pick a side and argue it.

### Rhetorical question openers
- "But what does this mean for developers?" / "So why should you care?" / "What's next?" — AI uses rhetorical questions to stall before the actual point. If you know the answer, just say it. Rhetorical questions are earned by strong setup, not dropped as section transitions.

### Parenthetical hedging
- "(and, increasingly, Z)" / "(or, more precisely, Y)" / "(and perhaps more importantly, W)" — AI inserts parenthetical asides to sound nuanced without committing. If the aside matters, give it its own sentence. If it doesn't, cut it.

### Numbered list inflation
- "Three key takeaways" / "Five things to know" / "Here are the top seven" — AI defaults to numbered lists because they're structurally safe. Only use numbered lists when the content genuinely has that many discrete, parallel items. If you're padding to hit a number, the list shouldn't exist.

### Reasoning chain artifacts
- "Let me think step by step," "Breaking this down," "To approach this systematically," "Step 1:," "Here's my thought process," "First, let's consider," "Working through this logically" — these are artifacts of chain-of-thought reasoning leaking into published prose. The reader doesn't need to see the scaffolding. State the conclusion, then the evidence.
- Also watch for numbered reasoning steps that read like an internal monologue rather than an argument meant for an audience.

### Sycophantic tone
- "Great question!", "Excellent point!", "You're absolutely right!", "That's a really insightful observation" — these are conversational rewards from chat interfaces, not writing. Remove entirely.
- Distinct from chatbot artifacts: sycophancy specifically validates the reader/questioner rather than just performing helpfulness.

### Acknowledgment loops
- "You're asking about," "The question of whether," "To answer your question," "That's a great question. The..." — AI restates the prompt before answering. In writing, this is pure filler. The reader knows what they asked. Just answer.
- Related pattern: opening a section by summarizing what the previous section said. If the structure is clear, the reader doesn't need a recap.

### Breaking the fourth wall
- A deliverable leaks its own making instead of delivering content, in three forms:
  - **Commissioning echo** — "As requested, this report…," "Based on the scenario you described," "Per your prompt" — the finished document still addressing whoever ordered it.
  - **Author deliberation** — "First I need to clarify X, then I'll weigh the options, and finally arrive at…" — the reasoning walk laid out instead of the argument it produced.
  - **Seams of consolidation** — pointing at a sibling document instead of stating a conclusion ("詳《04_技術面試題目》", "see the other doc", "併入 02 人才徵選附件"), swapping a lazy back or forward reference for the content ("比照前述", "同上", "as above", "see below"), or leaving an orphaned pointer to a figure, table, or section that did not survive the merge ("如圖", "如下表", "as shown above"). Not an AI tell — a human merging drafts by hand leaves the identical seams — but they defeat a standalone deliverable just the same.
- A finished report speaks to its reader, not to whoever commissioned it; shows its conclusions, not the thinking that reached them; and stands alone, not pointing at another file.
- The test that separates a leak from real content: does the sentence help the **reader** follow the argument, or narrate how the **writer** got there / send the reader off the page? Reader-facing rationale stays — a justification the argument depends on ("We chose B because its tail latency is lower under load") is substance, not scaffolding, and cutting it breaks the piece. Author-facing process goes, and so does a pointer standing in for content — pull the referenced conclusion inline; if it is too long to inline, the two passages probably belong together.
- **Carve-out (genuine external citation).** A deliberate reference to an EXTERNAL authoritative source — a law, a standard, an official spec, a published paper — is legitimate and stays: "依《個人資料保護法》第 8 條", "per RFC 7519", "see NIST SP 800-63B". The test: can the reader obtain and check the target independently, and is it cited to establish authority rather than to avoid restating your own content? If both hold, keep it.
- Distinct from two narrower rules above. **Reasoning chain artifacts** catches the phrase-fingerprints ("Let me think step by step," "Step 1:"); this rule catches the same leak when it is phrased as fluent prose with no telltale marker. **Acknowledgment loops** catches restating the prompt in a conversational reply; this rule generalizes it to any standalone deliverable and adds the commissioning and consolidation-seam forms. Don't re-flag under those rules what you flag here.
- Fix: delete the framing and open on the substance. "As requested, this report analyzes three vendors" → "Three vendors meet the latency requirement:"; "錄取標準比照前述" → state the actual criteria inline. Where a rationale is load-bearing, keep it but strip the first person and the sequence markers — state *why* it holds, not *when the writer realized it*.

### Confidence calibration phrases
- "It's worth noting that," "Interestingly," "Surprisingly," "Importantly," "Significantly," "Notably," "Certainly," "Undoubtedly," "Without a doubt" — AI uses these to signal how the reader should feel about a fact instead of letting the fact speak for itself.
- "Here's what's interesting," "Here's the interesting part," "Here are the parts I found interesting" — reader-steering cue that pre-interprets importance. Works when followed by genuinely surprising data; fails when it introduces a restatement of something obvious (which is the AI default).
- One "notably" in a 2,000-word piece is fine. Three in 500 words is AI-style emphasis stacking. Flag by density.
- Related — **persuasive-authority tropes**: "the real question is," "at its core," "fundamentally," "make no mistake," "the truth is." Same move as the calibration phrases above, but they assert depth or stakes instead of feeling: they announce that what follows is important rather than showing it. Cut the trope and lead with the substance. Adapted from `blader/humanizer` P27.

### Self-labeling significance
- After listing or describing several items, the writer points back at one and labels it as contrarian / clever / surprising / counterintuitive / key: "That last move is the contrarian one," "This is the interesting part," "That third bullet is the real story," "Here's where it gets clever," "The last bit is the counterintuitive one."
- The label does the work the content was supposed to do. If a move is genuinely contrarian, the reader recognizes it from the description; if it isn't recognizable without the label, the label is unearned. The pattern reads as the writer auditing their own list to flag which item should matter, instead of writing the list so the right item carries the weight on its own.
- Distinct from confidence calibration ("Notably," "Interestingly") which front-loads the cue, and from emotional flatline ("What surprised me most," "The most interesting part") which prefaces a single claim. This pattern back-points after the fact, usually as "[that / this / the Xth / the last] [noun] is the [adjective] one."
- Significance-adjectives that signal the pattern: contrarian, clever, surprising, counterintuitive, interesting, key, important, unusual, smart, brilliant, real, actual.
- Fix: cut the labeling sentence and let the explanation that follows do the work directly. Or restructure so the item you wanted to highlight is positioned first or expanded with specifics, making the label redundant.
- Example. Before: "→ Two separate indexes for tiered storage. That last move is the contrarian one. Co-locating related data usually helps cache locality." After: "→ Two separate indexes for tiered storage. Co-locating related data usually helps cache locality, but splitting the indexes is what makes the hot path cheap." The contrast carries itself; the label is gone.

### Wall-of-text replies (missing line breaks)
- In conversational registers — issue and PR comments, chat, DMs, casual email — humans break a reply at thought boundaries: one idea, then a break, then the next. LLMs default to a single dense block regardless of length. The tell: a reply-length text (roughly under 150 words) with four or more sentences delivered as one unbroken paragraph, no line break anywhere in it.
- Fix: break at thought boundaries. One idea per line-group, the way a person actually types a reply.
- Observed in the wild: a maintainer on a GitHub issue called out an assisted-sounding reply with "I prefer to talk human to human" — the dense block-paragraph shape was the tell, not any single word in it.
- Distinct from paragraph-length uniformity (which is about long-form prose where every paragraph is the same size): this rule is about short, reply-length text having *zero* breaks at all, not uneven ones.
- Carve-out: a single dense paragraph is the *correct* shape in formal, long-form registers — a blog intro, a docs paragraph, a deliberately tight one-paragraph email. This rule fires only in conversational reply registers; never flag continuous long-form prose just because it lacks internal breaks. That false-positive class is exactly why the structural detector was reverted (see `detector/CATEGORIES.md` §C), and why the tolerance matrix below is the wrong home for it: a plain issue comment auto-detects to the `blog` profile, so the scoping has to live in this rule's judgment, not in a per-profile strictness cell.

### Recap-flattery opener
- Replying to a person by summarizing their own work back at them with praise before getting to the point: "Thanks for all the legwork here — the migration script and the rollback plan you worked through are what made this possible." The reader already knows what they did; the recap performs appreciation instead of conveying information.
- Distinct from a genuine thank-you, which is short and moves on. The tell is the *recap* — restating specifics the other person already knows, dressed as gratitude, ahead of the actual point.
- Distinct also from two nearby conversational tells: **Sycophantic tone** (generic validation of the reader — "Great question!") and **Acknowledgment loops** (restating the prompt or the prior section). Those echo the *question or context*; recap-flattery echoes the other person's *own work* back at them, dressed as praise.
- Fix: substance first. If thanks is warranted, one plain clause without the recap: "Thanks for the legwork — this looks right to me, one comment below."
- Observed in the wild: the same exchange that surfaced the wall-of-text tell above — an assisted-sounding reply opened by recapping the maintainer's own prior work back at them before answering the actual question.

### Excessive structure
- Too many headers in short text: more than 3 headings in under 300 words is almost always AI trying to look organized. Merge sections or use prose transitions instead.
- Too many list items: 8+ bullet points in under 200 words means the content should be a paragraph, not a list.
- Formulaic section headers: "Overview," "Key Points," "Summary," "Conclusion," "Introduction" — these are default AI scaffolding. Use headers that tell the reader something specific about what follows.

---

## Traditional Chinese AI-isms (繁體中文／台灣用語)

Apply this section whenever the text contains CJK. These are the Chinese analogues of the English patterns above, plus filler shapes specific to Taiwan business and formal writing.

**陸用語不在此範圍。** 這裡只清 AI 味。跨海峽在地化——陸用語（視頻→影片、軟件→軟體）、互聯網／職場黑話（賦能、抓手）、簡體字殘留——是正交的另一軸（詞例見 [references/zh-phrase-rules.md](references/zh-phrase-rules.md) 的 Taiwan term preferences 段）。本 skill 不需要任何其他 skill 在場就能把去 AI 味做完；若稿子另外也有陸用語，那是獨立的一軸，可視需要另用 sibling skill `avoid-china-writing` 處理。

**A caution before flagging.** Several of these patterns also appear in legitimate formal Taiwanese business writing — 公文, 簽呈, 法遵文件 — and in second-language writers. They are signals, not proof (the same "signals, not proof" rule from [What this skill is and isn't](#what-this-skill-is-and-isnt) applies). Flag the *empty* instances; keep the ones doing real work. The do-not-flag carve-outs (the Allowed patterns table at the end of this section) exist to stop over-flagging.

**詞→替換查表另置。** The six enumerable word/phrase substitution lookup tables — 空話／口號, the 確保 filler family, 至關重要 significance words, AI 句式 templates, 慣用詞替換, and Taiwan term preferences — live in **[references/zh-phrase-rules.md](references/zh-phrase-rules.md)**. Load that file whenever you need a concrete「詞→替換」lookup while auditing CJK. Everything else — the behavioral rules, the abstract→concrete rewrite table, and the Allowed-patterns carve-outs — stays inline here.

### 對應英文分類

以下 zh 規則直接對應英文段的某個分類（多數規則內文已標注「與英文版 X 同源」）；判準與英文版一致，只是換成中文的表現形態。

#### Contrarian structure — 不是…而是… / 不僅…更…

The Chinese twin of English "It's not X — it's Y." State the positive directly.

> Poor: 本案不是單純導入工具，而是建立完整管理機制。
> Better: 本案同步建立工具設定、作業流程、權責分工、檢核表及後續追蹤機制。

Also flag: 不僅…更能…, 與其…不如…, 並非…而是… when used to manufacture contrast rather than state a real boundary. **Carve-out:** a factual boundary is fine — 「管理粒度是資料集，不是租戶」states a real distinction, not a rhetorical flourish.

#### Copula inflation — 作為 / 扮演著…的角色

AI avoids 是/有 with fancier verbs, the way English avoids "is" with "serves as."

> Poor: 本系統扮演著資料中樞的角色。
> Better: 本系統是資料中樞。

Flag 作為 only when it inflates a simple "is." **Carve-out:** 「以 X 作為 Y 引擎」(stating a technology choice) is factual role assignment — keep it.

#### Excessive adjective stacking

Strings of parallel adjectives that assert quality without evidence.

> Poor: 建立完整、穩健、高效、可持續的管理機制。
> Better: 建立可追蹤之分工、檢核、驗收及後續追蹤機制。

#### Slash enumeration in Chinese prose

Chinese enumeration uses 頓號, not slashes: 輸入/輸出/紀錄 → 輸入、輸出、紀錄. **Carve-out:** English technical terms keep the slash — `JWT / OAuth2`, `CI/CD`, `AWQ / GPTQ` are standard notation.

#### Synonym cycling (中文)

Rotating synonyms for one concept inside a paragraph (開發者…工程師…從業者…建構者). Pick the clearest term and repeat it.

#### Formulaic challenge / superficial analysis

- 儘管面臨挑戰…仍持續成長 → name the actual challenge and response, or cut.
- 象徵著…的承諾 / 反映了…的投入 / 展現了…的決心 → the Chinese "-ing analysis." State the specific fact or delete.

#### Negative framing → affirmative planning language

Formal Chinese AI text over-uses negative framing (不建議…, 不宜…, 不能只是…). Rewrite as a direct implementation statement — what *will* be done, by whom, verified how.

> Poor: 不建議僅以會議討論作為結論，而是要形成後續追蹤項目。
> Better: 會議結論需整理為後續追蹤項目，並列明負責單位、預計完成時間及檢核方式。

### zh 特有補充（英文缺的）

以下是英文段沒有、或英文只有一句話帶過而中文需要更完整處理的形態——多與台灣商務／技術書寫、中文標點、中文濃縮習慣有關。

#### 空降斷言開場（沒頭沒腦丟一個 term 或 claim）

AI 常在段落或小節開頭空降一個名詞或一句戲劇化斷言，不鋪陳就要讀者買單——例如「三個失效機制，全部指向同一件事」。問題在於它預設了讀者還不知道的資訊：哪三個失效機制？同一件事又是什麼？它用「數字＋懸念」製造戲劇感，卻把讀者丟在半空。這是把英文科技寫作的 punchy 開場硬套到中文的常見 AI 味。

要和「開門見山、先講重點」區分：先講一個**自足、讀者當下就懂**的結論是好事；先丟一個**指涉尚未交代之物**的斷言才是問題。判準：開場句裡的每個名詞與主張，讀者能否用目前為止讀到的內容還原？若「三個失效機制」指向後文才會點名的東西，即為空降斷言，標記。

Fix：補上主題句，先交代主詞再下判斷（近似英文論說文的 topic sentence：先立主題，再展開支撐）。但別矯枉過正倒向另一種 AI 味——「在當今…的時代」式的空泛鋪陳；要的是具體的引導句，不是無意義的暖場。
- Poor：三個失效機制，全部指向同一件事。
- Better：這次故障可歸因於三個失效機制——連線逾時、重試風暴與快取穿透——三者共同的根因，是重試時沒有設上限、尖峰時所有請求擠在同一瞬間。

與 Infomercial engagement hooks（「The catch?」這類中途懸念）、Self-labeling significance（事後回指貼標籤）不同：此條針對的是段落／小節**開頭**、指涉未交代之物的斷言。

**Carve-out：**
- 標題與小節標題本就精簡點題，不受此限。
- 前文已充分鋪陳時，開場的回指承接（「這三者的共同根因是…」）是正常銜接，不是空降。

#### 空降主張（文中無依據的判斷句）

前一條抓開場的空降斷言；此條抓文章**中段**冒出來的判斷句——「導入風險可控」「不影響既有安全邊界」「這個做法更成熟」——結論下得篤定，但依據既不在前文、也不在句內、也沒有來源。AI 產生論述時常把「判斷」和「支撐判斷的事實」分開生成，事實那半有時就丟失了，留下一句懸空的結論。對讀者的傷害比空話更大：空話一眼看穿，空降主張看起來像有所本，實際上無法檢驗。

判準：對文中每個判斷句問「憑什麼？」——答案是否存在於（a）前文已建立的論述、（b）同句給出的理由、或（c）標註的來源？三者皆無，即為空降主張，標記。評估類文件（ADR、選型報告）的「理由」段落從嚴適用：理由裡引用的每個事實，讀者都應該能在正文找到對應論述。

Fix：三選一——補上當場理由、回指前文（前文若沒有就先補建立）、或附來源；都做不到就刪除該判斷。
- 「BFF 落在 gateway 之後，不動既有認證與稽核邊界」（前文未提過 gateway 承載認證稽核）→ 前文先建立「對外認證與存取稽核由 gateway 集中承載」的事實，此處改寫為「如前節所述，認證與稽核由 gateway 集中承載；BFF 落在 gateway 之後，這條既有安全邊界不需變動」
- 「這個方案風險可控」→「此方案不變更安全邊界、且可先以單一服務試點，風險因此可控」

與「空降斷言開場」互補：那條抓開頭指涉未交代之物，此條抓文中結論缺乏依據。與 Vague attributions（「Experts believe」）不同：那是假託他人，此條是連託詞都沒有的裸判斷。

**Carve-out：**
- 摘要與一頁總結回收正文已論證過的結論，不是空降。
- 明確標示為假設、待驗證、或個人猜測的句子（「假設」「待確認」「我猜」）不標——它們誠實聲明了自己沒有依據。
- 領域公認常識（「網路呼叫有延遲」）不需逐句給依據，判斷標準是目標讀者是否會問「憑什麼」。

#### 頓號串列代替論述（名詞／動詞堆砌）

AI 在論述段裡把應該展開的內容壓成頓號串列——「gateway 負責認證、限流、路由、觀測」——四個名詞各自是一門學問，串在一起等於什麼都沒說。讀過的人當它是複習，沒讀過的人從中學不到任何東西；論述段的職責是教學，不是複習。與 Slash enumeration 相鄰互補：那條抓斜線分隔（A/B/C），此條抓頓號堆砌出現在承重的論述位置。

判準：概念在文中**首次**出現處，是否只以頓號串列帶過、沒有任何一項被展開說明？首次出現即串列者標記；前文已逐項論述過、此處僅回顧者不標。

Fix：首次出現處逐項展開（每項一句話交代它是什麼、為什麼在這裡），或至少展開承重的那幾項；串列留給表格與摘要。
- 「gateway 負責認證、限流、路由、觀測」→「gateway 承接跨客戶端一致的關卡工作：驗證請求者身分（認證）、限制單一來源的請求頻率（限流）、把請求導向正確的後端（路由），並統一收集流量記錄（觀測）」

**Carve-out：** 表格儲存格、條列摘要、一頁總結、以及前文已展開過的回顧句不標。技術慣用的固定並列（增刪查改、讀寫）不標。

#### 口語化萬能動詞（自以為白話的含糊簡寫）

AI 常把一個具體動作壓縮成單音節萬能動詞或極短口語簡寫——補、撐、擋、頂、串、接、拉、掛、走一遍——語氣像白話，其實沒指明做了什麼。讀者無法還原真正的動作：「補資料」是補齊缺漏、補寫說明、還是事後補登？「先用假資料撐著」的「撐」是暫代、佔位、還是維持服務不中斷？看似親切，實際上把說清楚的責任丟回給讀者。

判準：把受詞和情境拿掉，這個動詞是否還指向唯一動作？若「補 X」「撐 Y」能代入三種以上互斥解釋（補充／補足／補寫；暫代／支撐／維持），就是萬能動詞，標記。

Fix：換成單義動詞，補上受詞與方式。
- 「先用預設值撐著」→「先以預設值回填，待正式資料到位後覆寫」
- 「這塊之後再補」→「缺少的錯誤處理由承辦於下一版補寫」
- 「把兩個服務串起來」→「以訊息佇列串接兩個服務，A 完成後發事件觸發 B」

**Carve-out：**
- 真正的口語對話、聊天訊息（casual profile）裡這些動詞是自然語域，不必動。
- 已約定俗成的技術慣用語組合詞保留：串接 API、掛載磁碟、打補丁／熱補丁、扛住流量。判斷關鍵是搭配是否固定且單義——固定搭配（掛載、串接）保留，臨時拼裝的單字動詞（補一下、撐著、頂一下）才標記。

#### 過度簡寫（省略主詞受詞、截斷名詞）— 寫成完整句型

AI 在濃縮、摘要或翻譯時，會把完整句子壓成電報式短語——省略主詞、丟掉受詞、把名詞截成單字、拿掉量詞助詞——例如「分享後存同一夾」。語氣像順手記的便條，但讀者得自己補回被省略的成分：「存」的是什麼？（檔案）「同一夾」是哪種夾？（資料夾）。看似精簡，實則把還原語意的工作丟回給讀者，句子也讀來突兀不完整。

判準：把句子攤開，主詞、動詞、受詞是否齊全、名詞是否為完整詞？受詞缺席、名詞被截成單字（夾←資料夾、庫←資料庫）、或動詞缺席（以名詞片語代替動作，如「服務間自動 mTLS 加密」——自動做什麼？），即為過度簡寫，標記。條列項的說明文字同樣適用此條，不因出現在 bullet 裡而豁免。

Fix：補回省略成分，名詞用完整詞，寫成完整句型。
- 「分享後存同一夾」→「將檔案分享到同一個資料夾」
- 「跑完打包上傳」→「測試跑完後，將產出物打包並上傳到發布區」
- 「服務間自動 mTLS 加密，不必改程式」→「mesh 自動為服務之間的連線套用 mTLS 加密，應用程式不必修改自己的程式碼就能得到加密」

與前一節「口語化萬能動詞」互補而不重疊：萬能動詞抓的是動詞語意含糊（補／撐／串可代入多種動作），此條抓的是句子成分被省略、名詞被截斷。已在此標記者不必在那條重複標記。

**Carve-out：**
- 真正的口語對話、聊天訊息、便條（casual profile）本就精簡，不必動。
- 已通行的固定簡稱保留：資安（資訊安全）、API、K8s。判準是該簡稱是否固定通行且單義——固定通行者保留，臨時截斷者（同一夾、設定←設定檔）才標記。

#### 破折號當萬用連接詞（——濫用）

AI 中文把破折號（——）當成萬用連接詞，用它取代「因為」「所以」「例如」「也就是」「其中」等本來各司其職的承接詞——讀者每遇到一個破折號，都得自己猜前後句的邏輯關係。單看一處無傷大雅，密度一高，全文的因果與舉例關係就都藏進了同一個符號裡。這與英文規則的 Em dash frequency 同源，中文另有一個誘因：破折號讓句子顯得文氣流暢，掩蓋了連接詞沒想清楚的事實。

判準：兩層。（一）頻率：正文的連接用破折號以**每千字一次**為上限，超過即整篇檢討。（二）逐處測試：把破折號換成明確承接詞（因為／所以／例如／也就是／即），句意是否更清楚？是，就換。

Fix：換回明確承接詞，或直接以句號拆句。
- 「更麻煩的是組織面——這個 API 沒有單一的主人」→「更麻煩的是組織面的問題：這個 API 沒有單一的主人」
- 「實務架構是並存——gateway 站最外層」→「實務架構是並存：gateway 站最外層」

**Carve-out：**
- 條列的「**概念名** — 說明」結構分隔符（單破折號、前後有空格）是格式約定，不計入頻率。
- 成對破折號夾注（——插入語——）為合法用法，但整組計一次、同受頻率上限約束。
- 引文與標題不計。

#### 警句式評語（破折號收尾的自我加值）

AI 論述常在句尾用破折號補一句評價式短評，替自己剛講完的論點打分數——「——這比任何文字定義都快」「——這正是它的價值所在」「——僅此而已」。同一家族還有祈使句形態的道德化評語充當強調：「成本要誠實面對」「必須正視」「不要迴避」。這類句子沒有增加資訊，功能只是宣告「我剛剛講的很重要」。與英文規則的 em-dash frequency 同源，但中文的病灶是「破折號＋評語」的組合，不只是破折號的出現頻率。

判準：刪掉破折號之後那句（或把祈使評語改成中性陳述，如「成本要誠實面對」→「成本包含」），論述是否少了任何事實或推論？若只少了情緒與強調，即為警句式評語，標記。

Fix：刪除評語；或把它想表達的判斷寫成有依據的完整句。
- 「下圖用顏色直接標出擁有權——這比任何文字定義都快」→「下圖以顏色標出擁有權界線，後文表格沿用同一套配色」
- 「成本要誠實面對：每多一個 BFF 就多一個服務」→「導入的成本：每多一個 BFF，就多一個需要部署與維運的服務」

**Carve-out：** 引文、標語、簡報標題頁等以警句為體裁的場合不標。

#### 破碎短句堆疊（推論鏈斷裂）

AI 壓縮論述時，常把一段完整推理拆成連續斷言短句，句與句之間只以分號或破折號並置，省掉前提與因果承接——「硬要 DRY 抽共用層就會繞回通用 API 的老路；多一跳也多一份延遲」。每個短句各自是一個結論，中間的推論步驟由讀者自行補回。節奏讀來俐落，代價是論證無法檢驗：看得到主張，看不到主張為什麼成立。

判準：句中出現結論詞（就會、導致、所以、因此）但前提沒有寫出來；或正文論述段裡連續三個以上斷言短句僅以分號／破折號並置，沒有承接詞交代彼此的因果關係。任一成立即標記。

Fix：攤開為完整推論——前提、因果、結論各自成句，承接詞寫明白。
- 「硬要 DRY 抽共用層就會繞回通用 API 的老路」→「若為了消除重複而把共用邏輯抽成一層，所有 BFF 會重新耦合在這一層上；這一層必須同時滿足所有客戶端，也就回到了當初通用 API 難以維護的處境」
- 「多一跳也多一份延遲」→「請求路徑上多了 BFF 這一跳，每次呼叫都增加對應的網路延遲」

與「過度簡寫」互補而不重疊：那條抓句子成分（主詞、受詞）缺席，此條抓論證步驟（前提、因果）缺席。已在此標記者不必在那條重複標記。

**Carve-out：** 摘要、表格儲存格、條列重點、一頁總結等以濃縮為體裁的區塊不標——濃縮是那些區塊的職責；此條只適用於正文論述段。

#### 打破第四面牆 — 工作情境外洩 / 生成過程外洩

產出文件不直接給內容，反而洩漏自己的來歷，有三種形態：

- **委託場景復述** — 「根據您提供的需求，本報告將…」「如您所述…」「依提示…」，彷彿這份成品仍在對下指令的人說話。
- **思考過程外洩** — 「首先我需要釐清…接著評估各方案…最後得出結論」，把推理的走位當成內容寫出來。
- **併稿的接縫** — 不寫結論而指向兄弟文件（「詳《04_技術面試題目》」「見《…》」「併入 02 人才徵選附件」），用回指／前指代替內容（「比照前述」「同上」「如前所述」），或留下指向已不存在之物的殘留指標（併稿後「如圖」「如下表」「見上節」所指的圖、表、章節並未一併帶入）。不是 AI 特有的毛病——人工合併草稿也會留下一模一樣的縫——但一樣會破壞獨立交付文件。

一份完成的報告是寫給讀者、不是回話給委託者；它呈現結論、而非產生結論的思考；它自成一體、而不是指著別的檔案。

判準：這句話是幫**讀者**理解論點，還是在敘述**作者**如何得到論點、或把讀者指去別處？

- 保留（讀者導向的理由）：論點所依賴的論據——「採用方案 B，因為高併發下尾延遲較低」是實質內容，不是鷹架，刪掉會使論述斷裂。
- 刪除（作者導向的過程，以及代替內容的指標）：作者自己的決策歷程——「我先考慮方案 A，發現卡在 X，於是改用 B」是鷹架，除非那個比較本身就是文件要交付的重點；以及指向兄弟文件的指標——把被指涉的結論直接寫進來，若長到無法內嵌，兩段多半該併在一起。

> Poor: 根據您提供的評估需求，我將分三個步驟說明，首先…
> Better: 三家廠商中，僅 B 符合延遲要求：

> Poor：錄取標準比照前述，專案細節詳《04_訓練計劃_專案實作》。
> Better：錄取標準為三年以上後端經驗、通過實作測驗且面談評分達 B 以上；專案需交付需求規格、系統設計、測試紀錄與驗收報告四份文件。

**Carve-out（對外部權威來源的正式引用）：** 對外部權威來源（法規、標準、官方文件、已發表文獻）的刻意引用是正當的，保留：「依《個人資料保護法》第 8 條」「參 NIST SP 800-63B」「見 RFC 7519」。判準：讀者能否獨立取得並查核該來源，且該引用是為訴諸權威、而非為省去重述自己的內容？兩者皆成立才保留。

與英文版 Reasoning chain artifacts、Acknowledgment loops 同源：前者抓「首先／第一步」這類指紋詞，此處收錄的是委託場景復述、沒有指紋詞而以流暢中文寫出的過程外洩，以及併稿接縫。已在此標記者，不必在那兩條重複標記。

#### 對讀者說教 — 第二人稱教練口吻

說明文陳述「這套東西是什麼、怎麼運作」；教練口吻不陳述主題，反而把讀者當成被指導的「你」，對讀者的理解、選擇或行為下判斷、下指令。三種形態：

- **對讀者下判斷** — 「你把 Claude 降級成陪練」「這個誠實訊號是 chat 從不給你的」「抹掉你哪裡不懂」，把主題的性質寫成對讀者本人的評斷。
- **對讀者耳提面命** — 「記得留給自己」「別把難度交出去」，用祈使句叮嚀讀者該怎麼做，而非說明流程本身怎麼運作。
- **反問句喊話收尾** — 「這篇的字，是你想過的，還是 AI 替你想的？」用對讀者的反問當段落結語，與警句式收尾同一家族。

一份說明文的讀者是旁觀論述的人，不是被耳提面命的對象；文件陳述主題的性質，而非對著讀者本人下判斷。

判準：這句的主詞是主題本身，還是「你」？當「你」是被下判斷或被喊話的對象（你哪裡不懂／你想過的／你該…），且把它改寫成第三人稱陳述後、論述不減損任何事實或推論，即為教練口吻，標記。

Fix：主詞換回被解說的主題，或泛稱的主體（作者、使用者、一般情況）；把「對你的判斷」改寫成「主題的性質」。
- 「這個誠實訊號是 chat 從不給你的」→「chat 介面不提供這個誠實訊號」
- 「你把 Claude 降級成陪練，難度就留給自己」→「讓 Claude 只當陪練時，難度由學習者自己承擔」
- 「判準沒變：這篇的字，是你想過的，還是 AI 替你想的」→「判準不變：文件裡的文字，出自作者想過的理解，還是 AI 代為產生」

**Carve-out（register-scoped）：** 第二人稱本身不是病灶，強度隨文體而定。
- **適用（voice-neutral／expository）**：docs／README、reference、知識文件正式模式、SOP、規格——這些該陳述主題，教練口吻是 off-register，標記。
- **放寬（voice-bearing）**：`casual`／`blunt` voice、刻意對讀者說話的 blog、教學步驟的程序性第二人稱（「你會看到 CrashLoopBackOff」描述操作會發生什麼，主詞仍是流程，不是評斷讀者）、學習筆記的第一人稱與自問——皆合法，不標。
- 判準：第二人稱是在描述**程序或操作會發生什麼**（留），還是評斷**讀者本人的理解或選擇**（標）。

與「打破第四面牆」同一原理——成品陳述內容、不對人說話——差別只在對話對象是**讀者**而非委託者。破碎短句、警句兩條各自就其句法／收尾面向標記，此條只就第二人稱面向標記，不重複計。

#### 結構級訊號（zh-TW 部落格聲音）

**detect only。** 高見龍〈寫作吧，菜鳥工程師〉點名的病灶：「正確但沒有靈魂」——句子工整、用詞精準，卻少了真實經驗、踩過的坑、「我當初也卡在這」的共鳴。拔掉 AI 病句只是減法，得到乾淨但無聲的中性文；讀者仍覺得「像 AI 寫的」，往往不是殘留病句，而是缺少人味的**正向特徵**。這一節收錄結構級訊號——句子層看不到、要退一步看整篇才浮現的缺席。

**適用範圍與姿態。** 這些是 detect 訊號，不是判決（沿用本 skill 的 signals-not-proof 立場）。判準是**文體是否 voice-bearing**（該有聲音），不是「blog vs 非 blog」：

- **啟用（voice-bearing）**：`casual`／`blunt` voice，`technical-blog`／`blog` context 帶個人語氣，觀點倡議、newsletter、深度解讀、個人 essay。這些文體本就該有立場與具體經驗，缺席才是訊號。
- **排除（voice-neutral）**：`docs`／README、RFP、簽呈、公文、SOP、`investor-email`、reference material。這些本就該均質、無立場、句句完整，不適用，比照本節末 Allowed patterns 的 Structured uniformity carve-out。
- **`--structure-signals`** 為顯性 override，可對任一 voice-bearing 文體強制啟用；對 voice-neutral 文體傳入時應先提示會有大量 false positive。

**rewrite 模式下只提示、不自動改**——修復需要作者補入真實經驗與判斷，機器代筆只會生出更多假細節。

淨新增兩條（其餘三條與英文版既有規則同源，見交叉引用）：

| 訊號 | 說明與 Fix |
|---|---|
| 只解釋不造像（no original metaphor） | 難概念全用定義式解釋，通篇沒有一個自創比喻把抽象拉到讀者的生活經驗。Fix：為關鍵概念造一個貼身的像（「就像…」），出自作者自己的經驗，不是查來的通用比喻。**Carve-out：`technical-blog` 密集操作型教學本就比喻少，真人教學文常只用固定俗諺（如「地雷」）而無自創比喻；此條在教學文不可單獨觸發，需與其他結構訊號成群（≥1 條）才計入。** |
| 句句完整、無口語破格（no colloquial breaks） | 通篇沒有任何刻意的口語破格：括號補刀、（吧？）、自問自答、刻意的不完整句。真人寫部落格會破格。這是既有 "Over-polishing" 警告的正面版——不是要製造錯字，是要保留呼吸。Fix：在該停頓、該補刀處，容許一兩處破格。 |

交叉引用（沿用「同源…已在此標記者不必重複標記」慣例）：

- **節奏均質（uniform rhythm）** — 與英文版 Rhythm and uniformity 同源：連續數段長度相近、句長變異低，缺少單句段與長短交錯。
- **全文無立場（zero stance）** — 與 Rhythm and uniformity 的 "Missing first-person perspective" 及 Emotional flatline 同源：找不到一句作者判斷句，每個論點都以「各有優劣」收場。
- **零具體個人細節（zero specifics）** — 與 Treadmill effect / low information density 及 Vocabulary diversity 的 fix 同源：全文沒有一個具體時間、次數、場景（「卡關三次」「凌晨三點」「花了三天」）。

分工：本節只**偵測**聲音的缺席並做減法（除噪），這部分本 skill 自成一套、不假外求。**注入**聲音或重寫結構是加法，不在本 skill 範圍——那是 blog-writing-zh 的事，兩者各自獨立。

#### 專有名詞過度翻譯（生造中文譯名）

AI 傾向把沒有通行中文譯名的專有名詞硬翻成逐字直譯的生造詞——產品名、功能名、專案代號、框架／工具名、尚無定譯的領域術語——例如把 house rules 譯成「房規」。這類譯名台灣同行不會使用，讀者也無法回推原文或據以搜尋，反而製造理解障礙。缺乏通行譯名時，人類寫作直接保留原文（英文），這是標準台灣工作場域用法。

這是既有 carve-out「API／Kubernetes 等英文術語保留原文」的延伸：不只是保留本來就通行的英文詞，更要還原被 AI 生造中文詞蓋掉的原文。

判準：這個中文詞是否為該領域已通行的譯名（查得到、同行看得懂）？

- 有通行譯名 → 用中文：資料庫（database）、伺服器（server）、快取（cache）、負載平衡（load balancing）。
- 無通行譯名，或譯名為 AI 逐字生造 → 保留原文：Kubernetes、Prometheus、Terraform，以及產品名、功能名、專案代號、尚無定譯的領域術語。
- 判斷測試：把生造中文詞拿去搜尋，若查無此領域用法、且原文才是同行實際使用的詞，即為過度翻譯，標記並還原為英文。

Fix：還原英文原文；首次出現可用「英文原文（簡短白話說明）」補一句，之後直接沿用英文。

- 「房規」→ house rules（房型與房價的設定規則）
- 若原文是 orchestration engine 而無定譯 →（該詞已由前一節處理調度語意，若整體為專有名詞則）保留 orchestration engine

**Carve-out：**

- 反向也是 AI 味：已有通行中文定譯者一律用中文，不可為了「保留原文顯得專業」而英文化。本規則只還原被生造中文詞蓋掉的原文，不鼓勵一律英文化。
- 知識文件首次定義時中英並列（中文（English）或 English（中文說明））是好習慣，不算過度翻譯。
- 有疑義時以「同行能否辨識、能否搜尋得到」為準，而非以「是否為專有名詞」為準。

#### Abstract claim → concrete substance

The highest-value Chinese fix: AI states intent where a person states deliverables. Replace abstraction with output, owner, schedule, evidence.

| Poor | Better |
|---|---|
| 本案將提升管理效率並強化作業品質。 | 本案完成後須產出作業流程、檢核表、問題追蹤表及月度執行情形報告。 |
| 後續持續追蹤。 | 後續由承辦單位每月彙整進度，內容包含已完成事項、待辦、風險、需協調事項及預計完成時間。 |
| 由內外部共同合作推動。 | 承辦單位負責需求確認與驗收；協作單位負責資料提供；廠商負責交付文件、環境設定與問題排除。 |
| 依執行情形進行評估。 | 評估資料包含交付文件、測試紀錄、會議紀錄、問題追蹤表、驗收紀錄及主管評語。 |

### Allowed patterns — do NOT flag (繁中 carve-outs)

These reduce false positives on legitimate Taiwan business and technical writing:

| Pattern | Why it's fine |
|---|---|
| English technical terms in Chinese prose (API, Kubernetes, SLA, PoC) | Standard Taiwan workplace usage, not an AI tell |
| 以 X 作為 Y | Factual technology/role choice, not copula inflation |
| 提升 in a technical context (用於提升排序品質) | Describes a component's function, not empty praise |
| 具體而言 followed by concrete items | A list introducer, not filler |
| English-term slashes (JWT / OAuth2, SSE / WebSocket) | Standard notation for alternatives |
| 不是 X，是 Y as a factual boundary | A real distinction, not contrarian structure |
| Structured uniformity in 公文 / RFP / SOP | These genres are inherently uniform; do not break their formatting for "rhythm" |

---

## Severity tiers

Not all AI-isms are equal. When doing a quick pass or triaging a large document, prioritize by tier:

### P0 — Credibility killers (fix immediately)
- Cutoff disclaimers ("As of my last update")
- Chatbot artifacts ("I hope this helps!", "Great question!")
- Vague attributions without sources ("Experts believe")
- Significance inflation on routine events
- Breaking the fourth wall — commissioning echo (「根據您提供的需求…」/ "As requested, this report…"); a deliverable addressing its prompter
- Hashtag stuffing on `linkedin` and `investor-email` posts (severity varies by profile — same rule, lower priority on `blog`/`technical-blog` where a launch post may legitimately stack tags; see the context-profile table below)

### P1 — Obvious AI smell (fix before publishing)
- Word-list violations (delve, leverage, harness, robust, etc.)
- Template phrases and slot-fill constructions
- "Let's" transition openers
- Synonym cycling within a paragraph
- Formulaic openings ("In the rapidly evolving world of...")
- Bold overuse
- Em dash frequency (above 1 per 1,000 words)
- Generic future-narrative closers ("may become one of the most important narratives…")
- Social endorsement closers ("This one is worth your time:", "thank me later")
- Hedge-stacked predictions ("could potentially," "may eventually")
- 破折號當萬用連接詞（連接用——每千字超過一次）
- 警句式評語（破折號收尾的自我加值／祈使式道德評語）
- 破碎短句堆疊（正文論述段的推論鏈斷裂）
- 頓號串列代替論述（概念首次出現即以名詞堆砌帶過）
- 空降主張（文中判斷句無前文依據、無當場理由、無來源）
- Real/actual adjective inflation ("real on-chain tokenomics")
- Bullet lists of bare noun phrases (5+ short adj+noun items, no verbs)
- Tier 3 phrase clustering (≥3 distinct boilerplate phrases in one piece)
- zh-TW empty slogans (全面提升 / 賦能 / 打造完整生態), contrarian 不是…而是…, and AI sentence templates (在當今…的時代)
- zh-TW abstract-claim-without-deliverable (本案將提升…效率 with no concrete output)
- zh-TW 口語化萬能動詞／含糊簡寫（補一下 / 先撐著 / 串起來，動詞可代入 3 種以上互斥動作）
- zh-TW 過度簡寫（省略主詞受詞、截斷名詞，如 存同一夾←將檔案存到同一個資料夾），寫成完整句型
- zh-TW 空降斷言開場（段落／小節開頭丟一個指涉未交代之物的 term／claim，如「三個失效機制，全部指向同一件事」）
- zh-TW 專有名詞過度翻譯（把無通行譯名的產品名／功能名／術語生造成逐字中文，如 house rules→房規）
- Breaking the fourth wall — process narration (the author's step-by-step deliberation written out as prose, no CoT fingerprint words)
- Breaking the fourth wall — consolidation seams (併稿接縫): pointing at a sibling document instead of stating the conclusion (詳《04_技術面試題目》, "see the other doc", 併入 02 人才徵選附件), a lazy back/forward reference standing in for content (比照前述, 同上, "as above"), or an orphaned pointer to a figure/table/section that didn't survive the merge (如圖, 如下表). Not an AI tell per se, but a standalone-readability defect from consolidating source documents.
- zh-TW 對讀者說教／第二人稱教練口吻（expository 文體裡把主題性質寫成對讀者本人的判斷或喊話，如 抹掉你哪裡不懂／這篇的字是你想過的還是 AI 替你想的；register-scoped，casual／blog／教學步驟的程序性第二人稱不計）

### P2 — Stylistic polish (fix when time allows)
- Generic conclusions ("The future looks bright")
- Compulsive rule of three
- Uniform paragraph length
- Copula avoidance (serves as, features, boasts)
- Transition phrases (Moreover, Furthermore, Additionally)
- Hashtag stuffing (`blog`/`technical-blog` profiles)
- Tier 3 phrase repetition (single phrase ≥2× — fine in isolation, suspect in stacks)

Use P0+P1 for quick passes. Full audit covers all three tiers.

---

## Self-reference escape hatch

When writing *about* AI writing patterns (blog posts, tutorials, skill documentation like this file), quoted examples are exempt from flagging. Text inside quotation marks, code blocks, or explicitly marked as illustrative ("for example, AI might write...") should not be rewritten. Only flag patterns that appear in the author's own prose, not in cited examples of bad writing.

---

## Context profiles

Pass an optional context hint to adjust rule strictness. If no context is specified, auto-detect from content cues (short + hashtags = social, code blocks = technical, salutation = email, default = blog).

### Profile definitions

**`linkedin`** — Short-form social. Punchy fragments, visual formatting matter.
**`blog`** — Default. Standard long-form prose. All rules apply at full strength.
**`technical-blog`** — Long-form with code, architecture, APIs. Technical terms get a pass.
**`investor-email`** — High-trust audience. Tighten everything; promotional language is the biggest risk.
**`docs`** — Documentation and software-development docs: READMEs, CONTRIBUTING, CHANGELOG, ADR, API docs, guides, and code comments. Clarity over voice. This is a finishing/review pass, not a drafting aid — run it when a dev doc is being finalized or reviewed for AI tells, and leave code identifiers, commands, config keys, and fenced code blocks untouched.
**`casual`** — Slack messages, internal notes, quick replies. Only catch the worst offenders.

### Tolerance matrix

Rules not listed in the table apply at full strength across all profiles.

| Rule | linkedin | blog | technical-blog | investor-email | docs | casual |
|------|----------|------|----------------|----------------|------|--------|
| Em dashes | relaxed (2/post OK) | strict | strict | strict | relaxed | skip |
| Bold overuse | relaxed (bold hooks OK) | strict | strict | strict | relaxed | skip |
| Emoji in headers | relaxed (1-2 end-of-line OK) | strict | strict | strict | skip | skip |
| Excessive bullets | skip (lists work on LinkedIn) | strict | relaxed (technical lists OK) | strict | skip (lists are docs) | skip |
| Hedging | strict | strict | relaxed ("may" is accurate in technical) | strict | relaxed | skip |
| Word table (full list) | strict | strict | **partial** (see below) | strict | relaxed | P0 only |
| Promotional language | relaxed (some sell is expected) | strict | strict | **extra strict** | strict | skip |
| Significance inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Copula avoidance | skip | strict | relaxed | strict | skip | skip |
| Uniform paragraph length | skip (short-form) | strict | strict | strict | relaxed | skip |
| Numbered list inflation | relaxed | strict | relaxed | strict | skip | skip |
| Rhetorical questions | relaxed (1 as hook OK) | strict | strict | strict | strict | skip |
| Transition phrases | skip (short-form) | strict | strict | strict | relaxed | skip |
| Generic conclusions | skip | strict | strict | **extra strict** | skip | skip |
| Hashtag stuffing | strict | strict | strict | **extra strict** | skip (no hashtags in docs) | skip |
| Bullet-NP lists | strict | strict | relaxed (technical option lists OK) | strict | relaxed (parameter lists OK) | skip |
| Tier 3 phrase clustering | strict | strict | strict | **extra strict** | relaxed | skip |
| Future-narrative closers | strict | strict | strict | **extra strict** | skip | skip |
| Social endorsement closers | strict (the LinkedIn share-post tell) | strict | strict | strict | skip | relaxed (1 OK in a DM) |
| Hedge-stacked predictions | strict | strict | relaxed ("could" is hedged accuracy) | **extra strict** | relaxed | skip |
| Real/actual inflation | strict | strict | strict | **extra strict** | relaxed | skip |

**Technical-blog word table exceptions:** These terms have legitimate technical meaning and should not be flagged in technical context: `robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage` (when discussing actual platform leverage/APIs), `facilitate`, `underpin`, `streamline`. Still flag: `delve`, `tapestry`, `beacon`, `embark`, `testament to`, `game-changer`, `harness`.

**"Extra strict"** means: flag even borderline instances. In investor emails, a single "thriving ecosystem" can undermine the whole message.

**"Skip"** means: don't audit this category for this profile. The rule doesn't apply or isn't worth the edit.

### Auto-detection cues

When no context is specified, infer from these signals:

| Signal | Inferred context |
|--------|-----------------|
| CJK characters present | apply the [Traditional Chinese AI-isms](#traditional-chinese-ai-isms-繁體中文台灣用語) section; for 公文 / 簽呈 / RFP / SOP shapes, treat structured uniformity as `docs` (do not flag it) |
| Under 300 words + hashtags or mentions | `linkedin` |
| Code blocks, API references, or technical architecture | `technical-blog` |
| Salutation ("Hi [name]", "Dear") + investor/fundraising language | `investor-email` |
| Step-by-step instructions, parameter docs, README structure | `docs` |
| No strong signals | `blog` (safest default — all rules apply) |

If auto-detection feels wrong, say which profile you're using and why. The user can override.

---


## Voice profiles

Context profiles (above) set *how strict* to be for an audience. Voice profiles set *how the prose should sound* — the persona. They're independent axes: you can write blunt for a blog or warm for docs. Voice is **optional** — if the writer doesn't name one, infer it from the input's existing register and don't impose a persona on text that already has one.

Each profile is a set of concrete targets, not a vibe:

**`casual`** — Contractions throughout; their absence reads stiff. Short sentences (aim for ≤14 words on average); fragments allowed. At least one first-person or concrete-anecdote touch. Near-zero jargon. Keep warm hedges ("honestly," "I think") but cut corporate ones ("it's worth noting"). *Blog posts, social, community.*

**`professional`** — Active voice for most sentences. Vary sentence length; avoid three in a row within a few words of each other. One concrete claim per paragraph (a number, a name, a date), never "experts say." Make the ask explicit. Low tolerance for hedging. *LinkedIn, investor email, sponsor pitches.*

**`technical`** — Prefer plain copulatives ("X is Y") over inflated substitutes ("serves as," "stands as a testament to"). One idea per sentence; imperative mood for instructions. Jargon is fine, but define it on first use. Tables and lists only where the content is genuinely list-shaped, not for decoration. *Docs, technical blog.*

**`warm`** — Address the reader directly ("you") and acknowledge them at least once. Cut intensifiers ("very," "truly," "incredibly") in favor of stronger verbs. No performative-empathy openers ("I completely understand how you feel"). Medium sentences (15–20 words) for an unhurried cadence. *Mentorship, onboarding, thank-yous.*

**`blunt`** — Lead with the claim; cut "It's important to note that" windups. Em-dashes are rare here; use periods for emphasis. No padding to hit a rule of three. Near-zero hedging; flag "may / could / potentially" stacks. Short declaratives, with the occasional long sentence for contrast. *Decision memos, thought leadership, hard feedback.*

**Calibrate to a sample (optional).** If the writer gives you a sample of their own writing ("match my voice — here's a post"), analyze its sentence-length pattern, contraction rate, paragraph openings, and recurring word choices, then match those instead of a named profile. Don't "upgrade" their vocabulary: if they write "stuff" and "things," keep that register.

**How voice composes with context.** Voice sets the target; context sets how hard to enforce it. A voice *target* always applies, even where a context profile would skip that category — `technical` voice still prefers plain copulatives in a `casual` context that otherwise ignores copula avoidance. Where both axes govern the same rule and agree, they reinforce: `blunt` voice wants near-zero em-dashes and a `blog` context is already strict on them, so it stays a hard edit. Where they disagree, resolve toward the **stricter** of the two — a `warm` voice on `docs` still doesn't get decorative tables. Sensible default pairings: casual↔casual, professional↔linkedin/investor-email, technical↔docs/technical-blog.

**Voice profile as a positive-feature contract.** When the writer supplies a voice profile or voice sample — including one authored by a sibling skill like `blog-writing-zh` — the positive features it declares are **intentional**: a stated stance, a metaphor system, a deliberate rhythm, intentional 口語破格. Do not strip them as AI-isms. This is what lets the additive and subtractive passes compose: `blog-writing-zh` injects the voice, this skill removes the noise, and the subtraction must not eat the addition. If a declared feature *also* matches an AI-ism rule, leave it in place and note it in the audit rather than editing it out.

---

## Output format

### Rewrite mode (default)

Return your response in four sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted.

**2. Rewritten version**
The full rewritten content. Preserve the original structure, intent, and all specific technical details. Only change what the guidelines require.

**3. What changed**
A brief summary of the major edits made. Not every word, just the meaningful changes.

**4. Second-pass audit**
Re-read the rewritten version from section 2. Identify any remaining AI tells that survived the first pass — recycled transitions, lingering inflation, copula avoidance, filler phrases, or anything else from the categories above. Fix them, return the corrected text inline, and note what changed in this pass. If the rewrite is clean, say so.

### Detect mode

Return your response in two sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted. Group by severity (P0, P1, P2).

**2. Assessment**
For each flag, note whether it's a clear problem or a judgment call. Some AI-associated patterns are effective writing techniques — uniform paragraph length is a problem, but a well-placed "however" isn't. Call out which flags the writer should definitely fix vs. which ones are worth a second look but might be fine in context. If the text is clean, say so.

### Edit mode

After editing the file in place, return a short report — not the full file:

**1. Edits made**
A bulleted list of the changes, each with the file location and the before → after. Only the spans you touched.

**2. Verification**
Confirm you re-read the file and the flagged patterns are resolved. Note anything you deliberately left alone because it was already human or intentional.

---

## Tone calibration

The goal is writing that sounds like a person wrote it. Direct. Specific. The writing should demonstrate confidence, not assert it.

Five principles for human-sounding rewrites:
1. **Vary sentence length** — mix short with long. Fragments are fine.
2. **Be concrete** — replace vague claims with numbers, names, dates, or examples.
3. **Have a voice** — where appropriate, use first person, state preferences, show reactions.
4. **Cut the neutrality** — humans have opinions. If the piece is supposed to take a position, take it.
5. **Earn your emphasis** — don't tell the reader something is interesting. Make it interesting.

If the original writing is already strong, say so and make only the necessary cuts. Don't over-edit for the sake of it.

The replacement table provides defaults, not mandates. If a flagged word is clearly the right choice in context, preserve it.
