---
name: coff0xc-software-engineering
description: "Use when / 当用户请求 dev/software engineering：build product、repo repair、failing tests/CI、bugfix、feature/refactor、full-stack/end-to-end implementation、REST API/frontend UI implementation、scripts、Python/JS/TS/Go/Rust/Java/C/C++/Shell、dashboard/admin/API、browser smoke、diff/lockfile hygiene、最小修复、直接实现、证明好了。手动触发：使用 coff0xc-software-engineering。"
---

# coff0xc-software-engineering

<!-- skill-id: cs-swe-1a4f8c03 -->

## 快速规则（日常任务先读这里）
> **[先读仓库]** 先看 AGENTS/README、package/lockfile、入口、测试脚本和当前 dirty worktree。
> **[最小修复]** 只改请求范围；先复现/定位，再小步 patch，不做无关重构和新框架迁移。
> **[验证闭环]** 先跑目标 test/typecheck/lint/build，再按风险加宽；没跑不能写已验证。
> **[Git 边界]** 不回滚用户改动；push、PR、删除、生产、凭据、CI/CD 权限先确认。

普通开发任务按本节直接执行；只有大功能、架构/API/schema/auth、CI 发布或 skill 质量验证才展开完整工作流。

如果任务升级为多文件、多阶段、多 skill、架构/API/schema/auth 或多 worker 工作，先让 `coff0xc-skill-router` 读取 `references/complex-workflow.md`。本 skill 在该流程中负责实现、repo repair、测试和 diff 卫生。

## 能力定位
面向真实仓库的工程交付能力。适合把模糊需求变成可运行代码、可复现修复、可验证测试结果和清晰 diff 摘要。

## 能交付什么
- 代码补丁、脚本或配置修改
- 失败原因和根因链路说明
- 单元/集成/构建验证结果
- Git diff 摘要和剩余风险

## 可以接收什么输入
- 本地仓库、报错日志、测试输出、issue 描述
- 需求草稿、接口说明、UI 截图或现有模块
- package/lockfile、README、AGENTS、CI 脚本

## 放心使用的边界
- 可直接做本地、可逆、低风险的代码和测试改动
- 删除、远程 push、生产配置、凭据、付费服务和 CI/CD 权限变更必须先确认
- 不为小问题引入新框架或无必要依赖
- 默认只处理本地、可逆、可验证的低风险工作；涉及生产、凭据、付费、远程写入、删除、发布或权限变更时必须先确认。

## 为什么可以放心
- 先读项目结构和现有风格，再修改
- 先跑窄验证，再按风险跑宽验证
- 未运行的测试不会写成已通过

## 典型使用方式
```text
使用 coff0xc-software-engineering 修复这个 repo 的 failing tests，并说明验证结果。
使用 coff0xc-software-engineering 少问确认，直接实现这个多文件开发任务。
Use coff0xc-software-engineering to build this admin panel feature end to end with tests.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
