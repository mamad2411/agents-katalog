---
name: refine-quiz-questions
description: Refine quiz questions in TelNetQuiz CMS production data at cli/content/data/prod/chapter-*.json. Plan-first audit of each question against PUEBI/EYD ejaan, KBBI vocabulary, SPOK sentence structure, kaidah penulisan soal pilihan ganda (materi-konstruksi-bahasa), topic coherence between chapter title → level title → description → question → options, image-text synchronization, distractor quality so the correct answer never looks obvious, and Voice & Journey feel that casts the SMK student as a "Penjelajah" on a learning quest. Use this skill whenever the user asks to refine, polish, perbaiki, audit, improve, rapikan, or perhalus quiz questions / soal kuis / soal pilihan ganda; or mentions checking question quality, alur soal seperti sungai, kesinkronan gambar dengan deskripsi, kalimat baku, distraktor yang terlalu jelas, pengecoh terlalu mudah, feel petualangan, rasa journey, vibe penjelajah, hook deskripsi yang flat, or CTA yang kayak chore. Operates on chapter quiz files only — never touches pretest.json, achievements.json, image-assignments.json, upload-manifest.json, and never modifies the studyMaterial field.
user-invocable: true
---

# Refine Quiz Questions

A plan-first auditor and refiner for TelNetQuiz quiz content. Your job is to make each question read like a clean, focused river: chapter → level → description → question → options all flow toward one concept, with no broken Indonesian, no off-topic distractor, and no mismatch between the image and the words around it.

## Files at a glance

| Resource | Purpose | Read it... |
|----------|---------|------------|
| `scripts/prescan.py` | Mechanical scan (image sync, slang, panjang opsi, banned options, key position) — run first | Phase 2 opening |
| `references/quick-card.md` | One-page audit reference: rule codes, kata baku table, image-keyword map, descriptor shape | Always — primary reference |
| `references/deep/indonesian-language-rules.md` | Full PUEBI/KBBI/SPOK reasoning for borderline cases | Hanya kalau quick-card belum cukup |
| `references/deep/mcq-rubric.md` | Detailed MCQ rubric with paralel/non-paralel examples | Hanya kalau quick-card belum cukup |
| `references/change-map-format.md` | Output template for Phase 3 change map | Phase 3 |

## How questions render on the mobile app

The Android client (`QuestionScreen.kt`) renders each question top-to-bottom: level title → image (if `imageLink != null`) → description → question (centered, bold) → option A/B/C/D → verify button. Implications:

- **Level title is the on-screen anchor**, not chapter title. Coherence checks → primarily against level title.
- **"Gambar di atas" is literal** — image renders directly above description when present.
- **Options shown as A/B/C/D** — reference as "Opsi A/B/C/D" in the change map.
- **TTS reads** description + question + "Pilihan jawaban: A. ... B. ..." — punctuation drives pacing; avoid em-dash/parenthetical asides in `description`/`question`.
- **`audioLink` is pre-recorded** — never edit. Heavy text rewrites desync TTS audio; flag in finding.

## Non-negotiable scope

- **Read & write only**: `cli/content/data/prod/chapter-*.json`. Within those files, only edit: `description`, `question`, `options[i].text`.
- **Read-only**: `image-assignments.json` (treat as ground truth for image→question mapping).
- **Never touch**: `pretest.json`, `achievements.json`, `upload-manifest.json`, anything under `images/`, and these fields per question — `studyMaterial`, `audioLink`, `imageLink`, `isCorrect`.
- If a distractor is accidentally correct, raise as `KEY-CHECK` — never silently flip `isCorrect`.

If the user asks for something out of scope, say so plainly and either narrow the request or stop.

## The five-phase workflow (hard stop at phase 4)

### Phase 1 — Plan

1. Read each `chapter-*.json` in scope and `image-assignments.json` once.
2. Print a scope summary: chapters, levels, total questions, count of questions with images.
3. **If the user gave an explicit scope** ("Penuh", "chapter 2", "level 3 saja"), proceed directly to Phase 2 — no need to re-confirm. Only ask if scope is ambiguous.

### Phase 2 — Audit

**Step 2a — Run prescan first.** From the project root:

```bash
python .claude/skills/refine-quiz-questions/scripts/prescan.py --md
```

The script surfaces deterministic findings: image sync mismatches (description references gambar tapi imageLink null, atau gambar pakai konsep yang tidak disebut deskripsi), bare-stem verbs/slang/KBBI tidak baku, banned option patterns, panjang opsi tidak homogen (K5), number formatting (PUEBI), dan key position skew (K7) per level. Use its output as the seed list — every P1 item should become a finding unless you have a specific reason to dismiss it.

**Step 2b — LLM-only dimensions.** Prescan can't judge these, so for each question in scope run a quick mental pass:

- **M1-M4** (materi: one concept, one correct, homogen, coherent with level title)
- **K1, K4, K6** (stem clarity, paralelisme opsi, petunjuk gramatikal)
- **B3, B4** (tafsir ganda, kiasan di pokok soal)
- **V1, V2, V3** (Voice & Journey: hook vivid, CTA quest-like, level pacing builds)
- **River flow** — chapter → level → description → question → options stay on one concept

Open `references/quick-card.md` and consult its tables. Only open `references/deep/*.md` when a borderline case needs full reasoning.

**Step 2c — Capture each finding** with: file, level, qidx, field (`description` | `question` | `options[i].text`), one rule code from quick-card §1, the proposed exact replacement text, and a one-line reason tying to the rule.

Audit priority order: image sync first (binary, structural) → KBBI baku → MCQ kaidah → river flow → Voice & Journey. Image-sync errors are higher-impact than missing commas; fix load-bearing first.

**Distractor rewrites**: when an option is obviously wrong (gives the answer away by elimination) or accidentally correct, propose a homogen replacement (similar length, parallel grammar, same domain) that is plausible but unambiguously distinct. Never flip `isCorrect`. If you suspect the keyed answer is actually wrong, raise a `KEY-CHECK` finding and let the user decide.

### Phase 3 — Map

Render findings as a Markdown change map per `references/change-map-format.md`. Group by file → level → question. Show **Before** and **After** verbatim. Reason ties to one rule code from quick-card §1. Questions without findings: list compactly per level (`Level 1: Q2, Q4 — OK`).

If the change map exceeds ~30 questions touched, render in chunks per chapter and ask mid-stream whether to continue.

### Phase 4 — Approval gate (hard stop)

Print a one-paragraph summary (e.g. "Proposed: 12 description rewrites, 5 question rewrites, 8 distractor rewrites, 2 KEY-CHECK flags") and ask how to proceed. Accept: **All**, **Per chapter**, **Per question**, **Skip ...**, **Reject**. Don't interpret silence/"ok"/"go" as approval if scope is ambiguous — ask one clarifying question.

**Loop-context override**: when the invocation prompt explicitly contains the phrase `loop-context` (sent by `/loop-validate-refine`), skip Phase 4 entirely for non-KEY-CHECK findings — proceed directly to Phase 5 with implicit approval for all non-KEY-CHECK items. KEY-CHECK items are always surfaced separately to the user, never auto-applied. The orchestrator is responsible for capping iterations and surfacing KEY-CHECKs; the refine skill's job in loop-context is just to apply non-KEY-CHECK fixes deterministically.

### Phase 5 — Apply

Only after explicit, scoped approval:

1. Edit `chapter-*.json` files using exact-string replacements via the Edit tool. Do not reformat unrelated lines, reorder keys, or change indentation. Never use Write on the whole file.
2. After all edits, print a short summary: files touched, count of fields changed, KEY-CHECK items the user explicitly approved, and findings that were skipped (so the next session has a clean handoff).

## Voice & Journey — the rasa-petualangan dimension

The mobile app addresses the user as **"Penjelajah"** (see exit dialog in `QuestionScreen.kt`). Each question should feel like one waypoint in a journey through jaringan telekomunikasi, not a sterile exam item. This is a real audit dimension — a grammatically perfect question that reads like a textbook still fails it.

What it looks like in practice:

- **Hook (description sentence 1)**: relatable, sensory, specific. "Kamu buka HP, langsung tersambung Wi-Fi." > "Wi-Fi adalah teknologi nirkabel."
- **CTA (description final sentence)**: framed as a milestone or challenge. "Saatnya uji insting kamu!", "Ayo pecahkan misterinya!", "Gas, jawabannya!" > "Pilih jawaban yang benar."
- **Across a level**: questions cumulative (early warm-up, later deepen). Flat sequence = worksheet; paced sequence = chapter.

What it does **not** mean: not flowery prose; not gamified jargon ("XP", "level up" inside question text); not condescending; not at the cost of correctness. SMK students aren't children — cringe-y enthusiasm reads worse than dryness.

When proposing a rewrite for this dimension, cite `V1` (flat hook), `V2` (chore-y CTA), or `V3` (level pacing inconsistent).

## River flow — coherence rule

Every step from broad to specific should narrow toward the same concept:

```
Level title → Image (if any) → description (hook → image hint → concept hint → CTA) → question → opsi A/B/C/D
```

If sentence 1 talks about Wi-Fi but the question is about IP routing, the river is broken. The fix is usually to rewrite the description (cheaper) than the question. Description shape — see quick-card §7. The four-sentence shape is typical, not rigid; three sentences fine without a gambar.

Coherence break against **level title** = high priority (visible above description). Against **chapter title** only = low priority (off-screen on the question screen).

## Output discipline

- Write change map in Indonesian where source is in Indonesian — don't translate user-facing strings to English.
- Quote `Before`/`After` verbatim. Don't paraphrase. The user reviews a diff, not a summary.
- Reasons short and reference one rule code. "K5 (panjang opsi tidak homogen)" is good; "improved clarity" is not.
- Never bundle two unrelated fixes into one finding. One field, one rule, one fix — so the user can accept/reject each independently.

## Common pitfalls

- **Editing the wrong file**: confirm the file path starts with `cli/content/data/prod/chapter-` and is not `pretest.json` before any Edit call.
- **Silently flipping `isCorrect`**: never. Always raise as `KEY-CHECK`.
- **Reformatting JSON**: use Edit (exact string), never Write on the whole file. Preserve indentation and key order.
- **Over-editing the voice**: dataset has a distinctive playful CTA register. Refine grammar/structure, keep personality.
- **Skipping the approval gate**: the hard stop at phase 4 is the entire point. If you're about to apply without explicit scoped approval, stop.
