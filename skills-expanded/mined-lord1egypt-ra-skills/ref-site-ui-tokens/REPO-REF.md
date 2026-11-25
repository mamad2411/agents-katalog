# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/r/ref-site-ui-tokens/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 用户说「参考 X 网站改 UI / 照着 X 的风格做 / X 那种配色」时的落地流程。在没有浏览器的机器上（agent-browser、playwright 都没装，或 Chrome/Edge 不在标准路径）用 curl + 标准库 Python 抓下目标站的真实设计 token（颜色、圆角、字重、字号、间距），再据此改本地样式表。含一个可直接跑的抓取脚本 scripts/fetch_token
