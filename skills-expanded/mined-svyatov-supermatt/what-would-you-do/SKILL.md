---
name: what-would-you-do
description: "Explain the question you just asked and recommend an answer, with the case for and against each option."
argument-hint: "[which question, or the part I do not follow]"
disable-model-invocation: true
license: MIT
---

"What would you do?" The user answers a question you asked with this one, most often because they do not yet understand the problem well enough to choose. Take the most recent question or decision you put to them in this session; the arguments, if any, name another one, or the part they do not follow.

1. No open question in this session: say so and stop.
2. Do the legwork the answer needs: read the code, config, docs, or output the question touches. Done when every claim you make about an option rests on something you read or ran in this session.
3. Explain the problem in plain words: what is being decided, why it came up, and what changes in the project with each answer. Define every term from the question the user may not know.
4. List the options as O1, O2, and so on: the ones you offered, plus any better one the legwork turned up. For each: what it does, why pick it, and why not (cost, risk, what it rules out later, how hard it is to reverse).
5. Recommend one in so many words ("I recommend O2") and give the deciding reason. When the answer hinges on something only the user knows (a preference, a deadline, a plan), name it and say which option each answer leads to.
6. Hard question: the options stay close after the legwork and a wrong pick is costly to reverse. Give your lean anyway, then offer a jury: one ready-to-run `/jury <question>` line for Claude linked installs or Cursor, `/supermatt:jury <question>` from the Claude plugin, `$jury <question>` in Codex, or `/skill:jury <question>` in OMP. State the question, options, and constraints in full, so the panel needs nothing from this session. The user runs it.
7. End on the recommendation. The user decides; act only on their answer.
