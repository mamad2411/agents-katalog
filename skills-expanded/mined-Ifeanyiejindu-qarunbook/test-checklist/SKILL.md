---
name: test-checklist
description: Build a complete QA test plan for an app — every module, feature and user journey, across each platform it runs on. Use when asked for a test plan, QA checklist, test cases, regression suite, or "what should we test", or when preparing an app for QA, a release or a demo. Writes the plan, puts it into qarunbook (creating the app, or adding to it), then offers to start testing it straight away.
---

# Building a test checklist

> **Policy — mandatory, not advice.** Every assistant using qarunbook (MCP, API, plugin, any tool)
> follows these rules in full. Do not shorten it, skip a step, ask the person to waive it, or
> hand back steps this skill already tells you how to do: work from the runbook and the code yourself.
> "Generate test cases" means this skill: every check AND its automated test, from one code read. "Test the app" means this method, in order:
> tests up to date from the code (0 missing) → prerequisites proven (build, sign-in, test data) →
> sign-in, sign-up, onboarding first → the rest → fix every couldn't-check by cause in one batch →
> rerun only those → report numbers. qarunbook enforces the steps it can see: it refuses runs with
> missing tests and tests that break their framework's rules, and stops a run that cannot check.

The goal is a document a **non-technical tester** can work top to bottom, where
finishing it means the app has genuinely been exercised. A missing journey is a
missed bug.

## Derive it from the code, never from memory

**The code decides the checklist.** Never start from an existing checklist, a feature list or what
the app "should" do: read the code, write down what it does, and draw the checks from that. Do it
in this order — the **code map** — and keep the map as notes while you work:

1. **Routes first: the modules.** List every route (page or screen) and where it leads, and group
   them into the app's modules by what a person does there: authentication, onboarding, each
   product area, billing, settings, admin, public pages.
2. **Map one module end to end.** Walk its routes in the order a person goes through them and read
   each screen to the end. For every screen note:
   - **Inputs**: the name exactly as shown, whole — read the shared input/label component: a
     required `*` or "(optional)" is part of the name (`Full Name*`) — the placeholder, id or
     testID, type, validation and its messages, and **when** a message appears (typing, leaving
     the field, submitting). An error that appears under a field moves what is below it.
   - **Buttons and links**: the name as shown (an icon-only one: its aria-label, or note that it
     has none) and exactly when each is enabled or visible.
   - **Actions**: what each sends (endpoint, payload) and gets back, following the call **into the
     shared request helper**: many apps toast the server's message on every success or error, so
     a message the page also prints appears twice (the page's is a paragraph; the toast's is not).
   - **What is shown after** each outcome and **where it goes next**; what appears only under a
     run-time condition (an AI's reply, a role, a plan, a flag) and how a person makes it appear.
   - **The server**, when its code is there: exact messages, what it stores, and every email or text
     (subject; a code, a link, or both; how long they last). Without it, mark these "server: not in
     this code" and never guess.
   - **State**: what is stored, and what a signed-in or signed-out person sees on opening it.
   Every item names the file it comes from.
3. **Checks from the map**: the main path through each journey, each validation and error the code
   handles, each condition, each email — in the screen's own words, with the exact expected result
   the map shows.
4. **Tests from the map** (below): every name, message and wait in a test is an entry in the map.
5. **An existing checklist** is only compared after the map is made: keep a check that matches,
   correct one the code contradicts (`update_check`), flag one whose feature the code doesn't have,
   and add what the map has that it lacks (`add_check`).
6. **When the code changes**, map again only the modules whose files changed, then redraw their
   checks and tests.

Walk every codebase the product ships from — backend, web, each mobile app — and
build the module list from what is actually there:

- **Backend**: the modules directory is the authoritative feature list. Controllers
  give the real endpoints, and therefore the real capabilities.
- **Web**: the routes give the surfaces; look for separate mobile components, since
  a responsive app and a purpose-built mobile view are different code.
- **Mobile**: the modules/views directories.

A feature that exists on one platform and not another is exactly the kind of gap
the document must **expose**, not paper over. List those up front as known gaps so
testers do not report deliberate differences as defects.

If the product has an existing plan, read it first and extend rather than replace.

**The code isn't on this computer?** When the app's GitHub repositories are connected in qarunbook,
read them through it: `code_sources` names them (and which platforms each builds), `repo_files`
lists their source files, and `read_repo_file` reads one. Walk them exactly as you would a local
checkout — routes, screens, modules, controllers — and build the plan from what is there.

## Structure

**Part → Section → Journey**, with a result column per platform.

Group into parts by what a person is doing, not by how the code is organised:
account and access, the core object's lifecycle, the people involved, money,
engagement, collaboration, admin, then cross-cutting. A tester thinks in tasks.

Every journey needs:

| Field | Rule |
|---|---|
| **ID** | `PREFIX-NN`, prefix per section (`AUTH-01`, `BUY-02`). A stable handle people can quote in chat. |
| **Journey** | What is being checked, in the user's words. |
| **Preconditions** | Who is signed in, what state things must be in. |
| **Steps** | Numbered, followable by someone who has never seen the code. No file paths, endpoints or jargon. |
| **Expected result** | Concrete and checkable. Never "it works". |
| **Platform columns** | One per platform, `N/A` where the feature genuinely does not exist there. |

Mark **N/A** explicitly rather than leaving a blank — it tells the tester it was
considered, not forgotten.

## What makes these documents work

**Test both roles.** Almost every module has an owner/administrator side and a
recipient/guest side. The guest is usually anonymous, arriving from a link. That
is where most defects are found and where coverage is usually thinnest.

**Write the unhappy paths.** Required fields left empty, an expired or missing
code, insufficient balance, an empty list, a sold-out item, an already-claimed
item, a payment abandoned at the gateway, a duplicate submission, a stale link
opened twice.

**Encode the traps.** When a bug had a specific condition, put that condition in
the steps or it will not be caught again:

- a control that vanished on a short screen → name the screen size
- a flow that only fails on a first visit → say "in a fresh browser"
- a setting that only fails on the second pass → say "go back and return twice"

**Insist that a success message is not proof.** State it in the rules and repeat
it in the journeys that matter: if the journey says an email arrives, a balance
drops, or a value persists, the expected result must say to *check that it did*.
A success toast for something that never happened is among the most common and
most damaging faults, and the easiest for a tester to wave through.

**Say what to capture on a failure**: the page address or screen name, what they
tapped immediately before, the **exact error text**, the time, and the platform.
The time matters when session replay is available.

## Output

Write markdown to `docs/qa-test-plan.md` in the repo, so it reviews in a pull
request alongside the code it describes.

Open with:

1. **How to use this** — the platform codes, how to record a result, what counts
   as a fail, and what to capture when something fails.
2. **Coverage summary** — journey count per part, and the known platform gaps.

Then the parts. Use tables; keep the steps short enough to read on a phone.

## Format rules for the importer

qarunbook (https://qarunbook.com) reads this format directly: sections from the
headings, checks from the table rows, and platforms from the check table's header.
For that to work:

- Each section is a `##` heading, with its checks in one table beneath it.
- The first column of every check row is a reference like `AUTH-01`.
- Trailing columns are the platforms; their names become the platform codes.
- A cell reading `N/A` marks that platform as not applicable.

One thing to avoid: a legend table early in the document explaining the columns.
The importer skips tables whose rows are not checks, but a legend is still noise —
prefer a plain list.

## API checks (a backend)

When the app has a backend, give it an **API** platform (code `API`) and write its checks as
requests, so qarunbook runs them itself — no browser, in seconds, free. The other platforms are
N/A on these checks, and the API platform is N/A on screen checks.

Steps are request lines, each with what goes with it; the expected result is lines about the last
response:

```
Steps:
1. POST /auth/login
   Body {"email": "{{email}}", "password": "{{password}}"}
   Expect status 200
   Save data.token as token
2. GET /me
   Header Authorization: Bearer {{token}}
Expected:
Status 200
data.email equals {{email}}
Within 800 ms
```

- Paths go after the platform's base address; `{{name}}` comes from the platform's variables
  (test account, token), from `Save … as name` in an earlier step or check, or is built in:
  `{{email}}` (a fresh test inbox address), `{{random}}`, `{{timestamp}}`, `{{uuid}}`.
- `Save email code as otp` waits for the code mailed to `{{email}}`.
- Expectations it checks exactly: `Status 200` / `Status 4xx`, `Within 800 ms`,
  `a.b exists` / `is missing` / `equals x` / `contains x` / `is an array` / `has at least 1 item`,
  `header x contains y`, `body contains x`. Anything else, in plain words, is judged by AI.
- For every protected endpoint, add the matching refusal: the same request without the token,
  expecting `Status 401` (or `Status 4xx`) — and, where data is per user, someone else's id.
- An app with an OpenAPI/Swagger document can have these made for it: App configuration →
  Test configuration → the API platform → *Checks from your OpenAPI document*.

## Scale

Be exhaustive rather than tidy. A real product runs to a few hundred journeys; a
plan of thirty has not looked hard enough. If a feature's behaviour cannot be
determined from the code, list it anyway with a note saying what the tester should
establish — never omit it.

## Before handing it over

- Every expected result is something a person can actually verify.
- No step mentions a file, an endpoint, or a function.
- Both roles covered for every module that has two.
- Known platform gaps listed up front.
- Recently-fixed bugs have a journey that would catch them again.
- It is in qarunbook (below), not only in the repo.

State plainly that the plan describes what the app **does**, derived from the
code — not necessarily what was intended. Where those differ, the plan encodes
current behaviour, and the sections covering recently-changed areas are worth a
product owner's eye before testers work from them.

## Put it in qarunbook — always, without being asked

A plan that only exists as a markdown file is not finished. **Writing the file is not
the end of this skill: the plan goes into qarunbook in the same run**, so the team can
start working through it. Do not stop at the file and do not wait to be asked.

If the `qa-runbook` MCP tools are connected:

1. `list_apps`, to see whether this app is already in the runbook.
2. **Not there:** `import_plan` with the app's name and the whole markdown file as
   `markdown`. One call creates the app, its sections, its checks and its platforms.
3. **Already there:** do not create a second copy under another name, and never
   write its existing checks again. Call `code_sources` for that app first: it
   lists the app's platforms, the GitHub repositories connected to it (and which
   platforms each builds), and every check it already has. Read the code you were
   pointed to — those repositories, or the folders on this computer the person
   names — and decide which platforms it builds. Then:
   - For each of those platforms, one `apply_platform` call: the existing checks
     whose feature is in this code too go in `on`, the ones whose feature isn't go
     in `off` (marked N/A there). Pass `label` when the app doesn't have the
     platform yet; it is added. A web app read after the mobile one ends with the
     shared checks on web too and the mobile-only ones N/A on web.
   - Write only what this code has that the existing checks don't cover, as a plan
     in the format above, and `import_plan` it with `app` set (no `name`). A section
     with an existing section's exact name adds its checks there; a check only on
     the new platform is N/A on the others.
   Leave existing checks' wording and results alone. If the existing app turns out
   to be a different product that only shares the name, ask before touching it.
4. Read back what was created — sections, check count, platforms — and confirm it
   matches the file. If the import refused anything, fix the file and import again;
   do not report success on a partial import.

If the MCP tools are not connected, say so plainly, and tell the user the two ways
to get the plan in: in qarunbook choose **Add an app**, then **Use our template**,
and upload `docs/qa-test-plan.md` under "Upload it filled in"; or connect the MCP
server (https://qarunbook.com/guides/qa-mcp-server) and run this step again.

## Then write its automated tests

Each check should also come with automated tests, so it can be run again and again with no AI —
in the **test tools the app has switched on**: Playwright and/or Cypress for its web platforms,
Maestro for its phone apps. They are independent: a team that uses Cypress gets Cypress tests of
their own, not a copy of Playwright's. Call `automated_tests` (app) to see which are on, or to
switch one on when the person asks (Test configuration → Automated tests in the app). With none
on, the checklist is for people only: write no tests.

**The rule — never broken, whoever writes them (qarunbook's AI, the person's own key, you):** the
checklist says *what* a check tests; the code says *how*. Every test is written from the source
files of the screens its check goes through — never from the checklist's wording alone, never from
a list of words, never from another generated test (not even translating Playwright into Cypress).
- Human checks and their tests come from the **same reading of the code — the module's map**:
  write a module's checks, then its tests from the same map, before moving on.
- When the code shows a check is out of date (a renamed button, a step that no longer exists, a
  message worded differently), **correct the check** (`update_check`), then write the test for the
  corrected check. Never "correct" a check to hide a real bug.
- When a test tool is switched on for a checklist that had no tests in it, **go back to the code**
  for every check: write its test from the code, correct the checks that are out of date, and add
  the checks a section is missing (`add_check`), each with its test.
- **Where the code comes from** doesn't change the rule, but use the **most up-to-date** code. Look
  at every source you can reach: the local folder, your own GitHub access, and qarunbook's
  (`code_sources`, `repo_files`, `read_repo_file`). Use the one that's newest. Local is often ahead
  of GitHub (changes not yet committed or pushed: check `git status` and `git log` against the
  remote), or GitHub is ahead of an old local checkout. Make sure it's the branch the app being
  tested is built from. Say in one line which source you used and why. Nothing has to be installed
  first, not the qarunbook helper and not a test tool.
- Every test names the files it was written from (`set_check_scripts` `from_files`), as paths in
  the repository (or `repository:path`). qarunbook refuses a test without them.
- Every test follows its tool's own rules and best practice — how Playwright, Cypress and Maestro
  actually read a test (whole-text regex in Maestro, tab labels reading "Home\nTab 1 of 5" on iOS,
  the keyboard covering fields on Android, strict mode in Playwright, queued commands in Cypress,
  waiting on state never on time, independent tests that make their own data). `check_scripts` and
  `automated_tests` return them as `rules`: read them before the first test of a session and write
  every test to them. A test that breaks one of them is wrong even if it passes once.

- If the app's checklists are written by qarunbook's AI or the person's own key, qarunbook writes
  the tests itself, from the code, under the same rule — a checklist written from the code comes
  with its tests, and switching a tool on (or **Write … tests from the code**) goes back to the
  code for every check.
- If **you** write the checklists (the person's own assistant), write the tests yourself, a
  section at a time, in each framework that is on, and save each with `set_check_scripts` (its
  description has the exact format for Playwright, Cypress and Maestro), naming the files in
  `from_files`. Follow the method below.

### The method: every test from the screen's code

You have the code, so nothing about a screen is a guess: what it says, where things sit, how they
are styled, how a person gets there. A test that taps a name the screen does not draw, or a thing
it never scrolled to, fails on every run. Read before you write.

1. **Open the screen before writing a step.** For each step, open the file that draws that screen
   — web: the route's page and the components it renders; phones: the screen under `app/` or
   `screens/` and its components — and the files that lead to it (links, tabs, menus,
   `router.push`, `navigation.navigate`). Follow that path in the test. Never write from the
   checklist's wording, a screenshot or memory.
2. **Take each name as the code draws it.**
   - An id first: `testID` (React Native; Maestro `id:`), `data-testid` (web; `getByTestId`,
     `[data-testid=…]`).
   - Otherwise the visible words, copied character for character (apostrophes, "…", capitals).
   - Read the style as well as the words: `textTransform: 'uppercase'` or `'capitalize'`, CSS
     `uppercase`/`text-transform`, and tab bars that capitalise their labels (Material top tabs on
     Android) draw different letters from the source — match what is drawn (`OUTCOMES`) or use a
     case-insensitive pattern (`(?i)outcomes`, `/outcomes/i`).
   - Words from a translation file or an option list (`t('…')`, an options array) — look them up
     and use the words shown.
   - An icon-only button: its `accessibilityLabel` / `aria-label`. With neither and no id, it
     cannot be found reliably: say so, and use an id the code does have nearby.
3. **Know where it sits.** The code gives the order of the page. Anything inside a ScrollView,
   FlatList or long page after other content starts off-screen: scroll to it before tapping or
   checking it (Maestro `scrollUntilVisible`; on the web, a lazy list must be scrolled to load).
   A bottom sheet, modal, tab or collapsed section is opened first.
   **Every screen on the path, including the ones in between.** The code shows each sheet, dialog
   or prompt that appears along the way and when: an "Are you sure?" after a skip, an
   onboarding or permission prompt, a cookie banner. Handle each one, or the test stops there.
   (Sabi, Oct 2026: every sign-up test stopped at the "Are you sure about this?" sheet that
   follows "I'll do it later", because the tests went straight to the next screen.)
4. **Words that come from data are not in the code.** A name, amount, balance, date or count is
   matched by its id, by the fixed words beside it, or by a pattern (`₦[0-9,.]+`, `/\d+ results/`) —
   never by a value you happened to see. Text shown only in some states (an empty list, a funded
   or verified account) needs that state: make it in setup, or use a saved account that has it.
5. **Platforms differ in the code, so the tests do too.** `Platform.OS`, `.ios.tsx` /
   `.android.tsx` files and separate mobile web components draw different things: write for what
   each platform draws. One phone flow serves Android and iOS only where the code is the same.
6. **A value a flow saves must exist before it is used.** A `copyTextFrom` / `evalScript` value
   (`${output.x}`) that was never set is `undefined`, and the flow then looks for the word
   "undefined": qarunbook counts that test as broken. Save the value on a step that is sure to
   run, and test the script once on a device.
7. **Wait for what loads.** After a step that fetches data, wait for the element the next step
   needs (`extendedWaitUntil`, `expect(…).toBeVisible({ timeout })`, `.should('be.visible')`) —
   never a fixed sleep.
8. **Sign in the saved way, arrange in setup, check exactly the expected result.**
   `qa.signIn('Name')` / `cy.qaSignIn('Name')`; on phones `runFlow: ../qarunbook/sign-in.yaml`
   with the account's variables when the app has a saved phone sign-in (`test_accounts` says), else
   `${ACCOUNT_<NAME>_USERNAME}` / `_PASSWORD`. A fresh account with `qa.signUp()` /
   `cy.qaSignUp()`, the test inbox with `qa.email()` / `qa.emailCode()` (Cypress `cy.qaEmail()` /
   `cy.qaEmailCode()`; Maestro `${TEST_EMAIL}` and `../qarunbook/email-code.js`), and
   `qa.unique('x')` / `cy.qaUnique('x')` / `${UNIQUE}` for names that must not repeat. Arrange
   inside `qa.setup` / `cy.qaSetup`. Never a password in a test.

### Left to people: only for a reason on the list (enforced)

A check is left to people (`manual_why` plus `manual_reason`) ONLY for one of these:
`money` (a real card, bank or live payment), `camera` (photo, scan, recording), `identity`
(biometrics, liveness, an ID document), `physical-phone` (a real SMS to a handset, push on a
physical device, phone OS settings), `outside-sign-in` (Google, Apple or another provider's own
sign-in page), `design-file` (comparing with a Figma file), `long-wait` (something that only
happens after more than 30 minutes), `judgement` (looks right, feels fast).

Never for: a wait of up to 30 minutes (wait in the test, with a long enough timeout), an email
(read the test inbox), an account or data in a state (make it in setup, or use a saved account),
or two people or devices (two browser sessions with `qa.otherPage()`, or the phone against the
website). qarunbook refuses any other reason and the check stays owed its test. Only `judgement`
checks go to the AI tester; the rest are never tried by a run.

### Pre-save check — before EVERY `set_check_scripts` (mandatory)

Do this for every test, every time, including tests a subagent wrote. It is not optional overhead.

1. **Walk the screen as the code draws it at that moment**, step by step. For every tap and every
   assertion ask:
   - Is it on screen now, or must it be scrolled to first (`scrollUntilVisible`, rule 2)?
   - Is a dialog, bottom sheet, toast or permission prompt covering it (rule 9)? Close it first.
   - Is the keyboard up from the last `inputText` (rule 12)? Hide it, or tap a heading above.
   - Do the same words appear twice (the page and a toast, a heading and its button, rule 10/13)?
   - Is it a Flutter merged label (a card read as one label, rule 23) or a tab label
     (`"Home.*"`, rule 11)?
2. **Go through the framework's full rule list** (the rules `check_scripts` returns), one by one,
   against the test.
3. **Then save**, with `rules_checked`: one line per assertion saying how it is visible, naming
   its text or id (e.g. `"Welcome Back": first screen, top, no dialog, keyboard closed`). qarunbook
   refuses a test whose `rules_checked` is empty, boilerplate, or skips an assertion, and refuses
   tests that break a rule it can check (it names the rule number). Use `validate_only: true` to
   check a test without saving it.

When you hand test writing to a subagent, give it the full rules (or this skill) and this check.
Never tell it to skip or ignore the rules.

### Prove them before writing the rest

A test that has never run has never passed. qarunbook enforces this: a saved test is "not proven"
until its first real result on the live app (a pass, or a fail the app caused). A run proves new
tests first, in a run of their own, and stops itself when 5 of them (and over a third) don't
match the app. After the first three tests of a section, save them
and run them: `run_tests` (app, platform, `refs`) on each platform, then `run_results`. A test
that stopped because it could not find something is your mistake, not the app's — read that
screen's code again, find what you got wrong, and fix the same thing in every test of the section
before writing more. Only then write the rest, and run the section once it is saved.

When nothing can run them (no connected computer, the device is busy), save them and tell the
person plainly which sections' tests have not been proven yet.

## Keep it up to date after every fix

The checklist is never finished. Whenever a fix lands or a screen changes, go back to the code
for the area it touched. Correct the checks it made out of date, and rewrite their tests from the
code before anyone runs them. A run should never be what finds a missing or out-of-date test.
Before you hand over to a run, `progress` must show `no_usable_test` at 0 for the area, and the
saved sign-in must be proven to work (see "The method" in the qa-runbook skill).

## Then offer to run it

Finish by telling the user what is now in qarunbook — the app, how many sections
and checks, which platforms — and **ask whether they want to start testing now**
with the `qa-runbook` skill. For example:

> The plan is in qarunbook as "Acme Shop": 14 sections, 212 checks, on web,
> Android and iOS. Want me to start running it now with the qa-runbook skill?
> I can take the whole plan, one section, or one platform.

If they say yes, start the `qa-runbook` skill straight away on that app. You
already know which app it is, so do not ask again.
