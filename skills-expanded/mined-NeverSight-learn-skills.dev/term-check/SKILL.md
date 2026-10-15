---
name: term-check
description: Probe whether a candidate term carries its meaning alone, by asking three models to guess it from a bare scenario. Use when naming a field, an enum value, a table or a glossary word and several candidates are in play ("carry or carryOver", "does this name read", "which word is clearer").
---

A name earns its place when a reader who has never seen the docs guesses right. This probe measures that: one scenario, three candidate terms swapped in, three models, two runs each. Three arms are the default — when only two candidates are on the table, propose a third synonym and run all three.

## Steps

1. **Write the scenario** to a file: the domain in two sentences, the shape around the word, and `{TERM}` where the candidate goes. State only what a stranger needs to place the word, because a scenario that names the meaning under test answers its own question. Close with a fixed answer shape: one sentence plus `confidence: high|medium|low`, so the runs stay comparable.
2. **Run the probe**:
   ```
   bash .agents/skills/term-check/probe.sh <scenario-file> <term-a> <term-b> <term-c>
   ```
   Six runs per term, in parallel, about one minute.
3. **Score every run** against what the word must convey: right, partly right, or wrong. Keep each model's own confidence line beside its score.
4. **Report the scenario, then the table.** Quote the scenario exactly as the models got it, in a fenced block above the table, so the reader judges the question before the answers.

   One row per model and run, one column per term. Every cell reads `<icon> (<confidence>) -> <guess>`: the score as ✅ right, ⚠️ partly right or ❌ wrong, the model's own confidence word, and its guess in a few words, so the reader sees what the model understood. Right answers decide first, confidence second.

   | Model | `term-a` | `term-b` | `term-c` |
   | --- | --- | --- | --- |
   | Opus, run 1 | ✅ (medium) -> moves it to the next day's plan | ❌ (low) -> deletes it at the seal | ⚠️ (low) -> keeps it somewhere unnamed |

5. **Offer another round when the winner is weak.** A winner is weak when it takes no `high` confidence, or when it wins only because the other arms collapsed. Say so, name 3 or 4 fresh synonyms, ask the user whether to run them, and sharpen the scenario in the same breath, because a thin scenario holds every confidence down.

Done when all six runs per term carry an icon, a confidence and a guess, the scenario stands above the table, and the table names a winner, a tie, or a weak winner with a fresh set of synonyms offered.

## Reading the result

| Outcome | What it means |
| --- | --- |
| All arms score alike | First suspect the scenario, not the words: outcomes this similar usually mean the scenario hints too strongly and answers its own question. Re-read it, name the leaking phrase, and ask the user whether to run another probe with the scenario changed. Only when the scenario is clean does a tie mean the word does no work — then pick on other grounds: brevity, parallel with its siblings, the glossary |
| One arm wins | That word carries the meaning. Take it |
| All arms score badly | The words are fine and the shape is wrong. Fix the shape, then probe again |

## Limits

Each run starts from an empty conversation in a neutral directory, so no repo doc reaches the model. The global `~/.claude/CLAUDE.md` still loads. It holds no domain vocabulary and it loads for every arm alike, so a comparison between arms holds while an absolute score does not.

A model guesses from the whole scenario, so a scenario that leaks the answer scores every candidate right. Arms that tie are the signal to re-read the scenario before trusting the tie.

The confidence word is the model's own report, written because the scenario asks for it. No number stands behind it and nothing calibrates it, so read it as a tone and let the score carry the verdict. The measured number is the agreement rate: how many of the runs land on the same meaning. Raise the run count in `probe.sh` to sharpen it.
