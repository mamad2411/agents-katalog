# Repo Ref
- source: https://github.com/galact-byte/galact-skills (path: skills/hunt-prototype-pollution/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 在授权渗透测试中挖掘 JavaScript 原型污染（prototype pollution，服务端 Node.js 与客户端）。当目标把用户可控的键名递归合并进对象（merge/extend/set/clone、JSON body、query 解析）时使用——典型场景：用 `__proto__`/`constructor.prototype` 注入属性，污染全局原型，进而 DoS、改逻辑、配合 
