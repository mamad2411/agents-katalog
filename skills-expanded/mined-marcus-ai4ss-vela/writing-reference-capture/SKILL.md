---

name: writing-reference-capture

description: Use when a manuscript, review response, report, or export is being delivered and only the papers actually cited or used in that writing need citation-evidence verification, Zotero entry, and Obsidian sync. DOI must be verified when present in the evidence; user-provided sources, complete paper PDFs, and public academic index records can waive the requirement that every formal reference must have a DOI. Not for downloading PDFs or building a literature corpus.

---



# Writing Reference Capture



在研究写作进入正式交付前使用这个 skill。



## Scope



适用对象：

- 综述写作

- 审稿回复

- 项目简报

- 论文草稿

- 结构化导出文稿



不适用对象：

- 只是检索过、但没有真正写进论证链的候选文献

- DOI 无法核验，且也没有用户提供来源、完整论文 PDF 原文或公开学术检索记录的文献

- 真实性无法确认的网页材料



## Defaults



- `capture_scope = writing-used`

- `reuse_project = true`

- sync direction = `Zotero -> Obsidian`

- Zotero write path = `local connector first`



## Hard Gate



只有同时满足以下条件的条目，才允许进入正式写作链：

1. 确实在本次写作中被实际使用

2. 已通过 `citation-verifier` 或等价引用证据核验

3. 证据材料里出现 DOI 的条目必须完成 DOI 核验

4. 无 DOI 条目必须至少具备一种 DOI 豁免证据：用户提供来源、完整论文 PDF 原文、或 Google Scholar / OpenAlex / CNKI 等公开学术检索记录

5. 发表信息真实可核验；PDF 路径必须记录来源、首页/元数据、题名、作者、年份、来源和页数可读性；公开检索记录必须记录平台、检索入口或记录链接、核验时间和题名/作者/来源匹配

6. 如果本次交付是学术论文或正式综述，正文实际引用的每篇文献必须能回连到 citation evidence audit：引文表、证据句、标注 PDF、截图和最终 accepted registry。新增引用不能只进入参考文献表。

7. 若写作中新增、删除或改窄某条引用，必须回到 `evidence-based-literature-workflow` 的 PDF 标注和双复核 gate，更新证据表与 accepted registry 后再交付。



任一条件不满足，都必须停留在候选层，不得伪装成正式参考文献。



## Required Inputs



执行前先解析这些字段：

- `project_name`

- `project_slug`

- `writing_artifact`

- `writing_used_papers`



如果 `project_name` 为空，就从当前任务标题或写作目标归一化生成。



## Execution Order



1. 识别本次写作里实际用到的论文。

2. 排除没有真正进入论证、比较或正式引用的候选文献。

3. 对每条文献运行引用证据核验：证据材料里出现 DOI 时核验 DOI；无 DOI 时核验用户提供来源、完整 PDF 原文或公开学术检索记录。

4. 对正式学术写作，核对正文引用、参考文献表、citation evidence table 和 accepted registry 四者一致；发现新增或未标注文献时，先转入 `evidence-based-literature-workflow`。

5. 只保留 `verified-formal-with-doi` 或 `verified-formal-with-doi-waiver`。后者表示 DOI 缺失时，已用用户提供来源、完整 PDF 原文或公开学术检索记录完成可审计核验。

6. 解析 Zotero 目标：

   - 先匹配现有同名 collection

   - 再看用户显式指定的 target

   - 再决定是否允许回退到 library root

7. 优先使用本地 Zotero connector 直写，不把 Web API 作为默认前提。

8. 对已写入条目统一打上：

   - `source/codex-writing`

   - `project/{project_slug}`

   - 必要时 `status/preprint`

9. 把同步后的文献笔记写入：

   - `VELA Research/20-文献/_zotero-sync/{project_slug}/`

10. 更新或创建：

   - `VELA Research/10-项目/{project_slug}.md`



## Zotero Target Rule



本地 connector 已经支持“写入现有目标”和“会话内改投目标”，但不负责自动新建 collection。



因此目标解析固定为：

1. 复用现有同名或显式指定 collection

2. 如果没有现成 collection 且允许降级，回退到 library root

3. 如果既没有现成 collection、也不允许降级，就明确返回阻塞证据



不要把“本地 connector 不能新建 collection”误说成“Zotero 不可写”。



## Fulltext Acquisition Boundary



如果写作过程中发现需要“补齐全文 PDF”“下载参考文献原文”“CNKI 批量下载”或“整理已取得/缺失全文清单”，先转入 `reference-fulltext-acquisition`。



固定边界：

1. `writing-reference-capture` 负责正式写作里实际使用文献的引用证据核验、Zotero 入库和 Obsidian 同步。证据材料里出现 DOI 时必须核验；无 DOI 时记录用户提供来源、完整 PDF 原文或公开学术检索记录作为 DOI 豁免证据。

2. `reference-fulltext-acquisition` 负责全文 PDF 获取、授权下载、用户提供 PDF 归档、PDF 校验、已取得/缺失清单和 Zotero 附件导入计划。

3. CNKI、Google Scholar、OpenAlex、Semantic Scholar、浏览器和 Zotero 都是全文获取流程调用的工具层，不直接替代统一流程。

4. 下载文件不能直接升级成正式引用；正式引用仍然需要 citation gate。PDF 已核验时可作为 PDF 全文证据。

5. 无 DOI 条目进入正式写作链的前提是：已有用户提供来源、完整论文 PDF 原文或公开学术检索记录，并把 DOI 豁免证据写入核验报告；不能伪装成 DOI 完整条目。



## Local Script



优先复用：

- `<VELA_RUNTIME_ROOT>\skills\scripts\writing_reference_capture_local.py`



标准调用示例：



```powershell

& "<VELA_RUNTIME_ROOT>\.venv\Scripts\python.exe" `

  "<VELA_RUNTIME_ROOT>\skills\scripts\writing_reference_capture_local.py" `

  --project-name "CSS Writing Demo" `

  --doi "10.1126/science.1167742" `

  --doi "10.1038/445489a" `

  --doi "10.1146/annurev-soc-121919-054621" `

  --allow-library-root-fallback

```



## Output Contract



返回结构化结果：



```markdown

# Writing Reference Capture



## Project



## Zotero Target



## Verified Papers



## Newly Written Items



## Obsidian Sync Target



## Rejected Candidates



## Blockers

```



## Failure Rules



遇到以下情况必须停止并明确说明阻塞证据：

- 写作对象里提取不出稳定的论文列表

- 条目 DOI 无法核验，且没有可接受 DOI 豁免证据

- 条目真实性无法核验

- Zotero connector 不可用

- 项目匹配存在歧义

- Obsidian 目标目录无法解析
