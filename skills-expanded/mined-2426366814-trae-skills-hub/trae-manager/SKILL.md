# Trae Manager - 统一管理和部署工具

## 描述

Trae Manager是Trae环境的统一管理和部署工具，包含今天所有需求：
- 🔍 **技能搜索和比较** - 集成skill-seeker功能
- 🔌 **MCP自动寻找和安装** - 集成mcp-seeker功能
- ⚡ **一键自动安装** - 技能和MCP自动安装
- 🚀 **跨机器部署** - 导出/导入配置，快速部署

## 核心功能

### 1. 一键部署完整环境

```bash
# 部署所有内容（技能 + MCP + 依赖）
python trae_manager.py setup --full --auto-install

# 或分步部署
python trae_manager.py setup --skills    # 只部署技能
python trae_manager.py setup --mcp       # 只部署MCP
python trae_manager.py setup --deps      # 只安装依赖
```

### 2. 技能管理

```bash
# 安装核心技能套件
python trae_manager.py install-skills core

# 安装所有技能
python trae_manager.py install-skills --all

# 安装特定技能
python trae_manager.py install-skills docx,pdf,xlsx
```

### 3. MCP管理

```bash
# 安装推荐MCP套件
python trae_manager.py install-mcp --recommended

# 安装特定MCP
python trae_manager.py install-mcp postgres,mysql
```

### 4. 跨机器部署

**机器A（源环境）：**
```bash
# 导出完整配置
python trae_manager.py export --full > my-trae-setup.json

# 复制到新机器
scp my-trae-setup.json user@machine-b:~/
```

**机器B（新环境）：**
```bash
# 安装trae-manager（只需这个）
git clone <trae-manager-repo>

# 导入配置并自动安装所有内容
python trae_manager.py import my-trae-setup.json --auto-install
```

## 使用场景

### 场景1：新机器快速部署
```
用户：在新机器上部署完整Trae环境

Trae Manager：
1. 检查环境（Node.js、Python、Git）
2. 安装核心技能（skill-seeker、mcp-seeker、trae-manager）
3. 安装文档处理技能（docx、pdf、pptx、xlsx）
4. 安装推荐MCP（filesystem、fetch、git、pdf）
5. 安装所有依赖
6. 验证安装

✅ 5分钟完成完整环境部署
```

### 场景2：团队协作
```
团队成员A：
- 配置好完整环境
- 导出配置：python trae_manager.py export --full > team-config.json
- 提交到Git仓库

团队成员B：
- 拉取配置
- 一键部署：python trae_manager.py import team-config.json --auto-install
- 获得完全一致的环境
```

### 场景3：环境备份和恢复
```bash
# 备份当前环境
python trae_manager.py export --full > backup-$(date +%Y%m%d).json

# 恢复环境
python trae_manager.py import backup-20260202.json --auto-install
```

## 命令参考

### setup - 设置环境
```bash
python trae_manager.py setup [选项]
  --mode {full,skills,mcp,deps}  设置模式（默认：full）
  --auto-install                 自动安装所有内容
```

### install-skills - 安装技能
```bash
python trae_manager.py install-skills <技能列表>
  --all    安装所有技能
  core     安装核心技能
```

### install-mcp - 安装MCP
```bash
python trae_manager.py install-mcp <MCP列表>
  --recommended  安装推荐MCP
```

### check-env - 检查环境
```bash
python trae_manager.py check-env
```

### export - 导出配置
```bash
python trae_manager.py export [选项]
  --full  导出完整配置（包括依赖清单）
```

### import - 导入配置
```bash
python trae_manager.py import <配置文件> [选项]
  --auto-install  自动安装所有内容
```

## 依赖清单

Trae Manager管理以下依赖：

### 系统要求
- Node.js >= 18.0.0
- npm >= 9.0.0
- Python >= 3.9.0
- Git >= 2.30.0

### 核心技能
- skill-seeker：技能搜索和比较
- mcp-seeker：MCP自动寻找和安装
- trae-manager：统一管理和部署

### 文档处理技能
- docx：Word文档处理
- pdf：PDF文档处理
- pptx：PowerPoint处理
- xlsx：Excel表格处理

### MCP服务
- PostgreSQL：数据库连接
- MySQL：数据库连接
- MongoDB：NoSQL数据库
- SQLite：轻量级数据库
- Filesystem：文件系统访问
- PDF：PDF文件处理
- Git：版本控制
- GitHub：GitHub API
- Fetch：HTTP请求
- Puppeteer：浏览器自动化
- OpenAI：OpenAI API
- Hugging Face：模型集成
- Brave Search：搜索引擎
- Slack：消息管理
- Google Calendar：日历集成

## 配置文件

### dependencies.yaml
位于 `data/dependencies.yaml`，包含所有技能和MCP的依赖配置。

### 导出配置示例
```json
{
  "version": "1.0.0",
  "timestamp": "2026-02-02T14:45:00",
  "export_type": "full",
  "installed_skills": [
    "skill-seeker",
    "mcp-seeker",
    "docx",
    "pdf",
    "xlsx"
  ],
  "installed_mcp": [
    "filesystem",
    "fetch",
    "git"
  ],
  "dependencies": { ... }
}
```

## 最佳实践

### 1. 首次部署
```bash
# 检查环境
python trae_manager.py check-env

# 一键部署完整环境
python trae_manager.py setup --full --auto-install
```

### 2. 定期备份
```bash
# 创建备份脚本
#!/bin/bash
BACKUP_DIR="$HOME/trae-backups"
mkdir -p "$BACKUP_DIR"
python trae_manager.py export --full > "$BACKUP_DIR/trae-$(date +%Y%m%d-%H%M%S).json"
```

### 3. 团队协作
```bash
# 在项目中包含Trae配置
echo "trae-config.json" >> .gitignore  # 不提交个人配置

# 创建团队配置模板
python trae_manager.py export > trae-config.template.json
```

## 故障排除

### 环境检查失败
```bash
# 检查Node.js
node --version

# 检查Python
python --version

# 检查Git
git --version
```

### 安装失败
```bash
# 查看详细错误
python trae_manager.py setup --full 2>&1 | tee install.log

# 单独安装失败的组件
python trae_manager.py install-skills <skill-name>
```

### 导入失败
```bash
# 验证配置文件
python -c "import json; json.load(open('config.json'))"

# 手动安装
python trae_manager.py import config.json  # 不自动安装
python trae_manager.py install-skills ...  # 手动安装
```

## 更新日志

### v1.0.0 (2026-02-02)
- 初始版本
- 集成skill-seeker功能
- 集成mcp-seeker功能
- 实现一键部署
- 支持导出/导入配置
- 支持跨机器部署

## 相关链接

- [skill-seeker](../skill-seeker/SKILL.md)
- [mcp-seeker](../mcp-seeker/SKILL.md)
- [MCP.so](https://mcp.so/)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

---

**Trae Manager让您5分钟完成完整环境部署！** 🚀
