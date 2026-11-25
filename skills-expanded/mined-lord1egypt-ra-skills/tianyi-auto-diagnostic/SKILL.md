---
clawdbot:
  name: auto-diagnostic
  version: 1.0.0
  requires.env: []
  files: ["scripts/*"]
  homepage: https://github.com/openclaw_ceo/skills/auto-diagnostic
---

# Auto-Diagnostic - 自动诊断技能

> 自动诊断 OpenClaw 运行时问题并驱动修复


# Auto-Diagnostic 技能

自动诊断 OpenClaw 运行时问题并驱动修复。

## 核心流程

### 1. 问题识别

当用户报告问题或检测到异常时：

1. 收集上下文：
   - 读取相关日志：`\tmp\openclaw\openclaw-*.log`
   - 检查服务状态：`openclaw gateway status`、`openclaw browser status`
   - 读取配置文件：`~\.openclaw\openclaw.json`

2. 识别错误模式：
   - `token_mismatch` / `unauthorized` → 认证问题
   - `ECONNREFUSED` / `connect failed` → 连接问题
   - `JSON5 parse failed` → 配置语法错误
   - `port already in use` → 端口冲突
   - `extension not found` → 扩展未安装

### 2. 根因分析

根据错误类型匹配解决方案：

| 错误模式 | 根因 | 解决方案 |
|----------|------|----------|
| `token_mismatch` | 网关令牌不匹配 | 更新 `gateway.auth.token` 并重启网关 |
| `ECONNREFUSED:18792` | Relay 服务未启动 | 检查网关状态，确认 `gateway.mode: local` |
| `JSON5 parse failed` | 配置文件语法错误 | 用 `openclaw doctor --fix` 修复 |
| `port already in use` | 端口被占用 | 停止旧进程或更换端口 |
| `extension not installed` | Chrome 扩展未加载 | 运行 `openclaw browser extension install` |

### 3. 执行修复

调用相关技能或直接执行修复命令：

```powershell
# 示例：修复令牌问题
$config = Get-Content ~\.openclaw\openclaw.json -Raw
# 更新 gateway.auth.token 字段
$config | Set-Content ~\.openclaw\openclaw.json
openclaw gateway restart

# 示例：安装扩展
openclaw browser extension install
```

### 4. 验证修复

修复后执行验证：

```powershell
openclaw gateway status
openclaw browser status
```

确认服务恢复正常。

## 脚本工具

### scripts/diagnose.ps1

自动诊断脚本：

```powershell
param(
    [string]$Category = "all"  # gateway, browser, config, all
)

$ErrorLog = Get-Content "\tmp\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log" -Tail 50 -ErrorAction SilentlyContinue

if ($Category -in @("all", "gateway")) {
    Write-Host "=== Gateway Status ==="
    openclaw gateway status 2>&1 | Select-String -Pattern "Listening|failed|error" -Context 2
}

if ($Category -in @("all", "browser")) {
    Write-Host "=== Browser Status ==="
    openclaw browser status 2>&1
}

if ($ErrorLog) {
    Write-Host "=== Recent Errors ==="
    $ErrorLog | Select-String -Pattern "error|failed|unauthorized|exception" -Context 1
}
```

## 参考文档

### references/error-patterns.md

常见错误模式及解决方案：

#### 1. 认证错误

```
Error: unauthorized: gateway token mismatch
```

**原因**: 扩展程序/CLI 的令牌与网关配置不匹配

**解决**:
1. 检查 `openclaw.json` 中 `gateway.auth.token`
2. 在扩展程序选项中填入相同令牌
3. 重启网关：`openclaw gateway restart`

#### 2. 连接拒绝

```
ECONNREFUSED 127.0.0.1:18792
```

**原因**: Relay 服务未启动（网关未运行或非 local 模式）

**解决**:
1. `openclaw gateway status` 确认网关运行
2. 检查 `gateway.mode: local`
3. 启动网关：`openclaw gateway start`

#### 3. 配置解析失败

```
JSON5: invalid character '，' at line X:Y
```

**原因**: 配置文件包含中文标点或语法错误

**解决**:
1. `openclaw doctor --fix` 自动修复
2. 手动检查指定行的标点符号

#### 4. 端口占用

```
Port 18789 is already in use by pid XXXXX
```

**原因**: 网关进程重复启动

**解决**:
1. `Stop-Process -Id XXXXX -Force`
2. 或 `openclaw gateway stop` 后重新启动

## 触发条件

以下情况应触发本技能：

- 用户报告"连接失败"、"无法使用"、"出错了"
- 检测到 `unauthorized`、`failed`、`error` 等关键词
- 服务状态检查返回异常
- 配置验证失败
- 技能调用链中出现连续失败

## 输出格式

诊断结果应包含：

1. **问题摘要**: 一句话描述核心问题
2. **根因分析**: 导致问题的具体原因
3. **已执行操作**: 已尝试的修复步骤
4. **后续建议**: 需要用户配合的操作（如有）
5. **预防建议**: 如何避免类似问题再次发生

示例：

```
【诊断结果】
问题：Chrome 扩展连接失败（红色!标记）
根因：网关令牌配置为空，扩展程序填入的令牌不匹配

【已执行】
✅ 更新 gateway.auth.token = "tianyi2026"
✅ 重启网关服务

【需用户操作】
1. 在扩展程序选项中填入令牌：tianyi2026
2. 点击保存后重新连接

【预防建议】
令牌变更后需同步更新扩展程序配置
```

---

## ?? ȫ˽

### External Endpoints

| ˵ | ݷ | ; |
|------|----------|------|
|  () | 뿪 | вڱִ |

### Security & Privacy

- ? **ⲿ API ** - ݱڱ
- ? **־ȡֻ** - ޸־ļ
- ? **޸Ȩ** - ñûȷ
- ? **͸** - ϲͽɼ

### Model Invocation Note

ͨ OpenClaw  AI ģͽУ
- ־
- ʶ
- ޸

ģ͵еı׼Ϊ OpenClaw  utoInvoke: false á

### Trust Statement

**By using this skill:**
- ݱıػ
- ݷ͵
- ޸ֶȨ
- űȫ͸

** OpenClaw ̬ϵͳͱܴʱװ**

---

*Զϣ޸*
