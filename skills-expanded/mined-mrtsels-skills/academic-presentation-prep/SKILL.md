---
name: academic-presentation-prep
description: Bilingual Q&A + speech prep for academic poster talks.
metadata:
  source_frontmatter:
    version: 1.0.0
  imported_from: hermes
---

# Academic Presentation Prep (Q&A + speech, bilingual)

Prepare for academic poster/oral presentations: requirement checklist from the official email, a divergent Q&A bank, and a timed speech script. Trigger: 答辩/展示材料, poster Q&A, 讲稿, presentation prep. Companion to `internship-report` (CUHK report/poster *writing* — that skill is user-owned/external, read-only to autonomous curation; presentation *prep* lives here). Example outputs: `qna/poster_qna.md` + `qna/poster_speech.md` in the project repo.

## 1. Requirement check → checklist in TASK.md

- Convert the official requirements email into a per-item checklist with statuses: ✅ verified / ⏳ user action + deadline / ⚠️ difference needs decision / ℹ️ info.
- Verify every claim against actual files (`pdfinfo` page size/ratio, `grep -n \section`, count bib entries) — never trust filenames or memory (user has zero tolerance for fabrication).
- Order EVENT sections **chronologically** (setup before presentation), even when the email lists them in another order — user corrected exactly this (setup 08-13 precedes presentation 08-14).
- Status flips are the user's call: "mark as done" → ✅ (e.g. poster size decided); "no appearance" → delete stale sections outright, repurposed phases don't carry old content.
- User-action items (upload, print, sign-in, plagiarism/VeriGuide check) stay ⏳ with deadlines; never claim them verified. Tools requiring lead time get the lead-time deadline (VeriGuide ≥48h before submission → 2 days earlier).

## 2. Q&A bank (divergent questions, concise answers, bilingual)

- §0 key-numbers cheat-sheet table first — every number examiners may probe (params, latency, accuracies, deltas), consistent with the poster/report.
- Group questions widely: motivation / method design / experiments / limitations / divergent-tough ("why not a Transformer", "what would you do with three more months").
- Plant HONEST soft-spot questions with truthful answers (weak prediction heads on real data, low cross-domain scores, small eval sets, precision tradeoffs) — examiners probe these; prepared honesty beats hedging.
- Answers 1–2 sentences; re-verify every number from the deliverable files, never from memory of earlier turns.

## 3. Speech script (timed)

- Timing table first: total slot includes Q&A → script ≈ 60–70% of slot (10–15 min → ~8–9 min talk).
- 6 sections: opening (name + supervisor + one-line topic) / motivation / existing-solutions gap / method / results / limitations + future + close.
- Per-section poster-location pointing cues ("讲哪指哪"); delivery tips: lead with conclusion, slow down and stress numbers, mid-talk time checkpoints (e.g. 3:00 into method, 6:00 into results).

## 4. Bilingual format (user preference)

EN = deliverable/spoken (examiners/audience are English-speaking); CN = understanding gloss underneath. Always both, question and answer.

- **一句话一句话对照 (sentence-by-sentence alignment)** — user-corrected twice. When asked for 中英对照 in formula/steps content, do NOT write one EN paragraph followed by one CN paragraph. Interleave per line: `1. **EN:** <one sentence> **CN:** <same sentence>`, so each numbered step/line carries both languages inline. Applies to 构成步骤 blocks and any explanation content; Q&A entries keep their existing `EN:`/`CN:` separate-paragraph shape (that format was accepted), but numbered step lists must be line-aligned.
- For 公式速查 / formula sections: symbol table (符号/是什么/数值+出处 with `path:line`) → **构成步骤** (numbered step-by-step "怎么一步步算出来的", EN↔CN per line) → **怎么总结出来的** (provenance/derivation rationale, honest about experiment-set vs config-backed values). All three parts expected when the user says 把公式讲具体/怎么构成/怎么来的.

## 5. Git

Repo rule: add specific paths (no `add .`), one change = one commit, push immediately.

## Pitfalls

- Numbers drift between report/poster/qna — regenerate answers from the deliverables, not from earlier conversation turns.
- Keep claims within BOTH the poster and the report (examiners may have read either).
- Check physical fit explicitly when board limits differ from poster size (e.g. board 37″×74.5″ vs poster 35.1″×46.8″ — fits, but verify).
- **Formula claims drift from code** — when asked to explain a poster formula ("每个变量讲具体/怎么来的"), trace EVERY symbol to source (`encoder.py`, `losses.py`, `constraints.py`, config yaml) and cite `path:line`; never answer from memory. Known discrepancy classes found in this project: loss-function identity (poster "smooth-L1" vs code MSE), feature content (poster "normalized area" vs code confidence), metric-vs-loss confusion (IoU as eval metric vs MSE training loss), hyperparameter values (poster w_v=0.5 vs code CombinedLoss default 1.0). In Q&A, admit the discrepancy honestly instead of claiming the poster value is config-backed.
- Full grounded variable glossary for this project's poster formulas: `references/poster-formula-glossary.md`.
