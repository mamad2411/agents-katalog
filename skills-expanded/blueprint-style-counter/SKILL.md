---
name: blueprint-style-counter
description: "Prove the style bites: write texts that deliberately break the guide and confirm chaff reports them."
---

# Show that the style catches something

A style that no bad text can trip is a style nothing checks. This is the documents' version of breaking
the code to see a test go red.

Write a few short texts in `.blueprint/counter/`, in the same language and kind as the models. Each
breaks the guide on purpose, and each in a different way: a long run-on sentence, the wrong sentence
ending mixed in, a heading the next sentence merely repeats, padding and cushion phrases, a term spelled
against `STYLE.md`. Keep them plausible — the kind of draft a real writer produces on a bad day.

List them in `.blueprint/counter.json`:

```json
[{ "file": "run-on.md", "breaks": "語調と文末: 一文に三つ以上のことを詰めない" }]
```

## Done when

`node <usecase pack>/checks/counter.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the pack folders from your prompt) passes: chaff reports something in every counter text,
at least three different rules fire across them, and **every rule `chaff.yaml` turns on fires in at least one of
them** (a note counts). A consistency rule (contractions, the Oxford comma, heading case) reports only against a
clear majority, so its text must lean one way and break it once or twice — a text split evenly shows nothing. Never
write in the report that a rule "does not react" unless a text built to trip it was run and stayed silent. If a text raises nothing, the style does not reach what
it breaks: either that part belongs in STYLE.md only (a machine cannot see it — say so in the report),
or a rule is too loose or off — change it in `chaff.yaml` and record the new level and its reason in
`.blueprint/rule-decisions.json`. This step's check runs the rules step's check again first, so a change
that makes the models fail their own style, or a change without a reason, stops here.
