---
name: playwright-cookie-injection-pitfalls
description: >
  Playwright/Chromium persistent_context 用 add_cookies 注入 cookie 时的持久化陷阱。
  记录 add_cookies 不设 expires 导致 session cookie 无法持久化到 user_data_dir 的机制原理、
  实验验证方法、修复范式，以及与 Chromium 单例锁的交互关系。
  当用户在调试 cookie 注入浏览器、cookie 注入后关闭 context 再打开就丢失、
  persistent_context add_cookies 后 cookies() 返回空、session cookie 不持久化、
  user_data_dir 里 Cookies 文件没有注入的 cookie 时使用。
  触发词：add_cookies、cookie 注入、persistent_context、expires -1、
  session cookie 丢失、cookie 不持久化、user_data_dir Cookies、
  Chromium SingletonLock、cookie 注入后消失。
---

# Playwright Cookie 注入：add_cookies 的 expires 不持久化陷阱

## 现象

`browser_context.add_cookies([{name, value, domain, path}])` 不设 `expires` 字段时，
Chromium 默认把它当作 session cookie（等价 `expires=-1`）。
**你注入完成立刻 `ctx.cookies()` 能看到**，但一旦调 `context.close()` / `cleanup()` 关闭
context（或浏览器进程退出），**这些 session cookie 不会被写回 `user_data_dir` 的
`Default/Cookies` SQLite 文件**，下次启动 context 它们就消失了。

## 机制原理

Chromium 把持久化 cookie 写到 `Default/Cookies` SQLite 的 `cookies` 表；
session cookie 只在内存中。这是 Chromium 而非 Playwright 的设计，
[Playwright 文档](https://playwright.dev/python/docs/api/class-browsercontext#browser-context-add-cookies)
里未直接强调，踩坑成本极高。

## 验证方法

隔离变量实验：用假 cookie 字符串验证"expires 是持久化的唯一决定因素"。
**注意**：假 cookie 只用于机制验证，生产路径必须用真实 cookie 内容，
否则浏览器可能被平台反爬识别为伪造态导致页面崩溃。

```python
# 不设 expires → 不持久化
await ctx.add_cookies([{'name':'test_session','value':'abc','domain':'.example.com','path':'/'}])
await ctx.close()
cookies = await ctx.cookies()       # 返回 []  ← 注入消失

# 设 expires=未来 timestamp（秒级）→ 持久化
import time
await ctx.add_cookies([{'name':'test_session','value':'abc','domain':'.example.com','path':'/',
                        'expires': int(time.time()) + 30*86400}])
await ctx.close()
cookies = await ctx.cookies()       # 返回 [{'name':'test_session','value':'abc', ...}]  ✓
```

## 修复范式

`parse_cookie_header_to_dicts` 这类把 cookie 字符串转 Playwright cookie 字典的工具函数，
默认要给每条 cookie 设 `expires=now+N天`：

```python
def parse_cookie_header_to_dicts(cookie_header: str, domain: str, expires_in_days: int = 30) -> list[dict]:
    import time
    future_ts = int(time.time()) + expires_in_days * 86400
    result = []
    for pair in cookie_header.split(";"):
        pair = pair.strip()
        if not pair or "=" not in pair:
            continue
        name, _, value = pair.partition("=")
        result.append({
            "name": name.strip(),
            "value": value.strip(),
            "domain": domain,
            "path": "/",
            "expires": future_ts,   # ← 必须给正向未来 timestamp
        })
    return result
```

⚠️ 注意：若真实 cookie 本来就有 `expires`（比如从浏览器导出的），优先用真实值，
别套固定 N 天。从 Playwright `ctx.cookies()` 或 dump 文件读出来的 cookie 字典
已经带正确 `expires`，直接传给 `add_cookies` 即可，不要重新解析丢失字段。

## 何时不用 expires

- 一次性使用：调用方注入后立即 `page.goto` + 验证，不打算持久化的场景可不设 `expires`
- 但**只要调用链涉及「inject → cleanup → 重启 ctx 再 verify」，就必须设 expires**

## 与 Chromium 单例锁的关系

- Chromium 的 `SingletonLock` 会让两个进程用同一 `user_data_dir` 启动 chromium 时
  第二个进程启动失败。所以**注入要在独占 `user_data_dir` 的窗口内进行**。
- 注入完成后必须立即释放 chromium 进程，避免后续其他进程获取锁后启动 chromium 时冲突。

## 与其他 skill 的衔接

- 如果 cookie 注入后浏览器仍无 cookie，可能不仅是 expires 问题，还涉及单向同步反模式
  （DB 写了但没注入到浏览器 profile）→ 参考 `one-way-sync-antipattern`
- 涉及补丁掩盖问题 → 参考 `root-cause-no-patch`：
  不要为了让 cookie 校验过就在校验函数里加兜底补丁，正解是补齐注入路径
- 涉及跨容器操作 → 参考 `operate-through-channels`：优先走 HTTP API 走完整业务路径
- 涉及 commit message → 用 `chinese-commit-messages`