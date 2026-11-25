---
name: 31-production-checklist
description: 在 Cisco ASR1001-X 变更后做校验，分离验收与持久化，并基于端到端证据出具验收。
---

# 生产检查清单

## 目标

仅在所处理原因、保留服务与（如授权）持久化均被证明时出具验收。

## 前置条件

识别 ASR1001-X、IOS XE release、脱敏基线、变更范围、回滚与备用访问。

## 变更后检查清单

- [ ] 身份/release 仍符合预期。
- [ ] 仅授权对象发生变化。
- [ ] 关键接口/上行链路为 UP。
- [ ] 相关路由/FIB/CEF 一致。
- [ ] 适用时 BGP/OSPF 保持稳定。
- [ ] PPPoE/IPoE 仍可用。
- [ ] AAA/RADIUS 仍可用。
- [ ] NAT/CGNAT 创建预期翻译，且无新增 drops/失败。
- [ ] ACL/policy/QoS 保留未涉及流量。
- [ ] CPU/内存无明显回退。
- [ ] SSH/管理与管理 NAT/PAT 仍可用。
- [ ] 前后计数器证明双向转发。
- [ ] 有访问时已校验最终客户端。
- [ ] 无客户端访问时明确记录测试限制。
- [ ] 回滚仍可执行。

## 技术验收与端到端

可用充分证据验收某一层，但无客户端确认或等价测试时，勿宣称“端到端服务可用”。例如：NAT 翻译 + 回程到 BNG 证明 NAT 数据面，但不能替代客户端 DNS/HTTP/HTTPS。

## 持久化

已验收的 running-config 不自动授权 NVRAM。持久化需显式门禁。`write memory`/`copy running-config startup-config` 之后：

- [ ] 已记录成功返回；
- [ ] startup-config 恰好含已批准行；
- [ ] 既有对象完好；
- [ ] 脱敏证据已发布到 Source of Truth。

## 验收标准

同时满足时接受：

1. 根因已纠正；
2. 计数器/状态证明预期效果；
3. 须保留对象无回退；
4. 要求时客户端已确认服务；
5. 若授权持久化，已校验。

## 拒绝标准

出现新 drops、pool/端口失败、会话劣化、startup-config 意外差异、管理服务损坏或证据矛盾时拒绝或保持挂起。

## 回滚

触发该变更的专项计划并重跑本清单。勿把 clear/reload 当第一反应。

## 安全

脱敏凭据、个人数据与敏感标识符。勿版本化原始配置。

## 依赖

与 `30-safe-change` 及专用技术 skill 配合。PPPoE UP 但无法上网时用 `32-pppoe-up-no-navigation`。

## 来源

- Cisco ASR1001-X / IOS XE；以真实 CLI 为准。
- 由 IOS XE 17.09.03a 真实 CGNAT 校验提炼的流程，不含客户专属数据。
