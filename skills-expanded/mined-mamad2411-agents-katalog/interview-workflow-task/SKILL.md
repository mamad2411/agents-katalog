---
name: interview-workflow-task
description: >-
  Load this skill when repeated work must come out of someone's head before it is built: ask the
  nine questions a workflow needs and write the answers to a spec file. Trigger on "interview me
  about this task", "help me spec out this workflow". Produces the spec only.
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Interview a workflow task

Turn "we run this same pass every release" into a spec that `build-agentic-workflow` can design
from without guessing. This skill asks and records. It does not design, and it does not emit an
artifact.

Questions 8 and 9 are the two people skip, and they are the
two whose absence corrupts data or sends mail twice.

## Procedure

Triage first, in one line, against the **repetition test**: will the same steps run again in the
same shape, with only the input changing between runs? A workflow exists for that reason alone. A
one-off, or a **spike** done once or once more to learn how it goes, fails the test and gets no
spec, so say so and stop. A task whose steps change shape from run to run fails it too, because a
fixed flow would encode the wrong steps next time. Any task that passes gets the full interview
below, even when it looks small, because questions 8 and 9 matter most on the tasks that look too
small to ask them.

1. Read the spec file and this conversation, then label every row (Start from what already exists).
2. Ask only about the rows that fail, using the nine questions below and the rules under How to ask.
3. Record each answer under its fixed heading in the spec file (see Output).
4. Check the file against Done when, then hand off.

### Start from what already exists

**Read the spec file first if there is one**, along with anything the user already said in this
conversation. Then label every row before asking anything: each of the nine headings, and each
numbered step under 3, gets `ok`, `gate`, or `fails` plus the reason. Label the rows that look
fine too — the one that gets missed is the second soft proof in a section whose first one already
caught your eye. Ask only about the `fails` rows, and open by naming the ones you are skipping so
the user can correct you. Then amend those headings in place — never rewrite the file from scratch,
or you drop the answers that arrived before you did.

Arriving from `build-agentic-workflow` is the common case, and it arrives precisely because some
rows failed. Re-asking all nine there is the failure mode this section prevents.

### The nine questions

1. **The moment.** What happens right before you would want this to run? This becomes the trigger,
   and it must be a verb. If the answer is a topic rather than a moment, the artifact will never
   auto-fire and the interview is not done.
2. **The manual procedure.** Walk it step by step in the order you actually do it.
3. **Preconditions and proof.** Per step: what has to be true before it starts, and how do you know
   it worked? An answer you cannot check is not a gate — test every step's proof against that, not
   just the one that reads softest. Where a step genuinely turns on human judgement, record an
   explicit human go/no-go gate instead: who is shown what, and that a no-go stops the run. Vague
   confidence in the outcome is not a gate; a named person deciding is.
4. **Data flow.** Per step: what does it read, what does it leave behind, and which _later_ step
   reads that? Name the producing step, not just the artifact. And what does a run start from: an
   argument passed at invocation, or something the previous run left behind?
5. **Tooling.** Which CLIs, credentials, services, or network access does each step need?
6. **Done.** What is true at the end that was not true at the start?
7. **Interruption.** Does this run in one sitting, or can it stop partway and need resuming?
8. **Re-runs.** If it fails halfway and you start over, which steps would do damage if they ran a
   second time? Name them — this is the question people forget, and it is the one that corrupts data.
   An answer about _order_ rather than repetition — harmless twice, harmful early — is a
   precondition, not a re-run hazard: tighten that step under 3 and cross-reference it here. The next
   skill reads heading 8 as a run-once guard, so an ordering hazard left here alone is never gated.
9. **Irreversible steps.** Which steps touch something outside this machine that cannot be taken
   back: sending mail, charging a card, publishing, deleting?

### Done when

Check this the way you opened — row by row against the file as written, not against your memory of
what you fixed. Every one of the nine headings exists with an answer or an explicit `Declined`
under it, question 1's answer is a moment, every proof under 3 is either something a command or a
file check can settle or a declared human go/no-go gate, and every artifact read under 4 names the
step that produces it.

## Rules

### How to ask

- Write each answer into the spec as you get it, not at the end. An interview that dies halfway
  should leave eight answers on disk, not zero.
- Batch enumerable choices through `AskUserQuestion`; ask the open-ended ones plainly.
- **Never answer for the user, least of all when the answer looks obvious.** This applies to each of
  the nine separately, not just the two that read as risky. An unanswered question is recorded as
  unanswered: not as "none", not as what the procedure plainly implies, and not as an assumption of
  your own. Reading step 4, seeing that it mails finance, and writing that under 9 is the loud
  version, and relabelling it "partial" or "assumed" does not make it theirs — they may know the
  address is a dead alias. Deriving question 4's data flow from the steps listed under 2 is the
  quiet version, and the one that gets through, because the chain reads plausibly and nobody
  re-checks whether step 3's input has a producer at all. Silence on 8 becomes a workflow with no
  re-run guard, silence on 9 becomes one that publishes without pausing, and a guessed 4 becomes one
  whose steps hand each other data the user never said they hand.
- **A decline is not a gap.** When the user says they do not know or will not answer — most often
  on 8 or 9 — write `Declined` under that heading with their words, and stop asking. Re-asking a
  declined question is how the interview and the builder's intake gate bounce off each other
  forever. The builder has a conservative fallback for a declined row; it has none for a missing
  one, which is why the two are recorded differently.
- Push back on an answer that fails its own check above, then re-ask. A recorded answer that cannot
  be checked is worse than a gap, because the next skill trusts it.
- **No human to answer** (a headless run, or called by another agent): label every row as usual,
  ask nothing, and leave each `fails` row recorded as unanswered with the question it needs. Never
  fill it in yourself. Hand the spec path back and list the unanswered rows, so a person can answer
  them in one sitting.

## Output

### Where the spec goes

`$CEH_WORKFLOW_BUILD_DIR/<name>-workflow-spec.md`, defaulting to `.agents_workspace/`. Use a
provisional slug until the name is settled, then rename the file — otherwise a second interview
overwrites the first one's spec.

### The spec file

Fixed headings, in this order, one per question. The consumer gates on them by name, so keep all
nine as written and in this order — an unanswered question keeps its heading and says so underneath.
Anything you want to say that no heading covers belongs in the reply, not in a tenth section.

```markdown
# <name> workflow spec

## 1. Moment

## 2. Manual procedure

## 3. Preconditions and proof

## 4. Data flow

## 5. Tooling

## 6. Done

## 7. Interruption

## 8. Unsafe to re-run

## 9. Irreversible steps
```

Under 2, 3, and 4, keep the steps numbered and use the same number for the same step across all
three — the next skill reads them as one table, and a step that is `3.` in one section and `4.` in
another silently attaches a gate to the wrong step.

Never write a credential into the spec. Record where it lives: a secret-manager key, an env var name.

## Hands off to

- Hand the spec path to `ceh-workflow-builder:build-agentic-workflow`, or tell the user that is the
  next step if they did not arrive from there.
