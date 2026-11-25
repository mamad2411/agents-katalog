---
name: performing-cloud-penetration-testing
description: >
  对 AWS、Azure 和 GCP 云环境执行授权渗透测试，识别 IAM 错误配置、暴露的存储桶、过度宽松的安全组、
  无服务器函数漏洞以及从初始访问到账户沦陷的云特定攻击路径。测试人员使用云原生工具及 Pacu、
  ScoutSuite 等专用框架枚举并利用云基础设施。适用于云渗透测试、AWS 安全评估、Azure 渗透测试
  或云基础设施安全测试等请求场景。
domain: cybersecurity
subdomain: penetration-testing
tags: [cloud-pentest, AWS-security, Azure-security, IAM-exploitation, cloud-infrastructure]
version: 1.0.0
author: mahipal
license: Apache-2.0
---
# 执行云渗透测试

## 使用场景

- 在从本地迁移到云环境前后评估云基础设施的安全态势
- 测试 IAM 策略、安全组和网络 ACL 是否存在过度宽松的配置
- 评估无服务器架构（Lambda、Azure Functions、Cloud Functions）的安全性
- 识别包含敏感数据的暴露云存储（S3 存储桶、Azure Blob 容器、GCS 存储桶）
- 测试云安全控制的有效性（GuardDuty、Defender for Cloud、Security Command Center）

**不适用场景**：未同时获得云账户所有者书面授权以及遵守云服务商渗透测试政策（AWS 大多数服务无需事先审批；Azure 和 GCP 某些测试类型需提前通知或审批）。

## 前置条件

- 书面授权，指定目标云账户、区域和在测试范围内的服务
- 遵守云服务商渗透测试政策（AWS 渗透测试政策、Azure 渗透测试规则、GCP 可接受使用政策）
- 不同权限级别的云凭据（只读、开发者、管理员），用于测试授权边界
- 已安装 Pacu（AWS）、PowerZure（Azure）或 GCP 专用利用框架
- 已安装 ScoutSuite 或 Prowler，用于自动化云安全态势评估
- 已配置测试凭据的 AWS CLI、Azure CLI 和/或 gcloud CLI

## 工作流程

### 步骤一：云侦察与枚举

枚举云环境以映射攻击面：

**AWS 枚举：**
- `aws sts get-caller-identity` — 验证当前身份和账户
- `aws iam list-users` — 列出所有 IAM 用户
- `aws iam list-roles` — 列出所有 IAM 角色及其信任策略
- `aws s3 ls` — 列出所有 S3 存储桶
- `aws ec2 describe-instances --region us-east-1` — 列出 EC2 实例
- `aws lambda list-functions` — 列出 Lambda 函数
- `aws rds describe-db-instances` — 列出 RDS 数据库
- 使用 Pacu 进行自动化枚举：`run iam__enum_permissions`、`run iam__enum_users_roles_policies_groups`

**Azure 枚举：**
- `az account list` — 列出订阅
- `az ad user list` — 列出 Azure AD 用户
- `az vm list` — 列出虚拟机
- `az storage account list` — 列出存储账户
- `az keyvault list` — 列出密钥保管库
- `az webapp list` — 列出 Web 应用程序

**跨云：**
- 运行 ScoutSuite 进行全面态势评估：`scout aws --profile <profile>` 或 `scout azure --cli`
- 运行 Prowler 进行 AWS CIS 基准合规检查：`prowler aws`

### 步骤二：IAM 与身份利用

测试 IAM 策略的权限提升路径：

**AWS IAM 提权：**
- 检查过度宽松的策略：`aws iam get-user-policy`、`aws iam list-attached-user-policies`
- 测试已知 IAM 提权路径：
  - `iam:CreatePolicyVersion` — 创建授予管理员访问权限的新策略版本
  - `iam:SetDefaultPolicyVersion` — 将旧版、更宽松的策略版本设为默认
  - `iam:PassRole` + `lambda:CreateFunction` + `lambda:InvokeFunction` — 创建带高权限角色的 Lambda
  - `iam:AttachUserPolicy` — 为当前用户附加 AdministratorAccess 策略
  - `sts:AssumeRole` — 若信任策略允许则担任更高权限角色
- 使用 Pacu 进行自动化提权扫描：`run iam__privesc_scan`

**Azure 身份提权：**
- 枚举角色分配：`az role assignment list --assignee <user>`
- 检查订阅级别的 Contributor/Owner 角色
- 通过应用注册、服务主体和托管身份测试 Azure AD 权限提升
- 检查 Azure AD 中的全局管理员分配

### 步骤三：存储与数据暴露

测试云存储服务的数据暴露情况：

- **S3 存储桶安全**：对每个存储桶测试：
  - 公共访问：`aws s3 ls s3://<bucket> --no-sign-request`
  - ACL 错误配置：`aws s3api get-bucket-acl --bucket <bucket>`
  - 存储桶策略：`aws s3api get-bucket-policy --bucket <bucket>`
  - 版本控制（访问已删除数据）：`aws s3api list-object-versions --bucket <bucket>`
- **Azure Blob 暴露**：测试公共容器访问和共享访问签名（SAS）令牌泄露
- **存储中的密钥**：在存储内容中搜索凭据、API 密钥、数据库连接字符串和 PII
- **数据库暴露**：检查具有公共端点、默认凭据或安全组允许 0.0.0.0/0 访问的 RDS/Azure SQL 实例

### 步骤四：计算与无服务器利用

测试计算资源的漏洞：

- **EC2 实例元数据**：从已入侵实例查询 `http://169.254.169.254/latest/meta-data/iam/security-credentials/` 以提取 IAM 角色凭据
- **IMDSv1 利用**：测试是否强制使用 IMDSv2。IMDSv1 易受基于 SSRF 的凭据窃取攻击
- **Lambda 函数分析**：下载 Lambda 函数代码（`aws lambda get-function --function-name <name>`）并检查硬编码凭据、不安全依赖和注入漏洞
- **容器安全**：测试 ECS/EKS 的 Pod 级权限提升、容器逃逸和服务账户令牌滥用
- **用户数据脚本**：`aws ec2 describe-instance-attribute --instance-id <id> --attribute userData` 查找启动脚本中的凭据

### 步骤五：网络与安全组评估

测试网络控制的错误配置：

- **安全组分析**：识别允许 0.0.0.0/0 入站访问敏感端口（SSH/22、RDP/3389、数据库端口）的安全组
- **VPC 流日志**：检查是否启用 VPC 流日志以具备取证能力
- **跨账户访问**：测试是否存在允许其他 AWS 账户访问的过度宽松资源策略
- **VPC 对等**：识别 VPC 对等连接并测试对等 VPC 是否可访问敏感资源
- **VPN 和直连**：识别混合连接并测试云到本地的访问控制是否被执行

## 核心概念

| 术语 | 定义 |
|------|------------|
| **IAM 权限提升** | 利用过度宽松的 IAM 策略将有限访问权限提升至对云账户的管理控制权 |
| **实例元数据服务（IMDS）** | 云实例上提供实例配置和 IAM 角色凭据的 HTTP 端点（169.254.169.254），可通过 SSRF 被利用 |
| **角色担任（Assumed Role）** | 用户或服务临时担任的 IAM 角色，以获取其权限；受信任策略约束，定义谁可以担任该角色 |
| **SCP（服务控制策略）** | AWS Organizations 中的组织级策略，为账户设置权限边界，覆盖 IAM 策略 |
| **托管身份（Managed Identity）** | Azure 中相当于 AWS IAM 角色的服务机制，为 Azure 资源提供自动凭据管理 |
| **资源策略** | 附加到云资源（S3 存储桶、Lambda 函数、SQS 队列）的访问控制策略，定义跨账户和公共访问 |

## 工具与系统

- **Pacu**：开源 AWS 利用框架，支持 IAM 枚举、权限提升、数据外泄和持久化
- **ScoutSuite**：多云安全审计工具，根据安全最佳实践评估 AWS、Azure、GCP 和 Oracle Cloud 的安全态势
- **Prowler**：AWS 和 Azure 安全评估工具，覆盖 CIS 基准、PCI-DSS、HIPAA 和 GDPR 合规检查
- **CloudFox**：通过分析 IAM 角色、权限和信任关系识别云基础设施中可利用攻击路径的工具
- **Steampipe**：基于 SQL 的云基础设施查询引擎，支持跨云服务商 API 的复杂查询

## 常见场景

### 场景：SaaS 公司的 AWS 云渗透测试

**背景**：一家 SaaS 公司的整个平台部署在 3 个 AWS 账户（生产、预发布、开发）。测试人员获得了开发账户中的只读 IAM 凭据。目标是确定开发账户是否可用于横向移动至生产账户。

**方法**：
1. 使用 Pacu 枚举开发账户：发现 45 个 Lambda 函数、12 个 EC2 实例、8 个 S3 存储桶和 23 个 IAM 角色
2. 发现开发者角色可以调用 Lambda 函数；某个 Lambda 函数拥有具备 S3 完全访问权限和 STS 担任角色权限的角色
3. 修改 Lambda 函数代码以担任生产账户中的跨账户角色（信任策略允许 Lambda 角色进行此操作）
4. 从已担任的生产角色枚举 S3 存储桶，在未加密的存储桶中发现客户数据
5. 发现生产 EC2 实例使用 IMDSv1，结合 Web 应用中的 SSRF 漏洞可能导致凭据窃取
6. 记录从开发只读权限到生产数据访问的完整攻击路径

**常见陷阱**：
- 未检查云服务商的渗透测试政策，意外触发自动化滥用检测
- 仅关注 IaaS（EC2、虚拟机），而忽略了包含最多敏感数据的无服务器函数、托管服务和存储
- 遗漏了跨账户信任关系，该关系提供了在云账户之间进行横向移动的途径
- 未测试 IMDSv2 强制执行情况，而这是最常见的云特定漏洞

## 输出格式

```
## 发现：跨账户角色信任允许从开发账户横向移动至生产账户

**ID**: CLOUD-002
**严重性**: 严重（CVSS 9.6）
**云服务商**: AWS
**受影响账户**: 生产账户（111222333444）
**利用来源**: 开发账户（555666777888）

**描述**:
生产账户 IAM 角色 "ProdDataAccess" 的信任策略允许开发账户中的
Lambda 执行角色 "LambdaDevRole" 担任该角色。这一跨账户信任结合开发者
修改 Lambda 函数代码的能力，创建了一条从开发只读权限到生产数据访问的路径。

**攻击链**:
1. 枚举开发账户中的 Lambda 函数：aws lambda list-functions
2. 确认 LambdaDevRole 拥有 sts:AssumeRole 权限
3. 修改 Lambda 以担任 ProdDataAccess：aws sts assume-role --role-arn arn:aws:iam::111222333444:role/ProdDataAccess
4. 从已担任角色：aws s3 ls s3://prod-customer-data -> 230 万条客户记录

**影响**:
攻击者只需入侵任一开发者凭据，即可在不直接攻击生产账户的情况下
访问生产客户数据（230 万条记录）。

**修复建议**:
1. 将 ProdDataAccess 信任策略限制为仅允许特定生产角色
2. 从 LambdaDevRole 策略中移除 sts:AssumeRole 权限
3. 实施 AWS Organizations SCP，禁止开发账户进行跨账户角色担任
4. 启用 CloudTrail 对跨账户 AssumeRole 事件的告警
5. 使用开发账户无法访问的 KMS 密钥加密 S3 存储桶
```
