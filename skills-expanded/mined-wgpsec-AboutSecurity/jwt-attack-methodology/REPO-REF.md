# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/exploit/auth/jwt-attack-methodology/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: JWT Token 攻击方法论。当响应头/Cookie 中出现 eyJ 开头的字符串（三段式 base64，Header.Payload.Signature）、Authorization: Bearer token、API 返回 token/access_token 字段时使用。包含 alg:none 绕过、弱密钥爆破（hashcat/john/c-jwt-cracker/jwt_tool 完整工
