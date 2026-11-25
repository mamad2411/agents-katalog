---
name: industry-sector-analysis
description: 面向A股行业与概念板块的专项分析能力。适用于用户明确要求分析某个行业、赛道、概念或板块的景气度、驱动因素、产业链、市场表现、风险与机会时，返回结构化 Markdown 报告。研究对象为单只股票时应使用 stock-diagnosis 或相应单维度诊股 skill；用户只想发现当前热门方向时应使用 stock-market-hotspot-discovery。
version: 1.2.8
category: investment-finance
author: 东方财富
license: proprietary
agent_created: true
---

# 行业板块分析

围绕行业或板块的景气度、政策与事件驱动、产业链、市场表现、风险和机会进行专项分析。

## 使用边界

- 仅在用户明确要求该专项维度时使用。
- 典型问法：`分析当前半导体板块的景气度和机会`。
- 不要用于单只股票诊断，也不要替代市场级热点发现。
- 必须提供行业、赛道、概念或板块名称；缺少分析对象时先请用户补充。


## 产物保存与展示

- 将用户当前工作区下的 `outputs` 目录作为命令工作目录；目录不存在时先创建。
- 使用 Skill 安装目录中脚本的绝对路径执行查询，不得将工作目录切换到 Skill 安装目录。
- 不得使用 `--no-save`。
- 生成的 Markdown 应保存到：
  `<工作区>/outputs/miaoxiang/industry_sector_analysis/`
- 执行后读取 `Saved:` 路径并确认文件存在。
- 最终回复说明分析文件已保存，不展示本地路径或路径链接。
- 如果当前环境提供 `open_in_codex`，调用它在对话文件面板中打开该 Markdown 文件。

## 多板块处理规则

- 支持分析多个行业、赛道、概念或板块。
- 包含两个对象时，必须分别生成独立分析。
- 禁止进行横向对比、优劣判断、排序、相对估值或给出“哪个更值得关注”的结论。
- 每个板块使用相同的报告结构，分析结论彼此独立。

## 授权与依赖

本 Skill 依赖 `EM_API_KEY`。授权检查已内联到 `scripts/get_data.py`，直接执行查询，不要先运行 `auth.py ensure`。凭据按环境变量、`~/.mx-skills/em_api_key` 的顺序读取，不使用内置兜底 key。

| 退出码 | 含义 | agent 动作 |
|---|---|---|
| `0` | 成功 | 读取 `Saved:`（若有）及随后输出的 Markdown 正文 |
| `10` | 需用户授权 | 按下方 `need_auth` 流程处理 |
| `2` | 授权网络错误、接口错误或业务错误 | 检查网络后最多重试 1 次，持续失败则向用户说明 |
| `1` | 参数错误 | 不重试，向用户说明缺少或无效参数 |


授权、凭据持久化及 401 失效处理必须遵循 [授权协议](references/auth_protocol.md)。安装依赖时运行 `pip3 install -r requirements.txt`。

## 调用

```bash
python3 scripts/get_data.py --query "分析当前半导体板块的景气度和机会"
```

参数：

- `--query`：用户原始自然语言问句；也可由 stdin 传入。
- 默认不使用 `--no-save`；生成的内容必须保存为本地 Markdown 文件。

接口返回后，对用户的可见回复必须以 `data.displayData` 对应的 Markdown 正文为主体，不要二次编造或改变结论。脚本返回 `error` 或正文为空时，只说明失败原因。

## 输出与合规

- 成功时输出正文，并返回本地 Markdown 文件的 `output_path`；也可返回 `raw`。
- 需要授权时返回 `need_auth`、`authUrl`、`apiKeyUrl`。
- 新授权取得 `api_key` 时，只能保存到平台私有跨会话存储，不得向用户展示或写入业务文件。
- 结果仅供参考，不构成投资建议；信息可能随市场变化而变化。
