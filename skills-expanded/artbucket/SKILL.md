---
name: artbucket
description: Use the brand's asset library (artbucket) whenever work touches the brand - making anything with its colors, logo, type or tone, finding or embedding an image, logo or font, generating an image with any model or design tool, building a landing page, docs or guidelines site, or publishing an asset somewhere. Read the brand rules before making anything, file what you generate with its provenance, and check a use or a build before it ships.
---

# artbucket

artbucket holds the brand: its assets (logos, photos, fonts, generated images) and its rules (colors,
logo use, type scale, tone), per context. Treat it as the source of truth. Never guess a hex code, a
font or which logo to use, and never work from a screenshot of the guidelines.

Two ways in, same tools:

- **MCP** (preferred): the `artbucket` server's tools below.
- **CLI**, when there is no MCP here: `artbucket <command>`, signed in with `artbucket login`
  (it opens the browser to approve a code; `ARTBUCKET_URL` picks the server). Add `--json` for
  output to parse. `artbucket --help` lists everything.

## The workflow

1. **Rules first.** Before making anything on-brand, read the rules for the context you are working in:
   `brand_rules({"context": "instagram-story"})` (CLI: `artbucket rules --context instagram-story`).
   Leave the context out for every rule. Each rule has a `value` and a `usage`: follow the usage too.
2. **Find, then describe.** `search_assets({"q": "logo"})`, then `describe_asset` on the one you
   pick: it says what it is, its rights, whether something replaced it, and the brand rules that
   point at it (CLI: `artbucket search logo`, `artbucket describe <id>`).
3. **Hand out URLs, not bytes.** `rendition_url({"id": ..., "width": 800, "format": "webp"})`
   returns a stable, cached URL for exactly that size (CLI: `artbucket url <id> --width 800 --format webp`).
   Renditions never upscale.
4. **Check before it ships.** Before an asset is published, sent or handed out, ask
   `check_use({"id": ..., "channel": "instagram", "territory": "FR", "context": "dark-background"})`
   (CLI: `artbucket check <id> --channel instagram --territory FR --context dark-background`, which
   exits 1 when it may not). `allowed: false` comes with reasons and a `suggest`ion: use that instead,
   and tell the person why.
5. **What you add is a suggestion.** With a propose (Suggest) key, `ingest_asset` and `propose_tags` land
   in Review for a person to approve. `my_proposals` says what they decided and why. Don't treat a proposed
   asset as final. With a write (Edit) key an upload is in the library at once: say so, never that it waits.
   When the person asks you to review, `search_assets({"review": true})` lists what waits, and `review_asset`
   approves or rejects it (a rejection says why, in `note`) and applies or drops suggested tags and values.
   Never approve on your own initiative. What you proposed yourself, the server refuses to let you approve.
6. **A new version is not a new asset.** A redrawn logo or a corrected photo goes in with
   `ingest_asset({"url": ..., "versionOf": "<id of the old one>"})` (CLI: `--version-of`): once approved it
   replaces the old one everywhere, and checks point to it. Expired, archived and deleted assets are not
   served: their URLs answer 410, so never hand one out.

## Filing what a model made

Anything generated (by you, or by a tool you called) goes in with its provenance, so people can
tell it from photography and see how it was made:

```
ingest_asset({
  "url": "https://.../image.png",
  "origin": "generated",
  "generator": "recraft-v3",
  "prompt": "Four line icons for ... in #1A2B3C on white",
  "parentAssetId": "<the library asset it started from, if any>"
})
```

CLI: `artbucket ingest ./image.png --origin generated --generator recraft-v3 --prompt "..."`.
A local file works with the CLI; the MCP tool takes a public http(s) URL.

## Generators and design tools (Canva, Adobe, Recraft, Ideogram, Krea, ChatGPT, Gemini)

These have their own MCP servers or live in the chat; they can't call artbucket. You carry things
between them:

1. `brand_rules` for the context: palette, type, logo rules, tone.
2. Put them in the generator's prompt as exact values: hex codes, font names, what never to do.
   If it takes a reference image, pass a `rendition_url` of the logo or a brand photo.
3. Ingest the result with `origin: "generated"`, the `generator`, and the prompt you used.
4. `check_use` it for where it will run before you say it's ready.

## Building the brand's guidelines

A brand's guidelines are pages people read (and portals publish), laid out over its rules. You can build
them end to end over MCP, or with the CLI (`artbucket templates`, `pages`, `page save`, `page edit`,
`theme set`, `publish`). It takes a key with write on the project; publishing also takes the share ability.

Start with `brand_status`: it names every brand and lists what the one you work on still lacks (colors,
typefaces, logo, voice, pages, a publish, a portal), each step with the tools that do it. Take `next`
first, and ask again after each change until every step is done or only the person's decisions are left.
A new brand (a sub-brand, a product line) is `create_brand({"name": "Acme Kids"})`, empty, or with
`from` a copy of another brand's rules, pages and theme; `update_brand` renames one or makes it the default.
Group assets with `create_collection` and `update_collection_assets`; `list_collections` gives the ids that
`ingest_asset` and `create_site` take.

1. **Rules are the content.** `set_rules` makes or changes many at once: `{ key, type, value, usage }`,
   with keys like `color.primary`, `type.heading`, `logo.minSize`, `tone.avoid`. Name do and don't lists
   `always`/`do` and `never`/`avoid`/`dont`: pages show them green and red. Give a rule a `label` for the
   heading readers see (the key never changes), and a `spec` for what the value can't say: a color's
   CMYK, Pantone and tints, a gradient (`spec.gradient` stops name color rules; `value` is its solid
   fallback), a number's `unit`, a font's `role`, `tracking` and `case`.
2. **Pages are the layout.** Read `list_templates` (each template comes with an example), then
   `save_page` a whole page: sections top to bottom, each a template (cover, text, split, palette, type,
   logos, dodont, gallery, collection) with the `keys` of the rules it shows. A `collection` section shows
   live assets from a collection, a saved search or a `query` (`type=image&tag=campaign&f.channel=web`).
   For a brand with rules and no pages, `generate_pages` lays out a start (write the rules first: with none, it makes a cover and warns).
3. **Build a tree.** `parent` puts a page under another, three levels at most: Overview, then Identity
   with Color, Logo and Type under it. Renaming a page (`edit_page` with `{ "op": "page", "set": { "slug": ... } }`)
   keeps the old slug working. A home or campaign page takes `layout: "landing"` (no nav column,
   on-this-page or pager); every other page reads as a chapter (`book`, the default).
4. **Items and tones.** `items` are what a template lists: on `dodont`, a do or a don't with its picture
   (`{ "verdict": "dont", "asset": "<id>", "title": "Stretch it" }`); on `gallery`, a picture with its caption.
   `tone` sets a section's ground: `plain`, `tint`, `brand`, `panel`, `dark`, `color` (with
   `background.color`, a color rule), `image` (with `background.image`) or `pattern`.
5. **Never copy a value into a page.** A section binds rules by key: change a color with `set_rules` and
   every page follows. Page text (`title`, `body`, `lede`) is for what isn't a rule: an intro, the why.
6. **The theme is the look.** `set_theme` maps rules to parts (`accent`, `surface`, `ink`, `head`,
   `body`, `logo`) and sets `radius`, `width`, `density`, `nav`, `numbering`. It merges; `null` clears a
   setting. `get_theme` shows what is set.
7. **Every problem comes back at once**, each with its path (`sections[2].keys[0]: no rule "color.primery"`).
   Fix them all and save again. `edit_page` changes a few sections without resending the page.
8. **Check, then publish when asked.** Every write returns `warnings` (a link to no page, a key with no
   rule) and a `url` to open the page as readers see it; `get_page` returns the page as Markdown too. Edits
   are drafts. Publish only when the person asks, with a `note` saying what changed for readers (and an
   `image` beside it if one helps). Every change is in the brand's history, and a person can restore any version.
9. **Portals show the publish, never the draft.** `publish` answers with the portals now showing the brand.
   With a key that manages portals, `create_site` makes one for the brand (`access` members, password with the
   password the person gives you, or public once the person says so; `theme` for its logo and colors), and
   `list_sites` says which brands each shows (`publishedAt: null`: never published, so visitors see nothing),
   and `update_site` changes anything about it: brands, access and password, theme, closing date and site
   (footer, quick grab, terms, listed); `site` replaces the whole set, so send back what `list_sites` gave.
   Requests to get in wait in `list_site_requests` for `decide_site_request`.
10. **Comments and history.** Before publishing, `list_comments` for open threads; answer with `add_comment`
   and resolve with `update_comment`. `list_versions` shows the history; `restore_version` undoes a bad change
   as a new version, never losing anything.

## Building a site

A landing page, docs or a guidelines site you build yourself, in any framework that outputs static
files, is published to a site of its own, or beside a brand portal at a path. Deploying takes a key
that manages sites; checking, a read key.

1. **Build from the brand.** With a terminal, `artbucket site new <folder> --brand <slug> --kind docs`
   starts one (landing, docs or guidelines) that builds from the brand's release and deploys with
   `npm run deploy`; `artbucket brand export` gives any other build the release as files. Read
   `brand_rules` first, as above. Put assets in by their rendition
   URLs, `/c/{id}/w_800,f_webp` (from `rendition_url`), not as copied files: `/c/` follows the current
   version, so a new logo reaches the site with no rebuild. A file you copy in anyway is known by its
   bytes and checked the same.
2. **Check it before it ships.** `check_site({"files": [{"path": "index.html", "content": "..."}]})`,
   with `"base64": true` for images and fonts, answers what the build uses and every problem, each
   naming the file and what to use instead. Nothing is stored. Fix them all and check again. CLI:
   `artbucket site check dist`, which exits 1 on a problem. A site hosted elsewhere (Vercel, Netlify,
   GitHub Pages) stops here: put the CLI check in its CI.
3. **A site to publish to.** Take one `list_sites` names, or make one:
   `create_site({"name": "Acme docs", "kind": "docs", "access": "members"})` (`landing`, `docs`,
   `guidelines` or `storybook`). Members means the people of the project, signed in; make it public
   or set a password only when the person says so.
4. **Deploy.** `deploy_site({"address": "acme-docs", "files": [...]})` checks it again, puts it live and
   answers its `url`; the build before stays to restore. `path` (`"/docs"`) mounts a build beside a
   brand portal's pages. A refused deployment says why. A `held` one waits for whoever runs the
   server: tell the person it isn't live yet, and why. CLI: `artbucket site push dist --site acme-docs`.
5. **Redirects and headers** are files at the build's root, `_redirects` and `_headers`, in the
   Netlify and Cloudflare Pages format: a single-page app's `/* /index.html 200`, a moved page's 301,
   a header per path.
6. **Hand over the `url`**, and say who can open it.

## A brand kept as files

When the repository holds the brand (a `brand.yaml` with `rules/` and `pages/` beside it), edit those
files rather than the pages over MCP: the folder is what people review and push.

1. `artbucket brand diff brand` after each edit: every problem at its file and line, and what a push would
   change, down to each section. It exits 1 on errors.
2. `artbucket brand push brand` sends it. What people changed in the app since your last pull stays; where
   you both changed the same piece, yours wins and push says so.
3. `artbucket brand pull brand` brings in what changed in the app. It never writes over a file you changed
   and haven't pushed: push first.
4. Leave a section's `id` out unless something links to it: a new one is named after its template. Quote
   colors, `value: "#1f6feb"`: in YAML `#` starts a comment.

Publish only when the person asks: `artbucket brand push brand --note "What changed"`.

## Fonts

A brand rule may name a Google font that isn't in the library yet: `import_google_font({"family": "IBM Plex Sans"})`
adds every style, proposed like any upload.

## Icons

For icons the library doesn't have, `find_icons({"q": "outline"})` finds open source sets (with their license
and author), and `find_icons({"prefix": "tabler", "q": "arrow"})` a set's icons by name. Keep to one set, and
check its license suits the use. `import_icons({"prefix": "tabler", "icons": ["arrow-right", "search"]})` adds
them, one SVG each, proposed like any upload.
