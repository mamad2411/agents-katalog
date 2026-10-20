---
name: lean-software-stack
description: Curated directory of free, open-source desktop apps that replace common paid SaaS subscriptions — a workspace/docs tool, a notes app, a password manager, a live-streaming/recording studio, a video editor, a team chat app, a PDF toolkit, and a local file-transfer app. Use this when the user is setting up a new business or solo operation and wants to control software costs, asks "what can I use instead of paying for X," is choosing tooling before committing to a paid subscription, or wants a cost-conscious software stack for an early-stage/bootstrapped venture. Pairs with the `free-vs-paid-tool-decision` procedure for *when* a free tool is the right call vs. when paid SaaS is worth it.
---

# Lean Software Stack

Source: "8 Free Desktop Apps That Replace Paid Tools" carousel (@nawraskader). Eight open-source desktop apps, each replacing a category of paid SaaS tool a new or cost-conscious business would otherwise pay monthly for.

## The 8 apps, by category

| # | App | Category | Replaces | What it does |
|---|---|---|---|---|
| 1 | **AppFlowy** | Workspace | Notion, Coda, ClickUp | Local-first workspace for docs, tasks, and databases in one place |
| 2 | **Joplin** | Notes | Evernote, Notion, Craft | Privacy-friendly notes with notebooks, markdown, and sync options |
| 3 | **KeePassXC** | Password manager | 1Password, Dashlane, LastPass | Offline password manager — vault stays on your machine, supports TOTP and autofill |
| 4 | **OBS Studio** | Live streaming/recording | StreamYard, Riverside, Restream | Free studio for streaming, recording, and scene switching |
| 5 | **Kdenlive** | Video editor | Adobe Premiere Pro, Descript, Camtasia | Capable open-source editor: timelines, cuts, titles, exports |
| 6 | **Element** | Team chat | Slack, Discord, Microsoft Teams | Secure messenger built on the open Matrix protocol — chat, DMs, calls, rooms |
| 7 | **PDFsam Basic** | PDF toolkit | Adobe Acrobat, Smallpdf, iLovePDF | Merge, split, rotate, extract, and reorganize PDFs locally |
| 8 | **LocalSend** | File transfer | WeTransfer, Send Anywhere, Dropbox | Local-network device-to-device file sharing — no cloud upload step |

## When to reach for this list

- A new/bootstrapped business (see the-productize-yourself-blueprint / saas-idea-validator cluster) is choosing initial tooling and hasn't committed to paid subscriptions yet.
- The user asks "is there a free alternative to X" for anything on the replaces-list above.
- `the-leverage-stack-auditor` flags a recurring SaaS cost as a leverage leak worth cutting.
- `content-repurposing-service` needs a recording/editing stack (OBS Studio + Kdenlive cover the record → edit steps without a subscription).

## How to use this list

- Don't recommend blindly — apply the `docs/procedures/free-vs-paid-tool-decision.md` procedure first (team size, sync/collaboration needs, support vs. portability trade-off, security/compliance data handling, revisit-on-stage-change). These tools trade convenience (sync, support, integrations, team features) for cost and control; that trade isn't always the right one, especially once a team, not just a founder, is using the tool.
- These are standalone software installs, not skill files — this repo documents them, it doesn't vendor them (same convention as `claude-code-tooling` and `design-dev-resources`).
- Check current release activity/platform support before recommending one as production-critical — this is a snapshot from one source carousel, not a live-verified endorsement.

## Related skills in this repo

- **the-leverage-stack-auditor**: If a recurring SaaS line-item is flagged as a leverage leak, check this list before assuming a paid replacement is the only option.
- **saas-idea-validator** / **the-productize-yourself-blueprint**: Early-stage cost control matters most before revenue validates the idea — this stack keeps founder overhead near zero during that phase.
- **content-repurposing-service**: OBS Studio (record) and Kdenlive (edit) cover that skill's raw-recording → asset-pack pipeline without a paid tool.
- **doc-coauthoring** / **internal-comms**: AppFlowy and Joplin are viable drafting/organizing surfaces before content moves into `docx`/`pdf` for final delivery.
- **claude-code-tooling** / **design-dev-resources**: Sibling curated-tool directories — this one is for general business-ops software, not Claude Code tools or design assets specifically.
- **self-hosted-docker-stack**: The server-hosted sibling list — PDF tooling and password managers appear in both; use this skill's desktop options for a solo user with no sync/team need, that skill's server-hosted options once multiple devices/people need shared access. Shares this skill's `free-vs-paid-tool-decision` procedure.
- **attachment-intake**: This entry followed that procedure — inspected the carousel's actual content before building anything from it.

## Notes

Source: "8 Free Desktop Apps That Replace Paid Tools — Open-source picks worth knowing" carousel (@nawraskader).
