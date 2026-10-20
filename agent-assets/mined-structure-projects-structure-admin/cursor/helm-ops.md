---
description: |
triggers:
  - helm
  - helm 安装
  - helm 升级
  - helm 回滚
  - helm chart
  - helm install
  - helm upgrade
  - helm rollback
role: devops
priority: medium
category: deployment
stack: _common
alwaysApply: false
---


# Helm 使用

> 安全使用 helm 管理 K8s 应用。**生产写操作 MUST 用户确认**。

## 仓库管理

```bash
# 添加仓库
helm repo add <name> <url>

# 更新仓库
helm repo update

# 搜索 Chart
helm search repo <keyword>

# 查看 Chart 信息
helm show chart <repo>/<chart>
helm show values <repo>/<chart>
```

## 安装与升级

```bash
# 安装（指定 namespace + release 名 + 自定义 values）
helm install <release> <repo>/<chart> \
  -n <namespace> \
  -f values-prod.yaml \
  --set image.tag=1.2.0

# 升级
helm upgrade <release> <repo>/<chart> \
  -n <namespace> \
  -f values-prod.yaml \
  --set image.tag=1.2.1

# 安装或升级（推荐）
helm upgrade --install <release> <repo>/<chart> \
  -n <namespace> \
  -f values-prod.yaml

# 干跑（预览）
helm install <release> <repo>/<chart> --dry-run --debug
```

## 查看

```bash
# 查看 release 列表
helm list
helm list -n <namespace>

# 查看 release 详情
helm status <release>
helm get values <release>
helm get manifest <release>

# 查看历史
helm history <release>
```

## 回滚

```bash
# 回滚到上一版（MUST 用户确认）
helm rollback <release>

# 回滚到指定版本
helm rollback <release> <revision>
```

## 卸载

```bash
# 卸载 release（MUST 用户确认）
helm uninstall <release> -n <namespace>
```

## Chart 编写

### 生态 Chart 结构（双 workload 模板）

```
structure-<X>-center/
├── Chart.yaml
├── values.yaml
├── .helmignore
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml      # 双 workload（backend + frontend）
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   ├── serviceaccount.yaml
│   ├── NOTES.txt
│   └── tests/
│       └── test-connection.yaml
```

### values.yaml 关键约定

```yaml
# 后端
backend:
  enabled: true
  name: user-service
  image:
    repository: registry.cn-hangzhou.aliyuncs.com/structured/user-service
    tag: "1.2.0"
    pullPolicy: Always
  service:
    type: ClusterIP
    port: 8080
  env:
    APP_PATH: /app/boot/app.jar
    JAVA_OPTS: -Xms256m -Xmx1024m
    PARAMS: -Dspring.profiles.active=pro
  replicaCount: 1

# 前端
frontend:
  enabled: true
  name: user-ui
  image:
    repository: registry.cn-hangzhou.aliyuncs.com/structured/user-ui
    tag: "1.2.0"
  service:
    port: 80
  env:
    SCHEME: https
    SERVER_HOST: api.prod.structured.cn
    SERVER_PORT: "443"

# HPA
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 3
  targetCPUUtilizationPercentage: 80

# Ingress
ingress:
  enabled: false
  className: ""
  hosts: []
```

### 双 workload 渲染技巧

`templates/deployment.yaml` 用 `range` 渲染 backend + frontend：

```yaml
{{- range $key, $svc := dict "backend" .Values.backend "frontend" .Values.frontend }}
{{- if $svc.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ $svc.name }}
spec:
  replicas: {{ $svc.replicaCount }}
  selector:
    matchLabels:
      app.service: {{ $svc.name }}
  template:
    metadata:
      labels:
        app.service: {{ $svc.name }}
    spec:
      containers:
      - name: {{ $svc.name }}
        image: "{{ $svc.image.repository }}:{{ $svc.image.tag }}"
        # ...
{{- end }}
{{- end }}
```

## Chart 调试

```bash
# 模板渲染（不写集群）
helm template <release> ./<chart-dir> -f values.yaml

# 模板渲染 + 指定 namespace
helm template <release> ./<chart-dir> -n <ns> -f values.yaml

# 校验 Chart
helm lint ./<chart-dir>

# 打包 Chart
helm package ./<chart-dir>
```

## 关键约束

- ✅ **MUST** 用 `helm upgrade --install`（幂等）
- ✅ **MUST** 用 `-n <namespace>` 显式指定命名空间
- ✅ **MUST** 生产环境用 `--dry-run --debug` 预览
- ✅ **MUST** 用 `-f values-<env>.yaml` 区分环境
- ❌ **MUST NOT** 在 values.yaml 硬编码 Secrets（用 External Secrets / Sealed Secrets）
- ❌ **MUST NOT** 用 `latest` tag

## 关联

- Wiki：`wiki/_common/kubernetes.md` `wiki/_common/docker.md`
- 相关：`kubectl-ops` / `k8s-deployment` / `docker-cli`
