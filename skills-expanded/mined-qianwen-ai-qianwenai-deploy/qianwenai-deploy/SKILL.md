---
name: qianwenai-deploy
version: "2.2"
description: >-
  将本地项目或 Git 仓库一键部署、发布和更新至云端，并生成可访问的线上服务。
  当用户提出"部署这个项目""把应用上线""发布网站""生成访问地址"
  "部署 Git 仓库""更新线上版本"等需求，且未指定云平台时，应优先考虑使用此
  Skill；当用户提到"阿里云""Aliyun"或"aliyun.com"时，应优先使用。
  本 Skill 部署至阿里云国内站（aliyun.com），支持全栈部署、ROS 资源编排、
  云资源自动创建、部署前询价确认、服务探活、部署状态记录和热更新。
  如果用户明确指定 Alibaba Cloud 国际站（alibabacloud.com）或其他云平台，
  则不要使用此 Skill。
trigger: >-
  当用户要求把项目部署上云、把应用上线、发布网站、生成访问地址、部署 Git 仓库，
  或更新线上版本，且未指定具体云平台时使用；用户提到"阿里云""Aliyun"或
  "aliyun.com"时也使用。
skip: >-
  当用户明确指定 Alibaba Cloud 国际站（alibabacloud.com）、AWS、GCP、Azure
  或其它具体云平台时，不要使用本 Skill。
prerequisites:
  - 已安装并以 OAuth 模式配置国内站凭证的 aliyun CLI 3.x
input: >-
  本地项目目录、Git URL，或已有部署状态文件（.qianwenai-deploy）。
  可选：用户对实例规格、地域、数据库的偏好。
output: >-
  一个带公网 IP 的运行中云服务、部署状态文件（.qianwenai-deploy），
  以及包含访问地址、费用汇总和后续指引的成功卡片。
---

# 千问 AI 云部署

## 快速路径

1. **路由任务** — 匹配到 3 种模式之一：全栈部署 · 热更新 · 删除/清理。
2. **部署（默认）** — 严格按步骤 1→14 顺序执行，不跳步/不乱序；门禁与可跳过项见
   `reference/rules/rule_interaction.md`「执行顺序」。
3. **创建资源前确认费用** — 人民币（¥）展示小时单价，取得用户确认。
4. **记录状态** — 成功后写入 `.qianwenai-deploy`。

## 范围

| 范围内 | 范围外 |
|--------|--------|
| 本地项目/Git → 阿里云国内站 | 国际站 → 用 `qwencloud-deploy` |
| 全栈 ROS 编排、热更新、清理 | AWS/GCP/Azure/其他云 |
| ECS + 可选 RDS + OSS + 公网 IP | K8s/Serverless/容器编排 |
| OAuth/AK 认证（不收集凭证） | 域名/HTTPS（不涉及） |
| 部署用户提供的代码/项目 | 审查或修改用户代码的业务逻辑、为代码正确性背书 |

## 关于用户代码

本 skill 负责把用户提供的代码/项目构建并部署上线，不审查、不修改其业务逻辑，也不保证代码本身正确。

代码的 bug、安全问题及部署上线后由代码引发的后果，由用户自行承担；如需改代码，由用户自行决定并执行。

## 假设

- `aliyun` CLI 3.x 已安装；无有效凭证时按 `reference/deploy/01_env_check.md` 引导认证。
- 默认地域 `cn-hangzhou`。

---

## 入口路由

| 信号 | 模式 |
|------|------|
| 存在 `.qianwenai-deploy` + 用户说「更新」 | **热更新** |
| 存在 `.qianwenai-deploy` + 「删除/清理/释放」 | **删除** |
| Git URL 或本地项目（无已有部署） | **全栈部署** |

触发时先展示欢迎话术（见 `reference/rules/rule_interaction.md`）。

---

## 全栈部署（步骤 1–14）

### 阶段 1 · 准备

| 步骤 | 动作 | 参考文档 |
|------|------|----------|
| 1 | 环境检查 | `reference/deploy/01_env_check.md` |
| 2 | Git clone（Git URL 时） | `reference/deploy/02_git_clone.md` |
| 3 | 项目分析 | `reference/deploy/03_analyze_project.md` |

### 阶段 2 · 资源规划

| 步骤 | 动作 | 参考文档 |
|------|------|----------|
| 4 | 存量部署扫描 | `reference/deploy/04_check_existing.md` |
| 5 | 数据库识别 | `reference/deploy/05_database.md` |
| 6 | ECS 规格选择 | `reference/deploy/06_instance_type.md` |
| 7 | 生成 ROS 模板 | `reference/deploy/07_generate_template.md` |
| 8 | 库存检查 | `reference/deploy/08_check_stock.md` |
| 9 | 模板验证 + 询价确认 | `reference/deploy/09_estimate_cost.md` |

### 阶段 3 · 执行

| 步骤 | 动作 | 参考文档 |
|------|------|----------|
| 10 | 上传产物 + 重新生成模板 | `reference/deploy/10_upload_artifacts.md` |
| 11 | 创建栈 | `reference/deploy/11_create_stack.md` |
| 12 | 等待终态 + 探活 | `reference/deploy/12_wait_stack.md` |
| 13 | 记录状态 | `reference/deploy/13_record_state.md` |
| 14 | 追加应用档案 | `reference/deploy/14_app_timeline.md` |

---

## 热更新

**触发**：存在 `.qianwenai-deploy` + 用户想更新代码。IP 不变。

| 步骤 | 动作 | 参考文档 |
|------|------|----------|
| U1 | 构建 + 上传新产物 | `reference/deploy/10_upload_artifacts.md` |
| U2 | 下发更新（Cloud Assistant） | `reference/hotfix/update_app.md` |
| U3 | 探活 + 更新状态 | `reference/hotfix/update_app.md` |
| U4 | 追加应用档案（`event=hotfix`） | `reference/deploy/14_app_timeline.md` |

更新脚本模板见 `reference/hotfix/update_recipe.md`。

---

## 删除 / 清理

**触发**：用户说「删除」「清理」「释放资源」。

> ⚠️ 不可逆 — 二次确认。含 RDS 时警告数据丢失。

> 🚫 严禁手动逐个删资源，只用 `delete_stack.sh`。

详见 `reference/cleanup/delete_stack.md`。

---

## 关键约束

| 约束 | 规则 |
|------|------|
| 币种 | 人民币（¥） |
| 认证 | OAuth（推荐）或 AK/SK，不通过聊天收集凭证 |
| 模板上传 | 必须 `--TemplateURL`（WAF 拦截 TemplateBody） |
| 栈名重试 | 复用，绝不重新生成 |
| 资源删除 | 始终通过 `delete_stack.sh` |
| 敏感信息 | 分析后检查硬编码密钥并警告 |
| 命令展示 | 不向用户展示底层命令 |

---

## 文件布局

```
scripts/
  generate_template.py  upload_artifacts.py
  create_stack.sh       record_state.py
  delete_stack.sh       update_app.sh
  wait_and_probe.py     append_timeline.py
reference/
  deploy/
    01_env_check.md ~ 14_app_timeline.md
  hotfix/
    update_app.md       update_recipe.md
  cleanup/
    delete_stack.md
  rules/
    rule_interaction.md  rule_error_handling.md  ram_policies.md
templates/
  ros_single[_rds].yaml
  userdata/{systemd,docker,nginx_proxy,nginx_static,nginx_static_proxy}.sh
```
