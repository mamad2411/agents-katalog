# Repo Ref
- source: https://github.com/onescience-ai/oneskills (path: skills/onescience-live-literature/SKILL.md, branch: master)
- mined: 2026-11-23
- desc: OneScience 实时文献两级检索推理技能（对齐 Biomni 的 LiteratureSearch/Fetch 工具链），领域无关的通用流程。第一级按相关性实时检索 OpenAlex 拿论文摘要、建全局编号引用池并迭代精炼检索词；第二级对选中的开放获取论文经 Europe PMC/PMC 结构化 API 取全文细节；最终输出分层深度推理答案，References 按正文出现顺序连续编号。触发
