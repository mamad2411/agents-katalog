---
name: site-navigator
description: OpenClaw-native web browsing, site navigation, rendered-page inspection, logged-in access, and source-verification strategy. Use when the task involves visiting websites, reading pages, navigating dynamic or login-gated sites, extracting information from rendered UI, interacting with sites like GitHub, Zhihu, Xiaohongshu, and WeChat public content, or deciding between browser, web_fetch, direct page access, and parallel research. Prefer this skill for OpenClaw web tasks that should avoid Brave-based search and instead rely on direct site navigation, official sources, and browser-native access.
---

# site-navigator

Use OpenClaw native tools first. This skill is a **strategy layer** for web work in OpenClaw.

Primary goals:
- reach the target page with the lightest reliable method
- prefer direct site navigation and first-party sources over search-engine snippets
- use real browser state when the site is dynamic or login-gated
- keep user-visible conclusions stable instead of exposing noisy intermediate states

## Core operating model

Separate every web task into two layers:

### 1) Decision layer
This is what the user needs in order to act.
Examples:
- the answer to the question
- the identified article/post/repo/person/page
- the final source that supports a claim
- the stable comparison summary
- the confirmed page state before asking the user to inspect or decide

Do not surface this layer until it is reasonably stable.

### 2) Enhancement layer
This improves understanding but should not block the main answer.
Examples:
- screenshots
- extra source links
- additional metadata
- secondary comparisons
- more pages worth checking later

This layer can be progressive.

## Supported target classes

This skill is especially useful for:
- **WeChat public content** (微信公众号 / shared article links)
- **Xiaohongshu** (小红书 posts, creators, discovery/search flows)
- **Zhihu** (知乎 questions, answers, articles, profiles)
- **GitHub** (repos, issues, PRs, releases, docs, changelogs)
- official docs and product sites
- dynamic web apps and dashboards

## Trigger guidance

This skill should trigger when the user asks for things like:
- “去这个网站看一下”
- “看看这个页面/账号/帖子/文章/repo”
- “帮我在某个平台上找……”
- “验证这篇内容/这个链接/这个账号是不是真的存在”
- “比较几个官网/页面/平台内容”
- “需要登录态去看一下这个页面”

This skill is a better fit than generic search when the task is primarily about **site navigation, page-state verification, rendered content, or first-party evidence**.

## OpenClaw tool routing

Prefer these routes without depending on Brave search.

### Route A — Direct URL access
If the user provides a URL, begin with the URL.

Use:
- `web_fetch` for readable static pages
- `browser` for rendered, dynamic, login-gated, or interactive pages

### Route B — In-site navigation via browser
If the user names a site and a target but not an exact URL, prefer opening the site and navigating within it.

Examples:
- “看一下这个知乎问题下面的高赞回答”
- “去小红书搜这个账号”
- “看看这个 GitHub 仓库最近更新了什么”

Use `browser` when site structure and rendered state matter more than generic search discovery.

### Route C — Search for discovery only
Use `web_search` only when direct URL access or in-site navigation is insufficient.

Search is for discovery, not final verification.
Once candidate sources are found, move to first-party pages quickly.

## Tool selection rules

### Use `web_fetch` when:
- the page is mostly static and readable
- the task is reading, summarizing, extracting text, or checking a simple article/doc page
- the key information is in the page body, not in live UI state

### Use `browser` when:
- the page is dynamic or partially rendered
- the site depends on existing login state or cookies
- the task needs clicking, typing, filtering, tab switching, expansion, scrolling, or screenshot proof
- the useful information lives in rendered UI instead of raw article text
- the user asks to “go to” a site and inspect what is there

### Use `sessions_spawn` only when:
- multiple targets are independent
- parallel research saves meaningful time
- the subtasks can be summarized separately and then merged

Do not use subagents for one tightly-coupled browsing flow.

## Browser workflow in OpenClaw

When using `browser`, prefer this sequence:

1. `browser.open` or `browser.navigate`
2. `browser.snapshot` with `refs="aria"`
3. inspect page state before acting
4. `browser.act` for click/type/fill/press
5. `browser.screenshot` only when visual evidence matters

Guidance:
- prefer `snapshot + act` over brittle CSS assumptions
- prefer `refs="aria"` for stability across steps
- use the same tab target when chaining actions
- do not narrate every click unless the user asked for detailed play-by-play

## Logged-in browsing

Use existing browser state when the site depends on session state.

Guidelines:
- keep actions scoped to the task
- avoid modifying settings unless asked
- do not publish, post, or send content without explicit user approval
- if login is required and missing, say exactly what must be logged in

## Site-specific strategy

### WeChat public content
Prefer exact article URLs.

Default path:
1. try direct article URL
2. use `web_fetch` for reading/summarization
3. switch to `browser` if extraction is incomplete, blocked, or visual confirmation matters

Common good tasks:
- summarize article
- capture title/author/date
- verify whether an article still resolves
- extract main观点 / conclusion / timeline

### Xiaohongshu
Treat Xiaohongshu as **browser-first** in most cases.

Default path:
1. open site or exact link in `browser`
2. snapshot to understand visible cards/tabs/search state
3. navigate through UI like a user would
4. screenshot only when proof is needed

Use this for:
- finding a creator/account
- checking whether a post exists
- reading a post and its visible metadata
- collecting examples/screenshots for content analysis

### Zhihu
Use a mixed strategy.

Default path:
- direct question/article URL: try `web_fetch` first
- if ranking/order/context matters: move to `browser`

Use browser when:
- top answers matter
- the page context matters more than raw text
- profile/question navigation is part of the task

### GitHub
Prefer official repo pages or official structured data.

Default path:
- README, docs, changelog, release page: `web_fetch` is often enough
- rendered UI, Actions pages, interactive checks: `browser`
- structured GitHub operations: consider native GitHub CLI/skill when available

Always prefer first-party repo pages over mirrors and reposted summaries.

## First-party verification hierarchy

Read `references/source-hierarchy.md` when source strength matters.

For verification tasks, prefer:
1. official page / original URL
2. official repo / official docs / official changelog
3. directly rendered UI evidence from the official site
4. reputable secondary source only when first-party evidence is unavailable

When only secondary evidence exists, say so clearly.

## Stable-first output rules

Read `references/output-contract.md` when you need to format a user-facing browsing result.

When reporting results from browsing:
- first gather enough evidence for a stable answer
- then give the answer
- then attach screenshots or additional links if useful

Do not:
- present search snippets as evidence
- show unstable intermediate browsing conclusions as final
- overuse screenshots when extracted text is already enough

## Task pattern selection

Read `references/task-patterns.md` when the user task shape is unclear and you need a default execution pattern.
Read `references/target-page-judgment.md` when you need to decide whether the current page is still a discovery surface or already the real target page.
Read `references/runtime-modes.md` when routing may differ between desktop and server environments.

## Parallel web research

Use subagents only when the targets are independent.

Good examples:
- compare 5 products
- gather facts from 4 official sites
- inspect several GitHub repos independently

Bad examples:
- one browsing session with sequential dependencies
- one site flow where each click depends on the previous result

When using subagents:
- define the target and deliverable clearly
- ask for outcomes, not micro-steps
- merge the summaries centrally

## Site patterns

When repeated work reveals stable domain knowledge, store it under:
- `references/site-patterns/<domain>.md`

Record only validated facts:
- browser-first vs fetch-first
- good entry URLs
- navigation quirks
- common extraction failures
- login requirements
- known rendering/anti-bot limitations

Never store secrets, cookies, tokens, or personal data.

## References

Read these when relevant:
- `references/target-page-judgment.md` for deciding whether the current page is the real target
- `references/runtime-modes.md` for desktop vs server strategy differences
- `references/real-cases.md` for representative real-world usage cases
- `references/examples.md` for concrete task examples
- `references/failure-recovery.md` for what to do when browsing/extraction fails
- `references/task-patterns.md` for common browsing task shapes
- `references/source-hierarchy.md` for deciding whether evidence is strong enough
- `references/output-contract.md` for how to report browsing results clearly
- `references/openclaw-browser-playbook.md` for native browser operating patterns
- `references/site-patterns/wechat.md`
- `references/site-patterns/xiaohongshu.md`
- `references/site-patterns/zhihu.md`
- `references/site-patterns/github.md`

## Recovery rule

When a method fails, change the approach based on what the failure teaches you.
Read `references/failure-recovery.md` when you hit incomplete extraction, ambiguous page state, login walls, or unstable discovery paths.

## Anti-patterns

Avoid:
- treating search snippets as verification
- defaulting to web search when direct site access is available
- exposing unstable intermediate findings as final
- using browser automation for pages that `web_fetch` can solve cleanly
- parallelizing a single tightly-coupled browsing flow
- building ad-hoc sidecar browser stacks when OpenClaw already has native tools
