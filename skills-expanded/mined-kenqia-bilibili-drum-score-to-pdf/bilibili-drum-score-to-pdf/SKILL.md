---
name: bilibili-drum-score-to-pdf
description: 将 B站链接或本地纵向滚动鼓谱视频合成长截图，按连续谱面等比分页为 A4 PDF，可安全地局部去水印。
---

# 鼓谱视频转 PDF

交付以实际谱名命名的 A4 PDF。默认每页保留长截图中的一块连续谱面，保持原有行距及记号位置。原图直排未经逐符号校对，仍可能存在拼接、模糊或遮挡问题。

仅在用户显式选择 `$bilibili-drum-score-to-pdf` 时使用本 Skill。选择后提供视频链接或本地视频路径，即执行 PDF 流程。未指定输出位置时，在当前工作目录建立独立任务目录，保留已有同名文件。交付时报告 PDF 绝对路径。

从本文件实际位置确定 Skill 根目录。需要 Python 3.12、uv、ffmpeg、ffprobe、Poppler 和图片查看能力。使用隔离依赖环境，`<skill-root>` 替换为本文件所在目录的绝对路径：

```sh
uv run --python 3.12 --quiet --isolated --with-requirements "<skill-root>/scripts/requirements.txt" \
  python "<skill-root>/scripts/convert.py" '视频链接或本地视频路径' --output /absolute/new-task
```

## 正常流程

1. 准备后调用 `stage`，程序生成长截图和完整谱行切分。查看长图及原生首尾，检查明显漏行、重复和裁断，用 `review-longshot(title, notes)` 记录一次整体审阅。轻微模糊、底色、水印和播放标记可保留，不逐符号校对或逐行填写来源。
2. 如需去水印，只对实际确认没有音符、五线、标题或署名的区域调用 `clean-watermark`，提交当前长图 hash、矩形及安全确认。无法确认安全或水印与谱面重叠时保留。查看清理结果，原长图保持独立保存。
3. 再调用 `stage`，直接取得 A4 PDF 和全部有序预览。每页一块连续条带，统一比例并保持页内原行距。自动试算最多缩小 10% 的紧凑分页，仅在能减少页数且满足几何与字号门槛时采用；否则保留原尺寸。具体门槛见阶段指南。
4. 实际查看全部页面，核对谱名、首尾、明显漏行或重复、裁断及打印字号，特别查看每个分页切口两侧的渐强、圆圈及重音。紧凑版需确认稍小的音符仍可读。有疑问时通过 `layout(page_breaks)` 按原尺寸把相关行留在同页，再导出并重看全部页面。以当前 `output_revision` 调用 `review-pdf`。`stage.phase=complete` 后交付，使用实际输出的 `notice`，说明未经逐符号校对。

明显漏行或重复先用 `stitch` 修复拼接；严重遮挡优先 `capture` 查找原视频清楚画面，再用 `repair-longshot` 等尺寸替换局部，重新整体查看。仍无法恢复时说明限制，不猜隐藏符号，也不把已知缺段称为完整谱。恢复与清理字段读取 [stage-recovery-layout.md](references/stage-recovery-layout.md) 和 [reconstruction-entry.md](references/reconstruction-entry.md)。

## 可选重绘与矢量

用户明确要求重绘或矢量时，用 `pdf-route(route, notes)` 记录请求，route 为 redraw 或 vector。新任务不会因为外观不够干净自动切换路线。已有任务保留原路线及调用恢复；未知调用先恢复原 ID。

重绘执行、一次修正及矢量兜底按上述阶段指南处理。只有真实生图的结果才披露模型局部推测；矢量只转描可见外形，不能恢复隐藏记谱。`--summary` 的 `details.path` 保存完整回执，读取后取得全部请求和产物。

首版支持已有白底多行、固定比例的纵向滚谱，优先适配停驻后向上推进。缩放、横移、复杂翻页及没有谱面的演奏视频不纳入首版。无法查看图片时如实报告。匿名获取和宿主检查见 [support.md](references/support.md)。
