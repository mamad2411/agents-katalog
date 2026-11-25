# Repo Ref
- source: https://github.com/yehuzi2026/workbuddy-skills-hub (path: categories/02-document-processing/offline-office-extract/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 纯离线文档抽取（零依赖安装）。当沙箱/环境无法安装 pywin32、pymupdf、markitdown、RapidOCR 等第三方库（pip 经代理下载超时、无 LibreOffice/WPS）时，仅用 Python 标准库抽取 .doc(Word97-2003)、.docx、.pdf 的文本与内嵌/扫描图片，再用多模态 Read 直接识别图片内容（代替 OCR）。适用于读取招标文件/标书/扫描
