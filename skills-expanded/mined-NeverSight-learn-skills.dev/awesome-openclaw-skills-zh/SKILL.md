---
name: awesome-openclaw-skills-zh
description: OpenClaw 中文官方技能库 — 翻译自 Clawdbot 官方技能，按场景分类整理，支持中文自然语言调用
triggers:
  - "如何在 OpenClaw 中使用邮件自动化技能"
  - "查找 OpenClaw 办公自动化相关技能"
  - "OpenClaw 有哪些系统工具技能"
  - "如何集成 OpenClaw 技能到我的项目"
  - "查看 OpenClaw 开发运维技能列表"
  - "OpenClaw 技能库支持哪些 AI 工具"
  - "如何使用 OpenClaw 中文技能调用"
  - "查找 OpenClaw 邮件管理技能"
---

# Awesome OpenClaw Skills (中文官方库)

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenClaw 中文官方技能库是一个精心翻译和组织的技能集合，源自 Clawdbot 官方技能库。该项目提供了超过 100+ 个预构建技能，涵盖办公自动化、系统工具、开发运维等多个领域，支持在 QQ、企业微信、飞书、钉钉及本地客户端中使用中文自然语言调用。

## 项目特点

- **中文适配**：所有技能均已适配中文指令，支持自然语言调用
- **场景分类**：按办公自动化、系统工具、开发运维等场景分类
- **持续同步**：与 Clawdbot 官方技能库保持同步更新
- **多平台支持**：支持 QQ/企业微信/飞书/钉钉/本地客户端
- **开箱即用**：无需复杂配置，可直接在 OpenClaw 中调用

## 技能分类体系

### 一、办公自动化 📊

#### 邮件管理
包含邮件收发、邮件搜索、邮件自动化等技能：

```yaml
# Apple Mail 邮件客户端集成示例
技能名称: apple-mail
功能: 适用于 macOS 的 Apple Mail.app 集成
使用场景:
  - 读取收件箱
  - 搜索电子邮件
  - 发送电子邮件
  - 回复和管理消息
```

#### 日历与日程
```yaml
# CalDAV 日历同步示例
技能名称: caldav-calendar
功能: 使用 vdirsyncer + khal 同步和查询 CalDAV 日历
支持平台:
  - iCloud
  - Google Calendar
  - Fastmail
  - Nextcloud
```

#### 文档处理
包含 Google Workspace、Microsoft 365 等文档处理技能。

### 二、系统工具 ⚙️

#### 文件管理
文件操作、备份、同步等功能。

#### 系统监控
系统状态监控、资源使用情况查看等。

#### 网络工具
网络请求、API 调用、数据抓取等。

### 三、开发运维 🛠️

#### 代码开发
代码生成、代码审查、代码格式化等。

#### 部署与 CI/CD
自动化部署、持续集成等功能。

#### 数据库管理
数据库操作、数据迁移等。

## 安装使用

### 浏览技能库

访问项目仓库查看完整技能列表：

```bash
# 克隆仓库
git clone https://github.com/clawdbot-ai/awesome-openclaw-skills-zh.git
cd awesome-openclaw-skills-zh

# 浏览 README 查看技能分类
cat README.md
```

### 在 OpenClaw 中使用

1. **查找所需技能**

在 README 中根据分类找到需要的技能，记下技能的官方链接。

2. **安装技能**

```bash
# 通过 OpenClaw CLI 安装技能（示例）
openclaw skill install clawdhub.com/skills/apple-mail
```

3. **配置环境变量**

根据技能要求配置相应的环境变量：

```bash
# 例如：配置邮件相关的环境变量
export EMAIL_ADDRESS="user@example.com"
export EMAIL_PASSWORD="${EMAIL_PASSWORD}"  # 从环境变量读取
export IMAP_HOST="imap.example.com"
export SMTP_HOST="smtp.example.com"
```

4. **使用中文指令调用**

```python
# 在 Python 中调用示例
from openclaw import Agent

agent = Agent()

# 使用中文自然语言调用
agent.process("帮我搜索最近一周关于项目的邮件")
agent.process("创建一个明天下午3点的会议")
agent.process("查看今天的日程安排")
```

## 常用技能示例

### 邮件管理技能

```python
# 使用 Apple Mail 技能
from openclaw.skills import AppleMailSkill

skill = AppleMailSkill()

# 搜索邮件
emails = skill.search_emails(
    query="项目进展",
    from_date="2024-01-01"
)

# 发送邮件
skill.send_email(
    to="colleague@example.com",
    subject="项目更新",
    body="本周项目进展如下..."
)
```

### Google Workspace 集成

```python
# 使用 Google Workspace 技能（无需 Cloud Console）
from openclaw.skills import GoogleWorkspaceSkill

skill = GoogleWorkspaceSkill()

# OAuth 登录
skill.authenticate()

# 读取 Gmail
messages = skill.gmail.get_messages(query="is:unread")

# 操作 Google Calendar
events = skill.calendar.get_events(
    time_min="2024-01-01T00:00:00Z",
    time_max="2024-01-31T23:59:59Z"
)

# 访问 Google Drive
files = skill.drive.list_files(query="type='application/pdf'")
```

### Microsoft 365 CLI

```python
# 使用 Microsoft 365 技能
from openclaw.skills import Microsoft365Skill

skill = Microsoft365Skill()

# 管理 Outlook 日历
skill.calendar.create_event(
    subject="团队会议",
    start="2024-01-15T14:00:00",
    end="2024-01-15T15:00:00",
    attendees=["team@example.com"]
)

# 发送邮件
skill.mail.send(
    to="manager@example.com",
    subject="周报",
    body="本周工作总结..."
)
```

### 系统监控技能

```python
# 使用 Frigate NVR 监控技能
from openclaw.skills import FrigateSkill

skill = FrigateSkill(
    host="http://frigate.local",
    username="${FRIGATE_USERNAME}",
    password="${FRIGATE_PASSWORD}"
)

# 获取摄像头快照
snapshot = skill.get_snapshot(camera="front_door")

# 检索运动事件
events = skill.get_events(
    camera="driveway",
    after="2024-01-01"
)
```

## 配置文件示例

### 技能配置文件

```yaml
# ~/.openclaw/skills.yaml
skills:
  - name: apple-mail
    enabled: true
    config:
      default_account: "work"
      auto_archive: true
  
  - name: google-workspace-mcp
    enabled: true
    config:
      scopes:
        - gmail.readonly
        - calendar
        - drive.readonly
  
  - name: microsoft-365-cli
    enabled: true
    config:
      tenant_id: "${AZURE_TENANT_ID}"
      client_id: "${AZURE_CLIENT_ID}"
```

### 环境变量配置

```bash
# ~/.openclaw/.env
# 邮件服务配置
EMAIL_ADDRESS=user@example.com
EMAIL_PASSWORD=your_app_password
IMAP_HOST=imap.gmail.com
SMTP_HOST=smtp.gmail.com

# Microsoft 365
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret

# Google Workspace（使用 OAuth，无需 API Key）
# 仅需通过浏览器登录

# 其他服务
DEX_API_KEY=your_dex_api_key
FRIGATE_USERNAME=admin
FRIGATE_PASSWORD=your_password
```

## 技能开发指南

如需为 OpenClaw 开发自定义技能：

```python
# custom_skill.py
from openclaw.skill import Skill

class CustomEmailSkill(Skill):
    """自定义邮件处理技能"""
    
    name = "custom-email-processor"
    description = "高级邮件自动化处理"
    
    def __init__(self):
        super().__init__()
        self.triggers = [
            "处理待办邮件",
            "自动分类邮件",
            "智能回复邮件"
        ]
    
    def process_inbox(self, filters=None):
        """处理收件箱"""
        emails = self.fetch_emails(filters)
        
        for email in emails:
            # 使用 AI 分类
            category = self.classify_email(email)
            
            # 自动处理
            if category == "urgent":
                self.notify_user(email)
            elif category == "spam":
                self.archive_email(email)
            else:
                self.auto_reply(email)
    
    def classify_email(self, email):
        """使用 AI 分类邮件"""
        prompt = f"""
        分类以下邮件：
        主题: {email.subject}
        发件人: {email.from_address}
        内容: {email.body[:500]}
        
        类别: urgent/normal/spam
        """
        return self.ai_classify(prompt)
```

## 常见问题

### 技能安装失败

```bash
# 检查 OpenClaw 版本
openclaw --version

# 更新技能库
openclaw skill update

# 清除缓存重新安装
openclaw skill cache clear
openclaw skill install <skill-name>
```

### 环境变量未生效

```bash
# 检查环境变量是否正确加载
openclaw config show

# 重新加载配置
source ~/.openclaw/.env
openclaw config reload
```

### 技能调用权限问题

```python
# 某些技能需要额外授权
from openclaw import Agent

agent = Agent()

# 授权 Gmail 访问
agent.authorize_skill("google-workspace-mcp", scopes=[
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar"
])
```

### 中文识别不准确

```python
# 配置中文语言模型
agent = Agent(
    language="zh-CN",
    model="gpt-4-turbo",
    temperature=0.3  # 降低温度提高准确性
)
```

## 技能集成最佳实践

### 1. 组合多个技能

```python
from openclaw import Agent, SkillChain

agent = Agent()

# 创建技能链
chain = SkillChain([
    "apple-mail-search",      # 搜索邮件
    "email-template-gen",     # 生成回复
    "apple-mail"              # 发送回复
])

# 执行技能链
result = agent.execute_chain(chain, input={
    "query": "项目相关邮件",
    "action": "auto_reply"
})
```

### 2. 定时任务集成

```python
from openclaw.scheduler import SkillScheduler

scheduler = SkillScheduler()

# 每日早晨汇总邮件
scheduler.add_job(
    skill="morning-email-rollup",
    trigger="cron",
    hour=8,
    minute=0
)

# 每小时检查重要邮件
scheduler.add_job(
    skill="email-prompt-injection-defense",
    trigger="interval",
    hours=1
)
```

### 3. 错误处理

```python
from openclaw.exceptions import SkillError

try:
    result = agent.process("发送邮件给团队")
except SkillError as e:
    print(f"技能执行失败: {e}")
    # 回退到其他技能
    result = agent.process("使用备用邮件服务发送")
```

## 贡献指南

如需贡献新技能或改进翻译：

1. Fork 项目仓库
2. 创建功能分支：`git checkout -b feature/new-skill`
3. 添加或修改技能文档
4. 提交更改：`git commit -m "添加新技能: XXX"`
5. 推送到分支：`git push origin feature/new-skill`
6. 创建 Pull Request

## 相关资源

- **官方技能库**：https://clawdhub.com/skills
- **OpenClaw 文档**：https://openclaw.ai/docs
- **社区论坛**：https://community.openclaw.ai
- **技能开发文档**：https://docs.openclaw.ai/skill-development

## 许可证

本项目遵循原 Clawdbot 官方技能库的许可证要求。请在使用前查看具体技能的许可证信息。
