# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/m/model-config-check/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 校验模型配置是否正确、模型是否可以正常连接和返回内容。当用户说"检查模型"、"测试模型"、"模型能不能用"、"模型配置"、"诊断模型问题"时使用。**每次修改模型配置（config.patch/config.apply涉及models.providers）后必须自动执行校验。** 用户只给模型名+API key时，自动识别provider、查找配置、写入并校验。
