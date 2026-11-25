# Repo Ref
- source: https://github.com/meari-prototype/iftree-editor (path: .iftree-llm-workspace/skills/smart-import/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 把任意源文件整理成条件树文档并入库。适用于内置 agent、外部 LLM 或任何能跑脚本的工具执行导入任务：观察源文样本、写一次性切割脚本产出与 db push 同契约的 JSON，经 db import-json 校验入库。正文必须是源文的逐字节切片——LLM 只贡献结构，不贡献正文。
