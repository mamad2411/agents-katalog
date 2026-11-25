---
name: jobwatch
description: Run a job search from your agent with the jobwatch MCP server. It watches company job boards (Greenhouse, Lever, Ashby, Workday and more), ranks the new roles into a daily digest, queues the ones to apply to, tracks every application through to an offer, and builds interview prep from what you sent. Use when the user wants to find jobs at companies they name, see what's new, decide what to apply to, record an application or its status, read recruiter or status emails, or get ready for an interview.
---

# jobwatch

jobwatch is an open-source job-board watcher and application tracker (MIT, on PyPI). Its MCP server keeps a
watchlist of companies, checks their boards, and remembers every job, application and status in a local file
on the user's computer. Nothing is sent anywhere except the job boards it reads.

## Setup (once)

The jobwatch plugin from the `vinayvobbili/jobwatch` marketplace starts the server for you in Claude Code (the
Claude app's Code tab too) and Cowork. The jobwatch plugin in the Claude directory is this skill alone: there,
the server is added once (below). A
chat whose plugins run in the cloud has this skill but not the tools, because jobwatch's data is on the
person's computer: say so, and suggest the Code tab, or the jobwatch desktop extension (a `.mcpb` file on
github.com/vinayvobbili/jobwatch/releases) in a Claude Desktop with Settings → Extensions.

In Claude Code or Cowork with no `jobwatch` tools, the usual reason is that uv isn't installed: the plugin
starts the server with `uvx`. Check with `uvx --version`. If it's missing, say that jobwatch needs uv, a
small tool from astral.sh, and offer to install it: `curl -LsSf https://astral.sh/uv/install.sh | sh` on a
Mac or Linux (or `brew install uv`), `powershell -ExecutionPolicy ByPass -c "irm
https://astral.sh/uv/install.ps1 | iex"` on Windows. Run it only once the person says yes; then they restart
Claude so the plugin starts the server. With the skill alone (no server in the plugin), offer to add the server
once uv is there, and run it once the person says yes, then they restart Claude:

```
claude mcp add jobwatch -s user -e JOBWATCH_CONFIG=~/.config/jobwatch/config.yaml -- uvx --from jobwatch jobwatch-mcp
```

If the `jobwatch` tools still aren't available, set it up by hand:

```
pipx install 'jobwatch[mcp]'      # or: pip install 'jobwatch[mcp]'
jobwatch init                     # writes an example watchlist, jobwatch.yaml
claude mcp add jobwatch -s user -e JOBWATCH_CONFIG=~/jobwatch.yaml -- jobwatch-mcp
```

Other agents take the same command (`jobwatch-mcp`) with `JOBWATCH_CONFIG` pointing at the watchlist. Without
installing first: `uvx --with 'mcp>=2.2' jobwatch mcp`.

A new user has no watchlist yet: ask which companies they'd like to watch and what roles and places they're
after, then `find_board` and `add_board` for each company, which creates the file.

## The daily loop

1. **Build the watchlist.** For each company the user names, call `find_board` (a name, a job link or a
   careers page), then `add_board` with the entry it found. `list_suggested_boards` names companies whose jobs
   keep arriving while their board isn't watched.
2. **Check for new jobs.** `fetch_jobs` reads every board. If the user gets job-alert emails (LinkedIn,
   Indeed, Built In), fetch them with a mail connector and pass them to `import_job_alerts`. A LinkedIn or
   Indeed job list the user has open in Chrome ("Jobs based on your preferences", "Jobs for you", a search)
   goes to `import_job_list`: run the extractor (`jobwatch import-list --script`) on the tab with the browser's
   JavaScript tool, then pass its records; it reports how many jobwatch already had and tracks the rest.
3. **Show what's new.** `get_digest` ranks the new matches. Show the top few, not the whole list, each with
   why it fits and anything to check first (pay, location).
4. **Queue and apply.** `mark_job` with `queued` for the ones the user picks; `list_queued_jobs` lists them
   with people the user knows there (a referral is worth asking for before applying). `get_job` gives a
   posting's full text for tailoring a resume. With resume-kit installed, `tailor_resume` builds a resume for
   one job and keeps it with the application (the browser extension attaches it); the user reviews the PDF
   before applying.
5. **Record what happened.** After the user submits, `mark_job` with `applied`, and
   `save_application_package` with the resume and answers they sent. Later stages are `screening`,
   `interviewing`, `offer`, `rejected` (they said no) and `withdrawn` (the user ended it, or it went quiet) and `closed` (the company took the posting down:
   "Closed by company").

## Status emails

Search the user's mail for their applications' companies and phrases like "thank you for applying" or
"interview", and pass the messages to `read_status_emails`. It only proposes changes: show the proposals and
call `mark_job` only for the ones the user confirms.

## Before an interview

`get_interview_prep` puts the posting, the resume and what was sent on one sheet, with `story_gaps`: questions
a story from the user's own past would answer. Ask the user about one, and keep what they confirm with
`save_story`. `ranked=true` adds ranked questions: likely questions, most likely first, each technical,
behavioral or why-us, from the posting alone; use them to seed practice. `get_application_package` reads back
exactly what was sent.

## Other tools

- `list_applications`: where every application stands, with follow-ups due and ones gone quiet.
- `draft_followup`: a follow-up email for an application (about a week after it was sent), or with `thanks` a
  thank-you after an interview, written from the tracker by the local model. It only drafts: read the warnings,
  show the email, and leave sending it to the user.
- `get_company`: everything tracked at one company, closed postings too.
- `get_comps`: the live opportunities (or any jobs and companies you name) side by side, with a rule-based
  suggestion; explain its reasons and say what is missing. `set_comp` keeps what a recruiter said about pay
  (base, bonus, equity, asked, offered) as the user tells you, and the job's `role` (`product` builds the company's
  own product, `customer` is forward-deployed or customer-facing, `internal` builds internal tools) with a
  career note (with the company's kind, they set the suggestion's career part, scored against the user's
  `goals:` preferences when the watchlist has them, else the fixed rules). `set_company_health` keeps a
  company's funding, layoffs and rating that you looked up on the web (jobwatch fetches none of it): record the
  source links and the day, and leave out what you couldn't find. It also takes the company's `kind` (`tech`,
  `consulting`, or `enterprise`: a non-tech business whose IT builds for itself). Health older than 90 days is stale: look it up again.
- `find_past_answers`: what the user answered before to a form question ("notice period", "reason for
  leaving"), newest first: reuse it before writing a new answer.
- `rate_contact`: record whom the user wants asked for a referral first (`use`) or never (`skip`, e.g. someone
  who doesn't check messages), with a short note; `clear` undoes it. Call it when the user says so about a
  person in a "you know" list.
- `read_profile`: the roles on a LinkedIn experience page, from page text the user copied or you got from their
  browser (never a link: jobwatch doesn't fetch linkedin.com). Use it for who an interviewer is.
- `check_postings`: whether queued jobs and open applications are still posted.
- `list_jobs`: jobs by status. `find_duplicates`: the same opening tracked twice.
- `add_application`: an application found elsewhere, from its link or pasted text.
- `list_skill_gaps`: what the matching jobs ask for that the resume doesn't show, with courses to close it.
- `list_boards`, `remove_board`, `dismiss_suggested_board`: manage the watchlist.

## Rules

- **Never apply for the user.** Fill in what you can, then stop for them to review and submit. Use `applied`
  only after they say they submitted.
- **Check for duplicates first.** Before a referral request or an application, check `get_job`'s
  `duplicate_of` and the warnings in `list_queued_jobs`: a strong match means it was already applied to.
- **Only confirmed facts.** Don't put anything on a resume, form or saved story that the user hasn't confirmed.
- **Keep it private.** The tracker holds pay, notes and recruiter names: don't paste them anywhere public.
