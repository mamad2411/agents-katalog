---
name: multiplatform-release
description: Reference library for multiplatform game engineering — three-engine capability matrix and selection method, platform package and compliance constraints, per-platform release checklists, and project structure conventions for Cocos Creator, Unity and Godot. Use whenever you need concrete platform limits, engine support status, release checklists or project layout guidance.
---

# 多引擎多平台工程与发布规范（参考库）

本技能是「全平台游戏开发专家团」的共享参考资料库，覆盖 **Cocos Creator / Unity / Godot** 三引擎与 **微信抖音小游戏、Android、iOS、HarmonyOS、Windows、Web、Linux** 七类分发目标。**Unreal Engine 5 未纳入本矩阵**：其平台支持结论由 `unreal-engineer` 按 UE 大版本 + 目标平台单独评估，并以 Epic 官方文档核实，不套用本文件的三引擎判断。

## 查哪份文件

| 你要回答的问题 | 读哪份 |
|---------------|--------|
| 该选哪个引擎、某引擎支不支持某平台、跨引擎怎么迁 | `references/engine-matrix.md` |
| 某平台包体上限多少、需要什么资质、审核看什么 | `references/platform-matrix.md` |
| 发布前逐项检查什么、三引擎构建配置差异 | `references/release-checklist.md` |
| 工程目录怎么组织、资源放哪、分包怎么切 | `references/project-structure.md` |

路径相对于本技能目录（`skills/multiplatform-release/`）。

## 四条使用铁律

1. **数字必须复核**：包体上限、审核细则、资质要求会随平台政策变化。引用时必须标注"以官方最新文档为准"并指出复核入口。禁止把这里的数字当成永久事实直接写进交付物而不加限定。
2. **引擎能力必须带版本**：三引擎对同一平台的支持状态差异极大且迭代快。任何"支持 / 不支持"都必须写清引擎版本与核实方式。
3. **先约束后方案**：技术方案、美术规格、音频预算，都必须在「引擎 × 平台」约束确认之后给出。顺序反了就会返工。
4. **平台差异逐条说**：不要用"移动端""小游戏平台"一概而论。微信与抖音规则不同，Android 与 HarmonyOS 的构建与上架流程不同，iOS 与 Android 的支付与隐私要求不同。

## 三引擎速览（方向性判断，不是选型结论）

| 引擎 | 语言 | 最强场景 | 小游戏平台 | 主要风险 |
|------|------|---------|-----------|---------|
| Cocos Creator 3.x | TypeScript | 微信/抖音小游戏、H5、2D 与轻量 3D 手游 | 原生支持 | 三方 SDK 相对少、3D 重度上限较低 |
| Unity | C# | 3D 中重度、PC/主机/移动、生态最全 | 通常需 WebGL 转换，损耗需实测 | 包体大、转换后性能打折、授权政策 |
| Godot 4.x | GDScript / C# | 2D 与中小体量独立游戏、开源可控、PC 发行 | 缺官方路径，需第三方或自研 | 商业 SDK 少、部分平台导出成熟度待核实 |

真实选型必须按 `references/engine-matrix.md` 的五维矩阵逐项打分，并写出"结论会反转的条件"。
