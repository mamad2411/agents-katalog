---
name: cg-intent
description: Interview the user in plain Hebrew and English about who may see and change each kind of record in their app, then write the claudeguard.intent.yml that the business-logic checks run against. Use when the user types /cg-intent, when a scan reports businessLogic.status as assumed, or when they ask why the business-logic section says it guessed.
argument-hint: "[path]"
allowed-tools: [Read, Glob, Grep, Bash, Write, AskUserQuestion]
user-invocable: true
---

# /cg-intent — ask the app's owner what the app is supposed to permit

Every other check in ClaudeGuardIL asks a question the code answers by itself: is RLS on, is the key
behind a public prefix. This one asks a question the code **cannot** answer — *what is this app
supposed to permit?* "User A can read user B's order" is a critical bug in a store and a deliberate
feature in an admin console: byte-identical code, opposite verdicts.

So the tool proposes, and the **user confirms**. That confirmation is the entire difference between
guessing and reviewing, and it is the only thing this skill produces. See
`${CLAUDE_PLUGIN_ROOT}/skills/claudeguard/references/methodology/business-logic.md`.

Argument: `$ARGUMENTS` — the repo path to interview about (default: the current repo root).

## The two hard constraints

**You may write EXACTLY ONE path: `claudeguard.intent.yml` at the scanned repo's root.** No other
file, ever — not a scratch model dump inside their tree, not a backup copy, not a README note. Put
any working files in a scratch directory outside the repo and delete them. A skill that interviews
someone about their security model and then leaves extra files in their working tree has spent trust
it cannot earn back.

**The ceiling: every business-logic finding is capped at confidence `likely` and can never be
`confirmed`.** A multiple-choice answer is not a proof — the user may have misread the question, and
the code check against their answer may still be wrong. `grader.mjs` asserts the cap at module load.
Say this to the user in step 5, in one sentence, so a confirmed intent is not mistaken for a proof
of correctness. What confirming buys is that the checks run against *their* rules instead of the
tool's guess — that is real, and it is bounded.

---

## Step 0 — preflight, and two places you must STOP

Run the engine and read the table facts:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/project_model.mjs <path> > <scratch>/cg-model.json
```

Read `database.tables[]` from it: each entry has `name`, `columns[].name`, and `columnsKnownFrom`.

**STOP #1 — no columns.** If **every** table has `columnsKnownFrom !== 'migrations'`, the engine
could not read a single column, so every option you would offer would be one you invented. There is
nothing to interview about. Say so, offer the two ways out, and end:

- **Put the schema in the repo.** `supabase db dump --schema public > supabase/migrations/000_schema.sql`,
  or paste the `create table` statements into a `.sql` file under `supabase/migrations/`. Then run
  `/cg-intent` again. This is the one that unblocks this skill.
- **Answer the RLS half now.** `/cg-scan` prints a `verifyQuery` — run it against their own database
  and it settles, in about ten seconds, whether row-level security is on for each table. That does
  not give this skill its columns, but it is the more urgent question and it is available today.

**STOP #2 — no tables.** If `database.tables[]` is empty, there are no records to state rules about.
Stop and say so plainly. This is safe to do: with no `claudeguard.intent.yml` the business-logic
tier is **silent** — an absent optional config produces coverage rows, never a finding — so ending
here leaves the report exactly as honest as it was.

Neither stop is a failure. Both are the tool refusing to manufacture an answer, which is the same
rule the rest of it lives under.

## Step 1 — get the draft from the engine, never from your head

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs <path> --propose-intent
```

This prints the proposed `claudeguard.intent.yml` — the resources, and the column each one is
probably keyed on. **Do not compose this YAML by hand.** The renderer and the reader are one
matched pair (`business_logic.mjs`); a file you write freehand can parse and still mean something
different from what you meant, and a check that is silently off is exactly the confident silence
this whole tool exists to prevent.

Your job in step 2 is to collect answers, then reproduce this file's shape with those answers filled
in — same keys, same nesting, nothing invented.

## Step 2 — the interview

Use `AskUserQuestion`. Multiple choice, never free prose. **Every option must be built from the
user's OWN identifiers** read out of the model: their table names, their column names, their route
paths. An option that says "the ownership column" teaches nothing; an option that says
`user_id` — the column that is actually in their `orders` table — is a question they can answer.

### Rules for every question

- **Hebrew first, then English, in the same option label.** The audience reads Hebrew; identifiers
  stay in English because that is what is in their editor.
- **These words never appear in anything the user reads:** *intent*, *ownership column*, *tenant*,
  *state machine*. Also avoid *IDOR*, *authorization*, *multi-tenant*, *transition*. Say
  "who may see it", "which company it belongs to", "who may move it to `paid`".
- **`AskUserQuestion` shows at most four options per question**, and the user can always type
  something else. Spend those four carefully — and one of them is always the skip.
- **Never ask about a table the model did not enumerate**, and never offer a column that is not in
  that table's `columns[]`.

### Budget — a hard cap

**At most 6 resources and at most 6 screens.** If the model has more than six tables, take the six
that the most routes touch (`routes[].tablesTouched`) — those are the ones reachable from the web,
which is where the question matters. Say which ones you dropped and that they can be added by
re-running. An interview that runs to fourteen screens is one nobody finishes, and a
half-finished intent file is worse than none.

Screens: ownership (1–2, four resources per screen), the state question (1), the fields question
(1), system routes (1, only when triggered), admins (1).

### 2a — Who may see a row? (once per resource, up to 6)

The core question. For a table `orders`:

> **HE:** מי יכול לראות שורה בטבלה `orders`?
> **EN:** Who is allowed to see a row in `orders`?

Build the four options from what the table actually has. Let *person-column* be the first of
`user_id, owner_id, author_id, created_by, uid, profile_id, customer_id` present in
`columns[]`, and *group-column* the first of `org_id, organization_id, team_id, workspace_id,
tenant_id, account_id, company_id, group_id`:

| The table has | The four options |
|---|---|
| both | `רק מי שיצר אותה (user_id)` · `כל מי שבאותה חברה (org_id)` · `כל מי שמחובר` · `לא יודע/ת — דלגו על הטבלה הזו` |
| only a person-column | `רק מי שיצר אותה (user_id)` · `כל מי שמחובר` · `כל אחד, גם בלי חשבון` · `לא יודע/ת — דלגו` |
| only a group-column | `כל מי שבאותה חברה (org_id)` · `כל מי שמחובר` · `כל אחד, גם בלי חשבון` · `לא יודע/ת — דלגו` |
| neither | `כל מי שמחובר` · `כל אחד, גם בלי חשבון` · `רק מי שיצר אותה — ואני אגיד באיזו עמודה` · `לא יודע/ת — דלגו` |

Each label carries its English half and the real column name, e.g.
`רק מי שיצר אותה — only whoever created it (user_id)`.

How each answer is written down:

| Answer | Written as |
|---|---|
| only whoever created it | `owned_by: <person-column>`, `tenant: null` |
| everyone in the same company | `owned_by: null`, `tenant: <group-column>` |
| anyone signed in | `owned_by: null`, `tenant: null` — the resource is still listed |
| anyone at all | `owned_by: null`, `tenant: null` — the resource is still listed |
| **I don't know — skip** | **the resource is omitted from `resources:` entirely** |

**"I don't know — skip this table" is a first-class answer and you must treat it as one.** Omitting
the resource produces an honest `bl:no-intent:<table>` coverage row that says none of the ten
business-logic classes could be checked against it. Pressing for a guess produces a rule the user
never actually meant, and then a page of findings — or a clean section — derived from it. A guess
recorded as a confirmation is the single worst outcome this skill can produce. Never re-ask a skip,
never soften it into a default, never fill it in "for now".

Note that *anyone signed in* and *anyone at all* are written down identically: the file has no key
for "this data is public", so both simply state that no per-row rule applies. Say that out loud in
step 3 rather than implying the file captured a distinction it did not.

### 2b — Who may move a record to each state? (one screen, only when there is a state column)

Only ask when a resource has a state-shaped column (`status`, `state`, `stage`, `phase`) in
`columns[]` **and** some route actually writes a literal value into it. Read
`routes[].literalAssignments[]` — entries are `{ key, value }` with `key` already lowercased — and
keep the ones whose `key` equals the state column. Those values are the states the code really
writes; do not invent others, and do not ask about states nobody's code produces.

One question per value, up to four, on one screen:

> **HE:** מי אמור להיות מסוגל לסמן הזמנה בתור `paid`?
> **EN:** Who should be able to mark an order as `paid`?

Options: `רק המשתמש שההזמנה שלו — the user themselves` · `רק מנהל — an admin only` ·
`רק המערכת (למשל שרת התשלומים) — the system only, e.g. the payment service` ·
`לא יודע/ת — דלגו על השאלה`.

Write the answers as `state_column`, `states` (exactly the values you asked about — a transition
whose target is not in `states` is rejected by the validator) and `transitions` keyed `any-><value>`:
the user themselves → `[user]`, an admin only → `[admin]`, the system only → `[system]`. A skipped
value contributes no transition at all, so the check declares itself unanswerable for that value
rather than passing it.

### 2c — Which fields may a user set? (one screen, multi-select)

Collect the real body fields the routes write: for the routes that touch the chosen resources, take
`routes[].bodyFields[]` and keep the ones that are also a column of that resource. Ask **once**,
as a multi-select:

> **HE:** אילו מהשדות האלה משתמש רגיל אמור להיות מסוגל לקבוע בעצמו?
> **EN:** Which of these fields is a normal user supposed to be able to set themselves?

The options are those field names verbatim (`item`, `quantity`, `price`, `total`, `status`,
`role`…). The selected ones become `mutable_fields` on the resource they belong to. Anything the
user does **not** select stays out — and that is the point: a `price` the client sends and the
server stores is the money bug, and it is invisible until somebody says out loud that `price` was
never meant to be user-settable.

Absence and emptiness are different answers here, and the audit reads them differently:

- **Nothing was offered for a resource** (no route writes any of its columns) → **leave the key
  out**. That is "not stated", and it grades undeterminable.
- **Fields were offered and the user selected none of them** → **`mutable_fields: []`**. That is the
  claim "a user may set nothing on this record", and it makes every body field a reported one.

Writing `[]` where the truth is "not stated" invents a rule; leaving the key out where the user
really did say "none" throws away the answer they gave.

### 2d — Which routes does the system drive? (one screen, only when triggered)

Ask this **only** if some `routes[].file` or `routes[].urlPath` matches
`webhook|cron|job|stripe|paypal|paddle|lemonsqueezy` (case-insensitive). Otherwise skip the screen
entirely — a question with nothing real behind it burns a screen and teaches the user to click
through.

> **HE:** אילו מהכתובות האלה מופעלות על ידי שירות חיצוני ולא על ידי אדם שלוחץ באתר?
> **EN:** Which of these addresses are called by another service rather than by a person clicking in your app?

Multi-select over the matching route paths, verbatim. The selected ones become `system_routes` as
glob patterns over the route file path. This matters in exactly one direction: without it, a payment
webhook that legitimately writes `status = 'paid'` is reported as a user-driven write, which is a
false finding on correct code.

### 2e — Does the app have admins? (one screen, last)

> **HE:** יש באפליקציה שלכם משתמשים עם הרשאות מיוחדות (מנהלים)?
> **EN:** Does your app have users with special powers (admins)?

Options and what each one writes:

| Option | `roles` |
|---|---|
| `כן, יש מנהלים — yes, some users are admins` | `[anonymous, user, admin]` |
| `לא, כולם שווים — no, every account is the same` | `[anonymous, user]` |
| `יש גם חלקים פתוחים בלי התחברות, ואין מנהלים — parts are public and there are no admins` | `[anonymous, user]` |
| `לא בטוח/ה — not sure` | `[anonymous, user, admin]`, and say in step 3 that you assumed admins exist |

`default_role: user` in every case — it is the role the audit checks a route against, and every app
that has accounts has that role. Ask this **last**, because it is the one question the user can
answer without looking at anything, and ending on an easy one is how an interview gets finished.

## Step 3 — read it back in a sentence they can check

Before writing anything, state what you are about to record **in plain Hebrew and English, with no
YAML on screen**. The user must be able to catch a wrong answer without reading a config file:

> **HE:** רק מי שביצע הזמנה יכול לראות אותה. רק שירות התשלומים יכול לסמן אותה כמשולמת. משתמש יכול
> לקבוע `item` ו-`quantity`, אבל לא `price`. הטבלה `audit_log` דולגה — לא נבדק לגביה כלום.
> **EN:** Only the person who placed an order can see it. Only the payment system can mark it paid.
> A user may set `item` and `quantity`, but not `price`. The `audit_log` table was skipped — nothing
> was checked about it.

One line per resource, and **name every skip**, because a skipped table is the one thing a user will
otherwise assume was covered.

**If `claudeguard.intent.yml` already exists, never overwrite it silently.** Read it, and confirm the
tool can still read it too:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs <path> --check-intent claudeguard.intent.yml
```

Then show the **difference in the same plain-sentence form** — "today the file says anyone signed in
can see an order; your answers say only the person who placed it" — and ask whether to replace it. A
`rules:` block or a comment they wrote by hand is theirs: carry it across rather than dropping it.
If they say no, stop, and leave the file exactly as it was.

Then write `claudeguard.intent.yml` at the repo root. That one path, and nothing else.

## Step 4 — validate the file you just wrote

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs <path> --check-intent claudeguard.intent.yml
```

Exit 0 and `ok: …` means the file is readable. A non-zero exit prints the exact problem — fix it and
re-check; do not hand the user a file the grader will refuse.

**Pass `<path>` (or `--model <file>`) even though this subcommand only reads the YAML.** The grader
resolves its model before it looks at the flag, so the bare `--check-intent <file>` form waits on
stdin and dies with a JSON parse error that says nothing about your intent file.

This step is not a formality. The reader rejects an **unknown key** on purpose: a typo'd `owner_by:`
would parse as valid YAML, be ignored, and silently disable the ownership check on that resource —
the report would then show a business-logic section that ran and concluded nothing was wrong,
because the rule it needed had quietly been turned off. This command is what catches that.

## Step 5 — re-run the scan and name the delta

Run `/cg-scan` again in the same session and report what actually changed:

- `businessLogic.status` moved from `assumed` to `confirmed`, and `businessLogic.intentPath` now
  names the file the conclusions rest on.
- `businessLogic.resources[].rulesChecked / rulesTotal` rose for the resources they answered about,
  and `assumed` is now `false` on each.
- Any `bl:no-intent:<table>` rows that remain — one per skipped table — with a plain line saying
  those were not checked.

Then the ceiling, in one sentence: *"Every business-logic finding is still marked `likely` and can
never be `confirmed` — you told the tool the rules, you did not prove the code follows them."*
Findings from this tier never turn the headline verdict red, by design.

If nothing moved, say so instead of implying it did. An interview that produced no change in
coverage is a fact about the interview, and the user is entitled to it.
