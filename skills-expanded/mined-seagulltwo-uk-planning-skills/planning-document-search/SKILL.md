---
name: planning-document-search
description: >-
  Retrieve the documents attached to a UK planning application from the local
  council's public online planning portal, given the application reference and
  the council name. Covers the major portal vendors (Idox, Northgate, Civica,
  Ocella, Agile, NEC, TerraQuest, StatMap, DEF Atrium and more) with a
  per-vendor retrieval recipe and a council→portal→vendor registry.
license: MIT
---

# Planning Document Search Skill

Download the documents attached to a UK planning application from a council's
online planning portal, given the application reference number.

## When to use

The user gives you a planning application reference (e.g. `6/2026/1249/HOUSE`,
`5/2026/1349`) and a council name, and wants the associated documents (application
forms, plans, elevations, officer reports, etc.) downloaded.

## Scope and responsible use

Read this before running anything — it is a condition of the skill, not advice.

- **Not legal advice; no warranty.** This is a retrieval aid, provided "as is"; verify
  what it returns.
- **Public records only, retrieved the way a member of the public would.** UK planning
  registers exist for public inspection; this skill fetches documents a council has
  *deliberately published*. Use it for legitimate, targeted retrieval — a specific
  application a user needs — not for bulk harvesting, monitoring, or rebuilding a
  council's register.
- **Never defeat a bot challenge.** If a portal serves an actual challenge or `Blocked`
  page (Barracuda JS challenge, AWS WAF `202`/`x-amzn-waf-action`, an escalating
  Cloudflare interstitial), **stop the automated approach and hand the user a browser
  deep link** instead. The recipes are built around this: they work where access is
  open and defer to a real browser where it is not. Do not try to solve, replay, or
  fingerprint-spoof a challenge.
- **If retrieval struggles, stop and suggest a manual download.** The recipes are the
  method; they are not a licence to keep trying things. When a recipe doesn't work —
  persistent errors, downloads failing magic-byte verification, greps finding no links,
  a portal matching no vendor signature — make at most a couple of *documented*
  corrections (re-resolve the vendor per Step 0; re-check the base path and the
  authority profile's recorded `quirks`) and then **stop the automated approach**. Report exactly
  what was and wasn't retrieved, and hand the user a browser link to the application
  (the portal's detail or documents page, as deep as you can construct) so they can
  download the remaining files manually. Do not respond to failure by escalating —
  no improvised scraping approaches beyond the recipes, no headless browsers, no
  retry loops against a struggling portal. A clean handover to manual download is a
  successful outcome of this skill, not a failure.
- **Be a good citizen on every request.**
  - Send an **identifying User-Agent with a real contact address** on PlanIt calls
    (replace `you@example.com` with your own), and a normal browser UA on portal calls.
  - **Pace requests — at least ~1–2 s between calls to the same host**, and do not
    parallelise requests against a single council. Small council servers fall over
    under bursts.
  - **Honour `429` / `Retry-After` and back off.** Stop on repeated errors rather than
    retrying in a tight loop.
  - **`robots.txt` — honour it for enumeration; a user-directed retrieval is not
    crawling.** `robots.txt` is a convention addressed to **crawlers and indexers**:
    automated systems that traverse a site on their own initiative. When a person asks
    for the documents on a named application, this skill is acting as **their** user
    agent. An AI-assisted human is still a human — one member of the public exercising
    the right to inspect a public register — and the fact that a tool formats the HTTP
    request does not turn them into a robot.

    **The test is initiative, not technology:**

    | A specific person asking for a specific application, now | Human-directed. Proceed under the pacing rules above. |
    |---|---|
    | **Enumeration, sweeps, monitoring, whole-register harvests, or building a dataset across authorities** | **That is a crawler, however it was invoked.** `robots.txt` applies in full, including `Crawl-delay`. |

    Four things this does **not** license, and they are the point:
    - **It is not a volume allowance.** Everything above still binds — identifying UA,
      ~1–2 s spacing, no parallel requests to one council, back off on `429`.
    - **It does not touch the bot-challenge rule.** A challenge is the site actively
      refusing this client. Stop and hand over a browser link, always.
    - **Terms of use are a stronger signal than `robots.txt`.** Where a portal's terms
      expressly prohibit automated access, honour that and hand the user a browser link
      — it is specific and deliberate in a way a default `robots.txt` often is not.
    - **It is not a licence to fetch what the user did not ask for.** "User-directed"
      means the application they named, and the chain it belongs to — not the register
      around it.

    **Tell the user — this is not a decision to make silently on their behalf.** Where a
    portal's `robots.txt` disallows the path you are about to request, say so plainly
    when you hand the documents over: that the fetch was automated, that the site's
    `robots.txt` asks automated clients not to take that path, that you proceeded because
    they asked for a specific application on a public register, and that they can use the
    browser link instead if they would rather. One or two sentences, not a disclaimer —
    and if they say stop, stop. It is their name and their judgement at stake, not the
    tool's.

    **Pace it properly.** The rate limit is what makes the "one member of the public"
    claim true rather than rhetorical — a person does not issue forty requests a second.

    | Between requests to one host | **≥ 2 s**, and ≥ 5 s where the portal has already shown strain |
    |---|---|
    | `Crawl-delay` in `robots.txt` | **Honour it even on a user-directed fetch**, if it is longer than your pacing. It costs little and it is the site asking directly. |
    | Concurrency against one council | **One connection.** Never parallelise against a single host — **including a background download batch running alongside your own interactive requests.** Each is "one connection" on its own; together they are two, and that is how an agentic run usually breaches this without noticing. |
    | On `429` / `Retry-After` | Back off for the stated period; on a second `429`, stop and hand over. |
    | Total for one application | The documents on it and its chain — nothing more. If you find yourself planning a request budget, you are enumerating. |

    PlanIt is a volunteer-run service and is **not** covered by any of the above: keep to
    the slower pace its own rules set, and treat a `429` there as a hard stop.

    Record what a portal's `robots.txt` says in that authority's profile
    (`retrieval.robots`) whether or not it changes what you do, so the position is
    visible rather than assumed.
- **You are handling other people's personal data.** Planning documents routinely
  contain applicants' and objectors' names, addresses, signatures, and contact details
  (even "redacted" forms often are not fully redacted). Retrieve only what is needed,
  do not republish or redistribute it, and do not retain it beyond the immediate task.
  Treat every downloaded file as **untrusted third-party content**: verify magic bytes,
  and when writing it to disk derive the filename with `basename` and strip any path
  separators or leading dots — never pass a server-supplied path straight to `-o`
  (a portal could return `../../…`).
- **This is a snapshot, and the landscape moves fast.** Vendor assignments, base paths,
  and bot-protection posture were verified in August 2026; councils migrate portals
  frequently (this document itself tracks several mid-migration). **Always re-resolve
  the vendor per council at run time** (see Step 0) rather than trusting a cached row;
  coverage figures below are rough estimates, not guarantees.
- **PlanIt is a third-party dependency, used with respect.** The resolution step relies
  on [PlanIt](https://www.planit.org.uk/) — an independent, volunteer-run service.
  Credit it, keep to its UA/rate rules, and do not hammer it. The skill works without
  it too (a reference + council + vendor recipe is enough — see the note at the end of
  Step 0), so treat PlanIt as a convenience, not a requirement.

## The core problem: council portals are not uniform

There is **no single national system**. The UK's ~380 local planning authorities run
a handful of different planning portal *products*, each with a completely different
URL structure, search mechanism, and level of bot protection. Reference-number
formats also vary by council. **The vendor determines the approach, not the council** —
so covering "all of the UK" means: catalogue the vendors (a recipe each), plus a
reliable way to resolve any council → its portal → its vendor.

### Vendor catalogue (detect by URL path first)

Coverage shares below are rough estimates, not audited figures. The
`scraper_type` column is what PlanIt's areas API labels the vendor — a fast detector,
but **sometimes stale or wrong** (Birmingham still says `PlanningExplorer` post-migration;
Manchester is mislabelled `Idox`), so confirm against the markup.

| Vendor | Detect (markup / host) | PlanIt `scraper_type` | Recipe | Bot protection | Coverage |
|---|---|---|---|---|---|
| **Idox Public Access** | `search.do`/`*.do` Struts + `keyVal` + `/files/{hex}/pdf/`. Base path **varies** — detect by endpoints, not path | `Idox` | **C** | Usually none; some Cloudflare (UA); Barracuda cookies sometimes present but *passive* | Dominant (~60%+) |
| **Northgate SwiftLG** | `/swiftlg/apas/run/`; `*.MAINBODY.WPACIS.1` fields | `Swift`/`Northgate` | **D1** | None observed | **Dying** — presume migrated (see note) |
| **Northgate Planning Explorer** | `/Northgate/PlanningExplorer/`; `.aspx` + `__VIEWSTATE` | `PlanningExplorer` | **D2** | Cloudflare (passive); some origin-WAF quirks | Minority, also migrating |
| **NEC Assure ES** | `/NECSWS/ES/Presentation/`; `AssureLogo`; MVC+AJAX | may stalely say `PlanningExplorer` | **H** | None enforcing (F5 LB passive) | Growing (ex-Northgate) |
| **Civica Portal360** | `civica.loader.js`; `Handler.ashx`; `keyobjectsearchandview` | `CivicaJson` | **B** | Per-council — mostly passive/absent; St Albans enforces Barracuda | Minority |
| **Ocella** | `/OcellaWeb/planningSearch` | `Ocella` | **E** | None enforced (passive fingerprint at Arun) | Niche |
| **StatMap horizoNext** ("Mirage") | `*-publicportal.statmap.co.uk`; `/horizonext` SPA; JSON API `/horizoNext/api/` | `Custom` | **F** | None — open JSON API | Small (ex-SwiftLG) |
| **Agile Applications** | `planning.agileapplications.co.uk/<slug>/`; "Citizen Portal Planning"; `*.sunagile.com` CSP | `Agile` | **G** | None — open JSON API (3 headers) | Small, growing (ex-SwiftLG) |
| **TerraQuest PP2** | Next.js + `/__ENV.js` w/ `*.tqinfra.co.uk` API. NI: `planningregister.planningsystemni.gov.uk` | (indexed) | **I** | None — open JSON API (1 header) | All 11 NI authorities |
| **Arcus** (Salesforce) | `*.my.site.com`/`*.force.com`/council CNAME; Lightning SPA; `Server: sfdcedge` | often mislabelled | — browser-only* | Guest Aura curl-able; blocked on unknown apex sigs | Small, growing |
| **DEF Atrium** | `/Search/Results` POST + `__RequestVerificationToken`; `/Planning/Display?applicationNumber=`; `/Document/Download?module=PLA&…`; `/Content/def/` CSS | `Atrium` or `Custom` | **A** | None; Somerset adds a disclaimer-cookie gate | Small (incl. county registers) |
| **Tascomi RSH** (Idox group) | `index.html?fa=<action>` dispatcher; "Regulatory Services Hub" title; `AWSCaptcha.js` | `Tascomi` | — browser-only | **Enforcing AWS WAF challenge** (202 + `x-amzn-waf-action`) on the first request at every install tested | Growing (ex-PE); several large metropolitan councils |
| **Idox Publisher** (docs host) | `d0cs.*` host; `/Publisher/mvc/listDocuments?identifier=…&ref=…`; `/publisher/idoxui/` CSS | `Custom` | **J** | None seen (downloads session-gated) | Docs module only — pairs with bespoke registers (Colchester) |
| **Custom / bespoke** | none of the above | `Custom` | treat A as a template | Varies | Long tail |

\* Arcus public registers have no anonymous API surface — treat as browser-only and hand
the user a deep link. See the Arcus section.

Detection cheat-sheet for an unknown portal: `.do` actions + `keyVal` = Idox (any base
path); `/swiftlg/apas/run/` = SwiftLG; `/Northgate/PlanningExplorer/` = Northgate PE;
`/NECSWS/ES/Presentation/` = NEC Assure; `/OcellaWeb/` = Ocella;
`*-publicportal.statmap.co.uk` = StatMap; `planning.agileapplications.co.uk/<slug>` /
"Citizen Portal Planning" = Agile; Next.js + `/__ENV.js` on `*.tqinfra.co.uk` =
TerraQuest PP2; Salesforce `*.force.com`/`my.site.com`/`Server: sfdcedge` = Arcus;
`civica.loader.js` = Civica; `/Search/Results` + `__RequestVerificationToken` +
`/Document/Download?module=PLA` = DEF Atrium; `index.html?fa=` dispatcher + "Regulatory
Services Hub" = Tascomi (browser-only); `/CMWebDrawer/` = HP TRIM docs host (append
`&format=json`); `/Publisher/mvc/listDocuments` + `/publisher/idoxui/` assets = Idox
Publisher docs host (Recipe J — a documents module paired with a bespoke register);
`__VIEWSTATE` with none of the above = bespoke WebForms. **`__VIEWSTATE` alone is not
evidence of Planning Explorer**; that needs the `/Northgate/PlanningExplorer/` path. A
council-built WebForms register was once mislabelled that way.
**When the portal is a JS/SPA shell, fetch its runtime-config file** (`/__ENV.js`,
`config.js`, or the app bundle) — for the open-API vendors (StatMap, Agile, TerraQuest)
that file hands you the real API host, and often a tenant id/header you'll need.

> **⚠ SwiftLG is being retired fast.** Of four historic SwiftLG councils tested in
> Aug 2026, only Warwickshire still ran it — Mole Valley → StatMap, and Dudley,
> Snowdonia, Pembrokeshire → Agile (old hosts dead or DNS gone). **Presume any
> historic SwiftLG council has migrated until PlanIt's `planning_url` proves
> otherwise.** The successors are open JSON APIs (Recipes F/G), so migration usually
> makes retrieval *easier*, not harder.

## General procedure

**Step 0 — get the portal URL + vendor.** Everything the recipes need is the *portal
URL* and *vendor* for the user's council; the *reference* comes from the user. There are
two paths, and the first one needs no external service at all.

### Fast path — known council: you don't need PlanIt

**If the user gives you a planning reference and a council, and that council is in
[`planning-portal-registry.json`](planning-portal-registry.json) with `status:
tested-ok`, you are done resolving.** The index row gives you the portal URL, the vendor
and — in `detail` — the path to that council's profile in `authorities/`. **Read the
profile**, then go straight to the vendor's recipe and run it from the user's reference:
search the reference → detail/keyVal → documents → download.

Check the profile's `scriptable` field first. `false` means do not start an automated run
at all — go to the `browser_route` and hand the user a link. **`null` means untested, not
unreachable**: try the vendor recipe, say that you are doing so, and record the result.

**Skeleton entries: every authority has a row, but not every row has been run.** The
registry now covers every GB council area, and a large minority of those rows exist so that
no council is a blank — they carry a `skeleton-entry` quirk saying so. On one of those, the
portal URL is real and the vendor came from a landing-page fingerprint, but **the search
chain, the documents route, the file-GET gating and pacing are all unverified, and no
document has ever been downloaded there**. So:

- Treat the recipe as a **starting hypothesis**, not a tested route, and **tell the user**
  you are trying an untested profile.
- Expect the vendor to be wrong sometimes — check `portal.vendor_verified`. `false` means
  even the vendor is a hint (from a URL pattern or PlanIt), and the skill records PlanIt's
  `scraper_type` as stale at one authority and wrong at another.
- **Record what happens.** A skeleton row that gets run and updated is the point of it
  being there.

**PlanIt is not in the loop for this case.** Reference + council + this skill (index +
profile + recipe) is sufficient to retrieve the documents; do not call PlanIt just out of
habit.

(PlanIt's only remaining offer here would be the `n_documents` completeness figure — and
the recipes get that from the portal's own documents page instead; see the completeness
cross-check in the checklist. Skip PlanIt entirely on the fast path.)

### Resolution path — unknown/novel council: use PlanIt (or a council-site scrape)

If the council is **not** in the registry (or its recorded portal looks stale — councils
migrate), you need to resolve council → portal URL + vendor. Use the **PlanIt API** — the
live national LPA → portal directory — instead of hand-hunting the council website:

```bash
# Council -> portal base URL + vendor family (planning_url, scraper_type):
curl -s "https://www.planit.org.uk/api/areas/json?area_type=planning&auths=<council>" \
  -A "planning-doc-search (contact: you@example.com)"

# Reference -> the council application URL (the `url` field is the portal deep link):
curl -s "https://www.planit.org.uk/api/applics/json?id_match=<ref>" \
  -A "planning-doc-search (contact: you@example.com)"
```

```bash
# Need a fresh/recent application for an authority (e.g. to test with)? —
curl -s "https://www.planit.org.uk/api/applics/json?auth=<council>&pg_sz=3&recent=60" \
  -A "planning-doc-search (contact: you@example.com)"
```

PlanIt rules: **always send an identifying User-Agent** (403 without one) and
**back off on 429** (honour `Retry-After`). PlanIt gives you the council application
URL + vendor but **not** document file links — follow the URL into the portal and
apply the vendor recipe. (`planning.data.gov.uk` is spatial/policy constraints only —
Article 4, conservation areas, listed buildings, local plans — **not** a document
source.)

**⚠️ `auths=` is a fuzzy name match, and it returns neighbouring councils.** It is not a
lookup. Two hits from one batch: `auths=Renfrewshire` returned **East Renfrewshire's
building standards** register as well as Renfrewshire's planning one, and `auths=Warwick`
returned **North Warwickshire** (DEF Atrium) alongside Warwick District (Idox) — different
councils, different products. Taking the first row silently puts you on the wrong
authority's register, and retrieval then *works perfectly* and hands back the wrong
universe of applications. **Match the authority name exactly against the row before using
its `planning_url`**, and check the register is the planning one (see the building-standards
trap in Recipe C).

**An empty `areas` result is not evidence the council has no portal — try `applics`.** One
council returned *no* areas record at all while `applics` returned applications whose `url`
gave both the portal host and a detail-page pattern keyed by the human reference. If areas
comes back empty, pull a recent application for that authority before concluding anything.

Two further PlanIt caveats: the **areas record can mislead** — Camden's
`planning_url` points at a Socrata open-data dataset, not the portal; the *applics*
records' `other_fields` (`docs_url`, `url`, `comment_url`) are the real portal
pointers, so when the areas record looks odd, pull a recent applic and trust its URLs.
And **merged authorities fragment**: post-2023 Somerset still files current district
applications on the legacy district portals (Mendip/South Somerset Idox) while running
a consolidated DEF Atrium register for county matters — PlanIt lists legacy districts
as separate areas, and the per-application `url`/`docs_url` is the router that tells
you which portal a given reference lives on.

PlanIt shortcuts: applics records often carry
**`other_fields.docs_url`** — the fully-formed Idox documents-tab URL *including the
keyVal* — plus `n_documents` (a free completeness check against your scraped link
count). The `url` field frequently embeds the portal's opaque record id too
(Idox `keyVal=`, Ocella `planningDetails?reference=`, StatMap trailing internal id).
When present you can skip a recipe's search steps and jump straight to the documents
step — but for session-gated vendors (Idox) still hit the search page once first to
get a session cookie. Derive a portal's base path from the areas `planning_url` by
stripping the trailing `/search.do?...` page — do **not** assume `/online-applications/`.

If PlanIt lacks the council, fall back to the council website:

```bash
curl -s -L "https://www.<council>.gov.uk/view-and-track-planning-applications" -A "Mozilla/5.0" \
  | grep -oiE 'href="http[^"]*"' | grep -iE 'planning|search|idox|publicaccess|civica|swiftlg|ocella' | sort -u
```

**PlanIt is a convenience, not a requirement.** All the vendor recipes need is the
**portal URL + vendor**; the reference itself comes from the user. What PlanIt actually
buys you is (a) resolving council → portal URL + vendor without hand-hunting the council
site, and (b) shortcuts — `docs_url`/`keyVal`/internal ids that skip a recipe's search
step, and `n_documents` as a free completeness check. If you already know a council's
portal and vendor (e.g. it is in the registry with `status: tested-ok`), you can run the
recipe directly from the user's reference and **use PlanIt only for the `n_documents`
cross-check** — or skip it entirely. The registry is the offline substitute for (a); the
recipe's own search step is the substitute for (b).

**Steps 1–5 — identify the vendor** (table above) → **search** the reference →
**extract the detail-page / keyVal** → **enumerate document links** → **download**
each with the same session. Then **deliver** the files and **record the result**: the
index row (`status`, `scriptable`, `last_tested`) and the authority's profile in
`authorities/` (endpoints, quirks, pacing, a `verification` entry).

---

> ### How to read the recipes, and where the per-council detail actually lives
>
> **The recipes below are vendor-level.** They describe the product — its call chain, its
> tokens, the shape of its responses — and they are the same for every install of it.
>
> **Where a recipe names a council, treat it as an exemplar, not a specification.** The
> name is there because that install is where the behaviour was first isolated, and it
> makes an abstract step concrete. It is not a statement that the behaviour is universal,
> and it is not the authoritative record: **the per-install facts are in
> `authorities/<slug>.json`** — that install's endpoints, its parameter values, the headers
> it needs, its quirks, its pacing.
>
> So: **read the recipe for the method, and the profile for this council.** If the two
> disagree, the profile is about the portal you are actually calling. And if a run teaches
> you something new, ask which of the two it belongs in — the three-way test is under
> "What belongs where" below. A per-install fact written into a recipe is how one recipe
> silently forks into forty divergent copies.

## Recipe A — DEF Software "Atrium"

Originally documented as "custom ASP.NET" from Welwyn Hatfield; **identified as the DEF
Software Atrium product** — Somerset's consolidated register shares every form and
endpoint (detect: `/Search/Results` POST,
`__RequestVerificationToken`, `/Planning/Display?applicationNumber=`,
`/Document/Download?module=PLA&recordNumber=…&planId=…`, `/Content/def/` CSS,
`def.co.uk` privacy link; PlanIt `scraper_type: Atrium` or `Custom`).

The search form is a server-rendered POST protected by an ASP.NET anti-forgery scheme:
you need **two matching tokens** — the `__RequestVerificationToken` cookie *and* the
hidden form-field token from the page HTML. They are validated as a pair, so steps 1–2
must run against the same cookie jar.

With an exact application number, the search redirects straight to the detail page
(Welwyn) or links to `/Planning/Display?applicationNumber=<enc-ref>` (Somerset — the
human reference is the key; no opaque internal id needed).

**⚠️ Two generations ship under this vendor and they share no endpoints.** Everything below
is the **MVC "Atrium"** build. There is also an older **ASP.NET WebForms** build (`css/DEF/`,
`css/def/Site.js`) whose chain is entirely different: `disclaimer.aspx` cleared as a WebForms
postback (`…$btnAccept=Accept`, with `__VIEWSTATE` / `__VIEWSTATEGENERATOR` /
`__EVENTVALIDATION` echoed back) → `advsearch.aspx`, whose **Telerik date pickers need each
date as a pair of fields** (`…$txtDateReceivedFrom` *and* `…$txtDateReceivedFrom$dateInput`)
→ `searchresults.aspx` → rows linking to `plandisp.aspx?recno=<internal-id>`. There is no
`/Search/Results`, no `__RequestVerificationToken` and no `/Disclaimer/Accept`. **Its
documents have no URLs at all**: each is a grid postback
(`__EVENTTARGET=…$DocumentsGrid`, `__EVENTARGUMENT=RowClicked:<index>`) whose **response body
is the file**, with the real name in `content-disposition` — so there is nothing to grep for
as an href, and an href-shaped search concludes there are no documents. Fingerprint the
generation from the markup before picking a chain; `vendors.json` carries both.

**Two traps in newer MVC builds too**, both silent: the gate can be a plain form POST to
**`/Disclaimer/AcceptDisclaimer`** (token + `returnURL` field) rather than the
`/Disclaimer/Accept` below, which **404s**; and date inputs can be `type="date"`, which a
browser submits as **`yyyy-mm-dd`** even though the placeholder reads `DD/MM/YYYY` — the
wrong format is accepted and ignored, giving a clean zero.

**Somerset variant quirks**: a **disclaimer gate** precedes everything — POST
`/Disclaimer/Accept?returnUrl=<path>` with an **explicit `Content-Length: 0` header**
(the front-end 411s a plain empty POST) → sets an `AcceptedDisclaimer` cookie (~1h
expiry) that document downloads require (a cold download 302s back to the disclaimer).
Search-scope flags differ (`SearchPlanning`/`SearchAppeals` + `AdvancedSearch=True`),
and `DateReceivedFrom/To` (`dd/mm/yyyy`) date sweeps work for discovering references.

```bash
# 1. Load homepage: capture session cookie (-c) and the hidden form token
TOKEN=$(curl -s -c whc.txt "https://planning.welhat.gov.uk/" -A "Mozilla/5.0" \
  | grep -o '__RequestVerificationToken" type="hidden" value="[^"]*' \
  | sed 's/.*value="//')

# 2. POST the search — token + app number + the four search-scope flags
curl -s -b whc.txt -c whc.txt -A "Mozilla/5.0" -L \
  "https://planning.welhat.gov.uk/Search/Results" \
  --data-urlencode "__RequestVerificationToken=$TOKEN" \
  --data-urlencode "SearchPlanning=True" \
  --data-urlencode "SearchAppeals=True" \
  --data-urlencode "SearchEnforcement=True" \
  --data-urlencode "SearchTreePreservationOrders=True" \
  --data-urlencode "ApplicationNumber=6/2026/1249/HOUSE" \
  --data-urlencode "Address=" \
  -o results.html

# 3. Extract document download links (un-escape &amp;)
grep -oE 'href="/Document/Download[^"]*"' results.html \
  | sed 's/href="//;s/"$//;s/&amp;/\&/g' | sort -u

# 4. Download each doc, reusing the session cookie. Links differ only in
#    planId / imageId / isPlan / fileName; recordNumber is the internal app id.
curl -s -b whc.txt -A "Mozilla/5.0" -o "ApplicationFormRedacted.pdf" \
  "https://planning.welhat.gov.uk/Document/Download?module=PLA&recordNumber=111526&planId=2173461&imageId=2&isPlan=False&fileName=ApplicationFormRedacted.pdf"
```

Notes:
- **Download links are not always in `href`.** One install puts them in
  `data-disabled-link` attributes, which the page's script enables after a copyright
  tick-box. An `href` grep finds nothing, but a plain GET of the attribute's URL works.
  Grep for `/Document/Download` wherever it appears.
- **Links can be listed twice.** De-duplicate before comparing your count with the
  page's document count.
- **A disclaimer cookie can arrive already expired.** One install writes local time as
  GMT, so a strict client drops the cookie at once and every download bounces back to
  the disclaimer. Keep it for the session regardless of its stated expiry.
- **Detail links can be path-form.** Some installs link
  `/Planning/Display/<REF-with-slashes>` instead of `?applicationNumber=<ref>`, so a grep
  for the query form finds nothing and the search looks empty. Match both.
- **⚠️ A newer Atrium build does not match this recipe at all.** It runs on ASP.NET Core
  with none of the `/Content/def/` assets, and it has no `/Document/Download` links.
  - Every page first redirects to a disclaimer, accepted by a form POST to
    `/Disclaimer/AcceptDisclaimer` with the page's anti-forgery token.
  - The search form carries reCAPTCHA. **Do not script it.** Take the reference from the
    user or from PlanIt's applics record, and go to the detail page directly.
  - Each document row is a "View" button. The file comes from `POST /Document/GetFileBinary`
    as a **base64 string inside JSON**, so decode it before the magic-byte and size checks.
  Run as written, Recipe A reports these installs as having no documents. The per-install
  parameters are in the profiles.
- Always send a real browser `User-Agent` (`-A "Mozilla/5.0 …"`). Some council
  portals reject curl's default UA.
- The detail page also carries each document's description and created date next to
  the link — grep those out to label the files for the user.
- Verify downloads are real PDFs (`file *.pdf`) — a bot block or session timeout
  returns an HTML error page with a `.pdf` name. **Magic bytes are necessary, not
  sufficient**: check size and extracted text too (see the checklist at the end — some
  installs serve the rate-limit notice as a genuine PDF).

---

## Recipe B — Civica Portal360 (browser-only only where an enforcing Barracuda is present)

**Barracuda is a per-council property, not a Civica one.** Of the four CivicaJson sites
in PlanIt, Ashfield has no WAF, Waverley has passive Imperva Incapsula, and only
St Albans runs *enforcing* Barracuda. So on most Civica sites the JSON API is fully
curl-able — the browser fallback below is needed only when you actually get a
`Blocked` page.

### B (curl) — the JSON API chain

Everything is a JSON POST to the Civica `Handler.ashx` API. Two things are per-site;
**read them from the search page's inline config**, don't hardcode:
- `Civica.APIUrl=` → the API base path (`/civica/Resource/Civica/Handler.ashx/` at
  Ashfield; `/w2webparts/Resource/Civica/Handler.ashx/` at Waverley/St Albans; an
  absolute cross-host URL at Eastbourne).
- `Civica.PortalSettings.PlanningApplicationRefType` → the `refType`. **It is per-install
  and there is no default — always read it from the page config rather than assuming.**
  `GFPlanning` at Ashfield and Waverley; `PBDC` at St Albans **and at Lewes**,
  so `PBDC` is *not* a legacy St-Albans-only value as this skill previously recorded;
  `PLANNINGCASE` at Great Yarmouth; `APPPlanCase` at Eastbourne. Getting it wrong returns
  a 500 with a JSON error body — which is a wrong-parameter signal, not a block.
- **The honoured search field goes with the `refType`, and the page script names it.**
  Seen so far: `SDescription` with `GFPlanning`, `ref_no` with `PBDC`, and
  `PlanningApplicationId` with `APPPlanCase`. Read it from the page's inline script
  rather than guessing. A wrong field is ignored silently (see the traps below).

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
API="https://planning.ashfield.gov.uk/civica/Resource/Civica/Handler.ashx"   # from Civica.APIUrl
RT="GFPlanning"                                                              # from PlanningApplicationRefType
REF="V/2026/0515"

# 1. Search (JSON POST — NOT the old keyText GET). -> KeyObjects[].KeyNumber
curl -s -b civ.txt -c civ.txt -A "$UA" -H "Content-Type: application/json" \
  "$API/keyobject/pagedsearch" \
  -d "{\"refType\":\"$RT\",\"fromRow\":1,\"toRow\":10,\"searchFields\":{\"FullTextSearch\":\"$REF\"}}"

# 2. Document list for that KeyNumber (KeyText is the constant "Subject")
curl -s -b civ.txt -c civ.txt -A "$UA" -H "Content-Type: application/json" \
  "$API/doc/list" \
  -d "{\"KeyNumb\":244982,\"KeyText\":\"Subject\",\"RefType\":\"$RT\",\"ProcessNo\":\"\",\"PageSize\":50}"

# 3. Download one document by DocNo -> application/pdf
curl -s -b civ.txt -A "$UA" -o "SiteLocationPlan.pdf" \
  "$API/doc/pagestream?DocNo=19338083&pdf=true&filename=SiteLocationPlan.pdf"
```

Notes: a `500` with a JSON error body (LogRef) = wrong params, **not** a block —
distinct from a Barracuda `Blocked` HTML page. Empty `searchFields` returns zero rows
by design. Doc endpoints are defined in `civica.documents.js` under
`<base>presentation/bundle/` (not `civica.common.js`). PlanIt's applics
`url` carries `?RefType=&KeyNo=` for Civica sites — skip step 1.

More Civica facts:
- **Zip-all** — `GET <base>doc/list/zipstream?KeyNumb=<n>&KeyText=<kt>&RefType=<rt>&ProcessNo=`
  returns one zip of the entire document set. Prefer it for whole-application pulls;
  verify `PK` magic + entry count.
- **Three keying schemes**, not two: number-keyed (Ashfield/Waverley — `KeyNumb=<int>`
  from pagedsearch, `KeyText:"Subject"`), **reference-keyed** (Great Yarmouth and
  Eastbourne — `KeyNumb:0`, `KeyText:"<planning ref>"`, with that install's `RefType`), and
  **empty-`KeyText`** (Lewes — `KeyText:""`, with the honoured search field
  `ref_no`). The viewer deep-link fragment distinguishes the first two:
  `#VIEW?…&KeyNo=<n>` vs `…&KeyText=<ref>`. Treat `KeyText:"Subject"` as one install's
  value, not a constant.
- **⚠️ The POST-vs-GET trap, and it fails silently.** The search call must be a **POST**.
  Issued as a GET it still returns **HTTP 200** — and silently ignores the filter, handing
  back the *entire* register (one install returned 109,440 rows). Nothing in the response
  says the filter was dropped. Always check `TotalRows` against what you expected, and
  treat a suspiciously large result as a dropped filter rather than a broad match.
- **Silent search trap**: `FullTextSearch` can be ignored on some installs (Great
  Yarmouth returned the whole 30,992-row register) — always check `TotalRows` ==
  expected; the honoured field there was `searchFields:{"KeyNo":"<ref>"}`.
- `doc/list` rows may lack `FileName` (Waverley) — label from `DocDesc` +
  `FileExtension`; the `filename=` param on pagestream is client-chosen anyway.
- pagestream Content-Type can be `application/PDF` (uppercase) — match
  case-insensitively. Native `.docx` sources are converted to real PDF by `pdf=true`.
- Non-standard **ports** occur (Waverley `:4443`) — take host:port verbatim from
  PlanIt's `planning_url`.

### B (browser) — only when Barracuda actually enforces (St Albans)

`planningapplications.stalbans.gov.uk`. Here the page shell renders but every XHR/API
and document call returns a `Blocked` page. The server sends a
~67 KB obfuscated JavaScript fingerprinting challenge (loaded via a
`<script src="/bnith__…">` tag) that a **real browser must execute**: it computes a
device fingerprint, posts it back, and only then is a clearance cookie issued that
unlocks the API. Consequences:

- The top-level HTML page loads for curl (Barracuda allows the document navigation
  so it can serve the challenge), **but every XHR/API and document call returns a
  `Blocked` page**. No clearance cookie is ever set for a non-JS client.
- Reusing cookies from the HTML fetch does **not** help — there is no valid cookie
  to reuse until the JS challenge is solved.
- A headless browser (Playwright/Puppeteer) *might* work, but Barracuda is
  specifically designed to detect and block headless Chromium, so success is
  unlikely and not worth a heavy install as a first move.

### How to get past it: use a real browser session

1. **Claude in Chrome extension** (preferred if available) — drives the user's real
   Chrome, which passes the challenge invisibly because it's a genuine browser
   session. Requires the extension installed and signed in to the same account.
   (In this session it was "not connected", which blocked the automated route.)

2. **In-app Browser pane** — was **blocked by environment policy** for this domain,
   so unavailable here. Worth trying for other councils.

3. **Hand the user a one-click deep link** — the most reliable fallback. The
   full-text search deep link opens the application directly in the user's own
   browser:

   ```
   https://planningapplications.stalbans.gov.uk/planning/search-applications?civica.query.FullTextSearch=5%2F2026%2F1349
   ```

   (URL-encode the reference: `/` → `%2F`.) Civica deep-links to a specific record
   use the fragment form `#VIEW?RefType=PBDC&KeyNo=<internal-id>`, where `KeyNo` is
   the internal record id exposed in search-result links.

### Useful Civica internals (for when you *do* have a browser session)

- Config globals in the page: `Civica.APIUrl="/w2webparts/Resource/Civica/Handler.ashx/"`,
  `Civica.DocumentViewerUrl="/my-requests/document-viewer"`.
- Search service: `API.KeyObject` → `keyobject/search` and `keyobject/pagedsearch`.
- The planning search/view widget is `keyobjectsearchandview` with `RefType=PBDC`;
  its display fields include `ref_no`, `application_address`, `app_status`,
  `decision_date`, etc.
- JS bundles live under `/civica/Bundles/` (`civica.common.js` holds the API service
  definitions) — useful for discovering endpoint names without a browser.

---

## Recipe C — Idox Public Access

The highest-value recipe — Idox powers the majority of UK LPAs. The base path
**varies** — `/online-applications/` (common), `/idoxpa-web/` (Edinburgh),
`/publicaccess/` (Cardiff) all seen, and the wrong one 403s — so treat it as a
per-council variable and detect Idox by its endpoints (`search.do`, `keyVal`,
`/files/{hex}/pdf/`). Note Idox increasingly lives on **vendor-cloud hostnames**
(`*.idoxcloud`, Cardiff's `*.wales`) rather than council domains, so resolve via
PlanIt rather than guessing `<council>.gov.uk`. It is **session-gated** (a `JSESSIONID`
from the search page is required; results endpoints 500 without it — note JSESSIONID is
HttpOnly: rely on curl's cookie jar, not a Set-Cookie grep) and the search form carries
a `_csrf` token you must echo back (format varies: opaque hex or lowercase UUID).
Validated end-to-end against nine councils in August 2026, including Scottish and Welsh
authorities.

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
BASE="https://planningaccess.york.gov.uk/online-applications"   # <- swap per council; base path VARIES (e.g. Edinburgh /idoxpa-web)
BP=$(echo "$BASE" | sed -E 's#https?://[^/]+##')                # path part, e.g. /online-applications
REF="24/00593/FUL"

# 1. Establish session; capture JSESSIONID (-c) and the _csrf hidden token
curl -s -c idox.txt -A "$UA" "$BASE/search.do?action=simple&searchType=Application" -o s.html
CSRF=$(grep -oE 'name="_csrf"[^>]*value="[^"]*"' s.html | grep -oE 'value="[^"]*"' | sed 's/value="//;s/"//')

# 2. POST the simple search. All four fields are required — WITHOUT
#    searchCriteria.simpleSearch=true the server returns "Too many results".
curl -s -b idox.txt -c idox.txt -A "$UA" -L "$BASE/simpleSearchResults.do?action=firstPage" \
  --data-urlencode "_csrf=$CSRF" \
  --data-urlencode "searchType=Application" \
  --data-urlencode "searchCriteria.simpleSearchString=$REF" \
  --data-urlencode "searchCriteria.simpleSearch=true" \
  -o results.html

# 3. Extract the keyVal (opaque token, NOT the human reference). Usually ~13
#    uppercase alphanumerics, but NOT always (some use _GUILD_DCAPR_214647),
#    so match up to the next separator, never [A-Z0-9]+.
#    An exact-ref search may 302 to the detail page OR return a one-row results
#    list (both observed) — the grep covers both.
KEYVAL=$(grep -oE 'keyVal=[^&"'"'"' ]+' results.html | head -1 | cut -d= -f2)

# 4. Documents tab -> scrape file hrefs. PDFs are $BP/files/{32-HEX}/pdf/{name}.pdf
#    but NON-PDF attachments (JPG photos/plans) OMIT the /pdf/ segment
#    ($BP/files/{32-HEX}/{name}.jpg — Leeds had 4 of 6 docs like this), so do
#    NOT anchor the grep on /pdf/. Also grep against $BP, NOT a hardcoded
#    /online-applications/ — either mistake silently yields missing files.
#    Reconcile your link count against the documents tab's own total (it lists
#    one row per document) — see the completeness cross-check in the checklist.
DOCS="$BASE/applicationDetails.do?activeTab=documents&keyVal=$KEYVAL"
curl -s -b idox.txt -c idox.txt -A "$UA" "$DOCS" -o docs.html
grep -oE "$BP/files/[A-Fa-f0-9]+/[^\"]+" docs.html | sort -u > files.txt

# 5. Download each file WITH a Referer header = the documents-tab URL.
#    Some councils (verified: RBWM, Greater Cambridge) 404 the file without it;
#    harmless on the councils that don't need it, so always send it.
HOST=$(echo "$BASE" | grep -oE 'https://[^/]+')
while read -r f; do
  name=$(basename "$f")
  curl -s -b idox.txt -A "$UA" -e "$DOCS" "$HOST$f" -o "$name"
done < files.txt
```

Idox gotchas:
- **Base path varies** — **eleven** variants verified so far: `/online-applications/`
  (common), `/idoxpa-web/`, `/publicaccess/`, `/PlanningData-live/`, `/wam/`,
  `/public-access/`, `/online/`, `/Online/` (note the capital — paths can be
  case-sensitive), `/newplanningaccess/`, `/publicaccess-live/`, `/planning/`. Treat the
  list as open, derive the path from the authority's profile or PlanIt's `planning_url`,
  and never hardcode it in a grep (see step 4).
- **⚠️ A `publicaccess.*` hostname is not evidence of Idox.** Councils migrate portal
  products and keep the hostname. Two installs on `publicaccess.<council>.gov.uk` were
  found to be **Arcus** (`…/s/register-view?c__r=Arcus_BE_Public_Register`) and
  **Tascomi** (`…/index.html?fa=search`). Fingerprint the **markup or the URL path**, not
  the host — and be wary of any detection rule that would match a hostname, because it
  will quietly assign the wrong recipe and the failure looks like a portal fault.
- **Check you have the right register.** One authority's recorded Idox URL was its
  **building standards** register; retrieval worked perfectly and returned the wrong
  universe of applications. A successful download is not proof you are on the planning
  register.
- **⚠️ Read the tab list off the summary page — do not construct the documents-tab URL.**
  Not every install has a documents tab, and on one that does not,
  `applicationDetails.do?activeTab=documents` returns **HTTP 500** while the summary page
  200s — which reads as a portal fault rather than as "that tab does not exist here". GET
  `applicationDetails.do?keyVal=<k>&activeTab=summary` first (the results page's own href
  form), then take the real `activeTab=…` links from it and branch on what is actually
  there: `documents`, `externalDocuments`, or neither.
- **⚠️ Some installs publish no documents at all — a third case, distinct from the two
  below.** One install had **no documents tab and no `externalDocuments` tab** on any
  application checked, and no link out to a store anywhere on the detail page: search,
  dates, constraints and case metadata are all fully scriptable, and the documents are
  simply not published. Record that as `partial` with a `coverage` quirk, not as a
  retrieval failure — and check more than one application before concluding it, since a
  single application legitimately having no documents looks identical.
- **⚠️ The external-DMS variant — documents are not on the portal at all.** A significant
  minority of Idox installs do not serve a documents tab: the tab returns **HTTP 200 with
  a "Permission Denied" body**, or a detail page carries an `externalDocuments` link out
  to a **separate document store on another hostname**. This is the single most expensive
  Idox trap, because the recipe as written *appears to succeed* — a 200, no error, and
  zero files enumerated.
  - **Tell:** the documents tab 200s but lists nothing; or the detail page has an
    `externalDocuments` link; or `n_documents` is non-zero while your enumeration finds
    none.
  - **Shape:** `…/RunThirdPartySearch?FileSystemId=<XX>&FOLDER1_REF=<REF>` returns the
    document rows (often inline JSON), then `…/Document/ViewDocument?id=<Guid>` serves
    each file. **`FileSystemId` is per-authority** — record it in the authority's profile,
    never assume it.
  - **The host and the store vendor are per-authority too**, and the store is not always
    Idox: one install's documents sit behind a **Civica** endpoint on a different host.
    Read `portal.document_host` in the profile before assuming one host serves both.
  - **The hop can be to the council's own website, and the file URLs may not be hrefs.**
    One install's `externalDocuments` tab holds a single link to
    `<council>.gov.uk/…/related-documents?appref=<HUMAN REF>` — keyed by the human
    reference, not the keyVal — and that council page carries each file URL **inside an
    `onclick` `window.open(...)` handler** on a third host, so an href grep finds nothing.
    Parse the `onclick`. Two consequences: a filter that discards council-domain links as
    site chrome will miss the store entirely, and the store host may serve plain curl with
    no session from the register at all.
  - **The store's listing may not be in the HTML.** One store (AniteIM WebSearch, reached
    as `ExternalEntryPoint.aspx?…&FOLDER1_REF=<n>` → `RunThirdPartySearch?FileSystemId=<XX>`)
    returns HTTP 200 and a real page whose **document rows arrive over a SignalR hub** and
    render client-side. A plain client enumerates zero documents from a page that looks
    perfectly healthy. Do not reverse-engineer the hub: record it and hand over the link.
    **This store recurs, and its app path varies** — seen as `/AniteIM.WebSearch/` at one
    council and `/PublicAccess_LIVE/` at another, where the string "AniteIM" appears nowhere
    in the markup. Detect it on the **script set and endpoint** (`jquery.signalR-*`,
    `Views/SearchResult/Index.js`, `dataTables.select.min.js`,
    `SearchResult/RunThirdPartySearch`, a "Documents for reference &lt;n&gt;" title), never
    on the path. `FOLDER1_REF` is also per-install: an **internal folder id** at one council
    (scrape it from the `externalDocuments` tab) and the **human planning reference** at
    another (so the store link is constructible from the reference alone).
  - Do not confuse this with the Northgate/NEC `RunThirdPartySearch` documented later in
    this file — the call shape is similar and the products are different.
- **keyVal is opaque and per-application** — scrape it from the results/detail link;
  you cannot construct it from the reference. **Its format varies by install**: most are
  ~13 uppercase alphanumerics, but several installs use the form
  `_<SITE>_DCAPR_<n>` (e.g. `_GUILD_DCAPR_214647`). A `[A-Z0-9]+` pattern then matches nothing, and a search that
  returned dozens of results reads as having returned none. Match up to the next `&`,
  quote or whitespace instead. (PlanIt often hands it to you in
  `docs_url` / `url` — see the PlanIt shortcuts above.)
- **File-GET gating varies three ways — always send BOTH the session jar and the
  Referer**: *session-gated* (Glasgow, Leeds, Stockport, Highland — a cold GET returns
  an HTML 404 under the `.pdf` name, Referer irrelevant), *Referer-gated* (RBWM,
  Greater Cambridge — 404 without `-e <documents-tab URL>`), or *neither* (York,
  Tendring, East Suffolk, Edinburgh). Consequence: never "optimise away" the
  `search.do` session step when jumping via PlanIt's `docs_url`.
- **Non-PDF attachments lack the `/pdf/` path segment** — grep `/files/{hex}/` without
  anchoring on `/pdf/`, verify magic bytes per file, and reconcile the link count
  against the **documents tab's own row count** (this is what catches silent misses).
  Reconcile **file sizes** as well: Idox installs under load have been seen returning the
  rate-limit page as a valid ~1KB PDF, which passes the magic-byte check on every file.
  PlanIt `n_documents`, when you have it, is a secondary check only — it can lag
  (Highland 8 vs 9 real; Dudley 20 vs 22) so treat it as a lower bound, and note PlanIt
  omits `docs_url` entirely on applications it has seen zero documents for.
- **Session ~30 min idle timeout**; refresh (`search.do`) on long crawls.
- **The search-result metadata separator varies by install.** Most use `·` (U+00B7), some
  use `|`. A parser keyed on the wrong one gets each reference with its received and
  validated dates still attached, which silently defeats any filter on the type suffix.
  Split on the `<span class="divider">` element around the separator, not on a fixed
  character, and check that the references you extract look like references.
- **The advanced search form's date fields vary.** Some installs offer no received-date
  field, only validated. Read the `date(…)` field names from the form before posting. An
  unknown field is ignored and the search comes back as if unfiltered or empty.
- **Pace requests ~1–2s** — small council servers throw transient `000`/`500` on bursts.
- **Slow pacing can outlast the server's keep-alive.** A script that holds a persistent
  connection (a Python `requests.Session`, for instance) and waits several seconds between
  calls can find the server has closed it, and fails with "Remote end closed connection
  without response". That is a client-side artefact, not a block. Send
  `Connection: close` or open a fresh connection per request, and keep the cookie jar.
  Separate `curl` invocations, as in the recipe above, are unaffected.
- **WAF minority** — most Idox sites take plain curl; a few are behind Cloudflare
  (pass with the real browser UA above) and a rare few behind an *enforcing* Barracuda
  (browser-only, like Civica — see Recipe B). **Barracuda cookies ≠ blocked**: East
  Suffolk sets `BNIS_`/`BNES_` cookies in passive mode and plain curl works fine — the
  actionable signal is an actual served JS challenge or `Blocked` page, not BN* cookies.
- **recaptcha markup ≠ CAPTCHA enforced** — Idox comment/copy-request widgets carry
  recaptcha classes; search and downloads are unaffected. **The exception is an install
  that runs reCAPTCHA v3 on the search and downloads themselves.** There a scripted
  search or file GET returns 403 or "Permission Denied", even though the documents tab
  still lists the files. That is enforcement: stop, and hand over the documents-tab link.
- **The advanced *address* search needs `caseAddressType` as well as `_csrf`** — posting
  `searchCriteria.address` to `advancedSearchResults.do` with a freshly-scraped, valid
  `_csrf` still returns "No results found" unless `caseAddressType=Application` rides
  along. This is the same silent-zero failure mode as a stale `_csrf`, from a different
  cause, so a zero on an address search is never evidence the site has no applications
  until you have re-run it with both fields. (Isolated at Cheltenham, alternating
  with/without on fresh cookie jars.) Page results with
  `pagedSearchResults.do?action=page&searchCriteria.page=N`.
- **An application can be *withdrawn from public view* while its `keyVal` still
  resolves** — the deep link returns **HTTP 200**, not a 404, carrying "This application
  is no longer available for viewing. It may have been removed or restricted from public
  viewing." The case then disappears from simple search, advanced search *and* the
  weekly/monthly lists together, so no portal route recovers it. Detect it on the string,
  not the status code, and **report it as removed rather than as a retrieval failure** —
  they are different findings for the user. A national aggregator (PlanIt) that scraped
  the case before removal keeps the reference, description, dates, `keyVal` and
  `n_documents`; that metadata is recoverable, the documents are not.
- **⚠️ A single "No results found" is not evidence of absence.** An advanced search
  (proposal text, parent reference, address) can return a normal-looking empty results
  page on a session that has gone stale, while the same search on a fresh session returns
  real results. It has been seen on more than one install, and it looks exactly like a
  genuine empty result.
  Before recording that nothing matched:
  1. start a fresh cookie jar and a fresh `_csrf`;
  2. run the same search once more;
  3. if it is still empty, run a date-only control search on that session and confirm it
     does return results.
  Only an empty result that survives all three is a finding.

  **Vary the date window before you conclude anything, in both directions.** The result set
  is capped, so the same window is wrong at both ends of the size range: a one-month
  validated-date window returns **"Too many results found"** on a large authority and a
  normal empty page on a small one. And an empty *recent* window can be genuine while the
  portal is entirely healthy — at one install, three separate windows in the most recent
  quarter returned "No results found" while a window fifteen months earlier returned a full
  page of results, documents and a verified download. So: on "too many", narrow; on empty,
  widen **and** step back to an older period before recording anything about the portal.
- **The weekly/monthly lists are a second route onto a case** —
  `search.do?action=weeklyList` takes a `week` value in the portal's own display format
  (e.g. `29 Jun 2026`) plus optional parish/ward codes, and lists EIA screening and other
  non-application case types alongside applications. Useful as an independent check that a
  case really is absent rather than merely unmatched by your search terms.

---

## Recipe D — Northgate (two distinct products)

### D1 · SwiftLG APAS (`/swiftlg/apas/run/`) — ⚠ dying fast

Oracle-backed register, plain curl + cookie jar, no bot protection — **but presume any
historic SwiftLG council has migrated** (3 of 4 tested had: Mole Valley → StatMap;
Dudley, Snowdonia, Pembrokeshire → Agile). Confirm the portal still answers on
`/swiftlg/apas/run/` via PlanIt before applying this. Validated end-to-end at
Warwickshire; the whole chain is **stateless** (works cold, no cookies/CSRF/Referer).

- **Search**: POST `WPHAPPCRITERIA` with `APNID.MAINBODY.WPACIS.1=<ref>` and
  `SEARCHBUTTON.MAINBODY.WPACIS.1=<any non-empty value>` — the SEARCHBUTTON param
  **must be present** (omitting it returns a 110-byte stub); other fields omittable.
  Results render **inline in the POST response** (`WPHAPPSEARCHRES.displayResultsURL`
  is only the re-display/pagination URL). To find refs without PlanIt (which can't
  resolve county councils): date-sweep with `REGFROMDATE`/`REGTODATE.MAINBODY.WPACIS.1`
  (`dd/mm/yyyy`).
- **Detail**: `GET WPHAPPDETAIL.DisplayUrl?theApnID=<REF>` (`theApnID` is literally the
  reference, slashes unencoded). **Do NOT tab-hunt with `theTabNo`** — skinned installs
  render all tabs in one page and non-1 values throw `WCHINTERROR`; fetch with
  `theTabNo=1` (or omit) and grep the whole page for document links.
- **Documents**: hrefs are `<SKIN>DISPLAYMEDIA.showImage?theSeqNo=<n>&theApnkey=<key>&theModule=1`
  (the handler prefix is per-council skin — `WCH` at Warwickshire vs the generic `WPH`).
  This returns a **72-byte meta-refresh stub**, which `curl -L` does *not* follow —
  parse `URL=../MediaTemp/{apnkey}-{seqno}.pdf` out of it, then `GET` that with `-L`
  (it 302s to `/swiftlg/MediaTemp/…`) to get the PDF. **The stub request is what creates
  the MediaTemp file**, so it cannot be skipped. A direct GET of a constructed MediaTemp
  URL returns a small HTML "not available" page (under 1 KB), even though the name ends
  `.pdf`.
- **The base path is not always `/swiftlg/`.** `/swift/` has been seen too, and the Oracle
  paths under it are unchanged. Take it from the council's link or PlanIt's
  `planning_url`.

### D2 · Planning Explorer (`/Northgate/PlanningExplorer/`)

Classic ASP.NET WebForms — round-trip `__VIEWSTATE`, `__VIEWSTATEGENERATOR` **and**
`__EVENTVALIDATION` (all three), same cookie jar (`ASP.NET_SessionId`).

- GET `GeneralSearch.aspx`, capture the three hidden tokens (VIEWSTATE can be
  ~96–115 KB — build the POST body with a script, not shell args).
- **Reference lookup: POST the MINIMAL field set** — the three tokens +
  `txtApplicationNumber=<ref>` + `csbtnSearch=Search` (`rbGroup` optional). Every extra
  empty field is WAF-bait: Runnymede's origin WAF 403s any POST containing an empty
  `cboSelectDateValue`. (The `txtProposal` + date-range route is for proposal/date
  sweeps, not reference lookups.)
- Search 302s to `Generic/StdResults.aspx?...&PS=10&XMLLoc=/…/XMLtemp/<session>/<guid>.xml`.
  **Robust `PARAM0` source: skip `StdResults` entirely** — take `XMLLoc` from the 302
  `Location` header and GET that XML directly (same cookie jar); `<PK>` in it *is*
  `PARAM0`. This works even where `StdResults` is WAF-blocked (Runnymede 403s it
  wholesale) and is cleaner than scraping results HTML. Caveat: the `Location` header
  can contain **raw spaces** — percent-encode it yourself; don't rely on `curl -L`.
- Detail page on skinned sites is `Generic/StdDetails.aspx?…&TYPE=PL/PlanningPK.xml&PARAM0=<id>&XSLT=…`
  (the opaque key is **`PARAM0`**, not `keyVal`). Keep slashes literal in the
  `TYPE`/`XSLT`/`XMLSIDE` params — required at Wandsworth (`%2F` → 500), harmless at
  Runnymede. Detail hrefs carry literal CRLF/tabs — strip whitespace.
- **The documents module varies per authority** — both councils examined replaced the
  standard Northgate one, differently, and both work **cold** (no prior session needed
  if you have the ref):
  - *Wandsworth*: bespoke cross-host IAM — `planning2` host, `comments.aspx?case=<ref>`,
    WebForms category-expand postbacks, then `IAM/IAMLink.aspx?docid=<n>` → 302 → PDF.
  - *Runnymede*: NEC "Public Access" MVC on a `docs.<council>` host (a naming collision
    — **not** Idox) — `…/PublicAccess_LIVE/SearchResult/RunThirdPartySearch?FileSystemId=PL&FOLDER1_REF=<ref>`
    (constructible from the ref); the doc list is embedded in the HTML as
    `var model = {…Rows:[{Guid,Doc_Type,Date_Received,Doc_Ref2}]}`; download
    `GET …/Document/ViewDocument?id=<Guid>` (param must be `id` — check Content-Type).
  - *Camden*: **HP TRIM / Content Manager "CMWebDrawer"** on a `camdocs.<council>` host —
    fully constructible from the ref, stateless:
    `GET /CMWebDrawer/PlanRec?q=recContainer:%22<enc-ref>%22&format=json` (ServiceStack
    JSON: `Results[].Uri`, `RecordTitle`, `TotalResults`/`HasMoreItems`, `&pageSize=`
    honoured) then `GET /CMWebDrawer/Record/<Uri>/file/document?inline` → PDF. The
    HTML view double-lists each doc — dedupe on record id. The `&format=json` trick
    likely generalises to any TRIM WebDrawer council.

  PlanIt's `docs_url` points at whichever module a council uses — record it per council.
- WAF: Cloudflare has **three modes** on PE sites: absent (Wandsworth), **passive**
  (Runnymede — any UA passes; the old "empty/default UA gets 403" claim did not
  reproduce), and **score/rate-based enforcing** (Camden's register: the first ~2 curl
  requests reach origin, then *everything* — including previously-working URLs — gets
  the interactive challenge). On a score-based site, grab what you need in the first
  requests; "worked a minute ago, 403 now" = escalation, don't burn retries. Watch also
  for an *origin* WAF with narrow triggers (Runnymede's `StdResults`/
  `cboSelectDateValue` blocks above).
- NEC's `Redirection/redirect.aspx` deep links (PlanIt `url` for some PE councils)
  redirect via a **JavaScript stub, not a 302** — parse `document.location.href` out of
  the body; `curl -L` won't follow.
- **NB migration:** the PE fleet is dying but its successors are **diverse** —
  Birmingham → NEC Assure (Recipe H), Merton → Tascomi (browser-only), Stockport →
  Idox (Recipe C), Camden → cosmetically NEC (`/NECSWS/` paths) but still PE
  underneath. Re-detect the vendor per council; don't assume NEC.

---

## Recipe E — Ocella (`/OcellaWeb/planningSearch`)

Niche, plain server-rendered pages, and **completely stateless** — no session, CSRF,
keyVal, or Referer required anywhere (keep a jar + browser UA + pacing as hygiene).
`$BASE` = e.g. `https://www1.arun.gov.uk/aplanning/OcellaWeb`.

1. **Shortcut** — with an exact reference, skip search entirely:
   `GET $BASE/planningDetails?reference=<REF>&from=planningSearch` (raw ref *with*
   slashes works as-is). PlanIt's applics `url` field for Ocella councils **is** this
   deep link ready-made.
2. Otherwise `POST $BASE/planningSearch` with `reference=<REF>&action=Search`
   (other fields may be empty). **Exact reference only** — broad searches (e.g.
   location-only) silently re-render the empty form with no error. Extract detail
   links: `grep -oE 'planningDetails\?reference=[^"]*'`. Quirk: the postcode field is
   dotted (`OcellaPlanningSearch.postcode`); form dates are `dd-mm-yy` (8 chars).
3. Documents list: `GET $BASE/showDocuments?reference=<REF>&module=pl` (the detail
   page presents this as a POST form, but plain GET works; optional `&filterBy=TYPE`).
   Each row carries category, date (`dd-mm-yy`) and description — use them to label files.
4. Download: `GET` each `viewDocument?file=…&module=pl` href **verbatim from
   showDocuments** (don't construct: `file` is a URL-encoded server-side Windows path,
   `dv_pl_files%5C<REF-with-underscores>%5C<filename>`, spaces as `+`). Verify `%PDF-`.

Arun also injects a *passive* Barracuda fingerprint script (`bnith__`/`x-bni-*`
cookies) that never blocked anything — same lesson as East Suffolk: only an actual
`Blocked` page means blocked.

Ocella gotchas:
- **Grep tolerance**: skinned installs emit non-canonical attribute spacing —
  Hillingdon writes `href ="viewDocument?…"` (space before `=`), so `grep 'href="'`
  silently finds zero links. Match the endpoint name (`viewDocument\?file=`) or use
  `href *=` — a lesson that applies to every server-rendered recipe.
- **The documents module can be outsourced** (Great Yarmouth): `showDocuments` returns
  an **empty 200 page** (no error) while search/detail stay Ocella — documents moved to
  a Civica Portal360 host (reference-keyed Recipe B, RefType `PLANNINGCASE`). Before
  trusting `showDocuments`, check the detail page for a "View Documents" button opening
  another host (`window.open`), and check whether PlanIt's `docs_url` points off-host —
  that's the automatic tell. Same pattern class as PE's per-council doc modules and
  Agile's DMS switch.
- PlanIt shortcuts: `url` = ready `planningDetails` deep link **and**
  `other_fields.docs_url` = ready `showDocuments` link — both steps skippable. The
  applics `reference` field can be null (ref lives in `uid`).

## Recipe F — StatMap horizoNext / "Mirage"

Newer vendor appearing where SwiftLG sites retire. Detect: hostname
`*-publicportal.statmap.co.uk`, path `/horizonext`, title "StatMap Mirage". React SPA
over an **open JSON API** — no session, cookies, or CSRF. PlanIt labels these
`scraper_type: Custom`. `$API` = `https://<council>-publicportal.statmap.co.uk/horizoNext/api`.

1. Reference → internal id:
   ```bash
   curl -s -A "$UA" -H "Content-Type: application/json" \
     "$API/publicportal/planningApplications/pageRequest" \
     -d '{"pageSize":10,"offset":0,"filter":{"parts":[{"filterItems":[{"columnName":"appRef","operator":"=","value":"MO/2026/01108"}]}]}}'
   # -> {"records":[{"id":"130846","name":"MO/2026/01108",...,"total":1}]}
   ```
   **Only** the `filter.parts[].filterItems[]` shape is honoured — any other filter
   shape is *silently ignored* and returns the entire register (~123k records, ~54 MB):
   always send `pageSize` and check `total` == expected. The reference must be the
   exact zero-padded form (`MO/2026/1108` → 0 hits). PlanIt's applics `url` ends in
   the internal id, which lets you skip this step.
2. (Optional) detail: `GET $API/publicportal/planningApplications/{id}`.
3. Documents: `POST $API/mirage/attachments/P_APPLICATION/{id}` with body `{}` and
   JSON content-type (a bodyless/null POST 400s) → `attachments[]` with
   `id`/`name`/`description` (+ heavy base64 thumbnails; ignore them).
4. Download is **two hops**: `GET $API/mirage/attachments/download/{attId}` returns
   JSON `{fileName, url}` where `url` is on a *different* base path
   (`/publicportal-horizonService/attachments/{attId}/download`); GET that url = the
   PDF. (`/show` variant = inline view.)
5. SPA deep links (`…/horizoNext/publicportal/planningapplications/<id>`) 404 to
   direct GET — scrape via the API only.

## Recipe G — Agile Applications "Citizen Portal"

The other common SwiftLG successor. Detect: host
`planning.agileapplications.co.uk/<slug>/`, title "Citizen Portal Planning",
`*.sunagile.com` CSP; PlanIt `scraper_type: Agile`. SPA over a shared multi-tenant
**open JSON API** — no cookies/session/CSRF; the tenant is selected by an `x-client`
header. **Warning:** the portal host returns the 2.5 KB SPA shell with HTTP 200 for
*every* path (including fake `/api/*`) — never probe it for data; the API is a separate
host.

```bash
API="https://planningapi.agileapplications.co.uk"
# Resolve the client CODE (NOT always the URL slug — pcnpa -> PEMBROKESHIRECOAST):
CODE=$(curl -s -A "$UA" "https://identity.agileapplications.co.uk/api/client/get?url=snowdonia" \
  | grep -oE '"code":"[^"]*"' | head -1 | cut -d'"' -f4)
H=(-H "x-client: $CODE" -H "x-service: PA" -H "x-product: CITIZENPORTAL")   # all three required

# 1. ref -> internal id (or take it from PlanIt applics url tail and skip)
curl -s -A "$UA" "${H[@]}" "$API/api/application/search?reference=NP5%2F50%2F12N"   # -> results[].id
# 2. detail + 3. document list
curl -s -A "$UA" "${H[@]}" "$API/api/application/20774/document"   # -> [{documentHash,name,description,...}]
# 4. download — path-form needs NO headers (hash is self-authorizing)
curl -s -A "$UA" "$API/api/application/document/$CODE/<documentHash>" -o form.pdf
```

- Missing any of the three headers → `401 "Client has not beeing selected"` (sic);
  `x-service` must be `PA` (not `PLANNING`).
- **Per-tenant `DMS` switch** (from `GET identity…/api/service/configuration`, key
  `DMS`): `SHAREPOINT` or `LOCAL` → documents via the API above, **even where the
  configuration also carries a `DMS_URL`**. Only an external `DMS` setting uses it. `EXTERNAL`/`IAW` → the documents
  tab is just an **iframe of `DMS_URL + <ref>`** pointing at a *council-hosted* DMS
  (Pembrokeshire → NEC PublicAccess `RunThirdPartySearch`, same product as Runnymede's
  doc host). PlanIt's `docs_url` is that iframe link pre-built.
- Outage signature (don't misread as a block): `500` on every data call while
  `/api/system/checkserver` 200s and the external DMS host is TCP-dead = council
  backend down; retest later.

## Recipe H — NEC Assure "ES"

Where Northgate PE fleets are migrating (NEC Software Solutions = ex-Northgate). Detect:
path `/NECSWS/ES/Presentation/Planning/OnlinePlanning/`, `AssureLogo` branding,
ASP.NET MVC + AJAX. PlanIt may **stalely** report `PlanningExplorer` — trust its
`planning_url`, not the label. Everything keys off the **human reference**
(URL-encoded, slashes → `%2F`); the internal key is never needed. Docs/downloads work
cold (stateless).

1. Deep link (skip search): `GET …/OnlinePlanning/OnlinePlanningOverview?applicationNumber=<enc-ref>`
   (PlanIt `url`/`docs_url` are exactly this).
2. Docs list: `POST …/OnlinePlanning/GetOnlineDocuments?applicationNumber=<enc-ref>&currentPageIndex=0&IsDatePublishSortedDescending=true&pageSize=200`
   (params in the query string, empty body). **`currentPageIndex` is 0-based** — index
   `1` returns the correct total but *zero rows* ("No record(s) found"), a silent trap.
3. Download: `GET …/OnlineDisplayDocument/DisplaySearchDocument/<name>?applicationNumber=<enc-ref>&FileName=<name>&fileType=.pdf&aspectGuid=<32-hex>`
   — scrape hrefs verbatim (un-escape `&amp;`); `aspectGuid` is per-document, not
   constructible. (Bulk zip: `POST …/OnlineDisplayDocument/DownloadDocumentImages`.)

Search without a deep link is fussy (needs the full ~71-field jQuery-serialized form);
prefer the PlanIt deep link.

## Recipe I — TerraQuest "Planning Portal 2" (covers all 11 NI authorities)

One register covers **all of Northern Ireland** (`planningregister.planningsystemni.gov.uk`,
since Dec 2022; the `LA01`–`LA11` ref prefix identifies the council, `LA04`=Belfast).
Generic detection for any PP2 site: Next.js shell + a `/__ENV.js` runtime-config file
whose API is on `*.tqinfra.co.uk`. Open JSON API, anonymous, no cookies/WAF — but with
two novel traps.

```bash
BASE="https://planningregister.planningsystemni.gov.uk"
ENVJS=$(curl -s -A "$UA" "$BASE/__ENV.js")                 # ALWAYS fetch this first
API=$(echo "$ENVJS"   | grep -oE '"NEXT_APP_PLANNING_REGISTER_API":"[^"]*"' | cut -d'"' -f4)
TENANT=$(echo "$ENVJS"| grep -oE '"NEXT_APP_PP_TENANT_ID":"[^"]*"'          | cut -d'"' -f4)
T=(-H "TQ-Tenant: $TENANT")   # MANDATORY on every API call

# 1. ref -> applicationId (or take the id from PlanIt applics url tail and skip)
curl -s -A "$UA" "${T[@]}" --get "$API/applications" \
  --data-urlencode "SearchTerm=LA04/2026/1407/F" --data-urlencode "SearchStatus=0" \
  --data-urlencode "PageNumber=1" --data-urlencode "PageSize=10"   # -> applications.items[].applicationId
# 2. detail INCLUDES the document list (supportingDocuments[])
curl -s -A "$UA" "${T[@]}" "$API/application/711859"
# 3. per document: resolve the SAS url and download IMMEDIATELY (expires ~5 min)
URI=$(curl -s -A "$UA" "${T[@]}" "$API/application/711859/6290101" | grep -oE '"documentUri":"[^"]*"' | cut -d'"' -f4)
curl -s -A "$UA" "$URI" -o form.pdf   # Azure Blob SAS — no headers needed on the blob GET
```

- **Trap 1 — silent tenant failure:** a missing/wrong `TQ-Tenant` header does *not*
  error; search returns empty `items[]` and detail returns literal `null`,
  indistinguishable from "not found". Always re-read the GUID from `/__ENV.js`.
- **Trap 2 — SAS expiry:** `documentUri` is a ~5-minute Azure Blob SAS URL; resolve and
  download one document at a time, never batch-collect URIs first.
- `SearchStatus` must be the **integer** `0`/`1`/`2` (string `"All"` is rejected).
  Docs are **not all PDFs** (.docx common) — verify magic bytes per file.

## Recipe J — Idox "Publisher" document host (pairs with bespoke registers)

Detect: a separate documents host (e.g. `d0cs.<council>.gov.uk`) serving
`/Publisher/mvc/listDocuments?identifier=<module>&ref=<key>`, with `/publisher/idoxui/`
CSS and a "Document List" title. This is a **documents module, not a full portal** — the
register itself can be something else entirely (Colchester pairs it with a bespoke
Dynamics-based viewer at `www.colchester.gov.uk/wampd/?id=<ref>`). Same pattern class as
Planning Explorer's per-council doc modules and Ocella's outsourced doc hosts: find the
docs host from the detail page's documents link, or PlanIt's `docs_url` (pre-built).

Colchester specifics (validated end-to-end Aug 2026): the **human reference is the key
everywhere** — a bare 6-digit application number (e.g. `261486`) is simultaneously the
application number, the `wampd` detail id, and the Publisher `ref`. `identifier=DC` is the
planning module. The detail page renders its field values by script, so scrape nothing
from it — go straight to the docs host.

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
BASE="https://d0cs.colchester.gov.uk"
REF="261486"

# 1. listDocuments establishes BOTH the session and the document context
curl -s -c cj.txt -A "$UA" "$BASE/Publisher/mvc/listDocuments?identifier=DC&ref=$REF" -o list.html

# 2. Same jar -> JSON rows: [Type, Date, Description, viewPath, measurePath]
curl -s -b cj.txt -c cj.txt -A "$UA" "$BASE/publisher/mvc/getDocumentList" -o docs.json

# 3. Download each viewPath with the SAME jar. Label from Type+Description+Date.
grep -oE '"/docs/[A-F0-9]+/[^"]+"' docs.json | tr -d '"' | while read -r p; do
  name=$(basename "$p")
  curl -s -b cj.txt -A "$UA" "$BASE/publisher$p" -o "$name"
  sleep 2
done
```

Publisher gotchas:
- **Downloads are session-gated** — a cold GET of a `/publisher/docs/…` URL returns a 404
  JS/error page under the `.pdf` name. Keep one jar from step 1 through every download,
  and verify magic bytes per file.
- The page's own AJAX URL embeds `;jsessionid=…` — unnecessary when you carry the cookie
  jar; call the plain endpoint.
- **Completeness count**: `data` array length in the `getDocumentList` JSON is the
  portal's own document count; a non-null `serviceError` field is an error, not an empty
  set — distinguish the two.
- Path case is inconsistent as served (`/Publisher/mvc/listDocuments` entry point,
  `/publisher/…` everywhere else) — copy paths verbatim, don't normalise.
- The fifth column is an OMT "measure document" viewer link — ignore it.
- The page arms a session-idle timer — on long pulls, re-hit `listDocuments` to refresh.

## Arcus (Salesforce) — browser-only; hand the user a deep link

Public registers on Arcus are Salesforce Experience Cloud (Lightning) SPAs on
`*.my.site.com`/`*.force.com` or a council CNAME (`Server: sfdcedge`). There is **no
supported public API** for the register data: search, detail, and document listings run
through the Arcus managed package's custom Salesforce controllers, which are not exposed
to an anonymous HTTP client the way the open-API vendors are. Plain curl gets a
JavaScript app shell, not data.

**Do not try to reverse-engineer or replay the managed-package internals.** For Arcus
councils, the right outcome is to **hand the user a browser deep link** and let the
official site render it:

- PlanIt's applics `url` is the record deep link `…/pr/s/detail/<18-char-recordId>`;
- or the register landing `…/pr/s/register-view?c__r=Arcus_BE_Public_Register` (no known
  parameter to pre-fill a search).

PlanIt is unreliable for Arcus (it can mislabel `scraper_type` and carries no
`docs_url`/`n_documents`), but its `url` field is a good deep link. Known Arcus councils
include Manchester, Haringey, Bromley, Wiltshire, Anglesey, Powys, Ashford, and Salford.

---

## Committee papers — the committee system, not the portal

**For a committee-determined application, the planning portal is often not where the
committee's papers are.** Many councils publish the committee report, the update or
late-material sheet and the minutes on their committee-management system instead. The
portal's documents tab then carries the application documents and the decision notice, but
nothing showing what the committee was told or what it changed.

This is a silent failure. A retrieval that stops at the portal reports "no officer report"
when one exists, and nothing in the portal's response suggests otherwise.

- **Check the profile first.** `portal.committee_papers` names the committee system, its
  host and the planning committee id(s). Where it is set, go there for committee papers.
- **Where it is not set, check anyway** before recording a committee report as missing.
  The council website's "councillors and committees" or "meetings" page links to the system.
- **Record what you find** in the profile's `portal.committee_papers`, so the next run
  starts there.

Delegated decisions are different. A delegated officer report is normally on the portal
if it is published at all. The committee system holds only what went to committee.

### Modern.gov

A widely used committee system, and the one behind every case recorded so far. Detect it by `ieListMeetings.aspx`,
`ieListDocuments.aspx` and `mgCommitteeDetails.aspx` pages, a "Modern Council" or
council-branded title, and document links under `documents/`. Hosts vary, often
`moderngov.<council>.gov.uk`, `democracy.<council>.gov.uk` or
`<council>.moderngov.co.uk`. Pages are plain server-rendered HTML with no session, token
or cookie needed.

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
MG="https://moderngov.<council>.gov.uk"    # from portal.committee_papers.url
CID=138                                    # the planning committee id, from the profile

# 0. No committee id on file? The web service lists every committee with its id.
curl -s -A "$UA" "$MG/mgWebService.asmx/GetCommittees" \
  | grep -oE '<committeeid>[0-9]+</committeeid>|<committeetitle>[^<]*' | paste - - | grep -i plan

# 1. Meetings for a year -> each meeting's agenda link (ieListDocuments … MId=<n>)
curl -s -A "$UA" "$MG/ieListMeetings.aspx?CId=$CID&Year=2025" \
  | grep -oE 'ieListDocuments\.aspx\?CId=[0-9]+&amp;MId=[0-9]+' | sed 's/&amp;/\&/' | sort -u

# 2. One meeting's agenda -> its documents (hrefs are relative, spaces unencoded)
curl -s -A "$UA" "$MG/ieListDocuments.aspx?CId=$CID&MId=<MId>" \
  | grep -oE 'href="documents/[^"]+"' | sed 's/^href="//;s/"$//'

# 3. Download each one, percent-encoding the spaces; verify %PDF- AND size/text
#    (magic bytes alone are not enough — see the checklist)
curl -s -A "$UA" "$MG/documents/s<N>/<name%20with%20spaces%20encoded>.pdf" -o report.pdf
```

- **Two kinds of document link.** `documents/s<N>/…` are item-level: the report for an
  agenda item, a late-material pack. `documents/g<N>/…` are meeting-level: the agenda
  frontsheet and the printed minutes. `<N>` is not the meeting id, so scrape the links;
  never construct them.
- **Finding the meeting.** Start from the decision date, or the month or two before it,
  and read the agenda titles on the meetings in that window. The application reference
  usually appears in the agenda item title or in the combined report's contents.
- **Use `ieListMeetings`, not the calendar view.** `mgCalendarMonthView.aspx` has been seen
  to ignore its month and year parameters and show the current month. Both `CId=` and
  `CommitteeId=` are accepted on `ieListMeetings`.
- **A meeting page with no documents** is usually a cancelled meeting, or one whose papers
  are not yet published. It is not a retrieval failure. Move to the next meeting.
- **Committee reports are sometimes better copies.** Where the portal holds an image-only
  scan of a report, the committee system often has a text-layer PDF of the same report.
- **Update sheets and minutes matter most.** They carry the changes made on the night:
  amended conditions, added obligations, a different decision from the recommendation.
  They are the documents least likely to be on the portal.
- The same pacing and responsible-use rules apply. A committee system is a separate host,
  so pace it separately. It is still one council's server.

Other committee systems exist, such as CMIS and council-built pages. The principle is the
same: find the planning committee, find the meeting, fetch the report and the update
material. Record the host in the profile whatever the product.

---

## Reference-number formats (for search / normalisation)

No national standard — each LPA sets its own; feed the **exact original string
(including slashes)** back into a portal. Common shapes:

- `YY/NNNNN/TYPE` — year / serial / type, e.g. `25/01234/FUL`, `26/03301/LBC`
  (most Idox/Northgate).
- `AREA/YYYY/NNNN/TYPE` — leading district digit, e.g. `6/2026/1249/HOUSE`; type
  sometimes dropped: `5/2026/1349`.
- `PREFIX/YY/NNNN/TYPE` — council prefix + year + serial + type, e.g. `DC/26/2860/FUL`
  (East Suffolk).
- `PREFIX/NN/NNNNN` — 2-letter council prefix, e.g. `MO/2011/1449`; StatMap Mole
  Valley now uses `MO/YYYY/NNNNN` with a **zero-padded 5-digit serial**
  (`MO/2026/01108` — the unpadded form gets zero hits).
- `PARISH/NNN/YY/TYPE` — parish prefix with year *third*, e.g. `A/124/26/NMA`,
  `FP/101/26/T` (Ocella/Arun).
- `YYYY/NNNN` — bare year/serial, no type, e.g. `2026/2894` (Wandsworth);
  `YYYY/NNNNN/PA` (Birmingham/NEC).
- `P/YY/NNNN[/TYPE]` — e.g. `P26/0883`, `P26/0896/PNA` (Agile/Dudley).
- `NP<area>/<ward>/<serial><letter>` — Welsh national-park style, no year, e.g.
  `NP5/50/12N` (Snowdonia); `NP/YY/NNNN/TYPE` (Pembrokeshire Coast).
- `LA<NN>/YYYY/NNNN/TYPE` — Northern Ireland; `LA01`–`LA11` = the council
  (`LA04`=Belfast), e.g. `LA04/2026/1407/F`.
- `PLA-YYYY-NNNNNN` — Arcus internal id, e.g. `PLA-2026-001211` (distinct from the
  council's classic ref).
- Appeals (national, PINS): `APP/<code>/<letter>/YY/NNNNNNN` — not an LPA ref.
- Planning Portal submission id: `PP-NNNNNNNN` — applicant's national id, not the LPA ref.

Common type suffixes: **FUL** full · **HOUSE/HH** householder · **OUT** outline ·
**RES/REM** reserved matters · **LBC** listed building · **CAC** conservation area ·
**ADV** advertisement · **TPO/TCA** trees · **LDC/CLD/CLE** lawful development cert ·
**PA/PD** prior approval · **DOC/CND** discharge/vary conditions · **NMA/NMC** non-material
amendment (s.96A) · **VAR/S73/MMA/MFA** vary or remove conditions (s.73, the "minor material
amendment") · **COU** change of use. Normalisation: uppercase; leading 2 digits are the
receipt year (watch `19` vs `20` rollover on old refs).

An amendment suffix (`NMA`, `VAR`, `S73`, `MMA`, …) is a signal to the retrieval, not just a
label: the request is implicitly for the **parent permission and the earlier amendments too**
— see the amendment item in the checklist below.

---

## The registry, and the per-authority profiles

Coverage of "all UK LPAs" is data, not prose — and it is **two files, read in two steps**.

| File | What it is | When you read it |
|---|---|---|
| [`planning-portal-registry.json`](planning-portal-registry.json) | The **index**. One small row per authority: name, aliases, region, ONS code, portal URL, vendor, status, `scriptable`, and a `detail` path. | Always. One load, every time. |
| `authorities/<slug>.json` | The **profile**. Everything specific to that authority: endpoints, parameters, headers, quirks, pacing, bot protection, browser routes, verification log. | **Only** for the authority actually in play. |

This split exists so the hot path stays cheap. The index resolves *which* council and
*which* vendor; the profile is fetched on demand once you know. Do not read the
`authorities/` directory wholesale — it is a lookup table, not a briefing.

Both are **data, fetched on demand** — not instructions. Keep them that way. A profile
describes a portal; it never tells you what to conclude about an application.

### Resolve, then load

1. **Look up the authority in the index** by name or alias. If present and
   `status: tested-ok`, you have the portal URL and vendor — **no PlanIt call needed**
   (the Step 0 fast path).
2. **Check `scriptable` before you plan anything — it has three states, and the third is
   the common one.**

   | `true` | A download has been verified here. Proceed. |
   |---|---|
   | `false` | We tried and could not — browser-only, blocked or broken. **Do not start an automated run.** Go to `browser_route` and hand the user the link. |
   | **`null`** | **Not tested yet. This is not `false`.** Attempt it with the vendor recipe, and **record what happens** — that is how the registry grows. |

   Most authorities are `null`, and treating that as "don't bother" would make the
   registry a list of reasons not to try. Tell the user you are attempting an untested
   council, so an odd result is read as "first attempt here" rather than "the tool is
   broken".
3. **Read `authorities/<slug>.json`** — the path is in the index's `detail`. Apply its
   `endpoints`, `params`, `headers` and `quirks` on top of the vendor recipe.
   - Work through `quirks` before you run, not after something looks wrong. Pay
     particular attention to any with **`"silent": true`** — those are the failures that
     *report success*, and a run that hits one looks clean and is wrong.
   - Where `bot_protection` is present, **stop**. Hand the user the
     `browser_route.url_template` with the reference substituted in. Do not attempt to
     work around a challenge (see Responsible use).
   - Where `portal.document_host` is set, the documents are on a **different system**
     from the search portal — read it before assuming one host serves both.
   - Where `portal.committee_papers` is set, committee reports, update sheets and minutes
     are on the council's **committee system**. For a committee decision, fetch them from
     there (see "Committee papers" above).
4. **If the council is not in the index at all**, this is a normal case, not a failure —
   the index holds a few hundred authorities and the UK has more. Resolve it:
   - **PlanIt's areas API** (`?area_type=planning&auths=<name>`) for `planning_url` and a
     `scraper_type` hint — pace it, it is volunteer-run;
   - failing that, the council's own site → "view / track planning applications".
   - **Fingerprint the vendor from the markup**, using `vendors.json`. Do not trust
     PlanIt's `scraper_type`, and **never infer a vendor from a hostname** — councils
     migrate products and keep the host, so `publicaccess.<council>.gov.uk` has been
     found running both Arcus and Tascomi.
   - **Sanity-check the URL you were given is a register base**, not a search form, a
     disclaimer gate or a deep link. Directories publish whichever page they indexed, and
     the recipes append paths to it.
   - Then apply that vendor's recipe, tell the user this council was not on file, and
     write a profile from what you learn.
5. **Record the result back.** Add or update the index row, and write a profile in
   `authorities/`. This is how coverage compounds — every tested council makes the next
   one in the same vendor family cheaper.

### What belongs where — three kinds, three homes

The single rule that keeps these files small and honest. Before writing anything down,
ask which of the three it is:

1. **True of the vendor** — every Idox install, every Atrium install. → **A recipe in this
   file**, written once. Never copy it into a profile; that is how a recipe silently forks
   into forty divergent copies.
2. **True of this authority's portal** — its hostname, its `FileSystemId`, a header this
   install needs, a parser trap in its metadata, its rate limit. → **the profile**.
3. **About which applications count as this council's own decisions** — reference prefixes
   in and out, type suffixes, adjoining-authority consultations decided elsewhere,
   application-type filters. → **not retrieval at all.** It is cohort-scoping judgement.
   It sits in the profile's `cohort_scope` key, quarantined and ignored by retrieval, until
   the skill that should own it exists. Do not let it leak into `retrieval`.

### The profile schema

`authorities/_schema.json` is the contract, and every field carries a description saying
what it is for. Two fields deserve naming here because they are what makes these files
useful outside this skill:

- **`scriptable`** — the boolean an external caller branches on.
- **`ons_code`** — the GSS code, which joins a profile to the LPA datasets and to
  `planning.data.gov.uk`. Null where it does not apply: national parks, joint services,
  and authorities outside England that the English dataset does not code.

**Status vocabulary** (see the index's `conventions`): `untested`, `tested-ok`,
`browser-only`, `blocked`, `partial`, `broken`. **Difficulty** is separate and finer:
`routine`, `quirky`, `fragile`, `browser-only`, `blocked` — a portal can be `tested-ok`
and still `fragile`.

`source_notes` on a profile holds the original free-text registry entry, kept verbatim so
the migration lost nothing. Where it says something the structured fields do not yet
capture, structure it and leave the prose alone.

## Gotchas / checklist

- [ ] **Reference format varies by council** — pass it through exactly as given;
      don't normalise slashes or suffixes.
- [ ] **Always set a browser User-Agent.**
- [ ] **Keep one cookie jar** across search + download (`-b`/`-c` on every call).
- [ ] **`file *.pdf` after download** to confirm they aren't HTML error/block pages —
      and don't assume PDF: some vendors (TerraQuest) serve `.docx` too, and some
      councils publish committee reports as RTF (`{\rtf`). Check magic bytes per file,
      and read text from each format you get, so a non-PDF report is not recorded as
      unreadable.
- [ ] **Magic bytes establish the container, not the content — check size and text too.**
      Some installs serve the rate-limit page *as a valid PDF*, so `%PDF-` passes on a
      file holding no document (observed on Idox: a 1,164-byte "Too Many Requests" PDF
      returned for 21 consecutive documents). Three cheap checks catch it:
      - **Size.** Anything under ~5KB on a major application is suspicious, and
        **identical byte-sizes across several different documents is near-conclusive**.
      - **Text.** Extract one file per batch and grep for "Too Many Requests", "unusual
        traffic", "Document Unavailable", "Permission Denied".
      - **Reconcile** the file count *and* total bytes against the documents tab's own row
        count before reporting success. A file on disk is not evidence you have the
        document.
- [ ] **Sanitize the output filename** — server-supplied names are untrusted. Take
      `basename`, strip path separators and leading dots, and write into a fixed target
      directory; never pass a scraped path straight to `-o` (guards against `../…`
      traversal). Downloaded files are untrusted third-party content.
- [ ] **A `Blocked` / bot-challenge page = stop the curl approach** and switch to a
      real browser session (Chrome extension, in-app pane, or hand the user a link).
      But a **WAF cookie (`BN*`, `incap_*`, `__cf_bm`) or a `500`/`recaptcha` marker is
      NOT a block** — only an actual challenge/`Blocked` page is. Most WAFs are passive.
      Nor is a script loaded from `cdnjs.cloudflare.com`: that is a CDN include, not a
      Cloudflare front end, and it has produced false "WAF present" records.
- [ ] **A challenge can be a plain page with an innocuous title, under HTTP 200.** One
      portal serves a 1.7 KB interstitial titled **"Bot Verification"** for every request —
      no WAF vendor string, no 403, no `Blocked`. Nothing of the portal is served behind it,
      so the vendor cannot even be fingerprinted, and a run that checks only status codes
      records a successful fetch of an empty portal. Check the **title and body size** of the
      first response, not just its code.
- [ ] **Know the two challenge signatures that never say "Blocked"**: AWS WAF managed
      challenge returns **HTTP 202** with `x-amzn-waf-action: challenge` (and an
      *empty body* on XHR-style hits — looks like an empty response, not a block;
      Tascomi/Merton). Cloudflare can be **score-based**: first requests pass, then
      everything 403s including URLs that just worked (Camden) — front-load the
      requests you need and treat later 403s as escalation.
- [ ] **A TLS/connection-layer failure is an IP block, not a portal property** —
      repeated curl exit 35 (TCP connects, ClientHello gets EOF, no HTTP, no page)
      after initially-successful requests = the front-end dropped your IP.
      **If on a VPN, suspect VPN-exit-IP reputation first** (Swansea and Highland
      NetScalers did exactly this to a NordVPN IP and recovered instantly off-VPN);
      retest from a residential IP before recording the council as hostile.
- [ ] **Completeness cross-check — count the documents the portal itself reports, and
      confirm your enumerated links match.** This is the check that catches silent
      scraping misses (wrong grep, skinned `href ="` markup, outsourced doc modules
      serving empty 200 pages). Get the expected count **from the portal, not PlanIt**:
      most documents pages state a total or render one row per document (count the rows),
      and the open-API vendors return a `RowCount`/`total`/`TotalResults` field. Use
      PlanIt's `n_documents` only as a secondary check when you happen to have it (and
      treat it as a lower bound — it can lag, e.g. Highland 8 vs 9, Dudley 20 vs 22). If
      the counts disagree, you are missing files — widen the grep and re-enumerate.
- [ ] **When the portal is a JS/SPA shell, find its runtime-config** (`/__ENV.js`,
      `config.js`, app bundle) for the real API host, tenant id, and any required
      header — and never probe the SPA host for data (it may 200 with an empty shell
      on every path).
- [ ] **Watch for silent failures on the open-API vendors** — a missing tenant
      header/param can return empty results or `null` rather than an error (TerraQuest,
      StatMap, Agile). Verify a `total`/count, don't trust an empty list.
- [ ] **Verify the vendor before trusting PlanIt's `scraper_type`** — it can be stale
      (Birmingham) or wrong (Manchester). Its `planning_url`, `url`, and `docs_url` are
      reliable; the label is a hint.
- [ ] **A TLS certificate error is not a reason to turn verification off.** Some council
      servers omit their intermediate certificate. Browsers and the OS trust store fill
      the gap, while some HTTP libraries (Python's default bundle) fail. Use the OS trust
      store. Never disable certificate verification.
- [ ] **Distinguish a council backend outage from a block** — `500` everywhere while a
      health endpoint 200s and the doc host is TCP-dead = outage; retest later.
- [ ] **Label the files** using the description/date shown next to each link, and flag
      **consultee responses** (highway authority, LLFA, Environment Agency, ecologist,
      conservation officer, Historic England, environmental health…) as their own class —
      the triage and representation skills read those first.
- [ ] **Note the site's planning history** — portal detail pages usually list *related
      applications* (earlier refusals, appeals, extant permissions, s73s). When the retrieval
      feeds a triage or representation, pass those references on with the delivery.
- [ ] **An amendment application is not a self-contained retrieval — fetch the whole chain.**
      When the reference is a non-material amendment (s.96A) or a variation/removal of
      conditions (s.73), its own documents are only the delta, and the skills downstream
      cannot assess them alone. Deliver, alongside the amendment's own files:
      - the **parent permission's decision notice** (the full condition set, including the
        condition listing the approved plans) and its **approved drawings**;
      - the parent's **officer or committee report**, and the **s.106** with any deed of
        variation;
      - **every earlier amendment** on that permission, and any condition-discharge decisions.

      Finding them: the amendment's description almost always names the parent reference —
      take it from there, then search the **parent reference** and the **address** separately,
      because related-application panels are incomplete on many portals and a chain member
      filed under a different suffix is easy to miss. Say which links you could not retrieve
      rather than delivering a chain that looks complete.
- [ ] **Don't record a committee report as missing until the committee system has been
      checked.** For a committee decision, the report, update sheet and minutes are often
      on the council's committee system (Modern.gov or similar), not the portal. Check
      `portal.committee_papers` in the profile. If it is not set, find the system from the
      council's meetings page before concluding. See "Committee papers" above.
- [ ] **Don't believe a single empty search.** Retry once on a fresh session and run a
      date-only control search before treating "No results found" as a finding.
- [ ] **Report anything not retrieved** rather than silently returning a partial set.
- [ ] **Separate "removed from the register" from "I could not fetch it."** Councils do
      pull cases from public view, and several vendors answer a live deep link with a
      polite 200-carrying notice rather than a 404. If a reference is attested elsewhere
      (the user, a national aggregator, another application's history) but no portal route
      returns it, say so explicitly and hand over whatever metadata survives — that is a
      substantive finding about the register, not an error in the retrieval.
- [ ] **Struggling ≠ keep trying.** If the recipe (plus a couple of documented
      corrections) still isn't retrieving, stop and hand the user a browser link to
      download manually — see "If retrieval struggles" in the scope section.

## Coverage

Which authorities have been checked — with each council's `status`, `scriptable` flag and
`last_tested` — is recorded in
[`planning-portal-registry.json`](planning-portal-registry.json), with the evidence behind
each status in that authority's `authorities/<slug>.json` `verification` log.

Treat both as a **living cache**: portals migrate, vendors change, and a `tested-ok` row
is a statement about the day it was tested. Re-resolve the vendor per council at run time
rather than trusting a cached row, and when a run contradicts what a profile says, fix the
profile — that is what makes the next run cheaper.
