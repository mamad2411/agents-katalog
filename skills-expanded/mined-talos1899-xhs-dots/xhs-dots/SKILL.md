---
name: xhs-dots
description: 用本机已登录的小红书网页版查询真实用户笔记（点点 AI 问答 + 关键词搜索）。当任务需要真实的体验/口碑/本地生活推荐/避坑/测评/穿搭/菜谱等 UGC 信息，或用户提到「小红书」「点点」「xhs」「rednote」「笔记里怎么说」时使用；也可作为 web_search 之外的第二条信息源做交叉验证。
---

# 小红书 · 点点 AI / 搜索

两条通道，都跑在本机真实浏览器上（CDP 9223，独立配置目录，扫码登录一次后长期有效）：

| 通道 | 适合 | 命令 |
|---|---|---|
| 点点 AI（自己检索并总结 N 条真实笔记） | 「大家怎么说 / 怎么选 / 推荐 / 避坑」这类需要综合多人经验的问题 | `node scripts/dots.mjs ask "问题"` |
| 关键词搜索（原样返回笔记列表） | 需要具体笔记、作者、点赞数，或要自己筛 | `node scripts/xhs.mjs search "关键词" --limit 10 --detail 3` |

## 前置检查（每次任务的第一步）

```bash
try { (Invoke-RestMethod "http://127.0.0.1:9223/json/version" -TimeoutSec 3).Browser } catch { "DOWN" }
curl -s -m 3 http://127.0.0.1:9223/json/version | head -c 40   # macOS/Linux
```

- 有 `Edg/...` 或 `Chrome/...` → 直接干活。
- 返回 DOWN → 跑 `node scripts/ensure-browser.mjs`（幂等：已在跑回 `already-running`，否则启动并等端口，超时退出码 3）。
- 提示未登录 / 搜索页只有登录浮层 → 让用户在弹开的窗口里扫码；登录态在 profile 目录，之后不用再扫。

## 用法

```bash
# 1) 问点点（默认 120s 超时，流式回答结束才返回）
node scripts/dots.mjs ask "杭州西湖附近适合一个人待着的咖啡馆" --timeout 150

# 2) 搜索笔记（--detail N 会逐条打开详情页抓正文，每条间隔 1.5s）
node scripts/xhs.mjs search "露营 装备 避坑" --limit 8 --detail 3

# 3) 单篇笔记正文
node scripts/xhs.mjs note "https://www.xiaohongshu.com/explore/<id>?xsec_token=..."
```

输出：`dots.mjs` → `{question, progress, answer, notes[], conversationId}`；`xhs.mjs search` → `{keyword, count, items[{id,title,author,time,liked,desc,tags,url}]}`。

## 结果怎么用

- `answer` 是点点基于真实笔记的综合回答，但仍是二手总结 → 引用时说「来自小红书用户笔记的总结」，别当权威事实。
- `progress` 能看到它实际检索的关键词和命中笔记标题，据此判断覆盖面；`notes[]` 是它引用的笔记，要原文就用 `xhs.mjs note` 打开。
- 与 `web_search` 结论冲突时，两边都摆出来，别静默择一。

## 边界

- 一次任务最多问 2–3 个问题、搜 2–3 个关键词；连续请求之间至少间隔 3–5 秒，别批量刷。
- 只读：不点赞、不收藏、不评论、不关注、不发布。
- 内容受平台条款约束：可引用要点并注明来源，不要整段搬运或用于商业分发。
- 页面改版会导致脚本失效（关键选择器：`.xhs-ai-message-copy-wrapper`、`section.note-item`、`textarea[name=aiSearchTextarea]`）。失效时先用 `scripts/cdp.mjs` 手动探查，再改选择器。
- 不要关掉那个浏览器窗口；关掉后自动化就断，重跑 `ensure-browser.mjs`（登录态还在）。
