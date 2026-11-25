---
name: github-profile-coolify
description: "一键优化 GitHub Profile README（酷炫风格、Snake 动画、图卡健康检查与自动回退），适用于主页升级和图片失效排查场景。"
---

<role>
你是 GitHub 主页视觉工程师与自动化排障执行器，负责把用户的个人主页从基础版升级为稳定、可维护、可验证的酷炫版。
</role>

<purpose>
当用户想“美化 GitHub 主页”“做成酷炫版”“加贪吃蛇动画”“排查卡片不显示”时，用最少交互完成：权限检查、配置生成、自动推送、故障回退与验收。
</purpose>

<trigger>
```text
触发词/示例：
- 优化我的 GitHub 主页
- 做一个酷炫版 Profile README
- 给我加 snake 动画
- 为什么主页图片不显示
- 帮我修 GitHub stats 卡片
- github-profile-coolify
```
</trigger>

<gsd:workflow>
  <gsd:meta>
    <name>github-profile-coolify</name>
    <trigger>GitHub 主页美化、Profile README、snake 动画、stats 图片失效排查</trigger>
    <requires>Read, Write, Edit, Bash, AskUserQuestion, WebFetch</requires>
    <checkpoints>
      <checkpoint order="1">账号与目标仓库确认完成</checkpoint>
      <checkpoint order="2">GitHub 授权 scope 检查通过</checkpoint>
      <checkpoint order="3">README 模板与模块选择确认</checkpoint>
      <checkpoint order="4">Snake Workflow 已成功运行</checkpoint>
      <checkpoint order="5">所有图片 URL 可访问性检查通过</checkpoint>
      <checkpoint order="6">主页可见效果验收通过</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>在写入 README 之前必须先备份现有 README 内容</constraint>
      <constraint>外部图片服务返回 503/DEPLOYMENT_PAUSED 时必须自动切换备用源</constraint>
      <constraint>未经用户明确同意，不执行 destructive git 操作</constraint>
      <constraint>每次 push 后必须给出可验证链接和检查命令</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>将用户 GitHub 主页升级为“可展示 + 可排障 + 可持续更新”的酷炫版，并确保关键图片稳定显示。</gsd:goal>

  <gsd:phase name="preflight" order="1">
    <gsd:step>识别 GitHub 用户名与目标 profile 仓库（<username>/<username>）</gsd:step>
    <gsd:step>检查 gh、git 与网络连通性</gsd:step>
    <gsd:step>确认执行模式（全自动/半自动）</gsd:step>
    <gsd:checkpoint>环境预检完成</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="auth" order="2">
    <gsd:step>检查 gh auth 状态与缺失 scope</gsd:step>
    <gsd:step>若缺少 scope，引导用户完成授权</gsd:step>
    <gsd:step>授权失败时自动进入代理/重试分支</gsd:step>
    <gsd:checkpoint>授权通过</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="build" order="3">
    <gsd:step>生成或更新 README（酷炫模板）</gsd:step>
    <gsd:step>创建/更新 snake workflow</gsd:step>
    <gsd:step>提交并推送到远端</gsd:step>
    <gsd:checkpoint>基础配置生效</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="verify-and-fallback" order="4">
    <gsd:step>curl 检查所有图片 URL 的 HTTP 状态码</gsd:step>
    <gsd:step>对 503/超时的服务自动替换为备用服务</gsd:step>
    <gsd:step>再次推送并复验</gsd:step>
    <gsd:checkpoint>显示稳定</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="handoff" order="5">
    <gsd:step>输出变更摘要、验证链接、故障排查入口</gsd:step>
    <gsd:step>提供下一步可选增强方案</gsd:step>
    <gsd:checkpoint>用户验收完成</gsd:checkpoint>
  </gsd:phase>
</gsd:workflow>

# GitHub 主页酷炫化（含稳定性排障）

## 你需要先准备什么（权限申请清单）

| 类别 | 需要项 | 用途 | 申请方式 |
|------|--------|------|----------|
| GitHub CLI 登录 | `gh auth login` | 允许 CLI 访问 GitHub API | 首次执行时登录 |
| OAuth Scope | `user` | 读取/更新个人资料（如 Bio） | `gh auth refresh -h github.com -s user` |
| OAuth Scope | `repo` | 创建与推送 profile 仓库 | `gh auth refresh -h github.com -s repo` |
| OAuth Scope | `workflow` | 创建/触发 GitHub Actions（snake） | `gh auth refresh -h github.com -s workflow` |
| 网络（可选） | HTTP 代理 `127.0.0.1:10802` | 解决直连超时 | `HTTP_PROXY/HTTPS_PROXY` 环境变量 |

> 推荐一次性授权：
>
> ```bash
> gh auth refresh -h github.com -s user,repo,workflow
> ```

## 交互流程（Skill 必须问清楚）

### 1. 目标确认
- 询问：是否操作当前登录账号的 profile 仓库。
- 默认：是（`<username>/<username>`）。

### 2. 风格确认
- 选项：`lite`（简洁）/ `full`（完整酷炫版，默认）。
- `full` 包含：Typing、Stats、Streak、Activity、Snake、Featured Projects。

### 3. 自动化权限确认
- 询问：是否允许自动创建 workflow、自动 commit + push。
- 默认：允许。

### 4. 网络策略确认
- 询问：直连失败是否自动切换到本地代理 `127.0.0.1:10802`。
- 默认：允许自动切换。

### 5. 验收方式确认
- 输出两类验证：
  1. 页面链接验收（GitHub 主页）
  2. 技术验收（`curl -I` 状态码）

## 自动执行步骤（实施模板）

```bash
# 1) 进入 profile 仓库
cd <workspace>/<username>

# 2) 权限与网络检查
gh auth status -h github.com
gh auth refresh -h github.com -s user,repo,workflow

# 3) 提交与推送
git add README.md .github/workflows/generate-snake.yml
git commit -m "feat(profile): upgrade cool homepage with resilient cards"
git push origin main

# 4) 图片健康检查
curl -I "https://github-profile-summary-cards.vercel.app/api/cards/stats?username=<username>&theme=tokyonight"
curl -I "https://streak-stats.demolab.com?user=<username>&theme=tokyonight"
curl -I "https://raw.githubusercontent.com/<username>/<username>/output/github-contribution-grid-snake.svg"
```

## 图片不显示的自动回退规则（核心）

当检测到以下信号时触发回退：
- HTTP `503`
- 响应头包含 `x-vercel-error: DEPLOYMENT_PAUSED`
- 连接超时（`curl: (28)`）

回退映射：

| 原服务 | 常见问题 | 备用服务 |
|--------|----------|----------|
| `github-readme-stats.vercel.app` | 503 / paused / 超时 | `github-profile-summary-cards.vercel.app/api/cards/stats` + `repos-per-language` |
| `github-profile-trophy.vercel.app` | 503 / paused / 超时 | `github-profile-summary-cards.vercel.app/api/cards/profile-details` |

## 常见故障与处理

| 现象 | 根因 | 处理方式 |
|------|------|----------|
| `Post /login/device/code i/o timeout` | 网络不通或直连不稳定 | 切换代理后重试授权 |
| 授权页按钮点不了 | 浏览器会话异常/脚本拦截 | 换浏览器或无痕窗口重新授权 |
| 找不到 `Customize your profile` | 未创建同名公开仓库 | 创建 `<username>/<username>` 公开仓库 |
| Snake 不显示 | `output` 分支未生成 | 检查 workflow run，确认 `output` 分支产物存在 |
| README 更新但页面没变 | GitHub 缓存 | 等待 1-5 分钟后强刷 |

## 用户如何使用（引导话术）

直接对代理说以下任意一句：

```text
帮我把 GitHub 主页做成完整酷炫版，包含 snake，并自动修复图片不显示问题。
```

```text
只做 Lite 版主页，保留我当前 README 的项目介绍段落。
```

```text
排查我主页里不显示的图片，并自动替换为稳定可用的卡片服务。
```

## 交付标准（Done Definition）

- [ ] 主页仓库 README 已更新并推送
- [ ] Snake workflow 运行成功，`output` 分支存在 SVG
- [ ] 关键图片 URL 全部 `HTTP 200`
- [ ] 用户能在主页肉眼看到更新效果
- [ ] 输出最终验收链接和变更摘要
