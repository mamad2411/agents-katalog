---
name: aimm-newsletter
version: "1.0"
description: |
  Send an AIMM newsletter email to all members of the aimm_member contact group.
  Use when Lou wants to send an update, announcement, or newsletter to AIMM members.
  Trigger on: "send this to AIMM members", "send the AIMM newsletter", "email the group",
  "send to aimm_member", or any request to distribute a message to the mastermind group.
  Takes a subject and markdown body, previews recipients and content, then sends on confirmation.
---

# aimm-newsletter v1.0

## What this skill does

1. Collect subject + markdown body (ask if not provided)
2. Fetch `aimm_member` contact group via `get_contact_group`
3. Convert markdown → HTML and inject into the AIMM template
4. Show preview — wait for confirmation
5. Send individually to each member via `send_email`

---

## Step 1 — Collect inputs

If the user hasn't provided both, ask for:
- **Subject line**
- **Body** (markdown — supports `**bold**`, `*italic*`, bullet lists with `-`, headers with `##`, links `[text](url)`)

---

## Step 2 — Fetch members

Call `get_contact_group` with `group_name: "aimm_member"`, `account: "aimm_support"`.

---

## Step 3 — Convert markdown to HTML

Convert the markdown body to HTML using these rules:

- Double newline (blank line between paragraphs) → wrap each paragraph in `<p style="margin:0 0 20px 0;">...</p>`
- `**text**` → `<strong>text</strong>`
- `*text*` → `<em>text</em>`
- Lines starting with `- ` → collect into `<ul style="padding-left:20px; margin:0 0 25px 0;">` with each item as `<li style="margin-bottom:12px;">...</li>`
- `## heading` → `<p style="margin:0 0 8px 0;"><strong>heading</strong></p>`
- `[text](url)` → `<a href="url" style="color:#2c4d6e;">text</a>`
- Horizontal rule `---` → `<hr style="border:none; border-top:1px solid #cccccc; margin:30px 0;">`

Then read `~/.claude/skills/aimm-newsletter/assets/template.html` and replace `{{BODY_HTML}}` with the converted HTML.

---

## Step 4 — Preview HTML in Claude

Write the full HTML string to `/tmp/aimm-email-preview.html` using the Write tool. This automatically renders the email in the preview panel.

Show in text:
```
Subject:    <subject>
Recipients: <N> members — <comma-separated names>
```

Ask: **"Looks good? Send to all N members? (yes / no)"**

Do not proceed until confirmed.

---

## Step 5 — Send

For each member in the list, call `send_email`:
- `account`: `"aimm_support"`
- `to`: member's email address
- `subject`: `[AIMM] ` + the subject (always prefix — add it even if the user already wrote it)
- `body`: the full HTML string
- `is_html`: `true`

After all sends complete, report:
```
✓ Sent to N/N members.
Failed (if any): list names + errors
```

---

## Gotchas

- The `get_contact_group` tool returns `[{name, email}]` — use `email` for `to`, `name` for the report.
- Send individually (not BCC) — each member gets a personal send from Coach Lou.
- The template file path is absolute: `~/.claude/skills/aimm-newsletter/assets/template.html` — use the Read tool to load it.
- Do not skip the preview/confirmation step even if the user seems certain.
- If a send fails for one member, continue with the rest and report the failure at the end.
