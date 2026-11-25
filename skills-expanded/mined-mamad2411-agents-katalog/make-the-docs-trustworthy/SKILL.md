---
name: make-the-docs-trustworthy
description: >-
  Correct, create, or remove written material so a later reader can rely on it:
  documentation that no longer matches the system, a fact about to be written down
  a second time, prose restating what a config file or command already prints, a
  records folder that has drifted, or a decision worth recording so it stops being
  re-argued. Prose no human has read counts as a hypothesis, not a source. Use
  when the user says "the docs are out of date", "readme still says the old flow",
  "where does this go", "write this down", or "should this be an ADR". Not for
  judging docs inside a change under review, explaining an existing document, or
  looking up a third party documentation.
---

# Make the Docs Trustworthy

**Core principle.** A reader must be able to act on this page without checking it against the system first.

- **A second copy of a fact destroys that.** The two disagree in the end, and neither one announces itself as the stale one.
- **The weight sits in *Search before you write*.** Everything after it is what to do once the search has answered.
- **You opened this in the middle of something.** This is how to do that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## Search before you write

- **You MUST look for the fact first.** Where it already exists, edit it there.
- **A second copy adds no source.** It adds a sentence that will disagree with the first one.
- **The reader cannot tell which of the two is current.** That is the whole cost, and it lands on someone else.
- **Where something already prints the fact, write the pointer and stop.** A manifest, a config file, a generated block, a command's own help.

## Write only what cannot be found by looking

- **Keep the convention nobody wrote down.**
- **Keep the reason a thing is the way it is.**
- **Keep the trap that has caught people.**
- **Drop whatever one command or one file already answers.** That is restatement, and restatement is stale the moment it is written.

## Which rules to read

**This table is a gate, not a checklist.** Match the left column against what you are about to write, correct, or remove.

- **One rule per row.** The match sets where to start.
- **The change class sets what is permitted.** Name it before the edit.
- **Run the search this gate demands before any rule.** It can make the write unnecessary.
- **Read both rows where a claim matches two.** Reading is the cheap half. Writing the wrong thing is the expensive half.
- **Supersede where a rule would delete a decision record.**

| If you see... | Read |
| --- | --- |
| a fact about to be written down, or one that already appears in two places and they disagree | `rules/one-place-for-a-fact.md` |
| prose describing what a manifest, configuration, generated block, or command's own help already states | `rules/restatement-is-drift.md` |
| a claim that something is out of date, with no change to anchor it to | `rules/staleness-without-a-diff.md` |
| a file that has absorbed content beyond the job its name implies, or that nobody can describe in one line | `rules/one-artifact-one-job.md` |
| a document being cited as a reason, which no human is known to have read | `rules/unreviewed-prose.md` |
| a constraint invisible in the code, a deliberate deviation, or an alternative readers keep re-proposing | `rules/record-what-code-cannot-show.md` |
| a recorded decision whose answer has changed, or a page whose subject no longer exists | `rules/supersede-or-delete.md` |
| no established location, numbering, or heading scheme for what you are about to add | `rules/match-the-existing-shape.md` |

**Discriminators.**

- **One-place against restatement.** Split by what the duplicate is. Another piece of prose, against an artifact that renders the fact already.
- **Staleness against one-artifact.** Split by symptom. A sentence that is untrue, against a file whose job cannot be stated.
- **Record against supersede.** Split by moment. The first time it is written, against every time after.

**Default stance.**

- **Search for the fact before writing it**, and edit it where it already lives.
- **Write only what cannot be found by looking.** Anything a command already prints becomes a pointer.
- **Say what you chose not to write**, so the omission is a decision rather than a gap.

## Prose nobody has read is not a source

- **Do one of two things before citing a document as your reason.** Re-derive its claim from the system, or say plainly that you did not.
- **You SHOULD re-derive rather than disclaim** where the claim decides anything. Disclaiming is the honest option, not the cheap one.
- **You MAY take either one.** The silent third option is the one that costs.
- **That silence turns one wrong sentence into a convention.**
- **Agent-written prose piles up fastest and gets trusted first.** That is backwards.

## Settle the claim against the running system

- **This skill runs when nothing points at what changed.** Someone says the docs are wrong, and there is no diff to anchor it to.
- **Settle each claim yourself.** Run the command the page describes. Open the path it names.
- **Check the identifier is still exported.** Follow the link and see where it lands.
- **Report it confirmed or refuted, and name the thing that settled it.**
- **Judging docs inside a change is a review's job.** There a diff supplies the anchor, and findings are reported rather than applied.

## Name the change you are making

| Class | When | What it requires |
| --- | --- | --- |
| correct | the prose says something untrue now | cite what makes it untrue |
| add | the fact has no home yet | the search above decides where |
| supersede | a recorded decision changed | the old record stays, with a pointer forward |
| relocate | the fact is in the wrong file | leave no surviving copy behind |
| delete | the subject itself is gone | never for a decision record |

- **Deleting a page whose subject was removed is correct.** It is part of the removal.
- **Deleting a record because its answer changed is not.** It destroys the evidence that the old answer was once right.
- **The next reader then argues it again from nothing.**
- **Propose any deletion, and any new file, with what depends on them named.** Correcting and relocating need no proposal.

## Keep the verbatim set through any rewrite

- **A rewrite, a compression, or a move preserves these exactly.** Code, paths, identifiers, commands, error strings, numbers, versions, and frontmatter.
- **Frontmatter is the one that fails quietly.** A model told to preserve it rewrites it anyway.
- **Lift it out before the change and put it back after.**
- **Check the result against the original.** Never trust that the instruction worked.

## What to produce

```
Claim        "the setup guide is wrong"
Resolution   refuted for steps 1-3: ran them, they work.
             confirmed for step 4: it names a flag the command's own
             help no longer lists.
Changes      correct   <setup page>:22, replace the flag with a pointer
                       to the command's help
             delete    <old setup page>: its subject was removed here
Left alone   <troubleshooting page>: every command in it still runs
Not written  the retry default: the config command already prints it
Unreviewed   none
```

- **One instance, not the set.** What generalises is the shape.
- **Every claim gets a verdict, and every change gets a class.**
- **What you chose not to write is said out loud.**

## Do not skip this when

- **The fact seems new.** That is what every duplicated fact seemed like once.
- **The page is small.** A small page is read whole and believed whole.
- **You are only fixing a typo.** That is when the surrounding claim goes unchecked.
- **Nobody asked.** Prose nobody checked is what the next session will cite.

## Routing

- **The table above selects the rule.** Read it in full, and say which one you opened, in one line.
- **Whether a decision is worth recording at all is settled by the change-review rules, not here.** This skill owns writing it, placing it, and keeping it true.
- **A direct instruction from the user outranks anything here.**
