---
name: implementing-rbac-for-kubernetes-cluster
description: 配置 Kubernetes 基于角色的访问控制（RBAC），对集群资源强制执行最小权限访问。涵盖 Role/ClusterRole 设计、RoleBinding 配置、服务账户安全、命名空间隔离，以及多租户 Kubernetes 环境的审计日志。
domain: cybersecurity
subdomain: identity-access-management
tags: [iam, identity, access-control, authorization, rbac, kubernetes, k8s]
version: "1.0"
author: mahipal
license: Apache-2.0
---
# 为 Kubernetes 集群实施 RBAC

## 概述
配置 Kubernetes 基于角色的访问控制（RBAC），对集群资源强制执行最小权限访问。涵盖 Role/ClusterRole 设计、RoleBinding 配置、服务账户安全、命名空间隔离，以及多租户 Kubernetes 环境的审计日志。

## 目标
- 为多租户集群设计 RBAC 角色层次结构
- 为不同人员创建细粒度的 Role 和 ClusterRole
- 按最小权限原则配置 RoleBinding 和 ClusterRoleBinding
- 保护服务账户并限制其默认权限
- 将 RBAC 与外部身份提供商（OIDC）集成
- 使用 Kubernetes 审计日志审计和监控 RBAC 使用情况

## 关键概念

### RBAC API 对象
1. **Role**：命名空间范围的权限（命名空间内的 pods、services、deployments）
2. **ClusterRole**：集群范围的权限（nodes、namespaces、PVs、CRDs）
3. **RoleBinding**：在命名空间内将 Role 授予用户/组/服务账户
4. **ClusterRoleBinding**：在集群范围内授予 ClusterRole

### Kubernetes RBAC 动词
- `get`、`list`、`watch`：只读操作
- `create`、`update`、`patch`：写操作
- `delete`、`deletecollection`：破坏性操作
- `impersonate`：模拟其他用户身份
- `escalate`：修改 RBAC 角色（高度特权）
- `bind`：创建 RoleBinding（高度特权）

### 基于人员的访问模型
- **集群管理员**：完整的集群管理权限（限制 2-3 人）
- **命名空间管理员**：在分配的命名空间内完整控制
- **开发者**：在分配的命名空间内部署和管理工作负载
- **只读用户**：对命名空间资源的只读访问
- **CI/CD 服务账户**：部署工作负载，管理 configmaps/secrets

## 实施步骤

### 第 1 步：禁用默认宽松设置
1. 确保 API 服务器启用 `--authorization-mode=RBAC`
2. 移除非管理员用户的默认 cluster-admin 绑定
3. 禁用 pods 中服务账户令牌的自动挂载
4. 限制每个命名空间中默认服务账户的访问权限

### 第 2 步：创建自定义角色
```yaml
# 开发者角色 - 命名空间范围
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: app-team
  name: developer
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["pods", "deployments", "services", "configmaps", "jobs"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]  # 可读取但限制创建/更新
- apiGroups: [""]
  resources: ["pods/log", "pods/exec"]
  verbs: ["get", "create"]
```

### 第 3 步：将角色绑定到用户/组
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: app-team
subjects:
- kind: Group
  name: "dev-team"
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

### 第 4 步：保护服务账户
- 为每个应用创建专用服务账户
- 为不需要 API 访问的 pods 禁用 automountServiceAccountToken
- 使用带受众和有效期的投影服务账户令牌
- 为每个服务账户绑定最小所需权限

### 第 5 步：OIDC 集成
1. 使用 OIDC 标志配置 API 服务器（issuer-url、client-id、username-claim、groups-claim）
2. 在 RoleBinding 中将 OIDC 组映射到 Kubernetes 组
3. 使用来自 OIDC 提供商的短期令牌
4. 使用 OIDC 认证插件配置 kubectl

### 第 6 步：审计与监控
- 启用 Kubernetes 审计日志（audit-policy.yaml）
- 记录所有 RBAC 相关事件（角色创建、绑定变更）
- 对 ClusterRoleBinding 的创建/修改发出告警
- 监控权限升级尝试
- 定期审查具有 cluster-admin 访问权限的用户

## 安全控制
| 控制项 | NIST 800-53 | 描述 |
|---------|-------------|------|
| 访问控制 | AC-3 | RBAC 强制执行 |
| 最小权限 | AC-6 | 最小必要 Kubernetes 权限 |
| 账户管理 | AC-2 | 服务账户生命周期 |
| 审计 | AU-3 | Kubernetes 审计日志 |
| 职责分离 | AC-5 | 命名空间隔离 |

## 常见误区
- 向 CI/CD 管道授予 cluster-admin 权限
- 在 ClusterRole 中使用通配符（*）动词或资源
- 未限制 pods/exec（允许容器 shell 访问）
- 保留具有广泛权限的默认服务账户
- 未审计谁可以创建 RoleBinding（权限升级向量）

## 验证清单
- [ ] 所有用户通过 OIDC 认证（无静态令牌/证书）
- [ ] 无不必要的 ClusterRoleBinding 绑定到 cluster-admin
- [ ] 开发者仅限于其分配的命名空间
- [ ] 服务账户使用最小权限角色
- [ ] 默认禁用 automountServiceAccountToken
- [ ] 审计日志记录 RBAC 变更
- [ ] `kubectl auth can-i` 验证每个人员的预期权限
