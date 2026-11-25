# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/d/data-pipeline-field-drift/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当数据流水线里某个字段「一直读不到」、某类条目静默消失、或下游把「有数据」当成「没数据」时，用契约名比对法定位字段名漂移（同一逻辑字段在采集/暂存/落盘/读取四处各有一个名字），并写「契约名回归测试」钉死。含 grep 排查模板、死变量识别、回填对账顺序。当用户说「这个字段怎么一直是空的」「数据明明有却读不到」「回填没效果」「某类记录莫名不见了」时使用。
