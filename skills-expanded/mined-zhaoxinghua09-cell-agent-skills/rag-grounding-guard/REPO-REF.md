# Repo Ref
- source: https://github.com/zhaoxinghua09-cell/agent-skills (path: skills/rag-grounding-guard/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当用户说『RAG回答胡说八道/编造』『引用对不对』『回答有依据吗』『检索到的资料支撑不了结论』，或要给 RAG/检索增强回答做事实校验时使用。校验每条声明在检索来源里是否有支撑（ grounding 覆盖率），未覆盖的声明标红为幻觉风险，并要求来源带出处（有籍）。可运行脚本（grounding_check 校验器）。理论根基：LGD 三律之有籍(引用溯源)+有证(防幻觉可核验)。触发词：RAG校验
