---
name: urdu-voice-director
description: Recover the living Urdu scene, then refine and direct it for believable spoken delivery while preserving meaning, character, relationships, cultural context, pronunciation intent, and caption cleanliness. Use for naturalizing written or Roman Urdu; preparing conversation, children’s or family material, fiction, drama, dubbing, narration, explainers, education, accessibility, animation, games, news, public speech, religious or moral work, poetry, code-switching, or TTS; correcting ambiguous vowels or consonant substitutions; and adapting clean Urdu to an exact speech model without making provider markup the source text.
---

# Urdu Voice Director

Recover the scene already present in the Urdu, then make it believable to the ear. Literary life means presence, implication, rhythm, and restraint—not ornament or extra plot.

## Contract

- Preserve the original meaning and dramatic function.
- Preserve relationships, age, register, titles, religious wording, and code-switching.
- Do not invent facts, motives, memories, or emotions. Make affect audible when it is traceable to the words, dramatic function, supplied context, performance brief, or source attribution; if the reading is non-unique, label it as a performance option rather than a source fact.
- Do not rewrite a line merely to show activity; an unchanged line is a valid result.
- Keep clean spoken text separate from directions, context notes, captions, and TTS markup.
- Check the exact provider, model, surface, locale, and voice against current first-party documentation before using provider controls. Mark unresolved fields and listening-dependent behavior honestly.

Treat the Urdu source—not an English or Hindi paraphrase—as canonical. Do not infer gender, locale, relationship, pronunciation, or delivery range when the source leaves it open. Ask only when competing readings would materially change the result; otherwise state a conservative assumption.

## Load only what the task needs

Do not preload every reference. Open the smallest relevant set and follow a cross-link only when that issue actually appears.

| Task or issue | Read |
|---|---|
| Everyday conversation, children, Roman Urdu, or general naturalness | [spoken Urdu](references/spoken-urdu.md) |
| Age, `آپ`/`تم`/`تُو`, kinship, titles, religious wording, or code-switch identity | [relationships and register](references/relationships-and-register.md) |
| Intonation, focus, emphasis, or speech rhythm | [conversational prosody](references/conversational-prosody.md) |
| Pause, cutoff, interruption, word search, or filled pause | [hesitation and pauses](references/hesitation-and-pauses.md) |
| Fiction, drama/dubbing, narration, documentary/explainer, character voice, news, public speech, or devotion | [literary dialogue and performance modes](references/literary-dialogue.md) |
| Poetry, ghazal, nazm, quiet recitation, or mushaira | [poetry and recitation](references/poetry-and-recitation.md) |
| Ambiguous reading, diacritics, names, numbers, acronyms, or mixed-script text | [pronunciation](references/pronunciation.md) |
| TTS, a named provider, or synthesis-ready output | [provider capabilities](references/provider-capabilities.md) |
| Review, regression testing, benchmarking, or skill maintenance | [evaluation](references/evaluation.md) |

Examples are optional. Load only the closest one under [`examples/`](examples/). Maintainers use the assets under [`evals/`](evals/) and run `npm run validate:skill`.

## Recognize the performance

Do not direct all Urdu alike.

- **Everyday conversation:** interaction, relationship, and thought units lead.
- **Fictional dialogue:** source-supported subtext and character voice lead.
- **Drama or dubbing:** objective, stakes, interaction, timing, and authorized emotional range lead.
- **Audiobook narration:** viewpoint, narrative continuity, and quoted speech must remain distinct.
- **Documentary or explainer:** information, argument, listener orientation, and credible emphasis lead.
- **Animation or game character:** character continuity, playable energy, and medium constraints lead.
- **News reading:** informational grouping, names, numbers, and calm authority lead.
- **Public speech:** argument, audience address, and rhetorical structure lead.
- **Religious or devotional speech:** wording, reverence, pronunciation, and genre boundaries lead; never manufacture sermon-like intensity.
- **Poetry recitation:** metre, syllable length, rhyme, refrain, izafat, and semantic phrasing constrain delivery.
- **Mushaira performance:** the same poetic constraints remain, but audience address, anticipation, repetition, and response create a different event from quiet reading.

## Set the performance treatment

Choose a delivery range—**restrained**, **grounded** (default), or **heightened**—and separately choose **naturalistic** (default) or **stylized** treatment. These are production choices, not facts discovered in the source. Wider range or stylization must be supported by the words or brief and never licenses new inner life, facts, or audible events. When uncertain, keep a grounded-naturalistic baseline and label alternatives as performance hypotheses.

## Make the smallest justified intervention

Read the whole passage. For each turn, choose one: leave unchanged, refine words, direct delivery, or do both. A good refinement sounds spoken without erasing the speaker. Direction should name an audible action or change, sit immediately before the affected beat, and remain sparse.

Keep pauses functional. A conversational boundary, hesitation, cutoff, interruption, word search, and filled pause are not interchangeable. Punctuation can suggest structure but cannot by itself determine a performance.

For synthesis, audit every materially ambiguous reading and every critical consonant contrast. Put required diacritics or phonetic controls only in a separate provider pronunciation copy; keep canonical words and captions unchanged. A diacritic can resolve a vowel reading, but it cannot repair `ڑ`→`ر`, `ٹ`→`ت`, or another consonant substitution.

## Return only useful layers

Always provide **clean spoken Urdu**: the final audible words, free of directions and provider syntax. Preserve speaker labels when useful.

Add only what the request needs:

1. **Directed rehearsal script** — the same words plus clearly non-spoken, provider-neutral cues.
2. **Portable synthesis plan** — speaker, canonical utterance, delivery note, pause/beat, and pronunciation note.
3. **Provider adapter** — exact target metadata, canonical utterance, provider pronunciation copy/override ledger when needed, supported controls, identical clean caption copy, and explicit listening tests.

Provider markup never becomes the source text. If no exact target is known, keep direction outside the utterance instead of guessing syntax.

## Final check

Compare the result with the source. Reject meaning drift, relationship or register drift, invented inner life, provider leakage into clean text, and undocumented controls. For poetry, scan the verse and inspect pause sites before directing it. For consequential or synthetic output, require a native-Urdu listening pass with the selected voice; text review cannot prove pronunciation or prosody.
