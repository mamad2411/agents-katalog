---
name: markpdf
description: Convert Markdown to premium-themed PDFs, slide decks (PPTX/PDF), styled HTML, and shareable links via the MarkPDF MCP server. Use when raw Markdown isn't enough — reports, pitches, academic papers, résumés, decks, printable docs.
---

# MarkPDF Skill

MarkPDF turns Markdown into **production-grade** PDFs, decks, and HTML through a hosted MCP server. This skill teaches Claude:

1. The **default opinionated workflow** (what to do when the user just says "make a PDF")
2. The **decision tree** for variations (custom theme, sharing, password, email gate, etc.)
3. The **OS-aware delivery step** (auto-open the result when possible)

> **Read `references/workflows.md` for the full playbook with copy-paste recipes.** This file is the index + golden rules.

## When to use this skill

Trigger on requests like:
- "Make this a PDF / printable / executive report / brochure"
- "Turn this into slides / a pitch deck / a PowerPoint / a Marp deck"
- "Style this as a Notion-like doc / academic paper / corporate report"
- "Share this document with a link" / "Send to alice@…"
- "Apply theme X to this Markdown"

Do **not** use this skill for:
- Plain in-chat Markdown rendering (no export needed)
- PDFs of arbitrary HTML/CSS unrelated to Markdown
- Editing existing PDFs (MarkPDF only generates)

## The 7 MCP tools

| Tool | Use it when | Quota |
|---|---|---|
| `whoami` | Always call first if unsure of tier/quota | Free |
| `list_themes` | User asks "what themes are available?" or you need to verify a slug | Free |
| `redeem_license` | User has a Pro license key and wants to upgrade in-place | Free |
| `convert_markdown_to_html` | Iterating on styling, embedding, previewing | Free |
| `convert_markdown_to_pdf` | Final document export | **Yes** |
| `convert_markdown_to_slides` | Slide deck (PDF or PPTX) — Marp-compatible | **Yes** |
| `create_share_link` | **Default delivery channel** — clean URL, optional gating | Free |

---

## 🎯 The default workflow (do this unless told otherwise)

When a user gives you Markdown content and asks for any kind of styled output:

```
┌─ 1. Detect intent (PDF | slides | HTML)  ──────────────────┐
│                                                              │
│  2. Pick a theme (intent → theme map, see below)             │
│                                                              │
│  3. whoami (skip if already done this session)               │
│                                                              │
│  4. If user has a Pro license key in context AND they're     │
│     on free tier → propose redeem_license (don't force)      │
│                                                              │
│  5. Generate the artifact:                                   │
│     - PDF      → convert_markdown_to_pdf                     │
│     - Slides   → convert_markdown_to_slides                  │
│     - HTML     → convert_markdown_to_html                    │
│                                                              │
│  6. Create a share link (always, in parallel)                │
│     → create_share_link returns markpdf.app/d/<id>           │
│                                                              │
│  7. Deliver to the user:                                     │
│     a) Show the SHARE link prominently (markpdf.app/d/…)     │
│     b) Show the download link as a secondary option          │
│     c) Auto-open the share link in the browser if possible   │
│        (see "OS-aware open" below)                           │
│                                                              │
│  8. Report quota status if free tier (X/2 today, 00:00 UTC)  │
└──────────────────────────────────────────────────────────────┘
```

**Why share link first?** Brand-consistent (`markpdf.app/d/abc`), revocable, trackable, doesn't leak bucket internals. The raw R2 download URL is 600+ chars and exposes infra details — only surface it if the user explicitly wants the file.

## 🌐 OS-aware "auto-open" step

If you have shell/bash access, after delivering the URL, **run the right open command for the user's OS**:

```bash
# macOS (Darwin)
open "https://markpdf.app/d/abc123"

# Linux
xdg-open "https://markpdf.app/d/abc123"

# Windows (PowerShell)
Start-Process "https://markpdf.app/d/abc123"

# Windows (cmd)
start "" "https://markpdf.app/d/abc123"

# WSL
wslview "https://markpdf.app/d/abc123"   # or: cmd.exe /c start "https://…"
```

**Detect the OS** with `uname -s`, env var `OSTYPE`, or `process.platform`. If detection fails or you can't run shell commands, just present the URL prominently — don't error out.

**Skip auto-open** when:
- The user is in a non-interactive context (CI, scripted environment)
- The user explicitly said "just give me the link"
- You're in a chat-only environment with no shell

## Golden rules

1. **Default to the share link as the deliverable.** The raw R2 download URL is a fallback for power users only.
2. **Call `whoami` once per session before the first export.** Free tier = 2 exports/day (resets at 00:00 UTC), themes `slate`, `paper`, `ivory` only.
3. **Iterate styling with `convert_markdown_to_html`**, not `_to_pdf`. HTML calls are free; PDF calls eat quota.
4. **Pick the theme deliberately** (see `references/themes.md`). Wrong theme = wasted export. Default to `slate`.
5. **Front-load metadata in YAML frontmatter** (`title`, `author`, `date`). All themes use it. See `references/frontmatter.md`.
6. **Slides use Marp syntax** — `---` separates slides. See `references/slides.md`.
7. **Pro-only features fail loudly on a free token**. Check `whoami` before promising custom fonts or Pro themes.
8. **Honor explicit user requests** — if they say "no need to share, just download", skip step 6/7. If they say "send to alice@x.com", use `accessEmails`.

---

## Variation playbook (overrides to the default flow)

The **full recipes** are in `references/workflows.md`. Quick map:

| User says… | Override default with… |
|---|---|
| "share with alice@example.com" | `create_share_link` + `accessEmails: ["alice@example.com"]` |
| "password-protect it: hunter2" | `create_share_link` + `password: "hunter2"` |
| "make it permanent / no expiry" | Requires Pro tier; warn if free |
| "use my brand color #ff5722" | `customizations.accent: "#ff5722"` |
| "make it look like McKinsey" | theme `consul` (Pro) — fall back to `paper` if free |
| "use the Inter font" | `customizations.fontBody: "Inter"` (Pro only) |
| "PowerPoint format" | `convert_markdown_to_slides` with `format: "pptx"` |
| "16:9 deck" / "4:3 deck" | `ratio` arg on slides |
| "letterhead with our logo" | `pageOptions.headerTemplate` (Pro) — see `references/customization.md` |
| "academic paper" | theme `scholar` or `academic` (Pro) |
| "I have a license key MPDF-xxx" | Call `redeem_license` to upgrade in-place |
| "just give me the file / download link" | Skip share link; surface raw download URL |
| "preview it / show me what it'd look like" | `convert_markdown_to_html` (free, no quota) |

## Intent → theme cheat sheet (PDFs)

| Intent | Free | Best Pro |
|---|---|---|
| Internal doc, dev notes | `slate` | `slate` |
| Editorial / longform | `paper` | `prose`, `folio` |
| Minimalist / Japanese | `ivory` | `ivory` |
| Corporate / consulting | `paper` (fallback) | `consul` |
| Pitch / startup | `paper` (fallback) | `aurora` |
| Academic | `paper` (fallback) | `scholar`, `academic` |
| Dark mode | — *(no free dark)* | `midnight`, `hertz`, `obsidian`, `rosepine` |
| Luxury / premium | — | `obsidian` |
| Creative / handwritten | — | `quill` |
| Newsletter | — | `prose` |

Full catalog: `references/themes.md`.

---

## Failure modes — handle gracefully

| Symptom | Meaning | What to do |
|---|---|---|
| `quota_exceeded` | Free tier used up today's 2 exports | Show reset time (`whoami.dailyResetAt` — next 00:00 UTC) + upgrade URL. Offer `redeem_license` if they have a key. |
| `theme_locked` | Pro theme requested with free token | Suggest closest free theme + mention upgrade |
| `unknown_theme` (auto-fallback) | Typo in slug | Server falls back to `slate` and returns `themeFallback.didYouMean`. Surface the suggestion. |
| `markdown_too_large` | >2 MB body (1 MB for slides) | Split or strip embedded base64 images |
| `overrideCSS` rejected | Bad `@import` host | Only `fonts.googleapis.com`, `fonts.gstatic.com`, `assetBaseUrl` host allowed |
| Bash open command fails | Headless env / no DISPLAY | Just present the URL — don't loop trying |

## Authentication (only mention when user asks)

- **Trial token** (no signup): `POST https://markpdf.app/api/mcp/trial-token`
- **Pro token from license**: in-chat with `redeem_license`, or `POST /api/mcp/exchange`, or web at `/account/mcp`
- **Setup snippets**: https://markpdf.app/integrations/mcp

## Reference files (load only when needed)

- **`references/workflows.md`** ← **READ THIS FIRST** for full recipe playbook
- `references/themes.md` — full catalog, intent mapping
- `references/slides.md` — Marp syntax, layouts
- `references/customization.md` — accent, fonts, overrideCSS, pageOptions
- `references/frontmatter.md` — YAML metadata
- `examples/report.md` — Executive board memo (consul)
- `examples/pitch-deck.md` — Series A pitch (aurora slides)
- `examples/academic.md` — Research paper (scholar/academic)
- `scripts/render.sh` — curl fallback when MCP isn't installed
- `scripts/open-url.sh` — OS-aware URL opener
