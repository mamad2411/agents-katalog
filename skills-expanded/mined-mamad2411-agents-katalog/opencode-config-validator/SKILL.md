---
name: opencode-config-validator
description: OpenCode配置规范验证器 - 强制检测配置是否符合官方标准，避免客户端报错
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: configuration
  priority: high
---

# OpenCode配置规范验证器

## 直接触发指令

当OpenCode配置发生以下变更时自动激活此技能：
- "增加skills后"
- "配置MCP服务器后"
- "添加LSP服务器后"
- "修改opencode.json后"
- "检测配置规范"
- "验证OpenCode配置"

## 功能

在OpenCode配置发生实质性改动后，自动检测配置是否符合官方标准，避免客户端报错无法打开。

## 使用场景

- 新增skills后验证命名规范和文件结构
- 配置MCP服务器后验证参数格式
- 添加LSP服务器后验证配置选项
- 修改opencode.json后验证JSON语法

## 使用方法

在Solo模式下直接请求：

```
验证当前的OpenCode配置是否符合官方标准
```

```
检测skills配置规范
```

```
检查MCP服务器配置
```

```
验证LSP服务器设置
```

## 验证流程

### 1. Skills规范检测
- **文件名**: 检查SKILL.md是否大写
- **命名规范**: 验证技能名称是否符合`^[a-z0-9]+(-[a-z0-9]+)*$`
- **描述长度**: 检查描述是否在1-1024字符内
- **文件位置**: 验证技能文件是否在正确目录

### 2. MCP服务器规范检测
- **类型验证**: 检查type是否为"local"或"remote"
- **命令格式**: 验证command数组格式
- **环境变量**: 检查environment配置
- **超时设置**: 验证timeout设置
- **启用状态**: 检查enabled配置

### 3. LSP服务器规范检测
- **扩展名**: 验证extensions配置
- **命令格式**: 检查command数组
- **初始化选项**: 验证initialization配置
- **环境变量**: 检查env设置

### 4. 配置文件检测
- **JSON语法**: 验证opencode.json语法正确性
- **Schema验证**: 检查是否符合$schema规范
- **权限配置**: 验证permission设置
- **工具配置**: 检查tools配置

## ⚠️ 必需配置

此技能无需额外配置，但需要网络连接来获取官方文档。

## 使用示例

### 检测skills配置
```bash
# 检查所有skills的命名规范
验证skills命名是否符合官方标准
```

### 检测MCP配置
```bash
# 检查MCP服务器配置
验证MCP服务器配置是否正确
```

### 检测LSP配置
```bash
# 检查LSP服务器设置
验证LSP服务器配置是否符合要求
```

## 官方文档参考

此技能基于OpenCode官方文档：
- [Skills规范](https://opencode.ai/docs/skills/)
- [MCP服务器规范](https://opencode.ai/docs/mcp-servers/)
- [LSP服务器规范](https://opencode.ai/docs/lsp/)
- [配置文件规范](https://opencode.ai/docs/config/)

## 故障排除

### 常见错误
- **技能名称无效**: 名称不符合命名规范
- **MCP命令错误**: command数组格式不正确
- **LSP扩展名缺失**: extensions配置为空
- **JSON语法错误**: opencode.json格式错误

### 解决方法
1. 检查官方文档对应章节
2. 按照规范修正配置
3. 重新启动OpenCode客户端验证
4. 如仍有问题，查看错误日志

## 最佳实践

### 配置前检查
```bash
在修改配置前先运行验证器
```

### 配置后验证
```bash
修改完成后立即运行验证器
```

### 定期检查
```bash
定期运行验证器确保配置持续有效
```

## 配置检查清单

- [ ] Skills命名符合规范
- [ ] MCP服务器配置正确
- [ ] LSP服务器设置完整
- [ ] opencode.json语法正确
- [ ] 权限配置合理
- [ ] 工具配置恰当

## 资源链接

- **OpenCode官网**: https://opencode.ai
- **官方文档**: https://opencode.ai/docs/
- **GitHub仓库**: https://github.com/anomalyco/opencode
- **Discord社区**: https://opencode.ai/discord