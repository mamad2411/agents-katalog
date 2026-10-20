---
name: hunt-dependency-confusion
description: 依赖与包名供应链边界专项：验证自有构建配置是否把内部包名、registry 优先级、锁文件和发布权限错误暴露给外部解析；不发布包或触发构建。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-dependency-confusion

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`package_manifest`、`internal_package_name`、`registry_config`、`lockfile`、`ci_dependency_install`、`package_scope_hint`。

## 2. Preconditions / Discovery

仅在组织明确授权的 package namespace/registry 与只读 CI 配置下，识别 package manager、内部 scope、registry mapping、lockfile、缓存和发布策略；公开同名包不是结论。

## 3. Minimal Safe Validation

静态/只读审计 manifest、lockfile、registry 配置和自有测试 namespace，使用本地 resolver 配置模拟优先级，不向公共 registry 发布、保留或抢注名称。

## 4. Oracle / False Positives

有效：受控本地解析模型和构建配置证据一致显示内部依赖会被错误解析到未授权 registry，且 owner 确认该 namespace 属于组织。缺少 lockfile、搜索命中、理论猜测不成立。

## 5. Stop / Evidence / Routing

停止：发布/注册/占用包名、改 CI、触发生产构建、读取 registry token。保存 config/lockfile 的脱敏摘要、owner 证据、模拟结果。CI 相关转 `hunt-cicd`，IaC/secret 转 `hunt-iac-secret-exposure`。
