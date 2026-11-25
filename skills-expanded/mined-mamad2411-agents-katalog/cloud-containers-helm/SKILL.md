---
name: cloud-containers-helm
description: "apiVersion: rbac.authorization.k8s.io/v1 kind: RoleBinding metadata:   namespace: production subjects:   - kind: ServiceAccount     namespace: production roleRef:   kind: Role   apiGroup: rbac."
domain: cybersecurity
---

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: production
subjects:
  - kind: ServiceAccount
    namespace: production
roleRef:
  kind: Role
  apiGroup: rbac.authorization.k8s.io
```

## CI/CD Helm Security Pipeline

```yaml
# .github/workflows/helm-security.yaml
on:
  pull_request:
    paths: ['charts/**']

jobs:
  lint-and-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Helm lint
        run: helm lint ./charts/mychart --strict

      - name: Render plugins
        run: helm template test ./charts/mychart -f charts/mychart/values.yaml > rendered.yaml

      - name: Scan with kube-linter
        uses: stackrox/kube-linter-action@v1
        with:
          directory: rendered.yaml

      - name: Scan with trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: config
          scan-ref: rendered.yaml

      - name: Scan with checkov
        uses: bridgecrewio/checkov-action@master
        with:
          file: rendered.yaml
          framework: kubernetes
```

## Best Practices

1. **Sign charts** with GPG and verify before installation
2. **Render and scan** templates before deploying to catch misconfigurations
3. **Enforce security contexts** in values.yaml defaults
4. **Never store secrets** in Helm values - use external secrets or helm-secrets plugin
5. **Use image digests** instead of tags for immutable references
6. **Restrict Helm RBAC** to least privilege per namespace
7. **Pin chart versions** in requirements - never use `latest`
8. **Lint strictly** in CI with `--strict` flag
9. **Review third-party charts** before deploying to production
10. **Use Helm test hooks** to validate deployments post-install
