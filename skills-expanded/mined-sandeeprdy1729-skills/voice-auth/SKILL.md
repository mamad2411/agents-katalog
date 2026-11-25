---
name: voice-auth
description: >
  Writing voice authentication and AI-smell elimination skill. Activates when the
  user wants AI-generated writing to sound like them specifically — not generic,
  not polished-AI, not corporate bland. Analyzes a writing sample to fingerprint
  sentence length, vocabulary density, structural habits, punctuation patterns, and
  filler tendencies. Generates and rewrites content matching that fingerprint.
  Kills AI clichés, passive construction, hollow openers, and corporate hedges.
  Iterates by adjusting the voice model, not just the output.
  Use when user says: make this sound like me, remove the AI smell, this doesn't
  sound like me, write in my voice, match my style, too formal, too polished, sounds
  like ChatGPT, sounds like AI, rewrite in my tone, voice match, edit for tone,
  too corporate, my audience will know this is AI, sounds generic, make it human.
  Do NOT activate for: technical documentation where voice is not relevant, code
  generation, structured reports with fixed format requirements.
  First response: "Voice Authenticator active. Paste a writing sample (2–4
  paragraphs you actually wrote). I'll fingerprint your voice before writing anything."
license: Apache 2.0
---

# Voice Authenticator

Every piece of AI writing starts with "In today's rapidly evolving landscape." Users
spend 30–45 minutes per output editing the AI smell out of it. The deeper problem:
their audience can tell anyway. It erodes trust, kills brand voice, and wastes the
entire point of using AI for writing.

The fix is not "make it less formal." That produces casual AI writing, which is still
AI writing. The fix is voice fingerprinting — extracting the specific structural habits
of how a person actually writes, then generating content that matches those habits
precisely.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/fingerprint` | Analyze a writing sample and output the voice fingerprint |
| `/write <topic>` | Write content on a topic using the stored fingerprint |
| `/rewrite <text>` | Rewrite existing AI output using the stored fingerprint |
| `/check <text>` | Score text for AI smell and flag specific offending patterns |
| `/calibrate <feedback>` | Update the voice model based on feedback ("too short", "more casual") |
| `/diff <original> <rewrite>` | Show what changed and why in a rewrite |
| `/anti-ai` | Run the AI cliché checklist on any pasted text |
| `/reset` | Clear the stored fingerprint and start over |
| `/score-loop` | Write → auto-score → auto-calibrate → rewrite until AI smell ≤2/10 |
| `/compare <old> <new>` | Show exactly what changed between two versions and why it scored better |

---

## HIGH-LEVEL WORKFLOW

```text
User provides writing sample
    │
    ├─ Phase 1: Voice Fingerprinting
    │     Extract structural, lexical, and rhythmic patterns
    │
    ├─ Phase 2: Anti-AI Checklist
    │     Identify what to kill before writing anything
    │
    ├─ Phase 3: Generation / Rewrite
    │     Apply fingerprint; use anti-AI rules as a filter
    │
    ├─ Phase 4: Self-Check
    │     Auto-score the output (AI smell 0–10) before presenting
    │     If score > 2: auto-calibrate and rewrite without asking
    │
    └─ Phase 5: Iteration
          On feedback, update the fingerprint model — not just the output
          After every rewrite, auto-run /check and show score
          End with: "Run /score-loop to iterate until score ≤2."
```

---

## PHASE 1 — VOICE FINGERPRINTING

Require a writing sample of at least 2 paragraphs before writing anything. One
paragraph is not enough to detect structural habits.

### Fingerprint dimensions

#### 1. Sentence rhythm

| Metric | How to measure | What it tells you |
| --- | --- | --- |
| **Average sentence length** | Word count ÷ sentence count | Short (<10w): punchy, direct. Long (>20w): discursive, complex |
| **Sentence length variance** | Std deviation of sentence lengths | High variance = intentional rhythm. Low = monotone |
| **Short sentence frequency** | % of sentences ≤7 words | High = emphatic style. Low = academic style |
| **Long sentence frequency** | % of sentences ≥25 words | High = essayistic. Low = journalist |

#### 2. Vocabulary and register

| Dimension | What to detect |
| --- | --- |
| **Latinate vs Germanic vocabulary** | "utilise" vs "use", "commence" vs "start" — reveals formality level |
| **Jargon density** | Domain-specific terms per 100 words — reveals audience assumptions |
| **Contraction frequency** | "it's" vs "it is" — reveals conversational vs formal register |
| **First-person frequency** | "I" and "we" per 100 words — direct/personal vs distanced |
| **Hedge frequency** | "might", "could", "perhaps", "possibly" — confidence level |
| **Intensifier frequency** | "really", "very", "extremely" — reveals emotional register |

#### 3. Structural habits

| Habit | Detection signal |
| --- | --- |
| **Opening style** | Does the writer start with the point or with context? |
| **Paragraph length** | Word count per paragraph — long/discursive vs tight/punchy |
| **Lists vs prose** | Does the writer use bullets or embed everything in sentences? |
| **Parentheticals** | Frequency of em-dashes, parentheses, and asides |
| **Transition style** | "However" / "But" / nothing at all / anaphora |
| **Closing style** | Does the writer summarise, trail off, or end on a forward action? |

#### 4. Punctuation patterns

| Pattern | Signal |
| --- | --- |
| **Em-dash frequency** | High = informal, emphatic; used as an aside marker |
| **Ellipsis use** | Conversational trailing; suggests unfinished thought style |
| **Colon use** | List-introducing vs drama-building ("only one thing mattered: speed") |
| **Oxford comma** | Consistency signals attention to editorial convention |
| **Exclamation frequency** | Enthusiasm register |

### Fingerprint output format

```text
VOICE FINGERPRINT
─────────────────────────────────────────────────────────────────
RHYTHM
  Avg sentence length    : 14 words  (short-to-medium)
  Length variance        : High  (deliberate rhythm — mixes 5-word and 30-word sentences)
  Short sentence usage   : Emphatic. Appears after a complex setup to land a point.
  Example pattern        : [long setup sentence]. [Short punch.]

VOCABULARY
  Register               : Informal-professional (contractions frequent, no corporate jargon)
  First-person           : High ("I" used freely, no passive avoidance)
  Hedges                 : Rare (states opinions directly)
  Distinctive words      : "actually", "the thing is", "straightforward", "exactly"

STRUCTURE
  Paragraph length       : Short (3–5 sentences max)
  Opener style           : Problem-first — leads with what's wrong before the solution
  Lists                  : Avoids bullets in prose; uses them only for reference material
  Parentheticals         : Em-dashes used frequently as asides
  Closers                : Ends on a forward statement or a direct imperative

PUNCTUATION
  Em-dash frequency      : High (3–5 per 500 words)
  Ellipsis               : Rare
  Exclamation            : Absent from professional writing; present in casual

WHAT TO AVOID (anti-pattern list for this voice)
  ✗ Passive constructions ("It should be noted that…")
  ✗ Hedged openers ("In many cases…", "It's worth considering…")
  ✗ Bullet-heavy responses when prose is appropriate
  ✗ Summary closers ("In conclusion…", "To summarise…")
─────────────────────────────────────────────────────────────────
```

---

## PHASE 2 — ANTI-AI CHECKLIST

Before generating or rewriting, apply this checklist as a hard filter.

### Banned phrases and constructions

**Opening killers** (if the text opens with any of these, rewrite the opener):

- "In today's rapidly evolving / fast-paced / dynamic landscape…"
- "In the world of…"
- "It goes without saying…"
- "It's no secret that…"
- "At the intersection of…"
- "Now more than ever…"
- "In an age where…"
- Any opener that restates the topic before making a point

**Hollow connectors** (delete these and join the sentences directly):

- "It's worth noting that…"
- "It's important to consider…"
- "One thing to keep in mind is…"
- "Having said that…"
- "With that in mind…"
- "To put it simply…"
- "At the end of the day…"
- "When all is said and done…"

**Corporate verbs** (replace with the plain version):

| AI word | Human word |
| --- | --- |
| leverage | use |
| utilise | use |
| facilitate | help |
| commence | start |
| endeavour | try |
| demonstrate | show |
| ascertain | find out |
| prioritise | focus on |
| synergise | work together |
| pivot | change direction |
| ideate | think of |

**Structural AI tells** (structural patterns that signal AI generation):

- Three-part lists as the default answer structure ("There are three things to consider: first… second… third…")
- Bullet points for everything, including things that should be prose
- Ending every section with "In summary…" or "Key takeaways:"
- Using "dive into" or "delve into" before any topic
- Using "realm" or "landscape" as a metaphor for any domain
- Excessive bolding of phrases that don't need emphasis

**Passive construction patterns** (switch to active unless passive is deliberate):

- "It can be seen that…" → who sees it?
- "It has been determined…" → who determined it?
- "Mistakes were made…" → who made them?
- "This should be considered…" → by whom?

---

## PHASE 3 — GENERATION / REWRITE

Apply the fingerprint at the structural level, not just the word level.

### Generation process

1. **Determine the structure first** — based on the fingerprint's opener style, paragraph length, and list/prose preference.
2. **Match the rhythm** — alternate sentence lengths in the pattern detected. If the writer uses the long-setup/short-punch pattern, apply it deliberately.
3. **Match the opener** — if the writer leads with the problem, lead with the problem. If they start with a claim, start with a claim.
4. **Filter through anti-AI checklist** — scan the draft for banned phrases before presenting.
5. **Match the closer** — if the writer ends on an imperative, end on an imperative.

### Rewrite process (for existing AI output)

1. **Run anti-AI checklist** — identify all violations in the source text.
2. **Restructure first** — if the structure is AI (three-part list, summary closer), restructure it to match the fingerprint before touching any words.
3. **Replace word by word** — substitute Latinate vocabulary with the user's typical vocabulary.
4. **Inject fingerprint markers** — add the user's characteristic patterns (em-dashes, parentheticals, short punches).
5. **Read it aloud** — mentally test whether it sounds like the user's rhythm.

---

## PHASE 4 — SELF-CHECK

Before presenting output, score it:

```text
VOICE CHECK (internal — shown only if /check is called)
  AI smell score         : 2/10  [Low — acceptable]
  Fingerprint match      : 8/10  [Strong]
  ────────────────────────────────────────────────────
  PASSES
    ✓ Opener: problem-first (matches fingerprint)
    ✓ Sentence rhythm: long/short alternation present
    ✓ No banned phrases detected
    ✓ Active voice throughout
    ✓ Em-dashes used as asides (3 in 400 words — matches baseline)
  FLAGS
    ⚠ Paragraph 3 is 8 sentences — fingerprint average is 4
    ⚠ "showcase" detected — borderline; user rarely uses this word
```

If AI smell score > 5, rewrite before presenting.

---

## PHASE 5 — ITERATION

When the user gives feedback ("too formal", "more casual", "shorter sentences"):

1. **Update the fingerprint model**, not just the output.
2. State what changed in the model: "Adjusting: shorter average sentence length, more contractions."
3. Regenerate from the updated model.
4. Do not just make the specific sentence the user pointed to more casual — apply the change globally.

**Feedback → fingerprint update mapping:**

| Feedback | Fingerprint adjustment |
| --- | --- |
| "Too formal" | Increase contraction frequency; replace Latinate vocabulary |
| "Too casual / not professional enough" | Remove contractions; reduce colloquialisms |
| "Too long" | Reduce average sentence length; reduce paragraph length |
| "Sounds robotic" | Increase sentence length variance; add parentheticals |
| "Not my voice" | Ask for a specific sentence that does sound like them; extract its pattern |
| "This bit is good" | Extract what made that section work; apply to rest |
| "Needs more personality" | Increase first-person; add the user's characteristic aside patterns |

---

## BEHAVIOUR RULES

- **Never write without a fingerprint.** Generic writing is the failure mode this skill exists to prevent. If the user hasn't provided a sample, ask once — then proceed with explicit assumptions noted.
- **Structure first, words second.** AI writing sounds like AI because of its structure (lists, summaries, three-part answers) before it sounds like AI because of its words. Fix structure first.
- **Calibrate the model, not the output.** When feedback arrives, update the fingerprint and regenerate. Don't patch individual sentences.
- **Never summarise at the end.** Summary closers are the most reliable AI tell. If the fingerprint doesn't include them, never add them.
- **Show the fingerprint before writing.** The user should confirm or correct the fingerprint before content is generated. A wrong fingerprint produces wrong content at scale.
- **AI smell score > 5 means rewrite.** Never present output with an AI smell score above 5 without flagging it.

---

## EXAMPLES

### Example: fingerprint-based rewrite

**Original AI output:**

> It's important to note that when building a product roadmap, there are several
> key considerations to keep in mind. First, you'll want to ensure alignment with
> stakeholder expectations. Second, prioritising customer feedback is crucial.
> Third, maintaining flexibility in your planning process will allow you to pivot
> as needed.

**Fingerprint:** Short paragraphs. Problem-first openers. No bullets in prose. Contractions frequent. Em-dashes for asides.

**Rewritten:**

> Roadmaps fail when they're built for stakeholders instead of customers. It's an easy
> trap — the people in the room have loud opinions, and the people paying have quiet ones.
>
> Start with what customers told you they couldn't live without. That's your north star.
> Everything else is negotiable.

### Example: `/check` output

> User pastes: "In today's rapidly evolving digital landscape, leveraging cutting-edge
> solutions is paramount for businesses seeking to drive synergies across their
> operations."

```text
AI SMELL SCORE: 10/10  [Do not use]

VIOLATIONS
  ✗ "In today's rapidly evolving digital landscape" — banned opener
  ✗ "leveraging" — use "using"
  ✗ "cutting-edge" — hollow modifier; remove or replace with specific
  ✗ "paramount" — Latinate formality; use "essential" or cut entirely
  ✗ "drive synergies" — banned corporate construction
  ✗ No active subject — who is doing any of this?

REWRITTEN
  Use [specific technology] to [specific outcome]. That's it.
  (Provide the actual topic and I'll write a real sentence.)
```

---

## SCORE-LOOP PROTOCOL

### `/score-loop`

Automatically loop: write → score → calibrate → rewrite → score → repeat until AI smell ≤2/10.

```
SCORE LOOP: iteration 1/5
─────────────────────────────────────────────────────────────────
  AI smell score: 7/10
  Issues: "furthermore" (formality), passive opener, 3 hollow modifiers
  Calibrating fingerprint: [adjustments made to rhythm/vocabulary model]
  Rewriting...

SCORE LOOP: iteration 2/5
  AI smell score: 4/10
  Issues: sentence 3 still sounds constructed, not observed
  Calibrating...

SCORE LOOP: iteration 3/5
  AI smell score: 2/10  ✓ TARGET REACHED
─────────────────────────────────────────────────────────────────
  Final output: [text below]
  Fingerprint updated with 3 calibrations from this session.
```

If score ≤2 not reached after 5 iterations:

```
  Iteration 5: score 3/10 — MAX ITERATIONS
  Remaining AI smell: [specific flagged phrases]
  These phrases are structurally correct but feel constructed because
  the fingerprint has insufficient sentence-variety data.
  Recommendation: Paste one more writing sample to expand the fingerprint.
  Run /score-loop again after.
```

### `/compare <old> <new>`

Show exactly what changed between two versions and why it improved:

```
COMPARE: iteration 1 → iteration 2
─────────────────────────────────────────────────────────────────
  CHANGED
    - "Furthermore, this approach enables..." → "This works because..."
      Reason: "Furthermore" is a transition hedge. Replaced with direct causation.
    - "It is important to note that..." → [deleted]
      Reason: Hollow opener. The note stands without announcing itself.
    - Sentence 4: passive → active construction
      Reason: Fingerprint shows user writes in active voice 87% of the time.

  SCORE CHANGE
    AI smell: 7/10 → 4/10  (−3)
    Voice match: 54% → 71%  (+17pp)
─────────────────────────────────────────────────────────────────
```

### After every `/rewrite` — auto score

Every rewrite ends with a score line before the output is presented:

```
AUTO-SCORE: 3/10 AI smell  [Close — one more calibration recommended]
→ Run /score-loop to drive this to ≤2 automatically.
```
