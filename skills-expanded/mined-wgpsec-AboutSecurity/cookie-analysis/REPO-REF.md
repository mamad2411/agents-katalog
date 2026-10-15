# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/exploit/auth/cookie-analysis/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: Session cookie 分析与伪造方法论。当发现 Web 应用使用 cookie 进行认证、需要判断 cookie 类型并选择伪造方法时使用。覆盖 unsigned base64 cookie 直接伪造、Flask 签名 cookie（flask-unsign 爆破密钥）、加密/二进制 cookie 的识别。本技能负责 cookie 类型判断和分流：如果判断为 JWT（三段式 eyJ 开头）
