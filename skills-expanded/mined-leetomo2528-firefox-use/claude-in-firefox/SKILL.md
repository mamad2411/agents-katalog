---
name: claude-in-firefox
description: Drive the user's Firefox to do anything on the web - open sites, log in, fill and submit forms, click through an app, capture screenshots, scrape page content, upload files, watch console and network traffic, record a GIF of a flow. This is the DEFAULT way to operate a browser or a web page on this machine, so use it for any request that means "open/check/test/log into/click/screenshot a site or a local dev server", including Korean phrasing such as 브라우저, 웹사이트 열어/확인해, 로그인, 폼 입력, 스크린샷, 크롤링, 사이트 테스트. Invoke this skill BEFORE calling any mcp__claude-in-firefox__* tool.
---

# Claude in Firefox

These tools drive a real Firefox on this machine over WebDriver BiDi. They carry the same
names and parameters as Claude Code's Chrome integration, so anything you know about that
surface applies here. Tools read as `mcp__claude-in-firefox__computer` and so on; if your
tool list shows a different prefix, the part after it is still the tool name used below.

## When to use this

Reach for these tools whenever the task needs a browser that renders and clicks: opening a
page for the user, signing into a site, filling and submitting a form, walking through an
app, photographing a layout, reading a page that only exists after JavaScript runs, poking
at a local dev server, attaching a file, chasing a console error or a failing request.

Use something else when a browser is not the point. A static document or a JSON endpoint is
faster with WebFetch or `curl`. Local files and processes belong to the shell. And do not
write a throwaway Playwright, Puppeteer or Selenium script for this work - a real browser,
already logged in, is one tool call away.

Everything here is scoped to the Firefox window. Other applications, the Finder, system
settings and anything else on the desktop are out of reach; say so rather than improvising.

## Start of a session

Call `tabs_context_mcp` first, every time. It returns the tabs this session can act on,
with the numeric ids every other tool takes. Ids belong to the session that issued them -
never reuse an id you remember from an earlier conversation, and never guess one.

Open your own tab with `tabs_create_mcp` for the work you are about to do, rather than
taking over a tab that is already there. Use an existing tab only when the user points at
it. Close what you opened when you are finished - `tabs_close_mcp` - and leave a tab behind
only if the user wants to look at it.

Firefox starts on the first tool call. It runs a profile of its own at `~/.firefox-use/profile`,
so logins the user has done there persist between tasks and their everyday browser is never
touched. If a tool reports that a tab no longer exists, ask `tabs_context_mcp` again instead
of retrying with the old id.

If the browser tools are deferred and have to be loaded before use, load them in ONE
ToolSearch call - the select query takes a comma-separated list:

```
select:mcp__claude-in-firefox__tabs_context_mcp,mcp__claude-in-firefox__navigate,mcp__claude-in-firefox__computer,mcp__claude-in-firefox__read_page,mcp__claude-in-firefox__tabs_create_mcp,mcp__claude-in-firefox__tabs_close_mcp
```

Add whatever else the task obviously needs to the same call - `read_console_messages` and
`read_network_requests` for debugging, `form_input` for forms, `file_upload` for attachments,
`gif_creator` for a recording, `javascript_tool` for page scripting. One round trip, not six.

## The loop that works

1. `read_page` (or `find`, when you can name what you want in words) to get element refs.
2. Act on a ref: `computer` for clicks, hovers, typing and keys; `form_input` to set a field
   value directly, which is steadier than clicking and typing on a picky control.
3. Verify with a screenshot, `get_page_text`, or a second `read_page`.

Prefer refs to raw coordinates. A ref is re-resolved against the live DOM on every use, so
it either hits the element or tells you it is gone; a coordinate is a guess about pixels
that may have moved. When you do click a coordinate, take it from the most recent screenshot
and aim at the middle of the target.

Refs go stale on purpose. Once the page navigates or reloads, every ref from before is dead
and will report so - take a fresh `read_page` rather than reusing one. If a click seems to
do nothing, screenshot before clicking again; the first click may have worked and moved the
page underneath you.

`browser_batch` runs several calls in one round trip and stops at the first error. Use it
once you can see two or more steps ahead - navigate, click a field, type, press Return,
screenshot. Inside a batch every tool that touches a page needs an explicit `tabId`, and any
coordinates you write refer to the screenshot taken *before* the batch ran.

## Reading a page

`read_page` returns the accessibility tree with a `ref_N` on every element. `filter:"interactive"`
trims it to the controls you can act on, which is usually what you want; `depth` and `ref_id`
narrow it further when a page is enormous, and the output says so when it had to cut.

`find` takes a plain description - "the search box", "the accept cookies button" - and
returns up to 20 candidates with refs. It is the fastest path on an unfamiliar page.

`get_page_text` gives the readable text without the markup, for when you need to read rather
than click.

## Debugging a page

`read_console_messages` and `read_network_requests` capture from the moment the session
opens. Always pass a `pattern` to the console tool: a busy app logs hundreds of lines and
the filter is what makes the answer readable. Network requests filter by a substring of the
URL and reset when the tab moves to another domain.

`javascript_tool` evaluates an expression in the page and hands back the value of the last
expression, with top-level `await` available. It is the right tool for reaching into page
state that no screenshot can show.

## Recording a flow

`gif_creator` records what the browser does and exports an annotated GIF - click markers, a
progress bar, labels. Start it before the interesting part, take a screenshot right after
starting and right before stopping so the first and last frames are the states that matter,
and give the file a name that says what it shows. Worth doing for anything the user may want
to review or share.

## Dialogs

A native `alert`, `confirm`, `prompt` or beforeunload dialog blocks the page: until it is
answered, clicks and keys go nowhere. Avoid provoking one when you can, and warn the user
before touching a control that clearly will. When one does appear, `firefox_dialog` accepts
or dismisses it, and `firefox_status` tells you which tab is blocked. Actions on a blocked
tab fail immediately rather than hanging, so a fast failure with a dialog mentioned in it
means: answer the dialog, then carry on.

## When Firefox misbehaves

Every call comes back, as a result or as an error that says what went wrong; none waits more
than about two and a half minutes. A timeout says whether Firefox still answered a health
check - if it did not, the connection was dropped and the next call reconnects, relaunching
Firefox when it has to. Firefox can also end up running with no window at all (on macOS it
stays alive after its last window is closed); the next call that needs a tab restarts it on
its own and says so. For anything else that looks stuck, `firefox_restart` starts the browser
again: logins kept in the profile survive it, open tabs do not.

## When to stop and ask

Stop and check with the user when the task stops going forward:

- the same tool call fails two or three times;
- a page will not load, or an element ignores every click;
- the work is drifting into pages nobody asked about;
- you are about to do something with consequences - buying, sending, deleting, or posting
  under the user's name.

Say what you tried, what the page did, and what you would do next. That is more useful than
a fourth attempt.

## How this differs from Chrome

- The browser is a dedicated profile, not the user's daily one. Sites they logged into
  through these tools stay logged in; sites they use in their own Firefox do not carry over.
- There is no per-site permission prompt. Access is whatever that profile can already reach,
  and the user's off switch is `firefox-use stop`.
- Blocking dialogs are recoverable here rather than fatal.
- `file_upload` only accepts files under directories the server is configured to allow, so a
  page cannot talk you into attaching something from anywhere on disk.
