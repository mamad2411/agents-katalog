# Repo Ref
- source: https://github.com/galact-byte/galact-skills (path: skills/hunt-ssrf/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 在授权渗透测试中系统性挖掘服务端请求伪造（SSRF）。当目标存在"服务端按用户可控的 URL/主机/地址发起出站请求"的功能——如 URL 预览、图片/视频抓取、Webhook、集成回调、导入远程资源、PDF/截图渲染、代理转发——需要判定是否可绕过 SSRF 防护访问内网/云元数据/受限服务时使用。适用目标类型 REST API / Web 应用。触发场景包括用户说"测下这个 URL 抓取有没有
