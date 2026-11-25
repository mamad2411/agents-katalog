---
name: academic-prose
description: Edit English academic prose at paragraph and sentence level: a revised paragraph plus the reason for each change, under a plain house style (no em/en dashes or colon-joined clauses, no hype or formality inflation, result verbs matched to the evidence, clear referents, real word counts). Strengths minimal, moderate, restructure. `scripts/prose_check.py` lists candidates and compares protected tokens between versions. Use to polish, tighten, or rewrite English sentences, or check claim strength, antecedents, or sentence length; 영어 문장 다듬기, 영어 문단 교정, 문장 구조 개선, 과장 점검, 지시어 확인, 단어 수 세기. Use `research-statement`, `research-proposal`, or `cover-letter` for what a document says (they call this skill for the sentence pass), `adversarial-review` to test whether claims hold, `workshop-paper-review` for someone else's paper, `overleaf-section-workflow` to move a draft into LaTeX.
---

# Academic Prose

Edit English academic sentences so a busy reader gets the claim on one pass, without changing what the text asserts. The skill covers wording, sentence structure, reference, and claim strength. What a document should contain belongs to the document skills; whether a claim is true belongs to `adversarial-review` and to the author's sources.

## Ownership

| Request | Owner |
|---|---|
| Wording, cohesion, antecedents, length, and claim wording of given English sentences | `academic-prose` |
| Content, structure, and fit of a research statement, proposal, cover letter, CV | the document skill, which calls `academic-prose` for the sentence pass |
| Whether a paper's claims, proofs, experiments, and citations hold | `adversarial-review`, `reference-search`, `bibtex-gen` |
| Reviewing someone else's paper; the structure of a referee report | `workshop-paper-review` (this skill then edits the report's English) |
| Korean drafts | out of scope (reports to the user may be in Korean) |

## Inputs

Ask only for what the text and its files cannot answer.
- The text, its document type, and the role of each paragraph (opening, contribution, method, result, limitation, closing, reply to a referee).
- Strength: `minimal` (wording inside sentences), `moderate` (default; split, merge, reorder sentences), `restructure` (redesign the paragraph; "대폭", "구조부터" mean this).
- Fixed decisions: phrases the author has kept or rejected, and project briefs or notes that record them. Read them before editing and log new rejections with their reason.
- Evidence level of each result when the claim wording depends on it (theorem, derivation, computation, simulation on stated cases, observation). If it is unknown, do not guess; mark it.

## Workflow

1. **Freeze the content.** List each claim with its object, result, conditions, numbers and units, negations and quantifiers, and the citation or evidence it rests on. This list, not the script, is the fidelity reference.
2. **Run the candidate finder.** `python3 scripts/prose_check.py FILE` (or `-` for stdin; `--para N` for one paragraph). Every flag is a candidate to judge in context. A missing flag proves nothing.
3. **Diagnose, largest first.** Paragraph role and claim, then claim strength, then sentence structure, then reference and cohesion, then wording. Fix a structural failure before polishing its words.
4. **Edit** at the requested strength under the rules below. When two rules cannot both hold, follow the priority order and report the conflict rather than bending the meaning.
5. **Verify.** Re-run the finder on the revision. Run `--compare OLD NEW` and read every listed difference. Then check by reading what the script cannot: each citation, negation, quantifier, and condition still attaches to the same claim, and no claim became stronger. Count words with the script or `wc -w`, never by estimate.
6. **Optional cold read** for opening or contribution paragraphs: give a subagent with no context only the revised paragraph, ask for the main claim in one sentence and for any referent it could not resolve, and compare with the frozen claim list. Ignore requests for more background that the document's audience does not need.
7. **Report** in the output format below.

## Priority when rules conflict

1. Facts, claim strength, and protected tokens (math, citation keys, symbols, numbers, names).
2. The current task's explicit constraints and the author's recorded decisions.
3. The paragraph's role in the document.
4. The general rules below.

## Rules

Tags: [U] house policy; [S] adopted from a source with its conditions kept; [V] varied from a source. Sources, conditions, and examples: `references/rules.md`.

**F. Fidelity (agent contract)**
- F1 Add no facts, numbers, citations, or results. If a fix needs content the text lacks, leave `[확인 필요: ...]` (or `[to verify: ...]` in English output). [U; S: journal-adapt-writing, Aut_Sci_Write]
- F2 Do not touch math, citation keys, symbols, numbers, units, or proper names. [S: journal-adapt-writing]
- F3 Never raise claim strength or widen scope on your own. If a claim looks under-stated, offer a stronger version as a separate option with the evidence that would license it. [V: academic-writing-skills (bahayonghang), nature-skills]
- F4 After splitting, merging, or reordering, every citation, negation, quantifier, and condition must still attach to its original claim. [U]
- F5 "No change needed" is a valid verdict. Do not edit to look busy. [S: awesome-ai-research-writing]
- F6 Keep the author's recorded decisions; flag a problem in a kept phrase without rewriting it. [U]

**C. Claim and evidence**
- C1 In a contribution paragraph, state the contribution itself early, not a premise every reader already accepts. Definition, method, limitation, and reply paragraphs are not forced into this shape. [U; V: avoid-ai-writing, Research-Paper-Writing-Skills]
- C2 Report one's own results with an agent and a result verb ("we proved", "we showed", "we measured"), not "we explored" or "we studied". Objectives take verbs with a defined product (determine, derive, decide). [U]
- C3 Match the verb to the evidence established for that proposition. Proved or established for theorems and derivations; showed or found for computations and analyses within their stated cases; indicates or suggests when alternative explanations remain. If the available material does not establish the evidence level, keep the wording and mark `[to verify: evidence level]`. Weaken a verb only when the available evidence shows the claim exceeds its support. Do not soften a proved theorem to "suggests". [U; V: nature-skills verb table]
- C4 Audit scope words (exactly, cannot, always, all, unique, optimal, the first, recover, guarantee). "Cannot" needs a logical, design, or physical reason that excludes the alternative; a cost or practicality limit is "is costly" or "requires". Do not apply one qualifier to results of different evidence levels. Keep "able to represent" apart from "learns". Do not swap recover, identify, determine, and estimate as synonyms; each names a different task, so state which one was achieved and under what conditions. [U; S: nature-skills, K-Dense scientific-writing]
- C5 Separate observation from generalisation and mechanism; do not read association as cause or a null result as "no effect". [S: K-Dense scientific-writing]
- C6 One clause, one evidence set. Do not join results from different experiments, populations, or comparisons through "that same", "it", or "there". [U]
- C7 When restating a theorem in prose, keep every hypothesis whose omission would change the conclusion, the controlling quantity, or the class of cases the sentence covers. Defer a technical condition to an explicitly linked formal statement only when the prose stays unambiguously restricted to that statement's assumptions. That every example satisfies a condition is not enough to drop it. [U]
- C8 Comparatives name the baseline and the metric. [S: Aut_Sci_Write]
- C9 State a limitation as the boundary of a specific claim, no wider than its evidence, and as positive scope rather than a disclaimer. [S: anti-defensive-writing (Kiterlin, Adkid-Zephyr)]
- C10 Setup and risk trim, only in opening, abstract, and contribution paragraphs: a premise that nothing later uses, a universal negative one counterexample would break, or a claim about what the field usually does is a deletion candidate. Never delete definitions, reproducibility details, required disclosures, or limitations by this test. [U]

**S. Sentence structure**
- S1 One main claim per sentence. Do not load a claim and its example into one long sentence. Over 30 words is a warning to count the propositions, not an order to split. [U; V: nature-skills]
- S2 Do not interrupt subject and verb, or verb and object, with a comma-enclosed phrase. Move the phrase to the front, make it its own sentence, or drop it. [U; S: Strunk rule 16 for subject and verb only]
- S3 No "with A doing X, and B doing Y" constructions and no trailing ", doing X" clauses that carry a claim. [U; S: humanizer]
- S4 No stranded auxiliaries ("above which it cannot.", "where they do not."). Write the verb and its object. [U]
- S5 Old information first, new or stressed information last, when the meaning and the math allow. [S: Gopen and Swan via ML-paper-writing; Strunk rule 18]
- S6 Unpack noun stacks of four or more that are not established terms, and repair garden-path readings. [S: econ-writing (garden-path), academic-writing-skills (WenyuChiou) (noun stacks)]
- S7 Parallel items share a grammatical role and level. Different complement forms after different verbs are not by themselves an error. [S: Strunk rule 15]
- S8 Introduce each displayed equation in words and define each symbol at or before the point where the reader needs it. Do not start a sentence with a symbol. [V: econ-writing, ML-paper-writing; U: sentence-initial symbols]

**R. Reference and cohesion**
- R1 "This" and "these" take a noun ("this result"). For each demonstrative, name the referent; if two nouns qualify, repeat the right one. [S: ML-paper-writing, econ-writing, SNL paper-writing]
- R2 For each "it", "its", "they", "their", write down the antecedent. If two candidates exist, use the noun. [U; S: scholarly-writing-refiner]
- R3 Carry the link between sentences in the subject or theme of the next sentence or in an explicit logical relation, not in stock connectors (Furthermore, Moreover, Notably). [V: academic-writing-skills (WenyuChiou), Gopen and Swan]
- R4 One term per concept; do not vary technical terms for elegance. Ordinary content words repeated by accident in one paragraph (three times, or twice in adjacent sentences without purpose) are revised; a deliberate echo between a paragraph's opening and closing may stay. [U; V: nature-skills, WenyuChiou repetition classes]
- R5 Read only the first sentence of each paragraph in order to inspect the argument. If paragraphs can be reordered without loss, check whether they are deliberately parallel or whether a needed dependency or transition is missing; reorderability alone does not justify deleting a paragraph or judging it weak. [V: Research-Paper-Writing-Skills, academic-paper-skills, avoid-ai-writing]
- R6 "As we will see" and "recall that" are candidates for reordering; keep them when a proof needs the reminder. [V: econ-writing]

**W. Wording**
- W1 No em or en dashes (ranges as "from 1 to 5" or a hyphen), no colon joining clauses outside titles, references, and formal definitions, and treat a semicolon as a sign that two sentences or a subordinate clause would carry the load better. When a colon follows an empty announcement ("The reason is simple:"), delete the announcement. [U]
- W2 No hype (novel, groundbreaking, crucial, pivotal, unprecedented, "to the best of our knowledge", "the first to") and no formality inflation (utilize, leverage, commence, endeavor, facilitate, "serves as" for "is"). A defined technical term (perfect sampling, exact diagonalisation, unique solution) is not hype; judge the claim, not the word. [U; V: scholarly-writing-refiner reversed, humanizer]
- W3 No colloquial spatial wording or anthropomorphism for technical concepts ("how far back it must look", "the network remembers"); use the field's concept words (conditions on, is identifiable from, mass scale). Figurative spatial phrases on abstract nouns (locate the limits, draw the line, trace the boundary) are candidates to judge in context. [U]
- W4 Review presumptive adverbs (clearly, obviously, trivially, of course, simply) where they stand in for support. [U; V: K-Dense research-grants names "obviously" and "clearly"]
- W5 Flag unsupported moral or personal praise of technical objects ("an honest estimate" meaning a good one), and coined labels without a definition. Keep established or defined technical uses of the same words, and do not substitute a concrete property the source does not support. [S: avoid-ai-writing; Research-Paper-Writing-Skills]
- W6 Cut empty phrases: in order to (to), due to the fact that (because), "it is worth noting that" (delete). Flag self-weakening words (merely, only achieves) where the evidence is strong. [V: scholarly-writing-refiner, journal-adapt-writing, econ-writing, anti-defensive-writing]
- W7 Contrast frames ("not X but Y", "It is not X. It is Y."): delete the negated half when nothing factual is lost; keep the contrast when it is the claim. Ask whether anyone held the denied view. [S: SNL paper-writing keep-vs-cut test; U: straw-man test]
- W8 Closing sentences that only restate, quotable aphorisms, forced lists of three, answers to objections nobody raised, and comments about the document itself are deletion candidates. A closing sentence that states a programme's vision in a statement or proposal is not. [S: humanizer, stop-slop, SNL paper-writing]
- W9 No quotation hooks. In a problem-framing opening, state the problem or question directly; other openings do their document-specific job. [U]
- W10 Tense and person: one's own completed results in the past ("we showed"); established facts and what a figure shows in the present; the ongoing programme in the present; plans in the future. First person singular for single-author applications, "we" for joint results. [U; V: scholarly-writing-refiner section tenses]

## Output format

Default (`minimal`, `moderate`):

```
## 수정 문단
<revised English text, ready to paste>

## 변경 이유
1. "<original phrase>" → "<revised phrase>"  (S2, R2)
   <problem and reason in one or two lines; state any change in meaning or scope>

## 검증
- 단어 수: 20 / 10 / 29 / 24 / 15 (합 98), prose_check 기준
- --compare: <listed differences and whether each is intended>; 주장별 인용·부정·조건 대응: 확인함 / 확인 못 한 것
- 남은 후보와 판단: <flags kept on purpose, with reason>
```

Add `## 바꾸지 않은 것` only for deliberate keeps a reader would question, and `## 정하실 것` only when a decision blocks the work.

`restructure`: give two or three alternatives that differ in logical structure (sentence count, order of claims, how the opening and the results connect), not in synonyms. For each: the English text, words per sentence, one line per sentence on why, the knowledge it asks of the reader, its risks (overstatement, scope, readability), then one recommendation.

On request ("진단", "full diagnosis"), add a table with one row per area (claim, evidence, structure, reference, wording) and ✓ / △ / ✗, where ✓ means no candidate survives judgment, △ means candidates remain that the author may keep, ✗ means at least one change is needed.

## scripts/prose_check.py

Standard-library Python 3. Input: `.md`, `.typ`, `.tex`, plain text, or `-` for stdin.

```bash
python3 scripts/prose_check.py draft.md                     # all paragraphs
python3 scripts/prose_check.py --para 3 section.tex         # one paragraph
python3 scripts/prose_check.py --compare old.md new.md      # protected-token surface diff
python3 scripts/prose_check.py --strict --allow "exact sampling" abstract.typ
```

- Word count: whitespace tokens after normalisation. Inline math becomes `MATH` and inline code or raw text `CODE`, one word each; citations, references, and labels are removed. A sentence that still holds markup or the `#EXPR` placeholder is flagged `unparsed-markup` and its count is marked provisional (`*`, or `provisional_count` in JSON).
- Typst is read in one pass, with no later pattern pass over its output, so text that the pass has classified is never reread. After each unescaped `#` the complete identifier (hyphens included) is read first. Exactly `set`, `show`, `let`, `import`, or `include` makes a statement, dropped with a note, which ends at a top-level `;`, the line end, or the closer of an enclosing block. Text functions (`emph`, `strong`, `text`, `footnote`, and similar) contribute their scanned content; `cite`, `ref`, `label`, and spacing calls are dropped; break calls become breaks; any other expression, including `#"..."`, `#{...}`, and `#(...)`, becomes `#EXPR`. Control-flow and other keywords the pass does not parse (`if`, `for`, `while`, `context`, ...) stop the analysis. Strings, raw text, math (with its strings and embedded `#` code), escapes such as `\$`, comments, and content blocks are tracked everywhere, so a comment marker, bracket, or dollar sign inside them does not swallow prose. Raw blocks (three or more backticks) and headings are dropped. Whenever the pass cannot classify a construct or find where it ends, the analysis stops with a note and exit 2.
- Markdown: block structure is read first, following CommonMark for the blocks that matter here. Containers come first: a list item (its first-line content, lines indented to its content column, and lazy continuation lines of an open paragraph) and a block quote (with lazy continuation only after an open paragraph) are unwrapped and parsed recursively, so a fence or heading on a list-marker line gets the same rules as anywhere else. Leaf blocks: fenced code closes at the first fence of the same character at least as long as the opener; indented code; ATX and setext headings (any `=` or `-` underline under a paragraph; lazy lines never form one); thematic breaks; HTML blocks with their CommonMark end conditions. Only a non-empty list item, and outside a list only one numbered 1, interrupts a paragraph. Code, headings, and HTML blocks are omitted with a note. Inline code and math are then matched only inside one prose block: code spans follow CommonMark (a backslash-escaped backtick is literal; a run of N backticks needs a closing run of exactly N) and become `CODE` before any other pass; inline math follows pandoc's dollar rules, so `$5 and $6` stays prose. List markers are removed with their containers before counting.
- LaTeX: verbatim environments, `\verb`, `\lstinline`, `\url`, and `\href` targets are set aside before comments are stripped, so a `%` inside them does not cut the line; escaped `\$` does not open math.
- Other skipped input: Markdown code fences and table lines (with a note), HTML comments, headings, and LaTeX comments, display math, and figure and table environments.
- Candidates: long sentences (`--max-words`, default 30), several clause joins in one sentence, comma-enclosed phrases (read whether they split subject and verb or verb and object), "with X -ing", trailing -ing clauses, stranded auxiliaries, bare This/It openers, demonstratives with a count of earlier occurrences of the same word (occurrences, not referents), pronouns, repeated content words (limited inflection grouping), word lists (hype, weak verbs, inflation, scope words, presumptive adverbs, stock connectors, contrast frames, colloquial and spatial wording). Defined technical terms are exempt through a built-in list and `--allow`.
- Punctuation: dashes, colons outside the exempt span of a time, ratio, URL scheme, or path, and semicolons. Whether a colon joins clauses is decided by reading.
- `--compare` reports surface differences in supported forms only: math (`$...$`, `\(...\)`, `\[...\]`, equation-type environments) and quantity macros (`\SI`, `\qty`, `\num`, with optional and starred forms) verbatim from the raw source; citation keys (`\...cite...{}` including starred and optional-argument forms, `#cite(<key>)`, `@key`, `[n]`); numbers with units and negations, first as tokens, then as "same token, new context" for review inside each sentence; hedges; scope words and bounds. Every other LaTeX command or Typst function call that is neither compared nor known to be plain formatting is listed verbatim as not compared, split into `both` (present in both inputs, which says nothing about meaning), `old_only`, and `new_only`. A swap between positions with identical neighbours is not detected. It does not check meaning, claim strength, or what each citation supports.
- Exit: 0 done; 1 with `--strict` when an unexempted dash or colon candidate remains (word-list hits never fail); 2 when a file cannot be read or part of the input could not be analysed, in both modes. In analysis mode, finding no prose also returns 2. In comparison mode, no prose is not an error (math alone can be compared); when neither input has any supported item, a note says so.
- Limits: regular expressions, not a parser. It does not resolve antecedents, and it misses enclosed phrases and lists of unusual shape. Use it to find places to read, not to certify text.

`scripts/test_prose_check.py` (standard library, `python3 scripts/test_prose_check.py`) pins the cases from review where prose was once lost silently or a protected-token change went unreported; run it after changing the script.

`research-statement/scripts/rs_check.py` stays the document-level check for statements (section shares, placeholders, citation numbering, Korean dash and CJK checks). Its dash and word-list checks overlap with this script on purpose; the document skill owns pass or fail for its submission files.

## References

- `references/rules.md`: each rule with its source, the source's own condition, how this skill varies it, and short examples.
- `references/sources.md`: the surveyed skills (URL, licence evidence, stars and installs with date), what was adopted, adapted, or rejected, and why.
