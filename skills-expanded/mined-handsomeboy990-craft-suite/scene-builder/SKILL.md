---
name: scene-builder
description: Builds strong scenes: character objective, escalating conflict, costly outcome, reaction, dilemma, decision. Spatial anchoring, subtext, rhythm, irreversibility. Use to write a scene, repair a flat one, or verify that a scene changes the state of the narrative.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: [writing-constitution, chapter-architect]
  outputs: [written-scenes, scene-sheets]
---

# Scene Builder

Builds scenes that stand on their own: objective, conflict, cost, consequence.
This skill is the main production unit of the novel.

## 1. Working definition

A scene is a continuous block of time and place in which a character wants
something, meets resistance, and leaves in a different state from the one they
entered. Without a change of state there is no scene, only filler.

## 2. Canonical structure

### Action block

1. Objective: what the point of view character wants to obtain here and now,
   stateable in one sentence as an infinitive.
2. Conflict: what opposes it, escalating across at least three stages.
3. Outcome: failure, costly success, or success that makes the situation
   worse. Plain success is reserved for fewer than one scene in six.

### Reaction block

4. Reaction: immediate emotional response, bodily before mental.
5. Dilemma: two bad options, stated explicitly or not.
6. Decision: a new objective, which becomes the objective of the next scene.

The reaction block can be compressed to three lines in a thriller, or occupy a
whole scene in an intimate novel. It is never removed, or events follow one
another without being lived.

## 3. Writing protocol

### Step 1: fix the value

Write the value that swings, and its sign: freedom to captivity, trust to
suspicion, debt to settlement. One value per scene.

### Step 2: enter late, leave early

Start as close to the conflict as possible. Cut the arrival, the greeting, the
settling in. End on the last meaningful element, with no scene epilogue.

### Step 3: anchor the space in three touches

Three concrete elements are enough to establish a place: a material, a sound,
a physical constraint. The physical constraint pays best, because it creates
play: a door that does not close properly, a heat that forces someone to
stand, a floor that makes movement audible.

### Step 4: place the bodies

Know at all times where each character is, what their hands are doing, what
they are looking at. A dialogue scene with no physical blocking becomes two
voices in a void.

### Step 5: write in subtext

What characters say covers what they want. Method: write the explicit version
first, where everything is said, then rewrite it removing every sentence that
names the stake directly, replacing it with an object, a gesture or a detour.

### Step 6: set the internal rhythm

- Long sentences for duration, short sentences for impact.
- Reduce average paragraph length as tension rises.
- Insert a breathing space after a peak, never before.
- Avoid more than two consecutive descriptive paragraphs in a tense scene.

### Step 7: verify irreversibility

At the end of the scene, something can no longer be undone: a word spoken, a
door crossed, information received, an object broken. Otherwise the scene is
rewritten or merged.

## 4. Scene types and their traps

| Type | Dominant trap | Correction |
|---|---|---|
| Information dialogue | frontal exposition | make the information given reluctantly |
| Confrontation | linear escalation | insert a de-escalation attempt that fails |
| Action | list of gestures | anchor on a partial objective every five lines |
| Journey | summary with no stake | keep only what changes a relationship |
| Reunion | sentimentality | place an unresolved prior disagreement |
| Revelation | explanatory speech | make the one who knows resist |

## 5. Exit checks

- The scene has a stateable objective.
- The conflict escalates across at least three stages.
- The final state differs from the initial one.
- The reader knows where the bodies are.
- No character says what they could show.
- The constitution is respected on dialogue and flashbacks.

## 6. Auto-critique

Score 0 to 5: clarity of objective, escalation of conflict, irreversibility,
sensory anchoring, subtext, rhythm, accuracy of dialogue, economy, originality
of treatment, emotion produced.

Threshold: no axis below 3, average at least 3.8. Any scene under the
threshold is rewritten entirely, not patched.

## 7. Interfaces

- Upstream: `chapter-architect`, `character-psychologist`.
- Lateral: `dialogue-master`, `immersion-director`, `narrator`.
- Review: `quality/self-critique-protocol`.
