# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/m/meituan-paotui/references/meituan-passport-user-auth/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 美团 Passport 用户授权登录 Skill。通过 pt-passport CLI 获取授权链接，展示给用户完成确认后轮询拿到鉴权凭证。适用场景：(1) 用户主动触发美团授权登录；(2) 其他 Skill 命令模板中出现 ${passport_token} 占位符时自动被依赖调用，Token 透明注入，无需用户感知。不适用于服务端 AppKey/Secret 鉴权或非美团系统授权。触发词：美团
