---
name: shard-writer
description: Give a routine a write-what-where memory contract so tonight's run leaves something tomorrow's run can read. Use when asked to add memory to a routine, define what a routine should record, or make runs build on each other. Writes routine memory shards only — never posts, sends, or publishes anything.
---

# Shard writer

Turn a routine that remembers nothing into one run that writes and one later
run that reads. This skill exists because routines that write nothing are chat
with a subscription: the run happens, the context window closes, and next
week's run re-learns everything from zero — including the mistakes.

Use this skill for routine memory only: one routine in, a write-what-where
contract out, verified by a later run reading it back.

## The rule that matters more than the memory

**A run that writes nothing leaves nothing.** Every routine run ends with a
shard write or a stated reason it had nothing worth keeping ("no change since
last run" is a write, not an excuse — it tells the next run the check
happened). A routine whose shard is empty after three runs does not have a
memory problem; it has a contract nobody follows. Never write credentials,
tokens, or account identifiers into a shard; `${VAR}` names only, values
never.

## When to use

- Someone asks to give a routine memory, record run results, or make runs
  build on each other.
- A routine keeps re-learning the same facts, repeating the same mistakes, or
  re-asking the owner the same question.
- A new routine needs its memory contract defined before its first scheduled
  run.
- Do not use for chat history, conversation summaries, cross-routine
  knowledge bases, or anything that leaves the routine's own shard — one
  routine, one shard, tonight's scope only.

## Inputs and access

1. **Routine** — the required input: which routine, what it does, how often
   it runs. One routine per contract; a contract covering two routines
   covers neither.
2. **Write-what** — the short list of what this routine records: decisions
   made (with date), observations with their source, open questions with
   owners. At most five categories; a sixth is a second shard auditioning.
3. **Write-where** — the shard the routine owns: name, location, and the
   rule that no other routine writes there. Reads others, writes its own.
4. **Retention** — how long entries live and what supersedes what: dated
   entries, newer findings marked SUPERSEDED on older ones, never silent
   deletion. A shard that only grows is an archive, not a memory.
5. Access is the routine's own readable sources plus its shard. Integrations
   read through configured variables (for example `${ROUTINE_API_KEY}`);
   never paste values, names only. If a source needs access you were not
   given, record it as unreachable and move on.

## Sequence

1. **Scope** — name the routine, its shard, and the write-what list (at most
   five categories). Confirm the shard belongs to this routine alone.
2. **Write** — at end of run, append dated entries: what was decided or
   observed, the source behind it, what stays open and who owns it. Skip
   raw dumps; a shard holds conclusions with pointers, not transcripts.
3. **Read-back** — the next run opens by reading the shard and stating what
   it is acting on from the last run. A run that cannot say what the shard
   told it did not read the shard.
4. **Supersede** — when a new finding contradicts an old one, mark the old
   entry SUPERSEDED with the date; do not edit history into agreement with
   the present.
5. **Verify** — confirm two writes a later run actually read (see
   Validation). A contract unverified by read-back is a diary, not memory.

## Validation

- Two writes exist that a later run demonstrably read: the later run names
  the entries it acted on.
- Every entry carries a date and a source or owner; entries without either
  are demoted to notes or cut.
- No credentials, tokens, or account identifiers appear in the shard —
  `${VAR}` names only.
- No routine writes to another routine's shard; cross-references name the
  shard and date, never copy its contents over.
- Two runs the shape was built for: a steady-state run (writes "no change,
  check ran on <date>") and a finding run (writes the decision, its source,
  and the open question with its owner).

## Output

A write-what-where contract with:

- Routine, shard name and location, run cadence.
- **Write-what**: the category list (at most five) with one example entry
  each.
- **Write-where**: the shard boundary — this routine writes here, reads
  these others, touches nothing else.
- **Retention**: entry lifetime and the SUPERSEDED convention.
- Read-back proof: the two writes a later run read, named with dates.
- What could not be verified: unreachable sources, entries demoted to notes.

## Boundaries

- Write boundary: routine memory shards only. This skill never posts, sends,
  publishes, or edits anything outside the routine's own shard — no shard
  text leaves this skill for any other surface. Any use of shard contents
  elsewhere belongs to a separate routine with its own approval.
- Never paste credentials, tokens, or account identifiers into a contract or
  a shard; `${VAR}` names only.
- Never report shard contents beyond what the reader can already open. If a
  shard needs access you cannot read, record it as unreachable and move on.
