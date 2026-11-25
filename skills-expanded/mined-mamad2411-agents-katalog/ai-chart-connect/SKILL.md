---
name: ai-chart-connect
description: "Connect to a local AI chart workbench (http://localhost:3001) to CREATE chart templates, APPLY real data to render charts, EXPORT images, and BUILD illustrated analysis reports / periodic digests — all over HTTP. Use when the user wants to '做一个图表/仪表盘/可视化/柱状图/折线图/饼图/桑基图', '生成图表模板', 'replicate a chart', '把数据画成图/用数据出图/生成分析图', '批量出图', '导出图表/SVG/PNG', '生成分析报告/经营报告/数据报告', '做周报/月报/定期报告'. You generate template files yourself and write them through the API; you do NOT call the workbench's built-in AI."
version: 1.5.1
---

# 连接 AI 图表工作台

你（外部 Agent，如 Codex）通过 HTTP 操作一个本地图表服务来创建图表模板、
用真实数据渲染图表、导出图片。**你自己生成内容并通过 API 写入并自检**——
不调用工作台内置的 AI。这样既发挥你更强的模型能力，
也允许没有配置内置 AI 的用户使用。

> 这份 skill 独立于工作台的内置 skill 系统，内置 AI 不会加载它。

## 服务地址

默认 `http://localhost:3001`（下文 `$BASE`）。请求全部失败时先探活：

```
GET $BASE/api/health   →  { "ok": true, ... }
```

探活失败 → 服务没启动，告诉用户先 `npm run dev`。

## 你能做的五件事（按需读对应文档）

| 你要做 | 读哪个文档 | 一句话 |
|--------|-----------|--------|
| **创建图表模板**（从零生成一个新图表） | [`references/create-template.md`](./references/create-template.md) | 生成 5 个契约文件，PUT 写入，renderer 带 validate 自检，失败就修到通过 |
| **改已有模板**（换色/加标题/显示标签/改交互） | [`references/refine-template.md`](./references/refine-template.md) | 先读现状，按决策表改对文件，确保改动在预览里可见（头号坑：改了 config 但 renderer 没读） |
| **应用数据出图**（拿真实数据套模板出图） | [`references/apply-data.md`](./references/apply-data.md) | POST /export 带 `data` 字段，SVG/PNG 反映你的数据，模板文件不被动 |
| **生成分析报告 / 定期周报**（多张图+文字拼报告） | [`references/build-report.md`](./references/build-report.md) | 批量套数据出图 + 你的分析文字，组装 Markdown/HTML 报告；配方+cron 实现定期 |
| **`@ai-chart/layout` 壳 API 速查**（写 renderer 必读） | [`references/layout-shell.md`](./references/layout-shell.md) | ChartCanvas/Title/Legend/ChartArea 全 props、cartesian/polar/free 的 scales、组合原语、toSvgPoint |
| **导出图片 / API 速查**（端点参考） | [`references/api-reference.md`](./references/api-reference.md) | POST /export + GET /export-file，全部端点速查 |

**动手前先读对应文档。** 每份文档都有精确的字段契约、curl 示例、失败处理——
里面的每个示例都是真实跑通验证过的。

## 三件事共用的工作原则

无论做哪件，都遵循：

1. **绝不直接读写文件系统**——一切走 HTTP API。
2. **每个写操作都自检**——PUT 文件带 `validate:true`，写完确认渲染成功；
   失败读 `error.stage` + `error.message`，修复重写，直到成功。
3. **覆盖数据不持久化**——export 的 `data`/`configOverrides` 只影响本次渲染，
   workspace 的 sample-data.json / config.values.json 永远不被修改。
   这是"应用数据出图"的关键语义。

## 最快起步

如果你想马上开始（先读 create-template.md 再动手）：

1. `GET $BASE/api/health` 探活
2. `POST $BASE/api/workspaces` `{ name, chartType }` → 拿到 `workspaceId`
3. 依次 PUT 5 个文件：`manifest.json` → `config.schema.json` →
   `sample-data.json` → `config.values.json` → `renderer.tsx`
4. PUT `renderer.tsx` 时带 `"validate": true`；失败就修，重写，直到 `200`
   （renderer **必须用 `@ai-chart/layout` 的 `<ChartCanvas>` 壳**，见
   [`create-template.md`](./references/create-template.md) 硬规则⓪/E3）
5. 导出：`POST $BASE/api/workspaces/:id/export` `{ format: "png" }`
6. 或告诉用户打开 `http://localhost:5173` 在画廊里看

详细字段、枚举、渲染规则、最常踩的坑（rendererConfigCheck），
全部在 [`references/create-template.md`](./references/create-template.md)。

## API 速查（完整版见 api-reference.md）

| 操作 | 方法 | 路径 |
|------|------|------|
| 探活 | GET | `/api/health` |
| 列出/创建模板 | GET/POST | `/api/workspaces` |
| 读/写文件 | GET/PUT | `/api/workspaces/:id/file` |
| 预览/校验 | POST | `/api/workspaces/:id/preview` |
| 导出（可带 data/configOverrides） | POST | `/api/workspaces/:id/export` |
| 下载导出文件 | GET | `/api/workspaces/:id/export-file?path=` |

## CLI（不想手写 HTTP 时）

`cli/chart-tool.mjs` 是 API 的薄封装。`npm run chart-tool -- help` 看全部命令。
关键命令：

```
chart-tool new "名称" --type bar                     # 建空壳
chart-tool put <id> renderer.tsx file.tsx --validate # 写文件并校验
chart-tool pull <id> [dir]                           # 拉模板 5 个文件到本地（改模板第一步）
chart-tool push <id> [dir]                           # 改完推回去，逐个 --validate
chart-tool export <id> --format png --data data.json # 套数据出图
chart-tool validate <id>                              # 整体验证
chart-tool geocatalog                                  # 列内置地理数据集（地图图表）
chart-tool geoimport <id> <name>                       # 把地理边界导入 workspace
```
