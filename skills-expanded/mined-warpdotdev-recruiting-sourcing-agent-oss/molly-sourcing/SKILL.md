---
name: molly-sourcing
description: Executes Molly's daily sourcing cycle for approved roles. Use when triggered by the scheduled daily run for roles in Sourcing status, or when a recruiter explicitly asks Molly to start or resume sourcing.
---

# Sourcing

Triggered by the daily scheduled (cron) run once a role reaches `Sourcing` status (or when a recruiter asks Molly to run sourcing). For every role in `Sourcing`, Molly first folds in the talent team's feedback from the previous cycle — left as **notes** on yesterday's GEM candidates — updates the Profile Spec accordingly, then sources fresh LinkedIn candidates via Exa (`MOLLY_DAILY_SOURCING_TARGET`, default 25), submits each into that role's GEM project, and posts one daily digest to the sourcing channel.

The notes feedback loop is what makes sourcing sharpen day over day — it's the lightweight, ongoing analog of calibration. The team drops quick notes on the candidates they liked or didn't (right in GEM, where they're already reviewing), and the next run honors that signal. The digest closes the loop by reminding the team to leave feedback within the feedback window (`MOLLY_FEEDBACK_WINDOW_HOURS`, default 24h), before the next run.

GEM dedupes on LinkedIn handle, so re-running daily is safe — candidates already in GEM are matched, not duplicated.

## Inputs

- Env: `MOLLY_NOTION_API_KEY`, `MOLLY_EXA_API_KEY`, `MOLLY_GEM_API_KEY`, `MOLLY_SLACK_BOT_TOKEN`, `SOURCING_SLACK_CHANNEL_ID`, `MOLLY_TRACKER_DB_ID`
- Molly Tracker database: `$MOLLY_TRACKER_DB_ID`
- Each Sourcing role row must have a **GEM Project ID** (the GEM project candidates are filed into). Skip and flag any role missing it.

## Steps

### 1. Find roles in `Sourcing`

Query the Molly Tracker, filtering on the `Molly Status` status property:

```bash
curl -s -X POST "https://api.notion.com/v1/databases/$MOLLY_TRACKER_DB_ID/query" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"filter": {"property": "Molly Status", "status": {"equals": "Sourcing"}}}'
```

For each returned row, read: `Role name` (title), `JD Link` (url), `Profile Spec Link` (url), `GEM Project ID` (rich text). The JD/Spec page IDs are the last 32 hex characters of each URL.

The role's GEM project lives in the web app at `https://www.gem.com/projects/<GEM Project ID>`. Build this URL from the `GEM Project ID` — you'll link to it from the digest's **View candidates** button in step 8.

Process each role independently through steps 2–7, then post one combined digest in step 8.

### 2. Read the JD + Profile Spec

```bash
curl -s "https://api.notion.com/v1/blocks/SPEC_PAGE_ID/children?page_size=100" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

The search is driven by the Profile Spec's **Exa Search Strategy**, **Must-Haves**, **Evaluation Criteria**, **Target Companies**, any **Calibration Notes** (calibration already taught the spec what a strong match looks like — honor that feedback), and any **Sourcing Feedback Log** entries (the team's day-to-day notes feedback, already folded in — honor it too). Read the JD page too for added context.

### 3. Incorporate yesterday's feedback from GEM notes into the Profile Spec

Before sourcing anything new, fold in the talent team's feedback from the previous cycle. After each run the team reviews the candidates Molly filed into GEM and leaves quick **notes** on them (a 👍/👎 and a line on why) — that's how they steer sourcing day to day, the same way calibration steered the spec up front. Reading those notes first and updating the spec is what makes each run sharper than the last.

This is a no-op on the first run (no prior candidates yet) and on any day the team left no notes — in that case, skip straight to sourcing.

**a. Set the watermark, so each note is read once.** Find the most recent `## Sourcing Feedback Log — <date>` entry on the spec page (you already pulled the page in step 2) and use its run timestamp as the `created_after` bound below. If there's no log entry yet, fall back to ~`MOLLY_FEEDBACK_WINDOW_HOURS` hours (default 24) before now (the cron cadence). Because each run starts fresh with no memory of the last, this watermark is what keeps the same note from being applied twice.

**b. List the previous cycle's candidates in the role's GEM project.** Page through the project's candidates and keep those whose `created_at` is at or after the watermark — that's yesterday's batch.

```bash
curl -s "https://api.gem.com/v0/candidates?project_id=GEM_PROJECT_ID&page_size=100" \
  -H "X-API-Key: $MOLLY_GEM_API_KEY" \
  -H "Content-Type: application/json"
```

Paginate with `page`/`page_size` (1-indexed; max `page_size` 100 — the `X-Pagination` response header reports `total_pages`/`next_page`). If your key doesn't honor the `project_id` filter, list candidates and keep only those whose project membership includes the role's `GEM Project ID`.

**c. Read the notes on each of those candidates.** The notes endpoint returns an array of note objects and accepts `created_after`, so you only see feedback left since the last run:

```bash
curl -s "https://api.gem.com/v0/candidates/CANDIDATE_ID/notes?created_after=WATERMARK_ISO8601" \
  -H "X-API-Key: $MOLLY_GEM_API_KEY" \
  -H "Content-Type: application/json"
```

Read the text of each note (the note object's body/content field) plus its author and timestamp. Candidates with no new notes contribute nothing — skip them.

**d. Synthesize the feedback.** Cluster what you read into positive signals to lean into, negative signals / disqualifiers to avoid, and explicit directives (seniority, location, company types, must-have skills). Weight patterns that recur across several notes over any single offhand comment.

**e. Update the Profile Spec, then log it.** Patch only the sections the feedback actually bears on — **Must-Haves**, **Nice-to-Haves**, **Evaluation Criteria**, **Target Companies**, **Exa Search Strategy** — the same way calibration edits the spec (find the section's heading block and update the children beneath it; see `molly-calibration/SKILL.md` step 3). Keep edits concrete and search-driving: this is the spec today's search runs on.

Then append a dated log entry capturing what changed and why, stamped with this run's time so the next run can use it as its watermark:

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/SPEC_PAGE_ID/children" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"children": [
    {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Sourcing Feedback Log — YYYY-MM-DD"}}]}},
    {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Run at ISO8601_TIMESTAMP. Reviewed N notes across M candidates. Changes: ... Rationale: ..."}}]}}
  ]}'
```

If there were prior candidates but no new notes, still append a stamped "No new feedback this cycle" entry so the watermark advances, then proceed.

**f. Carry the summary into the digest.** Keep a short (1–2 line) plain-language summary of what you folded in this run — the recurring positive/negative signals and directives that changed the spec (or "No new feedback this cycle"). You'll surface this per role in the digest (step 8) so the team sees their notes reflected back. It's the same synthesis you just logged in the Sourcing Feedback Log, phrased for Slack.

### 4. Resolve Molly's GEM user ID

GEM requires a `created_by` user on new candidates. Fetch it once per run and reuse it:

```bash
curl -s "https://api.gem.com/v0/users" \
  -H "X-API-Key: $MOLLY_GEM_API_KEY" \
  -H "Content-Type: application/json"
```

Pick the user matching Molly's bot account (by name/email); fall back to the first user. Save its `id`.

### 5. Source the daily target of candidates via Exa

Run the spec's Exa Search Strategy — including the feedback updates you just made in step 3 — across 2–4 distinct angles, LinkedIn only. Over-fetch (`numResults` ~15–25 per query) so you net **`MOLLY_DAILY_SOURCING_TARGET` unique** profiles (default 25) after deduping within the run by LinkedIn handle **and after applying the minimum-tenure screen below**.

```bash
curl -s -X POST "https://api.exa.ai/search" \
  -H "Authorization: Bearer $MOLLY_EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY", "numResults": 25, "type": "neural", "includeDomains": ["linkedin.com"], "contents": {"text": {"maxCharacters": 3000}}}'
```

For each candidate, capture: full name (→ first/last), current title + company, **current-company start date / tenure**, **location** (city / metro / region), LinkedIn URL, the **handle** (path segment after `/in/`, e.g. `https://linkedin.com/in/jane-doe-123` → `jane-doe-123`), and a 1-line fit rationale citing specific evidence. **Location** and the **current role's start date / duration** both sit near the top of the profile text (in the header and the top of the Experience block), so they're reliably in the search snippet — pull them from there.

**Apply the minimum-tenure screen (`MOLLY_MIN_TENURE_MONTHS`, default 6 months).** Per the global sourcing rule (see `AGENTS.md`), drop anyone who has been at their current company for less than the threshold — they rarely move, so they waste sourcing effort. Read the current role's start date / duration from the top of the Experience block (LinkedIn's `... - Present` line and its `N mos / N yrs` duration) and measure it against today; if the tenure is under the threshold, exclude the candidate and pull in the next over-fetched profile so you still reach the daily target. Confirm borderline cases in the full-profile fetch below.

**School needs a deeper read — do not take it from the search snippet.** On LinkedIn the `## Education` section sits at the *bottom* of the profile, below the About and Experience blocks (Exa also injects a long stats blurb per company), so it's routinely **thousands of characters down** — often past 3,000 and sometimes past 12,000. A short search snippet almost never reaches it, and `autofill` will **not** fill it in later (autofill enriches email only — it never sets `school` or `location`). So the search snippet gives you location but not school. Fetch the finalists' full profiles and read `## Education` from there:

```bash
curl -s -X POST "https://api.exa.ai/contents" \
  -H "Authorization: Bearer $MOLLY_EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["LINKEDIN_URL_1", "LINKEDIN_URL_2"], "text": {"maxCharacters": 20000}}'
```

Pass all finalist URLs in one call, with `maxCharacters` high enough (~20,000) to reach Education. For each, find the `## Education` heading and take the most recent / most notable institution as **school**: it's the school on the first `### …` line beneath that heading — the name after ` at `, or the linked `### [School]` itself. Ignore lookalike headings such as `## Educational Activities`. Only leave `school` blank if the profile genuinely lists no education at all. Backfill `location` here too for anyone missing it from the search snippet.

### 6. Submit each candidate to the role's GEM project

For each candidate, create it in GEM and attach it to the role's project. Always pass `location` and `school` (top-level string fields) alongside the core fields so they're populated immediately — fields you pass explicitly are the only ones present on the create response. Pass `linked_in_handle` (GEM dedupes on it) and `autofill: true` so GEM enriches **email** from the handle.

**`autofill` email enrichment is asynchronous.** The create response — and the candidate for the next few minutes — comes back with `emails: []`; GEM backfills the email out of band, typically within ~5 minutes. Don't judge email coverage from the create response: confirm it in step 7 after a short wait.

```bash
curl -s -X POST "https://api.gem.com/v0/candidates" \
  -H "X-API-Key: $MOLLY_GEM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "created_by": "GEM_USER_ID",
    "project_ids": ["GEM_PROJECT_ID"],
    "first_name": "FIRST",
    "last_name": "LAST",
    "title": "TITLE",
    "company": "COMPANY",
    "location": "LOCATION",
    "school": "SCHOOL",
    "linked_in_handle": "HANDLE",
    "profile_urls": ["LINKEDIN_URL"],
    "autofill": true
  }'
```

Submit sequentially (GEM allows 20 req/s — well within limits). A successful create returns `201` with the new candidate `id` — **collect these IDs**; you'll re-fetch them in step 7 to confirm email enrichment. A handle already in GEM returns `400` with `errors.duplicate_candidate` — count those as *already in GEM* (a dedupe hit, not a failure). Track created vs. already-existing for the digest.

### 7. Confirm email enrichment before reporting

Because `autofill` enriches email asynchronously, the candidates you just created start with `emails: []` and fill in over the next few minutes. Confirm coverage before reporting so the digest reflects reality (and the team doesn't see empty emails right after a run):

1. Wait ~60s after the last create, then re-fetch each candidate created this run by `id`:

```bash
curl -s "https://api.gem.com/v0/candidates/CANDIDATE_ID" \
  -H "X-API-Key: $MOLLY_GEM_API_KEY" \
  -H "Content-Type: application/json"
```

2. Poll every ~60s — re-fetching only the candidates still missing `emails` — until coverage stops climbing or **~6 minutes** have elapsed (enrichment usually finishes within ~5 minutes).
3. Tally how many of the run's candidates have at least one `emails` entry; report that coverage in the digest. Any still missing after the timeout typically fill in shortly afterward — note the count, don't re-create them (re-creating returns a `400` duplicate).

### 8. Post the daily digest to the sourcing channel

After all roles are processed, post **one** message to `SOURCING_SLACK_CHANNEL_ID` (channel root, not a thread). Summarize each role and attach a **View candidates** button that links to that role's GEM project (`https://www.gem.com/projects/<GEM Project ID>`). For each role, add a short summary of the talent team's GEM notes you folded into the Profile Spec this run (the synthesis from step 3) — one or two lines on what feedback shaped today's search, so the team sees their notes reflected back; if there were no new notes, say so briefly ("No new team feedback this cycle"). List any roles skipped for a missing GEM Project ID — they have no project, so they get no button. Close with a reminder asking the talent team to leave feedback as GEM notes within the feedback window (`MOLLY_FEEDBACK_WINDOW_HOURS`, default 24h), before the next run — that's exactly the feedback Molly reads back in step 3 tomorrow.

```json
[
  {"type": "header", "text": {"type": "plain_text", "text": "🔎 Daily Sourcing — YYYY-MM-DD"}},
  {"type": "section", "text": {"type": "mrkdwn", "text": "*ROLE_NAME* · <SPEC_URL|Profile Spec>\nN_SUBMITTED candidates submitted to GEM · EMAILS_FOUND/N_SUBMITTED with an email\n📝 *Folded in team feedback:* FEEDBACK_SUMMARY"}, "accessory": {"type": "button", "text": {"type": "plain_text", "text": "View candidates"}, "url": "https://www.gem.com/projects/GEM_PROJECT_ID", "action_id": "view_gem_project_1"}},
  {"type": "divider"},
  {"type": "section", "text": {"type": "mrkdwn", "text": "*ROLE_NAME_2* · <SPEC_URL|Profile Spec>\nN_SUBMITTED candidates submitted to GEM · EMAILS_FOUND/N_SUBMITTED with an email\n📝 *Folded in team feedback:* FEEDBACK_SUMMARY_2"}, "accessory": {"type": "button", "text": {"type": "plain_text", "text": "View candidates"}, "url": "https://www.gem.com/projects/GEM_PROJECT_ID_2", "action_id": "view_gem_project_2"}},
  {"type": "divider"},
  {"type": "section", "text": {"type": "mrkdwn", "text": "💬 *Help shape tomorrow's search:* leave feedback on any candidate by adding a *note* in GEM — a quick 👍/👎 and one line on why. Molly reads these notes at the start of the next run, so add them within the next *24 hours*, before the next sourcing run."}},
  {"type": "context", "elements": [{"type": "mrkdwn", "text": "Sourced via Exa · deduped by GEM. Roles missing a GEM Project ID were skipped."}]}
]
```

```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $MOLLY_SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  --data @- <<EOF
{"channel": "$SOURCING_SLACK_CHANNEL_ID", "blocks": [...]}
EOF
```

## Notes

- **Dedup is GEM's job** — always send `linked_in_handle`. Re-creating an existing handle returns `400 duplicate_candidate`; treat that as *already in GEM*, not an error.
- **Minimum current-company tenure (`MOLLY_MIN_TENURE_MONTHS`, default 6 months)** — never submit a candidate below the threshold (they rarely move; sourcing them wastes the team's time). Screen this in step 5 from the current role's start date and over-fetch so exclusions still leave a full daily target. Global rule (`AGENTS.md`) — it applies to kick-off and calibration picks too.
- **Missing GEM Project ID** → skip the role and call it out in the digest so the team can fix the tracker.
- **"View candidates" button** → each role's digest section gets a Slack URL button (`accessory`) linking to its GEM project at `https://www.gem.com/projects/<GEM Project ID>`. It's a link-only button, so there's no interaction to handle; give each one a unique `action_id` (e.g. `view_gem_project_<n>`). Skipped roles have no project, so omit the button for them.
- **Always populate `location` and `school`** — pass both explicitly in the create payload (step 6). `location` comes from the search snippet; **`school` comes from the full-profile `/contents` fetch in step 5** (the `## Education` section), *not* the search snippet — Education sits at the bottom of the profile, thousands of characters down, so a short snippet misses it (location survives because it's near the top). `autofill` never fills `school` or `location` (it enriches email only), so never rely on it for these.
- **Email is enriched asynchronously** — `autofill` is the only path to it, and it lands a few minutes *after* create (the create response always shows `emails: []`). Never read email coverage from the create response; verify it in step 7 after a wait. This async lag — not the `location`/`school` change — is why emails look blank immediately after a run.
- Optionally add `sourced_from` or a custom field to tag candidates as Molly-sourced, if your GEM team has the matching source / custom field configured.
- **Feedback comes first** — every run starts by reading the team's GEM notes on the previous cycle's candidates and folding them into the spec (step 3). This is the daily, post-calibration steering mechanism; treat a thumbs-down as a real signal, but generalize across notes rather than over-fitting to one comment.
- **Each note counts once** — read notes with `created_after` set to the timestamp of the latest `## Sourcing Feedback Log` entry, and append a freshly stamped entry every run (even "No new feedback this cycle"). That log is the durable watermark that survives each run starting with no memory of the last, so feedback is never applied twice.
- **Always remind the team to leave feedback** — the digest must close with the feedback-window reminder (step 8). The loop only works if the team knows to drop notes in GEM before the next run.
- **Show the team their feedback landed** — the digest also surfaces, per role, a short summary of the GEM notes Molly folded into the spec that run (step 8), taken from the same synthesis logged in the Sourcing Feedback Log (step 3). Closing the loop visibly — "here's what your notes changed" — is what earns the next round of notes.
