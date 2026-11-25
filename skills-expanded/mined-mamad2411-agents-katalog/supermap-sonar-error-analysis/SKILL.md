---
name: supermap-sonar-error-analysis
description: |
  分析 SonarQube 质量门失败原因并提供改进建议。

  Use this skill when:
  - 用户提供 Sonar URL 或项目 key 并询问质量门状态
  - 需要排查 Sonar 质量门失败原因
  - 需要分析代码质量指标（覆盖率、重复率、问题等）
  - Pull Request 的 Sonar 检查未通过

  The skill will:
  1. 检查环境变量 SUPERMAP_SONAR_TOKEN
  2. 解析 Sonar URL，提取项目 key 和 PR 号（如有）
  3. 调用 Sonar API 查询质量门状态
  4. 质量门通过：返回简洁成功信息（含覆盖率、重复率）
  5. 质量门失败：获取具体失败指标、问题列表，分析并提供改进建议

  Requires: curl, SUPERMAP_SONAR_TOKEN environment variable
  Compatible with Windows, macOS, and Linux.
---

# SonarQube 质量门分析 Skill

## 使用前提

1. **环境变量**: 必须设置 `SUPERMAP_SONAR_TOKEN` 环境变量
   ```bash
   # Windows
   set SUPERMAP_SONAR_TOKEN=your_token_here

   # Linux/Mac
   export SUPERMAP_SONAR_TOKEN=your_token_here
   ```

2. **网络访问**: 需要能够访问 SonarQube 服务器

3. **工具依赖**: 需要 `curl` 命令可用

## 工作流程

### Step 1: 解析输入

从用户提供的 URL 或项目 key 中提取：
- **Sonar Base URL**: Sonar 服务器地址（默认 `http://sonar.ispeco.com:9001`）
- **Project Key**: 项目唯一标识（如 `com.supermap.cloud:ispeco-dashboard-api`）
- **Pull Request ID** (可选): PR 编号

支持的输入格式：
- Sonar 项目 URL: `http://sonar.ispeco.com:9001/dashboard?id=com.supermap.cloud:ispeco-dashboard-api`
- Sonar PR URL: `http://sonar.ispeco.com:9001/dashboard?id=com.supermap.cloud:ispeco-dashboard-api&pullRequest=3099`
- 纯项目 key: `com.supermap.cloud:ispeco-dashboard-api`
- 带 PR 号: `com.supermap.cloud:ispeco-dashboard-api#3099` 或 `com.supermap.cloud:ispeco-dashboard-api PR:3099`

### Step 2: 认证方式

SonarQube 使用 **Basic Auth** 认证：
- 用户名: Token 值
- 密码: 空

```bash
curl -u "${SUPERMAP_SONAR_TOKEN}:" "http://sonar.ispeco.com:9001/api/qualitygates/project_status?projectKey=..."
```

### Step 3: 查询质量门状态

调用 Sonar API：
```bash
# 普通分支
curl -u "${SUPERMAP_SONAR_TOKEN}:" \
  "http://sonar.ispeco.com:9001/api/qualitygates/project_status?projectKey={projectKey}"

# Pull Request
curl -u "${SUPERMAP_SONAR_TOKEN}:" \
  "http://sonar.ispeco.com:9001/api/qualitygates/project_status?projectKey={projectKey}&pullRequest={pr}"
```

### Step 4: 处理质量门状态

#### 通过 (status = OK)

输出简洁成功信息：
```
✓ Sonar 质量门通过
  项目: com.supermap.cloud:ispeco-dashboard-api
  分支: master (或 PR #3099)
  覆盖率: 78.5%
  重复率: 2.3%
```

#### 失败 (status = ERROR)

进入详细分析流程（Step 5）

### Step 5: 获取详细指标

调用 API 获取失败的详细指标：
```bash
curl -u "${SUPERMAP_SONAR_TOKEN}:" \
  "http://sonar.ispeco.com:9001/api/measures/component?component={projectKey}&metricKeys=coverage,new_coverage,duplicated_lines_density,new_duplicated_lines_density,bugs,vulnerabilities,code_smells"
```

关键指标说明：
| 指标 | 说明 | 质量门关联 |
|------|------|-----------|
| coverage | 整体覆盖率 | 代码覆盖率要求 |
| new_coverage | 新代码覆盖率 | 新代码覆盖率阈值 |
| duplicated_lines_density | 整体重复率 | 代码重复率要求 |
| new_duplicated_lines_density | 新代码重复率 | 新代码重复率阈值 |
| bugs | 可靠性问题 | 可靠性评级 |
| vulnerabilities | 安全漏洞 | 安全性评级 |
| code_smells | 代码异味 | 可维护性评级 |

### Step 6: 获取问题列表

调用 API 获取问题详情：
```bash
# 获取 blocker 和 critical 级别的问题
curl -u "${SUPERMAP_SONAR_TOKEN}:" \
  "http://sonar.ispeco.com:9001/api/issues/search?componentKeys={projectKey}&severities=BLOCKER,CRITICAL&statuses=OPEN&ps=20"
```

### Step 7: 生成分析报告

输出格式：
```
✗ Sonar 质量门未通过
  项目: com.supermap.cloud:ispeco-dashboard-api
  分支: PR #3099

【失败原因】
1. 新代码覆盖率 {actual}% < 要求 {required}% （差距 {gap}%）
2. 新代码重复率 {actual}% > 要求 {required}%
3. 发现 {bugs} 个可靠性问题
4. 发现 {vulnerabilities} 个安全漏洞

【问题统计】
- Blocker: X
- Critical: Y
- Major: Z
- Minor: W
- Info: V

【主要问题】
1. [Blocker] 问题描述
   文件: src/main/java/.../File.java:行号
   规则: 规则名称

2. [Critical] 问题描述
   ...

【改进建议】
1. 添加单元测试覆盖新代码，目标达到 {required}% 覆盖率
2. 提取重复代码到公共方法/类
3. 修复 Blocker 和 Critical 级别的问题
4. ...

【参考链接】
- http://sonar.ispeco.com:9001/dashboard?id=com.supermap.cloud:ispeco-dashboard-api&pullRequest=3099
```

## 平台兼容性

自动检测当前平台并提供对应命令：

| 平台 | 环境变量设置 | 路径分隔符 |
|------|-------------|-----------|
| Windows | `set VAR=value` | `\` |
| macOS | `export VAR=value` | `/` |
| Linux | `export VAR=value` | `/` |

## 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| SUPERMAP_SONAR_TOKEN 未设置 | 提示设置环境变量 |
| Token 无效 | 提示检查 Token 是否过期或权限是否足够 |
| 项目不存在 | 提示检查 project key 是否正确 |
| 服务器不可达 | 提示检查网络或 Sonar 服务器状态 |
| API 响应异常 | 输出原始错误信息供排查 |

## 示例

### 输入
```
http://sonar.ispeco.com:9001/dashboard?id=com.supermap.cloud:ispeco-dashboard-api&pullRequest=3099
```

### 输出（质量门通过）
```
✓ Sonar 质量门通过
  项目: com.supermap.cloud:ispeco-dashboard-api
  分支: PR #3099
  覆盖率: 78.5%
  重复率: 2.3%
```

### 输出（质量门失败）
```
✗ Sonar 质量门未通过
  项目: com.supermap.cloud:ispeco-dashboard-api
  分支: PR #3099

【失败原因】
1. 新代码覆盖率 65.2% < 要求 80% （差距 14.8%）
2. 发现 3 个 Blocker 级别问题

【问题统计】
- Blocker: 3
- Critical: 5
- Major: 12

【主要问题】
1. [Blocker] 空指针异常风险
   文件: src/main/java/com/supermap/cloud/dashboard/service/AnalysisService.java:142
   规则: java:S2259 - 空指针解引用

2. [Blocker] 资源未关闭
   文件: src/main/java/com/supermap/cloud/dashboard/util/FileUtil.java:89
   规则: java:S2095 - 资源应该在使用后关闭

【改进建议】
1. 为新代码添加单元测试，补充缺失的 14.8% 覆盖率
2. 修复所有 Blocker 级别问题
3. 优先处理 Critical 级别的安全漏洞

【参考链接】
- http://sonar.ispeco.com:9001/dashboard?id=com.supermap.cloud:ispeco-dashboard-api&pullRequest=3099
```
