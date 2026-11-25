---
name: litestartup-publish
description: >
  Publish blog posts, documentation, website pages, changelogs, and send emails
  via LiteStartup. Use when the user asks to publish content, sync a repo,
  write a blog post, send an email, or bind a content repository.
metadata:
  author: litestartup-com
  version: "1.3.5"
---

# LiteStartup Publish Skill

Publish content to [LiteStartup](https://litestartup.com) from your editor.
Git repo is the source of truth → sync to production in one command.

## Security

- API keys stored at `~/.litestartup/credentials` — scripts read internally
- **NEVER** read, display, or echo the key in conversation
- If auth fails → tell user to re-run bind flow (see `references/bind.md`)

## Prerequisites

**First, ensure a key exists.** If `~/.litestartup/credentials` is missing or empty, the user
hasn't connected to LiteStartup yet → run `references/init.md` (terminal onboarding: email →
claim code → key, no browser) before doing anything else. Never ask the user to paste a key.

Then check for `litestartup.yaml` in workspace.
- Found → this is the content repo, proceed with requested action
- Missing → the user has no content repo yet. Offer two paths:
  - **Default (recommended, one key only)**: create an LS-managed site on LiteStartup's
    hosted Git (private repo, push-to-publish, no GitHub/OAuth) — see `references/create.md`
  - **Bring your own GitHub public repo**: bind it — see `references/bind.md`

## Shared conventions (read FIRST, every time)

Before writing or editing **any** content — website, blog, docs, changelog, campaigns,
and any future content type — load these two repo-root files and apply them:

- **`shared.yml`** — the single source of truth for facts: identity (name/tagline),
  `facts` (product_version, pricing, urls, contact), and `terminology`. Use these values
  verbatim; never hardcode a fact that lives here, and never contradict another page.
- **`content-guide.md`** — voice, tone, terminology usage, and formatting conventions.

Both live at the repo root, are version-controlled, and are **non-secret** (API keys stay
in `~/.litestartup/credentials`, never in the repo). They are metadata — the server never
publishes them. If they are missing (older repo), offer to create them from
`assets/shared.yml` + `assets/content-guide.md`.

See `references/shared-conventions.md` for the field reference and the sync-time
consistency check.

## Capability Router

When the user makes a request, determine intent and load the relevant file:

| User Intent | Load | Script (Linux/macOS fallback) |
|-------------|------|------|
| "connect", "sign up", "get me a key", no key yet at `~/.litestartup/credentials` | `references/init.md` | (public onboarding; REST) |
| "register a domain", "buy acme.com", "get me a domain" | `references/domain.md` | (REST; charges balance — confirm first) |
| "launch/create a site", "new website/blog/docs", "start a site", "register domain + site" | `references/create.md` | (REST API; managed Gitea — default path) |
| "go live", "launch the site", "make it reachable", "add an inbox / email address" | `references/go-live.md` | (REST API) |
| "bind", "connect repo", "unbind", "list domains" | `references/bind.md` | `scripts/ls-bind.sh` |
| "publish", "sync", "deploy" | `references/sync.md` | `scripts/ls-sync.sh` |
| "send email", "send notification", "email someone" | `references/email.md` | `scripts/ls-send-email.sh` |
| "send campaign", "email campaign", "bulk email", "newsletter" | `references/campaign.md` | (uses sync) |
| "status", "what's synced" | `references/status.md` | `scripts/ls-status.sh` |
| "keep content consistent", "update pricing/version everywhere", shared facts/voice | `references/shared-conventions.md` | (shared.yml + content-guide.md) |

Scripts are Linux/macOS fallbacks. On Windows, call the REST API directly — each reference
documents the agent-native path.

When the user wants to **write content**, load the relevant reference:

| Content Type | Load | File Extension |
|-------------|------|----------------|
| Documentation | `references/docs.md` | `.md` (in `docs/{lang}/`) |
| Blog post | `references/blog.md` | `.md` (in `blog/`, translations in `blog/{lang}/`) |
| Changelog | `references/changelog.md` | `.md` (in `changelog/`, translations in `changelog/{lang}/`) |
| Website page | `references/website.md` | `.html` (in `website/`) |
| Campaign email | `references/campaign.md` | `.md` (in `campaign/`) |

After writing → run sync (`references/sync.md`).

## Content Repo Layout

```
<content-repo>/
├── litestartup.yaml          ← Binding config (created by `create` for managed, or `bind` for BYO)
├── blog/                     ← Blog posts (markdown → HTML by server)
│   ├── *.md                  ← Default language → /blog/{slug}
│   └── {lang}/*.md           ← Translations → /blog/{lang}/{slug}
├── campaign/*.md             ← Email campaigns (markdown → HTML, sent to tag contacts)
├── website/                  ← Website pages (raw HTML, Tailwind CSS)
│   ├── index.html            ← Homepage (type: website, full HTML)
│   ├── *.html                ← Root block pages (/pricing, /about, etc.)
│   ├── products/*.html       ← Product pages (/products/workmail, etc.)
│   ├── {lang}.html           ← Language root → /{lang} (owns localized partials)
│   └── {lang}/*.html         ← Localized pages → /{lang}/{page}
├── data/*.json               ← JSON data files for data-driven website pages
├── changelog/                ← Release changelogs (markdown → HTML)
│   ├── *.md                  ← Default language → /changelog
│   └── {lang}/*.md           ← Translations → /changelog/{lang}
└── docs/                     ← Documentation (Litestartup Docs format)
    ├── config.json           ← Docs site config
    └── {lang}/               ← Language dirs (en/, zh/, etc.)
        ├── _nav.md           ← Top nav tabs
        ├── _sidebar.md       ← Left sidebar
        └── **/*.md           ← Doc pages
```

**Language rule**: the language segment follows the module segment — `/blog/zh`,
`/changelog/zh`, `/docs/zh/...`. The website module has no module segment, so its
language sits at the site root (`/zh`, `/zh/plugins`). The default language always
lives in the module root, never in an `en/` directory.

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Key expired/invalid | Re-connect via `init.md`, or re-store a valid key |
| 402 | Insufficient balance (domain purchase) | Tell user to top up; do NOT auto-retry |
| 403 | Missing scope | Key needs `system.publish` |
| 404 | No binding | Create a managed site (`create.md`) or bind a repo (`bind.md`) |
| 409 | Already bound / pending order | Informational, not an error; do NOT double-charge |
| 410 | Onboarding code expired/used | Request a new code (`init.md`) |
| 422 | Sync/parse failed | Check file structure against spec |
| 429 | Rate limited | Wait. Do NOT auto-retry |

## DO NOT

- Read or display API keys
- Write content without first applying `shared.yml` + `content-guide.md`
- Put secrets (API keys) in `shared.yml` or anywhere in the repo
- Modify files outside the content repo
- Auto-publish without `git push`
- Auto-retry failed operations
- Write website pages as markdown (they are HTML)
- Write docs without `_sidebar.md` (required for navigation)
- Use query params for language URLs (use path: `/docs/en/...`, `/blog/zh`)
- Put the default language in an `en/` directory (it belongs in the module root)
- Name a blog post or changelog entry after a language code (`blog/zh.md`)
- Choose website page type without asking user (website vs block)
