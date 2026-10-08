---
name: remove-ai-style
description: Aggressively rewrite Chinese or English prose to remove AI-generated patterns. Use for de-AI polishing, natural-language rewrites, robotic or formulaic writing, and publication cleanup. Always run the bundled deterministic Markdown analyzer first, remove every editable exclamation mark, dash, and formulaic binary contrast, inspect every other reported location, then read the full article for semantic patterns the rules cannot enumerate.
---

# Remove AI Style

Use a two-layer workflow:

1. Run the deterministic analyzer to locate repeatable lexical, punctuation, structural, and assistant-residue signals.
2. Read the full article and make contextual judgments that rules cannot cover.

Apply one strong default. Fix confirmed findings at every severity, rewrite awkward passages, and remove unflagged formulaic rhythm while preserving facts, meaning, required structure, and the author's intended voice. Do not ask the user to choose an intensity and do not offer light, moderate, heavy, or full modes.

Most analyzer hits still require contextual judgment. Three rule families are hard publication constraints in editable prose:

- Remove all exclamation marks.
- Remove all em dashes, en dashes, and double hyphens used as dashes.
- Rewrite all formulaic binary contrasts, including “不是……而是……”, “并非……更是……”, “看似……其实……”, “not just X but Y”, and close variants, as direct claims.

The post-edit analyzer counts for `zh-exclamation` or `en-exclamation`, `zh-dash` or `en-dash`, and `zh-binary-contrast` or `en-binary-contrast` must be zero. The only exceptions are protected regions such as code, URLs, Markdown targets, and source text that must remain verbatim. Do not treat brand enthusiasm, casual tone, or a writer's habitual punctuation as reasons to keep these patterns.

## Required workflow

### 1. Determine input and language

Prefer an absolute Markdown file path. If the user provides text only, pass it to the analyzer through stdin.

Detect Chinese or English from the article. Override auto-detection only when the result is wrong or the user explicitly specifies a language.

Load the matching reference completely:

- Chinese: [references/chinese.md](references/chinese.md)
- English: [references/english.md](references/english.md)

### 2. Run the deterministic analyzer

Run before editing:

```bash
python3 <skill-root>/scripts/analyze_ai_style.py \
  <article-path> \
  --language auto \
  --format json
```

The report contains:

- stable finding ID
- rule and category
- severity
- line and column
- matched text
- local context
- suggested treatment
- repeated-rule and document-structure summaries

Do not replace this command with copied `grep` snippets. The bundled script is the single owner of deterministic detection logic.

### 3. Inspect every finding

Rewrite every editable finding from the hard-constraint rule families. Do not classify these findings as intentional or false positives merely because the usage is grammatically valid.

Classify every other reported item as one of:

- `confirmed`: rewrite it
- `intentional`: keep it because the genre or voice requires it
- `protected`: leave it because it belongs to code, source material, structure, or another preserved region
- `false_positive`: no change
- `semantic_review`: the local hit is real, but the correct fix depends on wider context

Read the reported context, then inspect the surrounding paragraph before deciding. Do not bulk-replace phrases across the document.

### 4. Read the full original article

Always read the complete article unless the user explicitly asks to process only an excerpt. The analyzer cannot reliably detect:

- excessive metaphors with novel wording
- argument structure that is too symmetrical
- repeated paragraph logic with different vocabulary
- synthetic emotional escalation
- vague claims that sound polished but say little
- reader-mind-reading and sentences that digest the point for the reader
- empty evaluative adjectives such as “很清晰” or “很重要”
- claims that announce importance without a mechanism, number, or example
- genre mismatch
- flattened author voice
- suspicious facts or citations

Use the language reference to perform this semantic pass. The report is a navigation aid, not a substitute for reading.

### 5. Record protected structure

Before editing, record the structures that must survive:

- YAML frontmatter
- fenced code blocks
- Markdown tables when their structure is intentional
- images and links
- HTML comments
- complete `VISUAL_TODO` blocks
- quoted source material and citations

Do not change facts, numbers, URLs, code, image paths, TODO IDs, or citation targets merely to make prose sound more natural.

### 6. Rewrite aggressively

Make contextual edits rather than phrase substitution:

- Prefer concrete subjects, actions, mechanisms, and results. Lead with the fact, then the judgment; do not add emphasis that the evidence already carries.
- Remove meta-writing, reader-mind-reading, generic importance claims, empty evaluative adjectives, assistant residue, and decorative transitions.
- Vary rhythm only where the current rhythm feels artificial; do not add slang, mistakes, or random fragments to imitate a human.
- Preserve deliberate voice, technical precision, and genre-appropriate structure. Judgments may sit next to narrative, but each judgment should rest on a fact or mechanism.
- Drive confirmed findings down as far as the material allows. The hard-constraint rule counts must reach zero outside protected regions.

When invoked as a Subagent on a file, edit the file directly, then return a concise change report. Do not delegate the rewrite to another agent.

### 7. Run the analyzer again

After editing, rerun the same command and compare before/after summaries.

Use the hard-constraint gate for the final rescan:

```bash
python3 <skill-root>/scripts/analyze_ai_style.py \
  <article-path> \
  --language auto \
  --format json \
  --fail-on-hard-constraints
```

Exit status `2` means at least one exclamation mark, dash, or formulaic binary contrast remains in scanned prose. Rewrite it unless inspection confirms that the match belongs to source text that must remain verbatim.

Review every remaining finding individually. A remaining non-hard-constraint hit is acceptable when it is intentional, protected, required for accuracy, or a documented false positive. A remaining hard-constraint hit is acceptable only when it is protected or must remain verbatim.

Finally, read the full revised article once more for continuity and voice. A lower finding count does not prove the rewrite is good.

## Completion report

Return:

- language
- before/after finding counts by severity
- confirmation that the hard-constraint rule counts reached zero, or an exact list of protected verbatim exceptions
- confirmed rules addressed
- intentional or protected findings left in place
- important semantic changes found only by full reading
- confirmation that protected Markdown structures survived
- any factual or citation issue that needs human verification
