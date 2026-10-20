---
description: |
triggers:
  - kubectl
  - k8s
  - k8s 操作
  - 查看 pod
  - pod 日志
  - k8s 部署
  - kubectl apply
  - kubectl get
  - kubectl logs
role: devops
priority: medium
category: deployment
stack: _common
alwaysApply: false
---


# kubectl 使用

> 安全使用 kubectl 操作 K8s 集群。**生产写操作 MUST 用户确认**。

## 上下文与命名空间

```bash
# 查看当前上下文
kubectl config current-context

# 切换上下文（MUST 用户确认）
kubectl config use-context <context>

# 切换命名空间
kubectl config set-context --current --namespace=<ns>

# 临时指定命名空间（推荐）
kubectl -n <ns> get pods
```

## 查看操作（只读，安全）

```bash
# 查看 Pod
kubectl get pods
kubectl get pods -n <ns>
kubectl get pods -o wide           # 含节点
kubectl get pods --watch           # 监听变化

# 查看 Deployment
kubectl get deployment
kubectl describe deployment <name>

# 查看 Service
kubectl get svc
kubectl describe svc <name>

# 查看 Ingress
kubectl get ingress

# 查看所有资源
kubectl get all

# 查看事件（定位问题）
kubectl get events --sort-by='.lastTimestamp'
```

## 日志与调试

```bash
# 查看日志
kubectl logs <pod>
kubectl logs -f <pod>              # 跟随
kubectl logs --tail=100 <pod>      # 最后 100 行
kubectl logs <pod> -c <container>  # 多容器 Pod
kubectl logs <pod> --previous      # 上次崩溃前日志

# 进入容器
kubectl exec -it <pod> -- /bin/sh
kubectl exec -it <pod> -c <container> -- /bin/sh

# 端口转发（本地访问集群内服务）
kubectl port-forward pod/<pod> 8080:8080
kubectl port-forward svc/<svc> 8080:80
```

## 部署操作（写，MUST 确认）

```bash
# 应用 manifest
kubectl apply -f deployment.yaml

# 应用整个目录
kubectl apply -f ./k8s/

# 查看 diff（先预览再应用）
kubectl diff -f deployment.yaml

# 删除资源（MUST 用户确认）
kubectl delete -f deployment.yaml
kubectl delete pod <pod>
kubectl delete deployment <name>
```

## 滚动更新与回滚

```bash
# 查看滚动更新状态
kubectl rollout status deployment/<name>

# 查看历史
kubectl rollout history deployment/<name>

# 回滚到上一版
kubectl rollout undo deployment/<name>

# 回滚到指定版本
kubectl rollout undo deployment/<name> --to-revision=<n>

# 重启 Deployment（拉新镜像）
kubectl rollout restart deployment/<name>
```

## 扩缩容

```bash
# 手动扩缩容
kubectl scale deployment/<name> --replicas=3

# 自动扩缩容（HPA）
kubectl autoscale deployment/<name> --min=1 --max=5 --cpu-percent=80
kubectl get hpa
```

## 配置与密钥

```bash
# 查看 ConfigMap
kubectl get configmap
kubectl describe configmap <name>

# 查看 Secret（base64 编码）
kubectl get secret
kubectl get secret <name> -o yaml

# 解码 Secret
kubectl get secret <name> -o jsonpath='{.data.password}' | base64 -d
```

## 节点与集群

```bash
# 查看节点
kubectl get nodes
kubectl describe node <node>

# 查看资源使用
kubectl top nodes
kubectl top pods

# 标记节点不可调度（维护时）
kubectl cordon <node>

# 驱逐节点上的 Pod
kubectl drain <node> --ignore-daemonsets

# 恢复调度
kubectl uncordon <node>
```

## 关键约束

- ✅ **MUST** 用 `-n <ns>` 显式指定命名空间
- ✅ **MUST** 写操作前 `kubectl diff` 预览
- ✅ **MUST** 生产环境写操作前用户确认
- ❌ **MUST NOT** 在生产 `default` namespace 操作
- ❌ **MUST NOT** 直接 `kubectl delete` 不带确认

## 常见问题

### Pod 一直 Pending

```bash
kubectl describe pod <pod>  # 看 Events
# 常见原因：资源不足 / 镜像拉取失败 / 调度限制
```

### Pod 频繁重启

```bash
kubectl logs <pod> --previous  # 看上次崩溃日志
kubectl describe pod <pod>     # 看重启原因
```

### Service 不通

```bash
kubectl get svc <name>
kubectl describe svc <name>
kubectl get endpoints <name>  # 看后端 Pod
```

## 关联

- Wiki：`wiki/_common/kubernetes.md`
- 相关：`helm-ops` / `k8s-deployment` / `docker-cli`
