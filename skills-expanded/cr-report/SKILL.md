---
name: cr-report
description: 打开已有的尽调报告、查看来源和策展列表、导出 PDF。用户要看报告或来源、要 PDF，或消息里带 export_pdf 操作时读这份。
---

# 看报告、看来源、导出 PDF

## 打开报告或来源

用户没说哪一份时，用 `selectedJobId` 指向的任务，没有就用最新完成的那个。

1. `selectedJobId` 设成这个任务。
2. `view` 设成 `report` 或 `sources`。
3. 看来源时，从 `sources.json` 读分数最高的 12 个写进 `sourcesPreview`，并把任务的 `updatedAt` 改成当前时间。文件不存在时（比如示例任务）保留现有的 `sourcesPreview`。
4. 看报告时，`reportPreview` 写报告开头约 1500 字。文件不存在时保留现有内容。

回复一句：哪份报告，多少来源，留下多少。

## 导出 PDF

只有 `completed` 的任务能导出，其他状态直接告诉用户还没有报告。

1. 确认 `app/jobs/<id>/report.md` 存在。示例任务没有这个文件：建目录，把 `reportPreview` 写成 `report.md`，并把任务的 `reportPath` 写好。
2. 轨 A 的任务且上游服务还在，先用上游生成：

   ```bash
   python3 "$HOME/skills/cr-research/scripts/upstream.py" pdf --job-dir app/jobs/<id>
   ```

   上游的 PDF 没有中文字体。报告里有英文以外的文字时，脚本会返回 `non_latin_report`，这时走下一步。

3. 其他情况用本地脚本。`HOME` 是这个 Bot 自己的目录：

   ```bash
   python3 "$HOME/skills/cr-report/scripts/export_pdf.py" --input app/jobs/<id>/report.md --output app/jobs/<id>/report.pdf --title "<公司> 尽调报告" --deps .cr-deps
   ```

   Windows PowerShell 用 `python "$env:HOME\skills\cr-report\scripts\export_pdf.py"`，后面的参数相同。

   返回 `missing_reportlab` 时，先安装到工作区，再运行一次。只安装这一次：

   ```bash
   python3 -m pip install --quiet --target .cr-deps reportlab
   ```

4. 成功时，任务写上 `pdfPath: "app/jobs/<id>/report.pdf"`，去掉 `pdfError`，`updatedAt` 改成当前时间，并用 `present` 把文件发给用户。
5. 失败时不要假装成功，也不要换别的办法反复试。把简短的原因写进任务的 `pdfError`，`updatedAt` 改成当前时间，告诉用户：
   - 没有 Python：要先安装 Python 3 才能导出 PDF，Markdown 报告不受影响。
   - pip 失败：多半是网络问题，可以稍后再试。

## 发到聊天渠道

用 `present` 发的文件和结果都回到当前会话。用户在 App 里要求“发到某个渠道”时直接说明：这里不能指定发到别的渠道；到那个渠道里对这个 Bot 说一声“把报告发给我”，就会发到那里。
