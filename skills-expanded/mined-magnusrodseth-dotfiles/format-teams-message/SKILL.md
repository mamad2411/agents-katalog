---
name: format-teams-message
description: Format a message for Microsoft Teams and copy it to the clipboard as HTML so Teams renders formatting (bold, headings, code blocks, lists, links, blockquotes) on paste. Use when the user wants to paste a formatted message into Teams. Triggers on "copy to teams", "format for teams", "teams message", "paste to teams", or any request to prepare a rich-formatted message for Microsoft Teams.
---

# Format Teams Message

Draft a message in Magnus's voice, format it as Markdown for Microsoft Teams, and copy it to the macOS clipboard as HTML.

Teams does **not** parse Markdown on paste. Pasting plain Markdown leaves the raw characters (`**`, `>`, `` ` ``, etc.) visible. To get real formatting, HTML must be placed on the macOS clipboard under the `public.html` flavor. Teams reads that flavor on paste and renders it.

## Workflow

1. **Draft the message in Magnus's voice.** Run the content through the `write-in-my-voice` skill so it reads like he wrote it, not like an AI drafted it (see "Composing the message" below). Skip only if the user pasted final text they want verbatim.
2. Ensure the result is valid Markdown. Adjust if the input has obvious mistakes that would break the HTML conversion.
3. Convert Markdown → HTML using `pandoc`.
4. Place the HTML on the clipboard using `osascript` with the AppKit framework.
5. Confirm the copy and remind the user to paste into Teams.

## Composing the message

Teams messages are outward-facing first-person text, so they go through `write-in-my-voice` (Norwegian or English, register auto-selected). On top of that skill's rules, lean into these for Teams specifically:

- **Smooth, connected sentences.** Favour flowing prose over choppy fragments. Let clauses join with commas, colons, and semicolons (never em dashes) so the message reads naturally start to finish.
- **English for technical jargon.** Keep technical and product terms in English even inside Norwegian prose: say "deployment", "pull request", "merge", "build", "endpoint", "rollback", "feature flag", "background job" rather than forcing a Norwegian equivalent. Magnus code-switches this way naturally; over-translated technical Norwegian reads stiff and wrong.
- **Plain Norwegian for everything else.** Only the technical nouns/verbs switch to English. The connective tissue, framing, and tone stay in natural Norwegian with correct æ/ø/å.

## Implementation

```bash
# 1) Write the voiced message to a temp file (use HEREDOC to preserve formatting).
cat > /tmp/teams-msg.md << 'EOF'
<VOICED MARKDOWN CONTENT GOES HERE>
EOF

# 2) Convert to HTML. Use --wrap=none to avoid pandoc inserting hard line breaks.
pandoc -f markdown -t html --wrap=none /tmp/teams-msg.md > /tmp/teams-msg.html

# 3) Put HTML on the clipboard via osascript (public.html flavor)
osascript <<'APPLESCRIPT'
use framework "AppKit"
use scripting additions
set theHTML to (do shell script "cat /tmp/teams-msg.html")
set pb to current application's NSPasteboard's generalPasteboard()
pb's clearContents()
pb's setString:theHTML forType:"public.html"
return "Copied to clipboard. HTML length: " & (length of theHTML)
APPLESCRIPT
```

After running, confirm with one line: "Kopiert til Teams-clipboard. Lim inn med Cmd+V."

## What Teams Renders Correctly

| Markdown | HTML pandoc produces | Teams render |
|---|---|---|
| `**bold**` | `<strong>` | bold |
| `*italic*` | `<em>` | italic |
| `~~strike~~` | `<del>` | strikethrough |
| `` `inline code` `` | `<code>` | monospace, grey background |
| ` ``` ` block | `<pre><code>` | code block |
| `# H1` / `## H2` / `### H3` | `<h1>` / `<h2>` / `<h3>` | larger text, bold-ish |
| `> quote` | `<blockquote>` | indented with left bar |
| `- bullet` | `<ul><li>` | bulleted list |
| `1. item` | `<ol><li>` | numbered list |
| `[text](url)` | `<a href>` | clickable link with text |
| Raw URL | text | auto-linked by Teams |

## Known Caveats

- **Tables** (`<table>`) only render in Teams posts/announcements, not in 1:1 or group chat. Convert tables to `key: value` lists or numbered lists if the target is regular chat.
- **Pandoc syntax highlighting** for fenced code blocks with a language hint (e.g. ` ```bash `) produces complex `<span class="...">` markup. Teams strips the classes but generally keeps the text and structure intact. If output looks noisy, add `--no-highlight` to the pandoc call:
  ```bash
  pandoc -f markdown -t html --wrap=none --no-highlight /tmp/teams-msg.md > /tmp/teams-msg.html
  ```
- **Images** via Markdown (`![](url)`) do not render. Provide a plain link instead.
- **Horizontal rules** (`---`) become `<hr>` and render as a thin line in Teams (usable).
- **Em dashes** (—) are fine in HTML but the user's house style forbids them. Use commas, parens, colons, semicolons, or separate sentences.

## Pairing With Other Skills

- **`write-in-my-voice`** drafts the message body before formatting (workflow step 1). This skill always pairs with it unless the user supplied verbatim text.
- For pure plain-text drafting (no Teams formatting), use `copy-to-clipboard` instead.
- This skill is the right choice **only** when the destination is Microsoft Teams. For Slack, iMessage, or email, use `copy-to-clipboard`.

## Failure Modes

- If `pandoc` is not installed: tell the user to `brew install pandoc`.
- If `osascript` complains about the framework directive: macOS may have a permissions prompt the first time. Re-run after granting.
- If Teams renders nothing or shows raw HTML tags: the message may have been pasted into a non-rich-text field (e.g. a Teams search box). Confirm the target was the message compose box.
- If special characters break the AppleScript (e.g. unbalanced quotes inside the HTML): the `do shell script "cat ..."` form avoids this because the HTML never passes through AppleScript string parsing. Keep that pattern.
