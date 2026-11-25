---
name: self-hosted-docker-stack
description: Curated directory of self-hosted, Docker-deployable services — an original 10-app batch covering game-server hosting, AI-powered local CCTV, media streaming, Docker stack management, PDF tooling, self-hosted AI chat, network-wide ad/tracker blocking, uptime monitoring, a password manager, and self-hosted Git; plus a second batch covering a document-processing pipeline (searchable document archive, messy-document-to-Markdown, RAG document prep, plain-English structured extraction, OCR) and business-ops SaaS replacements (privacy-first analytics, newsletter/mailing-list manager, screen recorder, Markdown notes, project/task board, low-code internal-tools builder, visual database, AI customer-support chatbot); plus a third batch (heavier-weight product analytics, no-code web scraping, local dubbing/subtitles, link attribution); plus a fourth batch (a personal finance / envelope-budgeting app); plus a fifth batch (no-code database, Firebase-alternative backend, API testing tool, Notion-alternative wiki) — each verified against its real GitHub/Codeberg repository. Use this when the user is planning a homelab, wants to self-host infrastructure instead of paying for a cloud/SaaS equivalent, asks "what should I run on my server," or is deciding between a hosted service and a self-hosted Docker alternative. Overlaps in part with lean-software-stack (both PDF tooling and password managers appear in both, as a desktop vs. server-hosted choice) — use that skill for desktop-app alternatives, this one for services meant to run continuously on a server/NAS.
---

# Self-Hosted Docker Stack

Source: "10 Docker Apps — Apps you'll actually use" carousel (@wellx.tech). Each entry's GitHub/Codeberg repo was verified by live web search (not taken from the carousel's branding alone) before being listed here.

## The 10 apps, by category

| # | App | Category | What it does | Verified repo |
|---|---|---|---|---|
| 1 | **Pterodactyl** | Game-server hosting | Free, open-source game server management panel — runs game servers (Minecraft, Rust, CS2, Valheim, etc.) in isolated Docker containers with a full admin/user UI | https://github.com/pterodactyl/panel |
| 2 | **Frigate** | Local AI CCTV | NVR with realtime local object detection for IP cameras — runs entirely on local hardware, no cloud dependency, MIT licensed | https://github.com/blakeblackshear/frigate |
| 3 | **Jellyfin** | Media server | Free, open-source personal media server (movies/TV/music/photos/live TV), multi-platform clients | https://github.com/jellyfin/jellyfin |
| 4 | **Dockge** | Docker stack management | Reactive, self-hosted `docker-compose.yaml` stack manager — create/edit/start/stop/update stacks from a web UI | https://github.com/louislam/dockge |
| 5 | **Stirling PDF** | PDF toolbox | Locally-hosted, self-hostable all-in-one PDF tool (merge, split, compress, convert, rotate, crop, reorder, watermark, protect/unlock, OCR, 50+ tools), REST API available | https://github.com/Stirling-Tools/Stirling-PDF |
| 6 | **Open WebUI** | Self-hosted AI chat | Self-hosted, privacy-first chat interface for local/API LLMs (Ollama, OpenAI-compatible APIs) — multi-model, RAG built in, MIT licensed | https://github.com/open-webui/open-webui |
| 7 | **AdGuard Home** | Network-wide ad/tracker blocking | DNS-level ad and tracker blocking for an entire network, not just one browser | https://github.com/AdguardTeam/AdGuardHome |
| 8 | **Uptime Kuma** | Uptime monitoring | Self-hosted uptime monitoring with status pages and alerting — a self-hosted alternative to a paid status-page SaaS | https://github.com/louislam/uptime-kuma |
| 9 | **Vaultwarden** | Password manager | Unofficial Bitwarden-compatible server written in Rust — lightweight self-hosted alternative to running the official (resource-heavy) Bitwarden server, compatible with official Bitwarden clients | https://github.com/dani-garcia/vaultwarden |
| 10 | **Forgejo** | Self-hosted Git | Lightweight, community-governed self-hosted Git service (a hard fork of Gitea) — repos, issues, pull requests; primary home is Codeberg, not GitHub | https://codeberg.org/forgejo (mirrors exist on GitHub, but Codeberg is the authoritative source) |

## Batch 2: document-processing pipeline + business-ops apps ("5 Github repos" / "repo of the day" carousels, @replace.so and @ty.prompts.ai)

Existence of every repo below was confirmed via a live `git ls-remote` check
before listing (star counts are as shown in source, not independently
re-verified).

**Document intake & processing** — complements Stirling PDF above rather
than duplicating it: Stirling PDF is a manual PDF-editing toolbox; these are
pipeline stages for turning a pile of documents into searchable/structured
data, mostly unattended:

| App | What it does | Repo |
|---|---|---|
| **paperless-ngx** | Scan-once, searchable document archive — indexes everything so a document is findable by typing a word instead of digging through folders | https://github.com/paperless-ngx/paperless-ngx |
| **MinerU** | Turns messy real-world documents (scans, Office files, tables, formulas) into clean Markdown/JSON — handles cases Stirling PDF's toolset isn't built for. Apache-licensed with added terms — read the license before selling a service built on it | https://github.com/opendatalab/MinerU |
| **docling** | Prepares documents for a gen-AI/RAG pipeline specifically (so a chatbot can actually read a contract instead of choking on the PDF); Linux Foundation project, MIT | https://github.com/docling-project/docling |
| **Unstract** | Describe the fields you want in plain English (invoice number, total, due date); returns structured JSON. Deployable as an API so invoice processing runs unattended | https://github.com/Zipstack/unstract |
| **PaddleOCR** | OCR toolkit — turns scanned PDFs/images into structured data; the engine behind the `oss-tool-to-service-ideas` procedure's document-digitization example | https://github.com/PaddlePaddle/PaddleOCR |

**Business-ops self-hosted apps** — each replaces a specific paid SaaS category:

| App | Replaces | What it does | Repo |
|---|---|---|---|
| **Umami** | Google Analytics / Plausible | Privacy-first, cookie-free web analytics (traffic, campaigns, behavior, conversions) | https://github.com/umami-software/umami |
| **Listmonk** | Mailchimp / ConvertKit | Self-hosted newsletter & mailing-list manager, PostgreSQL-backed, single-binary deploy | https://github.com/knadh/listmonk |
| **Cap** | Loom | Open-source screen recorder (macOS/Windows) with local editing, share links, transcripts; self-hostable storage | https://github.com/CapSoftware/Cap |
| **Memos** | Evernote / a private Twitter-style feed | Self-hosted, Markdown-native quick-capture notes with a timeline view | https://github.com/usememos/memos |
| **Kaneo** | Linear / Asana (light use) | Self-hosted project/task board with labels, self-hosted deployment | https://github.com/usekaneo/kaneo |
| **Appsmith** | Retool | Low-code platform for building internal dashboards/admin panels from a database or API | https://github.com/appsmithorg/appsmith |
| **Apitable** | Airtable | Open-source visual database/low-code platform for CRMs, forms, dashboards | https://github.com/apitable/apitable |
| **Botpress** | Intercom + a chatbot vendor | AI-native customer-support chatbot platform, TypeScript SDK/CLI | https://github.com/botpress/botpress |

## Batch 4: personal finance ("5 more open-source apps that replace paid subscriptions · pt 2", @dotdevs)

The other 4 apps in this source (Jellyfin, Nextcloud, Vaultwarden, Paperless-ngx) are already in the tables above; only this one is new:

| App | Replaces | What it does | Repo |
|---|---|---|---|
| **Actual** | YNAB | Envelope budgeting, with the data on your own machine | https://github.com/actualbudget/actual |

Not added to either table (reviewed, judged out of scope for this list):
**DeerFlow** (bytedance/deer-flow — a general-purpose research/coding
super-agent harness, closer to `claude-code-tooling`'s territory than a
single-purpose business app) and **Excalidraw** (excalidraw/excalidraw — a
whiteboard tool with no clear business-ops slot here; `design-dev-resources`
is the more natural home for a diagramming tool if one is wanted).

## Batch 3: analytics, scraping, dubbing, link attribution (@martiendejong_dev, @ty.prompts.ai)

Each confirmed to exist via `git ls-remote` before listing:

| App | Replaces | What it does | Repo |
|---|---|---|---|
| **PostHog** | Amplitude / Mixpanel / Hotjar | Product analytics, session replay, feature flags, experiments, error tracking — heavier-weight than Umami above; reach for this when the need is product analytics + session replay together, Umami when it's just traffic analytics | https://github.com/PostHog/posthog |
| **Maxun** | A paid web-scraping SaaS | Point-and-click, no-code scraper — turns a website into an API/spreadsheet without writing a scraper | https://github.com/getmaxun/maxun |
| **SmartSub** | A paid captioning/dubbing service | Desktop app: generates, translates, dubs, and burns subtitles using local Whisper speech-to-text — runs offline, no per-video cost | https://github.com/buxuku/SmartSub |
| **Dub** | A paid link-attribution platform | Modern link-attribution/short-link platform — answers which link/creator/video actually produced a conversion; open-core (enterprise features are paid) | https://github.com/dubinc/dub |

## Batch 5: business-ops apps ("10 GitHub Repos So Good They Shouldn't Be Free" carousel, @datawarlord_official)

Four of the carousel's eight tools were already covered above (Appsmith,
Memos) or explicitly excluded with reasoning in Batch 4's notes (DeerFlow,
Excalidraw — still excluded for the same reasons: DeerFlow is an
agent-harness, closer to `claude-code-tooling`'s territory, and Excalidraw
has no business-ops slot, see `dev-repos-to-clone` and `design-dev-resources`
instead). The remaining four are new. Each confirmed to exist via a live
`git ls-remote` check before listing:

| App | Replaces | What it does | Repo |
|---|---|---|---|
| **NocoDB** | Airtable | Open-source no-code platform that turns any SQL database into a smart spreadsheet-style workspace (tables, kanban, gallery, calendar, forms) | https://github.com/nocodb/nocodb |
| **PocketBase** | Firebase | Lightweight self-hosted backend in a single binary — SQLite database, auth, file storage, and realtime APIs together, MIT licensed, Go | https://github.com/pocketbase/pocketbase |
| **Hoppscotch** | Postman | Fast open-source API development tool for REST/WebSocket/GraphQL testing with real-time collaboration | https://github.com/hoppscotch/hoppscotch |
| **Docmost** | Notion / Confluence | Self-hosted collaborative documentation and wiki platform — rich editor, real-time collaboration, nested spaces, AGPL-3.0 | https://github.com/docmost/docmost |

## When to reach for this list

- Planning a homelab or personal/small-team server stack, not just a single desktop tool.
- A recurring server-side cost (uptime monitoring SaaS, hosted password manager seats, hosted Git seats, a cloud CCTV subscription) is worth evaluating against a self-hosted equivalent — apply the `docs/procedures/free-vs-paid-tool-decision.md` procedure from `lean-software-stack` first (it generalizes past desktop apps to this list too: team size, sync needs, support-vs-portability trade-off, who owns maintenance).
- `the-leverage-stack-auditor` flags a recurring SaaS line item and this list has a matching self-hosted alternative.

## Overlap with `lean-software-stack`

Two categories appear in both lists — the choice between them is desktop-local vs. server-hosted, not a duplicate recommendation:

| Category | Desktop (`lean-software-stack`) | Server-hosted (this skill) |
|---|---|---|
| PDF tooling | PDFsam Basic — a local desktop app, no server/network exposure | Stirling PDF — runs continuously on a server, has a REST API for integrating into other systems |
| Password manager | KeePassXC — a local encrypted vault file, no server component | Vaultwarden — a server that syncs across devices/team members via the Bitwarden client protocol |

Pick the desktop option for a solo user with no sync/team need; pick the server-hosted option once multiple devices or people need shared access.

## How to use this list

- These are standalone server software, not skill files — same non-vendoring convention as `claude-code-tooling` and `lean-software-stack`. Running any of them requires actual server/NAS/homelab infrastructure this environment doesn't provide.
- Every repo URL above was verified via live search before being listed, not assumed from the source carousel's app names/logos alone — the carousel itself didn't show repo URLs.
- Forgejo's authoritative home is Codeberg (codeberg.org/forgejo), not GitHub — don't assume every self-hosted tool's primary repo lives on GitHub.
- Check current release activity/license before recommending one as production-critical — this is a snapshot, not a live-verified endorsement.

## Related skills in this repo

- **lean-software-stack**: The desktop-app sibling list, with the shared `free-vs-paid-tool-decision` procedure for deciding when self-hosting is worth the maintenance burden vs. paying for a managed service.
- **the-leverage-stack-auditor**: Check a recurring hosted-SaaS cost against this list before assuming a paid replacement is the only option.
- **claude-code-tooling**: Sibling curated-tool directory (Claude Code-specific tools) using the same standalone-software, non-vendoring convention.
- **attachment-intake**: This entry followed that procedure — inspected the carousel, then verified each tool's real repo via search before documenting anything, rather than trusting branding alone.
- **oss-tool-to-service-ideas** (procedure): PaddleOCR in the batch-2 document table is the same repo that procedure's document-digitization example is built on.

## Notes

Source: "10 Docker Apps — Apps you'll actually use" carousel (@wellx.tech). Unlike earlier tool-directory entries in this repo, the source material didn't display GitHub URLs directly — each repo listed above was located and confirmed via live web search, not carried over from the carousel's branding/logos alone.

Batch 2 source: two "5 GitHub repos so good they shouldn't be free" carousels
(@replace.so) for the business-ops apps, and a "5 free repos that do the
paperwork you keep avoiding" carousel (@ty.prompts.ai) for the
document-processing table. Every repo path was confirmed to exist via a live
`git ls-remote` check (including three — Kaneo, Umami, Apitable — whose org
name wasn't visible on-screen in the source carousel and had to be
independently located and confirmed rather than assumed).
