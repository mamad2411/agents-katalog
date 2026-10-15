---
name: feynman-explain
description: Fixed-format explanation discipline for concepts, systems, and code. Use when the user asks "อธิบาย…", "นี่คืออะไร", "อันนี้ทำงานยังไง", "explain X", "what is X", "how does X work", "why does this exist"; when they ask for a simpler, shorter, or plainer version of something; when they say an answer was too long, unformatted, or unreadable; or when they invoke /feynman. Also use before teaching, onboarding, or presenting a concept to someone else.
argument-hint: "[deep] <the concept, system, file or question to explain>"
effort: max
---

# Feynman Explain

An explanation you cannot compress is an explanation you do not understand yet.
The answer is a **fixed card with hard caps**: the fuzzy parts get named out loud,
the gaps get filled from real evidence, and what survives is short enough to read
in one screen.

## The output contract

Emit these parts, in this order, and nothing else. Write the headings in the
user's language.

| Slot | ไทย | English | Cap |
|---|---|---|---|
| ① | `① อธิบายง่าย ๆ` | `① Plain explanation` | ≤ 60 words + one analogy line |
| ② | `② จุดที่ยังคลุมเครือ` | `② Fuzzy parts` | table, ≤ 3 gap rows + one jargon row per term used |
| ③ | `③ เติมช่องว่าง` | `③ Gaps filled` | ≤ 25 words per gap (question → answer → simple version → source) |
| ④ | `④ อธิบายใหม่` | `④ Tightened explanation` | ≤ 80 words + exactly 3 takeaways |
| 🎯 | `🎯 30 วิ` | `🎯 30 seconds` | one sentence, quoted |
| → | `→ ต่อ:` | `→ Next:` | one line offering the next move |

Shape of ② and ③:

```
② จุดที่ยังคลุมเครือ
| จุดที่พูดคลุม | คำถามจริงที่ค้าง |
| "..."        | ...              |
| jargon       | อธิบายง่ายได้? |
| "..."        | ได้ / ไม่ได้ / ครึ่ง ๆ |

③ เติมช่องว่าง
Gap 1 — <คำถาม> → <คำตอบ> → พูดง่าย ๆ ว่า <…>   (ที่มา: path/file.cs:118)
```

**Total default budget: ≤ 250 words.** Over budget means **cut scope** — narrow
the topic, drop the weakest gap, shorten the analogy. Never add a section, never
spill into extra prose, never continue past `→ ต่อ:`.

No preamble, no "great question", no closing summary paragraph — 🎯 *is* the
summary. Do not emit a process diagram of this skill: it costs screen space the
answer needs.

## Language

Mirror the language the user asked in. Keep the technical term in English on
first use with a ≤ 8-word gloss in parentheses — `pipeline (ลำดับโค้ดที่วิ่งต่อกัน)` —
then use the English term from there on.

## ② is not theater

Name at least one real fuzzy point in your own ① — the place you hand-waved, the
word you leaned on. Every piece of jargon that appeared in ① gets a jargon row
with an honest verdict. If you genuinely have no fuzzy point, say so and give the
reason instead of inventing one.

## ③ fills gaps from evidence, not confidence

| Gap is about | Fill it from | Cite |
|---|---|---|
| the user's system — code, repo, D365/Dataverse org, DB, pipeline, config | open the file / run the query / check git **before** answering | `path/file:line`, the query, or the commit |
| an external product, API, or platform behaviour | official docs (the `microsoft-docs` skill, or a fetched vendor page) | the URL |
| vendor lifecycle — SKU, exam code, retirement, pricing | hand off to `verify-then-advise` | that skill's verdict |
| a general concept with no artifact behind it | your own knowledge | mark it `(จากความรู้)` / `(from knowledge)` |

A gap you cannot fill **stays in ②** as `ยังไม่ชัด`. An unfilled gap is a finding
you report, not a failure you paper over — and never a sentence written
confidently enough to hide it.

## Analogy rule

One line, concrete, from everyday life: `X เหมือน Y เพราะ Z`. "Git is like time
travel" is abstract and fails; "Git เหมือนการเซฟดราฟต์เรียงความ — ย้อนกลับไปดราฟต์ไหนก็ได้"
works.

## Modes

- **default** — the contract above.
- **`deep <topic>`** — caps ×2.5, and one section diagram is allowed (type-matched
  per `references/diagram-convention.md`). Every gap gets its
  own evidence trail. Use only when the user asks for depth.
- The user wants something they can click through step by step → hand off to
  `problem-description`.
- The question is really "how *should* this work / what should we do" → hand off to
  `study-design-verify`.

If the answer is requested as a **Markdown file**, it becomes a generated document:
Rule 1 of the diagram convention applies (one overview Mermaid diagram at the top).

## Worked example

> **/feynman Dataverse plugin pipeline**

```
📘 Dataverse plugin pipeline

① อธิบายง่าย ๆ
โค้ดที่เราแทรกเข้าไปให้ทำงานตอนมีคนบันทึกข้อมูล Dataverse จะหยุดกลางทาง
เรียกโค้ดของเรา แล้วเดินต่อ เราเลือกได้ว่าให้แทรกก่อนหรือหลังเขียนลงฐานข้อมูล
เหมือนสายพานตรวจของ — ของวิ่งผ่าน 4 จุด ใครจะแทรกก็เลือกจุดได้

② จุดที่ยังคลุมเครือ
| จุดที่พูดคลุม | คำถามจริงที่ค้าง |
| "หยุดกลางทาง" | ถ้าโค้ดเรา throw แล้วข้อมูลที่เขียนไปแล้วย้อนกลับไหม |
| jargon | อธิบายง่ายได้? |
| stage | ได้ — จุดบนสายพาน |
| async | ครึ่ง ๆ — ยังไม่ได้พูดว่าออกนอก transaction |

③ เติมช่องว่าง
Gap 1 — throw แล้ว rollback ไหม → sync stage อยู่ใน transaction เดียวกัน ยกเว้น
PreValidation และ async ที่อยู่นอก → พูดง่าย ๆ ว่า "throw ตอน sync = ยกเลิกทั้งชุด"
(ที่มา: learn.microsoft.com/power-apps/developer/…/event-framework)

④ อธิบายใหม่
Dataverse เรียกโค้ดเราได้ 4 จุดรอบการบันทึก: PreValidation (นอก transaction),
PreOperation (ก่อนเขียน), PostOperation (หลังเขียน) และ async (หลังจบ ไม่ร่วม
transaction) สามจุดกลางอยู่ใน transaction เดียวกับการเขียน — โค้ดเรา throw คือยกเลิกทั้งชุด
1. เลือก stage = เลือกว่าเห็นข้อมูลตอนไหน
2. sync = ล้มพร้อมกัน, async = ล้มแยกกัน
3. อยากแก้ค่าก่อนบันทึก ต้อง PreOperation

🎯 30 วิ
"Plugin pipeline คือ 4 จุดที่เราแทรกโค้ดเข้าไปรอบการบันทึกข้อมูล — จุด sync ล้มแล้วยกเลิกทั้งชุด, async ล้มแยก"

→ ต่อ: เจาะ async กับ rollback / ดู stage ที่ org เราใช้จริง / deep
```

## Red flags — stop and re-cut

- A fourth paragraph appearing in ①, or prose after `→ ต่อ:`
- ② empty, or filled with fake gaps you already answered in ①
- ③ answering a question about *our* system with no `path:line`, query, or URL
- A section that is not in the contract table
- The default answer no longer fits one screen

**All of these mean: cut scope, not add words.**

---

Adapted from the `feynman` skill in
[neurofoo/agent-skills](https://github.com/neurofoo/agent-skills) (MIT) — the four
steps are theirs; the caps, the evidence rule for ③, the language rule, and the
handoffs are ours.
