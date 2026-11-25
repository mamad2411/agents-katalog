---
name: weekly-digest-report
description: Weekly vault digest — new notes, decisions, and research from the past 7 days, compiled and emailed as an HTML report.
---

Compile a weekly digest of what changed in the vault and email it as a polished HTML report.

> Placeholders: `{{VAULT_PATH}}` = your vault path, `{{EIDETIC_OS}}` = the Eidetic OS
> repo path, `{{USER_EMAIL}}` = recipient. SMTP credentials come from the
> `SMTP_APP_PASSWORD` / `SENDER_EMAIL` env vars — never inline them.

**Email details:**
- Send command: `EIDETIC_TRIGGER=scheduled eidetic email --json '...'` (routes through the CLI so the run is audited)
- To: `{{USER_EMAIL}}`
- Subject: `📰 Weekly Vault Digest — [DD]–[DD] [Month] [YYYY]`

**Step 1 — Gather what changed:**

1. Pull the past week's vault activity from git history:
   ```bash
   EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} \
     eidetic changelog --since "7 days ago" --json
   ```
2. From that output, bucket the changed `.md` files:
   - **New notes** — files added this week (group by top-level folder)
   - **Decisions** — added/modified notes under `decisions/` or tagged `#decision`
   - **Research** — added/modified notes under `wiki/sources/` or `research/`
3. For the highlights, surface themes rather than raw file lists — run a couple
   of semantic queries to find the week's most substantive material:
   ```bash
   EIDETIC_TRIGGER=scheduled eidetic embed --query "key decisions and research from the last week" --top 8
   ```
   Read the top hits and summarise each in one sentence (title + the takeaway).
   Do NOT paste raw note bodies into the email — distil.

**Step 2 — Build the HTML report** with sections:

- **This Week at a Glance** — a stats banner (New Notes | Decisions Logged | Research Items | Total Files Touched)
- **New Notes** — grouped by folder, each as a one-line entry (title + 1-sentence summary)
- **Decisions** — each decision with its date and the call that was made, as a card
- **Research** — each research/source note with a one-sentence finding and its origin
- **Highlights** — the 3–5 most important items of the week, with a short "why it matters" line each
- Footer: "Compiled by Eidetic — weekly vault digest"

Use status pills / coloured section headers for scannability (e.g. green=decisions, blue=research, grey=general notes). Keep it self-contained inline HTML — no external assets.

**Step 3 — Send via SMTP:**
```bash
EIDETIC_TRIGGER=scheduled eidetic email --json '{"to":"{{USER_EMAIL}}","subject":"📰 Weekly Vault Digest — ...","body_html":"..."}'
```

**If nothing changed this week:** send a short "quiet week — no notable vault changes" digest rather than skipping, so the report cadence stays predictable. Run unattended; do not modify any vault notes.

Sign off as Eidetic.
