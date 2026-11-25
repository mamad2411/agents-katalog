---
name: kms-knowledge
description: 当在字节跳动内部服务中接入KMS密钥管理平台、使用code.byted.org/security/gokms或code.byted.org/security/bytedkms等SDK、进行敏感数据加解密或敏感配置托管时使用。
user-invocable: false
---

# KMS 密钥管理平台

KMS（密钥管理系统）是字节跳动内部的密钥管理服务，提供**主密钥加解密迁移敏感信息托管**能力，包括数据密钥管理和敏感配置托管两大核心功能。平台支持对落盘的敏感数据（如手机号、身份证、金额等）进行加解密操作。

## SDK 接入

KMS SDK 支持多种编程语言，包括 Golang、Python、Java、C++ 和 NodeJS，分为 V1 SDK（Wrapper SDK）和 V2 SDK 两个版本。使用 SDK 时需要进行身份认证，本地测试可使用 doas 工具，服务部署时需在 TCE 上开启服务认证。

**主要使用场景**：
- **敏感数据加解密**：对数据库中的敏感字段进行加密存储和解密使用
- **敏感配置托管**：管理代码中的敏感配置信息，如数据库密码、API密钥等
- **多数据密钥管理**：支持同一服务使用多个数据密钥，通过密钥名称区分
- **固定密文加密**：使用 `encrypt_for_query_2` 函数实现同一明文加密结果相同

**SDK 版本选择**：
- **V2 SDK**：原生支持 KMS V2，支持 GDPR/ZTI Token 鉴权和零信任证书鉴权
- **V1 SDK（Wrapper SDK）**：最新版本支持根据 TCC 配置自动选择连接 KMS V1 或 V2

**核心功能函数**：
- `get_data_key()`：获取当前服务的默认数据密钥（name=default）
- `get_data_key_by_name(name)`：获取当前服务指定名称的数据密钥
- `decrypt_data_key_by_psm(psm)`：获取指定 PSM 的默认数据密钥
- `decrypt_data_key_by_psm_and_name(psm, name)`：获取指定 PSM 和名称的数据密钥

[kms-sdk-usage.md](./kms-sdk-usage.md) - KMS SDK 详细使用指南和代码示例
[kms-platform-guide.md](./kms-platform-guide.md) - KMS 平台操作和最佳实践指南

