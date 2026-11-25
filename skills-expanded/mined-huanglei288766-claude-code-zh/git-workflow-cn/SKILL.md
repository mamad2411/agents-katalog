---
name: git-workflow-cn
description: Git 工作流规范中文版，涵盖分支策略、Commit 规范、Code Review 流程、PR 模板、版本管理、常用操作速查
version: "1.0"
---

# Git 工作流规范

## 概述

本 Skill 定义团队 Git 协作的完整工作流规范，推荐 Trunk-Based Development 模式，适用于持续交付的敏捷团队。

适用场景：
- 新项目建立 Git 工作流规范
- 规范团队的分支策略和 Commit 风格
- 制定 Code Review 和 PR/MR 流程
- 版本号管理和发布流程

---

## 分支策略

### Trunk-Based Development（推荐）

```
main ─────●─────●─────●─────●─────●─────●────── 持续集成主线
           \   /       \   /       \   /
feature/    ●─●    fix/ ●─●   feat/ ●─●         短命分支（1-3 天）
user-auth          login-bug      order-api

release/1.0 ───●──────●                          发布分支（仅需要时创建）
                hotfix
```

**核心原则：**
- `main` 是唯一的长期分支，始终保持可发布状态
- 功能分支生命周期不超过 3 天
- 每天至少合并一次到 `main`
- 使用 Feature Flag 管理未完成功能
- 发布分支仅在需要时从 `main` 切出

### Git Flow（仅复杂发布场景使用）

```
main     ─────●──────────────────●───────── 生产环境
               \                /
develop  ──●────●────●────●────●────●────── 开发主线
            \  / \       /
feature/    ●●    \     /
user-auth          \   /
                 release/1.0 ──●──●         发布分支
                                  │
                               hotfix/      紧急修复
```

**适用条件：** 有明确版本发布节奏、多个版本并行维护。

---

## 分支命名规范

### 格式

```
{类型}/{简短描述}

类型选项：
  feature/     新功能
  fix/         Bug 修复
  hotfix/      生产环境紧急修复
  refactor/    重构
  docs/        文档
  test/        测试
  chore/       构建/工具链
  release/     发布分支
```

### 示例

```bash
# 正确示例
feature/user-auth            # 用户认证功能
feature/order-export-excel   # 订单导出 Excel
fix/login-token-expired      # 修复登录 token 过期问题
hotfix/payment-amount-error  # 紧急修复支付金额错误
refactor/order-domain-model  # 重构订单领域模型
release/1.2.0                # 1.2.0 版本发布分支

# 错误示例
feature/1                    # 无意义的名称
fix-bug                      # 缺少 / 分隔符
Feature/UserAuth             # 不要用大写
feature/add-user-authentication-and-authorization-module  # 太长
```

### 命名规则

```
规则                              示例
──────────────────────────────────────────────
全小写                            feature/user-auth
单词用连字符分隔                   fix/login-token-expired
不超过 50 个字符                   保持简洁
包含关联的 Issue 编号（可选）       fix/GH-123-login-bug
不包含个人姓名                     不要 feature/zhangsan-xxx
```

---

## Commit Message 规范

### 格式（Conventional Commits）

```
<类型>(<范围>): <描述>

<正文>（可选）

<脚注>（可选）
```

### 类型说明

```
类型       说明                             示例
────────────────────────────────────────────────────────────
feat       新功能                           feat(order): 添加订单导出功能
fix        Bug 修复                         fix(auth): 修复 token 刷新失败的问题
refactor   重构（不改变功能）                refactor(user): 重构用户领域模型
perf       性能优化                         perf(query): 优化订单列表查询性能
docs       文档更新                         docs(api): 更新 API 接口文档
test       测试相关                         test(order): 添加订单创建单元测试
chore      构建/工具链                      chore(deps): 升级 Spring Boot 到 3.2.0
ci         CI/CD 配置                       ci(github): 添加自动化部署流水线
style      代码格式（不影响逻辑）            style: 统一代码缩进为 4 空格
build      构建系统变更                      build(docker): 优化 Dockerfile 多阶段构建
revert     回退提交                         revert: 回退 feat(order) 订单导出功能
```

### 范围说明

```
范围用模块名或功能域，例如：
  (order)      — 订单模块
  (user)       — 用户模块
  (auth)       — 认证授权
  (payment)    — 支付模块
  (gateway)    — 网关
  (config)     — 配置
  (deps)       — 依赖
  (docker)     — Docker 相关
  (api)        — API 接口
```

### 完整示例

```bash
# 简单提交
git commit -m "feat(order): 添加订单批量导出功能"

# 带正文的提交
git commit -m "$(cat <<'EOF'
fix(payment): 修复支付金额精度丢失问题

支付金额使用 double 类型计算导致精度丢失，
改为使用 BigDecimal 进行金额运算。

影响范围：
- PaymentService.calculateAmount()
- OrderService.createOrder()

Closes #234
EOF
)"

# 包含 Breaking Change 的提交
git commit -m "$(cat <<'EOF'
feat(api)!: 统一 API 响应格式

将所有 API 响应封装为 Result<T> 格式：
{
  "code": 200,
  "message": "success",
  "data": {}
}

BREAKING CHANGE: 所有 API 响应格式变更，
前端需要统一适配新的响应结构。

Closes #456
EOF
)"
```

### Commit 检查规则

```
规则                                    说明
──────────────────────────────────────────────────────────
描述使用中文                             方便团队成员阅读
描述不超过 50 个字符                     简洁明了
描述不以句号结尾                         节省空间
正文每行不超过 72 个字符                 方便终端阅读
正文解释 "为什么" 而不是 "做了什么"       why > what
一个 commit 只做一件事                   原子化提交
不提交无关的格式化变更                   另起 style 类型提交
```

---

## Code Review 流程

### 流程图

```
开发者                        审查者                      CI/CD
  │                            │                          │
  ├─ 创建 PR ────────────────►│                          │
  │                            │                          │
  │                            │◄──── 自动触发检查 ────── │
  │                            │      (lint/test/build)   │
  │                            │                          │
  │◄── 提出修改意见 ──────────│                          │
  │                            │                          │
  ├─ 修改代码 ───────────────►│                          │
  │                            │                          │
  │◄── Approve ───────────────│                          │
  │                            │                          │
  ├─ Squash Merge ───────────────────────────────────────►│
  │                            │                     自动部署
  ├─ 删除分支                  │                          │
```

### Review 清单

```markdown
## 必查项（任何 PR）
- [ ] CI 检查全部通过（lint、test、build）
- [ ] 代码逻辑正确，无明显 Bug
- [ ] 无安全问题（SQL 注入、XSS、硬编码密钥等）
- [ ] 错误处理完善，无静默吞异常
- [ ] 命名清晰，代码可读性良好

## 功能性检查
- [ ] 业务逻辑符合需求描述
- [ ] 边界情况已处理（空值、并发、超时）
- [ ] 接口参数校验完整
- [ ] 返回值格式符合 API 规范

## 架构检查
- [ ] 分层正确（无跨层调用）
- [ ] 数据库查询已优化（无 N+1，已加索引）
- [ ] 新增的公共方法有单元测试
- [ ] 向后兼容（API、数据库 Schema）

## 可选检查
- [ ] 日志记录合理（关键路径有日志，无敏感信息）
- [ ] 配置项是否需要在各环境同步
- [ ] 文档是否需要更新
```

### Review 礼仪

```
作为审查者：
  - 先肯定优点，再提改进建议
  - 区分 "必须修改" 和 "建议优化"
  - 用 "我们可以考虑..." 而非 "你应该..."
  - 提供具体的改进方案，不只是指出问题
  - 对不确定的问题用 "nit:" 或 "question:" 前缀

作为开发者：
  - 理解 Review 是对代码不是对人
  - 所有评论都要回复（同意就改，不同意就讨论）
  - 不要在 Review 中加入无关的变更
  - PR 提交前先自己 Review 一遍
```

---

## PR/MR 模板

### PR 模板文件

```markdown
<!-- .github/pull_request_template.md -->
## 变更说明

<!-- 简要描述本次变更的内容和目的 -->

## 变更类型

- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 重构 (refactor)
- [ ] 性能优化 (perf)
- [ ] 文档更新 (docs)
- [ ] 测试 (test)
- [ ] 构建/CI (chore/ci)

## 关联 Issue

<!-- 关联的 Issue 编号，如 Closes #123 -->

## 变更详情

<!-- 详细描述变更内容，包括：
  - 为什么要做这个变更
  - 采用了什么方案
  - 有什么需要注意的地方
-->

## 影响范围

<!-- 本次变更可能影响的模块或功能 -->

## 测试说明

- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试通过

<!-- 描述测试步骤或截图 -->

## 数据库变更

- [ ] 无数据库变更
- [ ] 有数据库变更（请附 SQL 脚本路径）

## 部署注意事项

<!-- 是否需要：配置变更、数据迁移、服务重启等 -->

## 检查清单

- [ ] 代码已自我 Review
- [ ] Commit Message 符合规范
- [ ] 无硬编码密钥或敏感信息
- [ ] 接口向后兼容
```

---

## 版本号管理（SemVer）

### 语义化版本格式

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

示例：
  1.0.0         — 正式版
  1.2.3         — 正式版
  2.0.0-alpha.1 — 预发布版
  2.0.0-beta.3  — Beta 版
  2.0.0-rc.1    — Release Candidate
  1.2.3+build.456 — 带构建元数据
```

### 版本号递增规则

```
变更类型                      版本号变化         示例
──────────────────────────────────────────────────────────
Bug 修复、向后兼容的小改动     PATCH +1          1.2.3 → 1.2.4
新增功能、向后兼容             MINOR +1          1.2.4 → 1.3.0
不兼容的 API 变更              MAJOR +1          1.3.0 → 2.0.0
```

### 自动化版本管理

```bash
# 使用 standard-version 自动生成版本号和 CHANGELOG
npx standard-version                    # 自动判断版本号
npx standard-version --release-as major # 强制大版本
npx standard-version --release-as minor # 强制次版本
npx standard-version --release-as patch # 强制补丁版本
npx standard-version --prerelease alpha # 预发布版本

# Maven 项目版本管理
mvn versions:set -DnewVersion=1.2.0
mvn versions:commit

# 发布流程
git tag -a v1.2.0 -m "Release v1.2.0: 订单导出功能"
git push origin v1.2.0    # 触发 CI 发布流水线
```

### CHANGELOG 示例

```markdown
# Changelog

## [1.3.0] - 2026-03-14

### 新功能
- feat(order): 添加订单批量导出功能 (#234)
- feat(user): 支持手机号登录 (#256)

### Bug 修复
- fix(payment): 修复支付金额精度丢失问题 (#267)
- fix(auth): 修复 token 刷新偶发失败 (#271)

### 性能优化
- perf(query): 优化订单列表查询，响应时间降低 60% (#280)

## [1.2.1] - 2026-03-01

### Bug 修复
- fix(order): 修复订单状态流转异常 (#220)
```

---

## 常用 Git 操作速查

### rebase vs merge

```bash
# merge — 保留分支历史，产生合并提交
git checkout main
git merge feature/user-auth
# 结果：main 上多一个 merge commit，保留完整分支图

# rebase — 线性历史，无合并提交（推荐个人分支使用）
git checkout feature/user-auth
git rebase main
# 结果：feature 分支的提交被"移植"到 main 最新提交之后

# 交互式 rebase — 整理提交历史（合并、重排、修改）
git rebase -i HEAD~3
# 在编辑器中选择 pick/squash/fixup/reword/drop

# 黄金规则：不要对已推送到公共分支的提交做 rebase
```

### cherry-pick

```bash
# 选取特定提交到当前分支
git cherry-pick abc1234

# 选取多个提交
git cherry-pick abc1234 def5678

# 选取一个范围（不包含起点）
git cherry-pick abc1234..ghi9012

# 只暂存变更，不自动提交（用于合并多个 cherry-pick 为一个提交）
git cherry-pick --no-commit abc1234

# 解决冲突后继续
git cherry-pick --continue

# 放弃 cherry-pick
git cherry-pick --abort
```

### stash

```bash
# 暂存当前工作区变更
git stash

# 暂存并添加描述
git stash push -m "订单导出功能开发中"

# 暂存包括未跟踪的文件
git stash -u

# 查看暂存列表
git stash list
# stash@{0}: On feature/order-export: 订单导出功能开发中
# stash@{1}: WIP on main: abc1234 fix: login bug

# 恢复最近的暂存（保留 stash 记录）
git stash apply

# 恢复最近的暂存（删除 stash 记录）
git stash pop

# 恢复指定的暂存
git stash apply stash@{1}

# 删除指定暂存
git stash drop stash@{0}

# 清空所有暂存
git stash clear
```

### 其他常用操作

```bash
# 查看文件的每一行最后由谁修改
git blame src/main/java/com/example/OrderService.java

# 二分查找引入 Bug 的提交
git bisect start
git bisect bad                 # 当前版本有 Bug
git bisect good v1.2.0         # v1.2.0 没有 Bug
# Git 自动切换到中间版本，测试后标记 good/bad，直到定位问题提交
git bisect reset               # 结束查找

# 查看某个文件的修改历史
git log --oneline --follow -- path/to/file

# 查看两个分支的差异
git diff main..feature/user-auth

# 撤销已提交但未推送的 commit（保留变更）
git reset --soft HEAD~1

# 修改最近一次 commit message
git commit --amend -m "feat(order): 更新 commit 描述"

# 从其他分支获取单个文件
git checkout main -- path/to/file

# 清理已合并的本地分支
git branch --merged main | grep -v "main" | xargs git branch -d

# 查看远程分支
git branch -r

# 删除远程分支
git push origin --delete feature/old-branch
```

---

## .gitignore 模板

### Java + Spring Boot 项目

```gitignore
# ===== 编译产物 =====
target/
build/
*.class
*.jar
*.war

# ===== IDE =====
.idea/
*.iml
*.iws
.vscode/
.settings/
.classpath
.project
.factorypath
*.swp
*.swo

# ===== 日志 =====
*.log
logs/

# ===== 环境变量和敏感信息 =====
.env
.env.*
application-local.yml
application-local.properties
*-secret.yml

# ===== OS =====
.DS_Store
Thumbs.db
desktop.ini

# ===== Maven =====
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# ===== Gradle =====
.gradle/
build/

# ===== Docker =====
docker-compose.override.yml

# ===== 测试报告 =====
coverage/
test-results/
```

### Node.js / 前端项目

```gitignore
# ===== 依赖 =====
node_modules/
.pnp
.pnp.js

# ===== 构建产物 =====
dist/
build/
.next/
.nuxt/
out/

# ===== 环境变量 =====
.env
.env.local
.env.*.local

# ===== 日志 =====
*.log
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*

# ===== IDE =====
.idea/
.vscode/
*.swp

# ===== 测试 =====
coverage/
.nyc_output/

# ===== OS =====
.DS_Store
Thumbs.db

# ===== 缓存 =====
.eslintcache
.stylelintcache
*.tsbuildinfo
```

### 通用 .gitignore 原则

```
规则                                    说明
──────────────────────────────────────────────────────────
忽略构建产物                             target/, dist/, build/
忽略依赖目录                             node_modules/, vendor/
忽略 IDE 配置                            .idea/, .vscode/
忽略环境变量文件                          .env, .env.local
忽略日志文件                             *.log, logs/
忽略 OS 系统文件                          .DS_Store, Thumbs.db
不忽略锁文件                              保留 pnpm-lock.yaml, package-lock.json
不忽略 CI 配置                            保留 .github/, .gitlab-ci.yml
不忽略编辑器统一配置                       保留 .editorconfig
```

---

## 常见问题速查

| 问题 | 解决方案 |
|------|---------|
| 提交了敏感信息（密钥等） | 用 `git filter-branch` 或 BFG 清理历史，并立即轮换密钥 |
| merge 冲突太多 | 缩短分支生命周期，频繁 rebase main |
| commit 历史混乱 | 合并前用 `git rebase -i` 整理，或使用 Squash Merge |
| 误删分支 | `git reflog` 找到 SHA，`git branch recover-branch SHA` 恢复 |
| 大文件误提交 | 使用 Git LFS 管理大文件，用 BFG 清理历史 |
| 多人同改一个文件 | 拆分大文件，明确模块归属，缩短 PR 周期 |
| 忘记切分支就写了代码 | `git stash` → 切分支 → `git stash pop` |
| CI 不通过无法合并 | 先在本地跑通测试再推送，善用 pre-commit hook |
