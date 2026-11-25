# Repo Ref
- source: https://github.com/dangjian/faststudy-knowledge (path: tools/skills/kg-query/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 查中小学教材知识库（8,282 概念 / 99 册 / 10 学科）。入口是 graph/index.md 的「问句→路径」表；LLM 逐层下钻 Textbook→Chapter→Section→Concept，只读命中的 YAML 切片；kg_ask.ts 仅用于 ID 发现、先修闭包与关系切片。当用户问某个知识点是什么、在教材哪一节、先修是什么、和别的概念什么关系时使用。
