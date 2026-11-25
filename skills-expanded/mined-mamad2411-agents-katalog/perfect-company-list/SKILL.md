---
name: perfect-company-list
description: Build a near-complete company list for any ICP by learning how your real customers label themselves, pulling every industry and keyword they use, judging every single row with a cheap AI model (Jev or gpt-5-nano), and running a Claygent lookalike loop until it runs dry. The method from the SCULPT 2026 talk "Build the perfect company list". Use when a database filter feels too narrow or too noisy, when someone says "find every company like our customers", "our TAM looks too small", or "why is this list full of junk".
---

# Perfect company list

Database filters fail in two directions at once.

- **They miss real fits.** Industry labels are self-reported, or guessed: many LinkedIn company
  pages carry the banner "This listing was automatically created by LinkedIn", which means nobody
  at the company picked the label. We found an FDIC bank listed as *Construction*, an SEC-registered
  wealth manager listed as *Semiconductor Manufacturing*, and a New Jersey school district listed
  as *Retail Luxury Goods and Jewelry*.
- **They pull in junk.** A plain `Banking` + `United States` filter returned 16,895 companies. About
  10,500 of them were not banks: 3,679 mortgage companies and lenders, 2,414 credit unions, 2,210
  dead sites or unrelated businesses (a Toyota dealer, a pawn and gun shop, a youth soccer club),
  839 vendors that sell to banks, and the Federal Reserve Bank of St. Louis.

The fix is not a better filter. It is: **use filters to cast a wide net, and use AI to decide who
is in it.** Judging is now cheap enough that pulling five times too many companies costs almost
nothing.

## The workflow

```
1. Learn    your customers  -> the industries and keywords they actually use
2. Pull     every one of those industries + keywords (keep size and geo tight)
3. Judge    every single row with one ICP question
4. Loop     Claygent finds lookalikes of your fits -> dedupe -> same judge -> repeat
5. Stop     when 20 runs in a row add one company or fewer
```

### 1. Learn from your customers

Put your customer list (or dream accounts) through Clay's Enrich Company and record, per customer:

- the LinkedIn industry they self-selected
- keywords in their description and job posts
- headcount and HQ geography (the fields databases get right)

Then tally the industries. In our bank demo, 50 known banks used as the "customer list" came back
43 Banking, 4 Financial Services, 2 blank and 1 **Telecommunications**. You pull all four.

### 2. Pull every industry and keyword

If even one customer shows up under an industry, pull every company in that industry inside your
size and geography band. Add keyword searches over name and description ("bank", "school
district", "wealth management") with no industry filter, which is how blank-industry records get in.

Keep headcount and geography tight. Keep industries wide open. You will pull a lot of junk. That is
the point.

### 3. Judge every row

One question per company, yes or no. Write it so the edge cases are decided in the criteria, not
left to the model:

```text
Question: Is this company a bank or savings institution that takes deposits and would be
          FDIC-insured (commercial bank, community bank, savings bank, thrift, trust bank)?
Yes:      A deposit-taking bank or thrift (FDIC-insured type)
No:       Anything else: credit union, mortgage lender, fintech, broker, wealth manager,
          insurance, payments, consultancy, bank software vendor, bank holding company with
          no bank, association
```

Run it with `scripts/jev_judge.py` (Jev, standard library only):

```bash
TYPESAFE_API_KEY=... python scripts/jev_judge.py pulled.csv judged.csv \
  --question "Is this company a bank or savings institution that takes deposits?" \
  --yes "A deposit-taking bank or thrift" \
  --no  "Anything else: credit union, lender, fintech, vendor, association"
```

It sends 20 companies per request as one shared state with one question per company, which keeps
you under Jev's default 1,200 requests per minute. On a 60-row canary, batched and one-at-a-time
answers agreed on 51 of 54 rows. Canary 50 to 100 rows before you run the whole pull.

Any cheap model works for this step. What it costs to judge 10 million companies at ~350 input
tokens each, minimal reasoning:

| Model | Cost for 10M |
|---|---|
| GPT-6 Luna | $375 to $450 (batch: $188 to $225) |
| gpt-5-nano | $195 to $255 (batch: $98 to $128) |
| Jev | about $147 (output tokens are free) |

Leave reasoning on and output tokens dominate: $1,000 to $3,000 for the same job.

### 4. Loop with Claygent

Take companies you have judged as fits and ask Claygent: "these companies fit our ICP, find more
like these that we might have missed." For each result:

1. Check the domain against everything you have already judged. Skip it if you have seen it.
2. Run anything new through the **same** judge question.
3. New fits become the next seeds.

### 5. Stop when it runs dry

Stop when 20 runs in a row add one company or fewer. In our demos the loop was still adding about
one company per run at 150 runs, so also set a budget cap.

## Checking yourself

When a public registry exists, score against it. Registries are complete lists you can match on:

| Registry | Count (Sept 2026) | Has websites |
|---|---|---|
| FDIC BankFind (active insured banks) | 4,231 | 98% |
| SEC investment adviser roster (US) | 14,863 | 60% list a real website |
| NCES district directory (New Jersey) | 668 districts | yes |

Results from our runs, normal filter = every LinkedIn industry label that fits, industry only:

| List | Normal filter | This process |
|---|---|---|
| FDIC banks | 3,356 (79%) | 3,718 (88%) |
| SEC advisers | 4,636 (31%) | 13,621 (92%)* |
| NJ school districts | 360 (54%) | 532 (80%) |

\* The SEC number counts every firm found anywhere in the data stack, including exact-name matches
in a second database, because 2,729 advisers list no usable website on the SEC roster.

## Gotchas we hit

- **Match on every website a registry lists.** The SEC roster CSV shows only the first URL, which is
  often an Instagram or LinkedIn link. The full IAPD XML feed has all of them; switching added 1,263
  matches that were already in our list.
- **Enrichment providers mis-join.** One provider mapped `mariner.com` to a nursing home's LinkedIn
  page and `tagstonecapital.com` to a nail salon's. Verify any label you plan to quote on the live
  page.
- **Registries go stale too.** Some "missing" companies had a parked domain on the registry but a
  live site elsewhere. Search the name before you call something unfindable.
- **Some entities are not companies.** Separate bank charters of big brands, fund GP shells and tiny
  banks with no website exist in registries and nowhere else. No database will have them.

## Files

| File | What it is |
|---|---|
| `SKILL.md` | this method |
| `clay-workflow.md` | the three Clay workflows (learn, judge, loop) built from the `clay` CLI |
| `scripts/jev_judge.py` | batch judge for a CSV with Jev |

Verification: the method, numbers and gotchas above come from runs on 2026-09-27 against FDIC,
SEC and NCES registries (more than 900,000 company judgments across the demos, about $12 of Jev in total).
`scripts/jev_judge.py` was run on a 40-row sample (40 in / 2 fit). The Clay workflow in
`clay-workflow.md` is a specification: it has not been built and published end to end.

Related: [`list-expander`](../list-expander/) (seed fingerprinting and filter mining),
[`list-builder`](../list-builder/) (multi-source lanes), [`icp-prompt-builder`](../icp-prompt-builder/).
