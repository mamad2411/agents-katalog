---
name: cellar
description: Work the one-line thoughts dumped in Cellar about the repo you are in — pick one up, do it, report back in the user's voice, or ask when the thought is too thin to act on. Use when the user says "what's in the cellar", "anything dumped for this repo", "work the cellar", "pick up a thought/glitch/idea", when they ask what is left to do on a project, or whenever the cellar_* MCP tools are available and the session is about clearing dumped work. Also use before finishing a session in a linked repo, to catch anything worth dropping back in.
---

# Cellar

Cellar is a mind dump. One-line thoughts about things the user is building, filed under
projects, each with a **kind** (idea, removal, glitch, question, research, copy, design) and
a **state** (open, doing, blocked, done, dropped).

The thought is one line and **the reasoning behind it was never written down.** That single
fact drives everything below.

## The loop

```
cellar_orient  →  claim  →  work  →  append lines  →  finish
                                  ↘  ask  →  blocked  →  next thought
                                              ↖  cellar_check_answers
```

1. **`cellar_orient`** with the absolute path you are working in. One call gives you the
   project, its repo, what is open, what another session already holds, what is blocked.
   Do this before anything else; never ask the user which project this is.
2. **`cellar_claim_entry`** before touching code for a thought. It is atomic — if you are
   told someone else has it, pick another. It returns the full brief: the thought, what the
   user added since, what has already been reported, the kind's job, and the voice rules.
3. **Work it**, in the repo the brief names.
4. **`cellar_append_line`** for each real finding, as you go.
5. **`cellar_finish_entry`** as `done` or `dropped`, with one line saying what happened.
6. **`cellar_check_answers`** before picking up the next thought. Nothing interrupts you when
   the user answers something you asked — this is the only thing that tells you.

Claim one entry at a time and finish it before claiming the next. A queue of half-claimed
thoughts is worse than an untouched one.

## The lookups, when you are not working anything

Three slash commands sit beside this skill for the times you only want to see what is there.
They are read-only and they do not claim:

| command        | for                                                           |
| -------------- | ------------------------------------------------------------- |
| `/cellar-list` | what is open here, or in a named project, `all` or `inbox`     |
| `/cellar-find` | search the thoughts and the lines under them, across projects  |
| `/cellar-view` | one entry in full, by id prefix                                |

They live in `mcp/skill/commands/` and install next to this file — `mcp/README.md` has the
copy. Picking something up is still `pick up cellar entry <id>`, which lands back here.

### The live view

A lookup publishes a page instead of dumping rows into the terminal — **one page, reused**.
Every lookup overwrites the same artifact, so there is always exactly one "Cellar Live" in the
user's gallery and it always shows the last thing they asked for. Never publish a second one.

1. **Get the data.** `/cellar-list` and `/cellar-find` pass `json: true` to
   `cellar_list_entries`, which returns `{ rows, more }` — use the rows as they come, do not
   re-parse the text listing. `/cellar-view` reads `cellar_get_entry` and fills `entry`.
2. **Fill the template.** Read `live-view.html` — beside this file once installed
   (`~/.claude/skills/cellar/live-view.html`), `mcp/skill/live-view.html` in the cellar repo.
   Replace only what sits between `<script type="application/json" id="cellar-data">` and its
   `</script>`, and write every `<` inside a JSON string as `<` so a thought can never
   close the tag. Write the result to your scratchpad (or a temp directory) as
   `cellar-live.html`.
3. **Publish in place.** Already published it this session → publish the same path again.
   Otherwise `Artifact` with `action: "list"`, find the one titled **Cellar Live**, `read` it,
   then publish your file with its `url`. Only when none exists, publish a new one with
   `icon: "list"`. The page carries its own `<title>`; do not rename it.
4. **Say one line in the terminal**: the heading, the counts and the link. Not the rows —
   the page is the list now.

No `Artifact` tool in this session (another client, a bare CLI) → print the rows the way the
server returns them, exactly as before. The page is the nicer reading, never the only one.

The data block:

```json
{
  "lookup": "list | find | view",
  "heading": "the project name, the search text, or the entry's short id",
  "sub": "one line of counts, e.g. 13 open · 2 doing · 1 blocked",
  "at": "ISO timestamp of the lookup",
  "sections": [{ "title": "blocked on you", "rows": ["…rows exactly as json: true returns them"] }],
  "entry": null
}
```

For `/cellar-view`, `sections` is `[]` and `entry` is the brief as data: `id`, `text`,
`kind`, `state`, `agent`, `dumped`, `project`, `repo`, `yours` and `agent_lines` (each a list
of `{ text, age }`, kept apart as the brief keeps them), and `questions` (each `{ question,
options, taken, answer, status }` with `status` one of `pending | answered | dismissed` and
`taken` the options the answer picked).

## Ask instead of guessing

**This is a correct outcome**, not a failure to finish.

- **idea** and **removal** — ask essentially always. An idea is a direction, not a spec, and
  a removal destroys work. Name what it would mean concretely and what you would do, then
  ask before building or deleting.
- **everything else** — ask when two readings of the line would lead to different work.

Ask **one concrete question, naming the options**. "which surface — the dump field, the
filter sheet, or both?" is answerable in four words. "could you clarify what you meant?" is
not, and it will sit there.

A question waiting on an answer is better than a confident wrong build. It is also better
than a `done` the user later discovers was not.

## Where to ask, which is a different question

How much work is on the table decides it, and this is the part a model gets wrong in the
direction of interrupting.

**One task in this session → ask in the chat.** The user is sitting there. Routing the
question through the cellar would stall the only thing they asked for behind a notification.

**Several tasks → `cellar_ask` on the entry, then move to the next one.** It blocks that one
thought and leaves the rest of the list workable. Then:

1. **Ask the moment you know**, never at the end. The question is worth nothing until it is
   in their inbox, and a session that dies before you write it takes the question with it.
2. **Work everything that does not depend on the answer.** By the time the list is empty the
   answer may already be there — `cellar_orient` lists what has been answered since, above
   the open thoughts.
3. **`cellar_check_answers` as each thought finishes, and again before you end the session.**
   It takes no arguments and returns the questions *you* asked that have since been answered
   or waved off, with what the user said. An answer that arrived is yours to pick back up:
   the entry is `open` again, so claim it and carry on from the decision. Every write tool
   prints the same thing as a tail on its own result, so an answer will find you — but the
   tool is the one to call deliberately before you stop.
4. **Still unanswered and out of work → ask that same question in the chat**, then
   `cellar_answer_question` with what they said. The entry keeps the pair, so the decision
   does not live only in a conversation that is gone.

Pass **`options`** whenever you are choosing between named alternatives. They render as
a/b/c/d taps in the app, and a question answerable in one tap gets answered.

## What each kind is asking for

| kind         | the job                                                                |
| ------------ | ---------------------------------------------------------------------- |
| **idea**     | work out what it would actually mean, then **ask before building**      |
| **removal**  | find everything it touches, say what goes with it, **ask before deleting** |
| **glitch**   | reproduce, fix, cover with a test, report the cause in one line         |
| **question** | answer from the repo — do not change code to answer a question          |
| **research** | find out, report back compactly, no code changes unless asked           |
| **copy**     | write the string, matching the voice already in that UI                 |
| **design**   | general design work — layout, hierarchy, how a screen should feel       |

`design` does not mean "check it against a design system". Only reach for one if the project
actually has one.

## Groups

A shelf can hold **groups** — an ecosystem of projects that are one thing from far away.
Each group has a **general project** named after it, and a thought about the whole group
lives there. `cellar_list_projects` prints it as `(group — …)` with the group's projects
indented under it. If the general project is linked to the parent folder (`C:\ping`), an
agent standing there lands on it and one standing in `C:\ping\radar` still lands on radar —
the longest checkout wins. A follow-up that is about the ecosystem rather than one app goes
to the general project with `cellar_create_entry`.

## Testing on their phone

`cellar_orient` prints a **phone** line, read off a switch in the app's settings — *let agents
test on my phone*. It is the user's standing answer, given once, so never ask it again:

- **yes** → you may install the app on their phone over adb, launch it and drive it to check
  your change, the way the repo's own instructions describe. No need to ask first.
- **no** → do not install on it or drive it. If only a device test would settle something,
  say so and ask in the chat.

## Write like they do

Your lines sit in a list directly beneath the user's own thoughts. An assistant voice there
makes the list unreadable, and the list is the whole app.

- lowercase, one line, no full stop
- say what changed or what you found — **not** that you did it
- no markdown, no code fences, no bullets
- name the file or the surface when that is the useful part

> `fixed the nav island jump — keyboardVerticalOffset was missing on the dump field`
>
> not: `I've successfully resolved the issue by adding the missing prop.`

Lines are collapsed to one line and capped server-side, so a paragraph arrives truncated.
Send the sentence worth reading in six months. One line per real finding.

## The rest

- **`cellar_create_entry`** — something you found that is worth keeping but is not this
  entry. It lands open for the user to triage; never claim it straight back. Not a progress
  log — that is `cellar_append_line` on the entry you hold.
- **`cellar_archive_entry`** — already true, fixed elsewhere, no longer applies. Reason
  required. **There is no delete**: nothing in this app is destroyed to get it out of the
  way.
- **`cellar_check_answers`** — no arguments, scoped to your own agent name. The other end of
  `cellar_ask`: an answer lands in the database and nothing wakes you up to say so.
- **`cellar_answer_question`** — you asked on the entry, ran out of other work, asked again
  in the chat. This writes what they said back onto the question and unblocks the entry if
  it was the last one outstanding. Only ever what the user actually said — an answer you
  reasoned out yourself is a guess with their name on it.
- **`cellar_unclaim_entry`** — you ran out of room or the user moved on. Put it back. Only
  for a claim: it refuses a thought that is not `doing`.
- **`cellar_reopen_entry`** — a done, dropped or archived thought that should be on the list
  again: the user asked, or the fix did not hold. Reason required. It lands open with nobody
  on it — claim it if it is yours to work. Never reopen something just to take it.
- **`cellar_link_repo`** — `cellar_orient` found no project for a repo that clearly has one.
  Linking it is the one change that stops the question recurring in every future session.
  Offer it; do not invent a new project on your own.
- **The structure tools** — `cellar_list_shelves`, and creating, renaming and moving a shelf
  or a project. For a repo the cellar has no project for at all, where linking has nothing to
  link to: offer to make one on a named shelf, do not make it unasked. Nothing here deletes,
  and there is no settings tool — how the user's own app opens is theirs.

## Never

- work a thought you have not claimed
- re-claim something `blocked` — it is waiting on the user, not on you. Answering it in the
  chat and recording that answer is what unblocks it; the entry goes back to `open` and you
  claim it again from there
- sit waiting on a question instead of moving to the next task
- end a session without calling `cellar_check_answers` — an answered thought nobody picked
  back up is the whole cost of asking
- hold a question in your head until the end of the session
- touch an `archived` entry; it was put away on purpose
- mark `done` what you did not finish
- ask the user for their password — if a tool says the server is not signed in, tell them
  to run `npm run login` in `cellar/mcp`. If they say the account has no password because
  it was made with Google, point them at Cellar's settings → *password for agent tools*
