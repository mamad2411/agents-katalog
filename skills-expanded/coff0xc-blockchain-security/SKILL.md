---
name: coff0xc-blockchain-security
description: "Use when / 当用户请求 blockchain、smart contract、DeFi/Web3、多链安全：Solidity/EVM、Solana、Cosmos、Substrate、Cairo/StarkNet、TON、Algorand、AMM、oracle、bridge、token/NFT、Foundry/Hardhat/Slither、资产流和权限。手动触发：使用 coff0xc-blockchain-security。"
---

# coff0xc-blockchain-security

<!-- skill-id: cs-bcs-d2a58f13 -->

## 快速规则（日常任务先读这里）
> **[资产流先行]** 先看权限、资金流、状态机、价格来源、外部调用和升级/治理路径。
> **[证据门禁]** 每个发现绑定合约/函数/行号、前置条件、影响资产和可验证测试。
> **[修复闭环]** 优先最小补丁、属性/单元测试、模拟攻击和部署/迁移风险说明。
> **[硬边界]** 主网交易、私钥、真实资金、未授权合约交互、公开披露和 MEV 操作先确认。

普通链上/合约审计按本节先推进；只有主网响应、跨链事件或完整经济模型评审时再展开完整工作流。

## 能力定位
面向区块链、智能合约、DeFi 和多链项目的安全审计能力。重点是资金流、权限、状态转换、预言机、跨链和测试覆盖。

## 能交付什么
- 合约入口点和权限模型清单
- 资产流、状态机、价格来源和外部调用风险
- 漏洞发现、影响、PoC 思路和修复建议
- Foundry/Hardhat/链特定测试或审计检查清单

## 可以接收什么输入
- Solidity/Rust/CosmWasm/Cairo/TON/Algorand 合约
- 测试、部署脚本、白皮书、经济模型、审计报告
- 交易样例、事件日志、配置和权限说明

## 放心使用的边界
- 只处理授权代码和测试/本地链验证
- 真实链上操作、私钥、资金迁移、公开利用必须先确认或拒绝
- 不把理论漏洞当成已验证资金风险
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 先识别资产和权限边界
- 按链和框架使用对应安全检查
- 每个发现说明可达性、影响和测试建议

## 典型使用方式
```text
使用 coff0xc-blockchain-security 审计这个 Solidity 合约的权限、资产流和价格来源。
使用 coff0xc-blockchain-security 检查 Solana 程序的 PDA、signer 和 CPI 风险。
Use coff0xc-blockchain-security to review this DeFi protocol and propose Foundry tests.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
