# MCP Seeker - 自动寻找和安装MCP服务

## 描述

MCP Seeker是一个智能MCP（Model Context Protocol）服务发现和安装工具，让Trae能够：
- 🤖 **自动分析需求** - 理解用户任务，识别需要的MCP类型
- 🔍 **智能搜索MCP** - 从MCP.so、GitHub等多个来源搜索
- 💡 **智能推荐** - 基于匹配度评分推荐最佳MCP
- ⚡ **一键安装** - 自动下载、配置、安装MCP服务
- 🔄 **持续更新** - 定期检查新MCP和更新

## 核心特性

### 自动触发
当用户描述任务时，MCP Seeker会自动分析并推荐相关MCP：

```
用户：我要开发一个需要数据库支持的应用
MCP Seeker：🤖 检测到数据库需求，正在搜索相关MCP...
✓ 找到5个数据库MCP
✓ 推荐：PostgreSQL MCP (匹配度: 95%)
✓ 备选：MySQL MCP, MongoDB MCP
是否自动安装？[Y/n/对比/忽略]
```

### 多源搜索
- **MCP.so** - 搜索11,790+ MCP服务
- **GitHub** - awesome-mcp-servers等仓库
- **官方仓库** - Anthropic官方MCP
- **本地数据库** - 缓存的优质MCP列表

### 智能匹配
基于多维度评分：
- 关键词匹配度 (30%)
- 功能覆盖度 (25%)
- 下载量/流行度 (20%)
- 用户评分 (15%)
- 更新频率 (10%)

## 使用场景

### 场景1：自动推荐（默认）
```
用户：我需要处理PDF文件

MCP Seeker自动触发：
🔍 分析需求：PDF处理
📊 搜索到3个相关MCP：
  1. 🥇 PDF MCP (匹配度: 98%) - Anthropic官方
  2. 🥈 File System MCP (匹配度: 75%) - 通用文件处理
  3. 🥉 Document Parser MCP (匹配度: 65%) - 文档解析

🏆 推荐：PDF MCP
   ⭐ 4.9/5 | 📥 25.3K下载 | 🔄 上周更新
   功能：读取、编辑、转换、合并PDF
   安装：npx @anthropic-ai/mcp-pdf

[自动安装] [查看详情] [对比全部] [忽略]
```

### 场景2：手动搜索
```
用户：/find-mcp 数据库

MCP Seeker：
🔍 搜索关键词：数据库, database, SQL, PostgreSQL, MySQL
📊 找到8个MCP服务：

1. 🥇 PostgreSQL MCP (匹配度: 95%)
   ⭐ 4.8/5 | 📥 12.5K下载 | 🔄 3天前更新
   功能：连接池、查询、事务、迁移
   
2. 🥈 MySQL MCP (匹配度: 88%)
   ⭐ 4.6/5 | 📥 8.3K下载 | 🔄 1周前更新
   功能：连接、查询、存储过程
   
3. 🥉 MongoDB MCP (匹配度: 82%)
   ⭐ 4.5/5 | 📥 6.7K下载 | 🔄 2周前更新
   功能：NoSQL、文档存储、聚合查询

输入编号查看详情，或直接安装：
```

### 场景3：对比分析
```
用户：/compare-mcp PostgreSQL MySQL MongoDB

MCP Seeker：
📊 MCP对比报告

| 维度 | PostgreSQL | MySQL | MongoDB |
|------|------------|-------|---------|
| 匹配度 | 95% | 88% | 82% |
| 下载量 | 12.5K | 8.3K | 6.7K |
| 评分 | 4.8/5 | 4.6/5 | 4.5/5 |
| 更新 | 3天前 | 1周前 | 2周前 |
| 功能数 | 15 | 12 | 10 |

推荐：PostgreSQL MCP
理由：关系型数据库，功能最全面，社区最活跃
```

## 核心功能

### 1. 自动分析 (`/analyze`)
分析用户任务，识别MCP需求。

**参数：**
- `task` (string): 任务描述

**示例：**
```
/analyze task="开发一个需要用户认证的系统"
```

**输出：**
```
📋 需求分析结果：
- 主要需求：用户认证
- 相关MCP类型：Authentication, Database, Session
- 建议搜索关键词：auth, login, database, user
```

### 2. 搜索MCP (`/find-mcp`)
搜索相关MCP服务。

**参数：**
- `query` (string): 搜索关键词
- `source` (string): 搜索源 (mcp-so/github/official/all)
- `auto-install` (boolean): 是否自动安装最佳匹配
- `limit` (number): 返回结果数量

**示例：**
```
/find-mcp query="文件系统" source=all limit=5
/find-mcp query="API客户端" auto-install=true
```

### 3. 对比MCP (`/compare-mcp`)
对比多个MCP服务。

**参数：**
- `mcps` (array): MCP名称列表
- `criteria` (array): 对比维度

**示例：**
```
/compare-mcp mcps=["PostgreSQL", "MySQL", "MongoDB"] criteria=["downloads", "ratings", "features"]
```

### 4. 安装MCP (`/install-mcp`)
安装指定的MCP服务。

**参数：**
- `name` (string): MCP名称或GitHub仓库
- `configure` (boolean): 是否自动配置

**示例：**
```
/install-mcp name="@anthropic-ai/mcp-pdf" configure=true
/install-mcp name="owner/repo" configure=true
```

### 5. 更新MCP (`/update-mcp`)
更新已安装的MCP。

**参数：**
- `name` (string): MCP名称，空则更新所有

**示例：**
```
/update-mcp name="PostgreSQL"
/update-mcp  # 更新所有
```

### 6. 列出已安装 (`/list-mcp`)
列出所有已安装的MCP。

**示例：**
```
/list-mcp
```

## 工作流程

### 标准工作流程

```
1. 用户输入任务描述
   ↓
2. MCP Seeker自动分析需求
   - 提取关键词
   - 识别MCP类型
   - 生成搜索查询
   ↓
3. 多源搜索MCP
   - MCP.so API
   - GitHub仓库
   - 官方仓库
   - 本地数据库
   ↓
4. 智能匹配和评分
   - 计算匹配度
   - 排序和筛选
   - 去重处理
   ↓
5. 生成推荐列表
   - Top 3-5推荐
   - 显示详细信息
   - 提供对比选项
   ↓
6. 用户决策
   - 自动安装
   - 查看详情
   - 对比分析
   - 忽略跳过
   ↓
7. 自动安装（如选择）
   - 下载代码
   - 安装依赖
   - 配置环境
   - 测试连接
   - 更新项目配置
```

### 自动触发机制

**触发条件：**
1. 用户输入包含特定关键词
   - "数据库", "database", "SQL"
   - "API", "接口", "请求"
   - "文件", "file", "文档"
   - "认证", "auth", "login"
   - "搜索", "search", "查询"

2. 项目类型检测
   - Web应用 → 推荐Web相关MCP
   - 数据处理 → 推荐数据库MCP
   - AI应用 → 推荐AI服务MCP

3. 手动触发
   - `/find-mcp <关键词>`
   - `/analyze <任务描述>`

## 数据源

### MCP.so
- **地址**: https://mcp.so/
- **数量**: 11,790+ MCP服务
- **特点**: 最大MCP收录平台，支持分类筛选

### GitHub
- **awesome-mcp-servers**: https://github.com/punkpeye/awesome-mcp-servers
- **官方仓库**: https://github.com/modelcontextprotocol/servers
- **awesome-mcp-zh**: https://github.com/yzfly/awesome-mcp-zh

### 官方MCP
- **Anthropic官方**: https://github.com/modelcontextprotocol/servers
- **包含**: Filesystem, PostgreSQL, SQLite, Git, etc.

## 配置

### 配置文件: `config/settings.json`

```json
{
  "auto_trigger": true,
  "trigger_keywords": ["数据库", "API", "文件", "认证", "搜索"],
  "sources": {
    "mcp_so": {"enabled": true, "api_url": "https://mcp.so/api"},
    "github": {"enabled": true, "token": ""},
    "official": {"enabled": true}
  },
  "matching": {
    "min_score": 0.6,
    "weights": {
      "keyword": 0.3,
      "function": 0.25,
      "popularity": 0.2,
      "rating": 0.15,
      "freshness": 0.1
    }
  },
  "installation": {
    "auto_configure": true,
    "test_connection": true,
    "update_agents_md": true
  }
}
```

## 工具脚本

### 需求分析: `tools/analyze_requirements.py`
- 自然语言处理
- 关键词提取
- 需求分类

### MCP搜索: `tools/search_mcp.py`
- MCP.so API调用
- GitHub搜索
- 结果聚合

### 智能匹配: `tools/match_mcp.py`
- 匹配度计算
- 多维度评分
- 排序算法

### 自动安装: `tools/install_mcp.py`
- 代码下载
- 依赖安装
- 环境配置
- 连接测试

### MCP数据库: `data/mcp_database.json`
- 热门MCP缓存
- 本地索引
- 用户评分

## 最佳实践

### 1. 自动模式（推荐）
让MCP Seeker自动分析和推荐：
```
只需描述任务，MCP Seeker会自动推荐合适的MCP
```

### 2. 手动搜索
需要特定MCP时使用：
```
/find-mcp "关键词"
```

### 3. 对比选择
多个候选时使用对比功能：
```
/compare-mcp MCP1 MCP2 MCP3
```

### 4. 定期更新
保持MCP最新：
```
/update-mcp
```

## 注意事项

1. **网络依赖**: 搜索需要网络连接
2. **API限制**: MCP.so和GitHub API有频率限制
3. **自动安装**: 需要用户确认，不会自动执行
4. **配置备份**: 安装前会备份现有配置
5. **兼容性**: 检查MCP与当前项目的兼容性

## 故障排除

### 搜索无结果
- 检查网络连接
- 尝试不同的关键词
- 检查API配额

### 安装失败
- 检查Node.js/npm环境
- 查看依赖冲突
- 检查权限问题

### 连接测试失败
- 检查MCP配置
- 验证服务状态
- 查看日志信息

## 更新日志

### v1.0 (2026-02-02)
- 初始版本
- 实现自动分析和推荐
- 支持MCP.so、GitHub、官方仓库
- 智能匹配算法
- 一键安装功能

## 相关链接

- [MCP.so](https://mcp.so/)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
- [MCP官方文档](https://modelcontextprotocol.io/)
- [Anthropic MCP](https://github.com/modelcontextprotocol/servers)

---

**提示**: MCP Seeker会显著提升您的开发效率，建议保持自动触发开启！
