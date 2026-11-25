---
name: tech-distiller
description: Distill company/team technical knowledge from internal or external documents into a structured report, filtered by technical direction/role. Use when the user wants to: (1) collect and summarize technical docs from any source (URL, file, wiki, API, knowledge base), (2) filter content by role or direction (e.g., 搜索, 推荐, 后端, 基础架构, 数据平台, ML, 客户端, 前端), (3) generate a polished technical summary report capturing architecture, algorithms, interfaces, and design decisions, (4) evolve or refine an existing report with new documents. Triggers on phrases like "蒸馏技术文档", "生成技术报告", "distill tech docs", "tech knowledge report", "技术总结", "按职位方向生成报告", "公司技术蒸馏", "知识沉淀".
---

# Tech Distiller

蒸馏公司/团队技术知识，生成按职位方向过滤的结构化技术报告。

## Workflow

### Step 1 — Gather Inputs

Ask only for what is missing. Proceed as soon as enough context exists.

| Input | Description | Example |
|---|---|---|
| **文档来源** | URLs, file paths, API endpoints, wiki spaces, knowledge base IDs | `https://wiki.company.com`, local `.md` files, Feishu docs |
| **技术方向** | Role / domain to focus on | `搜索算法`, `推荐系统`, `后端服务`, `数据平台`, `基础架构`, `ML/AI`, `客户端`, `前端`, or free text |
| **输出格式** | Report format | `markdown` (default), `docx`, `pptx` |
| **报告深度** | Detail level | `overview` (高层概述), `detailed` (架构 + 接口 + 决策) |
| **目标受众** | Who will read this | `新员工`, `技术评审`, `外部分享`, `团队内部` |

---

### Step 2 — Fetch & Filter Documents

For each source:

1. **URLs** → `web_fetch`. Paginate if search-based, fetch multiple pages.
2. **Local files** → `read`.
3. **Knowledge bases / APIs** → use whatever skill or tool is installed for that platform. If no skill covers the source, ask the user for credentials or API details.

After fetching, **filter by technical direction** using `references/filtering-guide.md`:
- Keep paragraphs matching ≥ 2 direction-specific signals.
- Discard off-topic content (HR, legal, unrelated products).
- If fewer than 3 relevant documents found, warn the user and offer to broaden scope.
- For sources > 50k tokens, chunk and summarize in passes.

---

### Step 3 — Extract Technical Signals

Extract what exists; skip what doesn't:

- **Architecture overview** — components, data flow, dependencies
- **Core algorithms / models** — techniques, frameworks, training/serving approach
- **Key interfaces / APIs** — endpoints, schemas, contracts
- **Performance & scale** — metrics, SLAs, data volume, QPS
- **Design decisions & trade-offs** — why X over Y
- **Tech stack** — languages, frameworks, infra
- **Open problems / roadmap** — known limitations, future work

---

### Step 4 — Generate Report

Use `scripts/render_report.py` with a JSON payload, or generate directly in Markdown.

Report structure:

```
# [Direction] 技术蒸馏报告
**生成时间**: YYYY-MM-DD
**技术方向**: <direction>
**目标受众**: <audience>
**文档来源**:
- <source 1>
- <source 2>

---

## 1. 技术全景概述
## 2. 核心架构
## 3. 关键算法与模型
## 4. 接口与数据契约
## 5. 性能与规模
## 6. 技术决策与权衡
## 7. 技术栈速览
## 8. 已知问题与演进方向

---
*本报告由 tech-distiller 自动生成，请结合原始文档交叉验证。*
```

Omit sections with no content. Do not leave blank sections.

---

### Step 5 — Deliver Output

- **Markdown** → print in chat.
- **docx** → trigger the `docx` skill.
- **pptx** → trigger the `pptx` skill.

Always end with:
> 📎 共处理 **N** 份文档，覆盖 **M** 个技术主题。如需深入某一模块，请告知。

---

## Evolution — 报告进化机制

Tech-distiller reports are living documents. Support these update flows after initial delivery:

### 追加文档
User provides new documents → analyze incremental content → merge into the existing report sections → do not overwrite prior conclusions unless they conflict → append a `📌 本次更新` summary at the end.

### 对话纠正
User says "这个不对，实际上是 XXX" → write a `Correction` note into the relevant section, mark it with `⚠️ 已纠正`, and explain what changed.

### 版本管理
Each time the report is substantially updated, save a versioned snapshot:
- Use `scripts/render_report.py --output reports/<slug>-v<N>.md`
- Track versions in `reports/versions.json`
- Support rollback: "回滚到上一版" → restore previous snapshot

### 深挖模式
After report delivery, if the user asks "深入架构那部分" or "展开第3节":
- Re-fetch source documents for that section only
- Generate an expanded sub-report for that module
- Offer to merge it back into the main report

---

## Notes

- **保密原则**: Never include content marked confidential, internal-only beyond the user's access level, or PII. If in doubt, omit and flag.
- **Sparse sources**: Warn if < 3 relevant docs found before generating.
- **Quality > Coverage**: A focused 3-section report beats a shallow 8-section one.
- See `references/filtering-guide.md` for per-direction filtering heuristics.
