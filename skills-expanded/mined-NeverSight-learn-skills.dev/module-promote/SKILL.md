---
name: module-promote
description: "Promote an approved page or industry case candidate through the project development and production gates. Use only when an authorized project owner explicitly asks to sync, release, or publish a previously handed-off module and provides the exact candidate scope. Verify repository identities, scoped diffs, quality gates, release completion, live assets, and rollback evidence."
---

# 模块晋级发布

把已经由开发者确认的页面或案例候选，按开发仓 Gate 和生产仓 Gate 逐级晋级。此 Skill 与开发共创分离，绝不因开发者点击确认或生成交接单而自动触发。

## 触发条件

只有同时满足以下条件才开工：

- 项目负责人或具有同等权限的用户在本轮明确要求晋级、同步或发布；
- 提供可定位的候选交接单、分支或提交；
- 明确目标是只到开发仓，还是继续到生产仓；
- 允许执行目标仓库所需的推送和发布操作。

只有开发者确认、没有负责人本轮授权时，保持只读并说明需要负责人启动本 Skill。

## 先核对事实

1. 读取每个目标仓库最近的 `AGENTS.md`、`SAFETY.md`、`OPERATIONS.md` 和本地开发文档。
2. 用 remote URL 与 `.spark/meta.json` 双重识别开发仓和生产仓，不能只看目录名或 remote 名称。
3. 检查候选交接单、基线提交、工作树状态和精确文件范围。用户已有脏改动不得被覆盖或混入发布。
4. 对照 [双仓 Gate 与回执](references/promotion-gates.md) 建立本次晋级清单。

## 开发仓 Gate

1. 从干净远端基线建立隔离工作树，只带入已确认候选的精确变更。
2. 复核页面或案例元数据、渲染契约、默认组合和素材引用。
3. 运行项目要求的 verify、测试、diff 检查，并按风险补充 lint、生产构建和浏览器验收。
4. 仅在已获开发仓发布授权后推送并创建开发仓 release。
5. 等待 release `status=finished`，核对线上 `commit_id` 与发布提交一致。
6. 在真实开发地址验证页面正文、交互、图片、资源 MIME/body 和跳转链路，形成开发仓回执。

开发仓 Gate 未通过时停止，不进入生产仓。

## 生产仓 Gate

1. 再次确认本轮包含生产仓发布授权。
2. 从生产仓干净远端基线创建独立工作树，重放开发仓已经通过的精确候选；不要把开发仓其他改动一起同步。
3. 重新运行相同比例的工程与视觉检查。
4. 推送并创建生产 release，等待 `status=finished`，核对 `commit_id`。
5. 在真实生产地址复验关键页面、交互、访问范围和静态资源。
6. 输出双仓回执及可执行的回退锚点。

## 素材与 TOS

素材可以使用 TOS。不要把“开发仓与生产仓隔离”误解为禁止 TOS，而要把素材内容版本与环境交付地址分开管理：

- 为素材保留不可变内容标识或内容哈希；
- 记录开发仓引用与生产仓引用的映射；
- 如果 TOS 对 App 或环境隔离，生产晋级时重新上传并替换映射；
- 发布后逐项验证图片响应、MIME、内容和页面实际展示；
- 不用可被覆盖的同路径文件冒充版本管理。

## 停止条件

- 无法确认仓库或 App 身份；
- 没有目标环境的本轮明确授权；
- 候选范围不精确，或工作树包含无法隔离的用户改动；
- 质量门失败；
- release 未完成、`commit_id` 不匹配、关键资源或真实页面验证失败；
- 需要数据库迁移、历史报告批量变更或新的产品决策。

停止时保留当前状态、命令、错误和回退锚点，不绕过检查，不强推，不使用跳过钩子的参数。
