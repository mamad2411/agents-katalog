---
name: eliteforge-java-uml
description: 根据业务需求生成可落地的 Java 25 PlantUML 类图设计，统一分层建模、关系落点、分页查询、枚举字段化建模、类内说明和模块配色规则。用户提到“Java UML”“PlantUML 类图”“领域建模”“分层架构设计”“Repository 查询设计”“类图评审”时使用；优先输出 UML，禁止臆造与无落点关系。
---

# EliteForge Java UML

## 目标

- 生成可落地、结构清晰、边界明确、关系准确的 Java 25 UML 类设计。
- 优先保证正确性和可实现性，宁可少画，不可错画。

## 执行顺序（每次都做）

1. 识别业务中的聚合根、核心对象、规则对象、持久化对象、查询职责组件、操作职责组件。
2. 区分分层：`Controller`、`Service`、`Repository`、`Domain`、`Persistence`、`Enums`。
3. 识别闭集概念并优先建模为枚举（状态、类型、阶段、来源等）。
4. 为每个业务模块分配颜色，同模块统一同色系，不同模块区分色系。
5. 判断哪些对象需要审计字段，并补齐固定 6 个字段（见参考规则）。
6. 校验每条关系是否有落点：字段或方法签名（参数/返回值）。
7. 校验查询职责组件是否满足分页约束（`queryPage` 或 `queryByCursor`）。
8. 先输出 PlantUML 类图；信息不足时先输出可确定部分，再在图内注释不确定项。
9. 检查泛型写法：若出现 `Map~...~` / `List~...~` / `Optional~...~`，必须改写为 `&lt; &gt;`。
10. 按自检清单逐条检查后再给最终结果。

## 强制输出约束

- 仅输出 PlantUML 类图。
- 必须先输出 UML，再补充必要说明。
- 禁止为了“看起来完整”而臆造类、字段、方法、关系、枚举。
- 禁止绘制 `Dto` / `Vo` / `ResVo` 节点；它们只允许出现在方法签名中。
- 禁止绘制 `Page` / `PageResult` / `PageResponse` 等分页容器节点。
- 禁止无落点连线、禁止连线 label、禁止无必要噪音连线。
- 列表查询必须分页；禁止 `findAll` / `selectAll` / `queryAll` / `listAll` / `loadAll`。
- 所有节点（类/接口/枚举）必须写类内说明：`<<说明标题>>` + 至少 1 行说明。
- 枚举只展示实例（常量），不展示成员变量和内部方法。
- 泛型禁止使用 `~` 形式；必须输出为 `&lt;` `&gt;`，若检测到 `~` 泛型必须先重写再渲染。
- 颜色必须按模块划分；禁止只按技术层固定上色而忽略模块边界。
- 技能运行时必须先检测 `PLANTUML_ASL_JAR` 环境变量；未设置则直接结束，并提醒用户先配置。
- 只要新增或修改了 UML 内容，必须使用 `PLANTUML_ASL_JAR` 重新渲染成功，否则不输出最终结果。
- 最终产物必须同时输出 `*.puml` 与 `*.svg`，且 `*.svg` 与 `*.puml` 同级。

## 参考文件读取策略

- 处理普通 UML 设计请求时，先读 [references/uml-core-rules.md](references/uml-core-rules.md)。
- 用户强调布局、颜色、可读性、类内说明时，再读 [references/plantuml-template.md](references/plantuml-template.md)。
- 用户要求“给我一个可直接改的模板/示例”时，读 [references/plantuml-example-template.md](references/plantuml-example-template.md)。
- 用户担心渲染失败或版本兼容时，读 [references/plantuml-validation.md](references/plantuml-validation.md)。

## 输出风格基线

- 默认使用 `top to bottom direction` + `skinparam linetype ortho`。
- 先按模块上色，再在模块内组织分层节点；除非用户明确要求，避免使用外部 `note`。
- 枚举默认不连线，减少噪音。

## 输出模板

```plantuml
@startuml
top to bottom direction
skinparam linetype ortho

' 先放分层包，再放类定义与关系
' 信息不足时，用注释列出不确定项，仍保持 PlantUML 输出

@enduml
```

## 参考资料

- [通用 UML 规则与自检](references/uml-core-rules.md)
- [PlantUML 输出模板](references/plantuml-template.md)
- [PlantUML 示例模板](references/plantuml-example-template.md)
- [PlantUML 版本与校验](references/plantuml-validation.md)
