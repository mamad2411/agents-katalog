---
name: breakthrough-performance-db-setup
description: >
  One-time install of your Meta ad performance database: copy the template
  Lark Base, wire the daily sync to your own Meta token, reconcile it against
  Ads Manager, and leave a pointer note in your vault. The weekly read of the
  installed Base is /breakthrough-performance-analysis.
disable-model-invocation: true
---

# Breakthrough Performance DB Setup

You are installing one system, for one student, once. The end state is narrow and checkable: their own ad spend is landing in their own copy of the Base every day, the numbers on it agree with Ads Manager, and their vault holds a note that tells next week's session where all of this lives.

**The one sentence that governs everything below: every step of this install can fail while looking like it succeeded, so the job is not to complete the steps, it is to produce evidence that each one actually happened.** A copied Base with a disabled workflow looks identical to a working one. A sync that pulled 25 of 500 rows looks like normal data. A margin field with the average order value typed into it produces a breakeven line that is wrong on every single verdict, in the same direction, forever, and never errors. That is what gates 4, 6, 8 and the runtime checks exist for.

## Where you are in the product

**This skill runs inside a vault built by `my-second-brain`, and does not ship with it.** It is installed and updated separately, and everything it writes into the vault obeys the vault it is standing in, not this file.

**The law for anything that lands in the vault is that student's own `99_Meta/structure-doctrine.md`, read live, at the moment you write.** ⛔ This package carries no copy of it. Section 8 declares the shape of the note you write, section 0 is the filing decision tree, section 5 is the law on names. ⛔ Never a remembered version of section 8, and ⛔ never a key list quoted from here: this student may have amended their own constitution.

⭐ **The asymmetry matters, so do not over-apply the rule above.** The vault has a live source of law and you read it. **Lark and Meta do not.** There is no file in the student's world that records how a copied Base behaves, what `+field-update` silently destroys, or which failure a Meta token typically has, so the `references/` files in this package carry that knowledge **in full**, and they are the source. Read the vault's law live; read this package's mechanics from this package.

⛔ **This skill promises nothing.** No "installs in one session", no estimate of how long it takes, no claim about what the student will have by the end. Some students are blocked at gate 1 by an agency that owns their ad account, and there is no version of this install that rescues them. State what the current gate needs and what its pass test is. ⛔ Never put a duration or an outcome in the student's mouth before it exists.

**Speak the student's own language.** This file is in English; the session is not. Match whatever they write to you, including code-switching, and keep the field names and the verdict words exactly as they appear on their board.

## Gate 0: the toolchain, and it is a gate

**Every gate from 2 onward reaches the student's Base through `lark-cli`, under the student's own identity.** Gate 2 copies the template and reads the roster off the copy, gate 4 writes Targets and reads the row back, gate 5 clears six tables and counts them, gate 7 edits the sync workflow, gate 8 re-sums the raw rows without going through the board's own totals. ⭐ **So this is not an accessory to gate 2. It is the floor the rest of the install stands on**, and a session that discovers it missing at gate 4 has already spent the student's evening on gates 1 through 3.

**Three checks, and they are checks rather than questions**, the same discipline as gate 1's vault probe: you are looking for something that either works or does not, ⛔ never for the student's opinion about whether it is installed.

1. `lark-cli --version` returns a version.
2. `lark-cli whoami` returns a **user** identity whose token is not `needs_refresh`. ⚠️ A user token expires quietly (`lark-lessons.md:76`), and an expired one surfaces much later as a parse error on an auth object, which reads like a broken script rather than a dead login.
3. `lark-cli base +base-get --base-token <the master token in references/template-and-teaching.md>` returns the template's info. ⭐ **This single call proves four things at once**: the CLI is installed, the login is alive, the scopes reach Base, and **this student can actually see the template**. It is the same shape as gate 6, where one Insights call proves the app, the Marketing API product, the System User and `ads_read` together.

**When a check fails, the fix is the student's to run, and the browser part of it is two round trips:**

- `npm install -g @larksuite/cli` if check 1 found nothing. ⚠️ On a machine whose npm prefix is not on the shell's `PATH`, this succeeds and the binary still appears missing; resolve it by full path before concluding the install failed.
- `lark-cli config init --new` creates and binds a Lark app through the browser. ⛔ They do not have to hand-build an app in the developer console, and ⛔ you do not send them there.
- `lark-cli auth login --domain base,drive` grants the scopes. `drive` is needed alongside `base`, because copying a Base creates a file in their Drive.
- ⭐ **Guide it; do not attempt to do it for them.** Both commands block on a browser step only they can complete. Run the first in the background, take the verification URL out of its output, and hand them the URL exactly as printed. ⛔ Never retype, re-encode or reassemble that URL.

⛔ **Never offer the owner's credentials as a shortcut, at this gate or any later one.** They authorise the owner's entire tenant, they cannot be moved between machines in any case because the user token lives in the OS keychain (`lark-lessons.md:70`), and a copy made under them would land in the owner's Drive rather than the student's.

⚠️ **One failure this gate cannot fix, and naming it beats looping on it: a tenant that will not let this student create an app.** A personal Lark tenant makes them their own admin and it is theirs to do; a company tenant may refuse. If `config init --new` cannot complete for that reason, say which piece is blocked and who inside their organisation unblocks it, and stop. ⛔ There is no workaround, and improvising one is worse than the honest stop.

**Pass test:** check 3 returned the template's info under the student's own identity. ⛔ Not "they said they installed it".

## Gate 1: Qualification, in full

This is the gate most likely to end in **"no, and there is no workaround"**, which is why it is near the front and why it is written out here rather than in a reference file. ⛔ It is not the only one: gate 0 can end with a tenant that refuses to let them create an app, gate 6 can end with Meta refusing access, and this package promises no gate a fix. Running gates 2 through 7 for someone who was going to fail gate 1 wastes their evening and yours.

**Three checks about access.** Ask directly, and take the answers as claims to be confirmed later, not as facts:

1. **They own their own Meta Business Manager.** ⛔ An agency-owned account is the disqualifier. The student cannot create the System User the sync needs, and no amount of "I'll ask my agency" resolves it inside this session.
2. **They are an admin on the ad account**, not an advertiser or an analyst.
3. **They have a Lark account** that can hold a Base. ⭐ Gate 0 already proved this one physically, so treat it as settled rather than asking again.

⭐ **Checks 1 and 2 are load-bearing but self-reported, and that is acceptable here**, because a student who is wrong about them fails physically at gate 6, where creating a System User and calling Insights either works or does not. Gate 1 is there to save the ones who already know the answer is no.

**A fourth check that is a check, not a question: probe the vault.** Look for `99_Meta/structure-doctrine.md`.

- ⭐ **You are looking for a file.** If you do not know where their vault is, you may ask that one question ("where is your vault?") and then probe. ⛔ You may not ask "do you have a second-brain vault?", because that question returns an opinion and what you need is a file that either exists or does not.
- ⛔ **If the file is absent, stop the install.** Say plainly that this system leaves a note behind so next week's analysis can find the database without asking again, that the note has to be filed under a law this vault does not have yet, and that installing the vault is a separate job (`my-second-brain`) which is theirs to run. Say what is missing, say who fixes it, and stop.
- ⛔ **Do not degrade to writing a plain note instead.** A note in a shape the vault does not recognise is worse than no note: the vault's own maintenance pass will not see it, the frontmatter guard will refuse or flag it, and the student now believes they have a pointer they do not have.

**A fifth thing, which is a question, and it is the one people skip: "how are your leads attributed back to a specific ad?"** Not "do you track leads", but *how does a lead that arrives today get connected to the ad that produced it*. Make them describe the actual mechanism: a per-ad WhatsApp click-to-chat link, a form field, a landing page parameter, a dedicated phone number.

⛔ **State the scope-out here, at gate 1, before anything is copied.** In substance, out loud:

> This whole system runs on one text key: `<ad-id>__<YYYY-MM-DD>`. Every rolling window, every cost-per-qualified figure, every verdict is a lookup on that key. **A walk-in customer cannot carry an ad-id. A phone call to a shared number cannot carry an ad-id.** If that is how most of your leads arrive, the ad half of this board will be right and the lead half will be empty, and no migration, no formula and no later fix can invent a key that was never captured at the moment the lead arrived.

⭐ **Say this at gate 1 or the student concludes the material is broken.** They will not conclude "my attribution does not fit"; they will conclude the system does not work, three weeks after they built it, with their own data in it.

**When the funnel does not fit, say so plainly.** ⛔ Never pretend it fits, and ⛔ never quietly widen the definition of a "conversation" to make their numbers appear. The session **may** walk them through the existing design so they can build their own variant of the lead half. That is a legitimate thing to do and often the right one. ⭐ **If it does, it MUST record what was actually built in the student's vault note**, because next week's analysis will read that note and assume the standard shape unless the note says otherwise. The procedure is in [references/vault-note.md](references/vault-note.md).

## Gates 2 to 10, in governing form

**2. Copy the template, and you run the copy.** ⭐ **`lark-cli base +base-copy` does in one call what the student would otherwise do by hand**, under their identity from gate 0, and the copy lands in their Drive owned by them. ⛔ **This is not the thing the "template, not a provisioner" rule forbids.** That rule is about building the Base field by field: several hundred calls, every one a failure point. A copy is one call. ⛔ **It runs under the student's own credentials and never the owner's**, because the new Base belongs to whoever's token made it and the API has no parameter that says otherwise. Then **resolve every table by name, and read the roster off their copy at runtime**, because `table_id` regenerates on copy (`lark-lessons.md:706`), so an id written down anywhere is a bug waiting for its second student. ⛔ **Pass the copy an explicit time zone.** The call does not inherit one, and a copy made without it carries a timer whose time of day is not the time of day you can see on the template, so every student's 07:00 is quietly some other hour. The flag and its exact form are with the command in [references/template-and-teaching.md](references/template-and-teaching.md). ⛔ **Pass test item 1: the token of their copy is not the master token** ([references/changing-the-base.md](references/changing-the-base.md) §0). ⭐ Running the copy yourself makes that check stronger rather than redundant: the token now arrives as an API return value instead of off a student's clipboard. The master passes every other check on the list, because it is the healthy original; only the token tells the two apart. Then: all eight tables resolve by name, and the sync workflow came across **disabled** (a copy carries the workflow and keeps it disabled, `lark-lessons.md:702`). ⛔ **The manual path is not deleted.** If the call fails after gate 0 passed, hand them the link, let them click, and rejoin at the same pass test. The command, its conditions and the one new failure it introduces are in [references/template-and-teaching.md](references/template-and-teaching.md).

**3. Teach the demo board.** ⛔ **Teaching, not an exam.** Never ask "do you understand what this means" and then gate the install on the answer. ⭐ **Show them one pair and stop**: the cheapest ad per conversation on the board is a KILL, the most expensive is a SCALE. That single comparison is the reason this whole system exists. ⛔ Do not tour the other verdicts; they arrive on their own every week, attached to the student's own ads. There is no pass test here on purpose: they re-hear the whole thing next week with their own money on the board, which is when it actually lands.

**4. Fill in Targets.** ⭐ **They say the numbers, you write them in** ([references/changing-the-base.md](references/changing-the-base.md) applies: token check, then read the row back). ⛔ Do not send them in to type it themselves: the error this gate exists to stop is the order value landing in the margin field, and with you holding the keyboard it cannot happen at all. Compute the breakeven from their answers and get their agreement **before** you write. Ask which currency the figures are in and record it; gate 6 has no other source for that. ⭐ **This is where a single wrong number poisons every future verdict in the same direction**, because the pass line for ROAS is their breakeven point and breakeven is derived from margin. Two hard checks, both in the reference: **gross margin greater than or equal to average order value is dead on arrival**, and **breakeven ROAS landing near 1.0 is the signature of typing the order value into the margin field.** Pass test: they have seen the breakeven number their own inputs produced, and they agree with it.

**5. Clear the demo data.** Six tables to zero; Targets and Account keep their one row each. ⛔ Forgetting this mixes demo rows into real ones and every figure on the board is quietly wrong. This is a change to their Base, so it runs under [references/changing-the-base.md](references/changing-the-base.md), and it is verified by re-listing and counting the rows yourself. ⭐ **The ad layer you empty here is refilled by the first sync rather than by hand**, and the pass test for that lands at gate 7; both are in [references/template-and-teaching.md](references/template-and-teaching.md).

**6. Get the Meta token.** ⛔ **Do not hardcode click paths.** Meta's UI is renamed and rearranged constantly, and a skill full of stale menu names teaches the student that the material is out of date. Find the current flow at runtime and guide them through it. ⭐ **Verify the end state, not the steps**: one successful Insights call proves the app, the Marketing API product, the System User, the assignment and `ads_read` all at once, and it survives every redesign. ⚠️ **But a successful call does not prove provenance.** A short-lived user token also passes, and that is the single most common failure of this gate, discovered weeks later when the sync stops. So check expiry and provenance too, and on failure name **which** of the four pieces is missing rather than saying it did not work. The procedure, and the three runtime checks that hang off this first live call, are in [references/meta-token-and-sync.md](references/meta-token-and-sync.md).

**7. Wire the sync.** Every placeholder replaced, workflow enabled, run once by hand, and rows actually present afterwards. ⛔ **Do not carry a placeholder count into this gate**: read the workflow for how many HTTP steps it has and read each step for its own, because a step you never wired fails silently and only that step's table stops moving. **Three things make the pass test, and rows are only the first.** Rows in Ad Daily, not a green run. The ad layer refilled, at the row count gate 5's clearing implies. And `Account.sync-last-run` read back and holding this run: the gate stamps last, so a stamping failure leaves a run that looks perfectly healthy and produces its duplicate on the next trigger instead. ⛔ Never read "the workflow ran" as "the data arrived", and never read "the data arrived" as "the gate held".

**8. Reconciliation, and it is a gate, not a request.** ⛔ **"Does it match?" answered with "yes" is not evidence.** You did not observe that comparison happen, and every failure this system can have (a key with a stray space, a formula bound to the wrong object, a rollup silently returning zero) returns a plausible number rather than an error. ⭐ **Make the evidence flow toward you**: you name the date range, the student reports the Ads Manager figure, the token independently pulls Insights for the same range, and **you re-sum the raw Ad Daily rows yourself, not through the Base's own rollups, because the rollups are one of the things under test.** Three-way diff. Details in [references/reconciliation-and-handover.md](references/reconciliation-and-handover.md).

**9. Write the vault note.** One `it-system` note in the business wing's `01_Assets/IT-Systems/`, carrying the pointer to the Base and everything next week's session would otherwise have to ask for. One business wing resolves silently; two or more, ask once which business owns this ad account. ⛔ **The Meta token never enters it.** The full contract, including the frontmatter, the read-before-write rule and the filing-log line, is in [references/vault-note.md](references/vault-note.md).

**10. Handover.** Keep it short, and make the content an **order of reading**, not a feature tour: is the sync fresh, then can the team absorb more leads, and only then the verdict. ⛔ A student who reads SCALE first and acts on it will pour money into a funnel nobody is answering. Two caveats belong here and nowhere else: the Meta token sits in the workflow where **anyone with edit rights on that Base can read it**, and the timezone and currency facts from gate 6's runtime checks. In [references/reconciliation-and-handover.md](references/reconciliation-and-handover.md).

### Loading the rest of this skill

| When | Read |
|---|---|
| Gates 2 to 5, the Lark side | [references/template-and-teaching.md](references/template-and-teaching.md) |
| Gates 6 and 7, the Meta side | [references/meta-token-and-sync.md](references/meta-token-and-sync.md) |
| Gates 8 and 10 | [references/reconciliation-and-handover.md](references/reconciliation-and-handover.md) |
| Gate 9, anything landing in the vault | [references/vault-note.md](references/vault-note.md) |
| **Any change to the student's Base, at any gate** | [references/changing-the-base.md](references/changing-the-base.md) |

⛔ **Load on demand, at the gate that needs it.** A session that reads all five before it starts has spent its context on the whole install to run the first gate of it.

## Iron lines

- ⛔ **The Meta token never enters the vault**, in any note, in any example, in any quoted error message. It lives in the workflow placeholder and nowhere else this skill touches.
- ⛔ **Every change to the student's Base obeys [references/changing-the-base.md](references/changing-the-base.md), including its §1a.** That file separates three kinds of change, and only one of them carries the four conditions: filling gate 7's placeholders is install-time configuration, a **migration** to an already-working Base needs all four (declared in this package, versioned with it, recorded in the vault note, detectable as already-applied), and a student-owned variant satisfies none of the first two and instead owes a written record plus permanent unknown-shape treatment. ⛔ Do not apply the four conditions to all three: that forbids installing and forbids the variant this skill is explicitly allowed to help build. The test is whether the *next* session, holding only this skill and that note, can state what shape this Base is in. If it cannot, what you did was improvisation, and improvisation is what makes a student's copy undiagnosable.
- ⛔ **Read before you write, on any vault path that might already exist.** The frontmatter guard watches births only: `fm-guard-hook.sh:346` allows an existing path straight through, with the comment *"an edit, not a birth; this guard watches births"*, and `fm-guard-hook.sh:369` shows Edit is not even a matcher. So a second install run that blind-writes the note replaces the whole file, silently, with nothing to stop it.
- ⛔ **Vault notes go through the Write tool, never through Bash.** The guard can read a Write and check the frontmatter inside it; it cannot read the contents of a heredoc, and its regex blocks `>>` as well. A note written through the shell skips the only check that would have caught its shape.
- ⛔ **Exit code is never evidence, and `ok: true` is never evidence.** Read back what you wrote, count what you cleared, and compare it to what you intended.

## Judgment you need while installing

Three facts about this template that will otherwise cost you an afternoon each:

- **`NOW()` freezes inside a formula; `TODAY()` does not** (`lark-lessons.md:180-181`, measured against this exact template). ⭐ That is why every rolling window on this board is a live formula and the sync computes nothing at all: it writes raw rows, and the board does the arithmetic. ⛔ So never "fix" a stale window by writing a number into it. The window is not stale, and a literal there is a lie that never expires.
- **A link field named the same as the table it points at silently resolves to the whole table** (`lark-lessons.md:95`). It returns every row's value joined into one string, does not error, and **every row shows the identical value**, which reads like a data problem rather than a schema one. If you ever create or rename a field here, ⛔ never give it a table's name.
- **Cross-table rollups fail silently and downward.** Rows written by the sync do not attach themselves to link fields, so a rollup written across a link quietly omits them (`lark-lessons.md:680`); a formula column used as a FILTER result column comes back empty rather than erroring (`lark-lessons.md:222`). Both return a plausible smaller number. ⭐ **That is precisely why gate 8 re-sums the raw Ad Daily rows itself instead of trusting the board's own totals**: the totals are the thing being tested.

## Settled, and not to be reopened

Recorded so no session spends a student's time relitigating a decision already made:

- ⛔ **The template ships as it is.** No redesign, no wide schema, no second template, no A/C split, no e-commerce variant, no mode flags. All of these were considered and reversed. A proposal to add one is a product decision, not a session decision.
- ⚠️ **Version stamps were on that list and are no longer.** The product owner reversed that one on 2026-08-24, which is the route this line names, and the template now carries `Account.template-version`. ⛔ **Read the three clauses in [references/changing-the-base.md](references/changing-the-base.md) §1 before you use it**: they keep it out of the shape decision entirely. ⛔ The reversal is not a precedent for anything else on the list above.
- ⛔ **This skill never amends anyone's vault doctrine** and never proposes adding a `type:` to it to make room for its note. That is the vault owner's business, taken with their own vault tooling.
- ⛔ **This skill never edits the template Base itself**, only the student's copy of it. Reading it is fine, and gate 0's third check does exactly that; ⛔ writing to it is the one thing changing-the-base.md §0 exists to stop.
- ⛔ **The copy runs under the student's credentials or it does not run.** Settled: the session performs the copy rather than asking the student to click it, and it never does so with the owner's identity. A proposal to ship the owner's credentials, in any wrapper, is not a session decision and not a product one either.
- ⭐ **The install is the deliverable, and the vault note is what makes it survive.** A perfectly wired Base with no note is a system the student will be unable to explain, and that next week's session will have to rediscover by interrogation.
