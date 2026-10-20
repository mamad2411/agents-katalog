---
name: newsletter-build
description: Compile new ArtStroy articles into a Markdown newsletter draft ready for Buttondown. Runs weekly; sends draft to human for final review before dispatch.
---

# Newsletter Build

The newsletter surfaces the week's published articles to subscribers. It is always a draft — a human reviews and sends. The Distribution Manager never dispatches directly.

## When to Run

- Weekly (Friday, as part of the weekly content cycle)
- Only if at least one article was published since the last newsletter
- Triggered by the Distribution Manager on EIC's weekly-review cadence signal

## Step 1 — Collect New Articles

Read the sitemap or scan `src/content/articles/` for articles where `isDraft: false` and `publishedTime` falls within the last 7 days.

For each article, extract:
- `title`
- `description`
- `category`
- `publishedTime`
- Slug (directory name)

If zero articles published this week → skip newsletter build, leave a note on the weekly-review issue: "No new articles this week — newsletter skipped."

## Step 2 — Build the Draft

**Newsletter structure:**

```markdown
# ArtStroy Weekly — {YYYY-MM-DD}

Hi,

{1-sentence intro that calls out the theme or standout article of the week}

---

## New This Week

{For each article:}

### [{title}](https://artstroy.net/{slug}?utm_source=newsletter&utm_medium=email)

*{category} · {publishedTime formatted as "Month DD, YYYY"}*

{description — use frontmatter description verbatim or lightly adapted; 1–2 sentences max}

---

{Repeat for each article}

## Quick Links

- All articles: [artstroy.net](https://artstroy.net?utm_source=newsletter&utm_medium=email)
- Archive: [artstroy.net/archive](https://artstroy.net/archive?utm_source=newsletter&utm_medium=email)

---

*You're receiving this because you subscribed at artstroy.net. [Unsubscribe]({buttondown_unsubscribe_url})*
```

**UTM parameters for all links:**
- `utm_source=newsletter`
- `utm_medium=email`
- No `utm_campaign` unless EIC specifies a campaign name

## Step 3 — Buttondown API Draft Creation

Use `BUTTONDOWN_API_KEY` (declared in `.paperclip.yaml inputs.env`).

```bash
curl -X POST https://api.buttondown.email/v1/emails \
  -H "Authorization: Token ${BUTTONDOWN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "ArtStroy Weekly — {YYYY-MM-DD}",
    "body": "{newsletter markdown body — escaped}",
    "status": "draft"
  }'
```

`"status": "draft"` is mandatory — never `"published"` or `"sent"`. The API call creates a draft in Buttondown's interface for human review.

On success, the API returns an `id` and a preview URL. Record both in the newsletter issue comment.

## Step 4 — Report

Post to the current issue:

```markdown
## Newsletter Draft — Week of {YYYY-MM-DD}

**Articles included**: {count}
{list of titles}

**Buttondown draft**: {preview URL from API response}
**Draft ID**: {id}

Status: 📋 Draft created — awaiting human review before send.

*To send: open the Buttondown draft link, review, and click Send.*
```

## Quality Checks

- [ ] Every article link has UTM parameters
- [ ] `isDraft: false` confirmed for all included articles
- [ ] No article included twice (deduplication against previous newsletter)
- [ ] Subject line includes the date
- [ ] Unsubscribe placeholder present
- [ ] API call used `"status": "draft"` — never dispatched directly

## Invariants

- The newsletter is ALWAYS a draft. Human sends it. No exceptions.
- If `BUTTONDOWN_API_KEY` is not available, output the full Markdown draft as a comment and flag: "API key unavailable — paste this draft manually into Buttondown."
- One newsletter per week maximum. Check the last issue comment for a "Newsletter Draft" marker before building.
