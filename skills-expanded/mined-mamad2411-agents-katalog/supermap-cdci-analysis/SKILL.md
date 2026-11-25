---
name: supermap-cdci-analysis
description: |
  分析 TeamCity CI/CD 构建失败原因并提供解决方案。

  Use this skill when:
  - 用户提供 TeamCity 构建 URL 并询问构建失败原因
  - 需要排查 CI/CD 流水线故障
  - 需要分析构建状态
  - 构建失败后需要快速定位问题

  The skill will:
  1. 解析 TeamCity URL 提取构建配置信息
  2. 自动检测并尝试多种认证方式（Bearer Token、Basic Auth）
  3. 调用 TeamCity REST API 获取最新构建状态
  4. 构建成功：返回简洁成功信息
  5. 构建失败：渐进式获取日志，使用 LLM 智能分析，提供临时和长期解决方案
  6. 当日志无法获取时：基于 statusText 和问题信息进行降级分析

  Requires: Node.js
  环境变量:
  - SUPERMAP_CDCI_TOKEN: 用于 cdci.ispeco.com:90
  - SUPERMAP_CI_TOKEN: 用于 ci.iserver.com:90 或 ci.ispeco.com:90
  Compatible with Windows, macOS, and Linux.
---

# TeamCity 构建分析 Skill

## 如何执行

**重要说明**: 调用 `Skill` 工具只会加载本说明文档，需要**手动执行脚本**来运行分析。

### 方法 1: 直接运行 Node.js 脚本（推荐）

```bash
# 进入 skill 目录
cd ~/.claude/skills/supermap-cdci-analysis/scripts

# 执行分析脚本
node analyze-build.js "<TeamCity URL>"

# 示例
node analyze-build.js "http://cdci.ispeco.com:90/buildConfiguration/ICloudNative_00iCloudNativeGate_IcloudNativeMrGate"
```

### 方法 2: 在 Claude Code 中按照本文档指引逐步执行

按照下方"工作流程"章节的步骤，手动调用 TeamCity API 或运行相应的脚本命令。

### 方法 3: 原始数据模式（供 Claude 分析）

使用 `--raw` 参数获取原始构建数据，由 Claude 进行智能分析：

```bash
cd ~/.claude/skills/supermap-cdci-analysis/scripts
node analyze-build.js "<TeamCity URL>" --raw
```

输出包含：
- 构建基本信息（编号、状态、statusText）
- 构建日志（最后 500 行）
- 失败测试列表
- 问题列表
- 变更记录

Claude 将基于这些数据提供详细的失败分析和解决方案。

## 使用前提

1. **环境变量**: 根据 CI 服务器地址设置对应的环境变量

   | CI 服务器地址 | 环境变量 | 说明 |
   |--------------|----------|------|
   | cdci.ispeco.com:90 | SUPERMAP_CDCI_TOKEN | iSpeco CDCI |
   | ci.iserver.com:90 | SUPERMAP_CI_TOKEN | iServer CI |
   | ci.ispeco.com:90 | SUPERMAP_CI_TOKEN | iSpeco CI |

   ```bash
   # Windows
   set SUPERMAP_CDCI_TOKEN=your_token_here
   set SUPERMAP_CI_TOKEN=your_token_here

   # Linux/Mac
   export SUPERMAP_CDCI_TOKEN=your_token_here
   export SUPERMAP_CI_TOKEN=your_token_here
   ```

2. **网络访问**: 需要能够访问 TeamCity 服务器

3. **工具依赖**: 需要 Node.js 环境（使用原生 https 模块，无需 curl）

## 工作流程

### Step 1: 解析构建 URL

从用户提供的 TeamCity URL 中提取：
- **Base URL**: TeamCity 服务器地址（如 `http://cdci.ispeco.com:90`）
- **Build Type ID**: 构建配置 ID

### Step 2: 认证方式检测与环境变量选择

根据 CI 服务器地址自动选择环境变量：

| CI 服务器 | 环境变量 | 说明 |
|-----------|----------|------|
| cdci.ispeco.com:90 | SUPERMAP_CDCI_TOKEN | iSpeco CDCI |
| ci.iserver.com:90 | SUPERMAP_CI_TOKEN | iServer CI |
| ci.ispeco.com:90 | SUPERMAP_CI_TOKEN | iSpeco CI |

选择逻辑：
1. 解析 URL 获取 base_url
2. 判断 base_url 包含哪个 CI 服务器地址
3. 检查对应环境变量是否已设置
4. 如未设置，提示用户设置对应环境变量

自动检测可用的认证方式，按优先级尝试：

| 优先级 | 认证方式 | 说明 |
|--------|----------|------|
| 1 | Bearer Token | `-H "Authorization: Bearer $TOKEN"` |
| 2 | Basic Auth (密码) | `-u ":$TOKEN"` |
| 3 | Basic Auth (用户名) | `-u "$TOKEN:"` |
| 4 | Basic Auth (空格) | `-u " :$TOKEN"` |

- 首次请求时自动检测并缓存成功的认证方式
- 后续请求复用已缓存的认证方式
- 认证失败时自动回退到其他方式

### Step 3: 获取构建状态

调用 TeamCity REST API（使用 Node.js 原生 https 模块）：
```javascript
const https = require('https');

const options = {
    hostname: 'cdci.ispeco.com',
    path: '/app/rest/builds?locator=buildType:{id},count:1',
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${SUPERMAP_CDCI_TOKEN}`,
        'Accept': 'application/json'
    }
};
```

### Step 4: 处理构建状态

#### 成功
输出简洁成功信息：
```
✓ 构建 #4694 成功
  完成时间: 2026-03-09 16:34:27
```

#### 失败
进入分析流程（Step 5）

### Step 5: 渐进式日志分析与 Sonar 联动

1. **获取日志片段**: 尝试多种方式获取日志
   - API 端点: `/app/rest/builds/id:{id}/log`
   - 下载链接: `/downloadBuildLog.html`
   - 构建消息: `/app/rest/builds/id:{id}/messages`

2. **日志获取失败时的降级方案**:
   - 获取构建详情（statusText）
   - 获取失败测试列表
   - 获取问题列表
   - 获取变更记录
   - 基于以上信息进行降级分析

3. **LLM 分析**: 使用 Claude 分析日志或降级信息

4. **Sonar 失败检测**（新增）:
   - 如果分析结果包含 Sonar/质量门相关信息：
     - 包含 "sonar.ispeco.com" URL
     - 包含 "quality gate" / "质量门" / "Quality Gate" 关键词
     - 包含 Sonar 项目 key 模式 (com.supermap.cloud:*)
   - 提取 Sonar 项目 key 和 PR 号（如有）
   - 调用 `supermap-sonar-error-analysis` skill 进行详细分析
   - 将 Sonar 分析结果与 CI 分析结果合并输出

5. **判断信息充足性**:
   - **充足**: 直接生成解决方案
   - **不足**: 尝试获取更多信息或基于现有信息分析

### Step 6: 生成解决方案

输出格式（普通失败）：
```
✗ 构建 #4694 失败

【临时解决方案】（立即执行）
1. ...
2. ...

【长期解决方案】（根本解决）
1. ...
2. ...

【关键错误】（仅参考）
...

【提示】（如适用）
无法获取完整构建日志，分析基于可用信息。
```

输出格式（含 Sonar 失败）：
```
✗ 构建 #4694 失败

【失败原因】
CI 构建在 Sonar 质量门检查阶段失败

【Sonar 质量门分析】
✗ Sonar 质量门未通过
  项目: com.supermap.cloud:ispeco-dashboard-api
  分支: PR #3099

【失败原因】
1. 新代码覆盖率 65.2% < 要求 80%
2. 发现 3 个 Blocker 级别问题

【改进建议】
1. 添加单元测试覆盖新代码
2. 修复 Blocker 级别问题

【参考链接】
- http://sonar.ispeco.com:9001/dashboard?id=com.supermap.cloud:ispeco-dashboard-api&pullRequest=3099

【CI 构建临时解决方案】（立即执行）
1. ...

【CI 构建长期解决方案】（根本解决）
1. ...
```

## 平台兼容性

自动检测当前平台并提供对应命令：

| 平台 | 环境变量设置 | 路径分隔符 |
|------|-------------|-----------|
| Windows | `set VAR=value` | `\` |
| macOS | `export VAR=value` | `/` |
| Linux | `export VAR=value` | `/` |

### Token 自动清理

Token 中可能包含意外的空白字符（换行符、空格等），Skill 会自动清理：

| 场景 | 处理方式 |
|------|---------|
| 环境变量包含换行符 | 自动去除 `\n`、 `\r`、空格、制表符等所有空白字符 |
| Token 首尾有空格 | 自动 trim 处理 |

**注意**: 如果 Token 设置时包含换行符（例如从文件读取），Skill 会自动处理，无需手动修改环境变量。

## 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| SUPERMAP_CDCI_TOKEN / SUPERMAP_CI_TOKEN 未设置 | 根据 CI 服务器地址提示设置对应环境变量 |
| Token 无效 | 提示检查 Token 是否过期，已尝试所有认证方式 |
| 构建配置不存在 | 提示检查 URL 是否正确 |
| 服务器不可达 | 提示检查网络 |
| 日志端点权限不足 | 降级分析：基于 statusText 和问题信息 |
| 构建日志已清理 | 降级分析：基于可用信息进行分析 |

### 认证方式自动切换

当一种认证方式失败时，skill 会自动尝试其他方式：

```
尝试 Bearer Token → 失败
尝试 Basic Auth (密码) → 失败
尝试 Basic Auth (用户名) → 成功 ✓
缓存此认证方式供后续使用
```

### 日志获取降级

当无法获取完整日志时：
1. 尝试 API 端点 `/app/rest/builds/id:{id}/log`
2. 尝试下载链接 `/downloadBuildLog.html`
3. 尝试构建消息 `/app/rest/builds/id:{id}/messages`
4. 获取 statusText、问题列表、失败测试、变更记录
5. 基于以上信息进行降级分析

## 示例

### 输入
```
http://cdci.ispeco.com:90/buildConfiguration/ICloudNative_DistributeISpecoDashboardUi_11DeployTestISpecoDashboardUi
```

### 输出（失败）
```
✗ 构建 #4694 失败

【临时解决方案】（立即执行）
1. 增加 Node.js 内存限制：
   Windows: set NODE_OPTIONS=--max-old-space-size=4096
   Linux/Mac: export NODE_OPTIONS=--max-old-space-size=4096

2. 重新运行构建

【长期解决方案】（根本解决）
1. 修改 package.json 永久增加内存配置
2. 拆分测试批次，减少单批次内存占用
3. 升级 CI 构建节点内存配置

【关键错误】（仅参考）
FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory
```
