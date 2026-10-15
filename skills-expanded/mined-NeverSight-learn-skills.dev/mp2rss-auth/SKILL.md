---
name: mp2rss-auth
version: 0.1.0
description: 公众号 RSS 服务的认证管理 —— 登录 / 登出 / 查看登录状态。匹配「登录公众号 RSS 服务」「登出公众号 RSS」「我在公众号订阅工具里登录了吗」「查看我现在用的 Feed Key」「我的 RSS 订阅密钥是什么」「在 mp2rss 里登录」「mp2rss auth login / logout / status」。在调用公众号订阅相关 skill 前如不确定凭证状态，可先用本 skill 跑 `mp2rss auth status`。
---

# mp2rss-auth Skill

Mp2rss CLI 的登录态管理 —— 登录、登出、查看 Feed Key 与登录状态。

## Prerequisites

`mp2rss` 二进制已安装：

```bash
# 一键安装（macOS / Linux）
curl -fsSL https://raw.githubusercontent.com/areyoubugcoder/mp2rss-cli/main/scripts/install.sh | sh

# npm（Node ≥ 18）
pnpm add -g @mp2rss/cli
```

也可在 <https://github.com/areyoubugcoder/mp2rss-cli/releases/latest> 直接下载对应平台二进制。

## Commands

### Log in

```
mp2rss auth login [-k <feed-key>] [--no-browser]
```

| Mode | Command | Description |
|------|---------|-------------|
| 浏览器（默认） | `mp2rss auth login` | 打开浏览器走 loopback 授权，登录后自动写入 `~/.mp2rss/config.json` |
| Feed Key 直传 | `mp2rss auth login -k <feed-key>` | 直接传入 Feed Key，**先调用上游 `VerifyAuth` 校验，校验通过后写入 `~/.mp2rss/config.json`**，跳过浏览器流程；适用于 CI / 无头环境 |
| 远程模式 | `mp2rss auth login --no-browser` | 不打开浏览器，仅打印授权 URL，复制到本地浏览器打开后手动粘贴 Feed Key |

```bash
mp2rss auth login
mp2rss auth login -k <your-feed-key>
mp2rss auth login --no-browser
```

Feed Key 可在 <https://mp2rss.bugcode.dev/> 登录后查看或重置。

⚠️ `auth login` **不支持 `-o json`**，只输出纯文本反馈。

---

### Check status

```
mp2rss auth status [-o json]
```

显示是否已认证、Feed Key 来源、API URL、最近登录时间。

```bash
mp2rss auth status
mp2rss auth status -o json
```

JSON shape（已登录）：
```json
{
  "loggedIn": true,
  "source": "config",
  "apiUrl": "https://mp2rss.bugcode.dev",
  "feedKeyMasked": "abcdef***",
  "name": "张三",
  "email": "user@example.com",
  "lastLoginAt": 1705000000000,
  "lastVerifyAt": 1705000001000
}
```

`name` / `email` 仅在浏览器登录回调成功时落盘；`-k` / `--no-browser` 流程拿不到这两个字段，会以 `omitempty` 省略。

JSON shape（未登录）：
```json
{
  "loggedIn": false,
  "source": "none",
  "apiUrl": "https://mp2rss.bugcode.dev"
}
```

`source` 取值：`"env"`（环境变量）/ `"config"`（配置文件）/ `"none"`（未配置）。

---

### Log out

```
mp2rss auth logout
```

清空 `~/.mp2rss/config.json` 里的 Feed Key（保留 API URL 配置）。

---

## Agent Usage Notes

- 调用 `mp2rss mp` 任何子命令前如不确定登录状态，应先 `mp2rss auth status -o json` 解析 `loggedIn` 字段
- 时间字段均为 unix 毫秒数（number），不是格式化字符串
- 字段命名统一 camelCase（`loggedIn` / `apiUrl` / `feedKeyMasked` / `name` / `email` / `lastLoginAt` / `lastVerifyAt`）
- 本地配置：`~/.mp2rss/config.json`，目录 `0700` / 文件 `0600`
- Feed Key 优先级（高 → 低）：命令行 `--api-key` > `MP2RSS_FEED_KEY` 环境变量 > 配置文件
- API URL 优先级（高 → 低）：`--api-url` > `MP2RSS_API_URL` > 配置文件 > 默认 `https://mp2rss.bugcode.dev`
- 错误 JSON 形态：`{"error":{"message":"...","code":<int>}}`，`code` 为 HTTP 状态码或 CLI exit code
- Exit codes：`0` 成功；`1` 通用错误（网络）；`2` 参数错误；`3` 鉴权失败；`4` 资源不存在；`5` 上游不可用
