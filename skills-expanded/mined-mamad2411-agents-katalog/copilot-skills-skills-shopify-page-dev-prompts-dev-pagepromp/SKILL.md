---
description: '从 Figma 设计稿开发 Shopify 新页面（模板JSON + SCSS + 构建）'
agent: 'agent'
argument-hint: '页面名称，如 h16-pro-steam'
tools: [search, editFiles, runTerminal, Figma/*]
---

# 开发新页面

按照 [Shopify Page Dev Skill](../copilot/skills/shopify-page-dev/SKILL.md) 的完整流程，从 Figma 设计稿开发一个 Shopify 新页面。

## 所需信息

请用户提供以下信息（未提供的用默认值）：

| 参数              | 说明                                    | 默认值         |
| ----------------- | --------------------------------------- | -------------- |
| 页面名称          | URL handle 和文件名                     | 从用户消息推断 |
| Figma PC 链接     | PC 设计稿 URL 或 file key + node ID     | 必填           |
| Figma Mobile 链接 | Mobile 设计稿 URL 或 file key + node ID | 必填           |
| PC 设计宽度       | 设计稿画板宽度                          | 2560px         |
| Mobile 设计宽度   | 设计稿画板宽度                          | 390px          |

## 执行流程

1. **获取 Figma 数据** — 用 MCP 工具读取 PC + Mobile 设计节点
2. **分析设计区域** — 识别每个 section 的设计模式
3. **匹配现有 Section** — 优先级：pattern-learnings → Part 1（通用组件）→ Part 2（索引）→ 新建
4. **生成模板** — `templates/page.{name}.json`
5. **编写 SCSS** — `src/styles/{name}.scss`，所有值用响应式函数
6. **注册构建** — 更新 `scss-kit.config.json`
7. **编译验证** — 运行构建命令并检查错误
8. **更新知识库** — 将新模式写入 pattern-learnings.md

## scss-kit 0.7.x 约定

- `r.resp(pc, mobile)` 默认使用 `readable`；密集的产品卡、价格、tag、badge 区域使用 `dense`。
- 不要把 `h1`、`h2`、`body` 等元素类型传给 `r.resp()`；第三、第四参数是 profile、数字最小系数或 Sass bounds map。
- 需要让整个嵌套组件使用同一 profile 时，在父选择器写 `@include r.mode(dense);`，子选择器可显式传入 profile 覆盖。
- 如果大屏版心固定，在 `scss-kit.config.json` 配置 `fixedCore`；不要手动为每个 `r.*` 调用增加大屏固定值。
- `autofill.entries` 可以先登记不存在的 SCSS 文件；启动 `npm run dev:theme:auto` 不会失败，文件创建后 watcher 会自动补齐入口 boilerplate。

参考文档：

- [Section 目录](../copilot/skills/shopify-page-dev/references/section-reference.md)
- [模式学习记录](../copilot/skills/shopify-page-dev/references/pattern-learnings.md)
- [项目指令](../copilot-instructions.md)
