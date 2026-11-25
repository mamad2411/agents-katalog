---
name: wiki-maintenance
description: |
  YouDao Note Wiki 维护工作流。当用户要求"整理 wiki""修 wiki 格式""wiki lint"
  "检查笔记格式""统一风格"时触发。提供 P0-P4 五级问题分级、批量修复、
  验证迭代的完整 pipeline。适用于任何基于 youdaonote CLI 的 LLM Wiki。
triggers:
  - 整理 wiki
  - 修 wiki
  - wiki lint
  - 检查笔记格式
  - 统一风格
  - 维护知识库
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Wiki 维护工作流

## 0. 前置约束（不可违背）

以下约束来自 youdaonote-llm-wiki 官方准则，维护操作必须遵守：

| 约束 | 说明 | 违反后果 |
|------|------|---------|
| **raw 内容不可改** | `raw/` 下的正文内容（段落、观点）绝不修改。但格式恢复（HTML 反转义、补 `.md` 后缀）可以——这是还原可读性，不是修改内容 | 破坏素材溯源 |
| **.md 后缀不可去** | rename 或新建时标题必须以 `.md` 结尾。无 `.md` = 原生 Note，CLI 读不了、App 不渲染 | 笔记变"死"
| **标题小写连字符** | 新建/重命名用 `kebab-case.md`，如 `variant-calling.md` | 风格混乱 |
| **大批量先确认** | 一次维护影响 10+ 个已有页面时，**必须先询问用户确认范围** | 不可控变更 |
| **禁止孤立页面** | 每个页面至少用 `→` 引用一个其他页面。创建新页时必须同时建立交叉引用 | 知识库退化 |
| **搜索分页** | `youdaonote search` 每次最多 15 条，更多结果用 `youdaonote call searchNotes keyword=xxx startIndex=15` | 扫描遗漏 |

**会话启动（每次维护前）**：
1. `youdaonote list` 定位 `youdaonote-wiki-registry.md`
2. 读取注册表，A+B 策略选定目标知识库
3. 读取 schema.md 获取 ROOT_ID 及各子文件夹 ID、fileId 注册表

## 1. 问题分级（P0-P4）

任何 wiki 格式问题按此优先级处理。先扫 P0（机械化、零风险），再处理 P1-P2（需人工判断），最后补 P4。

| 档位 | 问题类型 | 处理方式 | 风险 | 批量？ |
|------|---------|---------|------|--------|
| **P0** | HTML 实体（`&gt;` `&lt;` `&quot;` `&amp;` `&#39;`）、cite/entity 编辑器标记 | sed/Python 反转义 | 零 | ✅ 全自动 |
| **P1** | 结构问题：无 Markdown 标题、中文数字编号（"一、二、三"）、空格分隔表格、纯文本无层级 | 全文重写为 H1→H2→表格 结构 | 低 | ❌ 逐篇 |
| **P2** | 标题与内容不符：笔记标题是 A，内容全是 B | rename 或重写 | 中 | ❌ 需先读内容确认 |
| **P3** | 占位草稿：仅 1-3 行、无实质内容、与其他笔记重复 | delete（需确认无价值） | 中 | ⚠️ 需人工确认 |
| **P4** | 缺交叉引用：无「关联页面」节、正文无 `→` 指向其他页面 | 脚本追加模板化「关联页面」 | 低 | ✅ 半自动（关键词匹配） |

**执行顺序**：P0 → P1 → P2 → P3 → P4。每档完成后做一轮验证，再进入下一档。

## 2. 批量修复脚本模板

### P0：HTML 实体反转义

**推荐：使用项目脚本**（`/root/llm-wiki/fix-html-entities.py`）：

```bash
# 单篇
python3 /root/llm-wiki/fix-html-entities.py --fid <fileId>

# 多篇
python3 /root/llm-wiki/fix-html-entities.py --fids <fid1> <fid2> <fid3>

# 从 index.md 全库扫描（自动跳过 raw/）
python3 /root/llm-wiki/fix-html-entities.py --from-index <indexFid> --raw-folder-id <rawId>

# 安全模式：只检查不上传
python3 /root/llm-wiki/fix-html-entities.py --fid <fileId> --dry-run
```

脚本自动处理：
- HTML 实体反转义（正确顺序：`&#34;/&#39; → &gt;/&lt; → &nbsp; → &amp;`）
- cite/entity 编辑器标记清理
- copy provenance 块识别（前 10 行不跳检）
- 修复后验证（残留实体、H1、摘要、交叉引用）
- raw/ 文件夹自动跳过（通过 `--raw-folder-id`）

**手动方案（脚本不可用时）**：

```bash
# Step 1: 下载笔记
youdaonote read <fileId> > /tmp/note.md

# Step 2: sed 反转义（8 类实体，顺序关键）
sed -e 's/&#34;/"/g; s/&quot;/"/g; s/&#39;/'\''/g; s/&apos;/'\''/g; s/&gt;/>/g; s/&lt;/</g; s/&nbsp;/ /g; s/&amp;/\&/g' \
  /tmp/note.md > /tmp/note-fixed.md

# Step 3: 验证
grep -E '&(gt|lt|amp|quot|#39|apos|nbsp);' /tmp/note-fixed.md && echo "FAIL" || echo "PASS"

# Step 4: 上传
youdaonote update <fileId> --file /tmp/note-fixed.md
```

**注意事项**：
- `&#34;`/`&quot;` 是双引号，`&#39;`/`&apos;` 是单引号，都要处理
- `&amp;` 必须最后处理，否则会把已修正的 `&gt;` 中的 `&` 再转义
- Youdao copy provenance 块（`> copied_from:`）中的 `>` 也会被写成 `&gt;`，需要一并修复

### P0-b：cite/entity 编辑器标记清理

```python
import re

with open('/tmp/note.md', 'r', encoding='utf-8') as f:
    content = f.read()

# entity 标记：提取名称保留（如 "10x Genomics"）
content = re.sub(r'entity\["[^"]*","([^"]*)","[^"]*"\]', r'\1', content)
# cite 标记：直接删除
content = re.sub(r'cite[^]*', '', content)
```

### P4：批量追加交叉引用

```python
import re

# 标题 → 模板映射（根据 wiki 主题定制）
TEMPLATES = {
    r'WES|wes|variant|VCF|BAM': "- 概念：→ wes-analysis-workflow\n- 实体：→ GATK",
    r'RNA|rnaseq|DE|差异表达|GSEA': "- 概念：→ bulk-rnaseq-workflow\n- 实体：→ DESeq2 / → edgeR",
    # ... 按需扩展
}

def get_template(title):
    for pattern, template in TEMPLATES.items():
        if re.search(pattern, title, re.I):
            return template
    return "- 系统：→ index.md / → schema.md"

# 追加到笔记末尾
appendix = f"\n\n## 关联页面\n\n{get_template(title)}\n"
```

## 3. 验证迭代法

**第一轮验证**：修完每档后，抽查 5-10 篇（覆盖不同类别）。

**第二轮验证**：换一批样本，用不同方法检查：
- 第一轮用 `head -5` 检查格式 → 第二轮读全文检查 HTML 实体
- 第一轮抽查 notes → 第二轮抽查 entities/concepts

**第三轮验证**：全库扫描脚本：

```bash
# 从 index.md 提取所有 fileId，逐个检查 HTML 实体
python3 -c "
import re, subprocess
fids = re.findall(r'[A-F0-9]{32}', open('/tmp/index.md').read())
for fid in set(fids):
    r = subprocess.run(['youdaonote','read',fid], capture_output=True, text=True)
    if r.returncode == 0:
        n = len(re.findall(r'&(?:gt|lt|amp|quot|#39|apos|nbsp);', r.stdout))
        if n > 0:
            print(f'{fid}: {n} entities')
"
```

**关键原则**：
- 验证脚本必须跳过 copy provenance 块（前 6-8 行）再检查正文格式
- provenance 块中的 `→` 是 `→ copied_to:` 不是真正的交叉引用
- "验证一次通过"不可靠，必须换方法再做一轮

## 4. 常见陷阱

| 陷阱 | 表现 | 解决 |
|------|------|------|
| **provenance 块误判** | 脚本看到 `→` 就认为有交叉引用，实际是 `→ copied_to:` | 跳过前 10 行再检查 |
| **H1 位置偏移** | copy provenance 块在 H1 之前，脚本读第一行找不到 `# ` | 在前 15 行内搜索第一个 `# ` |
| **&amp; 顺序** | sed 中 `s/&amp;/\&/g` 必须在 `s/&gt;/>/g` 之后执行 | 按 `&gt;→&lt;→&quot;→&#39;→&nbsp;→&amp;` 顺序 |
| **批量rename后不同步** | rename 了笔记标题，但 index.md 里还是旧名 | rename 后立即更新 index.md |
| **标题与内部H1不一致** | 笔记标题是 A.md，内部 H1 还是 `# B` | rename 后检查并修改内部 H1 |
| **去掉 .md 后缀** | rename 成 `variant-calling`（无后缀），笔记变原生 Note | 必须保留 `.md`：rename 为 `variant-calling.md` |
| **修改 raw/** | 脚本批量反转义时把 `raw/` 下的笔记也修了 | 扫描前先按 folderId 过滤，raw/ 下的 fileId 跳过 |
| **搜索分页遗漏** | 全库扫描只用 `youdaonote search`，只拿到前 15 条 | 循环调用 `searchNotes` 并递增 `startIndex` 直到无新结果 |

## 5. 维护后必须同步的文件

每轮维护完成后，必须更新：

1. **index.md**：删除已删除笔记的行、更新重命名后的标题、更新描述
2. **log.md**：追加维护记录（日期、触发原因、处理清单、结果统计）
3. **schema.md**（如有架构变更）：更新章节定义、folder ID 注册表
4. **schema.md 底部 fileId 注册表**：新建/删除/重命名笔记后，同步更新 `## fileId 注册表（Agent 维护）` 中的 ID 映射。这是跨会话恢复和注册表自动重建的基础

## 6. 决策树

```
用户说"整理 wiki" →
  1. 读取 index.md 和 schema.md 了解当前状态
  2. 抽样读取 5-10 篇笔记做体检
  3. 按 P0-P4 分级分类问题
  4. 询问用户修哪几档（默认 P0 必做）
  5. 批量修复 → 验证 → 下一档
  6. 更新 index.md + log.md
  7. 汇报统计
```
