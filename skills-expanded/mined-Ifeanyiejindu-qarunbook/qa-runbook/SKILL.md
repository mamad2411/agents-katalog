---
name: qa-runbook
description: Run a QA sweep for any app against the qa-runbook MCP — establish what is under test, create real test accounts, drive web and mobile, verify fixes, and record results with evidence. Use when asked to run QA, test a section, retest a check, clear a QA backlog, or verify a fix against a runbook.
---

# QA runbook

> **Policy — mandatory, not advice.** Every assistant using qarunbook (MCP, API, plugin, any tool)
> follows this skill's method in full. Do not shorten it, skip a step, ask the person to waive it, or
> hand back steps this skill already tells you how to do: work from the runbook and the code yourself.
> "Generate test cases" means the test-checklist skill. "Test the app" means this method, in order:
> tests up to date from the code (0 missing) → prerequisites proven (build, sign-in, test data) →
> sign-in, sign-up, onboarding first → the rest → fix every couldn't-check by cause in one batch →
> rerun only those → report numbers. qarunbook enforces the steps it can see: it refuses runs with
> missing tests and tests that break their framework's rules, and stops a run that cannot check.

Drive a QA runbook held in the `qa-runbook` MCP for whatever app is under test. This skill is
app-agnostic: it establishes what it needs, then applies the discipline below.

**If a skill already exists for this specific app, use that instead** — it will carry the real
URLs, credentials, device setup and known blockers. Check the available-skills list for something
matching the app name. This skill is for apps that don't have one yet, and it ends by offering to
write one.

## The method — follow it every time, without being told

The person using qarunbook should be able to say "test this app" and walk away. They should not
have to manage the order, chase "couldn't check" lists or tell you to go back to the code. This
method is how that happens. Every step is yours to do, not theirs to ask for.

**A runbook is kept up to date, so a run mostly tests.** qarunbook is where every fix is followed by
checking the code and bringing the checks and their tests up to date, so the next run gives real
results. A pile of "couldn't check" means the runbook was not kept up to date. That is the fault to fix,
not something to run again and again.

1. **Before every run, bring the area up to date from the code.** For the checks the run will
   cover (the whole app, a section, or the retests), find what changed in the code since their
   tests were written: fixes, renamed screens, new steps. Correct the checks that are out of date and
   rewrite their tests from the code (test-checklist skill), with `from_files`. `progress` and
   `list_checks` filter `no_test` name the checks with no usable test. **That number must be 0
   for the area before you start.** A run must never be the thing that discovers a missing test.
2. **Prerequisites first, once, before any check.** Before a run, prove each one yourself
   (`test_readiness`, `test_accounts`): the build on the device is the current code; every saved
   test account signs in (run the saved sign-in once and watch it reach the signed-in screen);
   the test data the checks need exists (a file to upload on the device, money in the wallet, a
   community to act on). A login is a prerequisite of every check behind it, a retest too.
   If one is missing, fix it now. Never start a run that will hit "could not sign in" on check
   after check. qarunbook also checks these itself: a run doesn't start when its AI account is out
   of credit; a web run signs in once as every saved account its checks use before any check, and
   stops there if one fails; a check that sets up an account most of the remaining checks need
   stops the run when it doesn't pass; and new tests are proven in a run of their own first.
3. **Clear the small foundation sections first.** Start with sign-in and sign-up (AUTH), then
   onboarding and anything every other section depends on: a handful of checks per platform.
   Finish them: passed, or failed on a real app bug. Only then run the big sections. A broken
   sign-in found at the start costs one fix. Found at check 200, it costs a whole run.
4. **Stop a run that is failing on a prerequisite.** If the first few results of a run are the
   same "couldn't check" (sign-in, no test, missing data), stop it (`stop_run`), fix that one
   cause for all the checks it touches, then start again. Don't let it work through hundreds of
   checks it can't reach.
5. **After the run: fix every "couldn't check" in one batch, then re-run only those.** Group them by
   cause (no test, out-of-date test, sign-in, data, device). Fix each cause once for all its checks,
   from the code. Then re-run just those refs. Report how many gave a real result on their own.
6. **After a fix lands, the same loop:** read the fix in the code, update the checks and tests it
   touches, then run the retests. A retest never goes out against a test written before the fix.
7. **Report numbers, not narration:** passed, failed (real app bugs, with their issues), and
   couldn't check grouped by cause. Couldn't check should be close to zero, and each one should
   say what is needed from a person (a real card, a second phone).
8. **Handing work to another assistant keeps the standard.** When you hand any of this work to
   another assistant or subagent, pass the test tool's rules in full (or have it load this skill)
   and require a rule-by-rule check before every save (test-checklist's "Pre-save check"). Never
   tell it to skip, ignore, shorten or read the rules only once. Saving usage means trimming logs,
   never dropping the standard. (The Confidant, Nov 2026: subagents told to "ignore" the rules after
   one read wrote Maestro tests that asserted below the fold, behind an open dialog and under the
   iOS keyboard, and the runs failed.)

## 1. Establish what you're testing

**Coming straight from the test-checklist skill?** The plan was just put into qarunbook
and you already know the app — skip choosing it and go to the rest of this section.

**No plan in qarunbook yet?** Nothing to run. Use the test-checklist skill first to write
the plan and put it in qarunbook, then come back here.

`list_apps` first — it names every app the runbook holds. If exactly one matches what the user
asked for, use it. If several could, or none obviously does, ask.

Then work out what you're missing. **Ask in one batch, not one at a time**, and only for what you
genuinely can't determine yourself:

- **Which app** in the runbook (skip if `list_apps` settles it)
- **The live URL(s)** — the web app, and the API base if the runbook has server-level checks
- **Codebase path(s)**, if any — without them you can still test behaviour, but you can't diagnose
  a cause or tell a stale build from a real defect. Ask which repos exist (backend / web / mobile
  are often separate) and whether pushing deploys anything.
- **How to get a test account** — existing credentials, or the signup flow. See §3.
- **Scope** — the whole runbook, one section, one platform, or re-verifying specific fixes.

Use `list_checks` and `progress` to see the shape before planning. A check's own wording is the
spec; read it before testing, not after.

## 2. The one rule

**Never mark a cell `P` you did not actually observe.** A stale "needs retest" you couldn't prove
stays that way. Quote the real request and response, or what was on screen. A note that says
"verified" and nothing else is worthless later — and a wrongly-passed cell is worse than an
untested one, because nobody looks again.

State in every note what your evidence does **not** cover. "The server refuses correctly; nobody
has seen a client render the refusal" is a complete, honest result.

Related traps:
- **A stale build is not a bug.** Before filing anything from a device or a deployed site, check
  what's actually running against the repo HEAD. Year-old binaries have produced whole batches of
  phantom failures.
- **Check the timestamps.** A cell marked failing before the fix shipped is a stale mark, not a
  defect. Compare the mark's date against the commit and deploy dates.
- **Don't let one platform's pass carry to another.** Verify each separately unless you can point
  at shared code *and* say so in the note.

## 3. Test accounts

There are two ways to be signed in, and one of them must be settled before anything behind a
login is tested: **an account the user gives you**, or **one you create yourself**. Never test
from a real customer's account, and never guess credentials.

**Check the app's saved test accounts first:** `test_accounts` (app) lists the logins the team keeps
for testing — an admin, a seeded customer — each with its username and a note on when to use it.
When a check needs that kind of account, the automated tests sign in with it by name (§4).
Passwords are never returned: on a device opened with `start_device` for a check done by hand, tap
the username field and `device_action` `type_account` (account, field `username`), then the
password field and `type_account` (field `password`) — qarunbook types the saved password for you.
An admin can save accounts with `set_test_account` (e.g. the ones a seed script creates); checks
about signing up still make a fresh account.

Ask for credentials in the §1 batch. If none are offered, create one — and say which address you
used, so the account can be found again later.

Creating one, the usual shape:

1. Get an address from the app's **test inbox**: `test_email_address` gives a fresh one
   (`test+…@in.qarunbook.com`) each time — one per account, since apps refuse an email they
   have seen.
2. Sign up with it — through the form, or `POST` the signup endpoint.
3. If the app emails a code or a link, read it with `read_test_email` (`to` = the address,
   `after` = when you signed up, `wait_seconds` ≈ 60). It returns the codes and links already
   picked out. No mailbox of the person's is touched, and nothing is written to the database.
4. Verify, then log in and keep the token.

Password resets and invitations work the same way: send them to a test address and read it
back. People on the app see the same inbox in qarunbook (the app's **Test inbox** button).

Check what signup fixes permanently — country, currency, plan, locale often can't be changed
later, so create the account you actually need.

**Do not write to a production database to activate an account.** The permission classifier
blocks it, and you should not route around it. If the email route genuinely doesn't exist, say so
and let the account owner decide.

Watch how the API returns its token: some already include the `Bearer ` prefix, and
double-prefixing produces 401s that look exactly like a correct refusal.

## 4. Running the tests

**The automated tests do the testing, not you.** Every check comes with automated tests written
from the app's code, in the test tools the app has switched on (`automated_tests` says which):
Playwright and/or Cypress for web, Maestro for phones. qarunbook runs them exactly as written,
with no AI driving:

1. `run_tests` (app, platform code; optionally `refs` or `section`) starts the run on the
   workspace's connected computer, or qarunbook's cloud for Playwright on web. Cypress runs on a
   connected computer (it sets Cypress up there the first time). qarunbook refuses a run with any check
   missing its test (it names them: write those from the code first); it runs sign-in, sign-up and
   onboarding first, and stops a run by itself when 3 checks in a row can't get to their start, 5 in a row can't be checked
   for any reason, or most of the checks done can't be checked. Fix the named cause; never work around it.
   A test the app outgrew is rewritten from the screen and run again. A platform
   with no test tool switched on can't be run: its checks are for people.
2. `run_results` (the run id) shows each check as it ends: passed, failed (an issue is raised),
   couldn't check (with why — usually a saved login or test data to fix), or still to come. Call it
   again until it says done, then report the numbers and the fails.

Results are recorded by the run itself: do not `set_result` them again.

**What each result means.** A result from a test stands on its own:
- **Passed / failed:** what the test saw. A fail is a fail even with no AI involved; an issue is
  raised for it.
- **Couldn't check, test needs regenerating:** the test is broken, not the app. Maestro could not
  read the flow, the flow looked for "undefined" (a value it never set), or it could not find
  something the screen no longer draws. The check stays untested; fix the test (below).
- **Couldn't check, could not get to its start:** the saved sign-in did not finish (a field or
  the signed-in screen never appeared). Fix the account or the saved sign-in, not the check's test.
- **Error:** the device or the test tool broke (Maestro crashed, the emulator stopped). Nothing
  was tested; run those checks again.
- **The same fail on many checks** at one step (a sheet that never opens, an expected word that
  never shows) is one cause: usually the test account's data (an identity check not done, no
  money, no positions) or a screen the tests do not expect. Find that one cause first.

While a run goes, the runbook shows it to anyone looking: "Testing now" on the check under way,
"Already tested · skipped" on checks the run passes over (they already have a result there), and
a bar with the run's progress.

**Only a check marked as not automatable is done by hand.** `check_scripts` says `left_to_people`
for those (how something looks, a camera, a real payment, a second person). For one of them,
`start_device` (app, platform code, `ref`) opens the app on a connected computer and returns a
screenshot; act with `device_action`: `tap` (x, y in the screenshot's pixels), `type` (into what
has focus — tap the field first), `type_account` (a saved test account's username or password,
typed for you — §3), `key` (Enter, Backspace, Tab), `scroll`, `swipe`, `back`, `open` (a link),
`wait`, `screenshot`. Read codes and links with `read_test_email`, record the check with
`set_result`, and `end_device` when done. A check that needs something nobody automated has (a
real card, a second phone) stays untested, saying why.

**A test that keeps failing for the wrong reason** (a renamed button the run could not fix, a
login that changed): read it with `check_scripts`, then the screen's code, and fix it the way the
test-checklist skill writes tests (the words and ids as the code draws them, scrolled to, matched
by pattern where they come from data, and to the tool's `rules` that `check_scripts` returns) — written again from the code, never patched from the old
test or the failure alone; save it with `set_check_scripts` (with `from_files`) and run it again with
`run_tests`. A run picks up a test fixed while it is going. When many tests fail the same way, fix
the cause in all of them, not one at a time. Fix the test, never mark the check by hand.

**Tips for the checks done by hand.**

**Web.** Login forms built on React controlled inputs ignore a plain `.value` set — use the
native setter and dispatch the events:
```js
const set=(el,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value')
  .set.call(el,v);el.dispatchEvent(new Event('input',{bubbles:true}));
  el.dispatchEvent(new Event('change',{bubbles:true}));};
```
Test phone width at a real narrow viewport, not by assuming the desktop result carries.

**Android.** `adb shell input text` mangles spaces — use `%s`; `#` needs `keyevent 18`. Screenshot
to confirm a field before submitting. `keyevent 4` (BACK) navigates away when no keyboard is up —
dismiss a keyboard with the IME chevron instead. Screenshot before navigating: a stale dialog will
swallow your taps.

**iOS.** Attach the simulator panel *before* building, so the user can watch and so device-access
prompts surface early.

**Rebuild mobile before testing it**, and point the build at the environment you mean to test.

## 5. Recording

- `set_result` takes `P` or `F`. To make a platform not applicable to a check, use `update_check`
  with `not_applicable_on` — never mark it `P` to get it out of the way.
- Where you need a durable note, `add_issue` with the evidence then `resolve_issue`.
- Resolving an issue moves its cells to "needs retest", not to passing — someone must then record
  a result.

**Scope an evidence note to the platform you are recording, and no wider.** `add_issue` takes the
pass away on every platform you list, and `resolve_issue` then leaves them all at "needs retest" —
including cells another tester had already passed. Three agents have now knocked down someone
else's `P` this way while finding nothing wrong with it. If your note is about WM, pass
`["WM"]`, not every platform the defect might theoretically touch. If you do displace a mark,
say so explicitly in your report rather than quietly re-marking a cell you did not observe.
- Found something genuinely broken? `add_issue` rather than quietly marking `F`.
- An issue that is vague or wrong — yours or a tester's — gets corrected with `edit_issue`, not a
  second issue. The original reporter stays on it and the old wording is kept in its history.
- `list_issues` names any files a tester attached (screenshots, recordings, logs). They are viewed
  in the web app; say in your report when one is worth a human looking at.

## 6. Fanning out

**Runs fan out by themselves.** Start `run_tests` once per platform (WL, WM, AND, IOS…): they run
side by side on the workspace's computers and qarunbook's cloud, each check its own test. No agents
are needed to test in parallel.

**One actor per device.** A simulator or emulator is a single, shared, stateful thing: while a run
or a `start_device` session is using it, nothing else touches it. Do the hand-done checks after the
run on that platform has finished.

**One phone test session per computer.** Every copy of Maestro on a computer talks to its device
over the same port, so a second Maestro — your own `maestro test`, a Maestro MCP, another
assistant's run, even on a different emulator — breaks the checks of a qarunbook run going there
(Oct 2026: two Sabi checks failed this way when another session started its own emulator and
Maestro). Before starting phone testing of your own on a computer, make sure no qarunbook phone run
is going on it (`run_results`, or the runbook's "Testing now"); wait for it, or use another
computer.

**Where phone tests run.** Lightest first, for computers that are not powerful or are busy:
- **Your own phone**, plugged in: almost nothing runs on the computer.
- **Limrun**: phones in the cloud, nothing installed.
- **Light Android**: Android 13 in a container, about 1 GB of memory instead of 3+, ready in
  seconds once set up (about 15 minutes the first time). Its results matched a full emulator's.
  It has no Google Play services: not for Google sign-in or push notifications. On a Mac it needs
  `brew install colima docker`; the helper does the rest.
- **A full emulator or simulator**: the heaviest; needed for Google sign-in, push, and iPhone
  simulators (Macs only).
The person chooses this in Run tests (or Test configuration) for each platform; suggest the
lightest one that can test what the app needs.

**"I could not log in" is not a result.** A run that says couldn't check because a saved login or
test data is wrong names it: fix the account (`set_test_account`) or the data, then run those
checks again with `run_tests` and `refs`.

**Read what a run refused to conclude.** A couldn't check names the real remaining work; report it
plainly rather than marking anything by hand.

## 7. Finding real causes

Two patterns account for a lot of hard bugs — check both before writing code:

- **The fix landed on a screen nobody opens.** Confirm which screen the user actually reaches.
- **The client speaks a vocabulary the API never sends.** Grep the server for the literal before
  trusting a client branch on it.

## 8. Safety

Read-only by default. Never complete a purchase, move money, submit a withdrawal, or delete data
you didn't create. Small test data is fine — **say what you left behind**, every time.

**Never put a destructive verb in a permission-probe battery.** The way you prove an
authorisation hole is to run the same request as the owner, as a stranger, and signed out. If
`DELETE` is in that list, the owner's pass *succeeds* — and on 19 Sep it did: an agent sweeping
X-20 deleted a live production event. `EventService.delete` is a HARD delete that cascades, so it
took the event, its 18 invitees, the staff access codes, seating, team grants, sessions,
registration forms and every submission. None of it is recoverable through the API, and the
observation it was meant to produce was worthless anyway — the stranger's 404 came back because
the row no longer existed, not because access was refused.

Build the probe so destructive verbs are only ever sent as the **unauthorised** identity. Read
first, and confirm the refusal is a refusal and not an absence.

**This applies to agents you dispatch.** "Do not commit and do not push" does not cover
`DELETE /event/:id`. Say the destructive rule out loud in every agent prompt.

## 9. Leave something behind

At the end of a sweep, offer to write an app-specific skill capturing what you learned: the URLs,
the account recipe, the gotchas that cost you a false finding, the blockers that need the owner.
That's what makes the next run cheap. Save it where your agent reads skills — `.agents/skills/<app>-qa/SKILL.md` in the repo, or `.claude/skills/`, `.cursor/skills/`, `.codex/skills/` — same shape as this
one, with the specifics filled in.
