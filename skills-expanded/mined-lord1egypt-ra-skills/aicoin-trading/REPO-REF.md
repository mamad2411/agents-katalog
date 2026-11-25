# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/skills_sh/s/skills-sh_aicoincom_coinos-skills_aicoin-trading/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: **CEX 中心化交易所**(Binance / OKX / Bybit / Bitget 等)的下单交易工具。严格规则:(1) 所有订单必须通过 node scripts/exchange.mjs create_order 执行,禁止写自定义代码下单 (2) create_order 分两步:第一次返回预览,展示给用户等确认,用户说确认后第二次加 confirmed=true 执行 (3) 禁止
