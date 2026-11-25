# Repo Ref
- source: https://github.com/waterbili/perimeterx_re (path: node_bridge/skill/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 用 jsdom + 11 个 env 补环境模块 + Python curl_cffi 协调器，给反爬 SDK（如 PerimeterX / Akamai / 类似厂商）做"补环境"路线的 fallback bridge，不依赖真浏览器。触发场景：(1) 纯算 generator 因 SDK 升级暂时跑不通，需要 Plan B 救火；(2) 新站点 spike — 30 分钟跑通后再决定是否值得做
