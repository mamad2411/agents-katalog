---
name: paper-download
description: 使用 ai4scholar.net API 下载论文 PDF。当用户给出 DOI 或标题，要求下载论文全文时使用此技能。
---

# 论文 PDF 下载技能

使用 ai4scholar.net API 下载学术论文的 PDF 全文。

## 触发条件

用户发送 DOI（如 `10.1038/s41586-021-03819-2`）或论文标题，要求下载 PDF。

## 使用方法

### API 密钥配置

用户的 API 密钥: `sk-user-ee5641ea7811c69b4c4dfaaa25f2fea1f9341ecd75c4cc00`

### 运行下载命令

**通过 DOI 下载:**
```bash
cd "/Users/richard/Documents/life/shared/inbox/zotero 插件/Ai4scholar" && python3 S17_pdf-download.py --api-key "sk-user-ee5641ea7811c69b4c4dfaaa25f2fea1f9341ecd75c4cc00" --doi "DOI" --output ./papers
```

**通过标题下载:**
```bash
cd "/Users/richard/Documents/life/shared/inbox/zotero 插件/Ai4scholar" && python3 S17_pdf-download.py --api-key "sk-user-ee5641ea7811c69b4c4dfaaa25f2fea1f9341ecd75c4cc00" --title "论文标题" --output ./papers
```

**批量下载 (CSV):**
```bash
cd "/Users/richard/Documents/life/shared/inbox/zotero 插件/Ai4scholar" && python3 S17_pdf-download.py --api-key "sk-user-ee5641ea7811c69b4c4dfaaa25f2fea1f9341ecd75c4cc00" --csv input.csv --output ./batch
```

## 输出结果

- PDF 文件保存在 `./papers/` 目录
- 元数据保存在 `meta.json` 和 `papers.csv`

## 注意事项

- 部分论文没有开放获取 PDF，此时只能保存元数据
- 脚本位置: `/Users/richard/Documents/life/shared/inbox/zotero 插件/Ai4scholar/S17_pdf-download.py`
