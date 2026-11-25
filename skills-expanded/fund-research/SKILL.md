---
name: fund-research
description: 依托东方财富数据库，生成单只公募基金的全面、体系化深度研究报告及 Markdown 数据底稿。当用户提及“基金研究”“基金深度分析”“基金研究报告”“帮我研究一下这只基金”“基金全面分析”或要求全面研究某只基金时使用。普通持有判断等轻量诊断应使用 fund-diagnosis；研究基金经理个人时使用 fund-manager-research。
version: 1.2.8
category: investment-finance
author: 东方财富
license: proprietary
agent_created: true
---

# 基金深度研究

将用户原始问句作为 `query` 调用基金研究接口，生成单只公募基金的深度报告。不要自行编造实体识别结果或报告内容。

## 使用边界

- 用于单只公募基金的全面研究、研究报告或体系化深度分析。
- 用户只做概括性诊断、持有判断或风险收益快速分析时，改用 `fund-diagnosis`。
- 研究基金经理个人时，改用 `fund-manager-research`。
- 用户没有提供可识别的基金名称或代码时，先请用户补充，不要调用接口。

## 授权与依赖

本 Skill 依赖 `EM_API_KEY`。授权检查已内联到 `scripts/get_data.py`，直接执行研究查询，不要先运行 `auth.py ensure`。凭据按 `EM_API_KEY` 环境变量、`~/.mx-skills/em_api_key` 文件的顺序读取，不使用内置兜底 key。

| 退出码 | 含义 | 处理方式 |
|---|---|---|
| `0` | 生成成功 | 读取正文、分享链接及附件路径 |
| `10` | 需要授权 | 展示 `authUrl` 二维码并停止本轮调用 |
| `2` | 网络或业务错误 | 返回失败原因，不编造报告 |
| `1` | 缺少 query/stdin | 补充基金名称或代码 |

授权、私有凭据持久化及 401 失效处理必须遵循 [授权协议](references/auth_protocol.md)。安装依赖时运行 `pip3 install -r requirements.txt`。

## 调用

```bash
python3 scripts/get_data.py --query "深度研究易方达蓝筹精选混合"
```

接口响应可能较慢。必须在当前会话同步等待命令结束，禁止后台执行或承诺稍后汇报。
脚本调用 SaaS 写作接口时会固定传入 `needFullContent=true`，以确保返回完整正文和溯源字段。

参数：

- `--query`：用户原始问句；也可由 stdin 传入。
- `--no-save`：只输出正文和分享信息，不保存附件。

代码调用：

```python
import asyncio
from scripts.get_data import generate_fund_research_report

result = asyncio.run(generate_fund_research_report("深度研究易方达蓝筹精选混合"))
```

## 返回字段

- `title`：报告标题。
- `article_id`：报告文章 ID。
- `share_url`：分享链接。
- `content`：报告正文。
- `attachments`：报告附件列表，每项包含 `type`（`PDF` 或 `DOCX`）和本地 `path`。
- `data_markdown`：接口 `data.dataMarkdown` 返回的数据底稿正文。
- `data_md_path`：保存后的 Markdown 数据底稿路径；接口未返回底稿或使用 `--no-save` 时为 `None`。
- `source_trace_path`：接口 `data.sourceTraceList` 原样保存后的 JSON 文件路径，固定保存到当前工作目录下 `miaoxiang/sourceTrace_<articleId>.json`；接口未返回 `articleId` 时使用随机 ID 兜底。
- 命令行成功输出使用统一字段标签 `source_trace_path: <path>`，不得改写为 `SourceTrace` 或省略该字段。
- `need_auth`、`authUrl`、`apiKeyUrl`：需要授权时返回。
- `remember_api_key`、`api_key`：刚完成授权时返回；凭据只能写入平台私有存储，不得展示给用户。
- `raw`：原始接口响应。
- `error`：失败原因。

## 用户可见输出

以接口返回内容为准，可对正文做简短提炼，但不得改变事实或编造缺失信息。报告附件与 Markdown 数据底稿仍按原流程保存，并以产物卡片正常交付；对话正文不列出附件信息。除非用户主动询问，否则不展示文件地址。

```text
## {title}

{content 或忠实提炼}

**研究报告分享链接：**
{share_url}
```

接口失败、正文为空或实体无法识别时，明确说明失败并请用户核对基金名称或代码；不得生成替代性报告。研究内容仅供参考，不构成投资建议。

## 执行超时要求（必须遵守）

本技能的脚本可能进入耗时较长的报告生成阶段。执行本技能下的任何脚本时，必须持续等待结果返回，并将工具层 `timeout` 设置为至少 `300000` 毫秒。
