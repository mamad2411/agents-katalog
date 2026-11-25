---
name: link-fix
description: Audit and fix the links stored in the Sanity dataset, three rules counted in one table first. own-domain turns links to the site's own domain (`https://example.com/pricing` or a bare `/pricing` in an external link, CTA, header/footer link or rich-text annotation) into references or internal paths. http upgrades `http://` links and URL fields to `https://` per host, optionally only where https answers. slash aligns internal paths, own-domain URLs and slugs with the trailing-slash convention in `web/next.config.*` and fixes double or missing slashes. The user picks the rules; a dry-run-first script writes them (`--apply`) and re-checks, then the code goes to `link-reviewer`. Use when the user asks to "fix links", "convert absolute URLs to relative", "editors pasted full URLs", "links to our own site open in a new tab", "replace http with https", "trailing slashes are inconsistent", "check our slugs", after a content import or migration, or before a domain change.
---

# Link fix: own-domain URLs, http and slashes

Three kinds of link go wrong in the dataset, mostly through pasting and imports:

- **Own domain as external.** Editors paste `https://example.com/pricing` into an
  **external** link. It works, but the site opens every `http(s)` link in a **new
  tab** (`opensInNewTab`, `web/src/ui/components/Link/BaseLink/utils.ts`), preview
  and staging deployments send visitors to production, a domain change breaks every
  one of them, and nothing stops someone deleting or renaming the target page.
- **`http://`.** Costs a redirect hop at best, a mixed-content warning or a dead
  link at worst, and some hosts never got https.
- **Slashes.** The site has one trailing-slash convention; a link that doesn't
  follow it costs a 308 redirect on every click and splits link signals between two
  URLs. A page slug with a slash at either end is never served at its URL.

Keep this flow: **check → ask → fix (dry run, then apply) → verify → check the
code.** Don't skip the question in step 2, and never run `--apply` without the
user's go-ahead.

## The script

`scripts/links.mjs` (logic in `scripts/lib.mjs`, tests in `scripts/lib.test.mjs`),
plain Node ESM. **Run it from the starter's `web/` folder**: it loads
`@sanity/client` and `dotenv` from there, reads `web/.env.local`, then `web/.env`,
and reads `web/next.config.*` for the trailing-slash convention.
From the project's `web/` folder:

```bash
LF=../.agents/skills/link-fix/scripts/links.mjs
node $LF check [--rules=own-domain,http,slash] [--host=example.com,old-example.com] [--verify-https] [--json]
node $LF fix --rules=… [--to=auto|reference|path] [--apply] [--drafts=both|skip] [--include-broken] [--verify-https] [--keep-http=host,…] [--json]
```

| Argument / env | Meaning |
|---|---|
| `check` | Read-only scan and counts |
| `fix` | **Dry run by default**: prints every planned change and the expected count after it. Writes only with `--apply` |
| `--rules=` | `own-domain`, `http`, `slash`, comma-separated. `check` runs all three by default; `fix` needs the list the user picked |
| `--to=` | own-domain only. `auto` (default): reference where a published document matches, path otherwise. `reference`: only references. `path`: only internal paths |
| `--host=` | Own domains, comma-separated. Added to `NEXT_PUBLIC_BASE_URL`; the `www.` variant always counts. Required for `own-domain` when the env has no base URL or it is `localhost` |
| `--trailing-slash=` | `auto` (default): read `trailingSlash` from `web/next.config.*`. `never` / `always` overrides it |
| `--verify-https` | Requests every upgraded URL (HEAD, then GET; 8 s timeout). `check` shows the result per host; `fix` upgrades only URLs whose https answers below 400 |
| `--keep-http=` | Hosts to leave on `http://` |
| `--drafts=` | `both` (default): patch published documents and open drafts. `skip`: published only |
| `--include-broken` | own-domain only. Also convert links with no route to paths (default: leave them and list them) |
| `--dataset=` | Overrides `NEXT_PUBLIC_SANITY_DATASET` |
| `NEXT_PUBLIC_SANITY_PROJECT_ID`, `NEXT_PUBLIC_SANITY_DATASET` | Required |
| `SANITY_API_READ_TOKEN` | Enough for `check` and the dry run; **without any token drafts are invisible** |
| `SANITY_API_WRITE_TOKEN` (or `SANITY_API_TOKEN`) | Editor token, required for `--apply` |

Ground rules: never read or print an `.env` file or a token (the script says what
is missing). Creating a token and writing to a production dataset are the user's
calls. If the starter was renamed or moved, adjust the path to the skill folder.
After editing `scripts/lib.mjs`, run `node --test scripts/lib.test.mjs` from the
skill folder.

## Step 1: check, report numbers

Ask for the live domain if `NEXT_PUBLIC_BASE_URL` may not be set locally (the dev
fallback is `localhost`, which the script ignores), and for any **old domains** or
preview hosts editors may have copied from (`old-brand.com`, `project.vercel.app`).
Then run `check` and relay its first table as it is: one row per rule and issue,
with `total`, `fixable` and the split into published, draft and release version.

What it scans: every non-system document in the **raw** perspective (published,
`drafts.*`, release `versions.*`), CDN off, so the numbers are current. Span text is
ignored, and so is a stale `external` value left on a link whose `type` is no
longer `external` (hidden in the Studio, never rendered). `mailto:`, `tel:` and
`#anchor` values are never touched.

### Where links live

Both starters model links the same way. Every link object is built on
`linkBaseFields` (`studio/src/sanity/schemaTypes/partials/linkBaseSchema.ts`):
`type` (`internal` | `path` | `external` | `download`), `internal` (reference),
`internalPath`, `external`, `file`, `params`.

| Field kind (report column) | Where it comes from |
|---|---|
| `link`, `simpleLink`, `headerLink`, `iconLink` (or the field name if the object has no `_type`) | CTA links (`cta`, `headerCta`), header/footer links, icon links, link lists, `redirect.destination`, `rewrite.destination` |
| `richText link` | Portable Text `markDefs` link annotations (`simpleLink`) in `richText`, `simpleRichText`, `pageRichText`, nested rich text in callouts etc. |
| `<type>.<field>`, e.g. `platformLink.url`, `metadata.canonical`, `alternate.href`, `author.linkedinUrl`, `site.sameAs[]`, `video-embed.url` | Plain URL strings (Sanity `url` fields) |

### own-domain

A URL counts when its host is an own domain (`http`/`https`, `www.` or not,
protocol-relative `//`), whatever the trailing slash, query or hash. A bare site
path in an `external` field (`/pricing`, which the Studio rejects but imports
don't) counts too. Each finding gets a status:

| Status | Meaning | Possible conversion |
|---|---|---|
| `document` | A **published** document lives at that path | Reference or path |
| `path` | A route exists, but there is no document to reference: a code route (`/llms.txt`, `/api/…`, `/admin`, `/styleguide`), the exact source of a CMS redirect, a `.md` twin, or a page that exists only as an unpublished draft | Path only |
| `broken` | No document and no known route answers there (a renamed slug, a deleted page, a typo) | Left alone by default; needs a human |
| `not convertible` | A plain URL field, not a link object. A canonical or a feed URL is meant to be absolute | None (the http and slash rules still apply) |

Path → document follows the starter's routing (`web/src/lib/resolveUrl.ts`,
`web/src/app/sitemaps/all.xml/route.ts`): `page` = `metadata.slug` as the full path, `post` =
`/blog/<slug>`, `case-study` = `/case-studies/<slug>`, `podcast-episode` =
`/podcast/<slug>`, listing pages = `/blog`, `/case-studies`, `/podcast`. If the
project added a routed type, add it to `REFERENCEABLE_TYPES` and the path maps at
the top of `scripts/lib.mjs` first, or its links show as `broken`. Matching is
case-sensitive, like the routes.

### http

Every `http://` value in an external link or a URL field. The check lists the
**hosts** with their counts; read them back, because an upgrade is only safe where
the host serves https. Local and private hosts (`localhost`, `*.local`, `*.test`,
IP addresses) are reported and never upgraded. An own-domain `http://` link is
counted under both rules; when own-domain converts it, the upgrade is moot.

### slash

The convention comes from `trailingSlash` in `web/next.config.*`: unset or `false`
(the starters' default) means **no trailing slash** (`/pricing`; Next 308-redirects
`/pricing/` to it), `true` means **always** (`/pricing/`). The root `/` and paths
ending in a file extension (`/llms.txt`) are exempt. The check prints the convention
and where it came from. If the project changed the convention, confirm that the link
resolver, sitemap and canonical builders follow it too: that is code, so it belongs
to `link-reviewer` (step 5).

| Where | Fixable | Report only |
|---|---|---|
| `internalPath` (links with `type: path`) | Trailing slash against the convention, missing leading slash, double slash, whitespace at the ends, uppercase when only the lowercase path exists | A full or protocol-relative URL, a space inside the path, a query or anchor with no path |
| Own-domain URLs (link `external`, URL fields) | Trailing slash, double slash in the path | |
| `metadata.slug.current` of `page`, `post`, `case-study`, `podcast-episode` | Leading slash, trailing slash, double slash. Page slugs are full paths **without** the leading slash (`about`, `services/web`; `/` is the home page): the page route matches the slug as stored, so `/about` or `about/` is never served, and the sitemap prints `//about`. Prefixed types are one segment | Uppercase or whitespace (fixing it changes a live URL: add a redirect), a slash inside a one-segment slug, a fix that would collide with another document's slug |

A value with any report-only issue is left whole for a human; the list shows the
suggested value next to it.

**Drafts and versions.** The counts are split by variant. A document with an open
draft can appear twice (published and draft); that is two values to fix, because
publishing the draft would bring the old value back. Release versions
(`versions.*`) are counted but never patched: tell the user to fix them in the
release. If the script warns that no token was set, the draft numbers are missing;
ask for a read token before going on.

## Step 2: ask which rules, and how

Relay the table, then ask **which rules to apply** (`--rules=`). Then, per rule
picked:

**own-domain: references or paths.** Explain the two link types like this:

| | **Reference** (`type: internal`) | **Internal path** (`type: path`) |
|---|---|---|
| Stores | A reference to the document (`internal._ref`) | A string like `/pricing` |
| Slug changes | The link follows the document; the href is rebuilt from the current slug | Breaks silently (404 or a redirect hop) |
| Deleting the target | The Studio shows it under "References" and blocks deleting a referenced document | Nothing warns |
| Validation | The Studio checks the target exists | Only "starts with a single `/`" |
| Works for | Documents in the CMS (`page`, `post`, `case-study`, listing pages, podcast) | Any route, including code routes and pages not in the CMS |

Query strings and hashes (`?category=news`, `#form`) move to the link's **URL
parameters** field (`params`) in both cases; internal paths are written in the
site's trailing-slash convention.

Offer three options and **recommend `auto`**: references wherever a published
document matches, internal paths for the rest. `reference` leaves path-only links
as they are (external); `path` turns everything into strings. For **broken links**
(`broken > 0`): fix them by hand in the Studio (the list has the document IDs), or
convert them to paths as they are with `--include-broken`. A broken link stays
broken either way, so the Studio fix is usually better.

**http: which hosts.** Recommend `--verify-https`, so only URLs whose https answers
are rewritten; the rest stay listed under "Skipped". Hosts the user wants left
alone go in `--keep-http=`. A failed check is not proof (some hosts block scripts):
the user can open the https URL and re-run without the flag for that host.

**slash: the convention.** Confirm the detected convention is the one the site
means to keep. Changing `trailingSlash` itself is a code change (and needs the
resolver, sitemap and canonical builders to follow); this skill only aligns the
content with it.

**Drafts** (`draft > 0`): patch the open drafts too (default) or only published
documents (`--drafts=skip`, then publishing a draft restores the old value).

## Step 3: dry run, then apply

Always show the dry run first and read it back in short: how many links become
references, how many paths, how many values get https or a slash fix, what is
skipped and why, and the `Expected count on the next check`.

```bash
node $LF fix --rules=own-domain,http,slash --to=auto --verify-https --host=example.com            # dry run, writes nothing
node $LF fix --rules=own-domain,http,slash --to=auto --verify-https --host=example.com --apply    # writes
```

Then ask: **run it yourself, or should I run it?** If the user runs it, give the
exact command from the starter's `web/` folder and suggest the `! <command>`
prefix so the output lands in the conversation. Suggest a backup first on a
production dataset: `pnpm exec sanity dataset export <dataset> backup.tar.gz`
from `studio/`.

What `--apply` does, so you can explain it:
- **One patch per document**, guarded by `ifRevisionId`. If someone edited the
  document after it was read, the patch is rejected (`document changed since it was
  read (re-run)`) instead of overwriting their work. Re-run the command for those.
- **Only the affected fields change.** own-domain: the link's `type`, then
  `internal` (reference) or `internalPath` (path), `params` set from the URL's query
  and hash (cleared when the URL had none), `external` removed. http and slash: the
  one string, with both fixes combined when a URL needs both. Labels, keys, `_type`,
  CTA variants, icons and the rest of the document stay untouched. Annotation
  `_key`s stay, so the marks in the text still point to them.
- **A link that becomes internal wins**: its `external` value is dropped, so an
  http or slash fix planned for it is not written (and counts as resolved).
- **Drafts are patched in place, never published and never replaced.** The draft
  keeps every other unpublished change; the published document gets the same fix
  separately. An editor with the document open sees the change arrive live.
- **Idempotent**: a fixed value no longer matches any rule, so a second run finds
  nothing to do for it.
- The API mutations fire the revalidate webhook (`sanity.blueprint.ts`) like a
  Studio edit, so the live site picks up the change without a deploy.

## Step 4: verify

Run `check` again with the same `--rules` and `--host` and compare the total with
the expected count the fix printed. Normally what is left is: report-only findings
(`not convertible`, report-only slash issues, local hosts), `broken` (unless
`--include-broken`), `path` findings when `--to=reference`, kept or unverified
http hosts, drafts when `--drafts=skip`, and release versions.

If the count is right, go on. If not, find out why before re-running anything:

| Symptom | Likely cause | What to do |
|---|---|---|
| `Failed: … changed since it was read` | Someone edited the document during the run | Re-run `fix --apply`; it is idempotent |
| `Failed: … permission` / 401 / 403 | Token is Viewer, expired, or for another project | User creates an Editor token as `SANITY_API_WRITE_TOKEN` |
| Count unchanged, nothing failed | Dry run (no `--apply`), a different dataset than checked (`--dataset`), or different `--rules` | Compare the header lines of both runs |
| Draft findings remain | `--drafts=skip`, or the first run had no token and never saw drafts | Re-run with a token and `--drafts=both` |
| Published findings come back later | An editor published an old draft over the fix | Fix the draft too and re-run |
| `version` findings remain | Release versions are never patched | Fix them inside the release in the Studio |
| http findings remain with `--verify-https` | The host's https did not answer, or blocks scripts | Open the https URL; re-run without the flag (or keep the host with `--keep-http`) |
| Slash findings flip after a config change | `trailingSlash` changed between runs | Settle the convention first, then run once |
| Studio still shows the old value | The Studio tab was opened before the patch and is offline / stale | Reload the Studio |
| The site still renders the old href | Cache not revalidated (webhook missing or failing) | `pnpm blueprints:plan`, or call `/api/revalidate-all`; the dataset itself is already fixed if `check` agrees |
| A link kind is never found | A project-specific link object that doesn't use `type`/`external`/`internalPath`, or a routed type missing from `lib.mjs` | Add it to `lib.mjs`, re-run `check` |

Spot-check one fixed page in the browser: an internal link should be root-relative
in the site's convention (`href="/pricing"`) and open in the same tab; an upgraded
external link should start with `https://`.

## Step 5: check the code

The dataset is half of it: hardcoded `http://` URLs, own-domain links in
components, `<a>` where `next/link` belongs, and a sitemap or canonical that
disagrees with `trailingSlash` produce the same problems from code. Hand that to
the **`link-reviewer`** agent (`.agents/agents/link-reviewer.md`): in Claude Code
it runs as a subagent; in agents without named subagents, read that file and walk
its checklist inline. It returns a verdict and findings and never edits; apply the
fixes it reports with the user's go-ahead.

## Report back

End with: the dataset, hosts and trailing-slash convention checked, the rules
picked, the counts before (the summary table, plus own-domain by document type and
field kind, and http hosts), the mode chosen, what was changed (references, paths,
https upgrades, slash fixes, documents patched, failures), the count after vs. the
expected count, what is left for a human (broken links, report-only slash issues,
hosts left on http, release versions, with document IDs), and the `link-reviewer`
verdict on the code.
