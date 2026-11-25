---
name: redpacket-claim
description: 全自动红包领取技能。当用户输入红包口令（如'天天开心'、'恭喜发财'等）时，自动检测并尝试在支持的平台上领取红包。支持微信、支付宝、QQ、抖音等主流平台，自动选择最佳领取方式。
triggers:
  - 红包口令
  - 抢红包
  - 红包领取
  - 口令红包
metadata:
  clawdbot:
    emoji: 🩺
  openclaw:
    requires:
      bins: [python3, curl]
    primaryEnv: REDPACKET_CONFIG
---

# 红包自动领取技能

全自动检测和领取红包口令，支持多平台智能选择。

## 快速开始

当用户输入类似以下内容时自动触发：
- "红包口令：天天开心"
- "抢红包：恭喜发财"
- "领取红包：新年快乐"
- 直接输入口令："大吉大利"

## 工作原理

1. **口令检测**：从用户消息中提取红包口令
2. **平台识别**：根据上下文识别目标平台（默认按微信→支付宝→QQ顺序尝试）
3. **自动领取**：使用最适合的方式尝试领取
4. **结果反馈**：返回领取结果和状态

## 配置

### 环境变量
```bash
export REDPACKET_CONFIG='{"platforms": ["wechat", "alipay", "qq"], "timeout": 30, "retry": 2}'
```

### 配置文件（可选）
在 `/root/.openclaw/redpacket-config.json` 中配置：
```json
{
  "platforms": ["wechat", "alipay", "qq", "douyin"],
  "priority": "wechat",
  "timeout": 30,
  "max_retries": 3,
  "browser": "chrome",
  "headless": false,
  "user_agents": [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42"
  ]
}
```

## 使用示例

### 场景1：直接输入口令
**用户输入**：
```
大吉大利
```

**AI自动响应**：
```
检测到红包口令：大吉大利
正在尝试领取...
✅ 成功在微信领取红包！
💰 金额：8.88元
⏰ 领取时间：2026-02-11 20:10:23
```

### 场景2：带平台指定
**用户输入**：
```
支付宝红包：新年快乐
```

**AI自动响应**：
```
检测到支付宝红包口令：新年快乐
正在支付宝平台领取...
✅ 支付宝红包领取成功！
💰 金额：5.20元
📱 已存入余额
```

### 场景3：多平台尝试
**用户输入**：
```
抢红包：恭喜发财
```

**AI自动响应**：
```
检测到红包口令：恭喜发财
尝试平台：微信 → 支付宝 → QQ
🔍 微信：未找到对应红包
✅ 支付宝：领取成功！
💰 金额：2.88元
```

## 支持平台

### 1. 微信红包
- **检测方式**：用户消息包含"微信"或上下文在微信对话中
- **领取方法**：模拟微信客户端请求
- **依赖**：需要登录态（通过配置文件设置）

### 2. 支付宝红包
- **检测方式**：消息包含"支付宝"、"Alipay"或支付宝口令格式
- **领取方法**：支付宝小程序/网页接口
- **特点**：支持余额直接到账

### 3. QQ红包
- **检测方式**：消息包含"QQ"或QQ群聊环境
- **领取方法**：QQ红包接口
- **注意**：需要QQ登录状态

### 4. 抖音/快手红包
- **检测方式**：消息包含"抖音"、"快手"、"TikTok"
- **领取方法**：APP内自动化
- **依赖**：需要Android自动化支持

### 5. 通用平台
- **检测方式**：无法识别具体平台时
- **领取方法**：智能猜测 + 多平台尝试
- **策略**：按用户历史偏好选择

## 脚本使用

### 主脚本
```bash
# 直接调用领取脚本
python3 scripts/claim_redpacket.py \
  --code "天天开心" \
  --platform wechat \
  --config /root/.openclaw/redpacket-config.json

# 多平台尝试
python3 scripts/claim_redpacket.py \
  --code "恭喜发财" \
  --platform auto \
  --timeout 30 \
  --retry 3
```

### 参数说明
| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--code` | `-c` | 是 | - | 红包口令 |
| `--platform` | `-p` | 否 | `auto` | 平台：wechat, alipay, qq, douyin, kuaishou, auto |
| `--config` | `-C` | 否 | `~/.openclaw/redpacket-config.json` | 配置文件路径 |
| `--timeout` | `-t` | 否 | `30` | 超时时间（秒） |
| `--retry` | `-r` | 否 | `2` | 重试次数 |
| `--headless` | `-H` | 否 | `false` | 无头模式（不显示浏览器） |
| `--verbose` | `-v` | 否 | `false` | 详细日志输出 |

## 高级功能

### 1. 智能上下文识别
- 根据对话来源（微信/QQ/Telegram等）自动选择平台
- 记忆用户偏好平台
- 学习用户常用红包类型

### 2. 多账号支持
```json
{
  "accounts": {
    "wechat": ["token1", "token2"],
    "alipay": ["user1", "user2"],
    "qq": ["qq1", "qq2"]
  },
  "strategy": "round-robin"
}
```

### 3. 定时领取
可结合 OpenClaw cron 定时检查新红包：
```bash
openclaw cron add \
  --name "redpacket-monitor" \
  --every 5m \
  --command "python3 scripts/monitor.py"
```

### 4. 统计报表
```bash
# 查看领取统计
python3 scripts/stats.py --period week

# 导出数据
python3 scripts/stats.py --export csv --output redpacket-stats.csv
```

## 安全与隐私

### 存储安全
- 登录令牌加密存储
- 本地配置文件权限限制
- 临时数据自动清理

### 使用限制
- 单用户频率限制：60次/小时
- 单IP频率限制：100次/小时
- 异常行为自动暂停

### 隐私保护
- 不存储红包金额详情
- 不记录用户敏感信息
- 可配置数据保留期限

## 故障排除

### 常见问题
1. **领取失败**：检查网络连接和登录状态
2. **口令无效**：确认口令未过期且格式正确
3. **平台不支持**：查看支持的平台列表
4. **频率限制**：等待限制解除或切换账号

### 调试模式
```bash
python3 scripts/claim_redpacket.py --code "测试" --platform wechat --verbose --headless false
```

### 查看日志
```bash
tail -f /tmp/redpacket-claim.log
```

## 扩展开发

### 添加新平台
1. 在 `references/platforms.md` 中添加平台文档
2. 在 `scripts/platforms/` 下添加平台实现
3. 更新配置文件验证逻辑

### 集成其他工具
- 结合 `agent-browser` 进行复杂网页自动化
- 使用 `nodes` tool 控制手机端APP
- 集成 `cron` 定时任务管理

## 免责声明

本技能仅用于学习和技术研究，请遵守：
1. 各平台用户协议
2. 相关法律法规
3. 尊重他人合法权益
4. 不用于恶意抢红包或干扰平台正常运行

---

**触发关键词**：红包口令、抢红包、领取红包、口令红包、红包码
**适用场景**：微信群、QQ群、支付宝聊天、社交媒体等
**自动化级别**：全自动（检测到口令即触发）
