---
name: tdx-publish
description: AAR 发布自动化 - 更新 FlutterBuild 仓库模板文件，触发 Jenkins 构建。支持单条与批量输入。触发词："发布AAR"、"编译模块"、"更新模板"。
---

# /tdx-publish Skill

> AAR 发布自动化 - 标准 SpectrAI Skill

## 功能描述

实现 QS_Android / TdxFlutter 单模块/批量构建发布自动化。AI 直接调用工具执行，无需外部脚本。

---

## ⚡ 前置检查流程（触发时必须首先执行）

**重要：执行任何发布操作前，必须先完成以下检查。凭据缺失或无效时必须交互式询问用户。**

### Step 0a: 检测并加载凭据

**执行顺序：**

1. **加载 .env 文件**（如果存在）
   ```bash
   if [ -f ~/.env ]; then set -a; source ~/.env; set +a; fi
   ```

2. **检测凭据是否已配置**
   ```bash
   # TFS Git 凭据（支持 PAT Token 或 账号密码）

   if [[ -n "${TFS_GIT_TOKEN:-}" ]]; then
     echo "TFS 认证方式: ✅ PAT Token"
   elif [[ -n "${TFS_USER:-}" && -n "${TFS_PASSWORD:-}" ]]; then
     echo "TFS 认证方式: ✅ 账号密码 (${TFS_USER})"
   else
     echo "TFS 认证方式: ❌ 未配置"
   fi
   ```

3. **如果凭据未配置 → 立即输出以下提示：**

   ```
   ═════════════════════════════════════════════════════════════════
   📋 检测到凭据缺失，请直接回复以下内容（复制粘贴填写）：
   ═════════════════════════════════════════════════════════════════

   TFS_USER=您的TFS用户名
   TFS_PASSWORD=您的TFS密码

   ═════════════════════════════════════════════════════════════════
   💡 说明：
   • TFS_USER/TFS_PASSWORD: TFS Git 登录账号密码
   • Jenkins 无需认证，使用 session cookie + CRUMB 方式触发构建
   ═════════════════════════════════════════════════════════════════
   ```

4. **用户回复后 → 解析并保存到 ~/.env 文件**
   ```bash
   cat > ~/.env << 'EOF'
   TFS_USER=用户输入的值
   TFS_PASSWORD=用户输入的值
   EOF

   set -a; source ~/.env; set +a
   echo "✅ 凭据已保存到 ~/.env"
   ```

### Step 0b: 验证凭据有效性（必须执行）

**⚠️ 重要：即使凭据存在，也必须验证有效性！**

**TFS Git 凭据验证：**
```bash
# 构建认证 URL
if [[ -n "${TFS_GIT_TOKEN:-}" ]]; then
  AUTH_URL="http://${TFS_GIT_TOKEN}@192.168.40.200:8080/tfs/OpenSDK/_git/FlutterBuild"
else
  AUTH_URL="http://${TFS_USER}:${TFS_PASSWORD}@192.168.40.200:8080/tfs/OpenSDK/_git/FlutterBuild"
fi

# 测试能否访问 FlutterBuild 仓库
RESULT=$(git ls-remote "${AUTH_URL}" HEAD 2>&1)

if echo "$RESULT" | grep -q "[0-9a-f]\{40\}"; then
  echo "✅ TFS Git 凭据有效"
else
  echo "❌ TFS Git 凭据无效，请重新输入"
  # 清除无效凭据，重新询问用户
fi
```

**Jenkins 连接验证（使用 session cookie + CRUMB）：**
```bash
# 获取 session cookie
curl -s -c /tmp/jenkins_session.txt -b /tmp/jenkins_session.txt \
  "http://192.168.30.28:8080/" -o /dev/null

# 用同一 session 获取 CRUMB
CRUMB=$(curl -s -c /tmp/jenkins_session.txt -b /tmp/jenkins_session.txt \
  "http://192.168.30.28:8080/crumbIssuer/api/json" | grep -o '"crumb":"[^"]*"' | cut -d'"' -f4)

# 测试触发构建
HTTP_CODE=$(curl -s -c /tmp/jenkins_session.txt -b /tmp/jenkins_session.txt \
  -X POST -H "Jenkins-Crumb: $CRUMB" \
  "http://192.168.30.28:8080/job/QS_Android/buildWithParameters?FILENAME=test&Module=tdxCore" \
  -w "%{http_code}" -o /dev/null)

if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "200" ]; then
  echo "✅ Jenkins 可触发构建（无认证，使用 CRUMB）"
else
  echo "❌ Jenkins 触发失败（HTTP $HTTP_CODE），请检查网络"
fi
```

**验证失败时 → 清除无效凭据，重新执行 Step 0a 询问用户**

### Step 0c: 检测 Git 工具

```bash
git --version
```

---

## 凭据说明

| 凭据 | 说明 | 获取方式 |
|------|------|----------|
| `TFS_USER` | TFS Git 用户名 | TFS 登录账号 |
| `TFS_PASSWORD` | TFS Git 密码 | TFS 登录密码 |
| `TFS_GIT_TOKEN` | TFS Git PAT Token（可选，替代账号密码） | TFS → 用户设置 → Personal Access Tokens |

**Jenkins 无需认证**，使用 session cookie + CRUMB 方式触发构建。

**保存位置：** `~/.env` 或项目目录 `.env`

---

## 触发方式

- **Slash 命令**: `/tdx-publish <template_file> <module> <branch> <commit>`
- **自然语言**: "发布 CCGR-native-beta.txt 中的 tdxCore，分支 master，commit abc123"
- **批量**: `/tdx-publish --input records.json`

---

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| template_file | **是** | 模板文件名，如 `HBZQ-native-beta-2026.txt` |
| module | 是 | 模块名称，如 tdxCore、tdxHQ、tdxframework |
| branch | 是 | Git 分支名 |
| commit | 是 | 构建使用的 commit hash（至少7位） |
| version | **是** | 版本号，如 `6.9.5`，**必填！为空会导致发布到 tmp 仓库** |

**⚠️ 重要：VERSION 参数必填，否则构建产物会发布到 `develop-snapshot-2026-tmp` 临时仓库！**

**Jenkins Module 可选值：**
```
all, tdxtoolutil, tdxCore, tdxCoreSo, tdxframework,
tdxfragmentandactivityutil, tdxHQ, tdxhqdg, tdxhqgg,
tdxjyframingmodule, tdxoemhqmodule, tdxoemjymodule, tdxweex
```

**可选参数:**
- `--dry-run`: 模拟执行，不提交 Git，不触发 Jenkins
- `--skip-jenkins`: 仅更新模板并提交 Git

---

## 模板文件说明

FlutterBuild 仓库地址: `http://192.168.40.200:8080/tfs/OpenSDK/_git/FlutterBuild`

模板文件格式（每行一个模块配置）:
```
// 注释行
tdxCore,master,abc123def,old_commit_hash
tdxHQ,master,xyz789,old_commit_hash
```

---

## 执行流程（AI 直接调用工具）

```
前置检查
├─ 0a. 检测凭据 → 缺失时询问用户 → 保存到 .env
├─ 0b. 检测 Git 工具可用
└─ 0c. 加载凭据到环境变量
      ↓
1. 克隆 FlutterBuild 仓库
   - Bash: git clone http://192.168.40.200:8080/tfs/OpenSDK/_git/FlutterBuild
   - 认证: 使用 TFS_GIT_TOKEN
      ↓
2. 搜索模板文件
   - Glob: 在仓库中搜索匹配 template_file
   - 支持路径: QS_Android/*.txt, *.txt
      ↓
3. 读取模板内容
   - Read: 读取模板文件
      ↓
4. 解析模板
   - 找到 module 对应行
   - 格式: module,branch,commit,old_commit
      ↓
5. 更新模板
   - Edit: 替换该行的 commit 为新值
   - 格式: module,branch,new_commit,old_commit
      ↓
6. Git 提交
   - Bash: git add, git commit, git push
   - commit message: "更新 {module} 到 {new_commit}"
      ↓
7. 触发 Jenkins 构建
   - WebFetch 或 Bash curl: 调用 Jenkins API
   - POST /job/{jenkins_job}/build
   - 认证: JENKINS_USER + JENKINS_TOKEN
      ↓
8. 轮询构建状态
   - 循环调用 Jenkins API 查询状态
   - 间隔: 10秒，最长: 30分钟
   - 状态: SUCCESS / FAILURE / BUILDING
      ↓
9. 获取构建结果
   - 提取 APK 下载链接
      ↓
10. 记录审计日志
   - Write: 写入 logs/{date}.jsonl
      ↓
11. 返回结果给用户
```

---

## 工具调用详解

### Step 1: 克隆仓库

```bash
# 使用 Bash 工具
# 认证方式：PAT Token 或 账号密码
if [[ -n "${TFS_GIT_TOKEN:-}" ]]; then
  git clone "http://${TFS_GIT_TOKEN}@192.168.40.200:8080/tfs/OpenSDK/_git/FlutterBuild" /tmp/FlutterBuild
else
  git clone "http://${TFS_USER}:${TFS_PASSWORD}@192.168.40.200:8080/tfs/OpenSDK/_git/FlutterBuild" /tmp/FlutterBuild
fi

# ⚠️ 重要：配置 Git 编码，避免中文乱码
cd /tmp/FlutterBuild
git config core.quotepath false      # 显示中文文件名
git config i18n.logoutputencoding utf-8
git config i18n.commitencoding utf-8
git config gui.encoding utf-8
```

### Step 2-3: 搜索并读取模板

```javascript
// 使用 Glob 工具搜索
pattern: "**/*CCGR-native-beta.txt"

// 使用 Read 工具读取
file_path: /tmp/FlutterBuild/QS_Android/CCGR-native-beta.txt
```

### Step 4-5: 解析并更新模板

```javascript
// 解析格式: module,branch,commit,old_commit
// 使用 Edit 工具替换
old_string: "tdxCore,master,abc123,old123"
new_string: "tdxCore,master,new456,abc123"
```

### Step 6: Git 提交

```bash
# 使用 Bash 工具
cd /tmp/FlutterBuild

# ⚠️ 重要：确保编码正确（避免中文乱码）
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 添加并提交
git add QS_Android/CCGR-native-beta.txt
git commit -m "更新 tdxCore 到 new456"

# 推送到远程
git push
```

**注意：Windows 环境 Git Bash 需要额外处理：**
```bash
# Windows Git Bash 编码设置
git config --global core.quotepath false
git config --global i18n.logoutputencoding utf-8
git config --global i18n.commitencoding utf-8

# 提交时使用 UTF-8 编码
GIT_AUTHOR_ENCODING=utf-8 GIT_COMMITTER_ENCODING=utf-8 git commit -m "更新 tdxCore"
```

### Step 7-9: Jenkins 操作（使用 session cookie + CRUMB，无需认证）

#### ⚠️ 关键改进：多模块构建队列监控

**问题根源**：Jenkins 触发返回的是 **queueId**（队列ID），不是 buildNumber。
多模块触发时，每个返回不同的 queueId，需要分别监控。

#### Step 7: 触发构建并获取 queueId

```bash
# 获取 session cookie 和 CRUMB
curl -s -c /tmp/jenkins_session.txt -b /tmp/jenkins_session.txt \
  "http://192.168.30.28:8080/" -o /dev/null

CRUMB=$(curl -s -c /tmp/jenkins_session.txt -b /tmp/jenkins_session.txt \
  "http://192.168.30.28:8080/crumbIssuer/api/json" | grep -o '"crumb":"[^"]*"' | cut -d'"' -f4)

# ⚠️ 关键：使用 -i 获取响应头，提取 queueId
# 触发成功返回 201 + Location: http://jenkins/queue/item/{queueId}/
RESPONSE=$(curl -s -i -c /tmp/jenkins_session.txt -b /tmp/jenkins_session.txt \
  -X POST \
  -H "Jenkins-Crumb: $CRUMB" \
  "http://192.168.30.28:8080/job/QS_Android/buildWithParameters?FILENAME=${FILENAME}&Module=${Module}&buildType=Android&VERSION=${VERSION}")

# 提取 queueId（从 Location 头）
QUEUE_URL=$(echo "$RESPONSE" | grep -i "^Location:" | sed 's/Location: //' | tr -d '\r')
QUEUE_ID=$(echo "$QUEUE_URL" | grep -o 'item/[0-9]*' | cut -d'/' -f2)

echo "✅ 触发成功: Module=${Module}, queueId=${QUEUE_ID}"
```

#### Step 8: 多构建状态监控（核心改进）

```bash
# ⚠️ 多模块场景：维护构建状态数组
# 格式: module:queueId:status:buildNumber

BUILD_TRACKER=""  # 初始化构建追踪器

# 函数：从 queueId 获取 buildNumber（修复版）
get_build_from_queue() {
  local queue_id=$1
  local queue_info=$(curl -s -b /tmp/jenkins_session.txt \
    "http://192.168.30.28:8080/queue/item/${queue_id}/api/json")

  # 检查是否已开始执行
  if echo "$queue_info" | grep -q '"executable"'; then
    # ⚠️ 修复：直接从 executable.number 字段提取，不依赖 url 解析
    # JSON 格式: {"executable":{"number":727,"url":"..."}}
    local build_num=$(echo "$queue_info" | grep -o '"executable":{[^}]*"number":[0-9]*' | grep -o '[0-9]*$')
    
    # 备用方案：如果上面失败，从 url 提取
    if [ -z "$build_num" ]; then
      local build_url=$(echo "$queue_info" | grep -o '"url":"[^"]*"' | head -1 | cut -d'"' -f4)
      build_num=$(echo "$build_url" | grep -o '[0-9]*$')
    fi
    
    echo "$build_num"
  else
    # 还在队列中等待
    echo "QUEUED"
  fi
}

# 函数：检查单个构建状态
check_build_status() {
  local module=$1
  local queue_id=$2
  local build_num=$3

  if [ "$build_num" = "QUEUED" ]; then
    # 还在队列中，尝试获取 buildNumber
    local new_build=$(get_build_from_queue "$queue_id")
    if [ "$new_build" != "QUEUED" ]; then
      echo "${module}:${queue_id}:BUILDING:${new_build}"
    else
      echo "${module}:${queue_id}:QUEUED:0"
    fi
  else
    # 已有 buildNumber，查询执行状态
    local build_info=$(curl -s -b /tmp/jenkins_session.txt \
      "http://192.168.30.28:8080/job/QS_Android/${build_num}/api/json")
    local result=$(echo "$build_info" | grep -o '"result":"[^"]*"' | cut -d'"' -f4)

    if [ -z "$result" ] || [ "$result" = "null" ]; then
      echo "${module}:${queue_id}:BUILDING:${build_num}"
    else
      echo "${module}:${queue_id}:${result}:${build_num}"
    fi
  fi
}

# 多模块轮询主循环
# 初始化追踪器（假设触发后已记录）
BUILD_TRACKER="tdxframework:101:QUEUED:0 tdxHQ:102:QUEUED:0 tdxhqgg:103:QUEUED:0"

MAX_ITERATIONS=180  # 30分钟 = 180 * 10秒
ITERATION=0

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
  ITERATION=$((ITERATION + 1))

  # 更新每个构建的状态
  NEW_TRACKER=""
  ALL_DONE=true

  for entry in $BUILD_TRACKER; do
    module=$(echo $entry | cut -d: -f1)
    queue_id=$(echo $entry | cut -d: -f2)
    status=$(echo $entry | cut -d: -f3)
    build_num=$(echo $entry | cut -d: -f4)

    new_entry=$(check_build_status "$module" "$queue_id" "$build_num")
    NEW_TRACKER="$NEW_TRACKER $new_entry"

    new_status=$(echo $new_entry | cut -d: -f3)
    if [ "$new_status" != "SUCCESS" ] && [ "$new_status" != "FAILURE" ]; then
      ALL_DONE=false
    fi
  done

  BUILD_TRACKER="$NEW_TRACKER"

  # 打印进度
  echo "[$ITERATION/$MAX_ITERATIONS] 状态: $BUILD_TRACKER"

  # 如果所有构建完成，退出循环
  if [ "$ALL_DONE" = "true" ]; then
    break
  fi

  sleep 10
done

# 输出最终结果（包含 Maven 下载地址）
echo "══════════════════════════════════════════════════════════"
echo "构建完成汇总:"

# 收集成功的构建号
SUCCESS_BUILDS=""

for entry in $BUILD_TRACKER; do
  module=$(echo $entry | cut -d: -f1)
  status=$(echo $entry | cut -d: -f3)
  build_num=$(echo $entry | cut -d: -f4)
  
  echo "  ${module}: ${status} (build #${build_num})"
  
  if [ "$status" = "SUCCESS" ]; then
    SUCCESS_BUILDS="$SUCCESS_BUILDS $build_num"
  fi
done

echo "══════════════════════════════════════════════════════════"

# 获取 Maven 下载地址（从构建日志解析）
if [ -n "$SUCCESS_BUILDS" ]; then
  echo ""
  echo "正在获取 Maven 发布地址..."
  
  for build_num in $SUCCESS_BUILDS; do
    maven_info=$(get_maven_info "$build_num")
    echo ""
    echo "📦 构建 #${build_num}:"
    echo "$maven_info"
  done
fi
```

#### 函数：获取 Maven 下载地址（从构建日志解析）

**⚠️ 重要：AAR 发布到 Artifactory Maven 仓库，不是 Jenkins artifacts！**

```bash
# 从构建日志解析 Artifactory Maven 发布地址
get_maven_url() {
  local build_num=$1
  
  # 获取完整构建日志
  local log_content=$(curl -s -b /tmp/jenkins_session.txt \
    "http://192.168.30.28:8080/job/QS_Android/${build_num}/consoleText")
  
  # 解析 Artifactory 发布地址
  # 格式: Deploying artifact: http://192.168.40.200:8081/artifactory/develop-snapshot-2026/tdx/android/aar/xxx/版本号/xxx.aar
  
  local maven_url=$(echo "$log_content" | grep -o 'Deploying artifact: http[^ ]*\.aar' | head -1 | sed 's/Deploying artifact: //')
  
  if [ -n "$maven_url" ]; then
    echo "$maven_url"
  else
    echo "未找到 Maven 发布地址"
  fi
}

# 获取完整的 Maven 信息（名称、版本号、下载地址）
get_maven_info() {
  local build_num=$1
  
  local log_content=$(curl -s -b /tmp/jenkins_session.txt \
    "http://192.168.30.28:8080/job/QS_Android/${build_num}/consoleText")
  
  # 解析 artifactoryPublish 任务输出
  # 格式: > Task :tdxframework:artifactoryPublish
  #       [pool-5-thread-1] Deploying artifact: http://.../tdxframework_XNZQL2/4.5-2604140829/tdxframework_XNZQL2-4.5-2604140829.aar
  
  local module_name=$(echo "$log_content" | grep -o '> Task :[^:]*:artifactoryPublish' | cut -d':' -f3)
  local maven_url=$(echo "$log_content" | grep -o 'Deploying artifact: http[^ ]*\.aar' | head -1 | sed 's/Deploying artifact: //')
  
  # 从 URL 提取版本号
  # URL 格式: .../tdxframework_XNZQL2/4.5-2604140829/tdxframework_XNZQL2-4.5-2604140829.aar
  local version=$(echo "$maven_url" | grep -o '/[0-9]\+-[0-9]\+/' | tr -d '/')
  
  echo "模块: ${module_name}"
  echo "版本: ${version}"
  echo "下载: ${maven_url}"
}

# 批量获取多个构建的 Maven 信息
get_all_maven_info() {
  local build_nums=$1  # 格式: "727 728 729"
  
  echo "═══════════════════════════════════════════════════════════════════"
  echo "AAR 发布结果汇总:"
  echo "═══════════════════════════════════════════════════════════════════"
  
  for build_num in $build_nums; do
    info=$(get_maven_info "$build_num")
    echo ""
    echo "构建 #${build_num}:"
    echo "$info"
  done
  
  echo "═══════════════════════════════════════════════════════════════════"
}
```

#### 输出示例（构建完成后）

```
═══════════════════════════════════════════════════════════════════
AAR 发布结果汇总:
═══════════════════════════════════════════════════════════════════

构建 #727:
模块: tdxframework
版本: 4.5-2604140829
下载: http://192.168.40.200:8081/artifactory/develop-snapshot-2026/tdx/android/aar/tdxframework_XNZQL2/4.5-2604140829/tdxframework_XNZQL2-4.5-2604140829.aar

构建 #728:
模块: tdxHQ
版本: 4.5-2604140829
下载: http://192.168.40.200:8081/artifactory/develop-snapshot-2026/tdx/android/aar/tdxhq_master-xnzq/4.5-2604140829/tdxhq_master-xnzq-4.5-2604140829.aar

构建 #729:
模块: tdxhqgg
版本: 4.5-2604140829
下载: http://192.168.40.200:8081/artifactory/develop-snapshot-2026/tdx/android/aar/tdxhqgg_XNZQL2/4.5-2604140829/tdxhqgg_XNZQL2-4.5-2604140829.aar

═══════════════════════════════════════════════════════════════════
```

**⚠️ 注意：Jenkins artifacts API 不适用于 Maven 发布的 AAR，必须从构建日志解析！**

#### 输出示例（构建完成后）

```
══════════════════════════════════════════════════════════
构建完成汇总:
  tdxframework: SUCCESS (build #145)
    📦 下载: http://192.168.30.28:8080/job/QS_Android/145/artifact/output/tdxframework-4.5.aar
  tdxHQ: SUCCESS (build #146)
    📦 下载: http://192.168.30.28:8080/job/QS_Android/146/artifact/output/tdxHQ-4.5.aar
  tdxhqgg: SUCCESS (build #147)
    📦 下载: http://192.168.30.28:8080/job/QS_Android/147/artifact/output/tdxhqgg-4.5.aar
══════════════════════════════════════════════════════════
```

#### 单模块简化版（向后兼容）

```bash
# 单模块场景：简化逻辑
QUEUE_ID=$(curl -s -i -X POST -H "Jenkins-Crumb: $CRUMB" \
  "...buildWithParameters?..." | grep -i "^Location:" | grep -o 'item/[0-9]*' | cut -d'/' -f2)

# 等待队列 -> 执行
while true; do
  build_num=$(get_build_from_queue "$QUEUE_ID")
  if [ "$build_num" != "QUEUED" ]; then
    break
  fi
  sleep 5
done

# 轮询执行状态
while true; do
  status=$(curl -s "...job/QS_Android/${build_num}/api/json" | grep -o '"result":"[^"]*"' | cut -d'"' -f4)
  if [ -n "$status" ] && [ "$status" != "null" ]; then
    break
  fi
  sleep 10
done
```

**⚠️ 关键：VERSION 参数必须明确传递，不能为空！**

### Step 10: 审计日志

```javascript
// 使用 Write 工具
file_path: logs/2026-04-07.jsonl
content: {
  "timestamp": "2026-04-07T12:00:00Z",
  "template_file": "CCGR-native-beta.txt",
  "module": "tdxCore",
  "commit": "new456",
  "jenkins_build": 145,
  "status": "success"
}
```

---

## 返回结果格式

### 成功

```json
{
  "success": true,
  "template_file": "CCGR-native-beta.txt",
  "module": "tdxCore",
  "commit": "a1b2c3d4",
  "jenkins": {
    "build_number": 145,
    "build_url": "http://jenkins/job/xxx/145/",
    "apk_url": "..."
  }
}
```

### 失败

```json
{
  "success": false,
  "error_code": "E-JEN-05",
  "error_message": "Jenkins 构建失败"
}
```

---

## Jenkins Job 映射

模板文件名 → Jenkins Job 名称（从 configs/jenkins.yaml 读取）:

| 模板文件 | Jenkins Job |
|---------|-------------|
| CCGR-native-beta.txt | QS_Android-CCGR-build |
| SJZQ.txt | TdxFlutter-SJZQ-build |

---

## 错误处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| E-AUTH-01 | 凭据缺失 | 询问用户输入 |
| E-GIT-01 | Git 未安装 | 提示安装 Git |
| E-GIT-03 | 克隆失败 | 检查网络和 Token |
| E-CFG-03 | 模板不存在 | 检查文件名 |
| E-JEN-01 | Jenkins 不可达 | 检查网络 |
| E-JEN-05 | 构建失败 | 查看日志 |

---

## 批量发布

### 支持的批量输入格式

#### 格式1：直接粘贴模板内容（推荐）

用户可直接粘贴模板文件内容，AI 自动解析：

```
XNZQ-native-beta.txt
tdxframework XNZQL2 99655b57ddfad71da8c35cf16ca0ee08a7922445 4.5
tdxHQ master-xnzq 5df3c336068dc43be81bdb1c50e791eaf8a90035 4.5
tdxhqgg XNZQL2 9acc73b5d769524dfe4cd160acd29b5e55a8a1bb 4.5
```

**解析规则：**
- 第一行：模板文件名（必须以 `.txt` 结尾）
- 后续行：`module branch commit version`（空格分隔）
- 支持注释行（以 `//` 或 `#` 开头）

#### 格式2：records.json 文件

```json
{
  "records": [
    {"template_file": "CCGR-native-beta.txt", "module": "tdxCore", "branch": "master", "commit": "abc123", "version": "6.9.5"},
    {"template_file": "CCGR-native-beta.txt", "module": "tdxTrade", "branch": "master", "commit": "def456", "version": "6.9.5"}
  ]
}
```

#### 格式3：命令行参数（单模块）

```
/tdx-publish HBZQ-native-beta-2026.txt tdxCore master 6af7a8a6 6.9.5
```

### 批量执行策略

**⚠️ 多模块触发策略改进：**

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **并行触发** | 同时触发所有模块，记录 queueId，统一监控 | 推荐：效率最高 |
| **串行触发** | 触发→等待完成→下一个 | 单模块或需要顺序控制 |

**推荐流程（并行触发）：**
```
1. 解析批量输入 → 提取所有模块配置
2. 并行触发所有模块 → 记录每个 queueId
   ├── tdxframework → queueId=101
   ├── tdxHQ → queueId=102
   └── tdxhqgg → queueId=103
3. 统一轮询监控 → 检查所有构建状态
4. 汇总结果 → 输出每个模块的构建状态
```

### AI 执行指令

当检测到多模块输入时：

```
1. 识别模板文件名和模块列表
2. 逐个触发 Jenkins（使用 Bash 并行或快速串行）
3. 每次触发后立即提取 queueId
4. 维护 BUILD_TRACKER 数组
5. 统一轮询直到所有完成
6. 汇总输出结果
7. ⚠️ 更新使用频率统计到 logs/usage-stats.json
```

---

## 使用频率学习机制

### 学习原理

每次执行后，技能会记录使用频率，动态调整示例排序：

**记录内容：**
- 模板文件名使用次数
- 模块名使用次数
- 最近使用时间

### 学习触发时机

| 触发点 | 操作 |
|--------|------|
| 构建成功 | 更新模板文件、模块的使用计数 |
| 执行结束 | 写入 `logs/usage-stats.json` |

### 统计文件格式

`logs/usage-stats.json`:
```json
{
  "template_files": {
    "XNZQ-native-beta.txt": {"count": 15, "last_used": "2026-04-14"},
    "HBZQ-native-beta-2026.txt": {"count": 10, "last_used": "2026-04-10"},
    "CCGR-native-beta.txt": {"count": 5, "last_used": "2026-04-08"}
  },
  "modules": {
    "tdxframework": {"count": 20, "last_used": "2026-04-14"},
    "tdxHQ": {"count": 18, "last_used": "2026-04-14"},
    "tdxCore": {"count": 12, "last_used": "2026-04-10"},
    "tdxhqgg": {"count": 8, "last_used": "2026-04-14"}
  },
  "combinations": {
    "XNZQ-native-beta.txt+tdxframework": {"count": 10},
    "XNZQ-native-beta.txt+tdxHQ": {"count": 8}
  }
}
```

### AI 动态示例生成

**每次触发时，AI 应按频率排序示例：**

```
# 高频使用示例（自动推荐）
/tdx-publish XNZQ-native-beta.txt tdxframework XNZQL2 <commit> 4.5
/tdx-publish XNZQ-native-beta.txt tdxHQ master-xnzq <commit> 4.5

# 或批量（高频组合）
XNZQ-native-beta.txt
tdxframework XNZQL2 <commit> 4.5
tdxHQ master-xnzq <commit> 4.5
tdxhqgg XNZQL2 <commit> 4.5
```

### 学习执行指令

```bash
# Step 11: 更新使用统计（构建成功后执行）
STATS_FILE="logs/usage-stats.json"

# 如果文件不存在，创建初始结构
if [ ! -f "$STATS_FILE" ]; then
  echo '{"template_files":{}, "modules":{}, "combinations":{}}' > "$STATS_FILE"
fi

# 使用 jq 更新统计（如果可用）
# 或使用简单的方式追加到审计日志
```

### 示例展示策略

**当用户询问"如何使用"或触发技能时：**

1. **检查 `logs/usage-stats.json` 是否存在**
2. **按 count 降序排列模板文件和模块**
3. **生成高频示例展示给用户**
4. **首次使用时展示默认示例**

---

## 常用示例（动态区域）

> ⚠️ 此区域由学习机制动态更新，手动编辑可能被覆盖

### 高频模板文件

| 模板文件 | 使用次数 | 最近使用 |
|---------|---------|----------|
| XNZQ-native-beta.txt | 15 | 2026-04-14 |
| HBZQ-native-beta-2026.txt | 10 | 2026-04-10 |

### 高频模块

| 模块 | 使用次数 | 最近使用 |
|------|---------|----------|
| tdxframework | 20 | 2026-04-14 |
| tdxHQ | 18 | 2026-04-14 |
| tdxhqgg | 8 | 2026-04-14 |

### 快速使用示例

```
# 单模块发布（高频）
/tdx-publish XNZQ-native-beta.txt tdxframework XNZQL2 abc123def 4.5

# 批量发布（高频组合）
XNZQ-native-beta.txt
tdxframework XNZQL2 99655b57ddfad71da8c35cf16ca0ee08a7922445 4.5
tdxHQ master-xnzq 5df3c336068dc43be81bdb1c50e791eaf8a90035 4.5
tdxhqgg XNZQL2 9acc73b5d769524dfe4cd160acd29b5e55a8a1bb 4.5
```

---

## 配置文件

项目包含 `configs/` 目录，提供以下配置：

| 文件 | 作用 |
|------|------|
| jenkins.yaml | Jenkins 服务器 URL 和 Job 映射 |
| tfs.yaml | TFS 仓库地址 |

---

## 安装方式

```bash
# 从 Git 仓库安装
npx skills add https://github.com/your-org/tdx-publish-skill --skill tdx-publish

# 或在 SpectrAI 中直接导入 skill 目录
```

---

## 触发关键词

| 关键词 | 功能 |
|--------|------|
| 发布 AAR、发布模块 | 单模块发布 |
| 批量发布、批量构建 | 批量发布 |
| 检查凭据 | 检测凭据配置 |

---

> **更新日期**: 2026-04-14
> **类型**: prompt（纯 Skill）
> **改进版本**: v2.1
> **最近更新**:
> - 修复 queueId → buildNumber 转换逻辑（直接从 executable.number 字段提取）
> - 修复下载地址获取：AAR 发布到 Artifactory Maven 仓库，从构建日志解析（不是 Jenkins artifacts）
> - 新增 get_maven_url/get_maven_info 函数从 consoleText 解析发布地址
> - 输出包含模块名、版本号、Maven 下载地址完整信息