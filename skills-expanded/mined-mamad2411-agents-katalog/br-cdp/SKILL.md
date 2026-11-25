---
name: br-cdp
description: |
  真实 Chrome 的 CDP 浏览器操作。复用已有登录态，执行打开页面、等待加载、执行 JavaScript、抓取文本与截图等操作。
  触发方式：/br-cdp、Hermes 路由名 `community/oh-story-claudecode/br-cdp`、slash command `/br-cdp`、浏览器操作、操作浏览器、Chrome CDP、复用登录态、browser automation、extract token from browser
---

# Browser CDP 操作工具

通过 CDP 协议控制 Chrome，复用已有登录态，执行浏览器自动化操作。

## 前置条件

- macOS，已安装 Google Chrome
- `agent-browser` 命令行工具已安装

---

## 第一步：启动 CDP Chrome 环境

```bash
bash {SKILL_DIR}/scripts/setup_cdp_chrome.sh 9222
```

成功后所有 `agent-browser` 命令带 `--cdp 9222`。

---

## 常用操作

### 打开页面并等待加载

```bash
agent-browser --cdp 9222 open "<URL>"
agent-browser --cdp 9222 wait 3000
```

### 提取页面文本内容

```bash
agent-browser --cdp 9222 eval 'document.body.innerText.substring(0, 8000)'
```

### 提取 Auth Token

```bash
# 从 localStorage 或 cookie 提取
agent-browser --cdp 9222 eval 'localStorage.getItem("token") || document.cookie'
```

### 页面截图 / 交互式快照

```bash
# 查找页面元素（用于登录按钮等交互）
agent-browser --cdp 9222 snapshot -i
```

### 点击元素

```bash
agent-browser --cdp 9222 click "<CSS selector>"
```

### 填写表单

```bash
agent-browser --cdp 9222 type "<CSS selector>" "<text>"
```

---

## ⛔ 铁律：永不操作用户浏览器进程

**绝对禁止：**
- 永不 `pkill Chrome` / `killall Chrome` / 杀任何 Chrome 进程
- 永不启动新的 Chrome 实例（`/Applications/Google Chrome ... &`）
- 永不更换 `--user-data-dir`（必须用用户已有 profile，保持 cookie/登录态/指纹）
- 永不更改 `--remote-debugging-port`（用用户已监听的端口，若无则报告，不自行开）

**正确做法：**
1. 先检查用户 Chrome 是否已监听调试端口：`curl -s http://127.0.0.1:9222/json/version`
2. 若已有 → 直接 `agent-browser --cdp <port>` 复用
3. 若无 → **报告用户**："请启用 Chrome 远程调试：`/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222`"，然后停止，等待用户操作
4. 任何情况下都不杀用户浏览器、不启新实例、不换 profile

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| CDP 端口未监听 | 告知用户手动启动 Chrome 远程调试，**不要自行操作** |
| 页面跳转到登录页 | `snapshot -i` 找登录按钮并操作 |
| eval 返回 null | 检查 localStorage key 名称，或改用 `document.cookie` |
| Chrome 进程残留 | ⛔ **永不杀进程** — 询问用户如何处理 |
