---
name: monthly-close
description: The month gets one honest close - every number written into your company's books with its named source, revenue read as promised vs paid straight from your client book, spend intentions checked against what actually left the account, and one month review on the record. Use when you say "werkforce, month", "close the month", "monthly close", "month-end numbers", "how did the month actually go", "write up this month", "tally the whole month". Run it in the first week of each new month - run-the-day nudges you when a month is sitting unclosed.
---

# Monthly Close - the month, written down honestly, once

Most founders never close a month. The numbers live in five dashboards, the feeling lives in their gut, and by March nobody can say what February actually did. Your workforce fixes this with one ritual: once a month, the real numbers go into `company/metrics.md` - each one with the name of where it came from - and the month gets a short, honest review on the record. Say "werkforce, month" and it happens.

One rule above all the others: your metrics file is a view, never a source. The money lives in your payment dashboard and your bank. The customers live in your client book. This close reads those places - through you, or through files you point me at - and writes down what they say. I never invent a number, I never estimate one to fill a gap, and I never smooth over a mismatch. A true zero beats a flattering guess, every time.

## Personalization

This skill works in YOUR company's voice. Before anything else, I find your HQ -
the `werkforce/` folder in the current folder if one exists, otherwise
`~/werkforce/` - and read `HQ.md` plus `company/profile.md`. If there is no HQ
yet, run **install-your-werkforce** first (or just tell me your company name,
what you sell, and who you sell to, and I will set up the basics now). I never
invent facts, numbers, or results about your business - blanks stay blank until
you give me something real.

**Type lens.** If `os/type.md` exists and names a type other than `business`, I read its vocabulary map and speak this skill's words in that type's words instead - "revenue" becomes "attainment" under `job`, same close mechanics, only the words change. Under `business`, or when `os/type.md` does not exist, nothing here changes.

## What you get

- One new `## YYYY-MM` section appended to `company/metrics.md` - your numbers, each with its named source. This skill is the SOLE writer of that file; nothing else in your workforce touches it, so every number in it went through this close.
- A revenue read from `company/customers/` - what the month promised vs what it actually paid, cross-checked against the revenue number you report.
- A spend read - what the decision log said you intended to spend vs what you tell me actually left the account.
- One dated month-review record in `records/reviews.md` - the month's warnings and lessons summarized, gaps named, nothing hidden.
- One line in `records/worklog.md` - the close, on the record, with a receipt.

## What I need from you

1. An installed HQ with at least a few weeks of real activity - boards, customer files, a decision log with entries.
2. Fifteen minutes and your real numbers: read them to me off your dashboards, or point me at files in your HQ that hold them. What you cannot provide stays blank - that blank is itself information.

## How it works

### Step 1 - Find the month that needs closing

I open `company/metrics.md` and look at the last `## YYYY-MM` section. The month to close is the most recent finished calendar month without one - usually last month. If more than one month is open, we close the oldest first, one month at a time, so each close stays clean. If the file is missing or malformed, I append one dated line to `records/warnings.md` as `- YYYY-MM-DD [monthly-close] finding - action taken`, seed the file with its H1 and comment, and keep moving. A warning is a flag on the play, never a stopped game.

You do not have to remember this ritual. **run-the-day** checks the metrics file every morning and nudges you in one sentence when a finished month is sitting unclosed - the nudge is its job; the close is mine.

### Step 2 - Gather the numbers, each with its named source

Now the interview. I ask for the handful of numbers that matter to your business - revenue collected, new customers, customers lost, active customers, and anything your `company/business-model.md` says you steer by. For every number, two things:

1. **The value.** From your mouth or from a file in your HQ you point me at - a finance-department cash snapshot in its outbox, a customer file, an inbox note you dropped. Never from my imagination.
2. **The source, named in your words.** "from my Stripe dashboard", "from the bank app", "from a count of company/customers/", "from the founder's estimate". If the honest source is an estimate, the line says so - a labeled estimate is honest; an unlabeled one is a lie waiting to age.

Then one cross-check, borrowed from how real finance teams stay honest: continuity. Last month's customer count, plus this month's new, minus this month's lost, should equal this month's count. When it does not, I say so out loud and the mismatch goes in the review record - I never quietly adjust a number to make the arithmetic behave. If you skip a number or a check, the record says unchecked, not passing. Every line I write about what I did carries its claim label: `[checked]` for what I verified in your files this session, `[from memory]` for anything recalled, and nothing dressed up as more certain than it is.

### Step 3 - The revenue read: promised vs paid

I walk every file in `company/customers/` and tally two numbers for the month: what the book says was **promised** and what it says was **paid**, reading the `Promised:` and `Paid:` lines and the dated history entries `[checked]`. Then I hold that against the revenue number you gave me in Step 2:

- Match - good, and the metrics line for revenue can cite both sources.
- Client book shows less than you reported - your book is stale; I list which customers likely need updating (updating them is **customer-book**'s job, not mine).
- Client book shows more than you reported - money may be promised that never landed; those names go in the review record as the month's follow-up list.

The gap between promised and paid is the single most honest number this close produces. It is next month's collections work, written down while it is still small.

### Step 4 - The spend read: intents vs actuals

Spending money is a reserved decision, so intended spend leaves a trail: I scan `company/decision-log.md` for the month's spend-related `DECIDED:` lines and total what the company said yes to. Then I ask you one plain question: what actually left the account this month? Your answer is the actual - I have no window into your bank and I do not pretend to. Intended vs actual goes into the review record, and the actual spend total goes into `company/metrics.md` with its source (`from the founder's report`). A gap in either direction is worth one sentence, not a judgment: unlogged spend means a decision skipped the queue; approved-but-unspent means a decision is still waiting to execute.

### Step 5 - Write the metrics section

Everything lands in `company/metrics.md` as one new section. The file is a LEDGER - I append the section and never edit an earlier month; a correction to an old number is a new bullet in a new close, dated, saying so.

```markdown
## 2026-07
- Revenue collected: $4,200 (from my Stripe dashboard; matches customer book paid total)
- Revenue promised, not yet paid: $1,500 (from a count of company/customers/)
- New customers: 3 (from a count of company/customers/)
- Customers lost: 1 (from the founder's report)
- Active customers: 9 (from a count of company/customers/; continuity check passed)
- Spend: $310 (from the founder's report; decision log intended $350)
```

Only lines with real values appear. A number you could not provide is not written as zero - it is named as a gap in the review record instead.

### Step 6 - The month review record

I read the month's lines in `records/warnings.md` and `records/improvements.md`, count them, and name the patterns - which skill warned most, which lesson repeated, what got fixed. Then one dated record goes into `records/reviews.md` (append-only; this file belongs to the weekly review, this close, and the quarterly review, nobody else):

```markdown
## 2026-08-03 - Monthly close: 2026-07
Numbers: written to company/metrics.md under ## 2026-07 (6 metrics, all sourced).
Revenue: $4,200 paid vs $5,700 promised - follow up: Acme Co, Rivera LLC.
Spend: $310 actual vs $350 intended - one approved decision not yet executed.
Warnings this month: 4 (2 from send-guard - claims needed sources twice).
Lessons this month: 3 lessons, 1 fix, 1 idea - repeat lesson: briefs filed without acceptance checks.
Gaps: no churn number provided; continuity check on customer count passed.
```

I summarize; I do not prescribe. Picking which changes to make is **weekly-review**'s job, and anything strategy-sized waits for **quarterly-strategy**. If a repeating pattern deserves a decision from you, it goes to `company/decision-log.md` as a QUEUED line with a recommendation attached - nothing waits on you silently.

### Step 7 - Log it

I close the loop on the record so the month is never in doubt again. One line to `records/worklog.md`:

```markdown
- 2026-08-03 [company] Monthly close for 2026-07 - receipt: metrics section in company/metrics.md, review record in records/reviews.md, reviewed by {founder}
```

And one line to the master audit log, `records/audit-log.md`, stamped in your HQ timezone (the `Timezone:` line in `HQ.md` governs - never UTC):

```markdown
- 2026-08-03 09:14 [note] [monthly-close] [company] Closed 2026-07: 6 metrics written, revenue read, month reviewed - company/metrics.md
```

You are the reviewer of record - these are your numbers, read back to you before anything was written. Then I give you the month in three sentences: what came in, what is owed, and the one thing the record says to watch.

## Do this now

1. Say "werkforce, month" - I will find the month that needs closing.
2. Have your payment dashboard or bank app open in another window before we start - real numbers, read live, beat remembered ones.
3. Answer the interview honestly, blanks included - then read the new section in `company/metrics.md` and check every source line is one you would defend.

Homework: open `company/metrics.md` after two or three closes and read it top to bottom in one sitting - that page is your company's trend line, and it only exists because you closed the months while they were fresh.

Next: install **quarterly-strategy** - three closed months are exactly what the quarter review reads, and it turns your metrics ledger into the org and strategy conversation this close deliberately stays out of.
