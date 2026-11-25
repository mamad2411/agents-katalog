---
name: prompt-builder
description: Draft, refine, or debug a prompt through structured questioning. Use when the user is writing a prompt or system prompt, says a prompt is not working or gives inconsistent results, asks how to phrase something for a model, or wants an existing prompt improved.
---

# Prompt Builder

Produce a prompt that reliably does what the user needs. Your job is to surface
the requirements they haven't stated, not to write something plausible from an
underspecified request.

## First, work out which situation you're in

**Building from scratch** — they have a goal, no prompt yet. Start at step 1.

**Debugging** — they have a prompt that misbehaves. Skip to *Debugging an
existing prompt* below. Do not rewrite it from scratch; find the specific cause
first.

## Building from scratch

**1. Get the shape of the task.** Ask what the prompt should do, and — the part
people skip — what a good output looks like versus a bad one. One concrete
example of each is worth more than a paragraph of description.

**2. Fill the gaps.** Most underspecified prompts are missing the same things.
Ask about whichever of these are unresolved and would change the output:

- Who reads the output, and what do they do with it?
- Length, and format — is it parsed by code or read by a person?
- What should happen when the task can't be completed?
- What's out of scope — what should it refuse or ignore?
- Is this one call, or does it run at volume against varied input?

Ask about the ones that matter. Don't run the whole list as an interrogation.

**3. Draft it,** using the structure in `reference/anatomy.md`. Show the draft.

**4. Test it against the ugly case.** Ask for a real input, ideally a messy one.
Run the prompt if you can. Clean invented examples hide the ambiguities that
break things later.

**5. Iterate on what actually broke.** Change one thing at a time so you know
what did the work.

## Debugging an existing prompt

Check these in order — the first three cover most cases:

1. **A contradiction.** Two instructions that can't both be satisfied. "Cite
   every claim" plus "one sentence" plus "never speculate" leaves some inputs
   with no legal answer, and the model picks arbitrarily.
2. **An example contradicting an instruction.** Demonstrated behavior beats
   stated behavior. If the instructions say 50 words and the examples are 200
   words, you get 200. This is genuinely hard to spot because the instruction is
   right there looking obeyed.
3. **No escape hatch.** If the prompt implies an answer exists, one will be
   produced. Add an explicit failure output with a detectable token.
4. **Underspecification.** Would two competent people produce the same output
   from this prompt? If not, the variance is the ambiguity reflected back.
5. **Buried constraints.** Long unstructured lists get partially applied. Group
   under headers.
6. **Stale scaffolding.** Elaborate chain-of-thought instructions on a model
   that reasons natively, or workarounds for failures the current model no
   longer has. Try deleting them.

## Rules

- **Never hand back a prompt full of bracketed placeholders you could have
  asked about.** One or two genuinely user-specific slots is fine; a template
  skeleton means you skipped the questions.
- **Don't add flattery, urgency, or fake stakes.** "You are a world-class
  expert", "this is critical to my career", offers of tips. These are folklore.
  A role that changes the substance of the answer is different and is worth
  including.
- **Keep it as short as it can be.** Every line should be doing work. If you
  can't say what a line changes, cut it.
- **Suggest evals when it matters.** If this prompt runs at volume or in
  production, three test cases beat another round of wordsmithing. Offer to
  write them.

## Output

Give the final prompt in a fenced block, ready to copy. Follow it with a short
note on which parts are load-bearing and what to adjust first if it
underperforms.

## Reference

- `reference/anatomy.md` — the parts of a prompt and what order to put them in
- `reference/techniques.md` — structure, examples, reasoning, structured output
- `reference/anti-patterns.md` — what to remove and why
