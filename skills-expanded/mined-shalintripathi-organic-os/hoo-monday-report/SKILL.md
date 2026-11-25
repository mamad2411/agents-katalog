---
name: hoo-monday-report
description: Use for a stakeholder-shareable weekly summary - "Monday report", "what happened this week", /organic-os:monday-report. Reads the brain only, invents no numbers, degrades to a shorter honest report on a sparse brain.
---

# Monday report

Resolve the brain: use registry.get_active() when running interactively;
scheduled runs receive the brain path from the routine configuration.

0. Run `core.contracts.check_schema(brain_path)` first. If not compatible,
   relay the action string and stop before any of the steps below.

1. Read the last 7 days only: `signals/YYYY-MM-DD.md` files in the window,
   `outcomes/` records touched in the window, `approvals/queue.md` as it
   stands today, `runs/` report folders created in the window, and any
   `skillbook.md` entries whose `last-confirmed` date falls in the window
   (cross-reference `reflections/` for the week to see which entries were
   added vs. just touched).
2. Write `runs/YYYYMMDD-monday-report/REPORT.md` with exactly these five
   sections, in this order, and no others:
   - **What moved** - the top 3 metric changes this week. Each line names
     the number and the file it came from (a signal line or an outcome
     record). When the week's signals carry `ai_referrals` lines, add one
     line for AI referrals - the week's total and the direction against
     the prior week (the AI-surface list is maintained in hoo-daily's
     SKILL.md); no `ai_referrals` lines in the window means no AI line,
     never an invented one. When the window's weekly run appended
     keyword-portfolio rows to `keywords/history.tsv`, add one line for
     the biggest mover - the keyword, position now vs the prior recorded
     week, labeled honestly as GSC average position, not scraped SERP
     rank (the rule lives in hoo-weekly's Keyword portfolio section); no
     new history rows in the window means no keyword line, never an
     invented one. When
     `~/.config/organic-os/cost-ledger-YYYYMM.tsv` exists,
     close the section with one cost line - runs this week, total
     duration, tokens where the ledger has them; no ledger means no cost
     line, never an invented number.
   - **What shipped** - proposals that reached `applied` and briefs that
     reached `published` this week, each with the item id and a link to
     its file in the brain.
   - **What needs you** - every item currently `proposed` in
     `approvals/queue.md`, one line each: what it is and what deciding it
     takes (a yes/no, not "please review").
   - **What we learned** - skillbook entries appended or edited this week,
     restated in plain language, no evidence-tier jargon, each with its
     source item.
   - **Next week** - the 2-3 highest-leverage `proposed` or `approved`
     items still queued, ranked by the expected impact stated in their own
     source signal or finding.
3. Every number and claim must trace to one specific file in the brain.
   Never invent a metric, a trend, or a "likely cause" the brain does not
   already state. If a section has nothing to report, say so in one line
   instead of omitting the section or padding it.
4. Write for a reader with no SEO background: plain nouns and verbs, no
   unexplained acronyms, no jargon. Keep the whole report under 400 words.
5. Sparse week (few or no signals, outcomes, or shipped items): the report
   gets shorter, not padded - state plainly what did not happen ("no
   proposals shipped this week; two are still waiting on your review").
6. Deliver the report as a document through the configured approval
   channel. Document delivery is a channel capability, not a Telegram
   feature (ADR-0009 in the repo): each adapter declares whether it can
   carry a file, and a channel that cannot reports the file path instead.
   The markdown REPORT.md stays in `runs/` as the canonical record either
   way - the document is a delivery format, never the source of truth.
   a. Render HTML next to the markdown:
      `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -c` snippet calling
      `core.report_render.render_html(markdown_text, title, site_name)`
      (title "Monday report YYYY-MM-DD", site_name from the profile) and
      writing `runs/YYYYMMDD-monday-report/REPORT.html`.
   b. Probe for a PDF converter with `core.report_render.find_pdf_converter()`
      (the probe list is canonical in `report_render.py`). If one is
      found, `core.report_render.to_pdf(html_path, converter)`; a None
      return means fall back to the HTML file, no error.
   c. Compose a two-line caption from the report itself: line 1 the week
      ("Monday report, week of YYYY-MM-DD - <site name>"), line 2 the
      single strongest What-moved line plus the count of items waiting
      ("3 waiting on you" / "nothing waiting"). No invented numbers here
      either - both lines quote the report.
   d. Send per channel: telegram - `core.telegram.send_document(token,
      chat_id, path, caption=...)` with the PDF if produced, else the
      HTML. in-session - save the file where step 2 wrote it and tell
      the user the exact path (attach it if the session surface can).
      slack/email - the adapter sends the file where the connector
      supports attachments; where it does not, deliver the caption plus
      the file path. pr-merge - the report is already in the brain repo;
      the caption plus the file path is the message.
   e. A failed send never fails the run: note it in one line at the end
      of REPORT.md and continue.
7. Commit "monday-report: YYYY-MM-DD" if git.
