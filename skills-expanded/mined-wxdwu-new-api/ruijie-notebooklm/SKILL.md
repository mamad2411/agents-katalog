---
name: 锐捷-读书助手
description: v2026.05.07.2；使用 NotebookLM 快速阅读 PDF 书籍。适用于“读书助手”“快速读书”“上传 PDF 书籍”“书籍总结”“书籍简述”“生成书籍思维导图/概念关系图/时间线”等请求；自动弹出 PDF 选择框、创建单书 NotebookLM 笔记本、上传 PDF 内容、生成中文 Markdown 阅读产出或 Mermaid 图表。
---

# 锐捷-读书助手

这是锐智内置“锐捷插件”提供的 skill。它面向小白用户，不要求用户理解 NotebookLM、notebookId、sourceId、token 或 SDK 方法。底层通过现有后端的 NotebookLM 桥接服务和书籍 PDF 处理接口调用 NotebookLM。

脚本内硬编码 token `st-ruijie`，不要向用户索要 token、cookies、账号或 2FA。

## 核心工作流

用户调用本 skill 时：

1. 先定位当前 skill 目录下的 `scripts/book-reader.mjs`。
2. 运行 `node <skill目录>/scripts/book-reader.mjs pick-upload`。
3. 脚本弹出系统文件选择框，限制用户选择一个 PDF。
4. 用户取消选择时，脚本返回 `{"status":"cancelled"}`，流程结束。
5. 用户选择 PDF 后，脚本创建一个新的 NotebookLM 笔记本，把 PDF 发给后端提取文字层，并将书籍内容作为 NotebookLM 来源提交。
6. 上传完成后，脚本在 stdout 输出 JSON，包含 `notebookId`、`sourceId`、`sourceIds`、`pdfName`、`notebookTitle`。
7. Codex 在当前对话上下文记住本轮返回的 notebook 信息。
8. 上传完成后，调用 `functions.request_user_input` 询问用户下一步：
   - 快速读书
   - 书籍总结
   - 生成图表
9. 如果用户选择“生成图表”，继续调用 `functions.request_user_input` 询问图表类型：
   - 思维导图
   - 概念关系图
   - 时间线
10. 调用 `node <skill目录>/scripts/book-reader.mjs generate --notebook-id <notebookId> --kind <quick|summary|diagram> [--diagram-type <mindmap|flowchart|timeline>]`。
11. 将脚本 stdout 中的 Markdown 先完整回复给用户。Mermaid 图表也直接以 Markdown 代码块回复，不下载、不打开文件。
12. 确认生成结果已经在聊天中可见后，再继续询问是否还要“快速读书 / 书籍总结 / 生成图表”，直到用户自然结束。

同一 Codex 会话里，用户多次调用本 skill 时，每次都运行 `pick-upload` 并为新的 PDF 创建新的 NotebookLM 笔记本。每个笔记本只放一本书的 PDF。不要把多本书塞进同一个 NotebookLM 笔记本。

## 交互规则

- 锐智默认启用 Codex feature `default_mode_request_user_input`，使 Default 模式也能使用 `functions.request_user_input`。
- 工具名就是 `functions.request_user_input`，不要写成 `ask`、`question` 或纯文本菜单。
- 不要在未尝试调用 `functions.request_user_input` 前声称交互选择器不可用。
- 如果用户在调用 skill 的同一句话里已经明确要求“快速读书 / 书籍总结 / 生成图表”，上传完成后直接执行对应生成动作，不再追问。
- 用户只调用 skill 且未指定动作时，必须先调用阅读动作选择器。
- 阅读动作选择器参数固定为：

```json
{
  "questions": [
    {
      "id": "reading_action",
      "header": "读书",
      "question": "《<pdfName>》已上传。接下来要做什么？",
      "options": [
        {
          "label": "快速读书 (Recommended)",
          "description": "快速抓住主旨、结构、关键案例和适读人群。"
        },
        {
          "label": "书籍总结",
          "description": "输出更完整的结构化中文 Markdown 总结。"
        },
        {
          "label": "生成图表",
          "description": "继续选择图表类型，并输出 Mermaid 代码块。"
        }
      ]
    }
  ]
}
```

- 阅读动作返回值映射：`快速读书` 或 `快速读书 (Recommended)` -> `--kind quick`；`书籍总结` -> `--kind summary`；`生成图表` -> 继续询问图表类型。
- 图表类型选择器参数固定为：

```json
{
  "questions": [
    {
      "id": "diagram_type",
      "header": "图表",
      "question": "要生成哪类书籍图表？",
      "options": [
        {
          "label": "思维导图 (Recommended)",
          "description": "适合展示书籍结构、核心概念和论证脉络。"
        },
        {
          "label": "概念关系图",
          "description": "适合展示概念关系、因果链和方法框架。"
        },
        {
          "label": "时间线",
          "description": "适合历史、传记、演化类书籍。"
        }
      ]
    }
  ]
}
```

- 图表类型返回值映射：`思维导图` 或 `思维导图 (Recommended)` -> `--diagram-type mindmap`；`概念关系图` -> `--diagram-type flowchart`；`时间线` -> `--diagram-type timeline`。
- 每次生成结束后，必须先把 stdout 中的 Markdown 发送给用户，再调用阅读动作选择器继续服务同一本书。
- 不要在生成结果尚未显示给用户时先弹下一轮选择器；这会让用户以为内容丢了。
- 如果需要在同一轮继续弹选择器，先用 `commentary` 发送生成结果，再调用 `functions.request_user_input`。
- 只有 `functions.request_user_input` 实际调用失败时才 fallback，不要提前假设不可用。
- fallback 时不要把工具不可用、Default 模式、Plan 模式等内部细节告诉用户。
- fallback 时用一句自然中文直接追问，例如：`已上传《<书名>》。接下来要快速读书、书籍总结，还是生成图表？`
- 不要因为 `functions.request_user_input` 不可用就自动默认生成“快速读书”。用户只调用 skill 且未指定动作时，必须先追问。
- 不要向用户展示 notebookId、sourceId、工具报错栈或内部执行判断，除非需要排障或用户明确索要。

## 脚本命令

查看帮助：

```powershell
node <skill目录>\scripts\book-reader.mjs --help
```

上传一本 PDF：

```powershell
node <skill目录>\scripts\book-reader.mjs pick-upload
```

生成快速读书：

```powershell
node <skill目录>\scripts\book-reader.mjs generate --notebook-id "<笔记本ID>" --kind quick
```

生成书籍总结：

```powershell
node <skill目录>\scripts\book-reader.mjs generate --notebook-id "<笔记本ID>" --kind summary
```

生成图表：

```powershell
node <skill目录>\scripts\book-reader.mjs generate --notebook-id "<笔记本ID>" --kind diagram --diagram-type mindmap
node <skill目录>\scripts\book-reader.mjs generate --notebook-id "<笔记本ID>" --kind diagram --diagram-type flowchart
node <skill目录>\scripts\book-reader.mjs generate --notebook-id "<笔记本ID>" --kind diagram --diagram-type timeline
```

调试时可绕过文件选择框：

```powershell
node <skill目录>\scripts\book-reader.mjs pick-upload --file ".\book.pdf"
```

## 脚本行为约定

- Windows 使用 PowerShell `System.Windows.Forms.OpenFileDialog` 弹出 PDF 文件选择框。
- macOS 使用 `osascript choose file` 弹出 PDF 文件选择框。
- 不安装 npm 依赖，不启动浏览器，不打开文件。
- 文件选择只允许单个 PDF；脚本用 `%PDF-` 文件头校验真实 PDF，不只靠扩展名判断。
- Notebook 标题格式为 `读书助手-<PDF文件名>-<短UUID>`。
- 后端一旦返回认证失败、配额不足、上传失败、来源失败或生成失败，脚本必须直接抛出错误。
- 最终机器可读 JSON 或 Markdown 只写 stdout；错误信息只写 stderr。

## PDF 与内容边界

上传本地 PDF 时，Agent 不要读取、解析或理解文件内容。脚本只读取文件头做 PDF 格式检查，并把二进制字节提交给后端书籍 PDF 接口；后端负责提取 PDF 文字层并将书籍内容作为 NotebookLM 来源提交。不要在 Codex 本地做 PDF 抽文本、OCR、截图识别、摘要或内容预览。PDF 判断以 `%PDF-` 文件头为准，不要只靠扩展名拦截。

生成结果必须来自 NotebookLM 对该笔记本来源的回答。NotebookLM 认证失效、Google 风控、配额不足或 SDK 报错时，直接报告错误；不要编造阅读结果。

## 输出规格

快速读书：

- 300 字左右
- 覆盖书名作者、核心主旨、内容结构、关键案例、适读人群
- 不补充来源外信息

书籍总结：

- 中文结构化 Markdown
- 覆盖章节推进、关键概念、论证链路、边界和实践启发
- 不推荐外部书单，不写来源外背景

图表：

- 直接输出 Markdown Mermaid 代码块
- `mindmap` 用于书籍结构、核心概念、论证脉络
- `flowchart TD` 用于概念关系、因果链、方法框架
- `timeline` 用于历史、传记、演化类书籍
- 不默认提供时序图、类图、甘特图

## 服务地址

默认通过现有部署入口 `http://107.175.202.99:5173` 调用 `/api/notebooklm-bridge`。如需切换环境，设置：

```powershell
$env:NOTEBOOKLM_BACKEND_BASE_URL = "http://127.0.0.1:3450"
```

不要直连公网 `3450`，当前公网 3450 会返回 503。

## Node.js 前置检查

调用脚本前先检查 Node.js：

```powershell
node --version
```

如果系统没有 Node.js，Agent 负责安装 Node.js LTS 后重试。优先使用系统已有包管理器。

## 高级排障

底层原生桥接 CLI 仍保留在 `scripts/notebooklm.mjs`。普通读书流程不要暴露这些命令给用户；只有排查后端桥接能力时再使用：

```powershell
node <skill目录>\scripts\notebooklm.mjs capabilities
node <skill目录>\scripts\notebooklm.mjs methods
```
