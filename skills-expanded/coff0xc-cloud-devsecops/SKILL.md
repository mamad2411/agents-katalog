---
name: coff0xc-cloud-devsecops
description: "Use when / 当用户请求 cloud、container、Kubernetes/K8s、serverless、DevSecOps、supply chain、CI/CD 或 secrets：AWS/Azure/GCP、IAM、S3/Blob/GCS、Docker、Terraform/IaC、GitHub Actions、SBOM/SCA、secret scanning、pipeline risk。手动触发：使用 coff0xc-cloud-devsecops。"
---

# coff0xc-cloud-devsecops

<!-- skill-id: cs-cds-0e9b4c6a -->

## 快速规则（日常任务先读这里）
> **[只读优先]** 先看 IaC、K8s、Dockerfile、CI workflow、依赖和密钥暴露面；默认不改云端。
> **[控制映射]** 把问题映射到身份、网络、密钥、镜像、供应链、pipeline 和审计日志。
> **[验证门禁]** 提供最小修复、配置 diff、扫描/策略检查和残余风险。
> **[硬边界]** 云资源写入、权限变更、CI/CD 发布、secret rotation、生产集群动作先确认。

普通云/DevSecOps 审查按本节先推进；只有真实环境变更、发布门禁或多云架构评审时再展开完整工作流。

## 能力定位
面向云原生、容器、CI/CD、供应链和密钥治理的只读优先评估能力。目标是让风险有证据、修复可落地、验证可复现。

## 能交付什么
- 云/IaC/K8s/CI/CD 风险清单
- 最小权限、网络隔离、pipeline gate 和密钥轮换建议
- SBOM/SCA/secret scanning 策略
- 本地 lint/plan/只读检查和验证路线

## 可以接收什么输入
- Terraform/CloudFormation、K8s manifests、Dockerfile
- GitHub Actions/CI 配置、lockfile、SBOM、镜像扫描结果
- 云账号只读输出、日志、env example、密钥发现线索

## 放心使用的边界
- 默认只读分析本地配置和授权证据
- 云端写入、IaC apply、kubectl apply/delete、workflow dispatch、密钥撤销必须先确认
- 发现秘密值只报告类型、位置和处置建议，不复述完整值
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 按身份、网络、数据、运行时、供应链分层审查
- 区分配置风险和真实可达风险
- 输出修复优先级和回滚/验证方法

## 典型使用方式
```text
使用 coff0xc-cloud-devsecops 检查 Docker、K8s、CI/CD 和供应链风险。
使用 coff0xc-cloud-devsecops 评估 Terraform 里的 IAM、S3 暴露和 serverless 权限。
Use coff0xc-cloud-devsecops to harden this GitHub Actions workflow and secret usage.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
