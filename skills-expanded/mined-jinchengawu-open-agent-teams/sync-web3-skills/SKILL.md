---
name: sync-web3-skills
description: 用户要接入或更新 web3-fe-superpowers、降低 install 门槛时使用——优先用 run-web3-skills-install.sh 与 .env.web3-skills，详见同包 dev-ops/skills.md
---

# Sync Web3 Skills（低门槛接入/更新）

## 何时用

- 业务仓库**首次**安装 Cursor / Claude / `.agents` 下的 superpowers skills
- **定期同步**远端 `ai-work-flow` 中 `packages/web3-fe-superpowers` 的更新
- 用户不想每次手写一长串 `export`

## 推荐步骤（业务仓库）

1. 在**业务仓库根**放置配置文件（任选其一）：
   - **本机已有 monorepo**：`.env.web3-skills` 中设置 `WEB3_FE_SUPERPOWERS_LOCAL_PATH` 为 `.../packages/web3-fe-superpowers` 的绝对路径（无需 Token）。
   - **GitLab 克隆**：复制模板 `packages/web3-fe-superpowers/templates/env.web3-skills.example` 为 **`.env.web3-skills`**，填写 `WEB3_FE_SUPERPOWERS_REPO_URL` 与 `WEB3_FE_SUPERPOWERS_GIT_TOKEN`。
   - 或：在 `~/.config/web3-fe-superpowers/env` 放同一套变量（多项目共用 Token / 本地路径时方便）。
2. 确保已存在 **`.cursor/skills/dev-ops/`** 下的 `install-web3-skills.sh` 与 **`run-web3-skills-install.sh`**（随 ai-work-flow 安装脚本分发）。
3. 在业务仓库内执行：

```bash
bash .cursor/skills/dev-ops/run-web3-skills-install.sh
```

4. 检查 `git status`，确认无误后提交。

## 与 `install-web3-skills` 的关系

- **`run-web3-skills-install.sh`**：加载 `.env` → 调用 **`install-web3-skills.sh`**（实际克隆与合并逻辑不变）。
- 完整环境变量与故障排查见 **[`dev-ops/skills.md`](../dev-ops/skills.md)**。

## 安全

- **勿**将含 Token 的 `.env.web3-skills` 提交到 Git。
- CI 使用受保护变量注入，勿写进仓库脚本。
