---
name: linkedin-company-post
description: Publish and interact on LinkedIn strictly as the Pravidhi Solutions company page via the BrowserOS MCP browser — story-style posts with credits, identity-gated composer flow. USE FOR: posting on LinkedIn, /linkedin, company page posts, like/comment as company page.
---

# LinkedIn Company-Page Posting (Verified Workflow)

The ONE rule that overrides everything: **posts must go out as the company page, NEVER a personal profile.**

## Facts (verified)

- MCP endpoint: `http://127.0.0.1:9000/mcp` (JSON-RPC over HTTP; SSE-framed responses possible).
- Company ID: `106762578` · Company name string: `Pravidhi Solutions`.
- Composer URL: `https://www.linkedin.com/company/106762578/admin/dashboard/`
- Posts list: `https://www.linkedin.com/company/106762578/admin/page-posts/published/`
- Composer identity button reads: `Pravidhi Solutions Pravidhi Solutions Post to Anyone`.
- Identity regex: `button "([^"]*?Post to[^"]*?)"` on the snapshot text.
- Success marker: dialog with text `Post successful. View post`.

## The flow (each step proven live)

1. **Find the LinkedIn tab**: `tabs` action=list → regex `\[(\d+)\][^\n]*linkedin\.com` for page id.
2. **Navigate** to the posts page (NOT the dashboard — the dashboard's Start-a-post widget lives in an iframe and clicks won't land).
3. **Snapshot** → find `Start a post` ref: regex `(?:button|link)\s+"Start a post"[^\n]*\[ref=e(\d+)\]`.
4. **Click** it. Use JS DOM click via `evaluate` when AX clicks land stale:
   `(function(){var b=Array.from(document.querySelectorAll('button')).find(function(x){return x.innerText.trim()==='Start a post';});if(!b)return 'nobtn';b.click();return 'clicked';})()`
   Verify with `evaluate`: `document.querySelectorAll('div[role=dialog]').length === 1`. AX-coordinate `act click` intermittently returns "ok" but does NOTHING (stale coords) — always confirm the dialog actually opened.
5. **Identity gate**: snapshot → compose_identity → if `Pravidhi Solutions` not in it: **ABORT, send nothing, log it.**
6. **Fill the editor** (evaluate):
   ```js
   (()=>{const eds=Array.from(document.querySelectorAll('div[contenteditable="true"]'));
   const ed=eds.find(e=>e.offsetParent!==null); if(!ed) return 'no-editor';
   ed.focus(); document.execCommand('insertText',false,JSON_POST_TEXT);
   ed.dispatchEvent(new InputEvent('input',{bubbles:true,composed:true,inputType:'insertText'}));
   return 'filled';})()
   ```
   Note: use a real double-quoted JSON string for the text (json.dumps).
7. **Verify Post armed**: Post button inside the dialog has `disabled:false` / no `aria-disabled`.
8. **Click Post** (JS click again; verify `Post successful` dialog or dialog count drops to 0).
9. **Close** the success dialog via its `Dismiss` button (aria-label).
10. **Verify published**: snapshot the posts page, grep for the hashtags/headline.

## Content rules (top-post style, credits mandatory)

- Hook line (bold, story/curiosity), 3-4 sharp bullet points, one line linking to Pravidhi Solutions services, credits line naming the tools/people, 4-6 hashtags on the final line.
- ~1,000-1,300 characters total (1,241 chars verified fine).
- ALWAYS credit: Pravidhi Solutions, Yashas Prakash, BrowserClaw/BrowserOS MCP, Claude Code, opencode, 9router, Telegram, GitHub + repo link `github.com/yashas-13/anything-telegram`.
- Generation: opencode CLI free model (`opencode run`), prompt = "content lead for Pravidhi Solutions (VAPT, SOC/MDR, Cloud Security), ~200 words, hook + 3 bullets + services + 4-5 hashtags, output ONLY the body".

## Like/comment (also company-identity-gated)

- Navigate to posts page → verify `Pravidhi Solutions` in snapshot (else abort).
- Like refs: `button\s+"React Like"[^\n]*\[ref=e(\d+)\]`; comment refs: `textbox\s+"Text editor for creating content"[^\n]*\[ref=e(\d+)\]` (1-indexed post number).
- Fill Nth visible contenteditable with JS, then press Enter to submit the comment.

## Gotchas

- Dashboard Start-a-post is an iframe widget → always use the posts-page URL.
- AX act-click coordinates go stale after page interaction → JS click fallback is the fix.
- Composer modal can take >2s to render → poll identity up to 4×2500ms before aborting.
- Keep ONE getUpdates poller on the bot token (HTTP 409 otherwise).
