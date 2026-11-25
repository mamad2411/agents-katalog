---
name: git-workflow-and-versioning
description: "Git 工作流与版本管理——Gitee/Coding/极狐 GitLab/GitHub 四平台适配。分支策略、提交规范、合并与变基、标签与发布、回滚与修复。"
version: "4.3.8"
updated: "2026-05-14"
---

# Git 工作流与版本管理

## 平台适配

| 特性 | Gitee | Coding.net | 极狐 GitLab | GitHub |
|------|-------|-----------|------------|--------|
| 国内访问 | 快 | 快 | 快 | 不稳定 |
| 免费私有 | 有 | 有 | 有 | 有 |
| CI/CD | Gitee Go | Coding CI | 内置 GitLab CI | GitHub Actions |
| 代码审查 | PR | MR | MR | PR |
| 制品库 | 有限 | 完整 | 完整 | Packages |
| 适合场景 | 开源/小团队 | 中大型团队 | 企业私有化 | 国际项目 |

### 各平台远程配置

```bash
# Gitee
git remote add origin https://gitee.com/<org>/<repo>.git

# Coding.net
git remote add origin https://e.coding.net/<team>/<project>/<repo>.git

# 极狐 GitLab
git remote add origin https://jihulab.com/<group>/<repo>.git

# GitHub
git remote add origin https://github.com/<org>/<repo>.git
```

### 多平台镜像推送

```bash
git remote set-url --add --push origin https://gitee.com/<org>/<repo>.git
git remote set-url --add --push origin https://github.com/<org>/<repo>.git
```

## 分支策略

### 主干开发（小团队）

```
main ──●──●──●──●──●── (始终可发布)
        \   /  \   /
feat/x  ●─●   ●─●       (短命分支，1-2 天)
```

- main 始终可发布，用 Feature Flag 隐藏未完成功能
- 分支生命周期 ≤ 2 天，每天至少合并一次

### 简化 Git Flow（中大团队）

```
main     ──●──────●──────●──── 生产（受保护）
            \    / \    /
dev      ──●──●─●──●──●─●──── 测试环境
             \  /    \  /
feat/x       ●●      ●●       功能分支
```

- main 受保护，只通过 PR/MR 合并
- feat 从 dev 拉出，合回 dev；dev 通过后合并到 main

## 分支命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 功能 | `feat/<描述>` | `feat/user-login` |
| 修复 | `fix/<描述>` | `fix/payment-crash` |
| 紧急修复 | `hotfix/<描述>` | `hotfix/login-crash` |
| 发布 | `release/v<版本>` | `release/v1.2.0` |

规则：全小写，`-` 连接，前缀明确类型。

## 提交前检查（强制执行）

1. **文档同步** — `README.md`、`AGENTS.md`、`.jarvis/README.md` 是否与本次变更一致
2. **.gitignore 检查** — 是否有新增临时文件类型（截图/日志/数据库/快照等）未加入 `.gitignore`，`git status` 是否干净
3. **版本号递增** — `package.json` 版本号是否按语义化版本递增完毕
4. **质量门** — Lint + Type-check + Test 全部通过

## 提交规范

### 格式

```
<type>(<scope>): <描述>

<详细描述>

<关联信息>
```

### 类型清单

| type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `test` | 测试 |
| `docs` | 文档 |
| `style` | 格式 |
| `chore` | 构建/工具/依赖 |
| `ci` | CI/CD |
| `revert` | 回滚 |

### 规则

- 描述 ≤ 72 字符，祈使语气（"增加"非"增加了"）
- 一个 commit 一件事
- 关联需求 ID：`REQ-XXX` / `Closes #123`
- Co-Authored-By 签名行由 AI 工具自动添加，不要手动删除或修改

### 好 vs 坏

```
✅ feat(auth): 添加用户注册 API [TASK-001]
✅ fix(login): 修复过期 token 未刷新问题
❌ update code / fix bug / WIP
```

## 合并 vs 变基

- **Merge**：功能分支 → 共享分支（安全，保留完整历史）
- **Rebase**：清理本地历史再推送（线性历史）
- **禁止**：rebase 已推送的公共分支

## 标签与版本管理

**每次代码变更完成后必须打 Tag，不可攒批。** 变更即打标，确保每个版本可追溯。

```
MAJOR.MINOR.PATCH
MAJOR：不兼容 API 变更    MINOR：向后兼容新功能    PATCH：Bug 修复
```

```bash
git tag -a v1.0.0 -m "v1.0.0：新增用户注册和登录"
> 🔴 **CI 门禁**：推送 tag 前确认 CI 已通过。Tag push 会触发 CI 发布流水线，CI 未通过时推送 tag 会导致发布失败。
git push origin v1.0.0
```

## 各平台 PR/MR 创建

### Gitee — `.gitee/PULL_REQUEST_TEMPLATE.md`
### Coding / GitLab — `.gitlab/merge_request_templates/default.md`
### GitHub — `.github/PULL_REQUEST_TEMPLATE.md`

```bash
# GitHub CLI
gh pr create --title "<title>" --body "$(cat <<'EOF'
## 变更概述
## 关联需求/任务
## 测试情况
## 部署注意事项
EOF
)"
```

### 模板内容

```markdown
## 变更说明
## 变更类型
- [ ] 新功能 [ ] Bug修复 [ ] 重构 [ ] 性能优化 [ ] 文档
## 关联信息
- 需求/Bug 链接：
## 测试情况
- [ ] 单元测试通过 [ ] 手动测试通过 [ ] 回归测试通过
## 部署注意事项
- [ ] 需数据库迁移 [ ] 需更新配置 [ ] 无特殊
```

## CI/CD 平台对照

| GitHub Actions | Gitee Go | Coding CI | 极狐 GitLab CI |
|---------------|----------|-----------|---------------|
| `on: push` | `triggers: push` | Jenkinsfile | `only:` / `rules:` |
| `jobs.<id>.steps` | `stages.jobs.steps` | `stages.steps` | `script:` |
| `secrets.X` | 环境变量配置 | 凭据管理 | CI/CD Variables |
| `artifacts` | `artifacts` | 制品库 | `artifacts:paths` |

## 回滚与修复

```bash
git revert <hash>          # 撤销已推送的 commit（安全）
git reset --soft HEAD~1    # 撤销未推送的 commit（保留更改）
git checkout -b hotfix/rollback v1.0.0  # 紧急回滚
```

## 常用操作

```bash
git status                    # 当前状态
git log --oneline -20         # 提交历史
git stash / git stash pop     # 暂存/恢复
git diff develop..feat/x      # 分支对比
```

## 反合理化表

| 借口 | 现实 |
|------|------|
| "commit message 随便写，只有我看" | 3 个月后的你也看不懂 |
| "小改动不用分支，直接 main 改" | 没有安全网，出问题无法回滚 |
| "一次 commit 放多个功能省事" | revert 会连坐丢掉其他功能 |
| "force push 没关系" | 破坏其他人的本地分支 |

## 红线

- 不写 commit message
- 共享分支 force push
- hotfix 不走分支流程
- 未测试就提交

## CI 门禁规则

### 推送前检查

| 操作 | CI 要求 |
|------|--------|
| `git push`（分支） | CI 通过（若有 CI） |
| `git push`（tag） | CI 通过（若有 CI）；tag push 触发发布流水线，CI 失败会导致发布失败 |
| PR/MR 创建 | CI 通过（若有 CI） |

### 红线
- CI 未通过不打 tag、不推送分支
- tag push 前必须确认 CI 绿色
- 不允许 `--no-verify` 跳过 CI 检查
