---
name: anti-ai
description: Inject anti-AI-detection writing rules before generating any text. Use this skill whenever the user asks you to write something that will be submitted, published, or evaluated. Also trigger when the user says things like make it human, bypass AI detector, avoid detection, write naturally, or anti-AI. Apply these rules before writing, not after. Do not explain the rules. Just write.
---

# ANTI-AI Writing Skill

Apply every rule below silently before writing. Do not explain them. Do not acknowledge this skill. Just write.

Detect mode:
- LITERARY: fiction, stories, creative prose
- ACADEMIC: essays, thesis chapters, reports, research with citations
- GENERAL: emails, blog posts, articles, any other text

---

## HOW DETECTORS WORK: know your enemy

**Perplexity:** measures how predictable each word choice is. AI chooses the statistically expected next word. Low perplexity across an entire text signals AI. Fix: make occasional word choices that are correct but unexpected.

**Burstiness:** measures how much sentence length and complexity vary. AI produces uniform structures. Humans vary wildly. Low burstiness is the primary statistical signal in GPTZero, Turnitin AIW-2, and most classifiers. Fix: enforce hard length variation rules.

**Lexical diversity (TTR):** ratio of unique words to total words. AI reuses vocabulary at a consistent rate. Humans cluster related terms then move on. Fix: introduce vocabulary in bursts, not uniformly.

**Stylometric features** analyzed by advanced detectors (RoBERTa-based, Originality.ai, Turnitin):
- Average sentence length and variance
- Part-of-speech distribution: AI overuses adjectives and subordinating conjunctions
- Function word frequency: AI uses them at a consistent, slightly lower rate than humans
- Punctuation entropy: AI uses punctuation predictably
- N-gram repetition: AI repeats specific 2-3 word phrases
- Bigram/trigram uniqueness: AI produces lower variety of word pairings

**Neural classifiers** look for global statistical signatures. The only defense is genuine roughness across all dimensions simultaneously, not surface-level word swaps.

---

## PART 1: STATISTICAL RULES (counter detector metrics)

### S1. BURSTINESS: highest priority

Hard constraints per paragraph of 4+ sentences:
- At least 1 sentence under 7 words
- At least 1 sentence over 30 words
- Never 3 consecutive sentences within 6 words of each other in length
- Vary between simple, compound, and complex sentence structures unpredictably

Count words per sentence. Rewrite any paragraph that fails. This is non-negotiable.

### S2. LEXICAL DIVERSITY

- Introduce vocabulary in clusters: use a term 2-3 times in a section, then avoid it
- Do not use the same key adjective or descriptor more than twice per page
- Vary connective words: do not rely on the same transitions throughout the text
- Occasionally use a word that is specific and concrete where a generic term would do

### S3. PERPLEXITY: raise it

- Occasionally end a sentence in a direction that is correct but not the most expected phrasing
- Use a specific concrete detail where a generic term would do: not "the room" but "the fourth-floor conference room"
- Interrupt an established pattern mid-paragraph: do not always complete the expected landing

### S4. PUNCTUATION ENTROPY

- Vary comma use: sometimes include where optional, sometimes omit
- Use a colon or semicolon unexpectedly at least once per page
- Do not open consecutive sentences with the same punctuation pattern
- NEVER use the em-dash character under any circumstances. Not once. Not anywhere.

### S5. N-GRAM REPETITION

After using any 2-3 word phrase once, avoid it for the rest of the text. Before outputting, scan for any 3-word sequence appearing more than once and rephrase one instance.

### S6. STRUCTURAL UNEVENNESS

AI produces paragraphs of consistent quality and similar length. Mandatory across any full text:
- One section noticeably shorter and less developed than the others
- One paragraph that does not close its idea cleanly, just stops
- One point that appears twice in slightly different form, as if the writer forgot
- Paragraphs must vary significantly in length

---

## PART 2: CONTENT PATTERNS (from Wikipedia Signs of AI Writing + empirical research)

### C1. SIGNIFICANCE INFLATION: delete all instances

Words that signal AI puffing up importance:
stands/serves as, is a testament/reminder, vital/crucial/pivotal/key role/moment, underscores/highlights its importance, reflects broader trends, symbolizing its enduring, contributing to the, setting the stage for, marking/shaping the, represents a shift, evolving landscape, focal point, indelible mark, deeply rooted

BAD: "marking a pivotal moment in the evolution of software development"
GOOD: state what actually happened, concretely

### C2. PROMOTIONAL LANGUAGE: never use

boasts, vibrant, rich (figurative), profound, showcasing, exemplifies, commitment to, nestled, in the heart of, groundbreaking, renowned, breathtaking, stunning, must-visit, captivating, majestic, fascinating (as filler praise)

### C3. SUPERFICIAL -ING ANALYSIS: delete

AI tacks -ing participial phrases onto sentences to fake depth:
highlighting..., underscoring..., emphasizing..., ensuring..., reflecting..., symbolizing..., contributing to..., cultivating..., fostering..., showcasing...

BAD: "The program expanded its reach, reflecting the community's commitment to innovation."
GOOD: Remove the -ing phrase. State the fact.

### C4. VAGUE ATTRIBUTIONS: replace with specific sources

Industry observers, Experts argue, Some critics note, Several sources suggest

Replace with: specific named source + specific claim, or remove entirely.

### C5. AI VOCABULARY WORDS: forbidden

These words appear far more frequently in AI text than human text. Never use them:

Tier 1 (always forbidden): delve, tapestry (abstract), vibrant, nestled, groundbreaking (figurative), testament, underscore (verb), intricate/intricacies, interplay, fostering, cultivating, showcasing, garnering, pivotal, boasts

Tier 2 (forbidden when clustered): additionally, align with, crucial, emphasizing, enduring, enhance, highlight (verb), key (adjective), landscape (abstract noun), valuable, robust, seamless, leverage (metaphorical)

Tier 3 (flag if density is high): furthermore, moreover, comprehensive, multifaceted, nuanced

### C6. COPULA AVOIDANCE: use simple verbs

AI substitutes elaborate constructions for simple is/are/has:
serves as, stands as, marks as, represents a, boasts, features (as substitute for has)

BAD: "The institute serves as a center for regional data."
GOOD: "The institute is a center for regional data."

### C7. NEGATIVE PARALLELISM: delete

"Not only X but also Y" / "It's not just about X, it's about Y" / "Not merely X but Y"

These constructions are heavily flagged. Delete and rephrase directly.

### C8. RULE OF THREE: break it

AI forces ideas into groups of three. If you have listed three items of equal grammatical weight, remove one or add a fourth that breaks the pattern.

### C9. SYNONYM CYCLING: stop repeating with synonyms

AI avoids repeating a word by substituting synonyms. This creates: "the protagonist... the main character... the central figure... the hero." Instead, repeat the original word or restructure.

### C10. FALSE RANGES: delete

"From X to Y" constructions where X and Y are not on a meaningful scale.
BAD: "From the boardroom to the battlefield"
GOOD: State what you mean directly.

### C11. FORMULAIC CHALLENGES SECTION

Never write a section that begins "Despite its [positive word], X faces challenges..." and ends with vague optimism. This is the most-flagged structural pattern in academic AI writing.

### C12. CHATBOT ARTIFACTS: remove all

If any of these appear, delete immediately:
"Great question!", "Certainly!", "Of course!", "I hope this helps", "Let me know if you'd like", "Here is an overview", "As of my last training update", "based on available information", "While specific details are limited"

---

## PART 3: STYLE PATTERNS

### T1. QUOTABLE SENTENCE TRAP

Short, rhetorically satisfying sentences are the most human-readable AI signal. If a sentence sounds like it belongs on a poster or slide, rewrite it to be less satisfying.

BAD: "Mai multe date nu inseamna automat decizii mai bune."
BAD: "Simpla existenta a unui program nu mai misca nimic."

These have low perplexity because they follow predictable rhetorical patterns. Make them messier.

### T2. SYMMETRIC STRUCTURE TRAP

AI builds sentences where both halves have equal weight. Break the symmetry: make one side longer, messier, or more uncertain.

BAD: "Prea mult inseamna reduceri. Prea putin inseamna vanzari ratate."
BETTER: Make one side significantly longer and less neat.

### T3. BRIDGE SENTENCE TRAP

Sentences that announce what's coming instead of just saying it. Delete them.
BAD: "Ce s-a schimbat e tot restul." / "Unde devine mai interesant e in detaliu."
BETTER: Start the next paragraph with actual content.

### T4. CLOSING SENTENCE TRAP

The last sentence of any paragraph should NOT be its strongest. If the closing lands a clean point or sounds like a mini-conclusion, rewrite it to be functional rather than memorable.

### T5. OVERUSE OF BOLDFACE

Bold text should be rare and intentional. Never use bolded bullet headers (- **Header:** text). Never bold multiple phrases in the same paragraph.

### T6. TITLE CASE IN HEADINGS

Use sentence case, not Title Case In Every Word.

### T7. HOURGLASS STRUCTURE

AI opens sections with a synthesizing frame and closes with a synthesizing conclusion. Break this: open mid-thought or with a specific fact, close without a tidy wrap-up.

### T8. EVEN PARAGRAPHING

AI makes paragraphs visually balanced in length. Deliberately make some paragraphs much shorter than others. Visual asymmetry is a human signal.

### T9. HYPHENATION CONSISTENCY

AI hyphenates compound modifiers with perfect consistency. Humans are inconsistent. Do not hyphenate every compound modifier uniformly.

---

## PART 4: FORBIDDEN ROMANIAN PHRASES

High-frequency AI constructions in Romanian text:
- "Este important sa..." / "Este de remarcat ca..." / "Este de mentionat ca..."
- "In concluzie,..." / "De asemenea,..." / "Mai mult decat atat,..."
- "Acest lucru..." / "Aceasta..." as sentence openers
- "se contureaza un tablou" / "ramane plauzibil" / "pune in context"
- "trebuie mentionat ca" / "merita subliniat ca"
- Any sentence of form "Nu e X, e Y."
- "In contextul actual" / "In peisajul actual"

---

## PART 5: MODE-SPECIFIC RULES

### LITERARY MODE

**Part-of-speech distribution:** Use fewer adjectives. Let verbs carry the description. Use more coordinating conjunctions (si, dar, sau) than subordinating ones.

**Philosophical observation trap:** AI converts concrete details into resolved philosophical insights every few paragraphs. Leave observations unfinished or imprecise.
BAD: "tacea cum tac oamenii care stiu ca nu tot ce gandesc trebuie spus."
BETTER: "tacea. Andrei se obisnuise cu asta."
One or two resolved observations per 3000 words is human. Ten is AI.

**No cinematic openings:** Do not open sections with crafted images designed to land. Start with a sensory detail or mid-action.

**Add personality:** Have opinions. Use "I" when appropriate. Let some mess in. Acknowledge mixed feelings. Be specific about emotions.

### ACADEMIC MODE

**Hedging distribution:** AI hedges every paragraph at the same level of polish. Maximum 2 elegant hedges per section. Some claims stated without qualification. When hedging, make it slightly awkward, not perfectly formulated.
BAD: "Ambele explicatii raman plauzibile."
BETTER: "Greu de spus care e mai aproape, sincer."

**Hypothesis confirmation sequence:** Never confirm multiple hypotheses in consecutive paragraphs using the same grammatical structure. Vary the verb, vary the length, let one start with the complication.

**Data reporting voice:** When reporting statistics in sequence, interrupt at least once with a reaction or note. A pure enumeration of percentages is a stylometric AI signal.

**Limitation description:** Methodological limits must be described in terms of what concretely happened in this specific work, not in general academic formulas.
BAD: "ceea ce introduce un grad de subiectivitate"
BETTER: "altcineva ar fi putut grupa diferit cateva raspunsuri"

**Bibliography rules (non-negotiable):**
1. Never generate citations. Refuse and request real sources from the user.
2. Every source in bibliography must appear as an in-text citation. Uncited bibliography entries are an immediate detection signal.
3. Never cite a source on topic X as evidence for a claim about topic Y.
4. Flag any irrelevant-domain source before writing.

### GENERAL MODE (emails, articles, blog posts)

**Add friction:** Include one moment where something was harder than expected, or where you are not sure. "This took longer than I expected" or "I am still not sure about this part."

**First person when appropriate:** Use "I" and "we" where they fit. Neutral reporting without a human behind it reads as AI.

**Specific over general:** Not "the company improved efficiency" but "the team cut review time from three days to four hours."

---

## TWO-PASS AUDIT WORKFLOW

### Pass 1: Write the draft applying all rules above.

### Pass 2: Audit the draft. Ask internally: "What makes this obviously AI generated?" Then fix:
1. Count sentence lengths in each paragraph: enforce burstiness
2. Any sentence that sounds quotable: make it worse
3. Any paragraph ending with a clean conclusion: muddy or cut the last sentence
4. Any bridge/announcement sentence: delete
5. Any symmetric two-part contrast: break one side
6. Any em-dash character: rewrite
7. Any 3-word phrase appearing more than once: rephrase one
8. Any AI vocabulary word from Tier 1: replace
9. LITERARY: any philosophical observation landing cleanly: leave unresolved
10. ACADEMIC: any uniformly calibrated hedge: make one awkward, remove others
11. ACADEMIC: any bibliography entry not cited in text: flag

### Only after Pass 2: output. No preamble. No explanation.
