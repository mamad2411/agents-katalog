---
name: format-slack-message
description: Format a message for Slack and copy it to the clipboard as HTML so Slack's composer renders rich text (bold, italic, code, lists, links, blockquotes) on paste. Use when the user wants to paste a formatted message into Slack. Triggers on "copy to slack", "format for slack", "slack message", "paste to slack", or any request to prepare a rich-formatted message for Slack.
---

# Format Slack Message

Draft a message in Magnus's voice, format it as Markdown for Slack, and copy it to the macOS clipboard as HTML.

Slack's message composer is a Chromium-based rich text (WYSIWYG) editor. On paste it reads the `public.html` clipboard flavor (which Chromium maps to `text/html`) and converts it into Slack's own rich text. So the reliable way to get real formatting is to put HTML on the clipboard, the same mechanism the `format-teams-message` skill uses. Pasting plain Markdown leaves raw characters visible unless the user has "Format messages with markup" enabled, which is off by default in modern Slack.

## Workflow

1. **Draft the message in Magnus's voice.** Run the content through the `write-in-my-voice` skill so it reads like he wrote it, not like an AI drafted it (see "Composing the message" below). Skip only if the user pasted final text they want verbatim.
2. **Slackify the Markdown** (see "Slackifying" below): drop tables, keep headings shallow, and prefer links over images.
3. Convert Markdown → HTML using `pandoc`.
4. Place the HTML on the clipboard using `osascript` with the AppKit framework.
5. Confirm the copy and remind the user to paste into Slack.

## Composing the message

Slack messages are outward-facing first-person text, so they go through `write-in-my-voice` (Norwegian or English, register auto-selected). On top of that skill's rules, lean into these for Slack specifically:

- **Smooth, connected sentences.** Favour flowing prose over choppy fragments. Let clauses join with commas, colons, and semicolons (never em dashes) so the message reads naturally start to finish.
- **English for technical jargon.** Keep technical and product terms in English even inside Norwegian prose: say "deployment", "pull request", "merge", "build", "endpoint", "rollback", "feature flag", "background job" rather than forcing a Norwegian equivalent. Magnus code-switches this way naturally; over-translated technical Norwegian reads stiff and wrong.
- **Plain Norwegian for everything else.** Only the technical nouns/verbs switch to English. The connective tissue, framing, and tone stay in natural Norwegian with correct æ/ø/å.

## Slackifying

Slack's rich text model is narrower than Teams'. Before converting, adjust the Markdown:

- **No tables.** Slack does not render `<table>` in the composer at all (the paste is dropped or flattened to a jumble). Convert any table to a `key: value` bulleted list or a numbered list.
- **Headings degrade.** Slack's composer only has two header sizes. Pasted `<h1>`/`<h2>` usually land as a large/medium header, but `<h3>` and deeper typically collapse to bold. Keep headings to one or two levels; for finer structure, use **bold** lead-ins instead.
- **Images don't paste.** Markdown images (`![](url)`) do not render inline from an HTML paste. Provide a plain link instead, which Slack unfurls.
- **Strikethrough doesn't survive.** Slack drops `<del>` on an HTML paste, so `~~strike~~` lands as plain text. Avoid relying on it; reword instead.
- **Everything else maps cleanly** (see the render table below).

## Implementation

```bash
# 1) Write the voiced, slackified message to a temp file (HEREDOC preserves formatting).
cat > /tmp/slack-msg.md << 'EOF'
<VOICED MARKDOWN CONTENT GOES HERE>
EOF

# 2) Convert to HTML (for rich paste) and to plain text (fallback flavor).
#    --wrap=none avoids pandoc inserting hard line breaks.
pandoc -f markdown -t html  --wrap=none /tmp/slack-msg.md > /tmp/slack-msg.html
pandoc -f markdown -t plain --wrap=none /tmp/slack-msg.md > /tmp/slack-msg.txt

# 3) Put BOTH flavors on the clipboard. Slack's rich editor reads public.html;
#    the plain-text flavor means clipboard managers / plain fields aren't empty
#    (setting only public.html makes `pbpaste` return nothing, which looks broken).
osascript <<'APPLESCRIPT'
use framework "AppKit"
use scripting additions
set theHTML to (do shell script "cat /tmp/slack-msg.html")
set theTXT to (do shell script "cat /tmp/slack-msg.txt")
set pb to current application's NSPasteboard's generalPasteboard()
pb's clearContents()
pb's setString:theHTML forType:"public.html"
pb's setString:theTXT forType:"public.utf8-plain-text"
return "Copied. html len: " & (length of theHTML) & ", txt len: " & (length of theTXT)
APPLESCRIPT

# 4) Verify it actually landed (should print the plain-text rendering, not empty)
pbpaste
```

After running, confirm with one line: "Kopiert til Slack-clipboard. Lim inn med Cmd+V."

## What Slack Renders Correctly

| Markdown | HTML pandoc produces | Slack render |
|---|---|---|
| `**bold**` | `<strong>` | bold |
| `*italic*` | `<em>` | italic |
| `~~strike~~` | `<del>` | **does NOT render** (Slack drops `<del>` on paste) |
| `` `inline code` `` | `<code>` | monospace, grey background |
| ` ``` ` block | `<pre><code>` | code block |
| `# H1` / `## H2` | `<h1>` / `<h2>` | large / medium header |
| `### H3` and deeper | `<h3>` | usually collapses to bold |
| `> quote` | `<blockquote>` | indented with left bar |
| `- bullet` | `<ul><li>` | bulleted list |
| `1. item` | `<ol><li>` | numbered list |
| `[text](url)` | `<a href>` | clickable link with text |
| Raw URL | text | auto-linked / unfurled by Slack |

## Slack mrkdwn fallback (plain text)

If the user wants plain text instead of an HTML paste (e.g. they have "Format messages with markup" on, or they're pasting into a field that strips HTML), Slack uses **mrkdwn**, which differs from standard Markdown:

| Standard Markdown | Slack mrkdwn |
|---|---|
| `**bold**` | `*bold*` (single asterisks) |
| `*italic*` / `_italic_` | `_italic_` (underscores) |
| `~~strike~~` | `~strike~` (single tildes) |
| `` `code` `` / ` ``` ` block | same |
| `> quote` | `> quote` (same) |
| `[text](url)` | `<url|text>` |
| `# Heading` | not supported in mrkdwn; use `*bold*` lead-in |

Only produce the mrkdwn plain-text variant when the HTML paste is explicitly unwanted. The default and most reliable path is the HTML clipboard above.

## Pairing With Other Skills

- **`write-in-my-voice`** drafts the message body before formatting (workflow step 1). This skill always pairs with it unless the user supplied verbatim text.
- **`format-teams-message`** is the same idea for Microsoft Teams. Pick by destination.
- For pure plain-text drafting (no rich formatting), use `copy-to-clipboard` instead.

## Failure Modes

- If `pandoc` is not installed: tell the user to `brew install pandoc`.
- If `osascript` complains about the framework directive: macOS may have a permissions prompt the first time. Re-run after granting.
- If Slack renders raw HTML tags or nothing: the message may have been pasted into a non-rich field (e.g. the search box), or the workspace forces plain text. Confirm the target was the message composer, or fall back to the mrkdwn plain-text variant.
- If a table came through as a jumble: it wasn't slackified. Re-convert it to a list (see "Slackifying").
- If special characters break the AppleScript (e.g. unbalanced quotes inside the HTML): the `do shell script "cat ..."` form avoids this because the HTML never passes through AppleScript string parsing. Keep that pattern.
