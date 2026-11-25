---
name: reference-fulltext-acquisition
description: "Use when the task is to obtain and verify full-text PDFs for a reference list or literature corpus: OA lookup, Google Scholar right-side PDF/all-versions clicking, CNKI authorized download, user-provided PDFs, acquired/missing lists, and Zotero attachment planning. Not for final writing citation capture."
---

# Reference Fulltext Acquisition

把这个 skill 作为“获取文献全文 PDF”的统一入口。`cnki-research`、`google-scholar-research`、`openalex-landscape`、`semantic-citation-tracer` 和 `zotero-sync` 都只是它按需调用的传感器或执行器，不直接替代全文获取流程。

CNKI 和 Google Scholar 的浏览器模式以 `skills/catalog/scholar_browser_patterns.json` 为准。外部仓的技能不整包安装；只吸收经过本地冒烟和安全审查的选择器、检索参数、断点恢复和停止规则。

## Hard Rules

1. 先核验文献，再标记全文已取得；不要伪造 DOI、标题、作者或来源。
2. Google Scholar 只做 PDF 候选发现，不做正式元数据来源。
3. 英文或国际文献必须先用 OpenAlex / Crossref / Unpaywall / Semantic Scholar / 出版社开放端点做批量开放源尝试；批量阶段没有取得可校验 PDF 的条目，自动进入 Google Scholar 逐篇精确题名检索，优先逐篇点击结果右侧 `[PDF] domain`，必要时进入“所有版本”和定向查询。不要把“批量阶段未发现全文”当作流程终点。
4. CNKI 只通过用户已授权登录态、官方 Chrome 插件接管的用户已登录 Chrome、Computer Use 可视操作、可控 Chrome/CDP、`envctl cnki-zotero` 或用户明确提供的批量下载脚本执行；不要保存 cookies，不绕过登录、验证码或访问权限。涉及 CNKI 登录态、下载按钮、CAJ/PDF 落地、验证码恢复或机构权限时，优先使用原生 Chrome/Computer Use；只有原生能力不足、需要项目下载目录控制、批量断点续跑或用户明确要求时，才退回专用可控 Chrome/CDP。
5. Sci-Hub、LibGen、Z-Library 等绕过访问控制的来源不得纳入流程。
6. 用户提供的 PDF 可以归档，但必须先和目标参考文献做标题、作者、年份、来源、DOI 或稳定 URL 校验。
7. PDF 只有通过校验后才进入“已取得”；失败文件放入 `rejected_mismatch/`，不能混进正式清单。
8. 涉及 Google Scholar、已登录状态、右侧 `[PDF]` 点击、浏览器插件 PDF Reader、Academia/ResearchGate/SSRN 页面、机构库 PDF viewer、扩展或下载目录回收时，优先调用用户已登录 Chrome，并通过官方 Chrome 插件接管该会话；需要可视确认或桌面下载回收时使用 Computer Use。只有原生能力不可用、未授权或无法连接时，才退回隔离可控浏览器、无头浏览器或脚本请求。
9. Google Scholar 右侧 `[PDF]` 链接不能只用脚本 HTTP 请求直拉后判定成败。Academia、ResearchGate、SSRN、机构库和出版社页面常会对脚本返回 403/HTML，但官方 Chrome 插件接管用户已登录 Chrome 后可以打开或转成最终 PDF URL；必须尝试官方 Chrome/Computer Use 点击、最终 URL 记录、浏览器下载目录回收和身份校验。
10. Google Scholar 右侧 `[PDF]` 只是候选，不是身份确认。若打开后是回应文章、综述、相近题名、书章、验证码页或无关论文，必须拒收；不能因为 DOI 或题名出现在评论标题、参考文献或正文中就计为全文。
11. 自动 DOI/题名校验失败但首页显示题名、作者、期刊/工作论文编号与目标一致的开放版本，应进入双独立审核；两个审核都通过才可标记为 `acquired_dual_agent_identity_accepted_open_version` 或等价状态。
12. 正式论文写作中的参考文献仍必须回到 `citation-verifier -> zotero-sync -> writing-reference-capture`；证据材料里出现 DOI 时必须核验。无 DOI 条目可用用户提供来源、完整论文 PDF 原文或公开学术检索记录作为 DOI 豁免证据，但必须记录可审计依据。

## Project Layout

项目型任务默认使用：

```text
<project_root>/outputs/inbox/reference-fulltext/
  pdfs/
  rejected_mismatch/
  tmp/
  metadata/
  reference_download_status.csv
  downloaded_pdfs.csv
  provided_originals.csv
  unable_to_download.csv
  acquired_fulltext.md
  missing_fulltext.md
  pdf_validation.csv
```

CNKI 专项批量下载继续使用既有项目收件箱：

```text
<project_root>/outputs/inbox/cnki-downloads
```

全文 PDF 和临时下载目录必须在项目 `.gitignore` 的输出区内；状态表、校验报告和已取得/缺失清单可以保留为项目证据。

## Required Outputs

每轮结束都维护这些文件：

- `reference_download_status.csv`
- `downloaded_pdfs.csv`
- `provided_originals.csv`，仅在用户提供原件时生成
- `unable_to_download.csv`
- `acquired_fulltext.md`
- `missing_fulltext.md`
- `pdf_validation.csv`

稳定状态值只使用：

- `downloaded`
- `provided_original`
- `not_downloaded`

## Execution Order

1. 解析参考文献表，保留原始引用、题名猜测、DOI、编号和来源上下文。
2. 对每条文献做引用证据与元数据核验：证据材料里出现 DOI 时通过 DOI resolver / 出版社、Crossref、OpenAlex、Semantic Scholar、正式期刊或数据库页面核验；没有 DOI 时记录 DOI 豁免依据，包括用户提供来源、完整论文 PDF 原文或 Google Scholar / OpenAlex / CNKI 等公开学术检索记录。
3. 先尝试合法开放全文：Crossref link、Unpaywall、OpenAlex OA location、Semantic Scholar `openAccessPdf`、出版社 PDF、机构知识库。OpenAlex 负责批量发现和开放源 URL 尝试，不是英文全文获取的最后一步。
4. 对英文或国际文献，批量尝试后若没有取得可校验 PDF，必须自动进入 Google Scholar 逐篇搜索。顺序为 DOI 精确检索、精确题名、`title + DOI`、`title + first author`、`title + journal`、`title + pdf`、所有版本页。优先在用户已登录 Chrome 中点击右侧 `[PDF] domain`，并通过官方 Chrome 插件接管可见页面；打开候选后记录最终 PDF URL 或点击浏览器下载按钮；必要时用 Computer Use 回收下载目录，再重命名并校验。遇到图片、滑块、短信、Cloudflare 或账号挑战时停止并交给用户处理。
5. 对 CNKI 文献，优先使用官方 Chrome 插件或 Computer Use 在用户已登录 Chrome 中的 CNKI 授权页面执行检索和下载；需要批量化、项目下载目录控制或断点续跑时，再用 `envctl cnki-zotero find/fetch/browser-download/ingest-plan` 或可控 Chrome/CDP 接管同一授权流程。限定作者单位时先通过高级检索、详情页或元数据侧车文件证明作者单位。
6. CNKI 批量下载遇到滑块或安全验证时，不得自动拖动或绕过。`envctl` 会生成 `captcha_checkpoint`，保留当前失败项和剩余队列；用户在已登录浏览器里手动完成验证后，用上一份报告继续 `browser-download`。
7. 对用户提供 PDF 或中文原件，复制到项目输出区并生成 manifest，再做题名/作者/DOI/稳定 URL 校验。
8. 校验 PDF：文件存在、文件头含 `%PDF`、页数合理、题名或 DOI 命中；文本不可抽取时记录元数据或首页证据。短题名、扫描件、工作论文版本和 PDF 字符乱码时，必须结合作者、年份、期刊/机构库、工作论文编号或稳定 URL 做身份核验。
9. 对自动校验失败但可能正确的 PDF，先放入人工/双审队列；两个独立审核均确认题名、作者和版本关系后，才从 rejected 或下载目录提升为已取得开放版本。两个审核不一致时保留为 `uncertain`，不计入已取得。
10. 更新已取得清单、缺失清单和 Zotero 导入计划；不要把“已下载 PDF”自动等同于“正式引用已通过”，但通过 PDF 校验后可以作为 DOI 豁免证据之一。

## Keyword Harvest Adapter

The local workflow absorbs the useful status discipline from `Jinze-Lee/codex-skills-workbench/keyword-literature-download`, but it does not install that upstream skill or make PubMed/Europe PMC the default social-science route.

When the user gives a topic, keywords, or a broad literature-collection request instead of a fixed reference list:

1. Build a no-dedup candidate table first, then deduplicate by DOI, normalized title, and source record only after raw metadata is visible.
2. Keep a priority table such as high / medium / low or included / background / reject, with a reason for each status.
3. Keep the PDF folder PDF-only. HTML, XML, landing pages, logs, and helper payloads must go to a separate metadata or cache folder.
4. Save failed download attempts, HTTP status, blocked pages, captcha stops, and retry decisions; do not silently drop failures.
5. Produce a dedup manifest that says which file is kept, which is duplicate, and what key caused the merge.
6. Use PubMed, PMC, or Europe PMC only when the topic is biomedical, life-science, medical, or otherwise appropriate. For normal social-science work, prioritize OpenAlex, Crossref, Unpaywall, Semantic Scholar, Google Scholar, CNKI/CSSCI, publisher pages, and library/catalog records.
7. Downloaded files still need the same PDF identity checks before they count as acquired full text.

## CNKI Commands

先检查运行依赖和可控 Chrome/CDP：

```powershell
python -m skills.scripts.envctl cnki-zotero status --check-cdp --cdp 9333 --project-root "C:\path\to\project"
```

如果返回 `missing-python-dependency:websocket-client`，说明当前 Python 环境缺少直连 CDP 依赖；如果返回 `cdp-endpoint-unreachable`，说明依赖存在，但专用可控 Chrome 尚未启动或端口不是 9333。不要把这两种情况笼统说成“CNKI 自动链路未完成”，也不要用开放网页检索替代正式 CNKI/CSSCI 候选 gate。

准备项目收件箱：

```powershell
python -m skills.scripts.envctl cnki-zotero status --project-root "C:\path\to\project" --ensure-inbox
```

只发现候选、不下载：

```powershell
python -m skills.scripts.envctl cnki-zotero find --query "主题" --field subject --sort relevance --limit 20 --project-root "C:\path\to\project"
```

已登录 Chrome 可由原生能力或可控链路接管时批量下载：

```powershell
python -m skills.scripts.envctl cnki-zotero browser-probe --project-root "C:\path\to\project"
python -m skills.scripts.envctl cnki-zotero browser-download --input candidates.json --project-root "C:\path\to\project" --output auto
```

直接检索并下载：

```powershell
python -m skills.scripts.envctl cnki-zotero fetch --query "工程控制论" --field subject --sort latest --limit 10 --project-root "C:\path\to\project" --cdp 9333
python -m skills.scripts.envctl cnki-zotero fetch --author "陈云松" --affiliation "南京大学" --field author --sort cited --pages 2 --limit 10 --project-root "C:\path\to\project" --cdp 9333
```

如果报告里出现 `captcha_checkpoint`，先在可见的已登录 CNKI 浏览器窗口中手动完成滑块验证，然后继续：

```powershell
python -m skills.scripts.envctl cnki-zotero browser-download --input "C:\path\to\project\outputs\reports\cnki-zotero\YYYY-MM-DD.json" --project-root "C:\path\to\project" --direct-cdp --cdp 9333 --output auto
```

这个命令会读取上一份报告里的 `captcha_checkpoint.resume_candidates`，从被验证码打断的论文继续。

下载后生成导入计划：

```powershell
python -m skills.scripts.envctl cnki-zotero ingest-plan --project-root "C:\path\to\project"
```

## Detailed Workflow

需要完整字段定义、Google Scholar 逐篇点击补抓、失败项重试、所有版本页、定向 Scholar 查询、未归档浏览器下载匹配、用户提供 PDF 纳入、中文原件归档和 PDF 校验细则时，读取：

- `references/fulltext-acquisition-workflow.md`
