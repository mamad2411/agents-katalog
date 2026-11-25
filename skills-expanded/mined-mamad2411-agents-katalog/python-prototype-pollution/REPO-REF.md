# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-wgpsec-AboutSecurity/python-prototype-pollution/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Python 原型链污染（属性注入/Class Pollution）检测与利用。当目标为 Python Web 应用（Flask/Sanic/Django/FastAPI）且存在递归合并(merge)、深度属性设置(pydash.set_)、JSON 配置更新接口时使用。覆盖污染入口识别、__globals__链构造、Flask SECRET_KEY/Jinja2定界符/searchpath污染、
