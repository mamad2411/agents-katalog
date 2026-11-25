# Repo Ref
- source: https://github.com/galact-byte/galact-skills (path: skills/hunt-open-redirect/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 在授权渗透测试中挖掘开放重定向（open redirect）及其危害升级。当目标按用户可控参数做跳转（登录后 next、SSO returnUrl、注销、短链、回调）时使用——典型场景：绕过 URL 白名单跳到外站钓鱼、泄露 token/Referer、开放重定向作为 SSRF/OAuth token 窃取的跳板。适用目标类型 Web / REST API / SSO。触发场景包括用户说"测下开放
