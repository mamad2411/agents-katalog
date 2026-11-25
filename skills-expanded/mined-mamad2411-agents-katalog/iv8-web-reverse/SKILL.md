---
name: iv8-web-reverse
description: Use ONLY when the deliverable is a runnable compact Python script that uses iv8 to execute browser-side JavaScript and Python requests/curl_cffi to send real HTTP requests. The default deliverable may include a main .py plus a tiny utils/iv8_silent.py helper to suppress iv8 import banners. Trigger for iv8 reproduction of dynamic cookies, h5st, a_bogus/BDMS rewritten URLs, __zp_stoken__, challenge-page cookies, Ruishu-style XHR suffix capture, trusted input/TDC collection, or adapting bundled real examples. Dynamic JS, downloaded challenge sources, temporary runtimes, samples, and reports must be written to the current workspace js_reverse_cache/. Do not use for only locating sign/token entry points, DevTools hook snippets, AST deobfuscation, generic Node.js env patching, or Ruishu pure algorithm research.
---

# iv8 Web Reverse

本 skill 只用于交付一个可运行的紧凑 Python 主脚本：用 `iv8` 执行浏览器侧 JavaScript，再用 Python `requests` 或必要时 `curl_cffi.requests` 发真实 HTTP 请求。默认可配套一个极小的 `utils/iv8_silent.py`，用于静默导入 iv8。

目标输出默认是 PyCharm 友好的紧凑主 `.py` 文件，不是框架、CLI 工具或通用模板集合。

## 硬性约束

- 自动下载或生成的目标站点动态材料、保护/挑战 JS、HTML 样本、临时 runtime JS、调试样本、运行报告和分析结果，统一写入当前工作目录的 `js_reverse_cache/`。
- 如果当前工作目录没有 `js_reverse_cache/`，生成脚本时必须先创建它。
- 不要把新任务中新下载的目标站点动态素材写入本 skill 目录或 `references/cases/`。
- skill 自带真实案例允许保留一份 frozen 示例素材，直接放在 `references/cases/js_reverse_cache/`。
- 真实案例依赖的本地 JS/HTML 素材路径写在对应案例说明里；不要用旧的 `js-assets/` 目录名。
- 默认不保存响应 JSON，不创建 `artifacts/*.json`；只有用户明确要求保存响应时才保存。
- 如果需要保存下载到的瑞数/保护源码，保存到 `js_reverse_cache/rs_source_code.js` 或带站点/时间戳的缓存子目录，不再保存到脚本目录根部。
- 真实请求链路要保持同一个 `requests.Session` 中的 Cookie、动态 JS、签名参数、时间戳和后缀，不要混用旧 Cookie、旧 suffix 或旧签名。
- 生成脚本时保留顶部可编辑常量；不要默认加 `argparse`。
- 创建新任务基础模板时，默认创建 `utils/iv8_silent.py` 并在主脚本导入 `import_iv8_silent()`；不要在每个主脚本里重复粘贴 iv8 静默导入实现，除非用户明确要求单文件。

## 参考文件

本 skill 基于本机真实 `iv8` 仓库 `C:\Users\poppies\Desktop\iv8` 和已复制进 skill 的真实案例。

- `references/api-inventory.md`：从 `README.md`、`README_EN.md`、`demos/*.py` 提取的 iv8 API 清单。
- `references/example-taxonomy.md`：真实 examples 的网站逆向分类。
- `references/script-writing-rules.md`：生成紧凑主脚本、`utils/iv8_silent.py`、缓存目录规则和写法约束。
- `references/cases/`：按类型分类保存的真实案例代码副本。
- `references/cases/js_reverse_cache/`：skill 自带的 frozen 示例素材，例如 JD h5st bundle、JD HTML、BDMS runtime。

执行任务时先读 `references/example-taxonomy.md` 选择最接近的案例，再读对应 `references/cases/` 下的完整 `.py`，缺 API 细节时再读 `references/api-inventory.md`。

## 触发范围

使用本 skill 当用户目标包含：

- 明确要求 `Python + iv8 + requests` 跑浏览器 JS 并真实请求接口。
- 用 iv8 生成动态 cookie、`h5st`、`a_bogus`/BDMS 改写 URL、`__zp_stoken__`、动态 header/sign、动态 URL 后缀。
- 改造本地 `iv8/examples/` 或本 skill `references/cases/` 里的真实案例为一个可直接运行的紧凑主脚本。
- 412/202/challenge 页面已确认要用 iv8 执行页面 JS 生成 cookie 或捕获 XHR 后缀。
- `rs-reverse` 已确认后缀请求失败，且目标是转为 iv8 执行链先跑通请求。
- 用户要求页码、关键词、pageSize、UA、URL 写在代码顶部，而不是终端参数。
- 需要 iv8 派发可信 mouse/pointer 事件采集 TDC/验证码行为数据。

不要使用本 skill 当：

- 只定位 sign/token/header 入口、脚本 URL、调用链。交给 `find-crypto-entry`。
- 普通 403/412/challenge 还没确认要用 iv8 跑，只是要分线或入口定位。交给 `js-reverse-strategy` 或 `find-crypto-entry`。
- 只要浏览器 DevTools hook snippet。交给 `browser-hook-snippets`。
- AST 解混淆、控制流还原、字符串数组还原。交给 `ast-deobfuscate`。
- 通用 Node.js 补环境。交给 `env-patch`。
- 瑞数固定项目结构、首跳材料缓存或最小 Node/proxy 观察。交给 `rs-reverse`。
- 瑞数 Cookie T/basearr 纯算、r2mKa 字节码或 URL suffix AST 深度研究。不要由本 skill 接管；只有用户明确要求 iv8 runtime reproduction 或请求可用性复现时才留在本 skill。

## 案例选择

写代码前先选择最接近的案例：

- `references/cases/signatures/jd-h5st.py`：京东 `h5st`，本地 HTML + 本地 JS bundle + `MessageChannel` patch + 真实请求。
- `references/cases/signatures/nmpa-md5-cookie.py`：业务 MD5 header sign + challenge 页面 JS cookie。
- `references/cases/js-challenges/chinatax-ruishu.py`：两阶段瑞数风格 cookie，然后 iv8 内触发 XHR 捕获带签名/后缀 URL。
- `references/cases/js-challenges/customs-ruishu.py`：两阶段瑞数风格 cookie + 捕获 URL/header/cookie 后重放。
- `references/cases/js-challenges/ouyeel-202-cookie-url.py`：HTTP 202 challenge，内联/外链 JS，load 事件，`netLog` URL suffix，`document.cookie`。
- `references/cases/browser-tokens/zhipin-stoken.py`：API 返回 `seed/name/ts`，iv8 计算 `__zp_stoken__` 后重试。
- `references/cases/network-hook-signing/douyin-bdms.py`：BDMS/a_bogus 风格 runtime hook XHR 并改写 URL，从 `netLog` 读取最终 URL。
- `references/cases/captcha/tencent-tdc-slider.py`：腾讯 TDC，可信 pointer/mouse 事件、POW、`collect`/`eks`。

案例文件用于学习 API 和流程，不要盲目整站复制。必须替换当前目标站的 URL、headers、params、cookies、JS 入口和分页逻辑。

## 输出规则

- 默认生成一个短主 `.py` 脚本；需要静默 iv8 banner 时同时生成 `utils/iv8_silent.py`。
- 顶部放可编辑常量，按需包含：`START_PAGE`、`PAGE_COUNT`、`PAGE_SIZE`、`KEYWORD`、`UA`、`PAGE_URL`、`API_URL`。
- 默认使用 `requests`；只有目标确实需要浏览器 TLS 指纹或原案例已经使用时才用 `curl_cffi.requests`。
- `loguru` 可选；默认使用极小 `log_info()` 或 `print` logger，不默认安装 `loguru`。
- 不添加 `logger.remove()` / `logger.add()`。
- 不添加 `sys.stdout.reconfigure(...)`。
- 主脚本用 `from utils.iv8_silent import import_iv8_silent` 和 `iv8 = import_iv8_silent()` 静默导入 `iv8`。
- 业务流程附近写短中文注释。
- 终端打印完整响应。
- 避免类、大型 wrapper 和未使用的通用能力。

## 生成脚本流程

1. 判断目标类型：签名、JS challenge cookie、浏览器 token、network hook signing、captcha/TDC 或带分页的组合。
2. 读取最接近的 `references/cases/` 案例。
3. 读取 `references/script-writing-rules.md`，使用其中的 `WORK_DIR = Path.cwd()` 和 `CACHE_DIR = WORK_DIR / "js_reverse_cache"` 规则。
4. 缺 iv8 API 细节时读取 `references/api-inventory.md`。
5. 在当前工作目录写最小可运行主 `.py` 文件，并按需写入 `utils/iv8_silent.py`。
6. 所有下载 JS、临时 JS、挑战 HTML、运行报告写入 `js_reverse_cache/`。
7. 如果 sign/header/token/suffix 与 page/body/timestamp 有关，必须在翻页循环内重建。
8. 可行时运行 `python -m py_compile <script.py> utils/iv8_silent.py`。
9. 如果网络、Cookie、账号和目标环境允许，再运行脚本或至少验证 iv8 生成链路。

## 常见工作流

### Challenge Cookie / 页面 JS

1. 用一个 `requests.Session` 发送首个请求。
2. 如果响应是保护/挑战页，保存 HTML、headers、cookies 到 `js_reverse_cache/`。
3. 提取外链 JS 或内联脚本。
4. 用同一个 session 和 headers 下载 JS，并保存到 `js_reverse_cache/`。
5. 创建 `iv8.JSContext(environment=..., config={"timezone": "Asia/Shanghai"})`。
6. 生命周期和外链脚本重要时用 `__iv8__.page.load(snapshot)`。
7. 只需要 DOM 或案例明确手动执行脚本时才用 `document.documentElement.innerHTML = ...`。
8. 有 timer/XHR/promise 时推进 `__iv8__.eventLoop.sleep(...)` 或 `drain()`。
9. 读取 `document.cookie` 或 `__iv8__.netLog.entries[-1].cookieHeader`。
10. 更新同一个 session 的 cookie jar 并重试真实 API。

### Runtime Sign / Header / Token

1. 把目标 JS bundle 或页面 snapshot 加载进 iv8。
2. 只补目标案例确实需要的最小 patch，例如 `MessageChannel` + `__iv8__.wrapNative`。
3. 调用已知 JS 入口，用 `ctx.eval(..., to_py=True)` 返回字符串或 dict。
4. 合并 sign/header/cookie 到 Python 请求。
5. 真实请求并打印完整响应。

### Dynamic URL / XHR Hook

1. 在 iv8 中初始化目标 SDK/保护 runtime。
2. 在 iv8 内创建目标 XHR/fetch。
3. 从 `__iv8__.netLog.entries` 读取最终 URL、headers、cookieHeader、body 元数据。
4. 用 Python `requests` 发送捕获到的真实请求。

### Trusted Input / TDC

1. Python 请求服务端 challenge/session 数据。
2. 必要时 Python 计算图片缺口、POW、轨迹。
3. 用 `ctx.expose(...)` 暴露轨迹和常量。
4. 用 `__iv8__.input.dispatchPointerEvent` 和 `dispatchMouseEvent` 派发可信事件。
5. 移动点之间推进逻辑时间。
6. 读取目标 JS telemetry 后用 Python 提交。

## 依赖

核心依赖缺失时才安装：

```bash
python -m pip install iv8 requests
```

`loguru` 是可选依赖。除非用户明确要求，不安装。

## 完成报告

完成后简短报告：

- 脚本路径。
- `utils/iv8_silent.py` 路径（如果生成）。
- 使用了哪个 bundled case 作为最近参考。
- 哪些常量控制分页或请求输入。
- `js_reverse_cache/` 是否创建。
- 动态 JS、临时 runtime、样本或报告保存路径。
- iv8 cookie/sign/header/token/URL 生成是否验证成功。
- 最终真实请求返回 `200` 还是实际状态码。
- 是否没有保存响应 JSON。
