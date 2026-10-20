---
name: fix-pr-comments-xbp
description: >
  Legacy XBP MCP fix-pr-comments. Prefer global fix-pr-comments-xbp-v2 (CLI-only,
  no MCP). Same red→green / allowlist / already-replied loop via XBP MCP slim bulk
  discussions, already-replied fingerprint, reply --if-not-fixed, resolve --comment-id
  (SSE http://127.0.0.1:1113/sse). Shell CLI is fallback only.
---

# Fix PR Comments (XBP) — MCP variant (legacy)

**Prefer `fix-pr-comments-xbp-v2`** (global, CLI-only, no MCP) for new runs.

End-to-end PR review loop driven by **XBP MCP** (slim + bulk + fingerprint).

| Artifact | Path |
|----------|------|
| **Preferred** | `~/.grok/workflows/fix-pr-comments-xbp-v2.rhai` |
| Workflow (this) | `~/.grok/workflows/fix-pr-comments-xbp.rhai` or project `.grok/workflows/fix-pr-comments-xbp.rhai` |
| Sibling | `fix-pr-comments` (gh-centric) |

## Invoke

```text
/workflow fix-pr-comments-xbp https://github.com/xylex-group/athena/pull/512#discussion_r3678324265 https://github.com/.../discussion_r...
/workflow fix-pr-comments-xbp {"pr":512,"discussion_urls":["..."],"max_comments":2}
/workflow fix-pr-comments-xbp {"paste":"..."}
```

```text
workflow tool:
  name: fix-pr-comments-xbp
  args: { paste, pr, discussion_urls }
  agent_budget: 64
```

## Prerequisites

1. Recent **xbp** with slim/bulk/fingerprint/view (build from xbp repo if needed).
2. MCP: `xbp mcp serve --detach` → `http://127.0.0.1:1113/sse`
3. Grok: `grok mcp add --transport sse --scope user xbp http://127.0.0.1:1113/sse`
4. `gh` for checkout / `user -q .login` only when needed

## SPEED path (agents must follow)

1. **`pr view`** for `head_ref` / `head_sha` (not gh first).
2. **One** `discussions` with `comments` or `urls` + **`slim=true`** + **`detect_fixed_reply=true`** + **`our_author`**.
3. **Reclassify / pre-ship:** `already_replied` bulk — not N fat discussion fetches.
4. **Ship:** `reply` with **`if_not_fixed`** + **`our_author`**; **`resolve` with `comment_id`** (no PRRT lookup).

## MCP tool map

Always: `json: true`, `format: "json"`. Reads: **`slim: true`**.

| Need | Tool | Key args |
|------|------|----------|
| PR head identity | `xbp__xbp_github_pr_view` | `pr` |
| Bulk inventory (preferred) | `xbp__xbp_github_pr_discussions` | `pr`, `comments` or `urls`, `slim`, `detect_fixed_reply`, `our_author`, `include_outdated` |
| Single thread | `xbp__xbp_github_pr_discussion` | `url` or `comment`, `pr`, `slim`, `detect_fixed_reply`, `our_author` |
| Fixed scan | `xbp__xbp_github_pr_already_replied` | `pr`, `author`, `comments` / `urls` |
| Reply | `xbp__xbp_github_pr_reply` | `comment_id`, `body`, `yes`, **`if_not_fixed`**, **`our_author`** |
| Resolve | `xbp__xbp_github_pr_resolve` | **`comment_id`** (preferred) or `thread_id`, `yes` |
| Reply+resolve | `xbp__xbp_github_pr_answer` | `comment_id`, `body`, `resolve`, `yes` |

### Scoped URL example

```json
{
  "name": "xbp_github_pr_discussions",
  "arguments": {
    "pr": "512",
    "urls": "https://github.com/xylex-group/athena/pull/512#discussion_r3678324265,https://github.com/xylex-group/athena/pull/512#discussion_r3678324257",
    "json": true,
    "format": "json",
    "slim": true,
    "detect_fixed_reply": true,
    "our_author": "YOUR_GITHUB_LOGIN",
    "include_outdated": true
  }
}
```

### Shell fallback

```text
xbp github pr view 512 --json
xbp github pr discussions 512 --comments 3678324265,3678324257 --slim --detect-fixed-reply --our-author YOU --json --format json
xbp github pr already-replied 512 --author YOU --comments 3678324265,3678324257 --json
xbp github pr reply 512 --comment-id ID --body-file fixed.md --if-not-fixed --our-author YOU --yes --json
xbp github pr resolve 512 --comment-id ID --yes --json
```

### Do not use

- `gh api graphql` / `resolveReviewThread`
- `gh api -X POST …/replies`
- Full comment paginate for inventory when bulk discussions works
- Fat discussion without `--slim` for agent inventory

## Phase rules

1. **Inventory** — view + bulk discussions slim + detect_fixed_reply; hard-scope exclusive ids  
2. **Reclassify** — `already_replied` bulk only  
3. **Checkout** — PR head (`gh pr checkout` / git)  
4. **Select** — P1 then P2; skip already_replied  
5. **Fix** — original-case regression → RED → fix → GREEN  
6. **Verify** — fail closed  
7. **Pre-ship** — bulk already_replied demote  
8. **Ship** — allowlist commit; reply if_not_fixed; resolve comment_id  
9. **Report** — SHA + proof table  

### Reply body fingerprint

```markdown
Fixed on tip `<short-sha>` (`<full-sha>`) on branch `<pr-head>`.

**What changed:** …

**Commit:** …

**Files:** …

**Regression:** Red → fix → Green. Original case: …

**Proof:** `<test-file>` — **P?: <exact subject>**
```

## Regenerate workflow after base changes

```text
python .grok/workflows/_gen_fix_pr_comments_xbp.py
```

## Definition of done

- [ ] Inventory used bulk + slim + detect_fixed_reply  
- [ ] Reclassify/preship used already_replied (not N fat fetches)  
- [ ] Ship used if_not_fixed + resolve comment_id  
- [ ] One regression test per fixed comment (original case)  
- [ ] Red→green proof  
- [ ] Allowlist-only commit  
- [ ] Report names `fix-pr-comments-xbp`  
