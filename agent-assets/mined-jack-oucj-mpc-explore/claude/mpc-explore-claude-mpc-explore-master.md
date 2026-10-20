# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## AI Guidance

* Ignore GEMINI.md and GEMINI-*.md files
* To save main context space, for code searches, inspections, troubleshooting or analysis, use code-searcher subagent where appropriate - giving the subagent full context background for the task(s) you assign it.
* After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
* For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
* Before you finish, please verify your solution
* Do what has been asked; nothing more, nothing less.
* NEVER create files unless they're absolutely necessary for achieving your goal.
* ALWAYS prefer editing an existing file to creating a new one.
* NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
* When you update or modify core context files, also update markdown documentation and memory bank
* When asked to commit changes, exclude CLAUDE.md and CLAUDE-*.md referenced memory bank system files from any commits. Never delete these files.

## Memory Bank System

This project uses a structured memory bank system with specialized context files. Always check these files for relevant information before starting work:

### Core Context Files

* **CLAUDE-activeContext.md** - Current session state, goals, and progress (if exists)
* **CLAUDE-patterns.md** - Established code patterns and conventions (if exists)
* **CLAUDE-decisions.md** - Architecture decisions and rationale (if exists)
* **CLAUDE-troubleshooting.md** - Common issues and proven solutions (if exists)
* **CLAUDE-config-variables.md** - Configuration variables reference (if exists)
* **CLAUDE-temp.md** - Temporary scratch pad (only read when referenced)

**Important:** Always reference the active context file first to understand what's currently being worked on and maintain session continuity.

### Memory Bank System Backups

When asked to backup Memory Bank System files, you will copy the core context files above and @.claude settings directory to directory @/path/to/backup-directory. If files already exist in the backup directory, you will overwrite them.

## Project Overview

### 项目背景与目标
这是一个基于Web3Auth MPC技术的**后端服务器项目**。项目的核心目标是构建一个支持多种登录模式和去中心化身份管理的IM即时通讯平台的**后端服务**。

**项目核心**：开发一个完整的后端服务器，集成Web3Auth的mpc-core-kit库，提供TSS私钥分片管理、MFA验证、区块链身份生成等核心API服务。

### 项目架构组成
**核心开发目标 - 后端服务器：**
- 基于Web3Auth mpc-core-kit构建的后端服务
- 提供完整的TSS私钥分片管理API
- 实现MFA多重身份验证服务
- 支持IM通讯的身份管理和加密服务

**支撑组件：**
- **mpc-core-kit/**: Web3Auth的核心MPC库，作为后端集成的基础
- **web3auth-backend/**: 现有的Web3Auth后端包架构，提供参考实现
- **mpc-flutter-quick-start/**: Flutter测试前端，**仅用于验证后端API接口**
- **demo/**: 功能体验报告和界面截图，提供需求验证和设计参考

### 核心功能需求（后端API服务）
1. **多模式登录API**
   - 游客登录接口
   - 邮箱/手机号登录接口
   - 游客升级为正式用户API

2. **TSS私钥分片服务**
   - 私钥分片生成API
   - 设备份额管理接口
   - 服务器份额安全存储
   - 恢复份额(RecoveryShare)管理

3. **MFA身份验证服务**
   - 认证App集成API
   - 生物识别验证接口
   - 设备管理API
   - 新设备验证服务

4. **区块链集成服务**
   - 以太坊地址生成API
   - 钱包余额查询接口
   - 交易签名服务
   - 智能合约交互API

### 技术验证基础
基于mpc-flutter-quick-start项目的完整功能测试，已验证以下**后端功能需求的可行性**：
- 邮箱验证登录流程 → 需要后端邮箱验证API
- MFA认证设置和管理 → 需要后端MFA管理服务
- 设备管理和新设备验证 → 需要后端设备管理API
- 区块链钱包功能 → 需要后端钱包服务API
- Web3合约交互功能 → 需要后端合约交互服务

**测试环境**：使用Ethereum Sepolia测试网验证了完整的用户身份管理和区块链交互流程。

### 开发重点（后端服务器）
1. **API架构设计**：设计RESTful API接口，支持前端各种操作需求
2. **TSS集成实现**：基于mpc-core-kit库实现TSS私钥分片的后端逻辑
3. **安全架构构建**：实现私钥份额的安全存储和管理机制
4. **MFA验证体系**：构建完善的多重身份验证后端服务
5. **数据库设计**：设计用户、设备、份额等数据的存储结构
6. **接口协议定义**：与Flutter前端的通信协议和数据格式

## 项目详细规划

### IM即时通讯软件核心需求

#### 登录系统架构设计
1. **游客登录模式**
   - 无需注册即可进入应用
   - 提供临时身份标识
   - 支持后续升级为正式账户

2. **传统登录模式**  
   - 邮箱验证登录（已验证）
   - 手机号码登录（待实现）
   - 第三方社交登录（待扩展）

3. **密码设置触发机制**
   - 游客模式下设置密码自动触发区块链身份生成
   - 后端调用TSS算法生成以太坊地址
   - 私钥自动分片存储（设备份额 + 服务器份额）

#### TSS多方安全计算实现
1. **私钥分片策略**
   - **设备份额(Device Share)**: 存储在用户手机本地
   - **服务器份额(Server Share)**: 存储在后端安全环境
   - **恢复份额(Recovery Share)**: MFA设置后生成，用于账户恢复

2. **2/3阈值签名方案**
   - 任意两个份额即可完成私钥重构和签名
   - 单个份额丢失不影响账户安全性
   - 支持灵活的恢复机制

3. **MFA集成逻辑**
   - MFA验证成功后自动生成RecoveryShare
   - RecoveryShare可与服务器份额配合完成签名
   - 提供账户安全的最后防线

### 技术体验验证成果

基于mpc-flutter-quick-start项目的完整功能验证，已确认以下核心功能可行性：

#### 认证流程验证 ✅
- **邮箱验证登录**: 六位数验证码机制，安全可靠
- **MFA多重认证**: 支持认证App、生物识别、设备管理等多种方式
- **新设备验证**: 完整的设备管理和验证流程

#### 区块链功能验证 ✅  
- **网络支持**: Ethereum Sepolia测试网验证成功
- **钱包功能**: 余额查询、私钥签名、转账交易全部正常
- **智能合约**: Web3合约交互功能完整

#### MFA管理体验 ✅
- **初次设置流程**: EnableMFA引导用户完成首次多重认证设置
- **管理界面**: ManageMFA提供完整的认证方式管理功能  
- **设备管理**: 支持设备添加、删除，保护Device Share安全
- **恢复机制**: 恢复短语对应TSS的1/3份额，符合设计预期

### 后端架构设计要点

#### Web3Auth mpc-core-kit集成策略
1. **核心库依赖管理**
   - 集成`@web3auth/mpc-core-kit`作为核心MPC功能
   - 配置TSS相关依赖库(`@toruslabs/tss-dkls-lib`, `@toruslabs/tss-frost-lib`)
   - 建立与现有web3auth-backend monorepo的架构一致性

2. **TSS私钥分片服务**
   - 设计安全的服务器份额存储机制
   - 实现设备份额的安全传输和本地存储
   - 建立RecoveryShare的生成和管理逻辑

3. **IM通讯架构集成**
   - 用户身份与区块链地址的映射管理
   - 支持游客模式到正式用户的无缝升级
   - 消息加密和身份验证机制

#### 安全性设计原则
1. **私钥份额安全**
   - 服务器份额采用硬件安全模块(HSM)或安全enclave保护
   - 设备份额仅存储在用户本地，服务器无法直接访问
   - RecoveryShare通过MFA验证后才能激活

2. **通信安全**
   - 所有TSS计算过程采用端到端加密
   - API接口实施严格的身份验证和授权机制
   - 支持零知识证明验证用户身份

## Development Commands

### Backend (web3auth-backend/)
Monorepo managed with Lerna and workspaces:
```bash
cd web3auth-backend/
npm run bootstrap           # Install dependencies for all packages
npm run build              # Build all packages
npm run dev                # Start development mode
npm run test               # Run tests for all packages
npm run lint               # Lint all packages
npm run clean              # Clean all packages and dependencies
```

### MPC Core Kit (mpc-core-kit/)
TypeScript library for MPC functionality:
```bash
cd mpc-core-kit/
npm run build              # Build the library
npm run dev                # Start development mode
npm run test               # Run tests with Node.js test runner
npm run lint               # Lint and fix TypeScript files
```

### Flutter Demo (mpc-flutter-quick-start/)
Flutter application for testing MPC functionality:
```bash
cd mpc-flutter-quick-start/
flutter pub get           # Install dependencies
flutter run               # Run the app
flutter test              # Run tests
flutter build apk         # Build Android APK
flutter build ios         # Build iOS app
```

## Architecture Overview

### Repository Structure
这是一个专注于**后端服务器开发**的多项目仓库，包含以下组件：

**核心开发项目：**
1. **目标后端服务器** - 待开发的核心项目
   - 基于Web3Auth mpc-core-kit构建
   - 提供完整的TSS私钥分片管理、MFA验证等API服务
   - 技术栈：Node.js, TypeScript, Express/Fastify, 数据库
   - 支持IM即时通讯的身份管理和加密服务

**支撑和参考组件：**
2. **mpc-core-kit/**: 核心MPC功能库
   - 提供TSS (Multi-Party Computation) 核心功能
   - 后端服务器的主要依赖库
   - Peer dependencies: TSS libraries (`@toruslabs/tss-dkls-lib`, `@toruslabs/tss-frost-lib`)
   - Technologies: TypeScript, Node.js ≥20, native Node test runner

3. **web3auth-backend/**: 参考架构和实现
   - Lerna monorepo结构参考
   - 现有Web3Auth后端SDK实现参考
   - Packages结构: `packages/node-sdk/` - 提供架构设计参考
   - Technologies: Node.js ≥18, TypeScript, Lerna, Mocha testing

**测试和验证工具：**
4. **mpc-flutter-quick-start/**: 测试前端应用
   - **仅用于测试后端API接口**
   - 验证后端功能的可行性和正确性
   - 模拟真实前端的API调用场景
   - Technologies: Flutter/Dart, Android/iOS platforms

5. **demo/**: 功能验证材料
   - 包含详细的功能体验报告和界面截图
   - 提供后端API需求的验证依据

### 后端开发核心技术栈
- **TSS (Threshold Signature Scheme)**: 多方安全计算的核心加密技术
- **Web3Auth mpc-core-kit**: 后端服务器的核心MPC功能库
- **Node.js + TypeScript**: 后端服务器主要开发语言和运行环境
- **数据库**: 用户数据、设备信息、私钥份额的安全存储
- **RESTful API**: 前后端通信接口规范
- **身份验证**: JWT/OAuth等认证机制
- **加密存储**: 私钥份额和敏感数据的安全存储方案

### 后端开发环境要求
**必需环境：**
- Node.js ≥20 (与mpc-core-kit要求一致)
- npm ≥9.x
- TypeScript 5.x+
- 数据库系统 (PostgreSQL/MongoDB 等)

**测试环境：**
- Flutter SDK (仅用于运行测试前端)
- Ethereum Sepolia测试网访问

**开发技能要求：**
- TypeScript/Node.js后端开发经验
- Web3/区块链基础知识
- 加密学和安全存储理解
- RESTful API设计经验
- MPC/TSS算法基本理解