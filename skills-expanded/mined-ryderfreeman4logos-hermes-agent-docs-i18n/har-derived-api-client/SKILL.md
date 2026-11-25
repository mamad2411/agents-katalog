---
name: har-derived-api-client
description: Record a site's XHR into a HAR, derive an HTTP client.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Browser, HAR, API, Reverse-Engineering, Playwright]
    category: web-development
---

# HAR派生API客户端

首先使用真实浏览器访问网站，并将其网络流量记录到HAR文件中，随后将该HAR文件转换成该网站的私有JSON API，这样就可以通过普通的HTTP请求直接调用它——这比每次请求都由浏览器控制页面要更加高效且成本低廉。该技术由Jared Longster提出，后经Dax（thdxr）推广普及。此工具仅用于捕获和回放网络请求，**不会绕过身份验证、破解验证码，也不会规避机器人检测**；如果网站需要登录会话，只需原样传递其请求头/Cookie，而无需伪造它们。

该工具的脚本基于stdlib及Playwright：捕获功能需要Playwright支持，转换过程则完全依赖标准库，而回放功能仅需`requests`/`httpx`（或`curl`）即可实现。

它支持**所有Hermes浏览器访问路径**：包括默认的本地`browser_navigate`后端，以及云端/远程后端（Browserbase、Browser-Use、Firecrawl），还有任何以 `/browser connect` 开头的CDP接口。由于两种情况下的HAR记录方式有所不同（详见“运行方法”），因此提供了两种捕获脚本——一种用于直接启动浏览器，另一种用于通过CDP连接浏览器。

## 适用场景

- “为<网站>构建CLI/客户端”——通过解析其API来实现功能，而非手动编写点击脚本。  
- “该网站没有公开API，但页面明显会加载JSON数据。”  
- 您正准备对同一查询反复调用`browser_navigate`函数——请停止操作，先一次性获取接口地址。  
- 对自动补全、搜索、内容源或结账相关的XHR请求进行逆向分析。  
- 您已通过Cloud Backend（如Browserbase / Browser-Use / Firecrawl）或`/browser connect`功能捕获了会话，希望在不重新租用浏览器的情况下获取API接口。

## 先决条件

- Playwright + 浏览器二进制文件（仅用于数据捕获步骤）：  
  - 先执行`pip install playwright`，再运行`playwright install chromium`  
  - （如果系统已通过`~/.cache/ms-playwright`路径安装了Playwright浏览器，可直接复用。）
- 用于数据回放步骤的`requests`或`httpx`库（标准库中的`urllib`也可使用）。  
- 不需要API密钥。客户端所需的任何密钥/令牌均可从HAR文件中获取。  
- 对于CDP路径（`har_capture_cdp.py`）：需有一个可访问的CDP接口地址。在Hermes系统中，可运行`/browser connect`查看当前活跃的接口地址，或直接读取配置文件中的`BROWSER_CDP_URL`/`browser.cdp_url`字段。Cloud Backend则会将相关地址分别标记为`cdpUrl`/`connectUrl`。

## 运行方式

该技能对应的脚本位于`scripts/`目录中，可通过`terminal`工具调用。  
**需根据数据捕获方式选择相应的工具**——这往往是用户容易混淆的部分。

| 浏览器启动方式 | Hermes的获取途径 | 数据捕获工具 |
|---|---|---|
| 本地`browser_navigate`（默认，agent-browser/Playwright） | 在本地直接启动 | `har_capture.py` |
| Camofox（已设置`CAMOFOX_URL`） | 本地REST/CDP接口 | 若该工具支持CDP，则使用`har_capture_cdp.py`，否则需自行实现捕获逻辑 |
| Browserbase / Browser-Use / Firecrawl（云端服务） | **CDP**（通过`cdpUrl`连接） | `har_capture_cdp.py` |
| `/browser connect <url>` / `BROWSER_CDP_URL` | **CDP** | `har_capture_cdp.py` |

通用原则：**若Hermes直接启动了浏览器，则使用`har_capture.py`；若通过CDP与浏览器连接，则使用`har_capture_cdp.py`。** `har_capture.py`依赖Playwright的`record_har_path`功能，而该功能仅能在本地运行的浏览器环境中使用。`har_capture_cdp.py`则通过`connect_over_cdp()`函数建立连接，并从`page.on("request"/"response")`事件中收集HAR数据，因为已连接的浏览器不支持`record_har_path`功能。

无论采用哪种启动方式，后续处理均需通过以下步骤：
- `har_to_client.py`——筛选出XHR/fetch/JSON类型的请求，按端点分组，并输出参数、请求头、请求体以及重放相关提示信息（如User-Agent、Cookie、认证信息）。

具体路径解析可参考该技能对应的目录结构。标准处理流程如下：

```bash
# 1a. Capture, LOCAL browser (Hermes launched it)
python3 scripts/har_capture.py "https://SITE/" out.har \
  --action "fill:input[name=search]:my query" --action "sleep:3" --wait 2

# 1b. Capture, CDP browser (cloud backend or /browser connect)
#     get the endpoint from /browser connect or BROWSER_CDP_URL
python3 scripts/har_capture_cdp.py "ws://HOST/devtools/browser/..." out.har \
  --goto "https://SITE/" --action "fill:input[name=search]:my query" \
  --action "sleep:3" --wait 2

# 2. Derive — read the endpoints out of the HAR
python3 scripts/har_to_client.py out.har --host SITE --max-body 400

# 3. Replay — write a tiny client from the printed endpoint (see Procedure)
```

## 快速参考指南

```
har_capture.py <url> <out.har> [--wait S] [--headed] [--action SPEC ...]
  action SPEC:  fill:SELECTOR:TEXT | press:SELECTOR:KEY | click:SELECTOR
                goto:URL | sleep:SECONDS      (run in order after page load)
  use when Hermes LAUNCHED the browser (local browser_navigate default)

har_capture_cdp.py <cdp_url> <out.har> [--goto URL] [--wait S] [--action SPEC ...]
  same action SPEC; attaches to an existing CDP browser and does NOT close it
  use for cloud backends (Browserbase/Browser-Use/Firecrawl) & /browser connect

har_to_client.py <in.har> [--host SUBSTR] [--include-static] [--max-body N]
  default: keeps only XHR/fetch/JSON; --host narrows to one domain
  prints per endpoint: query params, non-boring req headers, req body sample,
                       response status/content-type + body sample
  prints "### Replay hints": the browser User-Agent, cookie/auth presence
```

## 操作步骤

0. **根据捕获方式选择对应的工具**（详见“运行方式”表格）。在本地运行时使用 `har_capture.py`；通过 CDP 连接时则使用 `har_capture_cdp.py`。在 Hermes 环境中，当启用云端/远程后端时，执行 `/browser connect` 命令即可获取 CDP 端点地址。

1. **定位目标交互操作**。使用 `browser_navigate`（或带 `--headed` 参数的捕获模式）打开目标网站，确定需要输入何种选择器或点击哪些元素，同时通过开发者工具的网络面板确认是否有 JSON XHR 请求被触发。

2. **通过 `terminal` 工具捕获 HAR 文件**。首先指定 `--action` 参数以定位对应请求：先执行“填充表单”操作，随后设置足够的 `sleep` 时间以等待延迟处理的 XHR 请求完成，最后务必保留 `--wait` 参数以确保后续响应能够被完整输出。这两种捕获工具都会嵌入响应内容，因此生成的客户端代码能够呈现真实的请求数据结构。

3. **使用 `har_to_client.py --host <domain>` 进行转换**。该命令可输出以下信息：请求方法、URL/路径模板（数字或 UUID 格式的部分会简化为 `{id}`）、查询参数、请求体中的 JSON 数据，以及 `### Replay hints` 部分的内容。

4. **编写客户端代码**。需完全复现原始请求的各个要素——包括请求方法、路径、查询参数及请求体内容。同时要使用网站实际所需的请求头信息：至少需复制“重放提示”中的 **User-Agent** 值；如果提示中提到了 Cookie 或认证/令牌相关的请求头，也需一并包含。

5. **进行无浏览器测试**。使用 `terminal` 工具运行生成的客户端代码，确认其返回的数据与浏览器捕获的结果一致。这才是该流程的最终目标：整个处理过程无需依赖浏览器。

6. **（可选）封装为 CLI 工具**——可以为转换后的功能编写一个简单的 `argparse` 脚本，例如 `search.py "frank herbert"`，以便更便捷地调用。
示例演示（维基百科搜索标题、数据衍生处理及实时回放）：

```python
import requests
r = requests.get(
    "https://en.wikipedia.org/w/rest.php/v1/search/title",
    params={"q": "frank herbert", "limit": 5},
    headers={"accept": "application/json",
             "User-Agent": "Mozilla/5.0 ... Chrome/131 Safari/537.36"},  # from HAR
    timeout=15,
)
for p in r.json()["pages"]:
    print(p["title"], "-", p.get("description"))
```

## 常见问题

- **默认的浏览器 User-Agent 会触发 403 错误。** 许多网站（如 Wikipedia、由 Cloudflare 托管的 API）会拒绝 `python-requests/x.y` 这类 User-Agent。务必使用重放提示中提供的浏览器 User-Agent。这也是在浏览器操作成功的情况下，衍生客户端却失败的首要原因。
- **当 `--action` 操作失败时，HAR 文件尚未完成写入就会中断**——此时你将无法获得任何文件。如果在某个选择器上捕获到错误，整个运行过程将一无所获；请修正该选择器（可使用 `--headed` 模式进行观察），然后重新运行。切勿试图调试缺失的 HAR 文件。
- **服务器端渲染的页面没有可用于提取的 XHR 请求**——`har_to_client.py` 会输出“未检测到类似 API 的请求记录”。相关数据其实存在于 HTML 中，需通过抓取获取，或寻找那些会发送 JSON 数据的交互操作。
- **带有防抖功能或自动补全功能的 XHR 请求需要真正的暂停时间。** 在 `fill` 操作之后添加 `--action "sleep:3"` 参数；仅靠输入操作是无法在 HAR 文件关闭前触发请求的。
- **认证/会话相关接口需要使用已捕获的 `Cookie`/`Authorization` 请求头，而这些头信息是有有效期的。** 衍生客户端的稳定性完全取决于这些凭证的有效性；一旦出现 401 错误，就需要重新捕获凭证。HAR 文件中包含敏感信息——请将 `out.har` 视为机密文件，在完成衍生操作后立即删除。
- **设置 `record_har_content="embed"` 会导致 HAR 文件体积过大。** 可使用 `--max-body` 参数限制输出内容；对于内容包含大量媒体的页面，其 HAR 文件本身的体积也可能很大。
- **接口地址可能会发生变化。** 网站可能会在未提前通知的情况下更改其私有 API 地址。当客户端出现故障时，应重新执行捕获→衍生操作的流程，而非手动修改 URL 地址。
- **使用错误的捕获工具 = 无 HAR 数据。** 运行在云平台/CDP 后端上的 `har_capture.py` 不会记录任何数据（因为它会启动自己的本地浏览器，而非您指定的浏览器）。而 `har_capture_cdp.py` 需要对应的端点地址；在 Hermes 环境中，该地址可从 `/browser connect` 或 `BROWSER_CDP_URL` 获取。请根据捕获工具选择相应的配置路径（参见“运行方式”表格）。
- **“无头 Chrome”用户代理特征较不明显。** 通过本地浏览器或代理浏览器进行捕获时，生成的 User-Agent 通常为 `HeadlessChrome/...`；部分网站会检测“无头”标识。而云平台后端（如 Browserbase/Browser-Use）会发送真实的桌面版 Chrome 用户代理，因此基于云平台捕获生成的客户端能更稳定地模拟真实请求。如果基于无头浏览器生成的客户端会出现 403 错误，而普通浏览器却正常，那么在判定端点地址发生变化之前，应先将“无头”用户代理字符串替换为普通的 Chrome 用户代理字符串。
- **CDP 捕获方式不会关闭浏览器。** `har_capture_cdp.py` 会连接到它并不控制的浏览器，并让其保持运行状态——这正是 Hermes 所管理的云端/远程会话的运作方式。无需额外添加关闭操作，应由对应的后端负责终止浏览器进程。

## 验证方法

在没有 API 密钥的情况下，对真实网站进行端到端测试以验证功能。

```bash
python3 scripts/har_capture.py "https://en.wikipedia.org/wiki/Main_Page" /tmp/wiki.har \
  --action "fill:input[name=search]:dune messiah" --action "sleep:3" --wait 2
python3 scripts/har_to_client.py /tmp/wiki.har --host wikipedia.org --max-body 200
```

系统会输出类似 `GET https://en.wikipedia.org/w/rest.php/v1/search/title` 的请求内容，其中包含 `q` 和 `limit` 参数，同时返回一个 JSON 格式的 `pages` 响应。随后可利用相应的处理代码片段重新发送该请求，从而通过普通 HTTP 协议确认是否能获取到匹配的标题。
