---
name: implementing-privileged-identity-management-with-azure
description: 使用 Microsoft Graph API 配置 Azure AD 特权身份管理（PIM），管理符合条件的角色分配、即时激活、访问审查，以及用于零信任特权访问的角色管理策略。
domain: cybersecurity
subdomain: identity-access-management
tags: [Azure-AD, PIM, privileged-access, just-in-time, eligible-roles, Microsoft-Graph, zero-trust, access-reviews, Entra-ID]
version: "1.0"
author: mahipal
license: Apache-2.0
---

# 使用 Azure 实施特权身份管理

## 概述

Azure AD 特权身份管理（PIM）通过将永久角色分配转换为需要激活的符合条件分配，来强制执行即时特权访问。本技能使用 Microsoft Graph API 枚举活跃和符合条件的角色分配、创建资格计划请求、配置角色管理策略（MFA 要求、审批工作流、最大激活时长）、审计 PIM 激活日志，以及识别应转换为符合条件分配的过度授权永久分配。

## 前提条件

- Python 3.9+ 并安装 `msal`、`requests`
- 具有 `RoleManagement.ReadWrite.Directory`、`RoleEligibilitySchedule.ReadWrite.Directory` 权限的 Azure AD 应用注册
- Microsoft Entra ID P2 或 Microsoft Entra ID Governance 许可证

## 关键操作

1. **列出符合条件的分配** — GET /roleManagement/directory/roleEligibilityScheduleInstances
2. **创建资格请求** — POST /roleManagement/directory/roleEligibilityScheduleRequests
3. **激活符合条件的角色** — POST /roleManagement/directory/roleAssignmentScheduleRequests（action=selfActivate）
4. **审计角色激活** — GET /auditLogs/directoryAudits（按 PIM 活动过滤）
5. **审查角色策略** — GET /policies/roleManagementPolicies（检查 MFA/审批要求）

## 输出

包含永久与符合条件分配数量、过度授权账户、策略合规状态和最近激活历史的 JSON 审计报告。
