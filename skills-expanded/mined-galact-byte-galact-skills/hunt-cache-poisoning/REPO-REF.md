# Repo Ref
- source: https://github.com/galact-byte/galact-skills (path: skills/hunt-cache-poisoning/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 在授权渗透测试中挖掘 Web 缓存投毒与缓存欺骗（web cache poisoning / cache deception）。当目标前有缓存层（CDN/反代/Varnish）且缓存键未覆盖某些影响响应的输入（unkeyed header/参数/解析差异）时使用——典型场景：X-Forwarded-Host 反射进响应被缓存、unkeyed 参数、缓存键规范化差异、静态扩展名欺骗缓存私有页。适用目
