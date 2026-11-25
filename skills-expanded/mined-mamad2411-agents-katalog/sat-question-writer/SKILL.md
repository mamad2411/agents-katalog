---
name: sat-question-writer
description: Write entirely original SAT Reading & Writing or Math practice questions from scratch, in authentic College Board style, for Tutormigo. Use this skill whenever the user asks to generate SAT-style practice questions, create new questions for a specific domain/skill, extract a "blueprint" or "topic style" from source material, or build out Tutormigo's own original question bank. Triggers on requests like "write me 3 questions for X skill," "make original SAT questions," "extract the structural pattern from this," or any mention of generating practice content for a specific Digital SAT domain (Information and Ideas, Craft and Structure, Expression of Ideas, Standard English Conventions, Algebra, Advanced Math, Problem-Solving and Data Analysis, Geometry and Trigonometry). This skill NEVER reproduces or closely paraphrases real SAT passages/questions - it only extracts abstract patterns (topic style, sub-skill, distractor logic) and writes wholly new content from them.
---

# SAT Question Writer (Tutormigo)

Writes original, College-Board-style Digital SAT practice questions for Tutormigo's own question bank - never copies or closely paraphrases real exam content. Output is tagged `source: "Tutormigo"` and matches Tutormigo's Supabase `questions` schema, so it drops straight into the same pipeline as the College Board-sourced questions (kept separate via the `source` field - never mix AI-generated and CB-sourced content without that tag).

## Two-stage workflow

This skill runs in two distinct stages. Always keep them separate - don't skip stage 1 and freehand a question, and never let stage 1 output contain actual passage text, exact numbers, or verbatim wording from source material.

### Stage 1: Extract a blueprint (only when the user supplies source material)

If the user gives you real SAT questions/passages to analyze (their own licensed material, something they're allowed to reference), extract ONLY the abstract structural pattern - never copy passages, exact numbers, or wording.

Output a markdown table with these columns:

| Column | What goes here |
|---|---|
| Question ID | Q1, Q2, ... |
| Domain / Skill | e.g. "Information and Ideas / Central Ideas and Details" |
| Sub-Topic | e.g. "identifying the main claim of an academic argument" |
| Topic Style / Setting | e.g. "fictional study on deep-sea marine biology" — describe the *flavor*, not the actual content |
| Logic/Grammar Pattern | The specific mechanism being tested, described abstractly — e.g. "distractor must reverse cause and effect," "requires a colon to introduce an explanation," "discriminant = 0 for exactly one real solution" |

If the user has no source material and just wants questions for a given domain/skill, skip straight to Stage 2 - pull the topic style and logic pattern from the reference tables below instead of extracting one.

### Stage 2: Generate original questions from a blueprint row

For each blueprint row (or each domain/skill the user requests), write a wholly original question. Never look up or reference any real exam question while doing this - invent the specific content from the abstract pattern only.

**Always specify before writing** (ask the user if not given, or use sensible defaults from the reference files):
- How many questions, and for which domain(s)/skill(s)
- Difficulty tier (1=easy, 2=medium, 3=hard) - this affects sentence complexity, distractor subtlety, and (for math) number of solution steps
- Any topic-style constraint (e.g. "no fictional people's names," "science-flavored only")

**Structural discipline (non-negotiable):**
- Use the exact question stem wording specified in `READING.md` or `MATH.md` for that skill - these are College Board's own published stem formats, not invented ones
- Respect the word-count / sentence-count constraints in those files
- **Explicitly construct each distractor with a named error type** (see the distractor pattern tables) - never write a "just kind of wrong" option. AI-written distractors default to either too-obviously-wrong or randomly-wrong; naming the exact logical error (reversed cause/effect, too broad, too narrow, sign error, forgot to square a term, etc.) before writing it is what makes distractors realistic.
- Write a full rationale: why the correct answer is right, and *why each distractor's specific named error* makes it wrong (not just "this is incorrect")

## Scenario boundaries

Use only neutral, classroom-appropriate SAT-style settings. Favor fictional or
general contexts involving literature, history, archaeology, language,
astronomy, ecology, weather, agriculture, materials science, engineering,
manufacturing quality control, retail, personal finance, transportation,
education, sports statistics, museums, surveys, and non-sensitive research.

Do not generate scenarios involving disease, medical treatment, drugs,
weapons, violence, abuse, self-harm, crime, gambling, alcohol, tobacco,
controlled substances, explicit content, partisan politics, or personal
demographic/sensitive-trait claims. If a mathematical or statistical idea could
use one of those settings, replace it with a neutral scientific, academic, or
everyday setting instead.

Keep studies and surveys fictional and general. Do not use real people,
organizations, or news events as the basis for an original question.

## Output format

Return each question as a JSON object matching this shape (ready for Tutormigo's pipeline):

```json
{
  "question_id": "<short random hex id, e.g. python secrets.token_hex(4)>",
  "source": "Tutormigo",
  "domain": "<exact domain name from reference tables>",
  "skill": "<exact skill name from reference tables>",
  "tier": 1,
  "stem": "<passage/prompt text, question stem appended>",
  "blank_index": null,
  "choices": {"A": "...", "B": "...", "C": "...", "D": "..."},
  "correct_answer": "A",
  "rationale": "<full explanation, correct + each distractor's named error>"
}
```

For Standard English Conventions / grammar-style questions with a fill-in-the-blank, set `blank_index` to the character offset of the `______` marker in `stem` (same convention as the rest of Tutormigo's pipeline) instead of `null`.

Present a batch as a JSON array, or as one object per question if the user wants to review them one at a time — ask which they'd prefer for a first batch, then keep the same format for the rest of the session.

## Reference files

Read the one relevant to the domain being written before generating:
- `READING.md` — all R&W skills: exact stems, word counts, and distractor-type tables
- `MATH.md` — all Math domains: stem patterns, common-mistake distractor types, and difficulty-tier guidance

## Quality bar

Before returning a batch, self-check each question against:
1. Does the stem match the exact College Board wording for this skill?
2. Is every distractor traceable to a *named* error type, not just "wrong"?
3. Would someone who has actually seen real SAT questions in this skill recognize the *style* without recognizing any specific content? (style-match, not content-match)
4. Is the rationale specific enough that a tutor could use it verbatim with a student?

If a question fails any of these, rewrite it before including it in the batch - don't hand back weak questions and note the flaw, fix it first.
