# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-0xbb2b-bb-spec/config-constraints/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 后端配置载体三分——env/secret 装启动必需且不热更、yaml/configmap 装可热更且有默认值、DB+API 装业务方可改的动态配置；核心凭据默认只能 secret/KMS，下沉 DB 必须 envelope encryption；热更失败保留旧值 + 告警禁崩溃。触发：设计/实现配置加载、密钥存储、热更机制、新增 env/yaml/DB 配置项、k8s secret/config
