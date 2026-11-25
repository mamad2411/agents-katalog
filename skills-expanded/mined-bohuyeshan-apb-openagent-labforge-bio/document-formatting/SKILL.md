---
name: document-formatting
description: "论文DOCX格式规范v4最终版：14pt宋体/TNR正文、1.5倍行距、0.74cm首行缩进、全角中文标点、REF field code交叉引用、GB/T 7714-2015参考文献"
category: academic
exposure: standard
---

# 论文DOCX格式规范 v4（最终版）

用于生成学术论文 DOCX 的最终排版标准。**此版本为生产验证的 v4 最终版规范**。

## 一、正文格式

| 属性 | 值 |
|------|-----|
| 中文字体 | 宋体 SimSun |
| 英文/数字字体 | Times New Roman |
| 字号 | 14pt |
| 行距 | 1.5倍（全文统一） |
| 首行缩进 | 0.74cm |
| 段前段后 | 0行 |

## 二、标点符号

| 语境 | 规则 | 示例 |
|------|------|------|
| 中文 | 全角（，。；：""！？） | 结果表明，该基因显著上调。 |
| 英文 | 半角（,.;:""!?） | The results show that... |
| 数字/字母 | 半角 | 1.5倍、GeneA、PCR |

## 三、标题格式

| 级别 | 字体 | 字号 | 加粗 | 段前距 | 段后距 |
|------|------|------|------|--------|--------|
| 主标题 | 黑体 SimHei | 16pt | 是 | — | 24pt |
| 一级标题 (##) | 黑体 SimHei | 15pt | 是 | 18pt | 6pt |
| 二级标题 (###) | 黑体 SimHei | 14pt | 是 | 12pt | 3pt |

## 四、引文格式

- **上标**：14pt，superscript
- **多引用格式**：`[5][6]` 紧贴，**无逗号无空格**
- **编号顺序**：严格按正文**首次出现顺序**，1-28连续无跳号
- **交叉引用**：使用 Word 原生 `{ REF ref-N \h }` field code
  - 非 `{ HYPERLINK \l }`——`HYPERLINK` 在 Word 中不可靠
  - `Ctrl+点击` 跳转到参考文献条目
  - 在 Word 中按 `Alt+F9` 可看到 field code 源码

## 五、图片/表格标题

| 属性 | 值 |
|------|-----|
| 字号 | 12pt |
| 加粗 | 否 |
| 对齐 | 居中 |
| 行距 | 1.5倍 |

## 六、参考文献格式（GB/T 7714-2015）

| 属性 | 值 |
|------|-----|
| 编号格式 | Word 自动编号 `[1][2][3]`（非手打文本） |
| 编号间距 | `<w:suff w:val="space"/>` 禁用tab，仅一个空格 |
| 字体 | 12pt，宋体/Times New Roman |
| 行距 | 1.5倍 |
| 英文作者格式 | 姓全大写 + 名首字母（如 `LIN H, YAO Y`） |

**条目格式示例**：

| 类型 | 格式 |
|------|------|
| 期刊论文 `[J]` | 作者. 题名[J]. 刊名, 年, 卷(期): 页码. DOI |
| 学位论文 `[D]` | 作者. 题名[D]. 学校, 年份 |
| 会议论文 `[C]` | 作者. 题名[C]. 会议名称, 年份 |

## 七、页边距

| 方向 | 值 |
|------|-----|
| 上/下 | 1英寸 |
| 左/右 | 1.25英寸 |

## 八、DOCX 输出规则

- **管线**：直接解析 Markdown → 生成 DOCX（不经过 Pandoc，不经过 HTML）
- **引用处理**：REF field code + Word 自动编号（自定义 numbering XML 实现 `[%1]` 格式）
- **编号间距控制**：`<w:suff w:val="space"/>` 编号后仅一个空格，不插入tab
- **图片搜索**：多 base 路径搜索
- **生成后清理**：自动清除 python-docx 默认 author 信息（除非用户指定）
- **更新域标记**：在 `word/settings.xml` 中设置 `<w:updateFields w:val="true"/>`

## 九、辅助工具

| 脚本 | 用途 |
|------|------|
| `build_docx_ref_codes.py` | 主生成脚本：MD→DOCX v4 最终输出 |
| `renumber_citations.py` | 引文重排脚本：按正文首次出现顺序重新编号 |

## 十、关键技术点

1. **REF field code**（非 HYPERLINK），Alt+F9 可查看源码
2. **numbering.xml** 自定义 `[%1]` 编号格式
3. **引文逗号已移除**，多引用直接紧贴 `[5][6]`
4. **中文半角引号全部改为全角**
5. **编号间距**：`<w:suff w:val="space"/>` 禁用tab，仅一个空格
6. **引文重排脚本** `renumber_citations.py` 自动排序

## 十一、引用 Python 实现参考

生产脚本路径（已验证 v4 最终版）：
```
F:\swxxx\scripts\build_docx_ref_codes.py
F:\swxxx\scripts\renumber_citations.py
```

核心流程：
1. 逐行解析 Markdown（正则切分 `[N]` 引用、`**加粗**`、Markdown 有序列表 `N. `）
2. 正文 `[N]` → `add_ref_field()` 插入 `{ REF ref-N \h }` field code
3. 参考文献 `N. 作者...` → `add_ref()` 使用 Word `List Number` 样式 + 自定义 numbering
4. 保存后注入 `word/numbering.xml` 自定义编号格式 `[%1]`
5. 注入 `word/settings.xml` 的 `updateFields` 标记
6. `renumber_citations.py` 按首次出现顺序重新编号并更新全文引用
