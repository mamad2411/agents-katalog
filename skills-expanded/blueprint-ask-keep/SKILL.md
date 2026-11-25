---
name: blueprint-ask-keep
description: "Add the approved answers to FAQ.md when the person chose to keep them, after what it already holds; change nothing otherwise."
---

# Keep the answers

The person has read the answers and approved them. Read `.blueprint/answers.json` and
`.blueprint/replies.json`.

**Never change a document.** The check compares each one with the fingerprint recorded when the answers were
written.

If `keep` is `残さない（.blueprint の中だけ）`, there is nothing to write: leave `FAQ.md` exactly as it is,
run the check and stop.

Otherwise add to `FAQ.md` in this folder (create it if there is none). **Add after what it already holds;
never edit or reorder what is there** — the check compares the beginning of the file with what it held
before. For each question: the question as a `##` heading, word for word; the answer; and where it is
written (the document, and the place named as in the answer: 第4条第2項, or a section's heading in 「」 —
in an English FAQ, in "…" — never chaff's `h1.3`). For a question the documents do not answer, say so — that is worth keeping
too.

## Done when

`node <usecase pack>/checks/replies.mjs keep` passes.
