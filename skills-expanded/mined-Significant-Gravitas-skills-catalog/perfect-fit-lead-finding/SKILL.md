---
name: "perfect-fit-lead-finding"
description: "Use when the user wants new leads, clients or customers found for them, however broadly they ask. Turns what they sell into a narrow profile of buyers who need it now and can pay for it, then finds and checks each one with Firecrawl's live data tools: maps and reviews, company registers, site history and email finders."
triggers: ["find me leads", "find leads", "find me clients", "find new clients", "find customers", "get more customers", "prospects near me", "local businesses that need", "lead list"]
version: "1"
---

# Find perfect-fit leads

People ask for "leads" and mean "people who will buy". A long list of
loose matches wastes their week. Your job is a short list of businesses
that need what they sell right now and can afford it. Do the narrowing
yourself. Never wait for them to tell you to be selective, or which tools
to use.

Every run starts and ends with the lead sheet (section 6). Find it before
you search, so nothing already on it comes back.

## 1. Turn what they sell into a buyer profile

Work from what they sell, what it costs, and where they work: memory,
their own website, and this chat. Write the profile in five parts.

- **Need.** The visible sign that a business needs it. Someone selling
  websites looks for no website, only a Facebook page, or a site that is
  old, broken or not mobile friendly.
- **Means.** Public signs they can pay the price. For about £1,000: a
  good rating with steady recent reviews, several staff named in reviews,
  a real premises, a trade with decent-value jobs.
- **Moment.** What makes now the time: opened or changed owner in the
  last year, a second site, hiring, a move, a rebrand, reviews arriving
  fast, a new contract or tender.
- **Out.** Who never fits: chains and franchises run from a head office,
  firms big enough to have their own team for it, closed or dormant
  businesses.
- **Who decides,** usually the owner or manager, and the area.

A renovation firm looking for repeat work would get: need, manages
many rental homes; means, a steady flow of small repair jobs; moment,
reviews complaining that repairs drag on; out, national chains with their
own trades; decides, the agency manager.

Show the profile in a few lines with your assumptions marked, and start
the first batch in the same turn. Ask one question at most, and only when
you can't tell what they sell or where.

## 2. Find the right data tools

Run **Firecrawl Find Data Tools** with a plain-words query for each job,
in the user's country. It is free and searches thousands of data tools.
Then run the tool with **Firecrawl Run Data Tool**. Before a tool's first
run, read its options (find it again with its provider and capability and
expand "options") and pass them exactly. If a call comes back empty or
with an error, read the options again and retry once with corrected
inputs before you give up on that tool. Good starting points:

- **Places.** `firecrawl-maps`, `businesses/search`: a query like
  "electrician in Whitby" and the two-letter country code. Each page has
  20 places with rating, review count, phone and the website on the
  listing. `businesses/reviews` with the `feature_id` and newest first
  gives recent reviews.
- **Company registers.** UK: `find-and-update-company-information-service-gov-uk`.
  Its `companies/advanced_search` takes a SIC code, a registered-office
  town and an incorporation date range, which finds new businesses.
  `companies/officers` gives the directors. France:
  `recherche-entreprises-api-gouv-fr` (`companies/search_companies`,
  `companies/search_near_point`, `companies/get_company` with the
  executives). Elsewhere, search "company register" and the country.
- **Site history.** `web-archive-org`, `captures/history`, to see how
  long a site has gone unchanged.
- **Work emails.** `hunter` or `orbisearch`, `people/email-find`, with
  the person's name and the company domain.
- **Hiring.** Search for job postings in the country when hiring is a
  moment signal.

## 3. Screen cheaply, check deeply

A search costs a few Firecrawl credits, about a cent. The cost is in the
checking, so check only what survives the screen.

1. Search wide: one places query per trade per town, plus register
   searches for new businesses. When they give a radius, search the main
   town and the towns inside it. Cover enough ground to find ten that
   pass: several trades that fit the profile, and nearby towns when one
   runs dry. That is usually 10 to 30 searches, so don't stop at five.
2. Screen on the fields you already have. Towns share names across
   countries, so check each address is in the right one. Drop chains and
   anything that fails need or means. A blank website on a map listing
   is not proof: search the business name and town on the web before
   you call it site-less.
3. Check the survivors: recent reviews, the register, site history, and
   their own website and social pages. Read their contact and about
   pages with **Firecrawl Scrape**: a small business's own published
   email and the owner's name are usually there, at no data cost. Use
   an email finder only for a named person's work email at a domain.
4. Confirm every fact on a page you can link before it goes in. Match
   register entries by address, not by name alone. Sole traders are not
   on company registers, so take the owner's name from their own site or
   page.

A good weekly batch is a few hundred credits. Before a run over a big
territory, or more than about 50 paid calls, say the count and the cost
and wait for a yes.

## 4. Rank and cut

A lead must pass need, means and out, and you must know who decides.
Moment signals rank it up. So does public proof of the pain, such as
reviews saying customers couldn't find prices or get through. Hand back at
most 10 per batch, best first. Three excellent leads beat ten average
ones: if only three pass, give three and name the one rule you would
loosen to get more. When the user asks for a number or a full list, give
them that many, still screened and ranked, with each marked Strong or
Possible, rather than cutting it to ten.

## 5. What you hand back

For each lead: the business and its link, one sentence on why it fits
now with the links behind it, the decision maker's name and role, every
published way to reach them (email, phone, WhatsApp, Facebook,
Instagram), and a short, friendly first message for approval. The message
names one specific, fixable thing about their situation. Never quote
their customer reviews in it.

Put the batch in the lead sheet and link it. Then offer the weekly
routine, "Perfect-fit leads every Monday", which runs this skill in a
fresh chat each week and drafts one follow-up for anyone contacted a week
earlier who hasn't replied. It needs their yes to use their connected
accounts, because it reads and writes the sheet and runs the data tools.
Switch it on with `tool:schedule_routine` and `grants_credentials=true`,
and add the sheet's saved spreadsheet object to its prompt.

## 6. The lead sheet

The user never has to make, name or point you to it. Use the same sheet
in every chat, including scheduled runs.

**Find it.** In order: the routine prompt, if it carries the sheet; your
memory; then `list_workspace_files` with `include_all_sessions=true` and
`limit=100` for `lead-tracker.json`. Make a new sheet only when all three
come up empty; if you find a URL but no spreadsheet object, ask the user
to pick the sheet once rather than make a second one. If the user already keeps leads in their own sheet
or CRM, use theirs instead: read back its columns and map them once.

**If there is none, make it on the first run**, without asking:

1. **Google Sheets Create Spreadsheet**, titled "Lead tracker" plus their
   business name, with one sheet named "Leads". If Google isn't connected,
   the card asks once. Carry on with the batch meanwhile and fill the
   sheet when it connects.
2. **Google Sheets Write** the header to `Leads!A1:P1`, in this order,
   which every later run relies on: Found on, Business, Town, Fit, Why
   now, Decision maker, Email, Phone, Other contacts, Website, Evidence,
   First message, Status, Contacted on, Follow up on, Notes.
3. **Google Sheets Format** `Leads!A1:P1`: bold, text colour red 1,
   green 1, blue 1, background red 0.13, green 0.2, blue 0.33.
4. **Google Sheets Set Layout** on "Leads": freeze 1 row and 2 columns;
   column widths 95, 200, 110, 80, 320, 160, 210, 130, 200, 180, 220, 360,
   120, 110, 110, 240; wrap `A2:P1000`; filter and alternating colours on
   `A1:P1000`. If that block isn't available, skip this step.
5. **Google Sheets Add Dropdown** on sheet "Leads", range `M2:M1000`, with New, Contacted,
   Replied, Meeting booked, Won, Not interested, No reply.
6. Save `lead-tracker.json` with `write_workspace_file`: the spreadsheet
   object the create step returned (pass it through unchanged: it carries
   the hidden credential that later runs need), its URL, the column order
   and the buyer profile. Save the same spreadsheet object, name and URL
   to memory too.

**Every run:** read `Leads!A:P` first. Skip any business already there,
matched by name and town, phone or website. Respect each status, and list
the follow-ups that are due. Then add each new lead with **Google Sheets
Append Row** on sheet "Leads", one row per lead in the column order, with
Status "New" and Found on today. Never write new leads to a range you
worked out yourself: one row off overwrites a lead. Write links as
`=HYPERLINK("url","label")`, with the bare domain as the label in the
Website column so later runs can match it. Dates are YYYY-MM-DD.

Writes to the sheet may ask the user to approve them. When an Append Row
approval comes up, say once that allowing it in every chat with you lets
the Monday run add rows on its own.

## Boundaries

Nothing is sent without the user's yes. Contacts are found, never made:
no email built from a naming pattern, and a field you can't source stays
empty. Public business data only: no personal home addresses and nothing
behind a login.
