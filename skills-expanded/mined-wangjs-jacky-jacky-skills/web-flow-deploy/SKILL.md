---
name: web-flow-deploy
description: "web-flow 内部的 provider-neutral 部署阶段：在明确授权的前提下执行供应者预检，并在 G3 后发布，用 HTTP、浏览器和控制台证据验证真实 URL。仅在 web-flow 主 Skill 明确调用时使用；支持 preflight 与 publish。不要因普通用户请求单独触发。"
---

# web-flow-deploy · 预检与发布

本入口保持 provider-neutral：按当前环境选择已授权的部署供应者，供应者命令放在单独 reference。当前内置操作说明见 [provider reference](references/cloudflare-pages.md)。机器事件与证据要求以 [WebFlow 运行时](../web-flow/references/runtime-state.md)为准。

## 独立 memory

若本 Skill 的 `memory/index.md` 存在，只读取部署凭证、项目初始化和验活相关的 1–3 条记忆；不存在时直接继续。通过三项验证的候选只写回本 Skill 的 `memory/`。

## 授权边界

部署请求不等于授权。run 初始化时已明确 requested+authorized，可在开局执行一次只读早期 preflight；若初始化时未授权，只能在 G3 已批准之后、finalize 之前由用户追加授权。unattended 不能代替授权。未授权时不得登录、查询账号、创建远端项目、发布或调用 `deploy record`。

## `preflight` 模式

只在 run 同时满足 deployment requested 和 deployment authorized 时执行。初始化已授权可在开局预检；G3 后补授权则在进入 deploy 时预检。

1. 检查 provider CLI 或 API 是否可用，并验证当前登录身份。
2. 确认目标项目、生产分支、构建目录和创建权限；不存在时只记录 `needs_project_create`。
3. 写 `preflight/deployment-readiness.md`，包含 checkedAt、provider、命令摘要、退出结果，以及 CLI、身份、项目三类检查。早期 preflight 尚无 build，不得伪造 build ref/hash。
4. 调用 runtime `deploy record --mode preflight`。Node 只校验并登记证据，不执行网络操作。

预检失败时阻断 deploy，但不破坏 build、G3 或本地 preview。

## `publish` 模式（G3 后）

1. 再次校验 authorization event 位于 G3 后、finalize 前，并确认当前 build hash 仍与 G3 绑定一致。
2. publish 前重新执行会漂移的 preflight；旧身份、旧项目状态或旧 build 证据不能复用。
3. 只有当前授权覆盖远端创建时，才创建缺失项目；随后发布 sourceDir 构建产物。
4. 记录公开 HTTPS URL、provider 结果与 build ref/hash，不记录凭证或本机路径。
5. 验证三项事实证据：HTTP 成功、真实 browser 打开成功、console 与关键资源无阻断错误。
6. 写 `deploy/deployment-evidence.md` 和 `deploy/stage-result.md`，再调用 runtime `deploy record --mode publish`。证据文件一旦登记不可覆盖。
7. 调用独立 benchmark；deploy must-pass 全过后才能完成 deploy stage。

发布或验活失败时保留已批准 preview，把 deploy 保持 blocked，并以可解释 residual finalize 为 partial；不能把失败伪装成 success，也不能回滚已验证 build。

## 产物

- preflight：`preflight/deployment-readiness.md`
- publish：`deploy/deployment-evidence.md`
- publish stage result：`deploy/stage-result.md`

## 交接评分

publish 后调用 `web-flow-benchmark` 的 deploy rubric。主观评分最多两轮；URL、HTTP、browser、console、资源和 build hash 等 must-pass 必须以真实证据通过。
