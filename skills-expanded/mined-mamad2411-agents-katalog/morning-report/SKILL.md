---
name: morning-report
description: Use when generating or scheduling A-share-focused pre-market reports that summarize overnight markets, key signals, watch sectors, and risks before the trading day begins.
---

# morning-report

## 单一入口定位

`morning-report` 是 **标准化早盘报告** 的唯一 skill 入口。

- 直聊任务和 cron 都应调用这个 skill，而不是直接嵌入实现命令。
- 目标是让“盘前报告怎么做”只在这个 SOP 里定义一次。

## 适用场景

- 用户要求生成早盘报告 / 盘前摘要
- 交易日早晨的定时报告任务
- 需要快速建立“今天怎么看市场”的观察框架

## 输入参数

- `tradingDate`：交易日，格式 `YYYY-MM-DD`
- `mode`：`manual` / `scheduled`
- `dryRun`：是否只生成本地产物，默认 `false`
- `publish`：是否发布 HTML 并生成 URL，默认 `true`
- `sourceMode`：默认 `live`；必要时可切换为 `files`

## 固定 SOP

1. 确认目标交易日，并聚焦隔夜到盘前的有效信息。
2. 所有行情、消息、宏观变量必须使用真实数据；涉及新闻切片时，严格限定在上一个交易日结束到当前时间。
3. 在工作目录中使用 `exec` 运行统一 CLI，生成 report-data、Markdown、HTML 与发布结果。
4. 读取 stdout JSON，确认标题、结论、关注方向、风险提醒与发布 URL。
5. 检查输出是否真正回答“今天怎么看市场”，而不是堆叠新闻条目。
6. 若需要发送，只返回标题、结论、完整链接三行。

## 最终回复合同

- 第 1 行：报告标题
- 第 2 行：一句话结论
- 第 3 行：完整报告：`<url>`

若本次未发布 HTML，必须明确说明只生成本地文件，不能伪造可访问链接。

## 产物合同

- `data/morning/<tradingDate>.json`
- `reports/morning/<tradingDate>.md`
- `reports/morning/<tradingDate>.html`
- `reports/morning/<tradingDate>.publish-result.json`

## 降级规则

- 若隔夜或政策数据部分缺失：允许输出 `partial`，但必须明确标注“部分数据暂缺”
- 若 HTML 渲染失败：保底输出 Markdown
- 若上传失败：保留本地文件，不伪造 URL
- 若发送失败：显式返回失败信息

## 禁止事项

- 不输出交易动作或买卖建议
- 不伪造缺失数据
- 不把新闻堆砌成流水账
- 不在 cron 文案中复制内部执行命令

## 内部执行器

当需要实际生成报告时，在工作目录中运行统一 CLI：

```bash
cd /Users/zcg/.openclaw/workspace/agents/investment-advisor
node report-runtime/cli/run-report.mjs \
  --reportType morning \
  --tradingDate <YYYY-MM-DD> \
  --mode <manual|scheduled> \
  --dryRun <true|false> \
  --publish <true|false> \
  --sourceMode <live|files>
```

说明：

- 如需受控回放，可额外传入 `--briefFile <path>`。
- `publish=true` 时会调用共享 `report` skill，返回 DDM 平台报告地址。

## 验证清单

- 是否以结论先行而非新闻堆叠
- 是否明确外围影响、今日主线预判、风险提醒
- 若有缺口，是否诚实标注 `partial`
- 最终回复是否严格三行
