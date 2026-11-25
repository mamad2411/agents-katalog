---
name: table-me
description: Turn prose already discussed in this conversation into a comparison table, so the differences between the options become visible at a glance. Use whenever the user says "table me", "/table-me", "put that in a table", "tabulate that", "compare those side by side", or "I can't hold all this in my head". Also use, without being asked, when you are about to explain three or more items that differ along the same dimensions, or when the user sounds lost in a list you just gave them.
---

# Table Me

Prose makes the reader do the diffing. To compare four options across three
dimensions, the reader holds twelve facts in their head and subtracts. A table
does that work on the page.

So the value of the table is in the cells that **differ**. Everything here
protects that.

## Find the rows and the columns

Read back over what we discussed. Two questions:

- **Rows**: what are the things being compared? These are the units the user
  will act on: options, tools, files, approaches, candidates.
- **Columns**: on what dimensions do they actually differ? Take these from the
  prose. If the prose weighed cost and effort, those are columns.

If there are many dimensions and only two or three items, transpose it. Put the
items across the top and the dimensions down the side. A table that is 3 wide
and 9 tall reads better than one that is 9 wide and 3 tall in a terminal.

## Cut uniform columns, keep sparse ones

A column where **every** row says the same thing tells the reader nothing, and it
costs width a useful column needs. Cut it, and state the shared fact in one line
above the table instead. Padding a table with uniform columns is an easy way to
make it look thorough while making it harder to read.

Uniform is not the same as sparse, and this is where the rule is easy to
over-apply. A column holding two real values and two gaps still discriminates:
the reader learns which options were assessed on that dimension and which were
not. That is information, and moving it into prose below the table hides it. Keep
the column and mark the gaps.

Cut a column when the cells are the same. Keep it when the cells differ, even if
some of them differ by being empty.

Watch for the uniform failure in rows too: two rows with identical cells are one
row with two names.

## Cells are labels, not sentences

Budget about six words per cell. A cell holding a full sentence means one of
three things: the column is really two columns, the content belongs in a note
under the table, or the material was never table-shaped.

Keep the whole table under about 110 characters wide so it survives a normal
terminal. In practice that is three to five columns. Reach for a note below the
table rather than a sixth column.

## Do not fill gaps you cannot source

An empty cell is glaring, and the pull to fill it with something plausible is
strong. Resist it. Once material sits inside a grid, the reader assumes all of
it came from the discussion, so a guess in a cell reads as a finding.

- `—` means the prose never covered it.
- `?` means it is genuinely unknown or was left open.
- If you add something from your own knowledge rather than from our
  conversation, mark the cell and say so in one line under the table.

## Order the rows by the decision

Sort by whichever column carries the verdict: recommendation, cost, risk,
priority. Mention order is almost never the useful order. If nothing ranks,
group related rows together so the eye can compare neighbours.

## Then say what the table shows

Follow the table with one or two lines naming the pattern the grid makes
visible: the split, the outlier, the row that wins. Do not restate the cells.
If the table makes something obvious, the reader still benefits from you
confirming they read it right.

## Two table shapes, and when neither fits

Most requests want a **comparison** table: items down the side, the dimensions
they differ on across the top. That is the default above.

Some material has no competing items but still has repeated structure. A request
flow, a pipeline, a migration in phases. That takes an **enumeration** table: one
row per step, columns for what the step does, what it needs, what breaks if it
fails. This is a real table, so build it. Do not refuse a sequence just because
nothing is being compared. Say in one line that the rows are stages rather than
alternatives, so the reader does not try to pick a winner from them.

Refuse only when neither shape fits, which is rarer than it first looks: a single
thing explained in depth, or a narrative with no repeated structure to make rows
from. Then say so plainly in a sentence and name what fits instead:

- One thing in depth → keep the prose, or the `eli5` skill for a simpler pass
- A flow you want to *see* rather than read → a diagram
- A flat set with nothing in common → a plain list

Build the thing you are recommending in the same reply where you can. An answer
that only names a better format costs the user another turn to get it.

## Scope

Default to the topic just discussed, not the whole session. An argument narrows
it: `/table-me the four findings` means those, not everything since we started.

## Example

Prose we had been discussing:

> Redis is fast and we already run it, but everything is in memory so a restart
> loses the lot. Postgres we also run; it survives restarts and we know it well,
> though it is slower for this. DynamoDB survives restarts too and needs no
> operations work from us, but it is a new vendor and the latency is unproven.

Table:

| Store | Survives restart | Already run it | Speed here |
|---|---|---|---|
| Postgres | yes | yes | moderate |
| Redis | no | yes | fast |
| DynamoDB | yes | no | ? unproven |

Postgres is the only row with no `no` and no `?`. Redis trades the one property
we said we needed for speed we have not shown we need.

Note that "operations work" never became a column. Only DynamoDB's entry
mentioned it, so it goes in a line under the table if it matters, rather than
becoming a column that reads `—` for two of three rows.
