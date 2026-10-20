---
trigger: always_on
description: AMS 项目级规则（管理端工作区）。等价于根仓库 .windsurf/rules/project.md，对所有 Windsurf 会话生效。
---

# AMS 项目规则（管理端）

> 与根仓库 `/AGENTS.md` 同源；如有冲突以本文件为准（管理端工作区专用）。
> **完整版**：`admin/AMS.md`。
> CloudBase 模板规则继续生效（见 `admin/.windsurf/rules/cloudbase-rules.md` 与 `admin/rules/`）。

## 项目身份

- AMS = 资产管理系统（学校资产入库 / 借还 / 看板）。
- 本工作区 = 管理员 Web 端（Vue3 + Vite + Tailwind + DaisyUI + CloudBase JS SDK）。
- 兄弟端：教师微信小程序在 `../app/`（unibest + wot-ui v2）。
- 主题色：主 `#0096C2`，辅 `#006B8F`。**严禁 emoji**。
- 集合命名前缀：`ams_xxx`。

## 必读顺序（每次新会话过一遍）

1. `AMS.md`（本工作区精简手册）
2. `docs/README.md` → `docs/01-overview.md` → `docs/02-architecture.md` → `docs/03-data-model.md` → `docs/04-api-spec.md`
3. `docs/05-admin-features.md`（**管理端功能锚点**）
4. `docs/09-dev-conventions.md`
5. `.memory/PROGRESS.md`（当前进度）
6. `.memory/CHANGELOG.md`（重要历史变更）

> `docs/`、`.memory/`、`data/` 三个目录通过 junction 挂载，写入它们即写入根仓库。

## 子目录附加规则（按需读）

- 写云函数：`rules/cloud-functions/`
- 写 UI：`rules/ui-design/`
- 数据库 SDK：`rules/no-sql-web-sdk/`
- 鉴权：`rules/auth-tool/`、`rules/auth-web/`
- 接 AI：`rules/ai-model-cloudbase/`、`rules/ai-model-web/`

## 工程铁律

1. **字段事实唯一源** = `docs/03-data-model.md`。改字段先改文档。
2. **三端字段一致**：同名字段三端必须一致。
3. **读 SDK / 写云函数**：列表与看板用 SDK 直连；写操作通过云函数（鉴权 + 审计 + 日志）。
4. **业务状态枚举固定**：`IDLE` / `IN_USE` / `LENT` / `PENDING` / `MAINTAIN` / `SCRAPPED`。
5. **借用申请状态**：`PENDING` / `APPROVED` / `REJECTED` / `CANCELLED` / `RETURNED`。
6. **模块边界**：`admin/src/modules/<m>/` 内文件由该模块独占编辑。
7. **TypeScript 严格**：禁止 `any` / `@ts-ignore` / 空 `try/catch` / 删失败用例。
8. **完成前自验证**：`tsc --noEmit` + lint + build；UI 改动手动跑通。
9. **不擅自 git 提交**：提交时机由用户决定。

## 用户表达"提交"意图时的强制动作

当用户说出 **"提交 / commit / 推送 / push / 提到 GitHub / 提一下代码"**：

1. 更新 `.memory/PROGRESS.md`（已完成段追加，未完成移待办）。
2. 评估是否触发 `.memory/CHANGELOG.md`（数据库 / 云函数 / 路由 / 流程 / 依赖 / 部署任一变更即追加）。
3. `.memory/` 下的更新纳入本次 commit。
4. Commit message 用 Conventional Commits。

> 用户只说"保存"或"运行"不触发；用户说"不更新文档"则跳过。

## 禁止事项

- 业务代码不放仓库根（归 `admin/src/modules/` 或 `cloudfunctions/`）。
- `.env` / 代码不存秘钥；秘钥走 CloudBase 控制台环境变量。
- 进了子目录不读子目录规则。
- 用 `any` / 空 catch / 删失败用例换"通过"。
- agent 主动执行 `git commit` / `git push`。

## 协作建议

- 写完阶段性工作即使不提交，也更新 `.memory/PROGRESS.md`，便于跨会话续作。
- 遇歧义先查 `docs/11-open-questions.md`；不清楚就停下问用户，不要猜字段或规则。
