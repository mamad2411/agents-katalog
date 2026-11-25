---
name: mx-skills-suite-v2
description: >
  东方财富妙想金融技能套件（增强版），包含 5 个专业金融子技能：
  1. eastmoney_fin_data - 金融数据查询（行情、财务、关联关系）
  2. eastmoney_fin_search - 金融资讯搜索（新闻、公告、研报、政策）
  3. mx_select_stock - 智能选股（条件筛选、板块查询、股票推荐）
  4. mx_self_select - 自选股管理（查询、添加、删除自选股）
  5. eastmoney_stock_simulator - 模拟组合管理（持仓、买卖、撤单、委托、资金）
  
  ✨ 增强特性：配置文件持久化保存到 ~/.config/eastmoney-mx-skills/.env
  
  触发词：东方财富、妙想、金融数据、行情查询、股票资讯、选股、自选股、模拟交易、模拟炒股、持仓查询、东方财富数据、东方财富API。
author: Community (based on 东方财富妙想团队 original work)
version: 2.1.0
required_env_vars:
  - MX_APIKEY
credentials:
  - type: api_key
    name: MX_APIKEY
    description: 从东方财富妙想平台获取的 API Key，首次使用需注册获取
    setup_url: "https://marketing.dfcfs.com/views/finskillshub/indexyrxc2vtv?mksharest=1773325711118"
metadata:
  openclaw:
    primaryEnv: MX_APIKEY
    configPath: ~/.config/eastmoney-mx-skills/.env
    homepage: https://www.eastmoney.com
    requires:
      bins:
        - python3
      env:
        - MX_APIKEY
persistence:
  readWrite:
    - ~/.config/eastmoney-mx-skills/.env
    - ~/.openclaw/logs/mx_skills/
---

# mx-skills-suite-v2 - 东方财富妙想金融技能套件（增强版）

本技能套件基于**东方财富妙想平台 API**构建，提供一站式金融数据查询、资讯搜索、智能选股、自选股管理和模拟交易功能。

## ✨ 增强特性

相比原版，本版本增加了：
- **配置文件持久化**：配置保存在 `~/.config/eastmoney-mx-skills/.env`
- **Setup 脚本**：提供交互式配置向导 `bash setup.sh`
- **多账户支持**：支持配置多个东方财富账户
- **配置优先级**：配置文件 > 环境变量

## 包含的子技能

| # | 技能名称 | 功能说明 | 详细文档 |
|---|---------|---------|---------|
| 1 | **eastmoney_fin_data** | 金融数据查询：股票/行业/板块/指数/基金/债券的实时行情、主力资金、估值、财务指标、股东结构等 | `references/mx-data.md` |
| 2 | **eastmoney_fin_search** | 金融资讯搜索：新闻、公告、研报、政策、交易规则、事件分析等时效性信息 | `references/mx-search.md` |
| 3 | **mx_select_stock** | 智能选股：基于行情/财务指标条件筛选股票、板块成分股查询、股票推荐 | `references/mx-select-stock.md` |
| 4 | **mx_self_select** | 自选股管理：查询/添加/删除东方财富通行证账户下的自选股 | `references/mx-selfselect.md` |
| 5 | **eastmoney_stock_simulator** | 模拟组合管理：持仓查询、买卖操作、撤单、委托查询、资金查询 | `references/mx-stock-simulator.md` |

## 快速开始

### 方式一：使用 Setup 脚本（推荐）

```bash
cd /path/to/eastmoney-mx-skills-suite-v2
bash setup.sh
```

按提示输入您的 MX_APIKEY，配置将自动保存到 `~/.config/eastmoney-mx-skills/.env`

### 方式二：手动配置

创建配置文件：

```bash
mkdir -p ~/.config/eastmoney-mx-skills
cat > ~/.config/eastmoney-mx-skills/.env << 'EOF'
# 东方财富妙想金融技能套件配置文件
MX_APIKEY=your_api_key_here
EOF
chmod 600 ~/.config/eastmoney-mx-skills/.env
```

### 方式三：环境变量

```bash
export MX_APIKEY=your_api_key_here
```

## 获取 API Key

1. 访问：**https://marketing.dfcfs.com/views/finskillshub/indexyrxc2vtv?mksharest=1773325711118**
2. 下载并安装东方财富 APP
3. 注册/登录后，在首页搜索 **Skill**，领取 **API KEY**

## 配置文件说明

配置文件路径：`~/.config/eastmoney-mx-skills/.env`

### 配置文件格式

```bash
# 默认账户配置
MX_APIKEY=your_api_key_here

# API 基础配置（可选）
MX_BASE_URL=https://mkapi2.dfcfs.com/finskillshub/api/claw/query
MX_TIMEOUT=30

# 多账户配置示例（账户名前缀）
WORK_MX_APIKEY=your_work_api_key
PERSONAL_MX_APIKEY=your_personal_api_key
```

### 配置优先级

1. 脚本参数 `--api-key`
2. 配置文件 `~/.config/eastmoney-mx-skills/.env`
3. 环境变量 `MX_APIKEY`

## 使用方式

根据用户请求自动匹配对应子技能：

- **查行情/财务数据** → 加载 `references/mx-data.md`
- **搜新闻/研报/公告** → 加载 `references/mx-search.md`
- **筛选股票/选股** → 加载 `references/mx-select-stock.md`
- **管理自选股** → 加载 `references/mx-selfselect.md`
- **模拟交易/查持仓** → 加载 `references/mx-stock-simulator.md`

## API 基础信息

- **API 域名**: `https://mkapi2.dfcfs.com/finskillshub`
- **认证方式**: HTTP Header `apikey: {MX_APIKEY}`
- **请求方法**: 所有接口均使用 `POST`
- **Content-Type**: `application/json`

## 错误码说明

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 113 | 调用次数达上限 | 提示用户等待或更新 API Key |
| 114 | API 密钥失效 | 提示用户重新获取 Key |
| 115 | 未携带密钥 | 提示用户配置 `MX_APIKEY` |
| 116 | 密钥不存在 | 提示用户检查 Key 是否正确 |
| 404 | 未绑定模拟组合 | 提示用户先在妙想页面创建模拟账户 |

## 安全说明

- 配置文件保存在 `~/.config/eastmoney-mx-skills/.env`，权限为 `600`（仅所有者可读写）
- 数据仅发送至东方财富官方 API 域名 `mkapi2.dfcfs.com`
- API Key 通过环境变量或配置文件使用，不会在前端明文暴露
- 模拟交易功能仅用于学习练手，不涉及真实资金
