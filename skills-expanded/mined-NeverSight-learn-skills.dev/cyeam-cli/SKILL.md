---
name: cyeam-cli
version: 0.1.16
description: cyeam.com CLI — 安装、更新、输出格式说明、命令速查。各领域详情见独立 skill（live-broadcast、pinyin 等）。架构咨询走 MCP。【重要】必须先读 skill 原文获取正确命令格式，禁止瞎猜。
allowed-tools: Bash(cyeam:*)
---

# Cyeam CLI

## 规则

这个 skill 只描述 CLI 本身的安装、更新、输出格式和完整命令列表。**每个领域的具体用法和注意事项在对应的独立 skill 中（live-broadcast、pinyin、mo 等），AI 应先查那些 skill 再执行命令。**

---

## 安装

```bash
# macOS Apple Silicon
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Darwin_arm64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/
# macOS Intel
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Darwin_x86_64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/
# Linux amd64
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Linux_x86_64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/
```

安装检查：`cyeam version`

---

## 登录方式

```bash
cyeam login                           # 登录 Microsoft 账号
cyeam logout                          # 退出登录
cyeam whoami                          # 查看当前登录状态
```

- 登录采用设备码流程：命令会打印授权链接和验证码，并在有桌面环境的机器上自动尝试打开浏览器
- 无桌面环境的服务器上浏览器打开会静默失败，按打印出的链接和验证码在任意浏览器完成授权即可，CLI 会自动获取 token
- token 优先存系统钥匙串（macOS Keychain / Linux D-Bus），不可用时自动回退到 `~/.cyeam/token.json`

## 完整命令列表

```bash
cyeam version                          # 版本
cyeam update                           # 更新
cyeam login / logout / whoami          # Microsoft 登录
cyeam date holiday [YYYY-MM-DD]        # 节假日
cyeam tv ...                           # 直播 → 见 live-broadcast skill
cyeam news ...                         # 新闻 → 见 news skill
cyeam pinyin ...                       # 拼音 → 见 pinyin skill
cyeam mo ...                           # 书法 → 见 mo skill
cyeam roadbook ...                     # 路书 → 见 roadbook skill
cyeam cnote ...                        # 云笔记 → 见 cnote skill
cyeam mail ...                         # 多邮箱收发 → 见 mail skill
cyeam image ...                        # 图片转换 → 见 image skill
cyeam ai models [...]                  # AI免费模型 → 见 ai-models skill
cyeam trello ...                       # Trello任务看板 → 见 trello skill
```

所有命令输出 JSON 信封 `{"ok":true,"data":"...","_notice":{...}}`。加 `--pretty` 去掉信封。
