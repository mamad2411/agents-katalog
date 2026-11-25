---
name: dev-antd
description: antd 6.x、Ant Design Pro 5/ProComponents、Ant Design X v2 以及离线 `@ant-design/cli` 的决策指南。用于组件选型、主题/token、SSR、a11y、性能、路由/权限/CRUD、AI/聊天 UI 模式、本地 API 查询、调试、迁移与使用情况分析。
---

# Ant Design

## S - 范围
- 目标:`antd@^6` + React 18-19,需要时配合 `ant-design-pro@^5` / `@ant-design/pro-components` 和 `@ant-design/x@^2`。
- 工具:`@ant-design/cli`,用于离线获取组件元数据、demo、changelog、迁移、lint、doctor 检查和使用情况分析。
- 重点:仅提供决策指导;不面向最终用户的教程。
- 来源策略:仅使用官方文档;不使用未文档化的 API 或耦合内部 `.ant-*`。

### 默认假设
- 语言:TypeScript。
- 样式:token 优先,然后是 `classNames`/`styles`;避免全局覆盖。
- Provider:除非需要严格隔离,否则只用一个根 `ConfigProvider`。

### 强制规则
- 在编写或修改 antd 组件代码之前,先用 `antd info <Component> --format json` 查询组件 API。CLI 能离线回答时不要凭记忆。
- `antd` CLI 命令一律使用 `--format json`。
- 如果项目版本重要,用 `--version <x.y.z>` 匹配,或让 CLI 从本地 `node_modules` 自动检测。
- 修改 antd 代码后,运行 `antd lint <changed-path> --format json`。
- 如果某个 `antd` CLI 命令崩溃、返回错误数据或违反其文档行为,准备一个 `antd bug-cli` 预览供用户确认,而不是默默地绕过它。
- 对于组件问题,先将组件名映射到官方路由 slug `{components}`(小写 kebab-case,如 `TreeSelect -> tree-select`、`Button -> button`),然后按以下顺序请求文档(中文优先,英文兜底):
  1. `https://ant.design/components/{components}-cn`
  2. `https://ant.design/components/{components}`
  - 示例:`tree-select-cn -> tree-select`、`button-cn -> button`。
- 只使用已文档化的 antd/Pro/X API。
- 不要编造 props/事件/组件名。
- 不要依赖内部 DOM 或 `.ant-*` 选择器。
- 主题优先级:全局 token -> 组件 token -> alias token。

## P - 流程
### 1) 分类
- 识别层级:核心 antd、Pro 还是 X。
- 确认版本、渲染模式(CSR/SSR/流式)、数据规模,以及是否应将 `@ant-design/cli` 作为主要查询途径。

### 2) 查询权威来源
- 优先使用本地 `@ant-design/cli` 进行结构化查询:
  - `antd info` 查询 props/API
  - `antd demo` 获取可用基线
  - `antd doc` 获取完整文档
  - `antd token` / `antd semantic` 获取主题与样式钩子
  - 调试或升级时使用 `antd doctor`、`antd lint`、`antd usage`、`antd migrate`、`antd changelog`
- 当需要叙述性文档或交叉核对时,再请求官方组件文档(优先 `-cn`,英文兜底)。

### 3) 决策
- Provider 基线:CSR -> `ConfigProvider`;SSR -> `ConfigProvider` + `StyleProvider`。
- 主题基线:全局 token -> 组件 token -> `classNames`/`styles`。
- 输出建议 + 风险 + 验证点(SSR/a11y/性能),使用了 CLI 时引用其查询结果。

## O - 输出
- 提供简短的决策理由(1-3 句)。
- 包含最小化的 provider/主题策略。
- 包含具体的 SSR/a11y/性能检查项。
- 对于 Pro:包含路由/菜单/权限与 CRUD schema 方向。
- 对于 X:包含消息/工具 schema 与流式状态方向。

## 参考资料

| 文件 | 何时使用 |
| --- | --- |
| `references/antd-cli.md` | 需要离线 CLI 的确切工作流时:API 查询、demo、lint、doctor 检查、迁移、changelog 查阅、使用情况分析或 bug 上报。 |

## 回归检查清单
- [ ] 只有一个根 `ConfigProvider`;SSR 样式顺序/hydration 已验证。
- [ ] token 优先;没有大范围的 `.ant-*` 全局覆盖。
- [ ] Table 有稳定的 `rowKey`;排序/筛选/分页入口统一。
- [ ] Select 远程搜索模式下禁用本地筛选。
- [ ] Upload 的受控/非受控模式明确,且有失败/重试路径。
- [ ] Pro 的路由/菜单/权限与后端强制校验保持一致。
- [ ] X 的流式支持停止/重试和确定性的工具渲染。
- [ ] 如果使用了 `antd` CLI,命令均带 `--format json` 运行,且任何 CLI 缺陷都通过 `antd bug-cli` 预览进行了上报。
