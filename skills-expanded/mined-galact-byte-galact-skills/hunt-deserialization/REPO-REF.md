# Repo Ref
- source: https://github.com/galact-byte/galact-skills (path: skills/hunt-deserialization/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 在授权渗透测试中挖掘不安全反序列化（insecure deserialization）。当目标把用户可控数据交给 unserialize/Marshal/pickle/ObjectInputStream/BinaryFormatter/YAML.load 等还原成对象时使用——典型场景：cookie/token/viewstate/隐藏字段里出现序列化数据、导入文件触发对象还原、想借 gadget
