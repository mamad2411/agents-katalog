---
name: dialogue-master
description: Writes and validates dialogue to French publishing standards: guillemets, en dashes, incises, attribution by action, conflict of objectives, subtext, voice differentiation, multilingual handling. Use to write dialogue, correct its typography, or when every character speaks alike.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: [writing-constitution]
  outputs: [conformant-dialogue, voice-report]
---

# Dialogue Master

Writing and validating dialogue to French publishing standards. This skill has
authority over every line of speech produced by the tree.

Sections 1 and 2 are French typographic conventions. Sections 3, 4 and 6 are
structural and apply in any output language. When
`language.creative_output` is not French, replace sections 1 and 2 with the
target language's own conventions, stated explicitly rather than assumed.

## 1. Dialogue typography

### 1.1 Main system

French guillemets to open and close the dialogue, an en dash at the head of
each following line, one paragraph per speaker.

```
« Tu as vu l'heure ?
– J'ai vu l'heure.
– Et tu es rentré quand même.
– Je suis rentré quand même. »
```

Non-breaking spaces inside the guillemets and before double punctuation marks.

### 1.2 Light system

Dashes alone, without guillemets. Permitted, but held across the whole
manuscript. The two systems are never mixed.

### 1.3 Prohibitions

- Straight or English quotation marks.
- Em dash.
- Two speakers in the same paragraph.
- A line opened with a capital after an incise that did not end the sentence.

## 2. Incises

### 2.1 Form

Between commas, with subject and verb inverted.

```
« Je pars demain, dit-elle.
– Demain, répéta-t-il, comme si le mot appartenait à une autre langue.
```

Punctuation: if the line ends with a question or exclamation mark, that mark
replaces the comma but the incise stays lowercase.

```
« Tu pars ? demanda-t-il.
```

### 2.2 Economy

- Neutral verbs in four cases out of five: dit, répondit, demanda, reprit,
  ajouta.
- No manner adverb attached to a speech verb.
- No impossible verb: one does not smile a sentence, nor shrug a line.
- One incise per three lines at most.

### 2.3 Attribution by action

Replace the incise with a gesture that carries information. The gesture must
change the scene, not furnish it. A character who nods adds nothing; a
character who sets down their cup without having drunk adds everything.

## 3. Dramatic construction

### 3.1 Fundamental law

A dialogue is a conflict of objectives conducted through speech. Each
character wants something from the other. If both want the same thing and
agree, the scene does not need to be written.

### 3.2 Techniques

- Evasion: answering beside the question. Three consecutive evasions create
  immediate tension.
- Delay: deferring the expected information with an action or a digression.
- Pickup: taking the other's word and turning it around.
- Interruption: cutting before the end, marked by a suspension.
- Silence: a line of narration replaces the answer. Silence is a reply.
- Asymmetry: one character speaks in long sentences, the other in
  monosyllables.

### 3.3 What to cut

Greetings, introductions, confirmations, repetitions of what the reader knows,
courtesies with no stake, first names used at the head of a line.

## 4. Voice differentiation

Seven levers, chosen per character and recorded:

1. sentence length;
2. register, from formal to familiar, without phonetic transcription;
3. professional or social vocabulary;
4. relation to questions: asks them, or never does;
5. relation to the conditional and to politeness;
6. a syntactic tic, discreet, used at most once per page;
7. rhythm, clipped or ample.

Mandatory test: mask the incises. If attribution becomes impossible, the
differentiation has failed.

## 5. Multilingual dialogue

- A sentence in a foreign language must be understood from its immediate
  context.
- No translation in parentheses.
- No systematic italic when the language is that of the milieu represented:
  the italic exoticises it.
- A character who thinks in one language and speaks another shows it through
  syntax, not through isolated words.

## 6. Monologue and long speech

A speech longer than ten lines must be interrupted at least once by a physical
reaction from the listeners, a change of place, or an objection. Otherwise it
becomes a platform and the reader disengages.

## 7. Exit checks

- Typography conformant.
- One paragraph per speaker.
- Neutral speech verbs in the majority.
- No manner adverb on a speech verb.
- Voice test passed.
- No information delivered solely for the reader.
- Every line shifts the balance of the scene.

## 8. Auto-critique

Score 0 to 5: typographic conformity, voice differentiation, subtext, economy,
rhythm, spoken credibility, absence of exposition, accuracy of incises,
tension, at least one memorable line.

Threshold: no axis below 3, average at least 3.8.

## 9. Interfaces

- Upstream: `character-psychologist`, `scene-builder`.
- Review: `quality/proofreader`, `quality/literary-editor`.
