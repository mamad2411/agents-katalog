# Repo Ref
- source: https://github.com/wgpsec/AboutSecurity (path: skills/cloud/k8s-webhook-abuse/SKILL.md, branch: master)
- mined: 2026-10-14
- desc: Kubernetes Admission Webhook 滥用与策略引擎利用。当集群存在 Kyverno/OPA Gatekeeper/自定义 Webhook、DNS 扫描发现 kyverno-svc 或 gatekeeper 服务、或需要从 Mutating Webhook 提取注入的 Secret 时使用。核心手法：伪造 AdmissionReview 请求。任何在 K8s 中发现 Webho
