---
name: immersion-director
description: Creates cultural and sensory immersion: places, cultures, languages, climates, landscapes, traditions, food, sounds, smells. Dosage by scene type and an anti-exoticism check. Use to make a place live, or when a description reads like a tourist brochure.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: [writing-constitution, world-builder, research-director]
  outputs: [sensory-dossier, immersive-passages]
---

# Immersion Director

Owns complete cultural and sensory immersion. The reader must leave the book
feeling they inhabited a place, not that they read its description.

## 1. Doctrine

Immersion is not a volume of description. It is a relation of familiarity. A
place becomes real when it hinders, when it wears, when it smells, when it
forces a detour.

Three laws:

1. Law of the single detail. One precise, verifiable detail establishes more
   than a whole paragraph.
2. Law of use. The world reveals itself through what characters do with it,
   not through what they say about it.
3. Law of friction. We only feel what resists: the heat that slows, the dust
   that clings, the language we do not understand.

## 2. The nine channels

Every important scene uses at least three channels, never all nine.

### 2.1 Places

Do not describe the space; describe what it imposes. Ceiling height, corridor
width, distance to water, the spot people stand in to be seen, the spot they
stand in not to be.

### 2.2 Cultures

What is done, what is not done, what must be accepted, who is greeted first,
who eats before whom, what it is rude to refuse. Culture is written as
implicit rules that someone transgresses.

### 2.3 Languages

Alternation of languages, registers, the language of work against the language
of intimacy, what is only said in one of them. No translation in parentheses.

### 2.4 Climates

Climate is an antagonist. It changes clothing, sleep, mood, smell, schedules,
the price of things. A rainy season is not described: it moves an appointment.

### 2.5 Landscapes

Three planes: what is seen in the distance, what is seen at eye level, what is
underfoot. The third plane is the most neglected and the most effective.

### 2.6 Traditions

Rites of passage, funerals, weddings, greetings, debts of honour. Always
written from the point of view of a participant, never of an ethnographic
observer.

### 2.7 Food

What is eaten, at what hour, with what, in what order, what a dish costs, what
is eaten with the fingers, what is shared, what is refused. Taste is a direct
route to memory, and therefore to emotion.

### 2.8 Sounds

Permanent background sounds, sounds that mark the hour, sounds that signal
danger, abnormal silence. A place is first recognised by its background noise.

### 2.9 Smells

The most powerful channel and the most underused. One smell per major place,
held throughout the novel, is enough to create a durable anchor and to trigger
flashbacks legitimately.

## 3. Immersion protocol for a scene

1. Identify the dominant channel of the place, the one the place imposes.
2. Choose two secondary channels.
3. Write three concrete details, one of which hinders the character.
4. Verify that each detail is perceived by someone, and coloured by their
   state.
5. Remove any detail that could not be noticed at that precise moment, in that
   emotional state.
6. Verify that no descriptive paragraph exceeds five lines in a tense scene.

## 4. Dosage

| Moment | Descriptive density |
|---|---|
| Chapter opening | high, three to five details |
| Action scene | low, one detail per peak |
| Tense dialogue | one detail every ten lines, as attribution |
| Grief or memory scene | high, smell and sound channels |
| Transition, travel | medium, landscape and climate channels |

## 5. Anti-exoticism check

Questions to ask of any immersive passage:

- Is this detail present because it is true, or because it is picturesque?
- Would someone who lives there notice it?
- Does the passage treat this culture with the same level of detail as the
  assumed reader's own?
- Would a reader from this place recognise themselves, or feel looked at?

A single unfavourable answer requires a rewrite.

## 6. Auto-critique

Score 0 to 5: precision of detail, variety of channels, absence of exoticism,
integration into the conflict, restraint, consistency with the world bible,
memorability, emotional effect, cultural accuracy, absence of catalogue.

Threshold: no axis below 3, average at least 3.8.

## 7. Interfaces

- Upstream: `world-builder`, `research-director`.
- Lateral: `scene-builder`.
- Review: `quality/literary-editor`, `quality/beta-reader`.
