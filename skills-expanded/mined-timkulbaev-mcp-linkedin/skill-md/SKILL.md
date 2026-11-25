# Skill: LinkedIn Publishing via MCP

## Important: Agent Session Limitation

MCP tools (including all `linkedin_*` tools) are **not available in `--agent` sessions** (e.g. when launched via `claude --agent <name>`). They only load in top-level `claude` sessions.

**If you are inside an `--agent` session**, you must spawn a sub-agent to use these tools:

```bash
# Write your prompt first, then pipe it:
cat /tmp/linkedin-prompt.md | claude -p --dangerously-skip-permissions
```

The sub-agent runs as a top-level `claude` session and will have full access to all LinkedIn tools.

---

## Unipile Account Required

All 3 tools use [Unipile](https://www.unipile.com/?utm_source=partner&utm_campaign=tmc) as the LinkedIn API provider. You need a Unipile account with your LinkedIn account connected. Get your `UNIPILE_API_KEY` and `UNIPILE_DSN` from the Unipile dashboard and add them to your MCP config.

---

## Available Tools

| Tool | Purpose |
|------|---------|
| `linkedin_publish` | Create an original LinkedIn post (text + optional media + @mentions) |
| `linkedin_comment` | Comment on an existing LinkedIn post |
| `linkedin_react` | React to a LinkedIn post (like, celebrate, support, love, insightful, funny) |

---

## Safe Publishing Workflow

### CRITICAL: Always use dry_run first

`linkedin_publish` and `linkedin_comment` both default to `dry_run: true`.
**Never set `dry_run: false` without explicit user confirmation.**

---

## Tool: linkedin_publish

### Step-by-step workflow

1. **Call with dry_run: true** (default — can omit the parameter):
   ```
   linkedin_publish({ text: "Your post text here", dry_run: true })
   ```

2. **Present the preview to the user.** Include:
   - The final post text (with mention placeholders shown as `{{0}}`, `{{1}}`)
   - Character count vs 3000 limit
   - Media validation results (valid/invalid per file)
   - Resolved mentions (which company names were found vs not found)
   - Any warnings (e.g. "character limit exceeded", "1 media item could not be processed")
   - `ready_to_publish` flag

3. **Ask the user for confirmation** before publishing.
   Example: "The post looks good (142 chars, 1 image attached). Publish it?"

4. **Only after confirmation**, call with `dry_run: false`:
   ```
   linkedin_publish({ text: "Your post text here", dry_run: false })
   ```

5. **Report back** the post URL. Construct it from the `post_id`:
   ```
   https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/
   ```
   This step is **mandatory** — always include the clickable URL in your response.

6. The publish response includes `auto_like` — the post is automatically liked after publishing.

### Post formatting best practices

- **Hashtags**: Use 3-5 relevant hashtags at the end, preceded by a blank line
- **Line breaks**: Use double newlines for paragraph breaks in LinkedIn posts
- **Character limit**: 3000 characters max. Keep it under 1300 for better reach
- **Emoji**: Use sparingly at the start of bullet points or sections
- **Mentions**: Pass company names in the `mentions` array — they are resolved automatically

---

## Tool: linkedin_comment

### Step-by-step workflow

1. **Call with dry_run: true**:
   ```
   linkedin_comment({
     post_url: "https://linkedin.com/feed/update/urn:li:activity:12345",
     text: "Great insight!",
     dry_run: true
   })
   ```

2. **Show the preview** (post URN, comment text, character count).

3. **Ask for confirmation.**

4. **Call with dry_run: false** after confirmation.

---

## Tool: linkedin_react

```
linkedin_react({
  post_url: "https://www.linkedin.com/feed/update/urn:li:activity:7123456789012345678/",
  reaction_type: "celebrate"
})
```

Note: `linkedin_react` has no dry_run — confirm with user before calling.

Reaction types: `like`, `celebrate`, `support`, `love`, `insightful`, `funny`.

---

## Error Handling

| Error | What to do |
|-------|-----------|
| `"UNIPILE_API_KEY or UNIPILE_DSN not set"` | User hasn't configured Unipile credentials. Guide them to [Unipile](https://www.unipile.com/?utm_source=partner&utm_campaign=tmc) to get credentials. |
| `"No LinkedIn account found in Unipile"` | User has Unipile but hasn't connected LinkedIn. Direct them to Unipile dashboard. |
| `"Mention not resolved: X"` | Company name not found. Try a different spelling or omit the mention. |
| `"Post exceeds 3000 character limit"` | Shorten the post text. |
| `"File not found: /path/to/file"` | File path is wrong or file was deleted. Verify with user. |
| `"Download failed: ..."` | URL is unreachable or private. Ask for a local file path. |
| `"Unsupported media type"` | Convert to jpg, png, gif, webp, or mp4 first. |

---

## Auto-Like Behavior

`linkedin_publish` automatically likes the post immediately after publishing. This is reported in the response as:

```json
{ "auto_like": "liked" }
```

If the auto-like fails (e.g. rate limit), the response contains an error message but the post itself is still published successfully.

---

## Warnings

- **Never auto-publish** — always show the dry_run preview and wait for explicit user confirmation.
- Media files downloaded from URLs are stored in `/tmp/mcp-linkedin-media/` and cleaned up after publish.
- Mention resolution is best-effort. Unresolved mentions appear in `warnings` — the post can still be published without them.
