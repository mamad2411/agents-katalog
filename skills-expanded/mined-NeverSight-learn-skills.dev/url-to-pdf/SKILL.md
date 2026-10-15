---
name: url-to-pdf
description: 将一个或多个网页 URL 转成高质量 PDF，并保存到 `~/Downloads/PDF` 的时间戳目录。用户只要提到“导出网页为 PDF”“保存文章/文档页面”“把知识库/公众号/极客时间页面转成 PDF”“顺手上传到 NotebookLM”等场景，就应主动使用这个 skill，而不是只给脚本路径或手工步骤。
---

# URL to PDF

## 概述
这个 skill 负责把真实浏览器渲染后的网页保存为 PDF，并在需要时继续上传到 NotebookLM。

它不只是简单调用 `page.pdf()`，还会处理这些开发中经常踩坑的场景：

- 先跑环境诊断，避免缺依赖后才失败
- 识别需要登录的网站，并在必要时切到可见浏览器完成 bootstrap 登录
- 复用 `~/.url-to-pdf/session.json`，减少重复登录
- 触发懒加载、展开自定义滚动容器、隐藏干扰 UI
- 批量处理多个 URL，并自动避免文件名冲突

## 何时使用
在这些场景里优先使用这个 skill：

- 用户给出一个或多个网页链接，希望导出 PDF
- 用户提到公众号、极客时间、知识库、内部站点、长文页面等“网页转 PDF”
- 用户想把网页内容沉淀到 NotebookLM
- 用户在调试网页导出空白页、登录页、懒加载缺失、首屏截断等问题

如果用户只是想“解释某个 PDF”或“总结已经上传的文件”，不要用这个 skill。

## 核心工作流
1. 从用户请求中提取 URL。
2. 如果 URL 被阅读模式或代理包裹，例如 `https://pure.md/https://...`，只使用原始目标 URL。
3. 先运行诊断：
   `python3 scripts/doctor.py --json`
4. 读取诊断结果并解释给用户：
   - `playwright` / `playwright_package` 决定能否生成 PDF
   - `interactive_terminal` 决定当前运行方式能否完成网页登录 bootstrap
   - `auth_valid` 和 `nlm_auth_valid` 只表示 `nlm` / NotebookLM 上传认证状态
   - `auth_valid: false` **不代表目标网站未登录**
5. 优先通过统一入口调用脚本，而不是直接调用底层脚本：
   `python3 scripts/run.py convert_to_pdf.py <url1> <url2> ...`
6. 生成成功后，告诉用户输出目录在 `~/Downloads/PDF/<timestamp>/`
7. 如果用户要上传 NotebookLM，再继续走上传流程

## 环境判断
优先以 `python3 scripts/doctor.py --json` 的结果为准。

- 如果 `playwright_package` 为 false 或 `playwright` 为 false：优先引导用户使用
  `python3 scripts/run.py ...`
  让统一入口自动完成 `.venv`、Playwright 包、Chromium 浏览器的初始化
- 如果 `uv` 为 false：提示用户安装 `uv`
- 如果 `nlm` 为 false：提示用户安装 `notebooklm-mcp-cli`
- 如果 `auth_valid` / `nlm_auth_valid` 为 false：只提示“NotebookLM 上传前需要 `nlm login`”
- 如果 `interactive_terminal` 为 false：提醒用户避免依赖终端输入确认；优先使用自动轮询登录完成，必要时单独运行 bootstrap 登录脚本

不要把 `doctor.py` 的认证状态误解释为网页站点登录态。

## 登录与会话
转换脚本会优先尝试复用：

`~/.url-to-pdf/session.json`

开发时要知道这些行为：

- 无本地 session 时，会触发首次 bootstrap 登录
- 已有 session 时，会先走更严格的“session 失效”判断
- 如果页面标题或正文强烈像登录页，也会强制进入登录流程
- 交互登录成功后，会更新 `~/.url-to-pdf/session.json`
- session 失效时，应自动重新 bootstrap，而不是继续导出登录页
- 登录后如果页面仍停留在登录页，脚本会终止，不应继续保存“登录.pdf”

推荐模型是：

- 第一次 bootstrap 登录
- 之后默认无头运行
- session 过期时再次 bootstrap

如果网站需要登录，优先用支持交互的方式运行脚本，让用户在弹出的浏览器里完成登录。
优先使用自动轮询的 bootstrap 登录流程，避免依赖 `input()` 或“按 Enter 继续”。
登录轮询不应因为页面瞬时变化就立刻判定成功；应等待最短驻留时间，并确认 cookies / session 相比初始状态确实发生变化。
如果需要单独初始化登录态，可以运行：
`python3 scripts/run.py bootstrap_login.py <url>`

## PDF 质量策略
这个 skill 的价值在于导出的 PDF 不只是“有文件”，而是尽量接近完整阅读页。执行时默认依赖脚本内置能力：

- 触发懒加载内容
- 识别并滚动自定义滚动容器
- 展平 `flex` / `overflow` 限制，避免只截首屏
- 隐藏侧边栏、导航栏等干扰 UI
- 使用更安全的 token 级 class 匹配，避免误伤正文

如果开发中出现“只有首屏”“空白 PDF”“明明是正文却被隐藏”，优先检查 `scripts/convert_to_pdf.py` 里的滚动、flatten、hide-ui 逻辑，而不是先怀疑 Playwright。

## 批量处理
可以一次传多个 URL 给 `scripts/convert_to_pdf.py`。
更推荐的调用方式是：
`python3 scripts/run.py convert_to_pdf.py <url1> <url2> ...`

注意：

- 同名标题会自动追加 `_1`、`_2` 避免覆盖
- 如果批量任务中途被用户打断，先检查输出目录里已经落盘了哪些 PDF
- 只补跑未完成的 URL，避免重复生成已经成功的文件

## NotebookLM 上传
只有在用户明确表示要上传时才继续。

标准流程：

1. 询问用户：`Do you want to upload these PDFs to NotebookLM? (Y/N)`
2. 如果用户选择 `Y`，先运行：
   `nlm notebook list`
3. 让用户选择 notebook ID，或输入 `N` 创建新 notebook
4. 上传：
   `python3 scripts/nlm_upload_cli.py <output_directory> <notebook_id>`

补充开发约定：

- 如果用户说 `N` 且提供了新名称，可以直接用 `nlm notebook create <title>` 先创建，再把 ID 传给上传脚本
- 如果 `nlm notebook list` 或上传报认证错误，提示用户先执行：
  `nlm login`

## 输出要求
完成一次转换后，至少告诉用户：

- 是否成功生成
- 输出目录
- 关键 PDF 文件名
- 如果你做了核查，可顺手报告文件大小，帮助判断是否是空白页

如果生成失败，也要明确说明失败阶段：

- 依赖未安装
- 需要网页登录
- 登录后仍停在登录页
- 上传失败但本地 PDF 已成功生成

## 常用命令
```bash
python3 scripts/run.py doctor.py --json
python3 scripts/run.py convert_to_pdf.py <url1> <url2> ...
python3 scripts/run.py bootstrap_login.py <url>
nlm notebook list
python3 scripts/nlm_upload_cli.py <output_directory> <notebook_id>
```

## 相关文件
- `scripts/doctor.py`
  环境诊断与 NotebookLM 上传认证检查
- `scripts/run.py`
  统一入口，自动创建 `.venv`、安装 Playwright 及浏览器，再执行目标脚本
- `scripts/convert_to_pdf.py`
  网页转 PDF 的核心逻辑
- `scripts/nlm_upload_cli.py`
  将生成目录里的 PDF 上传到 NotebookLM
- `README.md`
  更完整的设计背景和实现亮点

## 示例
用户：
`@/url-to-pdf https://mp.weixin.qq.com/s/... https://time.geekbang.org/column/article/...`

期望行为：
- 先诊断环境
- 批量导出 PDF 到 `~/Downloads/PDF/<timestamp>/`
- 若站点要求登录，则明确引导用户完成网页登录
- 完成后汇报输出目录，并询问是否上传到 NotebookLM
