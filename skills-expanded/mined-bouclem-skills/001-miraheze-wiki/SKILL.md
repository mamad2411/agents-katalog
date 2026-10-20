---
name: miraheze-wiki
description: Helps an AI assistant work with the Miraheze wiki farm — writing wiki requests that get approved, navigating ManageWiki, doing common how-to tasks (templates, skins, permissions, custom domains, backups), writing regex for MediaWiki search-and-replace, AND writing actual article and page content for Miraheze-hosted wikis. Miraheze does NOT ban generative AI; AI-written content is permitted (subject to per-wiki rules). MADE BY SQERSTERS
risk: safe
source: community
version: 1.1.0
license: MIT
---

# Miraheze Wiki

## Purpose

This skill teaches an AI assistant how to help users work with **Miraheze**, a non-profit MediaWiki-based wiki farm. It covers the full lifecycle:

- Requesting a wiki and getting it approved.
- Setting it up via `Special:ManageWiki`.
- Editing it (pages, templates, skins, permissions, namespaces).
- **Writing actual article and page content** for the wiki.
- Doing regex-based maintenance.
- Operating within global community norms.

> ⚠ **Important:** Unlike Wikipedia, **Miraheze does not forbid LLM-generated content.** The May 2025 Generative AI RfC closed with all proposals to ban or restrict AI rejected, except one that simply **recommends a comment disclosing AI-generated code**. So this skill *is* the right tool for an AI to use when writing real pages for a real Miraheze wiki — within whatever local policy that specific wiki has set.

When this skill is active, the assistant must:

- Treat Miraheze as a **community-run, donation-funded** project — not a commercial host.
- Respect that **wikis are owned by their community**, not by individuals.
- Know the difference between **global policies** (apply everywhere) and **local policy** (each wiki decides — including any local AI rules).
- When it writes CSS, wikitext, or Lua for a wiki, **add an inline comment noting it was AI-generated** (recommended by the Content Policy as of 2025-05-28).

---

## Core Rule

When helping with Miraheze, identify which layer the task is on:

1. **Farm layer** — request a wiki, custom domain, Phorge ticket, contacting Stewards.
2. **ManageWiki layer** — extensions, skins, permissions, namespaces (no `LocalSettings.php`).
3. **MediaWiki layer** — pages, templates, modules, regex, gadgets.
4. **Content layer** — writing actual article/page content for the wiki.
5. **Community layer** — local consensus, bureaucrats, Stewards' role, dispute resolution.

If the user mixes layers (e.g. *"How do I install an extension?"* — farm or local?), clarify before answering. Many tasks have a different answer at each layer.

For the **content layer** specifically: pair this skill with `wikipedia-like-writing` if the user wants encyclopedic-style articles. The two skills are designed to compose.

---

## What Miraheze is

- A **non-profit wiki farm** running MediaWiki, hosting ~24,000 wikis.
- Run by **volunteers**, not staff. Key roles:
  - **Stewards** — global community leadership, intervene in cross-wiki issues.
  - **System administrators** — keep the technical infrastructure running.
  - **Wiki reviewers** — approve or decline wiki requests.
  - **Board of Directors** — WikiTide Foundation, the 501(c)(3) backing Miraheze.
- Funded **only by donations**. No ads. Editorial independence is a stated principle.
- Wikis cannot be created instantly — every wiki must be **requested and reviewed**.

---

## Requesting a wiki

The number-one task users ask about. A wiki request goes through `Special:RequestWiki` and is reviewed by the CreateWiki AI or a wiki reviewer.

### Pre-flight checks

- Read the Content Policy. Make sure the wiki concept complies.
- Check `Special:WikiDiscover` and the gazetteer — there may already be a wiki on the same topic.
- Check the desired subdomain isn't taken.
- **Limit:** 1 wiki request per user per week.

### The request form

| Field | What to put |
|---|---|
| Subdomain | Specific to the topic. *galapagoswildlife.miraheze.org* — not *wiki7.miraheze.org*. |
| Wiki name | Descriptive. *Galapagos Wildlife*, not *Galapagos*. |
| Language | The primary language of the wiki. |
| Category | Pick the closest fit (Art, Education, Gaming, History, etc.). Avoid "Uncategorised". |
| Private? | Tick only if the wiki should be member-only. |
| Subjects = real people/groups? | Tick if yes. |
| Purpose | Closest match (encyclopedia, documentation, fictional worldbuilding, RPG, etc.). |
| **Description** | The most important field. Cover purpose, scope, and topic. |

### What a description must contain

- **Purpose** — *"This wiki is intended to be a repository for encyclopedic articles on the ecosystem of the Galapagos Islands."*
- **Scope** — *"Articles will cover the islands' animals and plants, including some history, travel, and conservation information."*
- **Topic** — *"The Galapagos Islands are famous for their diverse wildlife (including giant tortoises and finches), studied by Charles Darwin…"*

### Good vs bad descriptions

✅ Good: *"This wiki will document the online video sharing service YouTube. It will document its history, content creators, achievements, and the videos hosted on it. Most pages will be about popular YouTubers, popular videos, and important events."*

✅ Good (short but complete): *"This wiki will be all about wikis. It will document wikis with at least 50 pages, as well as wiki farms and wiki engines, all from an encyclopedic point of view."*

❌ Bad: *"I want to archive fandom events."* — no scope, no topic.

❌ Bad: *"A wiki for my imaginary world."* — no detail at all.

❌ Bad: *"I want a wiki."* — guaranteed decline.

### Common decline reasons

1. Generic or irrelevant subdomain.
2. Wiki name doesn't match the wiki concept.
3. Wrong category.
4. Wrong purpose dropdown.
5. Description is too short or too vague.
6. Concept appears to violate the Content Policy.
7. Concept is likely to cause drama or harassment.

When a request is declined, **the user can edit and resubmit** via the request page's "Edit request" tab. Do not encourage giving up.

### Status terms

- **In Review** — queued.
- **Needs more details** — check the review comments and edit.
- **On hold** — second wiki reviewer needed.
- **Approved** — wiki is created at `subdomain.miraheze.org`.
- **Declined** — check the comments and try again.

---

## After approval — first steps

1. Check email / on-wiki notification for confirmation.
2. Visit the wiki. The default Main Page should be replaced with real content.
3. Open `Special:ManageWiki` to:
   - Pick a default skin (Cosmos for a Fandom-like look on mobile + desktop).
   - Enable extensions you need.
   - Configure permissions and namespaces.
4. There is **no `LocalSettings.php` access** — all configuration is via `Special:ManageWiki`.

---

## ManageWiki — what you can configure

Five sections:

| Section | What it does |
|---|---|
| Core settings | Site name, default skin, language. |
| Additional settings | Per-extension config exposed by Miraheze. |
| Extensions and skins | Enable/disable, no install needed. |
| Permissions | Who can do what (groups, individual rights). |
| Namespaces | Add, rename, delete custom namespaces. |

Bureaucrats can edit ManageWiki. Be careful who you grant the right to.

---

## How-to topics — quick router

Map common requests to the right page on Miraheze Meta.

### Setup and migration
- Write a wiki request → `Guide_to_writing_wiki_requests`
- Move a wiki *to* Miraheze → `Moving_a_wiki_to_Miraheze` (XML dump + image dump)
- Move a wiki *off* Miraheze → `Help:How_to_move_my_wiki_from_Miraheze`
- Custom domain → `Custom_domains`

### Editing and pages
- New page, edit, templates, infoboxes, Lua modules, multilingual support, interwiki links → all under `How-to_guides`
- ⚠ **Don't blindly import templates from Wikipedia** — they have heavy dependencies. Use `dev:Category:Templates` for simpler, well-documented Miraheze templates.

### Customisation
- Skins: change in ManageWiki → `Default Skin`. **Cosmos** is the Fandom-like skin and works on mobile.
- More styling: edit `MediaWiki:<skinname>.css` per skin, or `MediaWiki:Common.css` for all skins.
- Logo / favicon → ManageWiki page.
- Dark mode improvements, mobile-friendly tweaks, JavaScript gadgets → all have help pages.

### Permissions and access
- Restrict editing → `Special:ManageWiki/permissions`. Remove `edit` from the `*` (everyone) group.
- Moderate edits before publishing → enable the **Moderation** extension.
- Lock pages → enable **AuthorProtect** or **LockAuthor**.
- Read-only mode → enable the **Protect Site** extension.
- Add a user to a private wiki → `Special:UserRights`, add to `member` group. The user must visit the wiki at least once for their account to exist locally.

### Hiding content
- Detailed access restrictions are **not natively supported** by MediaWiki. Most "private page" hacks are insecure. If you really need this, use a different content management system.
- Spoilers → import `Template:Spoiler` from `dev.miraheze.org` or enable the Spoilers extension. For collapsing arbitrary content, use MediaWiki's built-in collapsible elements.
- NSFW → there is a separate compliance guide; refer the user to it.

### Search engines
- Register a search console with Google/Bing.
- Set up the **WikiSEO** extension.
- Optimise content following the SEO improvement draft.

### Backups
- Local administrators: `Special:DataDump` to request a backup.
- Larger exports: open a Phorge ticket.

### Closing / deleting
- Close: `Special:ManageWiki` → tick "Closed".
- Auto-close: governed by the **Dormancy Policy** (since 5 January 2016) for inactive wikis.
- Delete: `Steward requests/(Un)deletions`. Multi-contributor wikis need a local discussion with consensus first.

---

## Phorge — when to use it

**Phorge** is Miraheze's task tracker for technical issues that ManageWiki can't handle. Use it for:

- Configuration changes not exposed in ManageWiki.
- Technical bugs.
- Large data exports.

Don't use it for general support (CSS help, "how do I do X?"). Those go to the Help desk, Discord, or IRC.

To sign in to Phorge: click the MediaWiki logo on the sign-in page. Phorge is separate software but integrated with Miraheze accounts.

---

## Custom domains

Available if you own a domain. The wiki keeps its `miraheze.org` subdomain internally; the custom domain becomes the canonical URL via DNS pointing. See the `Custom_domains` page for the DNS setup.

---

## Governance — who decides what

| Layer | Who decides |
|---|---|
| Local content, local rules | Local community (consensus) |
| Local admins/bureaucrats | Elected by the local community where possible |
| Cross-wiki disputes | Stewards |
| Global rules (Conduct, Privacy, Content, Terms) | Global community + WikiTide Foundation |
| Server / technical | System administrators |

**Wikis are owned by their community.** No single person owns a wiki and acts as a dictator. Bureaucrats have authority but should not override local consensus on a whim.

**Consensus is not a vote count.** A well-reasoned argument outweighs ten one-line "I like it" votes.

**Stewards rarely intervene** in editorial disputes. They handle:
- Wikis without active local admins.
- Severe Global Conduct Policy violations.
- Sockpuppetry, CheckUser, Oversight (private info).
- Rights changes (promote/demote admins) where there's no local bureaucrat.

If you have a dispute:
1. Talk to the user.
2. Raise it with a local admin.
3. If unresolved and a global policy is involved, email `stewards@miraheze.org` or use the Stewards requests page.

---

## Regular expressions on a wiki

Regex is heavily used on Miraheze for search-and-replace tasks. The main contexts:

- WikiEditor's search and replace.
- The **MassEditRegex** extension.
- The **CirrusSearch** extension.
- Pywikibot's `replace.py`.

### Practice rule

Use [regex101.com](https://regex101.com/) when building any non-trivial regex. Test against real wikitext before running it.

### Core building blocks

| Pattern | Meaning |
|---|---|
| `[Ff]oo` | Character class — match `F` or `f`. |
| `(F\|f)oo` | Alternation — same effect, but supports multi-char options like `a(bb\|cc)d`. |
| `\{` `\}` | Escape special characters. |
| ` ?` | Optional space. |
| `*` | Zero or more of the preceding token. |
| `\s` | Any whitespace (space, newline, tab, CR, FF, VT). |
| `(...)` | Capture group — referenced by `\1` in the pattern, `$1` in replacements. |
| `(?=...)` | Lookahead — match without consuming. |

### Worked example: rename a template

Goal: replace `{{foo}}` with `{{Bar}}`, but **not** the word *foobar2000* in prose.

Steps to build the regex:

1. Match `{{` followed by `F` or `f`: `\{\{[Ff]oo`
2. Allow optional space: `\{\{ ?[Ff]oo`
3. Allow any amount of whitespace including newlines: `\{\{\s*[Ff]oo`
4. Allow optional `Template:` prefix: `\{\{\s*([Tt]emplate:)?\s*[Ff]oo`
5. Don't match `foo2` or `foo test` — use lookahead so we don't consume the next character: `\{\{\s*[Ff]oo(?=\s*[|}])`

Replace with `{{Bar`. The lookahead leaves the `|` or `}` intact so the existing template arguments remain valid.

### Worked example: clean up `[[Foo|Foo]]` → `[[Foo]]`

Pattern: `\[\[(.*)\|\1]]`
Replacement: `[[$1]]`

The capture group `(.*)` matches the article name, then `\1` requires the same string to appear after the pipe. `$1` in the replacement reuses it.

### Regex flavors

Different tools use slightly different syntax:

- PHP-style (MassEditRegex) — backslash references in pattern, dollar in replacement.
- Python (Pywikibot) — its own quirks for named groups and flags.
- GNU `sed` — its own `\(...\)` rules.

When in doubt, read the docs for the specific tool. LLMs often get regex wrong — always validate on regex101 before running on real data.

---

## Writing pages and articles for a Miraheze wiki

Because Miraheze permits AI-generated content, this skill is also the right tool for actually drafting pages on a Miraheze wiki. Here's how to do it well.

### 1. Match the wiki's tone

Miraheze hosts ~24,000 wikis with wildly different conventions. Before writing, look at:

- The wiki's existing top pages — what voice do they use?
- The Main Page — does it set any editorial standards?
- The wiki's About / Rules / Manual of Style page if one exists.
- The wiki's category — fan wikis sound different from documentation wikis from worldbuilding wikis from class projects.

Match what's already there. Don't impose Wikipedia's neutral tone on a fan wiki that uses an enthusiastic in-universe voice, and don't write fan voice on a documentation wiki.

### 2. Pick the right shape

| Wiki type | Page shape |
|---|---|
| Encyclopedia (general or specialized) | Lead → body sections → references. Use the `wikipedia-like-writing` skill. |
| Fictional worldbuilding / RPG | Infobox → in-universe description → out-of-universe notes. |
| Software documentation | Overview → installation → usage → API/reference → troubleshooting. |
| Hardware documentation | Overview → specs (table) → setup → troubleshooting. |
| Class / group project | Whatever structure the project uses — ask. |
| Fan wiki (game, show, book) | Infobox → appearances/history → relationships → trivia. |
| Eurovision-style song contest | Stats tables, season-by-season layout. |

When unsure, open three or four existing pages on the same wiki and copy the pattern.

### 3. Use MediaWiki conventions properly

- **Headings** start at `==` (level 2). The page title is implicitly level 1.
- **No links inside headings.**
- **First mention of the page title** is in `'''bold'''`.
- **Internal link**: `[[Target page]]` or `[[Target page|display text]]`.
- **External link**: `[https://example.com display text]`.
- **Templates**: `{{TemplateName|arg1|arg2=value}}`. Don't blindly copy Wikipedia templates — they often have heavy dependencies. Use `dev:Category:Templates` for simple Miraheze-friendly versions, or build a small custom one.
- **Categories** at the bottom: `[[Category:Whatever]]`.
- **Interwiki links**: `[[wikipedia:Article]]`, `[[w:c:fandom-wiki:Page]]` etc.

### 4. Citations and verifiability

Outside encyclopedic wikis (where Wikipedia-style citations are expected), citation needs vary:

- Fan wikis: cite primary works (episode, page number, in-game source).
- Documentation wikis: link to upstream docs and the source repository.
- Worldbuilding / fictional: no citations needed; the wiki itself is the canon.
- Class projects: cite per the assignment's rules.

When in doubt, default to citing — over-citation is rarely a problem on a wiki.

### 5. Disclose AI-generated code

When the page includes CSS, wikitext templates, or Lua modules generated by AI, add a comment:

```css
/* Generated with AI assistance */
```

```html
<!-- Generated with AI assistance -->
```

```lua
-- Generated with AI assistance
```

This matches the recommendation added to the Miraheze Content Policy on 2025-05-28. It is *recommended*, not required, but it's good practice and helps maintainers later.

### 6. Check the wiki's local AI policy

Even though Miraheze permits AI globally, **individual wiki communities can still ban or restrict AI**. Before publishing AI-written content, check:

- The wiki's Main Page or About page.
- A page named *Manual of Style*, *Editing rules*, *Wiki rules*, *Policy*, or similar.
- Recent discussion on the Community portal / Talk:Main Page.

If the wiki has a local AI ban, respect it. If unclear, ask the user. If the user is the wiki's owner, they can decide.

---



**Miraheze does not forbid generative AI.** This was settled by the May 2025 Generative AI RfC and the resulting amendment to the Content Policy (2025-05-28).

### What the Content Policy actually says

The Content Policy has exactly one section about AI, titled *"Coding and Generative AI"*, which says (paraphrased):

> If generative AI/LLM tools are used to create working CSS, wikitext, or Lua, the user is not required to understand the code before using it. It is recommended that users include a disclosure in code comments that the code was AI-generated.

That's the entire farm-wide rule. There is **no ban** on:

- AI-generated article or page content.
- AI-generated translations.
- AI-generated images, logos, favicons, or backgrounds.
- AI-generated JavaScript.
- Using Miraheze content as AI training data.

### Why so permissive — the RfC outcomes

| Proposal | Outcome | Practical effect |
|---|---|---|
| 1. Ban all AI-generated content farm-wide | ❌ Failed (overwhelming opposition) | No ban on AI content. |
| 1A1. Limit ban to Miraheze Meta / Commons / Dev | ❌ No consensus | No ban on official wikis either. |
| 2. AI grammar-fix only with human oversight | ❌ Failed | No specific rule. |
| 3. Ban AI translation into a language you don't know | ❌ Failed | AI translation is permitted. |
| 4. Ban AI-generated images for wiki assets | ❌ Failed | No ban on AI images. |
| 4A1. Same ban for official wikis only | ❌ No consensus | Same — no ban. |
| **5. AI-generated code: disclosure recommended** | ✅ **Passed** | Added to the Content Policy. *Recommended*, not required. Phrasing is "users include a disclosure in code comments". |
| 6. Ban AI-generated JavaScript | ❌ Failed | No ban — but security caution still applies. |
| 7. Ban using Miraheze content as AI training data | ❌ Failed | No ban. |

### Practical guidance for the AI assistant

- **The platform allows AI-written content.** When asked to write articles or pages for a Miraheze wiki, do it.
- **Per-wiki rules still apply.** Each wiki community can set its own AI policy. Before writing for an unfamiliar wiki, check its rules / Main Page / About page for any local AI restrictions. If unclear, ask the user whether the wiki has a local AI policy.
- **For code (CSS, wikitext, Lua):** add an inline comment marking it as AI-generated. Example for CSS: `/* Generated with AI assistance */`. For Lua: `-- Generated with AI assistance`. For wikitext: `<!-- Generated with AI assistance -->`. This matches the recommendation in the Content Policy.
- **For JavaScript:** same disclosure. Be extra careful — JS runs in every visitor's browser. Explain what the code does so the user can review it.
- **For translations:** permitted. It's good practice to mark a page as machine-translated so readers know to expect occasional errors, but this is not required by global policy.
- **For images:** permitted. Be aware that the copyright status of AI-generated images is contested in many jurisdictions; if the wiki cares about clean licensing, recommend that the user uploads with a clear "AI-generated" tag in the file description.
- **The user does not need to "understand" AI-generated code** to use it on their wiki. The Content Policy is explicit on this point.

---

## Common request patterns — quick answers

| User asks | Default answer |
|---|---|
| "How do I create a wiki?" | You request it via `Special:RequestWiki`. Walk them through the form using the description checklist above. |
| "My request was declined." | Read the review comments. Edit the request via the "Edit request" tab. Don't open a new one. |
| "How do I install extension X?" | Check `Special:ManageWiki/extensions`. If not listed, check the Extensions page on Meta. If still not available, open a Phorge ticket. |
| "How do I edit `LocalSettings.php`?" | You can't. Use `Special:ManageWiki`. |
| "How do I make my wiki private?" | `Special:ManageWiki/permissions`, remove `edit`/`read` from `*`. The Main Page is always public though — work around this with a redirect. |
| "How do I add a user to my private wiki?" | They must visit the wiki first to create their local account. Then add them at `Special:UserRights` in the `member` group. |
| "My wiki is being indexed/I want it indexed by Google." | Set up WikiSEO extension and register with the search engine's webmaster tool. |
| "How do I move my wiki to/from Miraheze?" | XML dump + image dump in either direction. See `Moving_a_wiki_to_Miraheze` for inbound, `Help:How_to_move_my_wiki_from_Miraheze` for outbound. |
| "Can I delete my wiki?" | Single-contributor: yes, via `Steward requests/(Un)deletions`. Multi-contributor: needs local consensus first. |

---

## What to refuse / push back on

- Requests to write **fake** wiki request descriptions designed to slip past reviewers.
- Requests to set up wikis that violate the Content Policy (advertising, hate, doxxing, sexualisation of minors, NSFW without compliance).
- Requests to generate JavaScript without explaining what it does — JS runs in every visitor's browser. Generate it, but always walk through the logic so the user can review it.
- Requests to import complex Wikipedia templates wholesale without checking dependencies.
- Requests to bypass Stewards / global policy through technical workarounds.
- Requests to write content for a wiki whose **local** policy bans AI when the user isn't authorized to override that policy.

---

## Sources

This skill is distilled from these Miraheze Meta pages:

- [FAQ](https://meta.miraheze.org/wiki/FAQ)
- [Guide to writing wiki requests](https://meta.miraheze.org/wiki/Guide_to_writing_wiki_requests)
- [Creating a wiki (disambiguation)](https://meta.miraheze.org/wiki/Creating_a_wiki)
- [How-to guides index](https://meta.miraheze.org/wiki/How-to_guides)
- [Help:How to write regular expressions](https://meta.miraheze.org/wiki/Help:How_to_write_regular_expressions)
- [Requests for Comment / Generative AI policy](https://meta.miraheze.org/wiki/Requests_for_Comment/Generative_AI_policy)
- [Content Policy](https://meta.miraheze.org/wiki/Content_Policy) — specifically the "Coding and Generative AI" section added 2025-05-28.

Content was rephrased and condensed for compliance with licensing restrictions. Source pages are CC BY-SA 4.0.
