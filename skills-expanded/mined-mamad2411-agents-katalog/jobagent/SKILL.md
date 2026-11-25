---
name: jobagent
description: Drive the JobAgent job-application pipeline — find postings, ingest them, read the form's questions, draft an application kit, fill it, and submit. Use when the user asks to find jobs, apply to a posting, work the application queue, or asks what needs their input on an application. Requires the JobAgent daemon (`pnpm run jobagent serve`).
---

# JobAgent (Claude Code)

**Read `skills/jobagent/SKILL.md` first and follow it.** That is the shared spec
for every platform: the verb table, the judgment rules, and the gate protocol.
This file only covers what is specific to Claude Code.

Do not restate the pipeline's rules here or in your replies. Run the verb,
report what it says.

## Platform specifics

**Searching (step 1 of the shared spec).** Use the `WebSearch` tool. Prefer
direct posting pages over aggregators, and pass each candidate through
`jobagent assess <url>` before ingesting — assess loads the page, so filter by
hand first rather than assessing forty search hits.

**The two gates.** Use `AskUserQuestion` at each one. This is the single place
where being a good Claude Code citizen and following the spec coincide: the gate
needs a real decision from a real person, and `AskUserQuestion` is how you get
one without burying it in prose.

- *Kit gate* — show the resolved fields with their provenance and the
  unresolved ones, then ask whether to approve. Offer the unresolved questions
  as the thing needing their answer, not the approval as a yes/no.
- *Submit gate* — `fill --follow` returns at the gate and prints the approval's
  `context` and id. Show that context verbatim and ask. Then run `decide`.

Never pass a gate on your own reasoning, and never treat an earlier "yes, apply
to jobs" as consent for this specific submit.

**Reporting.** The user reads your message, not the terminal. Summarise verb
output rather than pasting it wholesale — but quote error text verbatim, since
the daemon's messages say precisely what is wrong and paraphrasing loses that.

**When the daemon is down** (exit code 2), say so and stop. Do not start it
unless asked; it owns a browser bridge and the user may have reasons for it
being off.

**The tentative table.** Present the kit as a markdown table with the
provenance column intact — `PROPOSED ⚠` rows must be visually distinct from
library-resolved rows. Write long proposals (essays) to scratchpad files and
record them with `set … --file`, so the human can ask for edits without
re-pasting. Iterate until they're satisfied, record adoptions with `accept`
only when they say so (AskUserQuestion works well for "accept these three, or
tell me what to change").

## Worked shape

```
pnpm run jobagent status                     # first, always
WebSearch "senior frontend engineer remote"  # your search
pnpm run jobagent assess <url>               # filter, writes nothing
pnpm run jobagent ingest <url> --source websearch
pnpm run jobagent questions <name>
pnpm run jobagent draft <name>
pnpm run jobagent set <name> "<label>" --file essay.md --proposed --basis "posting: …"
   → present the full table; AskUserQuestion: iterate or adopt?
pnpm run jobagent set <name> "<label>" "<their words>"     # owner's answer
pnpm run jobagent accept <name> "<label>"                  # owner adopts a proposal
   → AskUserQuestion: approve the kit?
pnpm run jobagent approve-kit <name> --promote
pnpm run jobagent fill <name> --follow
   → AskUserQuestion: the approval context, verbatim
pnpm run jobagent decide <approvalId> approve
pnpm run jobagent submit <name> --follow
```

Add `--json` to any verb when you need to read a field rather than show a human.
