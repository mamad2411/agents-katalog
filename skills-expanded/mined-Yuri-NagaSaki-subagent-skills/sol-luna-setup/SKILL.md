---
name: sol-luna-setup
description: |
  在新机器或新项目上落地「高智商领导 + 便宜执行」分层子代理：Codex Sol 领导 + Luna 工人，
  可选 Claude Code 项目级 agents 与 Pi/pi-flow 跨工具编排。用于：
  (1) 从零安装并配置 Codex / Claude Code / Pi
  (2) 写入项目级 .codex/agents、AGENTS.md、.claude/agents
  (3) 修复 Sol 无法 spawn Luna 的 multi-agent catalog 问题
  (4) 跑 Sol/Luna/多代理冒烟验证
  触发：新机器设置、Sol-Luna、分层子代理、multi-agent 配置、codex agents 初始化
---

# Sol + Luna 分层子代理 Setup Skill

> Install: `npx skills add Yuri-NagaSaki/subagent-skills -g -y`  
> Repo: https://github.com/Yuri-NagaSaki/subagent-skills  
> Guide: https://catcat.blog/2026/08/sol-luna-layered-subagents-codex-claude-pi.html

## 目标

在**不把密钥写入仓库**的前提下，让项目具备：

- 主会话 **gpt-5.6-sol**（领导）
- 工人 **gpt-5.6-luna**（scout / worker / critic / tester）
- 项目级配置可 git 共享
- 可验证的冒烟结果

## 硬性安全规则

1. **永远不要**把 API Key、主机 IP、SSH 密码、私钥写进 `config.toml`、`AGENTS.md`、README、文章正文或 git commit。
2. 密钥只用环境变量：`OPENAI_API_KEY` / `GATEWAY_API_KEY` / `ANTHROPIC_API_KEY` 等。
3. `model_providers.*.env_key` 只写变量**名**。
4. 大文件 `models-v1.json` 默认 gitignore，用脚本生成。

## 前置

- Linux / macOS，Node.js 20+
- 可访问的 OpenAI-compatible **Responses** 端点（`wire_api = "responses"`）
- 账号侧启用 `gpt-5.6-sol` 与 `gpt-5.6-luna`

## 标准流程（Agent 必须按序执行）

### 0. 探测

```bash
node -v && npm -v
command -v codex || true
command -v claude || true
command -v pi || true
test -n "${OPENAI_API_KEY:-}" && echo "OPENAI_API_KEY=set" || echo "OPENAI_API_KEY=MISSING"
```

若缺少 Key：停止并要求用户 export，**不要**在对话外落盘明文。

### 1. 安装 CLI

```bash
npm i -g @openai/codex @anthropic-ai/claude-code
# 可选
npm i -g @earendil-works/pi-coding-agent
# 或 curl -fsSL https://pi.dev/install.sh | sh
pi install npm:@kky42/pi-flow   # 可选，需已装 pi
```

### 2. 全局个人默认（可选）

写入 `~/.codex/config.toml`（仅个人默认）：

- `model = "gpt-5.6-sol"`
- `default_subagent_model = "gpt-5.6-luna"`
- `[features] multi_agent = true`，`multi_agent_v2 = false`（配合 V1 catalog）
- `[model_providers.gateway]` + `env_key = "OPENAI_API_KEY"`

**不要**复制用户的真实 Key 进文件。

### 3. 项目级模板

在项目根运行：

```bash
bash /path/to/subagent-skills/scripts/bootstrap.sh "$(pwd)"
# 或安装 skill 后:
# bash ~/.claude/skills/sol-luna-setup/scripts/bootstrap.sh "$(pwd)"
```

会创建/更新：

```text
.codex/config.toml
.codex/agents/luna_{scout,worker,critic,tester}.toml
AGENTS.md
.claude/agents/luna-{scout,worker,critic}.md
CLAUDE.md
scripts/prepare-luna-catalog.sh
.gitignore 条目：.codex/models-v1.json、.env
```

保留用户已有无关配置；冲突时合并而非盲覆盖。

### 4. 修复 Sol → Luna spawn（必做）

症状：

```text
Unknown model `gpt-5.6-luna` for spawn_agent.
Available models: gpt-5.6-sol, gpt-5.6-terra
```

原因：目录里 Sol/Terra 常为 multi-agent **v2**，Luna 为 **v1**，V2 过滤掉 Luna。

处理：

```bash
bash scripts/prepare-luna-catalog.sh "$(pwd)/.codex/models-v1.json"
# 将 model_catalog_json 设为该文件的绝对路径
# multi_agent_v2 = false
```

### 5. 验证（必须全部通过再宣称完成）

```bash
# 单模型（注意 </dev/null）
codex exec --sandbox read-only -c 'model="gpt-5.6-sol"' \
  "Reply with exactly: SOL_SMOKE_OK" </dev/null

codex exec --sandbox read-only -c 'model="gpt-5.6-luna"' \
  "Reply with exactly: LUNA_SMOKE_OK" </dev/null

# 多代理
codex exec --sandbox read-only \
  "按 AGENTS.md spawn luna_scout 只读说明仓库结构，输出以 SCOUT_DONE 开头" </dev/null

# 可选 Pi
export GATEWAY_API_KEY="${OPENAI_API_KEY}"
pi --print --provider gateway --model gpt-5.6-sol --no-session --no-tools "Reply: PI_SOL_OK"
pi --print --provider gateway --model gpt-5.6-luna --no-session --no-tools "Reply: PI_LUNA_OK"
```

Claude Code：

- 非 root 用户更稳妥
- 对 haiku 做一次 `claude -p` 冒烟；若网关 Anthropic 通道 502，记录为供应商问题，仍可提交 agents 文件

### 6. 交付报告模板

```markdown
## Sol-Luna Setup Report
- Host OS / Node / Codex / Claude / Pi versions:
- Project path:
- Files created:
- Catalog fix applied: yes/no
- SOL_SMOKE: pass/fail
- LUNA_SMOKE: pass/fail
- MULTI_AGENT SCOUT_DONE: pass/fail
- Pi SOL/LUNA: pass/fail/skip
- Secrets in git: none (confirmed)
- Next user action:
```

## 角色政策（写入 AGENTS.md）

| 角色 | 模型 | 权限 |
|------|------|------|
| 主会话 Sol | gpt-5.6-sol | 规划、审核、commit/PR |
| luna_scout | gpt-5.6-luna | read-only |
| luna_worker | gpt-5.6-luna | workspace-write，禁止 commit |
| luna_critic | gpt-5.6-luna | read-only 对抗审查 |
| luna_tester | gpt-5.6-luna | 跑指定测试，返回证据 |

## 常见失败

| 现象 | 处理 |
|------|------|
| spawn 无 Luna | V1 catalog + multi_agent_v2=false |
| codex 吞掉后续 shell | `codex exec ... </dev/null` |
| wire_api 报错 | 使用 `responses`；确认网关实现 `/v1/responses` |
| Claude root 拒绝 bypass | 换非 root 或降低 permission mode |
| 工人写冲突 | 降并发、按文件分区 |
| 密钥进 diff | 立即剔除、轮换密钥 |

## 参考文件

- `scripts/bootstrap.sh` — 项目脚手架
- `scripts/prepare-luna-catalog.sh` — 模型目录修复
- `references/project-template/` — 可复制模板
- 博客长文：https://catcat.blog/2026/08/sol-luna-layered-subagents-codex-claude-pi.html
- 源仓库：https://github.com/Yuri-NagaSaki/subagent-skills

## Agent 行为准则

- 先探测、再安装、再写项目文件、再修 catalog、再验证。
- 展示关键 diff；不覆盖无关用户配置。
- 验证失败时给出可执行修复，不要假装成功。
- 用户若要求「只配置 Sol 和 Luna」：不要启用 Terra 作为默认，catalog 里可保留 Terra 条目仅用于兼容。
---
