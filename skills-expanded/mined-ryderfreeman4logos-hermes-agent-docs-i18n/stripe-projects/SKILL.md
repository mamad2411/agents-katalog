---
name: stripe-projects
description: Provision SaaS services + sync creds via Stripe Projects.
version: 0.1.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Payments, Stripe, Projects, Provisioning, Infrastructure]
    related_skills: [stripe-link-cli, mpp-agent]
---

# Stripe Projects 功能

该功能封装了 [Stripe Projects](https://projects.dev) CLI 插件，使 Hermes 能够统一管理各类 SaaS 服务（如 Neon、Twilio、Vercel 等）的配置，自动生成凭证并同步到用户的 `.env` 文件中，同时实现跨服务提供商的账单管理。

目前该功能仅支持 `[linux, macos]` 系统，而更广泛的支付相关功能集群仍在 Windows 上完善中。尽管 Stripe CLI 本身是跨平台的，但此限制主要是出于集群架构考虑，并非硬性规定。

## 适用场景

触发语句包括：

- “设置 <provider>”，“配置 <Neon|Twilio|Vercel|...>”，“创建数据库”
- “为这个项目提供一个 <Postgres|Redis|Twilio number|...>”
- “管理我的服务栈凭证”，“更换此密钥”，“升级我的套餐”
- “我可以添加哪些提供商？”

即使用户已拥有某个提供商的账户，仍可通过 `stripe projects link <provider>` 将其与 Hermes 连接。若用户希望使用现有的资源（如已有数据库或 Vercel 项目），需先确认该提供商是否支持此类操作；目前许多提供商仅支持创建新资源，暂不支持导入现有资源。

## 先决条件

- 已安装 Stripe CLI（macOS 可通过 Homebrew 安装，Linux 可通过包管理器安装，或从 https://docs.stripe.com/stripe-cli/install 下载）
- 已安装 Stripe Projects 插件
- 拥有 Stripe 账户。如果用户尚未注册，CLI 可在设置过程中引导其通过浏览器完成登录或账户创建。

## 安装方式

macOS：

```
brew install stripe/stripe-cli/stripe
stripe plugin install projects
```

Linux系统：请先按照https://docs.stripe.com/stripe-cli/install上的平台专属安装指南进行操作，随后：

```
stripe plugin install projects
```

## 运行方式

所有命令均需在用户的项目目录内通过 `terminal` 工具执行（CLI 会将 `.env` 文件及 `.projects/vault/vault.json` 文件写入当前工作目录）。

## 操作步骤

### 1. 初始化项目

```
cd <project-root>
stripe projects init
```

这将生成 `.projects/vault/vault.json` 文件（用于存储加密后的凭证），并为该项目接入各种提供程序做好准备。

### 2. 查找可用的提供程序

```
stripe projects catalog
```

列出 Stripe Projects 支持的所有提供商——包括数据库、托管服务、身份验证、人工智能、分析工具、消息传递等功能。

### 3. 添加服务

```
stripe projects add <provider>/<service>
```

示例：

- `stripe projects add neon/postgres`
- `stripe projects add twilio/sms`
- `stripe projects add runloop/sandbox`

该命令行工具会在用户自身的账户中通过对应提供商配置相关服务，生成凭证并将其同步到 `.env` 文件中，同时将该资源存储在安全保管库中。用户可能需要确认所选择的套餐等级或价格信息。 

### 4. 验证

```
stripe projects list
```

应显示新添加的提供程序及其 `.env` 配置键。 

### 5. 管理 / 升级 / 移除

```
stripe projects upgrade <provider>     # tier change
stripe projects remove <provider>      # deprovision
stripe projects rotate <provider>      # rotate credentials
```

## 常见问题与注意事项

- **`.env` 文件的写入为真实写入操作。** CLI 会直接追加到项目根目录中的 `.env` 文件内容。如果用户的 `.env` 文件已被加入 `.gitignore`（这是常规做法），则其中的配置信息将得到安全保存；否则，该功能可能会成为敏感信息泄露的途径。务必先检查 `.gitignore` 文件。
- **每个项目拥有独立状态。** `.projects/vault/vault.json` 文件是针对每个项目单独存储的。在两个不同的项目中配置相同的服务会生成两个独立的资源——进而产生两笔费用。
- **计费在 Stripe 端完成。** 在执行 `add`/`upgrade` 操作时出现的层级选择实际上都会触发真实扣费，因此在确认操作前应先向用户明确说明相关费用。
- **服务提供商的可用性可能会变化。** 服务目录会不断更新；如果用户指定的提供商未出现在列表中，建议先使用 `stripe projects catalog | grep <name>` 命令进行查询，而非直接导致 `add` 操作失败。
- **保险库中的敏感信息经过加密，但 `.env` 文件为明文形式。** 需遵循标准的 `.env` 文件管理规范——绝不可将其提交到版本控制系统中。
- **删除服务并不一定会彻底清除底层资源。** 某些服务提供商可能会留下处于暂停或休眠状态的资源。对于高成本服务（尤其是托管数据库），在执行 `remove` 操作后应查看该提供商的专用控制面板。

## 验证方法

```
stripe projects --version && stripe projects list
```

在已初始化的项目中，退出码为0表示该插件运行正常。
