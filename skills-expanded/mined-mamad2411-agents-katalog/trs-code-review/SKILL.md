---
name: trs-code-review
description: 在用户要求 TRS 前端代码审查、提交前检查、MR/PR 检查、完成验收，或需要按团队 Vue、TypeScript、样式、接口、表单、Store、Git 规范检查改动时使用。
---

# TRS 前端代码审查

## 定位

这是收尾审查技能。通用流程使用 Superpowers；具体实现规范按需调用对应领域技能；本技能负责最终把改动按 TRS 团队标准过一遍。

## 触发场景

- 用户要求 review / code review / 代码审查 / 帮我看看问题。
- 提交前、MR/PR 前、合并前、发版前检查。
- 完成开发后需要验收是否符合团队规范。
- 需要把多个领域规范合并成一份审查结果。

## 审查顺序

1. 明确范围：查看本次 diff 或用户指定文件，不审查无关代码。
2. 先查正确性：功能逻辑、数据流、边界条件、错误处理。
3. 再查团队规范：Vue、TypeScript、样式、自动导入、API、表单、Pinia；需要细化判断时读取 `references/` 下对应规范。
4. 最后查交付质量：快速验证、浏览器运行时验证、build 是否按用户确认执行、提交粒度、MR 描述、风险说明。
5. 输出按严重程度排序，只列真实问题；没有问题就明确说未发现阻塞项。

## 参考文档

- Vue 审查：`references/vue.md`
- TypeScript 审查：`references/typescript.md`
- 样式审查：`references/style.md`
- 调试、性能和浏览器验证：`references/debugging-performance.md`
- Git 与提交约定：`references/git.md`

## 严重程度

- P0：会导致线上故障、数据错误、安全问题或核心流程不可用。
- P1：会导致主要功能异常、常见场景失败或明显维护风险。
- P2：规范偏差、边界缺失、可维护性问题，但不阻塞基本使用。
- P3：建议优化、命名、可读性或非阻塞体验问题。

## 核心检查项

### Vue / 组件

- 组件职责是否单一，是否出现页面、业务组件、通用组件职责混杂。
- Props / Emits 是否最小化、类型清晰，避免 Boolean 陷阱和隐式双向修改。
- `<script setup>` 代码块顺序是否清晰：类型、Props/Emits、状态、计算、监听、函数、生命周期。
- 模板中自研组件是否使用 PascalCase，普通 HTML 非 void 元素不自闭合。
- `v-for` 是否有稳定 key，避免同元素同时使用 `v-if` 和 `v-for`。

### TypeScript / 命名

- 类型、接口、组件名 PascalCase；变量/函数 camelCase；常量 UPPER_SNAKE_CASE。
- 避免无意义命名，例如 `data`、`list`、`item` 在复杂上下文中缺少业务含义。
- 避免 `any`、过宽类型、重复类型定义和不必要的类型断言。
- 接口响应、表单模型、组件 Props 是否有明确类型边界。

### 样式 / 自动导入

- 布局、间距、尺寸、颜色、排版、交互状态是否优先使用 UnoCSS。
- Less / scoped CSS 是否只处理 UnoCSS 不适合的场景，如 `:deep()`、伪元素、keyframes、CSS 变量。
- 是否滥用 `!important`、重复属性、过深选择器或不必要的样式穿透。
- 是否手动 import 了项目已自动注入的 Vue API、Router API 或自动注册组件。

### API / 表单 / Store

- API 调用是否按复用程度选择就近或接口层；避免裸请求散落、重复错误处理，以及与项目 axios 封装不一致。
- loading、error、empty、重试等状态是否覆盖核心交互路径。
- 表单规则是否集中定义，新增/编辑回显、提交、重置逻辑是否清晰。
- Pinia 是否只承载跨组件共享状态，避免把局部 UI 状态放进 store。
- 异步 action 是否有明确错误处理，避免吞错或重复请求状态不一致。

### Git / 交付

- diff 是否只包含本次任务相关改动。
- 需求、功能、新页面、交互、接口、表单、Store、组件拆分任务是否经过 `trs-development-preflight -> brainstorming -> writing-plans -> 执行 -> chrome-devtools-mcp -> review`；纯文档、纯类型、纯配置、纯脚本、纯 skill 文案且无业务运行时影响的任务可走轻量流程。
- writing-plans 是否声明 `Required TRS skills`，且实际执行没有跳过计划中声明的领域 skill 约束。
- 是否按 `superpowers:verification-before-completion` 完成必要的快速验证、浏览器运行时验证或手动验证说明。
- 不得把 `pnpm build` 作为默认 review 动作；只有用户明确确认后才执行或要求执行。
- 最终回复不得把 `pnpm build` 作为默认已执行项或默认下一步；未执行 build 时，只说明“未按约定执行 build”。
- 涉及页面、组件、样式、交互、接口联调或性能问题的改动，是否已按 plan 使用 `chrome-devtools-mcp` 完成浏览器运行时验证，并说明页面路径、核心操作、Console/Network/布局结果。
- 纯文档、纯类型、脚本配置、无 UI/运行时影响的改动，可不要求浏览器验证，但需要说明判断理由。
- 是否保留用户已有改动，没有还原无关文件；若工作区有无关改动，应明确本次只检查任务相关 diff。
- 开发完成后是否先询问用户是否提交本次修改；用户明确确认前，不得执行 `git add`、`git commit`、`git push` 或创建 PR。
- 提交信息是否符合 Conventional Commits。
- MR/PR 描述是否包含改动内容、影响范围、验证方式和风险点。

## 输出格式

如果发现问题：

```text
**Review 结果**
- P1 `path/to/file.vue:42`：问题描述。说明影响，并给出建议修复方向。
- P2 `path/to/file.ts:18`：问题描述。说明影响，并给出建议修复方向。
```

如果没有阻塞问题：

```text
**Review 结果**
- 未发现 P0/P1 阻塞问题。
- 已检查：Vue/TS/样式/API/表单/Store/交付项。
- 验证：列出实际执行过的命令和浏览器运行时验证；未执行则说明原因。
```

## 与 Superpowers 配合

- 标准流程中，本技能位于 `trs-development-preflight -> brainstorming -> writing-plans -> 执行 -> chrome-devtools-mcp -> review` 的最后一步，负责检查实际 diff 是否符合 TRS 前端规范。
- TRS 开发任务的分析、计划和验证流程由 Superpowers 负责；本技能只做 TRS 前端收尾审查。
- `writing-plans` 阶段应已按任务类型结合 `api-integration`、`form-validation`、`pinia-store-design`、`vue-component-design`、`css-patterns` 等领域技能；本技能负责收尾验收，不重新替代实施计划。
- 完成开发后，先按 `superpowers:verification-before-completion` 做验证，再用本技能做 TRS 规范审查；审查结束后必须询问用户是否提交本次修改，用户明确确认前不得提交、推送或创建 PR。
- 用户明确要求 code review 时，可配合 `superpowers:requesting-code-review`，但本技能负责 TRS 前端检查项。
