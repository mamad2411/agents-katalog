---
name: anki-deck-audit
description: "Audits an Anki flashcard deck (the TSV produced by pareto-study-kit / book-to-anki, or any Front/Back TSV) for the defects that make a deck expensive to study: non-atomic answers, enumerative and double-barreled questions, near-duplicates, flat per-chapter distribution with no prioritization, missing tier tags, and the real study-hour cost. Prints numbers plus a pass/fail verdict, then a triage of what to cut. Use when the user asks to evaluate/audit a deck, asks 'dá para aplicar 80/20 aqui', complains a deck is too big or too slow, or as the final gate of a book-to-anki run."
argument-hint: "[path to a '- Study.txt' deck file, or a study/ folder]"
allowed-tools: Read, Bash(python3:*), Bash(ls:*), Bash(wc:*), Bash(awk:*), Bash(grep:*)
---

# Anki Deck Audit

Answers one question about a finished deck: **is it worth the hours it will
cost?** Structural validity — columns, header directives, deck names, tag
slugs — belongs to `book-to-anki`'s `anki-kit.py validate`. This skill assumes
the file imports fine and asks whether it should have been generated that way
at all.

It exists because of a real failure. A 533-card Kubernetes deck passed every
structural check and was still bad: 43% of the answers bundled several facts,
10% of the fronts asked for a list, every chapter got ~20 cards regardless of
whether anyone would ever use them, and 14% of the deck was Docker
prerequisites in a Kubernetes deck. Nothing in the pipeline was looking at
that, because nothing was measuring it.

## Step 1 — Run the script

```
python3 ${CLAUDE_SKILL_DIR}/scripts/deck-audit.py \
  --dir "<book folder>/study" --book "<Book Title>"
```

Or point it at a single file (works on a merged 4-column deck and on a raw
2-column subagent partial alike):

```
python3 ${CLAUDE_SKILL_DIR}/scripts/deck-audit.py \
  --flashcards "<path>/... - Study.txt" [--questions "<path>/... - Questions.txt"]
```

`--json` adds a machine-readable summary; useful when another skill consumes
the result. Exit code 1 means at least one **hard** threshold was breached.

## Step 2 — Read the verdict, don't just relay it

The script measures; you judge. Every `REPROVADO` line is mechanical and
reliable — those are counts, not opinions. The `AVISO` lines need you to look
at actual cards before you repeat them:

- **Respostas compostas / longas** — near-always a real defect. Open three of
  the flagged lines and confirm they bundle independent facts rather than
  being one fact that needs a subordinate clause.
- **Perguntas enumerativas** — confirm the front really asks for a list
  ("quais são as três...") and isn't just a plural noun ("quais recursos o
  Deployment cria?" with a single-concept answer is fine).
- **Perguntas duplas** — the ` e (como|o que|por que|qual)` pattern catches
  genuine two-question fronts, but also the occasional innocent coordination.
  Sample before quoting the number.
- **Distribuição plana (CV baixo)** — this is the finding the user usually
  cares most about and the one the script can only flag, never fix. A low CV
  means the 80/20 ran *inside* each chapter and never *between* chapters:
  the closing chapter and the prerequisite appendix got the same budget as
  the chapter about the thing the book is named after.
- **Concentração temática** — read the top-20 term table against the book's
  actual subject. Terms that dominate the deck but not the subject (a tool
  used in two chapters, a prerequisite technology, a dead project) mark
  material that should have been in the peripheral tier or cut.

## Step 3 — Turn the flat distribution into a concrete cut

When the deck has no tier tags, or has them and they don't filter (the script
warns above 45% núcleo), do the triage the generator skipped: sort every
chapter into **núcleo** (used constantly by anyone doing this work),
**complementar** (real but occasional), **periférico** (prerequisite tech,
one-vendor tooling, closing/meta chapters, obsolete projects) and give the
user the card counts and percentages per bucket, plus what the trimmed deck
would cost in hours versus the current one.

Name the chapters. "Corte os periféricos" is not actionable; "os 4 apêndices
são 73 cards (13,7%) de Docker, não de Kubernetes; o cap. 21 são 19 cards de
Kubeless, projeto morto" is.

## Step 4 — Report

In pt-BR, content-first. Lead with the numbers table (inventory, atomicity,
study cost), then the verdict, then the proposed cut with real chapter names
and real hour figures on both sides. End with the single highest-leverage
action, not a menu.

When invoked as the final gate of `book-to-anki`, keep it short: the numbers,
the verdict line, and — only if something breached a hard threshold — which
chapters need their subagent re-run. The orchestrator's own report carries
the curation narrative; don't duplicate it.

## Thresholds

Defined at the top of `scripts/deck-audit.py` and calibrated on the failure
above. Change them there, never inline in a one-off command, so every audit
stays comparable:

| Métrica | Limite | Tipo |
| --- | --- | --- |
| resposta média | <= 150 chars | duro |
| resposta individual | <= 200 chars | aviso |
| respostas compostas (>=3 frases ou `;`) | <= 20% | duro |
| perguntas enumerativas | <= 5% | duro |
| perguntas duplas | 0 | duro |
| fronts duplicados exatos | 0 | duro |
| CV de cards por capítulo | >= 0.30 | aviso |
| fatia do deck marcada como núcleo | <= 45% | aviso |
| tamanho do deck | 400 cards | aviso |
