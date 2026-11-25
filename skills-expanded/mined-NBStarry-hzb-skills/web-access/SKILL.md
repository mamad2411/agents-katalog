---
name: web-access
license: MIT
description: 搜索和核实网络信息、读取网页，或通过用户日常浏览器的登录态操作动态页面。公开内容优先用宿主搜索与抓取工具，需要登录态、DOM 或交互时使用浏览器 MCP。
metadata:
  version: "2.5.4"
---

# web-access

## 工具选择

公开网页优先使用宿主原生搜索、抓取工具。需要登录态、动态 DOM 或交互时，使用 hzb 的 Web Access Browser MCP，复用常驻 CDP Proxy。不要把每个浏览器动作拆成需要 Shell 网络审批的命令。

首次进入浏览器层调用 `browser_status`。已有 Proxy 就复用；用户明确指定浏览器时传 `browser: "chrome"` 或 `"edge"`。尚无偏好且需要选择时再询问用户，不自动换成另一个浏览器。首次连接可能需用户在浏览器授权一次。

| 工作 | MCP 工具 |
| --- | --- |
| 状态、页面列表 | `browser_status`、`browser_targets` |
| 打开、导航、后退 | `browser_open`、`browser_navigate`、`browser_back` |
| 页面信息、DOM 与 JS | `browser_info`、`browser_eval` |
| 点击、真实鼠标点击、上传 | `browser_click`、`browser_click_at`、`browser_set_files` |
| 滚动、截图、关闭 | `browser_scroll`、`browser_screenshot`、`browser_close` |

MCP 未加载时，先确认完整插件的安装与会话来源。只有宿主无此 MCP 时才用下面的兼容入口；本地 TCP 被沙箱阻止不等于浏览器未开启调试。

## 页面操作

默认在自己创建的后台 tab 中工作，保留用户已有 tab。结束时关闭本任务创建的 tab；Proxy 持续运行。代理只对自己创建的 tab 执行闲置清理，默认 15 分钟，`CDP_TAB_IDLE_TIMEOUT` 以毫秒配置。

先通过 DOM 或截图识别页面结构，再选择点击、填写或提取。站点交互产生的完整链接可能含必需参数，打开或导航时保留 query 和 fragment，不凭空拼接会话参数。

打开/导航返回、HTTP 200 或 `document.readyState === "complete"` 均不代表目标内容已经出现。用 `browser_eval` 检查实际目标；仍处于空白、加载、验证或登录跳转时，在默认 15 秒观察窗口内追踪 URL 和 DOM 的变化。读取目标内容，或确认持续存在的具体阻碍后，再判断结果。

登录提示不一定阻挡内容。先尝试读取目标，确实需要登录才请用户在浏览器登录，随后刷新继续。程序化操作失败时可用页面真实交互判断必需参数和跳转过程；GUI 操作也可能受站点限制。

图片与视频承载关键信息时，检查媒体元素、资源地址或截图。滚动可触发懒加载；Shadow DOM 需要遍历 `shadowRoot`，跨源 iframe 不能通过普通 `contentDocument` 直接读取。

## 脚本兼容入口

以下路径相对于当前加载的本 skill 目录，使用其真实安装路径，不写死 Claude 或 Codex 的缓存位置。需要 Node.js 22+；旧版 Node 可使用 scripts 目录的本地 `ws` 依赖。

```bash
node "$WEB_ACCESS_SKILL_DIR/scripts/check-deps.mjs" --browser chrome
# Edge 使用 --browser edge；省略参数时读取 skill 根目录 config.env
```

`check-deps.mjs` 返回 0 表示就绪，2 表示尚未选择浏览器，1 表示连接或配置失败。`config.env` 由模板创建，`WEB_ACCESS_BROWSER=chrome` 可保存偏好；文件不提交 Git，插件缓存更新后可能需要恢复。本次选择用 `--browser`，不改持久配置。

Chrome / Edge 在 `chrome://inspect/#remote-debugging` / `edge://inspect/#remote-debugging` 开启远程调试。指定浏览器不可用时不自动降级。需要切换浏览器或升级旧 Proxy 时，先结束本任务 tab，再核对并停止该 Proxy 的 PID；不要批量结束所有同名进程。新 Proxy 可能需要重新授权。

```bash
curl --noproxy '*' -s -X POST --data-raw 'https://example.com?q=a&lang=zh#section' http://127.0.0.1:3456/new
curl --noproxy '*' -s -X POST --data-raw 'https://example.com/next?a=1&b=2' "http://127.0.0.1:3456/navigate?target=ID"
curl --noproxy '*' -s -X POST --data-raw 'document.title' "http://127.0.0.1:3456/eval?target=ID"
curl --noproxy '*' -s "http://127.0.0.1:3456/close?target=ID"
```

从 2.5.3 起，`/new` 和 `/navigate` 的 URL 必须放在 POST body 中。旧 GET 写法按 [迁移说明](references/migration-2.5.3.md) 更新。完整端点见 [CDP API](references/cdp-api.md)。

## 本地 URL 检索与站点经验

用户要找本人访问过的页面、书签或内部系统时，可按关键词检索本地浏览器资料；普通公开网络搜索不需要读取历史。

```bash
node "$WEB_ACCESS_SKILL_DIR/scripts/find-url.mjs" 关键词 --browser chrome --only history --since 7d --limit 10
node "$WEB_ACCESS_SKILL_DIR/scripts/match-site.mjs" "目标域名或别名"
```

`find-url.mjs` 支持书签和历史，多关键词 AND，`--sort recent|visits`；历史查询需要系统 `sqlite3`。限制浏览器、时间和条数，避免无关记录。已有站点经验见 `references/site-patterns/{domain}.md`，将经验视为有日期的提示，失效时回到页面证据。保存经过验证的模式，不保存凭证、会话参数或个人浏览历史。

上游来源及本地差异见 [README](README.md)。
