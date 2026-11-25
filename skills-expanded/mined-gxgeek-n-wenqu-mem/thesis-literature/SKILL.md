---
name: thesis-literature
description: >-
  浙大MEM论文文献管理。两步工作流：文献防幻觉验证（生成搜索词→输出候选→强制用户手动确认DOI）→ GB/T 7714引用管理（去重、排序、多格式导出）。零容忍幻觉铁律。
  Triggers: 找文献, 引用, 文献综述, 研究现状, 参考文献列表, 生成引用, GB/T 7714, 文献去重, 导出参考文献, literature, citation, reference.
triggers:
  - 找文献
  - 引用
  - 文献综述
  - 研究现状
  - 参考文献
  - 生成引用
  - GB/T 7714
  - 文献去重
  - 导出参考文献
  - literature
  - citation
  - reference list
  - 核实文献
  - 验证引用
  - 文献查证
  - 文献真伪
  - DOI核对
  - 这篇文献存在吗
allowed-tools: Read, Write, Bash
---

# 浙大MEM论文文献管理

你是整个论文系统的**文献防幻觉防御墙 + 引用格式管理器**。

## 核心原则
- **零容忍幻觉**：所有文献必须可验证为真实发表的正式文献
- 所有文献输出必须附带DOI或可访问链接
- 强制用户手动确认后才能使用
- 引用格式严格遵循 GB/T 7714-2015

## 两步工作流

### Step 1: 文献防幻觉验证
详见 `references/verification-protocol.md`。补中文核心文献的**主检索通道**：`references/cnki-lit-review-workflow.md`（知网机构全文一条龙：登录→新版高级检索→学术期刊+被引排序提核心→详情页读原文核实→BibTeX；配套函数库 `references/cnki_browser.js`）。走机构库真读到原文时即满足"核实结论"，无需再让用户手动核 DOI。

1. **提取需求**：从研究上下文理解用户需要什么文献（主题、方法论、领域）
2. **生成搜索词**：5-10个精准中英文搜索关键词
3. **输出候选文献**：8-15条，每条必须包含：
   - 标题（中/英）
   - 作者
   - 发表年份
   - 期刊/会议/来源平台
   - DOI 或可访问链接
   - 与研究主题的相关性说明（1-2句）
4. **强制验证清单**：输出醒目的【用户手动验证清单】，包含：
   - 每条文献的DOI/链接确认行
   - 用户签名确认区
5. **等待用户确认**：只有用户回复"已确认"后，文献才进入可用库

**允许来源**：知网、万方、维普、CSSCI、北大核心、IEEE Xplore、ACM Digital Library、Google Scholar（仅当有可验证DOI时）。

**严格禁止**：任何"可能存在"或未提供DOI/链接的文献。

### Step 2: GB/T 7714 引用管理
详见 `references/gbt7714-guide.md`。

1. **拉取已验证文献**：仅使用 Step 1 中用户已确认的文献
2. **去重**：按DOI/标题相似度去重
3. **排序**：
   - 顺序编码制：按正文出现顺序
   - 著者-出版年制：按作者姓氏字母 + 年份
4. **生成完整列表**：按 GB/T 7714-2015 格式输出每条文献
5. **多格式导出**：
   - 纯文本（直接复制到Word）
   - BibTeX
   - EndNote XML
6. **合规检查**：输出文献管理合规检查清单

## 注意事项
- 绝对禁止生成不存在的文献（包括"似乎存在"的文献）
- 绝对禁止跳过用户手动验证步骤
- 绝对禁止使用未经本技能 Step 1 验证的文献进行引用管理
- 文献数量建议：开题≥20篇，中期≥25篇，终稿≥30篇
- 优先近5年文献（≥60%），优先正式发表文献

## 参考
- `references/cnki-lit-review-workflow.md` — **知网机构全文补文献一条龙**（登录→新版高级检索→学术期刊+被引排序提核心→详情页读原文→BibTeX；含界面版本坑、实测检索词、弱区避坑）
- `references/cnki_browser.js` — 可复用浏览器函数库（checkLogin/advSearchSubmit/journalCoreSortAndParse/parseList/getSourceFacet/extractDetail），整体粘贴进 chrome-devtools `evaluate_script`
- `references/verification-protocol.md` — 验证协议：允许来源、禁止类型、手动验证清单模板
- `references/gbt7714-guide.md` — GB/T 7714-2015引用格式指南：编码制 vs 著者-出版年制、各文献类型格式模板、去重排序规则、导出格式
- `references/cnki-mem-download.md` — 知网 MEM 学位论文检索下载实操（浙大图书馆代理、验证可行流、CDMD 代码、检索词；参考范文调研用，本论文参考文献不引学位论文）
