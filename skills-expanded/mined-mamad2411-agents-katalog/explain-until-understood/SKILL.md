---
name: explain-until-understood
description: >-
  Explain a subsystem, design, diff, or unfamiliar tool to someone in the session until they can
  answer questions about it unaided, assuming they know nothing, and close on a self-test. Writes no
  files. Not for a repo-wide orientation file (use ceh-codebase-explanation:explain-codebase).
argument-hint: "[what to explain]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Explain until understood

The target is a reader who can answer questions about the system **without the explanation in
front of them** — not a reader who followed along. Following along is the failure mode that feels
like success, on both sides.

The output is the conversation. By default this skill writes no files; the exceptions, each on
request, are in _Output_ below.

## Procedure

### Who you are explaining to

**Assume the reader is new here and knows nothing about the subject.** Not that they are
inexperienced — that it is their first day on this project. They have never seen this repo, this
tool, or the work that led to it, and they do not know the words any of it uses.

Project-local names are terms of art like any other, and get defined at first use: a service, a
table, an internal acronym, a file everyone refers to by a nickname.

The cost is asymmetric, and that is the whole argument. Explaining above someone burns a full round
trip, and they may not say they are lost. Explaining below someone costs one paragraph they skim in
three seconds.

**State the floor you are building from in one line before you start** — "assuming you have written
Python but never used asyncio" — so the reader can raise it. Then build strictly upward from it.

- **The floor scales like everything else** (see _Scale to the ask_). It belongs on anything running
  the full procedure; a one-sentence answer carries its floor implicitly. Spending half a short
  answer on a preamble about what you assume is its own way of explaining badly.
- **Raise the floor only on evidence:** they say so, or they ask a question that uses the vocabulary
  correctly. A job title is not evidence. Being in a terminal is not evidence. A term pasted out of
  an error message is not evidence they know it.

**Scale to the ask.** The full eight-step procedure is for something the reader has to hold in their
head afterwards — a subsystem, a design, a release's worth of change.

- **A small ask earns a small answer.** "What does this regex do" earns a sentence, and at most the
  wrong-conclusion framing from step 6. Running all eight steps on a one-line question is its own
  way of failing to explain.
- **Two steps resist shrinking.** Step 1 never scales away at all — the one-sentence answer is only
  right because you opened the file. Step 5 shrinks rather than disappears: two numbered lines
  tracing one real input beat a paragraph describing the mechanism in general.
- **The other end has a limit too.** When the subject is larger than one explanation can carry, name
  the slices, explain one, and say what the others are. A compressed tour of all of it leaves the
  reader able to answer nothing.

### Steps

Step 1 is what _you_ do. Steps 2 and 4–8 are what the _reply_ contains, in that order. Step 3 is
both: you run the command, and its output goes in the reply next to the claim it supports.

Do not narrate the doing. "I read the modules and ran the validator" is process, and the reader
asked for an explanation. Pasted output is evidence, not narration.

1. **Read the real thing first.** Never explain from memory, from a design doc, or from a summary —
   including a design doc you wrote yourself earlier in the session. A design doc says what the
   author decided; the source says what is true today.

   What "the real thing" is follows the ask:

   - **Repo code** — open the modules, read the docstrings, follow the call sites.
   - **"What changed since `<tag>`"** — the diff. Commit messages come after it and are labelled as
     claimed intent, never the changelog.
   - **An unfamiliar tool** — its own `--help`, plus one run against a real fixture, read-only per
     step 3. A tool with no read-only run is read, not run: say so, and mark its behavior
     unverified.

   The ban covers the _subject_ only. A step 2 foundation may come from your own knowledge — say
   plainly that it does. If the subject has an artifact you cannot reach, say so before explaining
   anything, and mark every claim that follows as unverified. A subject with no artifact to reach in
   the first place — a protocol, a general technique — is a different case: say once that it comes
   from knowledge, and do not label every line.

2. **Establish foundations before the specific case.** Name the two to four ideas the whole
   explanation rests on, and state each one plainly before you use it.

   - **Choose them for the reader's floor, not for the subject.** The foundation you owe them
     usually sits one layer _below_ where the subject's own documentation begins, because that
     documentation was written for someone who had already chosen to use the thing.
   - **The test for any term:** would a sharp person outside this field know it? If not, it is
     either a foundation to state here or a word to replace.
   - **Two tells that a definition is missing:** writing "as you know", and reusing a term
     introduced earlier in the session.
   - **More than four foundations means the subject is too big** for one explanation. Name the
     slices and explain one (see _Scale to the ask_).

   Everything after this step stands on these. A foundation that missed makes the rest unreadable
   rather than partly readable, which is the single most common cause of an explanation that has to
   be repeated. You do not stop mid-reply to check: aim step 8's first self-test question at a
   foundation, which is where a missed one surfaces cheapest.

3. **Verify by running.** Run the tool, the command, the throwaway script, and paste the real
   output. "semgrep found 2 hits, lines 22 and 23–27" beats "semgrep would flag the network call."

   - **Read-only runs only.** A command that changes state is not an illustration, and the contract
     requires it be requested first.
   - **Cheap runs only.** A throwaway snippet or one targeted command needs no permission. A full
     test suite, a build, or a repo-wide lint stays contract-gated even though it changes nothing —
     ask for it, or cite output that already exists.
   - **Where you cannot or may not run it,** say so in the same breath as the claim.

4. **Draw structure and time; write everything else.** Prose is bad at nesting, ordering,
   before/after, and data flow. Use a picture for those and a table or list for the rest — a diagram
   of a list is noise.

   - **Draw in ASCII in the conversation.** It renders on every surface. Mermaid renders only where
     the reader's client draws it, and a terminal does not, so Mermaid is for a file that will be
     viewed rendered.
   - **ASCII means the plain keyboard characters and nothing else:** `- | + / \ < > ^ v` for lines
     and arrowheads, `[ ]` or `+---+` for boxes. No box-drawing glyphs, no `→`, no emoji — those
     depend on the reader's font and terminal encoding, and one glyph that fails to render turns the
     picture into noise exactly where the picture was carrying the meaning.

   ```
   request --> [ router ] --+--> [ handler A ] --> db
                            |
                            +--> [ handler B ] --> queue
   ```

5. **Walk one concrete case, numbered, end to end.** Take a single real input — one request, one
   file, one commit — and number what happens to it, one hop per line, with the real names and the
   real values.

   This is the default form, not a fallback: prefer a walked case over a general description
   wherever a concrete case exists. A reader who cannot follow the general rule can almost always
   follow one worked case, and then read the rule back off it.

   - **Pick the ordinary case,** not the interesting edge — the edge is step 6's job.
   - **Mark any value you made up,** as against one that came out of the run in step 3.
   - **The walk and the step 4 picture describe the same thing** and must agree. Where they cannot,
     the picture is wrong.
   - **Where nothing concrete can be walked** — a naming convention, a policy — say so and skip the
     step rather than inventing a trace.

6. **Frame failure as "what you would wrongly conclude".** Not "this is a bug" but "you would read
   that as reconcile routing to verdict, and go debug the rule ladder — and the rule ladder is
   fine." The wrong conclusion is what makes a subtle failure memorable.

   The step frames a failure the code actually has. If reading it turned up none, say the path is
   straightforward and move on — an invented failure mode breaks the evidence rule.

7. **Show the tempting-but-wrong alternative.** For any non-obvious design, name the simpler thing
   a reader would reach for and show precisely where it breaks. This is what turns "the code does
   X" into "the code _must_ do X".

8. **Close with the transferable rule, then a self-test.** One sentence the reader can apply to the
   next case — "pass context explicitly wherever someone else's scheduler owns the task" beats
   re-listing the three call sites where it is passed. Follow it with two to five questions they
   should now be able to answer unaided.

   - **A wrong answer is the miss signal.** Go to the ladder below, but re-explain only the idea
     that answer got wrong rather than the whole subject. A wrong answer about a step 2 foundation
     goes straight to attempt 4.
   - **Silence is not a signal.** It reads as "understood" as often as "lost", so end the turn
     rather than re-explain unprompted.

### When it did not land

First ask _what kind_ of miss it was, because three of the four are not ladder moves:

- **"Wait, what?" with nothing specific.** They lost the thread of your last message, not the
  subject. Re-pitch it: its one point in two or three plain sentences, no new terms, then ask
  whether that is the part that broke. If the re-pitch misses too, it was one of the kinds below.
- **A word you never defined.** Define it and say the same thing again at the same level. This is
  not an attempt on the ladder — you owed them the definition and the explanation was otherwise
  fine.
- **A foundation you did state, that did not take.** Go to attempt 4 directly, per step 8. The
  words were on the page and still did not land, so restating them is what already failed.
- **They have the words and cannot assemble them.** This is what the ladder below is for.

Do not restate the same explanation with more words. Drop a level and change the representation.

Only the representation changes. A re-explanation still closes on step 8's rule and self-test,
pitched at the scale the first attempt was — one question is enough for a small ask — because the
self-test is how you find out whether the new form landed.

Locate yourself on the ladder by the **form of the last attempt**, not by how many messages have
passed. Invoked cold after a miss, look at what the previous explanation actually was and take the
next row down.

- **A table is attempt 1, not attempt 3.** It lays out facts side by side but carries no structure,
  ordering, or flow, so a reader stuck on _how the parts connect_ gains nothing from one.
- **Prose carrying one diagram is attempt 1** — that is step 4 done right, not the ladder skipped
  ahead. Prose carrying a numbered walk of a single case is attempt 1 too: that is step 5.
- **Attempt 2 is the _whole explanation_ rebuilt as numbered steps,** not one worked example sitting
  inside prose. Attempt 3 is that rebuild with a picture on every step.

| Attempt | Representation                                               | If it still misses                     |
| ------- | ------------------------------------------------------------ | -------------------------------------- |
| 1       | prose, tables, and code references                           | go to step-by-step                     |
| 2       | numbered steps, one idea each                                | go to pictures                         |
| 3       | one ASCII diagram per step                                   | stop adding pictures — go to attempt 4 |
| 4       | define the foundations, then rebuild the explanation on them | ask which sentence broke               |

A miss at attempt 3 is almost never a missing detail. It is a foundation the first three attempts
all assumed. Go back to step 2 rather than adding more pictures.

## Rules

- **Evidence over inference.** Unclear purpose is written as "purpose unclear — checked imports and
  call sites, no references found", never guessed at. Never invent a responsibility.
- **Don't paste code.** A signature or a three-line snippet is the ceiling. A literal that _is_ the
  behavior — a constant, a threshold, a regex, a status string — is quoted verbatim and does not
  count against that ceiling; paraphrasing a value loses the mechanism.
- **Describe what exists today**, not what was planned or is half-built.

### Plain language

The register of the explanation is a choice, and the default drifts technical because the source
material is technical. Steer it deliberately.

- **Concept first, name second.** Say what the thing does, then attach its name: "the call hands
  the work off and returns before it finishes — that is what `async` means here." The reverse order
  lets the name stand in for the idea, and the reader nods at a word.
- **Define every term of art at first use, in the same sentence.** Not a glossary at the end, not a
  link. If the definition needs more than a clause, it was a step 2 foundation and belongs there.
- **Prefer the shorter, older word** — "use" over "leverage", "start" over "instantiate", "check"
  over "validate". The exception is where the precise word _is_ the mechanism (a `422`, `SIGTERM`,
  the actual function name); those stay verbatim, like the literals in _Rules_.
- **One new idea per sentence.** A sentence carrying two unfamiliar things fails on both, and the
  reader cannot tell you which one broke.
- **An analogy is a bridge, not a claim.** Give one, then say where it stops being true. An
  unbounded analogy becomes a wrong mental model that outlives the explanation.

### Honesty

The output style's honesty rules apply unchanged. One addition specific to explaining:

**"Not documented" and "I did not check" are different answers.** "Not documented" is a claim, and
only a grep earns it; with no grep the honest answer is "I did not check". Report which of the two
you are giving. The same holds for "this path was never verified end to end" — often the single
most valuable line in the whole explanation.

### Anti-patterns

- Explaining from a design doc because it is well written. If the reader had understood the doc,
  they would not be asking.
- Opening at the level the subject's own documentation is pitched at, which already assumes the
  reader chose to use the thing.
- Treating a term as known because the reader typed it, when they may have copied it out of an
  error message.
- Reusing a term introduced earlier in the session as though it is now known.
- A diagram where a table would do; Mermaid where the reader has a terminal; box-drawing or
  arrow glyphs where a plain `+`, `-`, `|` and `-->` would have rendered anywhere.
- Describing a mechanism in general terms when one real case could have been walked step by step.
- Answering "is this documented?" with yes or no instead of a grep result per file.
- Ending on the mechanism instead of the rule of thumb.
- Restating attempt N as attempt N+1 with more words.

## Output

### Persisting the explanation

Explaining slides naturally into writing it down. Keep the boundary explicit:

- **Default: nothing is written.** The explanation is the reply.
- **Scratch notes** under `.agents_workspace/` are in scope when the user asks for something to
  re-read later.
- **A learning workspace**, when the user asks to learn something over several sessions ("teach
  me this over the week", "keep track of what I know"). See below.
- **Anything that lands in the repo** — `docs/`, README, architecture notes — is a different job.
  Hand off to the skill that owns it (see _Hands off to_) rather than writing it here.
- **One case has no owner:** a developer-facing explainer of a single subsystem, written into
  `docs/`. It is neither a whole-repo orientation file, nor product documentation, nor a decision
  record. Say that plainly instead of forcing a fit — `ceh-codebase-explanation:document-architecture` is
  the nearest, and it will reshape the material into diagrams plus Key Decisions rather than
  preserve the explanation you just gave. Having named the gap, write the file yourself if the user
  still wants it, keeping the explanation's shape. This is the one repo path this skill may write.

### Learning workspace

Opt-in only. Keep one file per subject at `.agents_workspace/learning/<subject>.md`, so a later
session starts from what the reader already knows instead of from zero:

```markdown
# Learning: <subject>

**Goal:** <what the reader wants to be able to do, in their words>
**Next:** <the one thing the next session explains first>

## Terms

| Term | Definition, as the reader put it back |
| ---- | ------------------------------------- |

## Rules of thumb

- <each transferable rule an explanation closed on>

## Self-test

| Question | Last answer          | Date       |
| -------- | -------------------- | ---------- |
| <q>      | unaided / missed / — | YYYY-MM-DD |

## Open questions
```

- **On load**, read the file before explaining anything. Ask two Self-test questions first, the
  missed ones before the oldest, and record each answer. A term the reader cannot use unaided goes
  back into the next explanation as a foundation, not as review.
- **After each explanation lands**, add its terms, its rule, and its self-test question, and
  rewrite Next. Record a definition only once the reader has said it back in their own words:
  the file tracks what they know, not what was said to them.

## Hands off to

| Want                                                      | Use                                                                                                                      |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| A repo-wide orientation file, component by component      | `ceh-codebase-explanation:explain-codebase`                                                                              |
| Diagrams and decision records that live in the repo       | `ceh-codebase-explanation:document-architecture`                                                                         |
| Docs for people who _use_ or _operate_ the product        | `ceh-documentation:write-guides-and-runbooks` for the tasks, `ceh-documentation:write-project-docs` for a whole docs set |
| Someone in this session needs to understand something now | **this skill**                                                                                                           |
