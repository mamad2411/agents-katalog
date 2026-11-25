---
name: markitdown
description: 把当前项目的 DOCX、XLSX、PPTX 办公材料读成有标题和表格的 Markdown。
disable-model-invocation: true
---

# 读取办公材料

取得当前项目办公材料中可供分析、引用和制作演示的实际内容。使用 MarkItDown 0.1.8 的本地转换器，支持 DOCX、XLSX、PPTX；PDF 的文字和版面继续用 pdf skill。

```bash
uv run --no-project --no-build --locked <本技能目录>/scripts/读办公材料.py 材料/项目说明.docx --out 草稿/项目说明提取.md
```

程序输出提取文件的实际路径，再按当前问题读相关部分。标题、表格、工作表名称和演讲备注尽量保留；数值与引用需要回到原材料核对，尤其是 Excel 中没有缓存值的公式。

依赖由脚本和锁文件声明，通过项目 uv 缓存准备 Python 3.12 与办公转换库，不全局安装，也不启用云解析、图片模型或第三方插件。已有输出默认不覆盖，需要替换时显式加 `--overwrite`。使用 `--check` 可查看实际 Python 和包版本。

这是内容读取，不是 Word/PPT 排版还原，也不重算或修改 Excel。图片中的文字、复杂合并单元格和版面关系未必完整；需要这些依据时查看原材料。固定版本及来源见 [来源](references/来源.md)。
