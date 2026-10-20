---
name: investor-match
description: Find ranked investors and their contacts for a company using the Caeros Vault matcher (caeros_investor_match). Use when asked to find investors, build a target investor list, match a company to VCs or funds, find who to raise from, or get investor contacts for outreach.
---

# Investor Match

`caeros_investor_match` is the ONE tool that produces ranked investors and their
contacts. It runs the entire production pipeline on the Caeros backend in a
single blocking call and auto-exports the CSV. There is no second tool to call,
nothing to poll, and nothing to assemble yourself.

## What the one call actually does

| Stage | What happens |
|---|---|
| `embedding` | Your `description` + `keywords` + `country` become one Conare embedding vector. This is why description quality decides result quality. |
| `semantic_retrieval` | Two parallel ConareDB searches: the company namespace and the investor namespace. Candidate pool is `top_k` times 50 for companies and times 25 for investors, clamped to between 500 and 5,000. |
| `vault_portfolio` | BigQuery hydrates the candidate graph: investors, portfolio companies, and the links between them. |
| scoring | Vector similarity plus portfolio evidence produces the ranked firm list. |
| `lazy_people` | Contacts are attached from the Vault, then rows are re-scored so contact-aware ranking is final. |

Vectors nominate, the Vault decides. Contacts come only from Vault data, so no
external provider is called and no data credits are spent.

## The procedure, in order

1. **Assemble the brief.** You need `company_name` and `description` at minimum.
   Load the `company-brief` skill for the field contract and the rules on
   gathering missing information. Do not proceed on a one-line description; it
   produces a weak embedding and a weak list.
2. **Confirm the brief with the user** when you filled any gap yourself, and
   confirm the knobs if they asked for anything non-default (geography limits,
   list size, firms to exclude).
3. **Call `caeros_investor_match` exactly once.**
4. **Wait.** The call blocks through all five stages and can take minutes. Call
   NO other tool while waiting. Do not retry, do not start a second match, do
   not "check on it".
5. **Read the response envelope** and report it (see below). The CSV already
   exists.
6. **Stop.** Delivering the summary plus the CSV link is the whole job.

## Arguments

Required:

| Field | Notes |
|---|---|
| `company_name` | The company being matched, not the investor. |
| `description` | What the company does. Drives the embedding. See `company-brief`. |

Worth passing whenever known:

| Field | Notes |
|---|---|
| `website` | The company's own domain. Also joins it to the Vault graph if it is already known there. |
| `keywords` | Comma-separated sector and technology terms. Joined into the embedding text. |
| `country` | Company geography. Joined into the embedding text. |
| `cap_table_domains` | Domains of investors already on the cap table. They get pinned as existing investors rather than presented as fresh targets. |

Filters, only when the user asked:

| Field | Default | Notes |
|---|---|---|
| `top_k` | 100 | Firms to return. At the default the company candidate pool is already at its 5,000 ceiling, so raising `top_k` returns more of the same pool rather than searching deeper. Lower it for a tighter list. |
| `min_score` | 0.20 | Minimum final score to include. Raise it for a shorter, higher-conviction list. |
| `exclude_countries` | none | Geographies to drop. |
| `exclude_investors` | none | Firms or domains to drop. |
| `preferred_contact_locs` | none | Preferred contact cities or countries. |
| `preferred_contacts_only` | false | Return ONLY contacts in those locations. Use with care: it can empty out otherwise good firms. |

Scoring weights (`w_portfolio` 0.45, `w_profile` 0.20, `w_collab` 0.35,
`collab_threshold` 0.20): **leave these alone** unless the user explicitly asks
to reweight. They are calibrated against the current embedding model. Changing
one silently changes what "score 0.6" means, and results stop being comparable
to any earlier run.

## Reading the response

The tool returns one envelope. The fields that matter:

- `status`, and `error` / `message` if it failed.
- `n_firms`, `n_contacts`, `n_results` (result rows), `top_score`.
- `n_existing` (firms already on the cap table), `n_warm_thesis`,
  `n_warm_relationship` (warm-intro paths found).
- `csv_path`, `csv_download_url`, `artifact_id`, `expires_at`.
- `top_firms_preview` plus `preview_note`.
- `export_warning` if the CSV did not write.
- `runtime_seconds`, `job_id`.

Report to the user: firm count, contact count, top score, how many were existing
investors or warm paths, and the CSV link. Use `top_firms_preview` for the
in-chat preview. The download URL expires, so mention `expires_at` if the user
is not acting immediately.

## The CSV

Rows are flat and one per contact, with the firm's fields repeated on each of
its contact rows. Columns include:

- Firm: `investor_website`, `firm_name`, `investor_country`, `investor_city`,
  `investor_stage`, `deal_count`, `portfolio_size`, `portfolio_relevance_pct`,
  `is_existing_investor`.
- Scores: `score` (final), `raw_score`, `content_score`, `profile_score`,
  `collab_score`, `focus_score`.
- Evidence: `closest_portfolio_company`, `closest_portfolio_company_name`,
  `closest_portfolio_company_desc`, `closest_similar_investor`, `explanation`.
- Warm intro: `warm_intro_type`, `warm_intro_score`, `warm_intro_investor`,
  `warm_intro_via_deal`, `warm_intro_deal_name`, `warm_intro_deal_match`,
  `warm_intro_note`.
- Contact: `contact_rank`, `contact_name`, `contact_first_name`,
  `contact_last_name`, `contact_title`, `contact_email`, `contact_linkedin`,
  `contact_company_name`, `contact_city`, `contact_country`,
  `sector_contact_name`, `sector_contact_title`.

When the user wants firms rather than contacts, deduplicate on
`investor_website` and keep the best `contact_rank` per firm. Use `explanation`
and `closest_portfolio_company_name` to justify a ranking; they are the reason
the firm scored, not decoration.

## Failure handling

- `status: failed`, or an `error` field: STOP. Report the error as a blocker.
  Hosted matcher outages are internal Caeros service problems, not user setup
  tasks. Never ask the user for backend secrets or service configuration.
- `export_warning`, or a missing `csv_path`: STOP. Report the match counts and
  the warning. Do NOT retry the match and do NOT rebuild the CSV another way.
- Do NOT fall back to the Vault, web search, or model knowledge to produce a
  substitute investor list. A failed match returns nothing rather than something
  invented. If the user wants a Vault-only slice instead, that is a new,
  explicit request: load `investor-vault-queries`.

## Never do this

- Never call the match twice for one request, including "to compare settings",
  unless the user explicitly asks for a second configuration.
- Never call any tool while the match is running.
- Never call `analyst_export_csv` after a match. The CSV is already exported.
- Never re-read, reformat, or re-export the returned CSV. Hand over the link.
- Never call `analyst_vault_query` to "enrich" or "verify" match output. The
  contacts are already Vault rows.
- Never call `caeros_investor_match_start`, `_status`, `_get`, `_list`,
  `caeros_icp_lookalikes`, or any `caeros_matcher_cache_*` tool. These are not
  registered in the live toolkit; calling them wastes a turn and fails.
- Never invent, guess, or pattern-match an email address or LinkedIn URL. If the
  Vault has no contact for a firm, that firm has no contact. Say so.

## Family offices are a different universe

Family offices are NOT in the investor results. They live in their own dataset
with their own search tool. Load `family-office-match` when the user asks for
them.
