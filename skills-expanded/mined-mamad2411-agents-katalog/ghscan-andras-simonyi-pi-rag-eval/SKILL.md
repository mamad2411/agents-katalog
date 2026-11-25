# Bootstrap 3 — turn what you just did into a skill

Run this AFTER Part 8, in the same session that produced REPORT.md. The session
history is the raw material — do not start fresh.

---

We just built an eval set, swept ten configurations, scored them and wrote a
report. The next time the corpus changes, someone will have to check whether
retrieval quality regressed, and they will have to work all of this out again
from scratch.

Use the skill-writer skill and capture it.

Write a skill called `retrieval-regression`: given a corpus that has changed,
re-run this evaluation and report whether quality moved.

Base it on what actually happened in this session, not on how you would design
the procedure now. Specifically, include:

- the things that went wrong and how we recovered
- the order that turned out to matter
- anything we had to look up or work out
- what a fresh agent would get wrong without being told

Follow the structure guidance in skill-writer: short SKILL.md, detail in
reference/, anything deterministic in scripts/.

Then critique your own skill against the review checklist in skill-writer and
fix what you find.
