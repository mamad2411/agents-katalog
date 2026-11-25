---
name: vibes-are-not-a-spec
description: Turn a vague request like "make it secure", "make it look professional", "make it easy to use", "make it work on my phone", "make it automatic", "make it smarter", "make it fast", "is it actually done?", "fix it" or "make it better" into a full audit-and-fix playbook with evidence, tests and stop rules. For people building apps and sites with AI who are not engineers.
---

# Vibes are not a spec

**This file is the whole skill.** Give it to Claude Code, Codex or any coding agent. Claude Code: save it as `~/.claude/skills/vibes-are-not-a-spec/SKILL.md`. Codex: `~/.agents/skills/vibes-are-not-a-spec/SKILL.md` (older versions: `~/.codex/skills/`). Claude app: upload it as a skill. Any other chat: paste it in.

## Agent: do this when someone uses one of these words
1. Match their intent to the table, including paraphrases. If several apply, name them and their order in one line. If none fits, ask one focused question first. Stay within what they asked.
2. Say what you are about to check in plain language, one short paragraph, no jargon. The owner may not be technical.
3. Run the playbook together with the Rules. Answer every question you can from the product itself; ask the owner only what the product can't tell you.
4. Report in plain language first (what was wrong, what changed, what they must do), the technical table after.

| They say | Run |
|---|---|
| make it secure, is my app safe, make sure nobody can hack it | Database LARP, then API LARP, then Edge & Headers LARP |
| protect my users' data, is my database safe | Database LARP, then API LARP |
| protect my API, lock down my backend | API LARP |
| add security headers, fix the security warnings | Edge & Headers LARP |
| make it look professional, make it clean | Design LARP |
| make it easy to use, people get confused | Usability LARP |
| make it work on my phone, make it responsive | Phone LARP |
| make it automatic, automate this | Automation LARP |
| make it smarter, the AI gives bad answers | AI Quality LARP |
| make it fast, make it efficient, it's slow, get 100 on Lighthouse | Speed LARP |
| is it actually done, is it done, did it work, are you sure | LARP check |
| fix it, it doesn't work | Debug LARP |
| make it better, improve this | Better LARP |

## Rules (apply to every playbook)

```
Rules for this audit.
Inventory before judging, judge before fixing.
For security playbooks, write an access matrix first: who may do what with which data
(anyone, logged-in user, owner, team, admin, signed webhook, job); if my intent is
unclear, ask, don't assume owner-only.
For implementation claims cite file:line; for behaviour claims save the command or
browser steps, the actual result, the environment and the artifact path.
Use test accounts and synthetic data.
Before saving or reporting evidence, redact passwords, keys, tokens, cookies, connection
strings and personal data; identify a leaked secret by location and key type, never by
value.
A code citation alone cannot prove behaviour.
PASS applies only to the scenario and environment actually exercised.
Check which browser, runtime and test tools exist first; if one is missing, mark the
affected checks NOT RUN.
Never invent runs, screenshots, users or results.
Status per check: FAIL, PASS (with how you checked), NOT APPLICABLE (with why),
UNVERIFIED (with what I must check and where), NOT RUN (never counts as PASS).
Only I can mark something ACCEPTED.
Exercise the actual application logic and never stub the behaviour being asserted; use
sandbox services or labelled fakes for unsafe external effects and leave untested
provider behaviour UNVERIFIED; security tests run as real low-privilege users
(anonymous, user A, user B), never with an admin or service key.
In security tests, every denied test gets an allowed twin that succeeds and every denied
write is followed by proof nothing changed.
Fix highest severity first, one change at a time, re-run the proof after each.
Abuse and destructive tests only on local or staging with test data.
Never deploy, merge, delete production data, change DNS, rotate keys or print secrets
yourself: give me the exact steps.
You may create and remove clearly identified test fixtures on local or staging.
Don't swap the stack or add paid services without asking.
P0 means ongoing severe harm or a core service down, P1 a core task blocked or real user
harm, P2 a lesser defect; taste is a recommendation, not a failure.
After 5 fixes, checkpoint progress and remaining risks; revert an unsuccessful change of
yours without touching unrelated work; a playbook's own limit takes precedence.
Report: findings (severity, proof, status), changes per file, tests with before and
after, what I must do, what you couldn't check.
```

## Playbooks

### API LARP

```
API LARP.
Assume every backend entry point can be abused until a request proves otherwise.
Inventory every callable surface, not just /api: route handlers, server actions, edge
functions, client-callable RPC or database functions, webhooks, cron and jobs, each with
method, path, file:line, who may call it, what it reads or changes, which fields it
accepts and returns.
Then probe:

(1) as user A, read, list, change and delete user B's object by swapping the ID in URL,
    body and query;
(2) call protected surfaces with no session, an expired one and a tampered one and check
    no work happens before the check (public routes and signed webhooks keep their own
    correct check);
(3) responses leaking fields the caller shouldn't see and requests that set role, owner,
    plan, credits or price by adding them, nested objects included;
(4) no numeric limit on requests, page size, body size or time for expensive calls (AI,
    email, uploads) and limits held in memory on serverless;
(5) admin actions callable by a normal user because the check lives only in the UI;
(6) one-time benefits (coupon, trial, invite, credits) redeemed twice by two
    simultaneous requests;
(7) server fetching a user-supplied URL that can reach localhost, 169.254.169.254,
    private ranges or IPv6 equivalents, including via redirects;
(8) stack traces, SQL errors or debug routes in responses;
(9) forgotten test, seed or old routes still live;
(10) webhooks or third-party responses used without signature check or validation;
(11) user input reaching SQL, shell or templates as code.

For each finding: severity (P0/P1/P2), the exact request and response that prove it, the
fix at the point the data is accessed (caller from the verified session, never the body;
field allowlists in and out; server-side role checks; limits in a shared store;
signature on the raw body; resolved-address checks for fetches; bound parameters) and
the guardrail that stops it coming back: an automated test with its allowed twin.
Re-run the proving request after each fix.
```

### Database LARP

```
Database LARP.
Assume any row can be read or changed by the wrong person, script or AI tool until a
test proves otherwise.
Identify the database first: these checks target Supabase and PostgreSQL; on another
stack map each check to its equivalent or mark it NOT APPLICABLE with a reason.
Inventory every table, view and function in schemas the client API exposes, every
storage bucket, every use of a secret key (service_role, sb_secret_, database password
or connection string) and every AI tool or MCP server connected to the database with the
credentials it uses.
Per table: RLS on or off, every policy with command, role, USING and WITH CHECK and the
grants client roles hold.
Then probe anonymously with the publishable key and no user token and as user A and user
B with that key plus each user's own valid token:

(1) tables in an exposed schema with RLS off and client grants;
(2) policies broader than the access matrix (applicable permissive policies combine with
    OR and restrictive ones with AND, so judge each policy's role, command, USING and
    WITH CHECK together with grants);
(3) users updating their own row can also set role, plan, credits or verified, or move
    user_id to someone else;
(4) views without security_invoker and client-callable SECURITY DEFINER functions
    returning rows the caller may not see;
(5) a secret key in frontend code, the built bundle, source maps, the repo, git history,
    CI logs or an MCP config;
(6) functions building SQL from text with EXECUTE;
(7) backend routes using the secret key without their own object check;
(8) an AI tool that can read private data and also reads text users wrote (tickets,
    comments, profiles, documents), only if one exists;
(9) public buckets holding private files;
(10) no backups or point-in-time recovery, schema changed by hand on production;
(11) integration tokens or personal data readable by anyone with table access.

For each finding: severity, the query or request and result that prove it, the fix (RLS
plus per-operation policies from the access matrix using (select auth.uid()); revoke
table-level UPDATE from every applicable client role, including inherited grants, then
grant UPDATE only on approved columns; change sensitive columns through a server
function that checks the caller's permission; security_invoker on views, execute revoked
or an auth check plus fixed search_path on definer functions; leaked secret keys listed
for me to rotate; AI tools stripped of secrets and unneeded data first, read-only,
scoped, no free SQL where a narrow function works, every sensitive read and every write
shown to me before it runs, nothing they write lands where users can see it unreviewed)
and the guardrail: a test as a real user with its allowed twin.
A model refusing a planted instruction once proves nothing: prove the tool can't reach
the data.
```

### Edge & Headers LARP

```
Edge & Headers LARP.
Assume the edge leaks until a request proves otherwise.
List production and preview URLs.
Use curl -sS -I for first header checks on the home page, the login page and one API
route, then test the real GET or API method where behaviour matters, with a test session
and a browser for cookies, CORS, caching and redirects.
Abuse tests only on local or staging.
Check:

(1) http serves content without upgrading to https (check the redirect destination;
    prefer a permanent redirect), or an https page lacks HSTS;
(2) on HTML pages, CSP missing or allowing 'unsafe-eval' or *, no object-src 'none', no
    base-uri, no frame-ancestors, judged by actual effect; JSON API responses don't need
    a document CSP;
(3) X-Content-Type-Options nosniff, Referrer-Policy or Permissions-Policy missing;
(4) an unapproved origin (send Origin: https://evil.example and Origin: null) can read a
    private response in a real browser with credentials; report * with credentials as an
    invalid configuration and separately prove whether private data is readable;
(5) request concrete paths for secret files, backups and debug endpoints (/.env,
    /.git/config, /.DS_Store, source maps, .bak, .sql, .zip, /admin, /debug, API docs,
    GraphQL introspection), inspect the content and follow redirects; FAIL only when an
    unauthorized caller gets sensitive content or performs a protected action and record
    soft 404s separately;
(6) version numbers in Server or X-Powered-By, stack traces or framework error pages in
    production;
(7) session cookie without Secure, HttpOnly, SameSite, or scoped to the parent domain
    without need;
(8) /login?next=https://evil.example (and redirect=, returnUrl=) leaves the site;
(9) pages with personal data cached by the CDN or without Cache-Control: private,
    no-store;
(10) preview deployments public or on production keys and data, staging indexable;
(11) DNS records pointing at services we no longer use: list them, never touch DNS.

For each finding: severity (P0/P1/P2), the exact request and response that prove it, the
fix in the file that owns the config and the guardrail that stops it coming back: a line
in scripts/check-edge.sh that fails on it.
Fix highest severity first; prepare CSP as report-only, list what really loads, test it,
then prepare the enforcing config and give me the deployment steps; re-run the proving
request after each fix; click through the 3 main pages and check the console for CSP
errors; revert if anything breaks.
```

### Design LARP

```
Design LARP.
Assume it looks unfinished until screenshots prove otherwise.
Before judging, ask me: who is this for, 3 sites I like and 1 I don't and why.
If I have none, propose 2 written directions and wait for my choice.
Capture screenshots of the 3 main pages at 1440 and 390 wide, plus empty, loading, error
and success states.
Then check:

(1) type: list every font family, size and weight in use; flag more than 2 families or
    sizes with no clear scale for review, FAIL only on a violated requirement or
    demonstrated usability defect; and, as our own readability recommendation rather
    than a failure, body text under 16px or lines over about 80 characters;
(2) spacing: list every margin, padding and gap value; flag near-duplicates like 13, 14
    and 15px for review and keep intentional adjustments;
(3) hierarchy: each page has one h1 and one visually dominant primary action;
(4) colour: list every colour; text contrast at least 4.5:1, large text at least 3:1 and
    3:1 for the visual parts needed to identify a control;
(5) consistency: count the variants of buttons, inputs, cards, corner radius and shadows
    and name every variant with no purpose;
(6) alignment: elements off the shared grid or with uneven edges;
(7) states: hover, keyboard focus, disabled, empty, loading, error and success exist for
    every interactive element;
(8) leftovers: lorem ipsum, placeholder or broken images, default favicon, default page
    titles, mixed capitalisation, emoji used as icons;
(9) trust: real contact, privacy and legal links that work.

For each finding: severity (P0/P1/P2), the screenshot or file:line that proves it, the
fix and the guardrail that stops it coming back.
Reuse the existing design system; consolidate only the values behind a demonstrated
defect and keep intentional exceptions.
Don't rewrite copy, change the brand or invent logos, testimonials or numbers.
Guardrail: a check that fails on colours or spacing values outside the tokens, plus
before and after screenshots at both widths.
```

### Usability LARP

```
Usability LARP.
Assume a first-time visitor gets stuck until a walkthrough proves otherwise.
Work out the likely user and propose 3 start-to-finish tasks from the product itself; I
only correct them.
Run each task in a real browser with the right starting point (signed-out visitor, new
account, or returning account with realistic data), record every screen, click, required
field and error with screenshots and verify the result was really saved.
Check:

(1) the first screen says what this is, who it's for and what to do next;
(2) steps per task and every step that could be removed or defaulted;
(3) sign-up or payment demanded before the user sees any value;
(4) words: buttons and labels in the user's language, no internal or technical terms;
(5) forms: every field needed, visible labels rather than placeholders, correct input
    types, errors next to the field saying how to fix it, typed data kept after an
    error;
(6) feedback: every action shows that it's working and that it finished;
(7) dangerous actions need a confirmation or can be undone;
(8) dead ends: empty states, 404s and errors offer a next step;
(9) orientation: the user can tell where they are and go back and browser back works;
(10) keyboard: every task can be finished without a mouse, focus is visible, controls
    have names.

For each finding: severity, the screenshot and step that prove it, the smallest fix and
the guardrail: an end-to-end test per task, with a maximum step count written down.
Don't redesign pages or remove features without asking.
Your walkthrough is not a user test: mark "real users understand it" as UNVERIFIED and
give me a short script to watch 5 people try the 3 tasks without helping them.
```

### Phone LARP

```
Phone LARP.
Assume it breaks on a phone until each width proves otherwise.
Propose the 3 tasks that must work; I only correct them.
Using device emulation, run them at 320, 360, 390 and 430 wide in portrait, 768 wide and
one phone in landscape, with screenshots of every step.
Emulation proves only the browser you ran; the real keyboard, browser bars, notch and
iPhone focus zoom stay UNVERIFIED without a real device.
Give me exact URLs and steps for a 2-minute check on my own phone.
Check:

(1) the viewport meta tag exists and doesn't block zooming;
(2) horizontal scrolling: at each width, compare document scrollWidth with the window
    width and name the element that overflows;
(3) tap targets measured against WCAG 2.5.8 (24 by 24 CSS px unless the spacing,
    equivalent, inline, user agent or essential exception applies, recording which) and
    44 by 44 recommended for primary actions as our own rule;
(4) inputs under 16px font size flagged as an iPhone zoom risk, to confirm on a real
    phone and never fixed by disabling zoom;
(5) forms: correct type, inputmode and autocomplete so the right keyboard and autofill
    appear;
(6) 100vh layouts cut off by the browser bars (dvh or svh handle the bars, not the
    keyboard);
(7) the on-screen keyboard covering the active input or submit button;
(8) content under the notch or home bar (safe-area-inset);
(9) anything that only works on hover;
(10) fixed headers, banners and chat bubbles covering content or buttons;
(11) tables, modals, menus and long words at 320 wide;
(12) text enlarged to 200% still readable with nothing cut off;
(13) if speed is a complaint, run the Speed LARP on mobile.

For each finding: severity, width, the screenshot or measured value that proves it, the
smallest fix and the guardrail: an automated test at each width that fails on horizontal
overflow and completes the 3 tasks.
Desktop must look the same as before unless I agree.
```

### Automation LARP

```
Automation LARP.
Assume every automation will fire twice, fail halfway and stop silently until a test
proves otherwise.
Before building or judging, write one row per automation: what triggers it, what goes
in, each step, what comes out, where the result is stored, who gets told, who owns it
and what it may cost.
Ask me for anything missing.
Then check:

(1) trigger: the exact event or schedule and what happens if it fires twice or two runs
    overlap;
(2) duplicates: for each email, payment, file or record, a stable key stored before
    sending, the provider's own duplicate protection where it exists and a plan for when
    the result is unknown (a timeout doesn't mean it didn't happen); test two copies at
    once and a failure right after the provider accepted;
(3) failure at each step: timeout set, retries capped with increasing delay and only
    steps that are safe to repeat get retried;
(4) half-finished runs: what state is left if step 3 of 5 fails and how it resumes or
    undoes;
(5) after the last retry: failed jobs go to a visible list and a named person is told;
(6) silent death: a scheduled job that doesn't run raises an alert;
(7) bad input: missing, malformed, huge or duplicate data stops cleanly before any side
    effect;
(8) permissions: each step has only the access it needs;
(9) cost: a hard cap on runs, items and AI spend and no loop without an end;
(10) keep routine automation I already authorised; require my approval, with a concrete
    preview, for new recipients, bulk or irreversible actions, or anything outside the
    approved templates, permissions and budget;
(11) records: every run has an ID and a log of input, steps, result and error, without
    secrets or personal data;
(12) control: a dry-run mode and an off switch I can use without a developer.

For each finding: severity, the file:line or run that proves it, the fix and the
guardrail: a test that replays a duplicate event, forces a failure at each step and
feeds bad input and records how many times each side effect actually happened in each
tested case.
Test with fake recipients and test payment keys only.
```

### AI Quality LARP

```
AI Quality LARP.
Assume every "it got smarter" is one lucky answer until a test set says otherwise.
Ask me: smarter at what and what does a good answer look like?
Collect 20 to 50 real examples with the expected result, including hard cases, missing
information and cases where the right answer is "I don't know" or "ask a person".
Tune on those.
Afterwards have me or a separate process supply unseen cases; never call examples you
have already read a blind test.
Write down how each answer is scored.
Run the current version and record the baseline, cost and response time.
Then sort every failure:

(1) wrong facts or invented details;
(2) it never received the data it needed;
(3) retrieval returned the wrong document or none;
(4) instructions missing, contradictory or buried;
(5) no examples of good output;
(6) output format broken;
(7) wrong tool, wrong arguments or a tool result ignored;
(8) answered when it should have refused or asked;
(9) forgot earlier context or lost it to truncation;
(10) too slow or too expensive.

Fix the largest failure group first, one change at a time, usually starting with data,
retrieval and instructions and changing the model last (our practice, not a law).
Keep a change only if the working set improves and nothing important gets worse.
For each finding: severity, the example IDs and the real outputs that prove it, the
change, before and after scores and the guardrail: the test set runs before every
prompt, model or data change.
Report the score on the unseen cases once, at the end.
Don't add autonomy, new tools or a bigger model to chase the score without asking me.
A handful of examples is directional, so say how many cases the result rests on.
```

### Speed LARP

```
Speed LARP.
Assume every "it's fast" is a guess until a measurement says so.
Pick up to 3 page types that matter (include a logged-in page if the app has one) and
confirm each URL renders its real content, not a redirect or error.
Fixed, written-down setup: production build, Lighthouse version, mobile emulation, same
throttling, cold cache; 3 runs per page, keep all, report medians for score, LCP, CLS,
TBT, transferred KB and requests; add PageSpeed Insights field data if it exists, with
its period, mobile or desktop and URL or whole origin, judged at the 75th percentile and
kept separate from lab medians (none is "unknown", not "good").
Targets: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, TBT under 200 ms,
Lighthouse performance 90 or more; 100 is not required.
Then find the cause in the trace, not in a checklist:

(1) the LCP element (image, poster or text) and which part is slow: server response,
    late discovery, download or render;
(2) CSS, fonts and scripts blocking first paint or LCP;
(3) the largest transfers and whether the first screen needs them;
(4) main-thread tasks over 50 ms during load and what runs in them;
(5) real interactions (menu, dialog, typing, checkout in test mode) measured in the
    DevTools performance panel, because TBT is not INP;
(6) the insertion, image, font or banner causing each layout shift, including after
    load;
(7) caching and compression on HTML, JS, CSS and media and what a repeat visit downloads
    again;
(8) every third-party script with its size, main-thread cost and load timing;
(9) slow server responses and requests that run one after another but could run
    together.

Fix only what a trace points at, one change at a time, using what the framework already
offers; never remove consent, analytics, auth or checkout and never change the design
without my yes; HTML may be cached with revalidation, personal pages never shared.
After each change, same setup, 3 runs, compare the raw metric against the run-to-run
spread, keep it or revert.
Guardrail: the named interactions still work after deferred scripts load, before/after
screenshots at mobile and desktop match, accessibility, best practices and SEO don't
drop.
Log per change: finding, change, before, after.
```

### LARP check

```
LARP check.
Run this after any task you told me is done.
Assume nothing works until it is proven.
Go through everything you changed or claimed and check:

(1) functions returning hardcoded or sample data instead of the real thing;
(2) tests that mock the logic they test, always pass, were skipped, or were edited to
    pass;
(3) try/catch or fallbacks that swallow errors and hide failure;
(4) validation, permission or signature checks that exist but never run on the real
    path, or only in the UI;
(5) async calls never awaited or checked;
(6) code paths, commands or migrations written but never executed;
(7) secrets or deployment-specific config hardcoded where it should come from the
    environment; intentional public URLs, constants and test fixtures are fine;
(8) words in your summary ("tested", "secure", "faster", "fixed") with no command
    output, test result or measurement behind them;
(9) parts of my request skipped, simplified or postponed without saying so;
(10) queries without limits, loops without an end, requests without timeouts.

For each: what you claimed, what you found, the evidence (file:line, the command and its
real output) and the Rules status.
Add REAL only for a claim supported by evidence, LARP for a contradicted or unsupported
claim.
Never upgrade to REAL without evidence.
Then fix every LARP item, most serious first, one at a time, show the real output after
each fix and give me the corrected summary.
```

### Debug LARP

```
Debug LARP.
Assume your first explanation is wrong until an experiment proves it.
Before changing anything, write down: what I did, what I expected, what happened, the
exact symptom, error and any available trace with secrets removed and how often it
happens.
Reproduce it and show the output; if you can't, say so and add the logging needed
instead of guessing.
If real users are affected right now, stop the damage first and tell me the option (roll
back, turn the feature off), then diagnose.
Ask what touched it last: recent commits, dependency updates, environment changes, data
changes.
List up to 3 possible causes, ranked, each with the cheapest test that would rule it
out.
Run those tests before editing code.
Name the root cause with evidence: file:line and the output that proves it.
Write a test that fails because of this bug, for the expected reason and not a setup
error and show it failing; if a bug can't be automated, save repeatable manual before
and after steps.
Make the smallest fix at the cause, then show that test passing and the existing tests
still passing.
Forbidden, unless I say yes: deleting or weakening a check, validation or test; catching
and hiding the error; hardcoding the expected value; special-casing the failing input;
increasing a timeout without knowing why it was slow; updating a snapshot just to make
it green; rewriting nearby code.
Search for the same mistake elsewhere and list it, but don't fix it in this change.
After 3 ruled-out causes or 2 failed fixes, stop and report what you learned; revert
only your own unsuccessful changes, keep useful tests and diagnostics, never touch
unrelated work.
Guardrail: the regression test stays in the suite.
Report: symptom, root cause, proof, the fix, before and after output and what you could
not verify.
```

### Better LARP

```
Better LARP.
"Better" means nothing until it has a number or a named judgement.
Before changing anything, ask me: better for whom and at what?
If I can't say, propose 3 possible goals, each with how we'd measure it and what it
would cost and wait for my choice.
Write down: one goal; one main measure; how it is measured, by whom and over what
period; the target; and up to 3 things that must not get worse.
Measure the current state and save it.
Then:

(1) list what stands between today and the target, with the evidence for each;
(2) rank by expected effect on the measure and by effort and mark which rankings are
    guesses;
(3) pick one change and predict what it will move and by how much;
(4) make only that change;
(5) measure again under the same conditions and compare;
(6) keep it only if the measure improved in the intended direction by more than a
    threshold set in advance and more than normal variation, with nothing protected
    worse; otherwise report it as inconclusive or revert only your change.

If the goal is a matter of taste, show the old and new side by side against criteria I
approved and I decide.
If the numbers are small, label the result directional rather than proven.
Forbidden: polishing things the goal doesn't touch, rewriting what works, changing the
measure halfway, or calling something better because it is newer or longer.
Stop when the target is reached, after 5 changes, or when two changes in a row don't
move the measure.
Guardrail: the goal, baseline and results stay in one file so the next session starts
from them.
Report: goal, before, each change with its result, after and what you'd try next.
```

This is a checklist, not a security audit. For anything that handles money or personal data, have a person who does security review it.

Made by @long.integer (Instagram). Sources for every playbook: the `extras/playbooks` folder in https://github.com/open-longlabs/vibes-are-not-a-spec
