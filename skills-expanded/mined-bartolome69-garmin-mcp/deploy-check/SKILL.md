---
name: deploy-check
description: The checks to run before and after every deploy of the hosted Daash server (garmin-mcp-1b4387 on Fly). Use whenever a change is about to be deployed, when Bart says "deploy", and again within the hour after a deploy finishes. Covers the local test suites, checking a change against real users' data and state rather than the case it was built for, a dry run for anything that emails or messages people, checking plan numbers against a real plan, and the post-deploy checks in PostHog.
---

# Deploy check

Daash is live with real people every day. Most bugs that reached them were not
caught by the tests because the change was only tried against the case it was
built for. This checklist exists to test changes against **real users' data and
the state they are in on the day the change goes live**.

Work through every section. Say in the report which checks were skipped and why.

## Ground rules

- Deploy only when Bart's latest message says "deploy". A "deploy" covers what
  existed when he said it, not code written afterwards.
- Deploy: `gh api -X POST repos/bartolome69/garmin-mcp/actions/workflows/deploy-hosted.yml/dispatches -f ref=main`,
  then watch the run until Test, Check sign-in and Deploy all succeed.
- Fetch and merge `origin/main` before pushing; other sessions merge PRs into it.
  Never force push. Push to `main` and to the session's branch.
- Keep emails, distinct ids and secrets out of this repo: it is public.

## 1. Before deploying

### 1.1 Local test suites (all must pass)

```bash
# Once per container: Python 3.12 (3.11 can't install the pinned garminconnect)
/usr/bin/python3.12 -m venv .venv && .venv/bin/pip install -r requirements-hosted.txt

for t in hosted_test oauth_test smoke_test progress_test official_test signup_test; do
  echo "== $t"; .venv/bin/python tests/$t.py 2>&1 | grep -E "  FAIL|check\(s\) failed|all checks passed|Traceback"
done
NODE_PATH=$(npm root -g) node tests/card_test.js 2>&1 | tail -1
```

- Every new behaviour gets a test in the matching suite, including the case
  that should **not** happen (the email that shouldn't go, the file that should
  be refused).
- The smoke test caps the size of the tool list (every tool description is sent
  in every chat). Trim wording rather than raise the cap.
- Changed `docs/_privacy-source.html`? Rebuild:
  `python3 scripts/build-page.py docs/_privacy-source.html docs/privacy/index.html`.

### 1.2 Read the diff as a reviewer would

`git diff origin/main` and ask:
- What existing accounts does this touch the moment it is live, not just new ones?
- What does it do with data in a shape I didn't test (empty, huge, another
  language, miles, a plan from a coach, two plans at once, an official-route
  account with no history)?
- Could it show a number that is wrong but looks right?
- Does what the model is told match what the card shows?

### 1.3 Blast radius: answer each that applies

| If the change… | Check before deploying |
|---|---|
| **Sends email or any message** | Run it in log-only mode first, or compute who would get it **right now** (query in 3.2) and show Bart the count and why. Check it can't go to existing accounts for whom it's wrong. |
| **Parses a file or user text** | Try real samples, not hand-made ones. Ask for exports in other languages and in miles if none are on hand. Look at the countries of recent users (query 3.1): about half aren't English-speaking. |
| **Changes numbers on the card** (totals, km, phases, done/planned) | Call `get_plan` through the Daash connector on Bart's own account (his 24-week London build, label `MAR`) and compare weekly totals with the sessions in it. Totals must add up, and nothing unknown may be drawn as zero. |
| **Changes sign-in or OAuth** | Run signup and oauth tests; afterwards watch connections against token pickups (query 3.4). Phones with Claude through Garmin's page are fragile. **Never switch every new sign-up to a different route at once.** The password route is everyone's; Garmin's page opens to new sign-ups only after Garmin confirms in writing, and to a test group first. Schedule a check of completed sign-ups for an hour later and for the next morning before ending the session. |
| **Reads Garmin data in a new way** | Think about Garmin's official route (data only from connection day, no fitness or recovery tools) as well as the password route. |
| **Changes what tools say to the model** | Check the wording can't lead it to contradict the card or ask the user to change their plan for a display bug. |
| **Touches long plans** | Test 1, 12, 24 and 30 weeks; partly-read weeks; races; phases including Taper. |

### 1.4 Ship small

One concern per deploy where possible, so a misbehaving piece is easy to find.

## 2. After deploying (within the hour)

1. Confirm the run: all of Test, Check sign-in and Deploy succeeded.
2. Look at the first real events (queries in section 3):
   - **Errors**: any `$exception` since the deploy.
   - **Cards**: `card_shown` with `ok = false`, against the previous day.
   - **Tool use**: `tool_used` per hour holding steady.
   - **Sign-in**: `connector_connected` against `connector_token_issued` (3.4), and `sign_in_failed` reasons.
   - **The new feature's own events**: firing, for the right people, with sensible values (for example who got an email and how long ago they connected).
3. If something is wrong: tell Bart straight away with the numbers, fix, and
   ask to deploy the fix. Don't wait to be asked.

## 3. PostHog queries (project 127720)

Exclude Bart's own accounts from user counts (their distinct ids aren't kept in
this public repo: take them from Bart or recent session notes). Times in
Europe/London.

**3.1 Who uses Daash now: countries, apps, devices, route (last 7 days)**
```sql
SELECT toString(properties.country) AS country, toString(properties.app) AS app,
       toString(properties.device) AS device,
       if(toString(properties.route)='official','garmin_page','password') AS route, count() AS n
FROM events WHERE event='connector_connected' AND timestamp > now() - INTERVAL 7 DAY
GROUP BY country, app, device, route ORDER BY n DESC
```

**3.2 Who an email would reach right now** (adapt to the feature's rule; run before switching anything outbound on)
```sql
SELECT distinct_id, min(timestamp) AS connected, argMin(toString(properties.route), timestamp) AS route
FROM events WHERE event='connector_connected' AND timestamp > now() - INTERVAL 14 DAY
GROUP BY distinct_id ORDER BY connected
```
Then, for that list, check the state the rule depends on (for example: have
they already had activities? `tool_used` with `get_activity_details` before now
means they have).

**3.3 Errors and failing cards since the deploy**
```sql
SELECT event, toString(properties.error) AS error, toString(properties.app) AS app, count() AS n
FROM events WHERE timestamp > now() - INTERVAL 1 HOUR
  AND (event = '$exception' OR (event = 'card_shown' AND toString(properties.ok) = 'false'))
GROUP BY event, error, app ORDER BY n DESC
```

**3.4 Connections the app never picked up**
```sql
WITH c AS (SELECT distinct_id, if(toString(properties.route)='official','garmin_page','password') AS route,
                  toString(properties.app) AS app, toString(properties.device) AS device, timestamp AS t
           FROM events WHERE event='connector_connected' AND timestamp > now() - INTERVAL 1 DAY),
     tok AS (SELECT distinct_id, groupArray(timestamp) AS ts FROM events
             WHERE event='connector_token_issued' AND timestamp > now() - INTERVAL 1 DAY GROUP BY distinct_id)
SELECT c.route, c.app, c.device, count() AS connections,
       countIf(arrayExists(x -> x >= c.t AND x < c.t + INTERVAL 10 MINUTE, tok.ts)) AS picked_up
FROM c LEFT JOIN tok ON tok.distinct_id = c.distinct_id GROUP BY c.route, c.app, c.device
```

**3.5 A new event, by value**
```sql
SELECT formatDateTime(toTimeZone(timestamp,'Europe/London'),'%d %H:%i') AS at, distinct_id, properties
FROM events WHERE event = '<new_event>' AND timestamp > now() - INTERVAL 1 DAY ORDER BY timestamp
```

## 4. Report to Bart

Short, plain words:
- What's going out, in one line per change.
- Tests: all suites pass; the new checks added.
- Checked against real data: what and how (for example "would email 3 accounts
  connected today, none with earlier runs").
- **Not tested**: say it plainly (for example "hand-made files, not real exports").
- After deploy: what the first events showed, or when you'll look.

## 5. Lessons so far

Each of these reached real people. The check that would have caught it is now
in the list above.

| Date | What happened | What would have caught it |
|---|---|---|
| 30 Oct | Long-plan change left threshold sessions out of later weeks' totals: bars 15–18 km short but looking whole | 1.3 numbers: compare totals with Bart's real plan |
| 30 Oct | Phase bands carried Build to race day, then broke into pieces | 1.3 long plans: check phases with partly-read weeks |
| 31 Oct | First-run email went to accounts days old that already had runs | 1.3 email: who it would reach right now (3.2) |
| 31 Oct | CSV upload refused Italian and French files, three tries each | 1.3 parsing: real samples, other languages; 3.1 countries |
| 31 Oct | Claude's iPhone app didn't pick up 4 approvals through Garmin's page | 2 after deploy: connections against pickups (3.4) |
| 11 Nov | Sign-ups reopened on Garmin's page for everyone after one re-approved test account; Garmin's cap was still on, and 16 people tried overnight and none connected | Garmin's page stays closed to new sign-ups (GARMIN_OFFICIAL_SIGNUPS=paused) until Garmin confirms in writing that the cap is lifted; then a small test group first, with completed sign-ups (3.4) checked within the hour and again the next morning, before everyone |
