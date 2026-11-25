---
name: topic-research-report
description: 面向专题研究报告生成的能力。适用于用户提出“某主题/事件/政策的深度研究报告”类请求时，自动生成结构化研究内容。覆盖主题投资、政策影响、事件冲击、趋势判断等跨行业议题。触发核心条件：用户目标是“专题研究/深度解读/报告输出”，而非单行业常规研究或单标的诊断。
version: 1.2.7
category: investment-finance
author: 东方财富
license: proprietary
agent_created: true
---

# 专题研究报告

通过**自然语言 query**生成专题研究报告，返回 Markdown 正文及分享信息，适用场景包括：
- **事件驱动研究（政策、国际事件、宏观变化）**
- **主题投资研究（赛道、技术趋势、概念演化）**
- **跨行业影响分析（单一行业难覆盖的问题）**
- **快速输出可分享的专题深度内容**


## 功能范围

### 基础生成能力
- 输入专题 query，调用专题研究接口生成完整报告
- SaaS 写作请求固定传入 `needFullContent=true`，确保返回完整正文和溯源字段
- 返回报告标题、正文、文章ID、分享链接及附件路径等结构化字段
- 若返回 `wordBase64/pdfBase64`，自动解码保存为本地 `.docx/.pdf` 附件

### 触发规则（何时使用本技能）
- 用户明确要求“专题研究/深度分析/研究报告”
- 研究对象为主题、事件、政策、趋势、跨行业议题
- 典型问法：`东方财富专题研究`、`美联储加息对A股影响`、`AI Agent产业链专题`

### 不触发规则（何时不要使用本技能）
- 用户只问单行业基础研究（应走行业研究技能）
- 用户只问单只股票/基金买卖判断（应走诊断技能）
- 用户要求指标级计算、回测、量化建模（应走量化类能力）

### 触发示例

| 触发（专题研究） | 不触发（其他能力） |
|---|---|
| 东方财富专题研究 | 半导体行业最新景气度（行业研究） |
| 美联储加息对A股影响 | 海康威视值得买吗（个股诊断） |
| 一带一路主题投资机会 | 永赢先锋半导体风险大吗（基金诊断） |
| ChatGPT对教育行业冲击 | 丹化科技MACD是否金叉（指标计算） |


## 授权与依赖

本 Skill 依赖 `EM_API_KEY`。授权检查已内联到 `scripts/get_data.py`，**直接执行专题研究查询，不要先单独运行 `auth.py ensure`**，也不要把授权作为另一轮前置工具调用。凭据按 `EM_API_KEY` 环境变量、`~/.mx-skills/em_api_key` 文件的顺序读取，不使用内置兜底 key。

### 退出码与授权输出

| 退出码 | 含义 | 处理方式 |
|---|---|---|
| `0` | 查询成功 | 读取标题、正文、分享链接及附件路径 |
| `10` | 需要用户授权 | 展示二维码并停止本轮调用 |
| `2` | 网络或业务错误 | 返回明确失败原因，不编造研究报告 |
| `1` | 缺少 query/stdin | 补充有效问句后再调用 |

需要授权时，stdout 输出带标签文本：

```text
need_auth: true
authUrl: https://...
apiKeyUrl: https://...
```

授权、凭据持久化及 401 失效处理必须遵循 [授权协议](references/auth_protocol.md)。安装依赖时运行 `pip3 install -r requirements.txt`。


## 快速开始

### 1. 命令行调用

```bash
python3 scripts/get_data.py --query "东方财富专题研究"
```

**输出示例**
```text
Title: 东方财富日报专题研究报告
ShareUrl: http://aife-test.eastmoney.com:9001/researchShare?shareId=xxx&scene=research
DOCX: /path/to/workspace/topic_research_report/5f14e352-cd8e-4169-9d69-7399f1eb8328_docx.docx
PDF: /path/to/workspace/topic_research_report/5f14e352-cd8e-4169-9d69-7399f1eb8328_pdf.pdf
（随后输出 Markdown 正文内容）
```

**参数说明：**

| 参数 | 说明 | 必填 |
|---|---|---|
| `--query` | 用户原始专题研究问句 | ✅（`--query` 或 stdin 二选一） |
| `--no-save` | 仅输出结果，不保存 `.docx/.pdf` 附件 | 否 |

注意：禁止调用 任何「后台执行、稍后汇报」的方式跑本脚本，只能在当前会话中同步等待到命令完成，拿到 stdout 的结果后再继续，否则会导致本 Skill 失败。


### 2. 代码调用

```python
import asyncio
from pathlib import Path
from scripts.get_data import generate_topic_research_report

async def main():
    result = await generate_topic_research_report(
        query="东方财富专题研究",
        output_dir=Path("workspace/topic_research_report"),
        save_to_file=True,
    )
    if result.get("need_auth"):
        print(result["authUrl"])
    elif "error" in result:
        print(result["error"])
    else:
        print(result["title"])
        print(result["share_url"])
        print(result["content"])
        if result.get("output_path"):
            print("已保存至:", result["output_path"])

asyncio.run(main())
```

## 输出文件说明

| 文件 | 说明 |
|---|---|
| `<articleId>_docx.docx` | 由 `wordBase64` 解码得到的 Word 附件（若返回） |
| `<articleId>_pdf.pdf` | 由 `pdfBase64` 解码得到的 PDF 附件（若返回） |
| `../sourceTrace_<articleId>.json` | `data.sourceTraceList` 原样保存的溯源 JSON，实际固定保存在当前工作目录的 `miaoxiang` 目录 |

## 返回字段说明

- `title`：报告标题（来源于 `data.title`）。
- `article_id`：报告 ID（来源于 `data.articleId`）。
- `share_url`：报告分享链接（来源于 `data.shareUrl`）。
- `content`：报告正文（优先 `data.content`）。
- `attachments`：附件列表（解析 `wordBase64/pdfBase64` 后的本地路径）。
- `source_trace_path`：`data.sourceTraceList` 原样保存后的 JSON 路径，固定为当前工作目录下 `miaoxiang/sourceTrace_<articleId>.json`；无 `articleId` 时使用 UUID 兜底。
- 命令行成功输出使用统一字段标签 `source_trace_path: <path>`，与其他研究类 skill 保持一致。
- `raw`：原始接口返回，便于调试或二次处理。
- `need_auth`、`authUrl`、`apiKeyUrl`：需要用户授权时返回。
- `remember_api_key`、`api_key`：刚完成授权时返回；`api_key` 只能写入平台私有凭据存储，不得展示给用户。
- `error`：接口调用失败时返回错误信息。

## 输出格式规范

接口返回后，必须严格按以下模板输出：

#### 输出格式

```
## {title}

**正文：**

已经生成专题研究报告。此处仅展示部分正文内容，请下载附件查看报告详情和参考信息。

{content}

**分享链接：**
{share_url}

```
字段映射规则：
- `{title}` = 脚本返回的 `title`
- `{content}` = 脚本返回的 `content`
- `{pdf_file_path}` = 脚本返回的 `attachments` 中 `type` 为 `PDF` 的 `path`
- `{word_file_path}` = 脚本返回的 `attachments` 中 `type` 为 `DOCX` 的 `path`
- `{share_url}` = 脚本返回的 `share_url`
- `{source_trace_path}` = 脚本返回的 `source_trace_path`

## 常见问题
**如何只看输出，不落盘？**
```bash
python3 -m scripts.get_data --query "东方财富专题研究" --no-save
```
**注意：专题研究报告接口响应时间较久，请耐心等待~**  
→ 在当前会话中同步等待到命令完成，拿到 stdout 的结果后再继续输出，否则会导致本 Skill 失败。

**异常场景**

| 异常场景                  | 处理方式                                      |
|--------------------------|----------------------------------------------|
| 接口调用超时              | 原样返回："报告生成服务暂时不可用，请稍后重试。" |
| 接口返回空数据            | 返回兜底话术："内容涉及敏感信息，请尝试其它主题。" |
| 接口返回格式异常          | 原样返回："内容无法解析" |

## 合规说明

- 研究内容仅供参考，不构成投资建议，输出时应附风险提示。
- 禁止在代码或提示词中硬编码账号 ID、会话 ID 或 token。
- 接口失败时不得编造结论，应返回明确错误或不确定性说明。

## 执行超时要求（必须遵守）

本技能的脚本可能进入耗时较长的报告生成阶段。执行本技能下的任何脚本时，必须持续等待结果返回，并将工具层 `timeout` 设置为至少 `300000` 毫秒。
