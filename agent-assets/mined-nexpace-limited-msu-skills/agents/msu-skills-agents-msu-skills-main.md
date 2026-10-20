# msu-skills

The `msu-skills` catalog — the skills NEXPACE publishes for MSU builder work, packaged
as one plugin per coupling boundary. Anything reusable across that work lives here,
whether or not it is MapleStory-specific; product-specific skill sets live in their own
repositories and depend on these.

**This repository is public on GitHub.** Everything committed here is world-readable.

## Commands

Skills have no build and no package manifest: one is edited in place at
`plugins/<plugin>/skills/<name>/SKILL.md` and shipped verbatim. The landing page is the
only thing here that is built, and it is built *from* those files — see *The landing
page*. The commands below stand in for a test suite, and CI runs all of them.

```bash
claude plugin validate .                            # marketplace catalog
claude plugin validate plugins/<plugin>             # one plugin, and its skill files
npx skills add . -l                                 # skills the skills CLI discovers
bash install.sh --target /tmp/probe                 # smoke-test the manual installer
bash install.sh --plugin <plugin> --target /tmp/one # ...and the single-plugin path
bash scripts/test-remote-installer.sh               # piped installer, local archive adapter
bash plugins/<plugin>/tests/test.sh                 # a plugin's own executables, if it ships any
bash scripts/check-endpoints.sh                     # no leaked endpoint or credential
cd web && npm ci --ignore-scripts && npm run build  # export the landing page into web/out/
```

Pointed at the repo root the validator reads `marketplace.json`, and for every
local-path entry it also reads that plugin's `plugin.json` — so the first line covers
the packaging as a whole. The second is still worth running once per plugin you touched,
because only the plugin-directory form checks the skill, command, and hook files.

The last line runs with the working directory at `web/`, because the app resolves the
repository it reads as the parent of the working directory. `npm ci`, never `npm install`:
`web/package-lock.json` is committed and `ci` installs exactly what it pins rather than
re-resolving. `--ignore-scripts` is required of both workflows — see *Public-repository
rules*. CI runs Node 22.

`make check` runs that list in one pass, and `make dev` runs the site locally on whatever
port is free (`make help` lists the rest). The Makefile is a convenience wrapper only —
CI runs these commands directly, so `ci.yml` stays the authority and a new check belongs
there first.

## Contributing

The contributor's half lives in [CONTRIBUTING.md](CONTRIBUTING.md) — where a skill file
goes, which plugin it belongs in, how to write it, what the local checks do and do not
catch, and how to open the pull request. Send anyone contributing a skill there rather
than here; what follows governs the repository rather than the contribution.

A PR opened against `main` is moved onto `develop` by `retarget-prs.yml`, which comments
when it does; it acts only when the PR is opened, so a change that genuinely belongs on
`main` (a hotfix, a release-machinery change) keeps its base by being moved back
once, by hand.

`main` stays the default branch because every install channel reads it, and it is
protected: direct pushes are rejected for everyone, admins included. **Merging the
release PR is the release** — work integrates on `develop` and ships when a
`develop` → `main` PR merges, so a mistake merged to `develop` can still be caught
before it is live. See *Versioning and release* for how that PR is cut.

CI runs on every push to `main` or `develop` and on every pull request:
`plugin-validate`, `install-smoke`, `skills-discovery`, `site-build` — which installs
`web/`'s dependencies from the committed lockfile and runs the export — `guards`, and
one of two version guards picked by base branch — `no-premature-bump` into `develop`,
`version-bump` into `main`. `pages.yml` then republishes the landing page, but only
after a `main` run of CI succeeds: it triggers on that run's completion rather than on
the push, so a release whose guards failed is never published, and a `develop` run
never publishes anything.

## Core principle — one source, three channels

The Agent Skills open standard (`SKILL.md`) is adopted by Claude Code, Codex CLI,
Gemini CLI, and Kimi CLI. So there is **no conversion, and nothing on an install path is
built**: the `SKILL.md` files under `plugins/*/skills/` are the only source, shipped
verbatim everywhere. The landing page under `web/` is a real build, but it sits
downstream of those files — it reads them, and no channel reads it.

Skills install automatically on all three; for a skill, the channels differ only in what
happens to the `maple-lookup` MCP server. A plugin's `scripts/` is not a skill and is the
one thing that does not travel — see the paragraph below the table.

| Channel | `maple-lookup` MCP |
|---|---|
| Claude Code plugin (`msu@msu-skills`) | automatic — bundled `.mcp.json`, key via `userConfig` prompt |
| `npx skills add NEXPACE-Limited/msu-skills` | **manual** — README "MCP Configuration" |
| `install.sh` via curl or checkout (Codex / Gemini / Kimi) | best effort — prints the Codex TOML snippet, runs `mcp add` for Gemini/Kimi when `$MSU_OPENAPI_KEY` is set |

**Do not break this shape.** Per-platform copies or build artifacts fork the source.

A plugin may also ship an executable the *host* runs rather than an agent — a status
line, a hook. That is not a skill and does not go under `skills/`: both flat channels
copy skill directories, so anything below one is carried to CLIs that have no concept
of it, under a name that then has to be unique across the whole catalog. It lives in
the plugin's own `scripts/`, which only the Claude Code channel reads, and the skill
that installs it reaches it through `${CLAUDE_PLUGIN_ROOT}`. Its checks go in the
plugin's `tests/test.sh`, which `guards` runs.

**The skills CLI reads the catalog.** `vercel-labs/skills` (measured at 1.5.22) is not a
blind recursive glob: when `.claude-plugin/marketplace.json` is present it scans exactly
the plugins that catalog lists. A directory under `plugins/` with no catalog entry is
invisible to that channel — which is why `skills-discovery` in CI enumerates plugins
from the filesystem and requires every skill to turn up in the CLI's output. Forget the
entry and CI says so.

It still has no plugin *boundary* for the user: `npx skills add
NEXPACE-Limited/msu-skills` offers every catalogued plugin's skills at once, and there
is no remote sub-path form to narrow it. `--skill <name>` is the only selector, and the
README says so. `install.sh` keeps the boundary through `--plugin`. MCP configuration is
outside the Agent Skills standard, so no plugin's `.mcp.json` is applied on that channel.

## Layout

```
.claude-plugin/marketplace.json          # the catalog: msu-skills. Lists every plugin
plugins/<plugin>/.claude-plugin/         # plugin.json — name, version, userConfig
plugins/<plugin>/.mcp.json               # MCP servers this plugin owns, if any
plugins/<plugin>/skills/<name>/SKILL.md  # the only source. name = dir name = kebab-case
plugins/<plugin>/skills/<name>/references/  # files the skill loads on demand
plugins/<plugin>/scripts/                # executables the host runs, not the agent
plugins/<plugin>/tests/test.sh           # checks for those. bash, no network. CI runs it
install.sh                 # local or curl installer for non-Claude CLIs; --plugin selects one
Makefile                   # wrappers: make check, make dev. See Commands
web/                       # the landing page: a Next.js App Router app, statically exported
web/next.config.mjs        # output:'export' (prod only). basePath and site URL from the catalog
web/lib/*.ts               # the repository read into the data every page renders from
web/app/**                 # the page types, plus the sitemap.xml and llms.txt handlers
web/public/                # og.png, favicon.svg, logo.svg — copied into the export as-is
web/package.json, web/package-lock.json  # the app's deps. Both committed; npm ci reads them
scripts/check-endpoints.sh # public-repo scan, inherited from the retired hub
.github/workflows/ci.yml   # the commands above, plus guards, on every PR and push
.github/workflows/pages.yml # builds and publishes the page after CI passes on main
.github/workflows/retarget-prs.yml # moves a PR opened against main onto develop
.github/workflows/release-pr.yml # opens/refreshes the release PR, Mondays 00:00 UTC
.github/ISSUE_TEMPLATE/    # issue forms; blank issues stay enabled
CONTRIBUTING.md            # the contributor's half: writing a skill, placement, the PR
AGENTS.md                  # this file. CLAUDE.md and GEMINI.md are one-line @ imports
```

`AGENTS.md` holds the content. Gemini CLI does not read it by default, so `GEMINI.md`
is what loads this context there; `CLAUDE.md` is the same pointer for Claude Code.

Catalog name is `msu-skills`, and every plugin in it installs as `<plugin>@msu-skills`.
Which plugins exist is `.claude-plugin/marketplace.json`'s answer, not this file's — read
the catalog, and do not expect a roster here. Skill name ≠ plugin name ≠ catalog name:
`plugins/msu/skills/maple-make/` is invoked as `msu:maple-make`.

## The repository is its own catalog

`.claude-plugin/marketplace.json` names the catalog `msu-skills` and lists each plugin
by local path (`"source": "./plugins/msu"`). Users add this repository and install from
it directly, and a release is whatever sits on `main`.

**Every plugin gets its own root under `plugins/`.** That is not cosmetic. Two entries
sharing one plugin root (`"source": "./"` twice, split by the `skills` field) do isolate
skills, but `userConfig` is read only from `plugin.json` — an entry-level `userConfig` is
silently ignored — so every plugin in the repository would inherit the MSU OpenAPI key
prompt and the `maple-lookup` server. A plugin that needs no credential must not acquire
one, which forces separate roots.

This replaced a separate `nexpace-skills-hub` repository that held the only catalog: a
release needed two repositories in agreement, and that private catalog was the only way
to reach a public plugin.

**Exactly one catalog may name a plugin.** Two give it two install identities, and a
user who added both ends up with two copies of every skill. The hub still lists `msu`
pinned at `msu--v0.2.0`, so `msu@nexpace` and `msu@msu-skills` both resolve today —
dropping that entry is the follow-up that makes this rule true again.

The other two channels read this repository rather than through a marketplace, but
neither is indifferent to the catalog: `install.sh` walks `plugins/` in a checkout or a
temporary GitHub source snapshot, and the skills CLI scans the plugins
`marketplace.json` lists. A catalog entry is what makes a plugin real on every channel.

## MCP ownership

**The `msu` plugin owns `maple-lookup`.** The definition, the URL, and the key prompt
all live in `plugins/msu/`; downstream plugins consume it through a dependency
declaration and must not redefine a server under the same name.

- `plugins/msu/.mcp.json` holds the server. `${user_config.openapi_key}` resolves from
  the `userConfig` block in `plugins/msu/.claude-plugin/plugin.json`, which marks the
  key `sensitive`.
- A server belongs to exactly one plugin, because its `.mcp.json` sits inside that
  plugin's root. Do not put an `.mcp.json` at the repository root: it would be loaded as
  a *project-scoped* server while working in this repo, where `${user_config.*}` does
  not resolve, and it would not belong to any plugin.
- Never commit a key. `install.sh` itself never prints a key value — its own messages
  show the env-var form only, and a failing CLI's stderr is relayed with literal key
  occurrences redacted to that form.

## Consumers

Downstream product plugins depend on `msu` rather than vendoring its skills, so the
source stays single. Three obligations follow:

- **Skills are called by name, not by path.** A consumer's skill body says "find the
  `maple-make` skill and follow its SKILL.md". Cross-plugin file paths break under
  Claude Code — `${CLAUDE_PLUGIN_ROOT}` points at the caller's own root, and
  `../<other-skill>/` only happens to work in flat non-Claude installs.
- **Renaming or removing a skill here is a breaking change** for anyone name-calling
  it, even though nothing in this repo references it. Same for the contract surface a
  consumer wires into (recipe IDs, profile fields). What that costs in a version number
  is *Versioning and release*'s table, which is the only place that enumerates them.
- **A dependency names the catalog, not only the plugin.** Consumers declare
  `{ "name": "msu", "marketplace": "msu-skills" }` and list `msu-skills` in their own
  marketplace's `allowCrossMarketplaceDependenciesOn`. Renaming this catalog breaks
  every one of them.

## The landing page

`https://nexpace-limited.github.io/msu-skills/` is generated, not written. `web/` is a
Next.js App Router app that reads `.claude-plugin/marketplace.json`, every plugin's
`plugin.json` and `.mcp.json`, and every `SKILL.md` frontmatter at build time, then
exports static HTML (`output: 'export'`). `next build` writes `web/out/`, and that
directory is what Pages serves; nothing runs at request time.

```
/                   hero, install channels, the plugin list, MCP setup, the notices
/<plugin>/          that plugin's identity, its own install commands, and its skills
/<plugin>/<skill>/  one skill: its description, what it bundles, how it is invoked
/mcp/               the server: its values, its tools, and the skills that call it
/sitemap.xml        every page the build published, absolute
/llms.txt           the same pages as a plain-text index for an LLM reader
```

A skill has its own page, so the published URL set grows with the catalog rather than
holding at one page per plugin. A plugin card, and a skill's description, bundled-file
count, `plugin:skill` invocation, and MCP requirement, all come from the files above. A
page links to `references/` only when the skill has one — not every skill does.

**Never retype a plugin's or a skill's own fields into a component.** Components carry
page structure and the prose that has no other source — the install narrative, the
README's notices. Anything a manifest or a frontmatter already declares is read by
`web/lib/` and passed in. The MCP server's name, URL, header, and transport come from
`.mcp.json`, the per-CLI snippets are built from those same values, and the credential's
title resolves through the `userConfig` key its header references. Adding a plugin or a
skill updates the pages with no edit here, the same property every CI check has.

README repeats those MCP values as prose, for the channels that configure the server by
hand. It is the one copy the build cannot keep honest, so `guards` fails when README
stops mentioning a name, URL, header, or `--transport <type>` the server declares.

- **The site's URL identity is derived, never typed.** `web/next.config.mjs` reads the
  catalog and computes `basePath` and the absolute site URL from the repository it names,
  then hands both to the app through `env`; `web/lib/site.ts` reads them back and is the
  only module allowed to know those strings. A repository rename re-points every
  canonical, every sitemap `<loc>`, and the OG image with no edit. A literal
  `/msu-skills` anywhere else breaks a fork.
- `trailingSlash: true` is mandatory. Without it the export writes `<plugin>.html`, and
  Pages serves no redirect from the slash form every indexed URL uses.
- `metadataBase` keeps its trailing slash. URL resolution drops the last non-slash
  segment, so a base without it resolves a relative `og.png` against the host root.
- The canonical link and `og:url` are set per page, never on the root layout: a layout
  canonical is inherited verbatim by every route, including the 404, which then declares
  itself a duplicate of the home page. The not-found routes carry no canonical and
  `robots: noindex, nofollow` instead.
- Next applies `basePath` to `next/link` and to bundled assets, but **not** to a raw
  `href`/`src` or to a metadata icon URL. Those go through `asset()` in `web/lib/site.ts`;
  a bare `/favicon.svg` 404s on a project Pages site.
- `sitemap.xml` and `llms.txt` are Route Handlers with `export const dynamic =
  'force-static'`, not `app/sitemap.ts`. The built-in convention serialises with its own
  indentation, so byte-continuity with what the site published before is unreachable that
  way. Both read one list of published URLs, so neither can claim a URL no route
  generates.
- `sitemap.xml` carries `<loc>` and nothing else: Google ignores `<priority>` and
  `<changefreq>`, and reads `<lastmod>` only where it is consistently accurate, which a
  build that rewrites every page cannot claim. It lists real pages only, so its `<loc>`
  count is lower than the number of exported `index.html` files — Next adds `404/` and
  `_not-found/`, and neither is published.
- `web/out` also holds React Server Component payload sidecars, named `__next.*.txt` and
  `index.txt` at any depth. Anything that prunes them matches those two shapes: a blanket
  `*.txt` deletes `llms.txt`, the one `.txt` the site publishes.
- A sub-page's breadcrumb is rendered twice — visibly and as `BreadcrumbList` JSON-LD —
  from one set of values, because structured data has to represent what the page shows.
  The catalog page is the root and gets neither.
- `.mcp.json` says how to reach a server, never what it answers, so `/mcp/` reads its tool
  names and purposes from the `## MCP Tool: <server>` table the owning plugin's skills
  already keep for their own agent. Find no table and the build stops rather than render a
  page that names no tool. `/mcp/` is also a route, and a plugin named `mcp` would shadow
  it with the App Router reporting nothing, so the data layer refuses that name.
- **The export makes exactly one request to a host it does not serve**, and everything else
  is served from the site. Fonts are self-hosted: `next/font` downloads both families at
  build time, so neither costs a request. The one exception is the Cloudflare Web Analytics
  beacon in the root layout — GitHub Pages keeps no access log and reports no visitor count,
  so it is the only thing that measures whether the site is read. Do not delete it as a
  stray third-party asset, and hold a second one to the same bar: name what it answers that
  nothing here already answers. It sets no cookie and collects no personal data, which is
  why README's notices say nothing about it. The beacon's token is public by design and is
  written in the layout; a static export inlines an env var into the HTML regardless, so
  hiding it there would only make it look secret.
- **The top bar is sticky, and two things depend on its height.** `--topbar-h` in
  `globals.css` is the only place that height is stated: `.topbar .wrap` takes it as
  `min-height`, and `html { scroll-padding-top }` is computed from it so an anchor jump
  never lands its target underneath the bar — which governs `#main` (the skip link) and
  `#plugins`. Change the bar's height there and nowhere else. Its
  `z-index: 40` sits in a fixed budget: above the page, below the palette veil (60), the
  palette (61) and the skip link (80); it deliberately does not need to outrank
  `.colorhead::before`, which is sealed by its own `isolation: isolate`. The background
  stays fully opaque — a translucent bar would render the nav over arbitrary page content
  at an unmeasured contrast on every scroll position.
- **The motion system is CSS only.** It adds no dependency, no client JavaScript and no
  marker on `<html>`. Three invariants hold it there. The motion header in `globals.css`
  states each one and is the authority; this list carries the names so a reviewer knows
  what to check.
  1. Every `@keyframes` declares only a `from`, so the base rule is the finished state and
     `animation: none` renders the page that ships. `animation-fill-mode: forwards` must
     never appear in the file.
  2. Any hidden initial state sits inside `@media (prefers-reduced-motion: no-preference)`
     nested in an `@supports` test for the timeline that rule uses. Most readers are inside
     that fence and Firefox stable is outside it, so a rule that forgets the fence hides
     content from the majority rather than from an edge case.
  3. A scroll range is an absolute length off `cover`, never a percentage of `entry`, which
     resolves against the subject's own height. This one carries a layout constraint:
     a reveal needs `--reveal` (200px) of scrollable document below its subject's top edge,
     so nothing in the last 200px of a document may carry one.

  Two gestures divide the work — colour unfurls, ink rises. A coloured field grows from an
  anchored edge; type fades up into place on scroll. They are told apart by what moves, so
  no box carries both. Every base rule is opacity 1 and no keyframe declares a `to`, so a
  fade's endpoint is always the measured value. Two states drop the animation onto that base
  rule rather than tune it: an element containing `:focus-visible`, because a focus ring must
  never be half-drawn, and `.skill-body:has(details[open])`, because a disclosure does not
  scroll. That is also why the `prefers-reduced-motion` guard keeps its blanket `!important`
  — Radix Presence unmounts cmdk's dialog only when the computed `animationName` is `none`,
  so weakening it leaves the palette hanging open, and a palette entrance is scoped to
  `[data-state="open"]` rather than declared on `.pal` itself.
- `web/public/og.png` is the link-preview card, the one asset that is drawn rather than
  generated. It carries no counts and no plugin names, so only a change to the headline
  or the wordmark makes it stale.
- `favicon.svg` and `logo.svg` are deliberate copies of one mark, not a duplication to
  clean up: a favicon URL is cached hard by browsers and its box is cropped for 16px
  chrome, so the in-page wordmark has to be free to change without waiting out that cache
  or inheriting that crop.
- **There is no ownership marker any more, and nothing replaces it.** `next build` empties
  `web/out` unconditionally, and that path is fixed inside `web/` rather than an argument,
  so there is no stale page to leave behind and no way to aim a build at a directory
  somebody else owns. What went with it is the ability to render into an arbitrary
  directory at all — the old `OUT=` and `make clean` — and the guard that made it safe.
- Preview with `make dev`. It serves every page, `sitemap.xml` and `llms.txt` at the same
  paths Pages will, because the dev server applies the base path too — which also means
  the bare host root is a 404 and the URL the dev server prints for itself leads nowhere.
  There is deliberately no target that serves `web/out`: `next start` refuses outright
  under `output: 'export'`, and any static server would have to re-create the base-path
  prefix before a single asset resolved. The copy buttons need a secure context, so
  `localhost` shows them working and a `file://` open does not.
- **`output: 'export'` is withheld in development, and that conditional is load-bearing.**
  MEASURED in `next/dist/server/dev/next-dev-server.js`: while `output` is `'export'` the
  DEV server throws `Page "/[plugin]/page" is missing param …` for any path that matches a
  dynamic route but was not returned by `generateStaticParams()` — before the component
  runs, so `notFound()` never fires and `not-found.tsx` is unreachable. `make dev` answered
  a stray URL with a `500` and an error overlay instead of the 404 page. The guard is
  spelled `output === 'export'` and consults nothing else, so `export const dynamicParams =
  false` does not lift it; do not add it for this. Withholding the value in dev lets the
  path fall through to the route and reach `notFound()`, which is what a static host does
  by serving `out/404.html` for a path with no file behind it. `next build` sets `NODE_ENV`
  to production, so the build CI runs and Pages publishes always has `output: 'export'` —
  VERIFIED by building both ways and diffing: all 14 exported pages render identical
  markup, and `sitemap.xml`, `llms.txt` and the stylesheet are byte-identical. (The export
  is not byte-reproducible in general — the build id and the RSC row numbering move between
  two runs of the *same* config, so compare rendered markup rather than hashes.)
- `web/out/`, `web/node_modules/` and `web/.next/` are gitignored; the pages are built on
  deploy and never committed. `web/package-lock.json` is committed — see
  *Public-repository rules*.
- `site-build` builds on every pull request. It looks for each skill on *its own plugin's
  page*, anchored on the `data-skill="<name>"` attribute its card carries — searching the
  whole site would prove nothing, because the catalog page's plugin card already lists
  every skill name, and a class name is a styling decision that must be free to change.
  It also fails a site-internal path that is missing the base path.
- `setup-node` needs `cache: 'npm'` **and** `cache-dependency-path: web/package-lock.json`
  in every job that installs: its default search looks for a lockfile at the repository
  root, where there is none.
- `pages.yml` publishes once CI passes on `main`, so merging the release PR is what
  republishes the site and a merge to `develop` publishes nothing. A release whose guards
  failed publishes nothing either; deploying anyway, after a CI outage rather than a real
  failure, is `workflow_dispatch`.
- This repository's Pages source is GitHub Actions, and `pages.yml`'s build job is gated
  on `github.event.repository.fork == false`, so a fork publishes nothing. A fork's copy
  would carry this repository's analytics beacon token and canonical URLs — both are
  inlined into the export — so a second live copy reports into the same Cloudflare
  property. Whether a fork enables Pages at all is outside this repository's reach; the
  workflow that would fill it is not. A fork meant to publish deletes that condition
  deliberately.
- The catalog page repeats the README's legal notices verbatim. Keep the two in step, and
  do not soften them here either.

## Versioning and release

**Plugins version independently, and versions move only on the release PR.** Work
merges to `develop` with version strings untouched. To release: take the release PR —
`release-pr.yml` opens or refreshes it Mondays 00:00 UTC while `develop` is ahead,
`workflow_dispatch` any time — read `git diff main...develop` plugin by plugin, and
commit one bump per touched plugin to `develop` at the level the table below picks.
Merging that PR is the release — no tag to cut, no second repository to bump. A change
confined to one plugin leaves the others' version strings alone, so their installed
users are not disturbed.

**One question picks the level: does a consumer that calls this plugin by name have to
read the diff before taking it?** Skills are called by name and nothing here references
them, so what breaks is a name that disappeared or a shape that changed — never an
import a checker could follow.

| Level | When | Triggers |
|---|---|---|
| major | something a consumer names is gone or means something else | a skill renamed or removed; a contract surface changed (recipe IDs, profile fields, an output shape a consumer parses); an MCP server or tool renamed; a **required** `userConfig` field added |
| minor | purely additive | a new skill; a new MCP tool; an **optional** `userConfig` field |
| patch | everything else | a body edit that preserves observable behaviour; a new `references/` file; description wording; a template fix; a typo |

A skill's body is its behaviour, so preserving observable behaviour is the whole of what
makes a body edit a patch: change what a skill emits or how it is invoked and that is
the contract-surface row, however small the diff looks. `references/` is loaded by the
owning skill and named by nobody else, which is why adding one is patch and not minor.

Every change under `plugins/<name>/` moves that plugin's version, down to a typo —
there is no no-bump level, which is where this departs from plain semver. A doc fix
would go unreleased there; here the version string is the update signal, so an unbumped
fix reaches nobody.

**A plugin's own name, and the catalog's, are not version events.** Renaming `msu`, or
renaming `msu-skills`, starts a fresh install identity and ends the stream the old name
published; a major bump announces it to nobody, because nobody is watching the new name
yet. Those are coordinated with consumers rather than expressed as a number.

Merge the release PR with a merge commit. Squashing forks `main`'s history away from
`develop`'s, and every later release PR re-shows diffs that already shipped. The rare
PR that lands on `main` directly bumps its own plugins — `version-bump` gates every
PR into `main` — and is followed by merging `main` back into `develop`, or the next
release PR conflicts on those files.

`version` belongs in `plugin.json` and nowhere else. The catalog entry omits it on
purpose: Claude Code always reads the `plugin.json` value and ignores a `version` in the
entry without warning, so declaring both creates a field that drifts while looking
authoritative. The consequence worth remembering is that the version string *is* the
update signal — push commits without bumping it and installed users keep the cached
copy. CI's `version-bump` job fails a PR into `main` that changes a plugin without
bumping *that* plugin, because nothing else catches it now that the hub's
catalog-agreement check is gone. It compares the two version strings and stops there —
which level was chosen is a judgement made once, on the release PR, by whoever reads the
diff.

`web/package.json` carries a `version` of its own. It is not a release identity and does
not move on a release: the site is not installed, not catalogued, and not depended on, so
nothing reads that string. Both version guards enumerate plugins from `plugins/`, and a
PR touching only `web/` bumps nothing.

Tags are optional. Nothing in the install path reads them — `/plugin marketplace add`
clones the default branch — though a marketplace source does accept a `ref`, so
`claude plugin tag --push` is still there if a pinnable ref is ever wanted.

## Writing skills

How to write one is [CONTRIBUTING.md](CONTRIBUTING.md): the path and the kebab-case
naming, the placement test, repository-wide name uniqueness, the `description` as
matching input, the thin body over `references/`, and the rule against naming
CLI-specific tools. Maintainers write against that document too, so do not restate its
rules here — a rule stated twice drifts.

The README `## Skills` table is inventory on purpose. It is where a browsing user sees
what the catalog holds, which is why it carries a list where this file must not.

Adding a plugin is four files: `plugins/<name>/.claude-plugin/plugin.json`, at least one
`plugins/<name>/skills/<skill>/SKILL.md`, an entry in the catalog pointing at
`./plugins/<name>`, and a README row. Every CI check discovers plugins from the
filesystem, so none of them needs editing.

**This file is not the fifth.** It states rules, not inventory: no sentence here should
count the plugins, name the full set, or describe one as the only. Naming a plugin is
fine where it is the subject — `msu` owns `maple-lookup`, and that stays true as the
catalog grows — but write anything else against `<plugin>`. If adding a plugin forces an
edit here, the sentence it forced was keeping a roster, and the fix is to rewrite that
sentence rather than update the count.

## Public-repository rules

- **Do not name unreleased NEXPACE products** in any committed file, including this
  one. Refer to them as "product-specific skill sets" or "downstream plugins". Public
  release timing differs per product and this repo is already public.
- README carries the legal notices (API terms, model-training prohibition, credential
  handling). Do not drop or soften them when restructuring.
- README is English. Keep committed prose in English for consistency.
- **`web/package-lock.json` is committed, and both workflows install with `npm ci
  --ignore-scripts`.** `ci` installs exactly what the lockfile pins instead of
  re-resolving, so the published site is built from the dependency tree that was reviewed.
  `--ignore-scripts` blocks every dependency's install hooks, which is what keeps a
  transitive package from running code of its own in the Pages job — that job holds
  `pages: write` and `id-token: write`. The app needs no install script; the export builds
  under the flag.
