---
name: map-shaping
description: >
  How to shape a mindmap.io map well: what belongs in the root node, when to
  branch versus append, when to fan a node out with auto-expand, and which node
  type to reach for. Use whenever you are building or growing a map with the
  mindmap.io tools, before deciding where a new node goes.
---

# Shaping a mindmap.io map

The tools tell you what each operation does. This tells you where to put things.

A map is worth building only if its shape carries meaning. A transcript of a
conversation does not become a map by being drawn as one.

## The one mechanic everything follows from

**A node's context is its ancestor chain, root first.** When a node generates,
the model sees the root, then each node down the path to it, then the node's own
prompt. It sees nothing else.

Two consequences do all the work:

- **Depth accumulates.** A child inherits everything above it. A node six levels
  down carries six nodes of context whether or not they help.
- **Siblings are invisible to each other.** Two branches off the same parent
  never contaminate each other. That is isolation you can use on purpose.

So placing a node is not filing. It is choosing what the model will read.

## The root node is the brief

Every descendant inherits the root. It is the only node with that reach, which
makes it the right place for the things that should hold everywhere:

- the subject, stated the way you would state it to a colleague
- the audience and the purpose, if either changes the answer
- standing constraints: the stack, the market, the word budget, the reading level
- source material short enough to be worth carrying everywhere

Make it a `data` node, not a `prompt`. The root frames the map, it does not ask
a question.

What does not belong there: anything that is true of one branch only, and
anything long enough to crowd out the actual questions. A 4,000-word document in
the root is paid for by every single generation on the map. Put it in a `data`
node on the branch that needs it.

There is no separate "map instructions" call in the agent tools, and that is
deliberate. The root already reaches every descendant, and it is visible on the
canvas, where a hidden system prompt would not be.

## Branch or append

Ask one question: **does this depend on the answer above it?**

**Append** (child of the node you just ran) when the next step builds on what
came back. Follow-ups, "now go deeper on the second point", refinements,
critiques of an answer. The chain is the reasoning, and the accumulated context
is exactly what makes the next answer good.

**Branch** (new child of a shared ancestor) when the next step is a separate
line of inquiry into the same subject. Comparisons, alternatives, the four
options you are weighing, the same question asked of three different sources.
Branching keeps each line clean, and it is what makes the finished map readable:
a map with five branches shows five things it considered.

The failure mode is a map that is one long chain. It reads as a chat log, the
context grows until early nodes get trimmed, and every answer is coloured by
questions that had nothing to do with it. If you have appended four times and
the last two did not need the first two, those two wanted to be a branch.

The opposite failure is a fan of ten shallow children that each restate the
root. Breadth without depth is a list, not a map.

## Node types

- **`prompt`** is a question to run. It is the only type that generates.
- **`data`** is content you place yourself: a topic, a pasted document, a
  finding worth keeping, a conclusion you want the branch below it to inherit.
  A data node is how you inject context at a chosen depth rather than at the
  root.
- **`note`** is annotation: your commentary on a node, for a human reader.

Writing a conclusion back into the map as a `data` node is one of the highest
value things an agent can do. It makes what you learned inheritable by
everything you run next, and it leaves the person a map that states its
findings instead of one they have to re-read to reconstruct.

## Fanning out

Auto-expand asks the model for follow-up questions from a node's context and
adds them as children, ready to run. It does not run them, it does not recurse,
and it costs a generation each time you call it.

Reach for it when you have a completed answer and **do not yet know** which
questions matter. It is a discovery move.

Do not reach for it when you already know what to ask. Writing the three
questions you actually want is faster, cheaper, and better than generating four
and running the two that fit.

When you do expand:

- Read the answer first. Expanding an unread node fans out from a direction you
  have not checked.
- Steer it. An untargeted expansion drifts toward the generic.
- Two or three is usually right. Four children each spawning four is sixteen
  generations, and nobody reads sixteen answers.
- Run the children you want and delete the ones you do not. A queued node that
  is never run is clutter with no content.

Recursion is yours to drive, which means the depth budget is a decision you make
rather than one the tool makes for you. Two levels deep with three good branches
beats four levels of everything.

## A shape that works

For research, the shape that reliably reads well:

1. A root `data` node holding the subject and the constraints.
2. Three to five `prompt` children, one per real dimension of the question.
   These are your branches, and they are invisible to each other, so each gets a
   clean run at its own angle.
3. Under each, one or two levels of appended follow-ups where the answer earned
   them. Not every branch deserves the same depth.
4. A `data` node under each branch holding what that branch concluded.

The map is then readable top-down by someone who was not there, which is the
point of building it in a map instead of a thread.

## Finishing

When the person will share or revisit the map, publish it and hand back the
link. A map nobody opens was a slow way to write an answer.

Check before you build: if the person wanted a paragraph, write the paragraph. A
map earns its cost when the structure is part of the answer.
