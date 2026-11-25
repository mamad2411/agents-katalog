---
name: company-context
description: >
  Looks up facts in the user's inbox profile (company, offer, rates, affiliate and
  payment terms, tools, contacts) and fills the {{TOKEN}} placeholders the inbox
  skills use. Load before any draft states a price, term or product claim; it never
  invents a value. Also for "what does my profile say about X" or updating a fact.
---

# Company context: the user's facts

The other skills carry **method**. This skill supplies **facts**: when a skill
writes `{{AFFILIATE_RATE_STANDARD}}` or "per `deals.md`", the value comes from the
user's profile, never from memory, never from an earlier email.

## Where the profile lives

Run `inbox profile-dir` once per session. It prints the active folder:

- normal use: `~/.claude/inbox/profile/` (the user's own, private files)
- demo mode (`provider: demo` in settings): the fictional profile `demo_profile` picks

Creator notes live in `~/.claude/inbox/creators/` (demo: `<profile>/creators/`).
Find one with `inbox creator <name|handle|email|code>`.

## Which file answers which token

| File | Holds |
|---|---|
| `me.md` | `OPERATOR_*`, `ESCALATION_CONTACT`, `FINANCE_CONTACT`, tools (`EMAIL_PLATFORM`, `CRM_PLATFORM`, `CHAT_TOOL`, `DOCS_TOOL`, `DATA_AGENT`, `CALL_RECORDER`), `ONBOARDING_FORM_URL`, `TEAM_ROSTER`, working norms |
| `company.md` | `COMPANY*`, `PRODUCT*`, brand assets, `VALUE_PROP`, `CORE_FEATURES`, `CREDIT_UNIT`, `ICP1/2`, `TARGET_NICHES`, `EXCLUDED_NICHES`, `CURRENCY`, `PLAN_*`, `TRIAL_TERMS`, `CREATOR_PROMO_OFFER`, `CREATOR_TRIAL_GRANT`, `COMPETITOR_*`, `DIFFERENTIATORS` |
| `program.md` | how the program runs: `model`, `budget`, `success`, `pricing`, `deal_shape`, `creator_types`, `PROGRAM_PITCH`, `CURRENT_CAMPAIGN`, `CAMPAIGN_CALENDAR`, `CAMPAIGN_BUDGET` (internal only), `CREATORS_PER_CAMPAIGN`. Read through `inbox program`. |
| `deals.md` | `MIN_PIECES_FIRST_DEAL`, `TRACK_GATE_MEDIAN_VIEWS`, `CASH_FLOOR_FIRST_DEAL`, `PAYOUT_VENDOR`, `NET_TERMS`, `PAYMENT_SPEED_CLAIM`, tax (gross/net), procurement (`PO_PROCESS`, `TAX_FORMS`, `SUPPLIER_PORTAL`, `AP_RUN_DAY`), `BOOSTING_TERMS`, `USAGE_RIGHTS_RATES`, `EXCLUSIVITY_RATES`, `CONVERSION_VALUE`, `PAYBACK_WINDOW`, deal process, `CANCELLATION_TERMS`, `SEEDING_POLICY`, `SEEDING_FORM_URL`, giveaway limits |
| `rates.md` | the rate bands: `CPM_BANDS`, `GEO_TIER_1/2/3` and `GEO_VALUE_MULTIPLIERS`, `RATE_FLOOR_SHORTFORM`, `RATE_FLOOR_LONGFORM`, value per 1k views. Read through `inbox rate`, not by hand. |
| `affiliate.md` | every `AFFILIATE_*` token, `PAYOUT_THRESHOLD`, `PAYOUT_CADENCE`. First line `none` = no program: never mention one. |
| `voice.md` | the user's voice (loaded by `comms-style`) |
| `house-rules.md` | optional: decisions the user taught the workflow ("always add the brief link"). Always on when present |
| `settings.md` | provider, house-style switches, run log, link domains, teammates |
| `data-sources.md` | advanced, optional: CRM (`CRM_*`) and warehouse (`WAREHOUSE_*`, `TBL_*`, `COL_*`, `LEAK_*`, `REGIME_*`) |

Tokens by prefix: `CRM_FIELD_*`, `CRM_OBJ_*`, `TBL_*`, `COL_*`, `WAREHOUSE_*`,
`LEAK_*` all resolve from `data-sources.md`. If that file says `none` for them,
the capability that needs them is simply off - work from creator notes instead.

## Rules

1. **Unfilled means unknown.** A value that is `TODO`, blank or missing is not a
   gap to fill with a plausible guess. The calling skill drafts without that claim
   (and flags it ⚠️ in the run report), or asks the creator, or asks the user.
   A wrong commission rate or price in a creator email is worse than no number.
2. **`none` is an answer.** `CRM_PLATFORM: none` means "don't look for a CRM".
   `Program: none` in `affiliate.md` means "we have no affiliate program".
3. **Money facts are quoted exactly as written.** Rates, commissions, payout
   thresholds and terms go into drafts verbatim from the file.
4. **The profile beats everything else.** If the profile and a previous email
   (even one the user sent) disagree, the profile wins and the discrepancy is
   flagged in the report. Terms change; old wording lingers in sent mail.
5. **Updating facts.** When the user says "our affiliate rate is now 25%" or "add
   this to my profile", edit the right file in their profile folder (never the
   plugin's templates, never the demo profile) and confirm what changed.
6. **Never copy profile contents anywhere public.** The profile holds commercial
   terms. It stays on the user's machine.

## First-time setup

If `inbox profile-dir` shows a folder full of `TODO`s, hand over to the
`inbox-setup` skill ("set up my inbox profile"). It interviews the user, reads
their website to pre-fill `company.md`, and writes the files with them.
