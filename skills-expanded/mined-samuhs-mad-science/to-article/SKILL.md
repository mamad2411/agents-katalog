---
name: to-article
description: >-
  Use when asked to generate, draft, or rewrite a scientific/technical
  article in Computer Science (conference paper, journal paper, or survey) from a
  topic/idea plus the repository's code, experiments, and results. Also use when
  asked to structure, review, or de-slop an existing draft. Triggers: "write the
  paper", "write an article", "generate the article from the repo", "turn this
  experiment into a paper", "review/reformat my draft".
mode: true
icon: crown
color: red
---

# to-article

Produce a complete, submission-ready scientific article in the correct template,
written with human, anti-slop prose and grounded in the actual code and results
present in the working directory — never invented from memory.

## Core principles

1. **Ground in the repo.** The article's theory, method, and numbers come from
   files in the target directory (docs, code, experiment outputs). If evidence is
   missing, say so and stop — do not fabricate metrics, datasets, or claims.
2. **Derive before writing.** Complete the derivation (references/derivation.md)
   BEFORE generating prose. Without it the model defaults to the slop register.
3. **Anti-slop is a post-pass, not an avoidance list.** Never load "words to
   avoid" into context while generating (that primes them). Write to a positive
   register; run the anti-slop audit on the finished draft (references/anti-slop.md).
4. **One section at a time, spec-first.** For each section, first state what it
   must contain (references/section-spec.md), then write it against the derived
   register. No filler paragraphs.

## When to use / when not

- Use: creating a new article from repo evidence, or reviewing/reformatting an
  existing draft.
- Not for: narrative blog posts, marketing copy, or non-scientific writing.

## Workflow

### 1. Detect target template
- If the user names a venue (conference/journal), use it.
- Else infer from context: target repo language pt-BR or Brazilian venue → SBC;
  arXiv/acmart or English conference → ACM sigconf; IEEEtran or IEEE venue → IEEE.
- Load that template's rules from references/templates.md. Record the choice.

### 2. Run derivation (mandatory)
Fill these silently (references/derivation.md for full spec):
- readerProfile — one specific reviewer: what they know, what they must be able
  to do after reading.
- registerTarget — the venue/template whose register the prose must match
  (e.g. "SBC conference paper in pt-BR", "ICSE paper in English").
- sceneAnchor — where the reader meets the text.
- textureConstraint — concrete vocabulary from the repo: method names, metric
  names, dataset names, file/table names.
- antiPattern (optional) — one positive redirection for a known prior failure.

### 3. Extract evidence from the repo
Run references/extraction.md against the working directory (or the path the user
pointed to). You need three things, each with a source path:
- Theoretical basis — README, docs/, design docs, related papers cited there.
- Experiment code — entrypoints, configs, training/eval scripts, notebooks.
- Results — CSV/JSON/TSV outputs, logs with metrics, plots, saved artifacts.
Extract boundaries: keep the raw bytes out of context (parse/summarize in
processor; cite `path:line` when quoting a number). Record a small evidence map:
topic → files → key numbers.

### 4. Choose the article shape
From evidence + template + article type (empirical / systems / survey / position):
pick the section layout in references/section-spec.md. Confirm the skeleton with
the user before drafting (short checkpoint; skip only if the user said to go).

### 5. Draft section by section
For each section in order (see section-spec), write against the derived register
and the template's expectations. Write the **abstract last**. Keep placeholder-free
prose: if a number isn't in the evidence map, leave an explicit `[EVIDENCE: metric
X from file Y]` marker rather than inventing it.

### 6. Audit (anti-slop pass) — on the finished draft, not while writing
Run the presence-test checklist in references/anti-slop.md. If a section fails,
revise that section only. Then run the template's format checklist
(templates.md): keywords/CCS Concepts, reference style, page limits, metadata.

### 7. Deliver
Return: proposed file path(s) (template-specific, e.g. SBC `.tex`/`.md`), the full
article text, and a 3–5 bullet summary of evidence used and any `[EVIDENCE]` gaps
left unresolved for the author to fill.

## Common mistakes

| Mistake | Fix |
|---|---|
| Inventing metrics not in the repo | Stop; mark `[EVIDENCE: ...]` and ask the author. |
| Abstract written first with generic claims | Write abstract last, from the actual results. |
| Filler intro / "in this paper we..." meta-talk | Cut meta-talk; first paragraph of each section states the claim (single-pass rule). |
| Em-dashes, "leverage", "robust", triple lists (AI tells) | Caught in the audit pass; rewrite to plain verb + concrete noun. |
| Template mismatch (e.g. SBC format on an IEEE target) | Re-check the templates.md detection step; re-run the format pass. |

## Quick reference
- Derivation fields: readerProfile · registerTarget · sceneAnchor · textureConstraint · antiPattern
- Section order: Title → Abstract → Keywords/CCS → Intro → Related Work → Method → Results → Discussion → Conclusion → Refs
- Anti-slop audit = presence checks, not absence lists: human subject? concrete noun per
  paragraph? first sentence = claim? varied rhythm? earned emphasis (no "this matters")?
- Evidence rules: every number has a `path:line`; no placeholder-free inventions.