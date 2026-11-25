# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/s/siliconflow-ocr/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 使用 SiliconFlow API（OpenAI 兼容接口）做图片/PDF 文字识别。默认走 PaddleOCR-VL-1.5（文档 OCR SOTA，速度比 Qwen3-VL 快 40%、表格公式更强）。支持本地路径或 URL、单页/批量并发、坐标 token 清洗。密钥通过 OpenClaw secret-egress-proxy 注入，需保留 `requests`+网关 proxy。
