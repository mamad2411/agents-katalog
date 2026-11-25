# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: analysis/check-review-alignment/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 当用户明确要求"核查/优化综述 `{主题}_review.tex` 的正文引用"或"运行 check-review-alignment"时使用。通过宿主 AI 的语义理解逐条核查引用是否与文献内容吻合，只在发现致命性引用错误时对"包含引用的句子"做最小化改写，并复用 `systematic-literature-review` 的渲染脚本输出 PDF/Word。核心原则：不为了改而改，无法确定是否
