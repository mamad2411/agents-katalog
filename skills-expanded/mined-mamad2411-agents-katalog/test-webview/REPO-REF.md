# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-0xbb2b-bb-spec/test-webview/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 网页项目全量交互验证——Docker 整栈拉起→经浏览器 MCP（playwright/chrome-devtools）逐个跑完 webview 测试用例；每用例派隔离串行 subagent，主上下文只留 verdict 摘要；全程零并发；跑完无条件 docker compose down -v；失败转 /revise。触发：/test-webview、跑网页交互测试、端到端验证网页、webvie
