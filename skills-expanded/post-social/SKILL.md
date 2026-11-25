---
name: post-social
description: >
  Post content to social media platforms. X/Twitter, Instagram, LinkedIn, Reddit, Threads,
  YouTube, Discord. Use when: "post a tweet", "share on LinkedIn", "upload to YouTube",
  "send Discord message", "post to Reddit", "share on Instagram", "publish on Threads",
  "tweet this", "post on X", "share on social media".
disable-model-invocation: true
allowed-tools:
  - mcp__sh__platform_guide
  - mcp__sh__playbook_preflight
  - mcp__sh__browser_open
  - mcp__sh__browser_navigate
  - mcp__sh__browser_click
  - mcp__sh__browser_fill_form
  - mcp__sh__browser_stealth
  - mcp__sh__browser_wait
  - mcp__sh__browser_page_info
  - mcp__sh__browser_js
  - mcp__sh__browser_dom
  - mcp__sh__key
  - mcp__sh__type_text
  - mcp__sh__click_with_fallback
  - mcp__sh__screenshot_file
  - mcp__sh__observer_start
  - mcp__sh__observer_status
  - mcp__sh__observer_stop
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
  - mcp__sh__memory_record_error
  - mcp__sh__memory_query_patterns
---

# Social Media Posting

You are posting content to a social media platform using ScreenHand's browser automation with anti-detection.

## Intelligence Wrapper

Every tool call returns automatic hints from the server. Watch for:
- **`[HINT]`** — selector suggestions from curated reference files (e.g., `data-testid` values for X/Twitter)
- **`[WARNING]`** — this tool has failed before on this platform, includes the fix
- **`[STRATEGY]`** — suggested next step based on past successful posting sequences

The server auto-loads the matching reference file when you navigate to a platform URL. You'll see hints with exact selectors — use them.

## Available Platform References

These are the exact `platform` names to use with `platform_guide`:

| Platform | Reference Name | Has Playbook |
|----------|---------------|--------------|
| X/Twitter | `x-twitter` | Yes (`x-twitter`) |
| LinkedIn | `linkedin` | Yes (`linkedin`) |
| Instagram | `instagram` | Yes (`instagram`) |
| Reddit | `reddit` | Yes (`reddit`) |
| Threads | `threads` | Yes (`threads`) |
| YouTube | `youtube` | Yes (`youtube`) |
| Discord | `discord` | Yes (`discord`) |

## Pre-Flight (MANDATORY — do this every time)

1. **Load platform knowledge**: `platform_guide(platform="x-twitter")` — use the EXACT name from the table above. Returns curated selectors, flows, known errors, policy notes.
2. **Check verified learnings**: `memory_query_patterns(scope="x-twitter")` — selectors verified through repeated success.
3. **Check for blockers**: `playbook_preflight(url="{platform_url}")` — CAPTCHAs, login walls, shadow DOM, React SPA.
4. **Recall past strategies**: `memory_recall(task="post on {platform}")`.
5. **Start observer**: `observer_start(bundleId="com.google.Chrome")` — detects popups, cookie banners, CAPTCHA overlays during interaction.

If preflight returns RED (CAPTCHA detected) → stop and tell the user to solve it manually.

## Anti-Detection (MANDATORY for all social platforms)

Call `browser_stealth()` ONCE before any interaction. This patches:
- `navigator.webdriver` detection
- Plugin/language/permission fingerprinting
- Chrome automation markers

Use `browser_fill_form` for composing posts — types character-by-character with randomized delays like a human.

## Platform-Specific Flows

### X / Twitter
1. `browser_navigate(url="https://x.com/compose/tweet")` or click compose button
2. Compose selector: `div[data-testid='tweetTextarea_0']`
3. Use `browser_fill_form(selector, text)` to type the post
4. For media: click `input[data-testid='fileInput']` area
5. Post button: `[data-testid='tweetButton']`
6. Verify: `browser_wait` for tweet URL in address bar or success toast
7. **Limit**: ~50 posts/day. Check `policyNotes` from `platform_guide`.

### LinkedIn
1. `browser_navigate(url="https://www.linkedin.com/feed/")`
2. Click "Start a post" button
3. Compose selector: `div.ql-editor[contenteditable='true']`
4. Use `browser_fill_form` for the post body
5. Post button: `button.share-actions__primary-action`
6. Verify: `browser_wait` for the compose modal to close
7. **Limit**: Be cautious with connection requests (~150/week)

### Instagram
1. `browser_navigate(url="https://www.instagram.com/")`
2. Click create/new post button (SVG icon, use `browser_dom` to find)
3. Instagram web has limited posting — primarily for images via drag-and-drop
4. Use mobile user-agent if needed: `browser_js` to check/set
5. **Note**: No links in post body. Hashtags in comments perform better.

### Reddit
1. `browser_navigate(url="https://www.reddit.com/r/{subreddit}/submit")`
2. Title field: `textarea[name="title"]` or `input[name="title"]`
3. Body: Rich text editor or markdown mode
4. Select post type (text, link, image)
5. Submit button: look for submit/post button via `browser_dom`
6. **Requires**: Subreddit name from user. Ask if not provided.

### Threads
1. `browser_navigate(url="https://www.threads.net/")`
2. Click compose button
3. Type in the text area
4. Post button
5. Verify post appeared
6. **Note**: Relatively new — selectors may change. Use `browser_dom` to discover if reference is stale.

### YouTube (comments/community posts, not video upload)
1. `browser_navigate(url="https://www.youtube.com/")`
2. For community posts: navigate to Your channel > Community
3. For comments: navigate to video page, scroll to comment section
4. Comment box: `#simplebox-placeholder` to activate, then `#contenteditable-root`
5. **Note**: Video upload requires Studio — `browser_navigate` to `studio.youtube.com`

### Discord
1. `browser_navigate(url="https://discord.com/channels/{server}/{channel}")`
2. Message input: `div[role='textbox']`
3. Use `browser_fill_form` for the message
4. Press Enter to send: `key("enter")`
5. Verify: message appears in chat

## Media Upload Pattern

For platforms that accept image/video uploads:
1. Find the file input: `browser_dom(selector="input[type='file']")`
2. If hidden, trigger it: `browser_js(expression="document.querySelector('input[type=file]').click()")`
3. The native file dialog will open — use `type_text` to enter the file path + `key("enter")` to confirm
4. Or use `browser_js` to set files programmatically if the platform allows

## Post-Success

1. Take `screenshot_file` as confirmation
2. `observer_stop()` — stop popup detection
3. `memory_save(task="posted on {platform}: {summary}")` — persist the strategy
4. Report to the user: platform, post content summary, any URL if visible

## Error Handling

- **Login wall**: Take `screenshot_file`, tell user to log in, wait for them to confirm
- **CAPTCHA**: Stop immediately, ask user to solve manually
- **Rate limit**: Record with `memory_record_error`, wait 15 minutes, retry once
- **Selector changed**: Use `browser_dom` to rediscover elements, update memory with `memory_record_error`
- **Popup/cookie banner**: Check `observer_status()` — auto-detected, dismiss with `click_with_fallback`

$ARGUMENTS
