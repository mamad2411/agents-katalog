---
name: asking-to-understand
description: "Socratic questioning discipline - the user is asked, not told, until they can state the rule themselves. Use when the user says \"ช่วยถามคำถามหน่อย\", \"ถามให้คิด\", \"ask me questions\", \"grill me\", \"quiz me\", \"make me think\"; when they own an artifact they do not understand - \"ยังไม่ค่อยเข้าใจสิ่งนี้ที่ให้ AI ทำ\", \"I don't understand what was built for me\", a plan/map/pipeline/codebase handed to them; before a sign-off, handover, or onboarding onto a system they now own. Not for explaining on request (feynman-explain) and not for challenging a plan before building it (grill-then-plan)."
argument-hint: "<the file, map, plan, pipeline or system to be questioned on>"
effort: max
---

# Asking To Understand

A question the answerer can answer from memory taught nobody anything.
The session is **one grounded question per turn**, and it ends when they state
the rule in their own words - not when your question list runs out.

**The failure this prevents:** an agent asked to "ask questions" dumps eight at
once, none standing on anything it looked at, each with the answer already folded
into the wording. The answerer picks the easiest one, everyone feels productive,
nothing moves.

## The session contract

Four phases, in order. Phases 1-3 loop.

| Phase | ไทย | What it is |
|---|---|---|
| ⓪ | `ตั้งพื้น` | Read the artifact and RUN the cheap checks - before the first question |
| ① | `ถามหนึ่งข้อ` | Exactly one question per turn, then stop |
| ② | `รับคำตอบ` | Classify the answer; the class picks your move (table below) |
| ③ | `ต่อจุด` | Every 3-4 questions, say out loud which two answers share a shape |
| ④ | `ปิด` | Park what is open, list what is concretely undone, hand the turn back |

## ⓪ Ground first - no question before evidence

Spend 3-8 read-only checks before opening your mouth. The minimum bar:

**verify that what the artifact CLAIMS exists actually exists.**

That one check alone - `git ls-tree`, `ls`, `git check-ignore`, a REST GET -
routinely finds the gap the whole session then turns on. A document is not
evidence of the thing it describes.

Every question you ask must stand on something you looked at. A question with no
measurement behind it is an opinion in disguise, and the answerer can smell it -
they start answering defensively instead of thinking.

## ① One question per turn

Shape of a question turn:

```
<evidence: 3 lines max - the measured fact, with path:line, command output, or API response>

**คำถาม: <one sentence>**

<optional: what a complete answer must contain - "ตอบให้ครบสามชั้น: A, B, แล้ว C">
```

**One question. Then stop and wait.** Silence after a question is the instrument,
not an awkward gap. Two questions in a turn means they answer the easy one and the
hard one dies unnoticed.

A parenthetical follow-up is allowed **only** when it is the same question one
layer deeper (`คำถามซ้อน:`), never a second topic.

### Choosing which question - the ladder

Ask the one highest on this ladder:

1. **They cannot answer it from memory** - it forces them to simulate the system
   or go look. *"Stage 3 fails after stage 2 deployed - what state is production in?"*
   beats *"do you think this pipeline is good?"*
2. **The answer changes what they do tomorrow** - prefer the shallow-but-live
   question over the deep-but-theoretical one, early.
3. **You do not know the answer either** - both sides have real evidence, so any
   answer is usable.

### The admission test - run it on every question before sending

> **If they answer this perfectly, is the question still worth having asked?**

- **No** - it is not a question, it is a trap. Delete it.
- **Yes** - send it. Either way, both sides leave with something.

## ② Receiving the answer - the class picks your move

| Answer class | Your move |
|---|---|
| **ถูกหมด** | Name what it unlocks, go to the next question |
| **ถูกครึ่งเดียว** | State which half is right and supply the missing half **as fact** - do not re-ask |
| **อาการ ไม่ใช่กลไก** ("we forgot", "AI slipped") | Push **once** on the same question: *"นั่นคืออาการ - กลไกคืออะไร"* |
| **ผิด** | Give the measured fact. Verdict on the artifact, never on the person |
| **ไม่รู้ / เลี่ยง** | Answer it yourself, then move on. Never ask the same question twice |

**Symptom vs mechanism is the move that pays.** A symptom answer produces "next
time be more careful", which fixes nothing. One more push produces a rule that
outlives the session. This is the step most often skipped, because pushing feels
like nitpicking - it is not, it is refusing to let the answer expire.

**Half-right answers get a named half, not a "ใช่ครับ แต่".** Telling someone
exactly which half they missed respects them more than a softened correction does.

## ③ Connect - this is the payload

Every 3-4 questions, look back across the answers and ask yourself whether two of
them are **the same bug in different clothes**. When they are, say so explicitly.

That is the thing a checklist cannot do and the reason a human is asking. A
session that never connects two answers was a quiz, not a grilling.

## ④ Closing

Stop when they state a rule in their own words. Questions after that point are a
performance. Then emit exactly:

```
**คำถามที่ยังค้าง** - by name, with the question restated in one line each
**ของจริงที่ค้าง** - the concrete measured facts that still need action
→ ถามต่อ หรือ ลงมือเก็บของจริงก่อน?
```

Parking a question out loud (`ขอค้างข้อ 5 ไว้ก่อน เดี๋ยวกลับมา`) is part of the
discipline - it keeps a thread alive without forcing it closed early.

## Language

Mirror the language the user asked in, including the questions themselves. Keep
technical terms in English with a short gloss on first use. If they ask in Thai,
ask in Thai.

## Worked example - one turn

> Artifact: a decision map an AI produced. Ground phase found the deliverable
> file is not where the map says it is.

```
ไฟล์มีจริง 308 บรรทัด แต่อยู่ที่ tmp/DEPLOY.md ไม่ใช่ root ของ repo โค้ด
และ tmp/ ถูก gitignore ไว้ (.gitignore บรรทัด 26) - ไม่เคยถูก commit

**คำถาม: คนที่คู่มือนี้เขียนถึง - dev คนอื่นที่ไม่ใช่คุณ - เขาจะเปิดไฟล์นี้เจอได้ยังไง?**

(ถ้าคำตอบคือ "ผมส่งให้" - คำถามคือคุณส่งเวอร์ชันไหน และอีกสามเดือนจะรู้ได้ยังไง
ว่าเวอร์ชันที่เขาถืออยู่ตรงกับของจริง)
```

Answer comes back: *"น่าจะอัพเดทไม่ครบ"* - class **อาการ ไม่ใช่กลไก** - push once:

```
"อัพเดทไม่ครบ" คืออาการ ยังไม่ใช่กลไก - ถ้าหยุดตรงนี้ วิธีแก้จะกลายเป็น
"คราวหน้าอัพเดทให้ครบ" ซึ่งแปลว่าไม่ได้แก้อะไรเลย

**กลไกคืออะไร - อะไรคือความต่างเชิงโครงสร้างระหว่างคำอ้างสองแบบนี้?**
```

## Red flags - stop and re-cut

- Two questions in one turn
- The answer is already folded into the question's wording
- A question sent before opening a file or running a command
- `"ใช่ครับ แต่..."` - a correction wearing a compliment
- Re-asking a question because the answer disappointed you
- Still asking after they have stated the rule
- Four questions in and nothing has been connected to anything

**All of these mean: fewer questions, more ground.**

## Handoffs

| Situation | Go to |
|---|---|
| They want it explained, not to be asked | `feynman-explain` |
| Challenging a **plan** before it is built | `grill-then-plan` / `sp-grill-with-doc` |
| It has turned into reviewing the work itself | `scrutinize` |
| What surfaced should become a durable lesson | `reflect` |
| An interactive click-through would land it better | `problem-description` |
