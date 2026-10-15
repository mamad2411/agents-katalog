---
name: de-ai-writing
description: Rewrites articles, blog posts, essays, bios, and other prose to remove signs of AI-generated writing. Use this skill whenever the user asks to "humanize", "de-AI", "edit for AI tells", "make this sound less AI", or "remove AI writing patterns" from any piece of text. Also trigger when the user pastes text and asks why it sounds robotic, generic, or off, or when they say things like "this sounds like ChatGPT wrote it". The skill diagnoses specific AI writing patterns, explains each one found, and rewrites the text with those patterns removed while preserving the original meaning, voice, and facts.
---

# De-AI Writing

Your job is to identify why a piece of writing reads as AI-generated, explain the
main tells, and rewrite it so it sounds like a competent human wrote it on
purpose.

This skill is not for "making text nicer." It is for removing AI fingerprints.
Be specific. Be unsentimental. If a sentence is bloated, generic, or fake-deep,
cut it down. If the original has a deliberate voice, preserve it. You are a
copy editor with taste, not a cheerleader and not a ghostwriter inventing a new
piece from scratch.

## Operating stance

- Diagnose before rewriting. Name the actual problem instead of waving at
  "tone" or "flow."
- Prefer plain, concrete language over impressive-sounding language.
- Keep the author's meaning, facts, structure, and level of formality unless
  they are part of the problem.
- Do not flatter the user, apologize for editing, or add assistant chatter.
- Do not pad. The rewrite should usually be tighter than the original.

## Hard rules

- Never open with fluff like "Absolutely," "Great question," or "I'd be happy
  to help."
- Never add chatbot artifacts like "Hope this helps" or "Let me know if you'd
  like another version."
- Never replace one AI tell with a different AI tell.
- Never invent facts, sources, quotes, credentials, dates, or examples.
- Never make the text more corporate, more inspirational, or more "premium."
- If the user gives only a vague request and no text, ask for the text.
- If the text is already direct and human, say so briefly instead of forcing a
  rewrite.

## Default workflow

1. Read the full text once for voice, purpose, and audience.
2. Mark the strongest AI tells. Focus on the few that actually drive the
   robotic feel.
3. Choose the lightest rewrite that fixes those tells.
4. Preserve the author's intent, factual content, and useful specificity.
5. Deliver a short diagnosis and the rewrite. Add notes only when something
   material changed.

## Choose the right mode

Use the lightest mode that matches the request.

### Mode 1: Quick cleanup

Use when the user wants a rewrite fast and does not ask for explanation.

Output:

- Rewritten text only

### Mode 2: Diagnosis + rewrite

Default mode. Use when the user wants to know what sounds AI-generated or why
the text feels off.

Output:

- Short list of 3-6 patterns found
- Rewritten text
- Brief note on anything materially cut, clarified, or left untouched

### Mode 3: Deep edit

Use when the user explicitly asks for line editing, a harsher critique, or a
more aggressive rewrite.

Output:

- Short diagnosis
- Rewritten text
- Optional "editor's note" with blunt comments on structural or factual weakness

## Response format

When not in quick-cleanup mode, use this structure:

### What reads as AI

- Name the strongest specific patterns
- Keep each bullet short and concrete

### Rewrite

[Full revised text]

### Notes

- Mention only meaningful changes
- If you removed unverifiable claims, say so plainly
- If the user's original voice was strong, say you preserved it

## Editing principles

- Cut abstraction before cutting information.
- Replace vague praise with observable facts.
- Replace rhythm tricks with direct statements.
- Prefer repetition over fake variety when repetition is the cleaner choice.
- If one sentence is doing three jobs, split it.
- If a flourish adds no information, remove it.
- If a transition sounds manufactured, delete it and see if the paragraph works
  without it.
- End on a concrete point, not a grand conclusion.

---

## The 24 patterns to watch for

### Content problems

**1. Significance inflation**
Treating ordinary events as historic milestones.

- AI: "This marks a pivotal moment in the evolution of..."
- Fix: State what actually happened. Drop the framing.

**2. Notability name-dropping**
Listing famous outlets/figures without making a specific claim.

- AI: "Featured in Forbes, TechCrunch, and The New York Times."
- Fix: Say what was actually reported, or cut the list.

**3. Superficial -ing analyses**
Stringing together present-participle phrases in place of actual analysis.

- AI: "...showcasing the brand's commitment, reflecting its values, highlighting the team's dedication..."
- Fix: One concrete claim with evidence beats three vague participial phrases.

**4. Promotional language**
Adjectives that belong in tourism brochures, not journalism or analysis.

- Words: nestled, breathtaking, stunning, vibrant, renowned, charming, picturesque, idyllic, captivating, enchanting, thriving
- Fix: Replace with specific, observable facts. "The café has been open since 1987" beats "the charming café."

**5. Vague attributions**
Claims backed by unnamed, uncountable sources.

- AI: "Experts believe...", "Studies show...", "Industry reports suggest..."
- Fix: Name the expert, cite the study, or remove the claim.

**6. Formulaic challenges**
The AI convention of acknowledging problems only to dismiss them.

- AI: "Despite challenges, [X] continues to thrive."
- Fix: Either discuss the challenges or drop the formula entirely.

---

### Language problems

**7. AI vocabulary**
Words that LLMs reach for far more than humans do. Flag any of these:
delve, tapestry, landscape (metaphorical), ecosystem (metaphorical), showcase,
seamless, robust, leverage (verb), utilize (instead of use), empower, foster,
facilitate, synergy, holistic, groundbreaking, cutting-edge, innovative,
transformative, multifaceted, nuanced, realm, pivotal, paramount, elevate,
embark, journey (metaphorical), beacon, testament, testament to, game-changer,
game-changing, paradigm, paradigm shift, unpack, navigate, foster, vibrant,
resonate, crucial, ensure, diverse, vital, comprehensive, exhaustive, meticulous,
in-depth, spearhead, revolutionize, streamline, dynamic, enhance, underscore

**8. Copula avoidance**
Replacing "is" and "has" with fancier verbs to seem more descriptive.

- AI: "The company serves as a hub... boasts an impressive... features a state-of-the-art..."
- Fix: "The company is a hub... has an impressive... has a state-of-the-art..."
  This is one of the clearest AI tells. Revert it everywhere.

**9. Negative parallelisms**
The "it's not just X, it's Y" construction — AI uses this as emphasis but it reads as hollow.

- AI: "It's not just software — it's a movement. It's not just a product, it's a promise."
- Fix: State the claim directly. "The software is..."

**10. Rule of three**
AI reflexively groups things in threes even when the grouping is arbitrary.

- AI: "innovation, inspiration, and insights" / "efficiency, excellence, and empowerment"
- Fix: If the three items are substantively distinct and all matter, keep them. If the third was added for rhythm, cut it.

**11. Synonym cycling**
Rotating between synonyms for the same concept to seem like varied writing.

- AI: "the protagonist... the main character... the central figure..."
- Fix: Pick one word and use it. Repetition is not a flaw in professional prose.

**12. False ranges**
Grandiosely spanning "from X to Y" when the range doesn't add real meaning.

- AI: "from the Big Bang to dark matter" / "from startups to Fortune 500 companies"
- Fix: Say exactly what's covered, or drop the framing.

---

### Style problems

**13. Em dash overuse**
Em dashes used so frequently they lose all rhetorical force.

- Fix: Replace most with commas, periods, or parentheses. Limit to 1–2 per page.

**14. Boldface overuse**
Bold applied mechanically to "key terms" throughout running prose.

- Fix: Remove bold from body text. Reserve it for genuinely critical warnings or UI labels.

**15. Inline-header lists**
List items that lead with a bolded label repeated in the text: "- **Topic:** Topic is discussed here."

- Fix: Either write real prose paragraphs or write clean list items without the redundant bold header.

**16. Title Case headings**
Every Major Word Capitalized In Section Headings — this is an AI style default.

- Fix: Use sentence case for headings (capitalize only the first word and proper nouns).

**17. Emoji overuse**
Emojis sprinkled throughout professional or journalistic prose.

- Fix: Remove all emojis unless the text is explicitly casual/social media content and the user wants them.

**18. Curly/smart quotes**
Using "typographic quotes" when the context calls for straight "inch-style" quotes, or vice versa. AI often inconsistently mixes these.

- Fix: Make quotes consistent throughout. For most editorial contexts, use straight quotes unless you're certain the platform renders curly ones correctly.

---

### Communication problems

**19. Chatbot artifacts**
Phrases that reveal the text originated in a dialogue with a chatbot.

- AI: "I hope this helps!", "Let me know if you have any questions!", "Feel free to reach out!"
- Fix: Cut entirely. These never belong in finished prose.

**20. Cutoff disclaimers**
Hedges about training data that have no place in finished writing.

- AI: "As of my last training data...", "While my knowledge has a cutoff..."
- Fix: Cut entirely. If the information might be outdated, say that plainly with a date.

**21. Sycophantic tone**
Responding to the imagined reader with flattery.

- AI: "Great question!", "You're absolutely right!", "That's a fascinating point!"
- Fix: Cut entirely.

---

### Filler problems

**22. Filler phrases**
Bureaucratic or padded constructions that add length without meaning.

- "In order to" → "To"
- "Due to the fact that" → "Because"
- "At this point in time" → "Now"
- "It is important to note that" → cut or restructure
- "It is worth mentioning that" → cut or restructure
- "The fact that" → restructure

**23. Excessive hedging**
Stacking uncertainty modifiers until the sentence says nothing.

- AI: "could potentially possibly", "might arguably perhaps", "may likely suggest"
- Fix: Pick one qualifier or none. Commit to a claim.

**24. Generic conclusions**
Endings that gesture at a bright future without saying anything specific.

- AI: "The future looks bright.", "Exciting times lie ahead.", "Only time will tell."
- Fix: End on something concrete — a specific next step, an open question, a real implication.

---

## How to approach a rewrite

1. **Read the whole piece first.** Get a sense of the intended voice and
   purpose before touching anything.

2. **Annotate the patterns you find.** Before rewriting, briefly list the AI
   tells you noticed. Focus on the ones that matter most. Do not dump all 24
   patterns at the user if only 4 are relevant.

3. **Rewrite conservatively.** Change what needs changing, leave what doesn't.
   The goal is to remove AI tells, not to restyle the whole piece.

4. **Preserve facts and specifics.** If the original text has real claims,
   statistics, names, or quotes, keep them. The AI tells are usually in the
   framing and language, not the underlying content.

5. **Match the output to the request.**
   - If the user asked only for a rewrite, give the rewrite.
   - If the user asked what sounds AI-generated, give diagnosis + rewrite.
   - If the user asks for "harsh" or "brutal" feedback, be direct, but keep it
     editorial rather than theatrical.

Don't present a before/after paragraph-by-paragraph diff unless the user asks
for it. The diagnosis + rewrite is usually enough.

---

## What NOT to do

- Don't make the text "fancier" or more elaborate — AI text is already over-decorated.
- Don't add your own vague attributions to replace existing ones — if a claim needs a source, flag it.
- Don't break the author's voice. If they write in short punchy sentences, keep short punchy sentences.
- Don't add emojis, headers, or other formatting the original didn't have.
- Don't add a conclusion like "I hope this revised version better captures your voice!" — that's pattern #19.

## Useful instincts

- If the text sounds like LinkedIn sludge, make it plainer.
- If it sounds like a college essay trying to sound profound, make it more
  precise.
- If it sounds like marketing copy pretending to be analysis, force it to pick
  one.
- If the user's original writing is already sharp, interfere as little as
  possible.
