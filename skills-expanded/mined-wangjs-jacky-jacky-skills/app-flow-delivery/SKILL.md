---
name: app-flow-delivery
description: "在需要打包、签名、OTA、APK/IPA、GitHub Release、商店提交、部署、回滚或验活时使用；支持独立窄任务，也支持作为 app-flow 的当前行动。它核对具体渠道授权，可复用用户明确记录的项目级 preview OTA 持续授权并在验证通过后自动发布；未获授权只做预检。"
---

# App Flow Delivery

把已构建、已验证的产物按具体渠道交付出去，并对交付本身负责。交付边界由目标仓库与渠道现场决定，不预设某种技术栈或发布方式。

## 授权是第一约束

- 打包、签名、OTA、APK/IPA、Release、商店提交、部署、回滚都属于外部副作用，执行前都要核对当前渠道与动作是否已获用户明确授权。
- 对低风险、可逆的 preview OTA，可复用用户明确授予的**项目级持续授权**。把仓库范围、preview 通道、允许动作与撤销条件写入本 Skill 的 `local/`；授权有效且自动化检查通过后直接自动发布，**不再逐次确认**或提醒用户发布。
- 持续授权只覆盖记录中的项目与 preview 通道。目标仓库或通道变化、原生变化需要重新构建、凭据/回滚条件异常，或用户撤销自动发布时，停止真实发布并报告实际状态。
- 长时间执行或无人值守只延长持续性，**从不**自动获得 push、Release、部署或商店提交授权。
- 未获授权时只做 dry-run 预检并把结果交接给用户，不执行任何真实发布。
- production / 正式 OTA、商店提交、付费、不可逆或公开动作不受 preview 持续授权覆盖，即使有历史授权也先确认当次意图。

## 交付前预检

0. **先读项目 / 本机的具体交付经验，别裸跑自造流程**：本 skill 的 references 只给通用边界，不含具体命令。动手打包 / 发布前，先查当前项目仓库（`AGENTS.md` / `CLAUDE.md` / 脚本）和宿主的 experience 类 skill 的 `local/`——那里往往有本机验证过的精确命令、易漏参数与渠道配置（如「只打 arm64 架构」「发到版本化 Release」「走代理」等）。历史教训：跳过这一步裸跑本地构建，漏了关键参数、打出臃肿包、也漏了规范发布通道。
1. **产物核对**：版本号、内部构建号、包标识、签名、权限、runtime 是否与目标渠道一致且单调递增。
2. **通道匹配**：产物走的更新/分发通道是否与目标渠道（内测/正式/OTA）一致，避免开发产物流入正式。
3. **回滚预案**：能否快速回滚到上一稳定产物；回滚路径本身是否已验证。
4. **上游就绪**：基础代码问题、必要的静态检查与回归是否已由构建/评审完成——交付不修基础问题，发现缺陷退回对应能力。
5. **验活方式**：发布后如何确认真实生效（可安装、可启动、关键路径可用），而不是只看渠道返回成功。

## 参考知识

按当前交付形态选一个读取，不预先展开：

- [`references/ota-production.md`](references/ota-production.md)：正式 OTA 的通用边界——只适用 JS 兼容改动、runtime/通道核对与回滚。
- [`references/ota-preview.md`](references/ota-preview.md)：预览 OTA 的通用边界——内测通道、发布前的可自动化检查。
- [`references/apk-distribute.md`](references/apk-distribute.md)：安装包/直装分发的通用边界——签名、版本、安装来源与完整性。

这些是跨技术栈的思路骨架，不含任何具体命令、地址或密钥；真实渠道配置只留在被忽略的 `local/`。

## 独立与 Flow 两种模式

- **独立模式**：短任务直接返回预检或交付结果，不建立全局恢复点。
- **Flow 模式**：把完整 `outcome`、`acceptance_status`、`authority_check`、`preflight`、`evidence`、`risks`、`next` 返回给 `app-flow` 父 owner，本能力不创建全局恢复指针。

`acceptance_status` 显式取值：`completed`（已授权并有生效证据）、`partial`、`failed`、`unverified`（已发布但未验活）、`blocked`（缺授权、缺产物或渠道未就绪）。只有真实证据支持时才能声称已发布或已生效。

## 本地 Memory

本 Skill 只拥有自己的 `local/`，默认被 `.gitignore` 排除。首次需要读写时，从当前 Skill 目录按需加载 `../../../docs/philosophy/references/local-memory.md`；引用不可读时以本节摘要继续并保留诊断。默认从 `local/INDEX.md` 进入一个作用域 map，再读少量命中正文，不递归扫描。

Memory 使用不可变记录，修正由新记录 `supersedes` 旧 ID；保存不等于可信。渠道地址、账号、token、签名密钥等敏感信息一律不进入 `local/`，属于专门的凭据系统。稳定、脱敏、反复验证的方法才晋升到 `references/`。
