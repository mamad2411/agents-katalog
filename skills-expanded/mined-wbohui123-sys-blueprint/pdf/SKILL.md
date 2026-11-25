---
name: pdf
description: 提取 PDF 文字或查看页面。
disable-model-invocation: true
---

# 读 PDF（poppler）

需已安装 Poppler；用 `pdftotext -v` 和 `pdftoppm -v` 确认所需命令可用。

## 用法

```bash
pdftotext 文件.pdf -                          # 抽全文，直接打到屏幕上读
pdftotext -layout 文件.pdf 出.txt             # 保留版面（表格、分栏用这个）
pdftotext -f 2 -l 5 文件.pdf -                # 只要第 2 到第 5 页
pdftoppm -png -r 100 -f 1 -l 1 文件.pdf 页    # 第1页转成图，出 页-1.png，再用 read_image 看
```

## 怎么选

- **先抽文字。** 抽出来能读懂就不要转图 —— 转图再看，一页就是一张图的钱，长文档会很贵。
- **抽出来是空的或乱码** → 它是扫描件（图片），只能转图看。
- **要看版面长什么样**（排版、图表位置）→ 转图。

## 坑

- **查版本是 `pdftotext -v`，不是 `--version`**，而且它打到 stderr。
- `pdftoppm` 的最后一个参数是**前缀**不是文件名：写 `页` 出来的是 `页-1.png`。
- `-r` 是 dpi，100~150 够读；调到 300 图会很大。
