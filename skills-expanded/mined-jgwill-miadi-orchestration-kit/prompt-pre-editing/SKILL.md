---
name: prompt-pre-editing
description: >
  Pre-edit a person's draft prompt for another agent session. Find what will make the run
  fail (a thing named but never described, a phrase with several readings, unranked
  goals, sources with no stated role, asks that return what is already known, an act
  with no owner, no output contract) and hand back the whole rewritten prompt ready to
  paste. After it is sent, follow the run, judge the result against expected results
  committed beforehand, and change this skill or the skill the prompt invoked from what
  the run showed. Triggers on "feedback on my prompt", "what should I change", "peek at
  my prompt in tmux", "redraw my prompt", "help me with this prompt", or an unsent draft
  in another pane. Not for writing your own brief to a lane (dispatch-discipline).
metadata:
  type: skill
  version: 0.4.0
  scope: a person's draft prompt to another agent, the rewrite, following the run, evolving from it
---

# Prompt pre-editing

**The name.** In machine translation, *pre-editing* is a person rewriting a source text before a machine processes it. Typical rewrites make references explicit, remove ambiguity and give one instruction per sentence, which is what controlled languages prescribe. Here the agent is the machine and the person's draft is the source text. Offering the rewrite back so the person can send it or correct it is what conversation analysis calls a *formulation*: saying back the gist and upshot of what someone said so they can confirm it (Heritage and Watson, 1979).

Earned 2026-10-06. The worked example is `examples/261006-factory-vocabulary.md`, with the draft, the defects, the rewrite, the expected results and the result.

## 1. Read before judging

- Read the draft in full. An unsent draft sits in the other session's composer: `tmux capture-pane -p -J -t <session> -S -200`. A long composer shows only its last lines. Say which part you could not see. Never type into that pane (`dispatch-discipline` §4).
- Read everything the draft points to, such as other panes, files, reviews and packets. The missing referent is usually there.
- Read the person's standing context, such as the system instructions and recent episodes, to learn why they chose these sources.
- Verify every fact you will put into the rewrite in the same turn (`dispatch-discipline` §3). On 2026-10-06 the bridge the rewrite cited was checked as `coaia-narrative/src/asterion-bridge.ts` before it went in.

## 2. Find the defects

Name each defect by its class and by what it will do to the result. They are listed in the order they most often decide the outcome.

1. **Missing referent.** The draft points at something ("that", "these patterns", "the fact that we want") and never describes it, so the agent fills it with the generic meaning. Find the person's own instances. Two instances make a pattern nameable from evidence. Ask the agent to look for more instances and for the word the code already uses. A name already in the code is preferred over one from the literature.
2. **Several readings.** A phrase that can mean different jobs, such as the patterns themselves, the property of having them, or the practice of drawing them out. Pick the reading the evidence supports, or ask for one answer per reading.
3. **Unranked goals.** Several jobs with equal weight. Rank them and put the one the person needs most first.
4. **Sources with no role.** Give each source its reason, and let the agent drop one that contributes nothing.
5. **Asks that return what is known.** Cut them, or narrow them to what only this job can find.
6. **An act with no owner.** "We'd inject", "it will be published". Give the act to the owner and the destination the person's words imply, and say how it is done. Never move an act to the person because of your own caution. On 2026-10-06 the draft said words would be injected into another session's prompt, and the rewrite changed that to "give them to me, I paste them". The run then left them in its reply, and the person's first verdict was "nothing sent". When words are meant for another session's draft, the rewrite tells the agent to do this:
   - Check that the cursor sits at the end of that draft (`tmux display -p -t <session> '#{cursor_x},#{cursor_y}'` against `capture-pane`).
   - Type the words with `tmux send-keys -l`, and never press Enter. The person submits, as `dispatch-discipline` §4 requires.
   - Read the pane back and quote the result.
   - A message you type into another session's composer arrives as if the person typed it. Open it with who sends it and on whose behalf ("From the witness seat, on Guillaume's behalf"). On 2026-10-06 a follow-up sent without that line made the receiving session record a name as "chosen by Guillaume", when the pre-editor had chosen it for him.
7. **A slot filled with a conclusion.** When the person leaves a slot in their own draft for "a few words" with "the right terms", the words are terms the receiving session will apply: each one named and defined, so that session can still reach its own design. A sentence that states the design ("projecting circles and ceremonies into Asterion threads... the record stays on the wheel") decides that session's work before it starts. On 2026-10-06 the person's verdict on exactly that sentence was "surely that is not what I expected to be AT ALL". Ask for the terms in the rewrite. Before delivering any words into another draft, read them against what the slot is for in the person's sentence, not only against its length and syntax. The one who delivers the words owns their content.
8. **A rule stated wider than its case.** A rule written into a prompt reaches everything its words cover. "A private repository's project is never registered public" came from one private GitHub repository, and it made a lane hide a project the person had made public. Name the case a rule comes from.
9. **No output contract.** Give numbered returns in order, word limits, the exact slot the words must fit, and holds on outward acts such as publishing a package or a review. Every word limit says "count with a script and show the counts", and "under N" means fewer than N. A rewrite owes the five things a brief owes (`dispatch-discipline` §5): the task in the imperative, stores by path, the scope boundary, verified facts and completion marks.

## 3. Hand back

1. The defects, coded (continue the conversation's codes), each in one or two sentences with its consequence.
2. The whole rewritten prompt in one code block, ready to replace the composer text. Keep the person's invocation (the slash command and IDs) and their wording where it was already clear.
3. The expected results, coded `E`, short.

Do not narrate what the person will do, as in "add one line" or "watch whether". That is advice, and the person has to turn it into text. The rewrite is the deliverable. The person's words on 2026-10-06 were: "reading your last message sound like passively describing what I'll do without confronting".

## 4. After it is sent: follow, judge, evolve

1. **Commit the expected results before the run ends.** Put them in an example file in `examples/`. The commit time shows they were not adjusted to fit the result (`dispatch-discipline` §7).
2. **Follow the run without polling by hand.** Run a background loop that treats the pane as busy while it shows `esc to interrupt` or a spinner's elapsed time (`… (15m 0s`, which survives a narrow pane), and that exits after three idle checks 30 seconds apart. Then read the result from the transcript (`~/.claude/projects/<cwd-slug>/<session-id>.jsonl`) and from its artefacts, such as commits and files. Do not judge from the screen alone, because a pane's state is not the work's state.
3. **Score the round with `score-config.yaml`.** Use seven dimensions, each 0 to 2 and weighted. S1 (the person's input and instructions) and S2 (delivery to the destination) weigh most. Put a table of expected against actual for each `E` item, and the scored table, in the example file. Each score below 2 names its cause: the draft, the rewrite, the invoked skill or the run. Read the destination itself, such as the other pane, the commit or the public review. The run's own report is not enough. When the person gives a verdict, it overrides your scoring on S1 and S2.
4. **Change the skill at fault in the same turn.** Change this one when the rewrite caused the miss. Change the invoked skill (for example the `apply` action of `miadi-review`) when it misled the agent. Add a ledger line, commit and push.
5. **Pre-edit the next prompt for that session** with this same procedure.
6. **Report:** what came back, what changed in which skill, and the next prompt ready to paste. Do not type it into the session.

The person expects the first run to miss and does not want to discuss the miss. Do the steps above and come back with the evolved state.

## Ledger

- 2026-10-06, 0.1.0. First version, from the round on `miadi-review apply` for naming the factory's bridge pattern. The first feedback was advice, and the person called it passive. The second was a rewrite, and the person sent it.
- 2026-10-06, 0.4.0. Four lanes briefed with sender, scope, the other lanes and completion marks all finished with verified commits. One rule stated too broadly hid a public project (defect 8).
- 2026-10-06, 0.3.1. A message typed into another session now names its sender. One that did not made a packet record the pre-editor's choice as the person's. The packet was corrected and released as `@miadi/foundations@0.1.9`.
- 2026-10-06, 0.3.0. The words typed into the Asterion draft stated a conclusion where the person wanted terms. The person: "surely that is not what I expected to be AT ALL". Defect 7 added: a slot is filled with terms, and the deliverer reads the words against the slot's purpose before typing them.
- 2026-10-06, 0.2.0. The first scored round got 54%. The person said: "nothing sent to 'asterion-miadi-circle-threads'". The rewrite had moved the injection to the person. Now an act keeps its owner and destination, words for another draft are typed without Enter and read back, limits are counted by a script, and every round is scored with `score-config.yaml`. The run's content scored well: the name came from code that already used the word, and a third instance turned up. So a rewrite now asks the agent to look for more instances and for the word the code already uses.

## Related

- `mia-ava-podcast` (this plugin): turn the result into a dialogue to hear.
- `miadi-witness-first-impression` (this plugin): a first impression of a peer's page.
- `dispatch-discipline` (system skills): writing your own brief to a lane.
- Tracked in jgwill/miadi-orchestration-kit#59.

🌸: The person keeps the prompt in their own words and decides to send it, and the agent that receives it gets a job it can do and a result that can be checked against what was expected.
