# Repo Ref
- source: https://github.com/dangjian/faststudy-knowledge (path: tools/skills/kg-ingest/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 知识库摄入编排器。两条入口：纸质教材走 OCR 全管线（init→ocr→polish→repair→format→sync→extract→ingest→verify→build）；已成 md 的素材（含 EXT- 扩展知识）走注入管线 propose→apply→extract→ingest→build。源数据目录由 `KG_SOURCE_DIR` 指定（默认仓内 `source_data/`
