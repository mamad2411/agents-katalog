---
name: leadgen-romania
description: Romanian company data through the Leadgen MCP server (official ONRC registry of 4.2M firms, ANAF fiscal status, 2008–2025 financial statements). Use when the user wants to find, check, list, match or monitor Romanian companies, for example a lead list by CAEN activity and county, a check of a firm or CUI before a deal, matching a client list or CSV to registry records, who is behind a .ro domain, or alerts on new firms in a niche. Also when the user mentions ONRC, Registrul Comerțului, CUI, CAEN, ANAF or "firme din România".
---

# Leadgen: Romanian company data

Leadgen serves Romania's official business registry to agents: every firm registered with ONRC
(4.2M, 2.2M of them struck off), ANAF's fiscal layer (VAT, e-Factura, fiscal inactivity, phone)
and the Ministry of Finance filings 2008–2025. This skill says which tool to call for which job
and how to present what comes back.

## Connect

The tools come from a remote MCP server. If no `lookup_business` tool is available, help the
user add it:

- Endpoint (Streamable HTTP, no OAuth): `https://leadgen-mcp.adrianhomelab.com/mcp`
- Claude Code: `claude mcp add --transport http leadgen https://leadgen-mcp.adrianhomelab.com/mcp --header "Authorization: Bearer <key>"`
- claude.ai / Claude Desktop: Settings → Connectors → Add custom connector → the URL above.
- Without a key: 30 lookups a day on this MCP endpoint (5 on the REST API). With a free key
  (email only, no card) from https://leadgen.adrianhomelab.com/start: 50 a day. Paid plans: Pro €9/month (500/day),
  Business €29/month (5,000/day). Send the key as `Authorization: Bearer <key>` or `X-API-Key`.

Never ask the user to paste their key into the chat. It belongs in the connector configuration.

## Pick the tool

| The user wants | Call |
|---|---|
| One firm by name or CUI | `lookup_business` (start here for any named firm) |
| Many firms by CUI (up to 100) | `lookup_companies` |
| Their own list (names, counties, domains, CUIs) matched to the registry | `match_companies` (up to 500 rows) |
| "Firms that do X in county Y" | `lookup_by_category` |
| The firm behind a website | `find_company_by_domain` |
| Firms a person runs | `lookup_director` |
| Emails/phones from a firm's site | `enrich_company` (registry + site in one call) or `extract_contacts` |
| Revenue, profit, headcount over the years | `lookup_financials` |
| Trend, margins, health score, peer percentile | `lookup_financial_ratios` |
| DNS, WHOIS, SPF/DMARC of a domain | `lookup_domain` |
| Alerts on a firm or on new firms in a niche | `watch_company`, `watch_caen`, then `poll_watchlist`; `unwatch` to stop |
| How many lookups are left today | `get_usage` (free, not counted) |
| Something missing or wrong in the data | `report_issue` (free, not counted) |

Parameters for each tool: [references/tools.md](references/tools.md).

## Workflows

### A lead list ("electricians in Cluj", "IT firms in Timiș with 10–50 people")
1. Turn the niche into CAEN codes. Use [references/caen-niches.md](references/caen-niches.md),
   or pass the user's words as `topic` and read `matched` / `caenCodes` in the answer. If the answer
   is `error: ambiguous_topic`, show the `candidates` and ask which one; never guess.
2. Call `lookup_by_category` with `topic` = the codes (`"4321"` or `"4321,4322"`), `county`, and
   `legal_form: "SRL,SA"` unless the user wants sole traders. Without it the newest-first list
   fills with freshly registered PFAs.
3. Add `main_activity_only: true` when the user wants firms that really do the activity. Many firms
   are only authorised for dozens of codes. Add revenue/headcount bands (`min_revenue` in RON,
   `min_employees`) or `vat_payer` when asked.
4. `active_only` is on by default and removes struck-off, dissolving, insolvent and ANAF-inactive
   firms. Say how many it removed (`inactiveFilteredOut`; when the answer marks it approximate,
   say "about N ± margin").
5. Ask for `compact: true` or `fields` for lists longer than about 10, so the answer stays small.
6. For contacts, run `enrich_company` on the firms the user picks. Not on all of them: each call
   crawls a website and counts as a lookup.

### Check a firm before a deal
1. `lookup_business` with the CUI (exact) or the name plus `county`. If several firms share the
   name, list them with status and county and ask which one.
2. Read `risk`: `level` (ok / watch / inactive / dissolving / insolvent / closed), `reasons`,
   `notChecked`.
3. `lookup_financial_ratios` for the trend, health score and red flags; `lookup_financials` for the
   raw years.
4. Report it as a first look, never a verdict (see the answer rules).

### Match the user's client list
1. Build `rows` from their file: `{name, county?, domain?, cui?}` per row. A valid CUI wins at
   confidence 1.0.
2. Call `get_usage` first when the list is long: a batch counts one lookup per row, and a batch
   bigger than what is left today is refused whole. Split it, or tell the user what is left.
3. Report matched / no_match counts. Show `no_match` rows with their `candidates` and any row
   flagged `ambiguous`, `nameDiffers` or `countyMismatch` for the user to confirm. Never silently
   accept a match below about 0.8 confidence.

### Monitor
`watch_company` (a firm) or `watch_caen` (new firms in a code and county) register a watch on the
user's key. `poll_watchlist` returns what changed, most severe first, and lists every watch the
key holds (`active`). `unwatch` (`cui`, or `code` with its `county`) stops one; clean up the
watches you set for a one-off check. Watches need a key.

## Answer rules

- **Cite the date.** Every answer carries `asOf`. Say "as of the ONRC snapshot of <asOf.registry>",
  name `asOf.financialYear` with any figure and `asOf.anaf` with VAT or inactive status. The registry
  is a periodic snapshot, not live.
- **Coverage.** `risk.level: ok` only means no distress signal in the ONRC statuses and ANAF flags
  Leadgen holds. The insolvency bulletin (BPI), tax debts, court cases and shareholders are **not**
  checked (`risk.notChecked`). Never call a firm clean, safe or solvent from this data alone; say
  what was not checked.
- **Money.** Financial figures are in RON from the firm's own filing for that year. Say so, and
  don't convert unless asked.
- **People.** Directors and sole traders (PFA, II, IF) are personal data. Show them only when the
  user's task needs them, and never build profiles of private individuals.
- **Credit the data** when the user publishes or ships results:
  "Source: ONRC and Ministry of Finance (data.gov.ro, CC BY 4.0; financial statements 2008–2010
  under OGL-ROU-1.0) and ANAF, via Leadgen (leadgen.adrianhomelab.com)". The answers carry it as
  `attribution`.
- **Links to share.** A company result's `url` is its public record page: give it to the user when
  they want to see or keep the record (it is null for sole traders and other natural persons). A
  `lookup_by_category` list carries `appUrl`, the same list opened in the Leadgen app. Pass both on
  as they are.
- **Limits.** When a call is refused for the daily limit (`daily_limit_reached`, MCP error -32002),
  quote the limit from the refusal, say when it resets (midnight Romanian time, 00:00 Europe/Bucharest) and give the `get_a_key` link it
  carries. Don't retry in a loop.
- **Plans.** If a tool answers `error: plan_required`, explain that the feature needs a paid plan and
  show the `upgrade` link from the answer. Don't work around it with many smaller calls.
- **Language.** Search is diacritic-insensitive; plain ASCII works (`"brasov"`, `"constructii"`).
  Answer in the user's language and keep Romanian legal terms (SRL, PFA, radiată, CAEN) as they are.

## Wrong or missing data

If a record looks wrong (a closed firm shown as active, a missing firm or field), call
`report_issue` with `kind: "wrong_record"` and the `cui`, or `kind: "gap"`. It's free and reaches
the founder. ONRC is the legal source of truth; corrections to the registry itself go through ONRC.
