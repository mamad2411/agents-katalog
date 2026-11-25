---
name: zhihu-draft-helper
description: 当用户提到知乎、知乎发文、知乎发布文章、知乎草稿、知乎编辑文章、知乎登录后操作、知乎API、知乎直连发布、知乎草稿工具、知乎内容同步、绕过知乎编辑器、知乎批量发布、帮我发一篇知乎测试文章、帮我在知乎上操作网页时使用。
version: 1.0.0
last_updated: 2026-04-18
---

# 知乎草稿助手

> 版本：`1.0.0`
> 
> 更新日期：`2026-04-18`
> 
> 功能：通过API直接操作知乎草稿，绕过富文本编辑器限制，支持创建、读取、更新草稿，支持从Markdown文件同步内容。

用于在Minis内通过API和浏览器完成知乎草稿相关操作，包括直连API创建草稿、网页端最终发布、内容同步等。

## 适用范围

- 通过API直接创建知乎草稿
- 通过API读取和更新草稿
- 将本地Markdown文件同步到知乎草稿
- 在网页端完成最终发布操作
- 批量创建和管理草稿
- 绕过知乎富文本编辑器限制

## 核心功能

### 1. API直连操作（已验证）
- **草稿创建**：`POST /api/v4/editor/default-settings`
- **草稿读取**：`GET /api/v4/editor/default-settings?content_token={id}`
- **草稿更新**：`PATCH /api/v4/editor/default-settings?content_token={id}`

### 2. 网页端操作
- 打开编辑页面完成最终发布
- 设置话题、封面图、摘要等
- 处理发布审核状态

### 3. 文件同步
- 从Markdown文件读取内容
- 保持格式转换（Markdown → 知乎格式）
- 批量同步多篇文章

## 工作流程

### 快速发布流程
1. **获取Cookie**：通过浏览器登录知乎，获取Cookie环境文件
2. **创建草稿**：使用API工具创建草稿
3. **网页发布**：在浏览器中打开编辑页面，点击发布按钮
4. **验证状态**：检查发布是否成功

### 详细步骤

#### 步骤1：获取知乎Cookie
```bash
# 在浏览器中登录知乎
browser_use navigate --url https://zhuanlan.zhihu.com/write

# 获取Cookie环境文件
browser_use get_cookies
# 环境文件保存到：/var/minis/offloads/env_cookies_zhihu_com_*.sh
```

#### 步骤2：使用API工具
```bash
# 使用包装脚本（推荐）
cd /var/minis/shared/my_mini_skills/zhihu-draft-tool
./zhihu_draft_tool_wrapper.sh create \
  --base-id 2028607956032176996 \
  --title "文章标题" \
  --content-file content.md \
  --summary "文章摘要" \
  --comment-permission all

# 或直接使用Python脚本
python3 zhihu_draft_tool.py get \
  --cookie "$COOKIE_STRING" \
  --id 2028871642558787933
```

#### 步骤3：网页端发布
```bash
# 打开草稿编辑页面
browser_use navigate --url https://zhuanlan.zhihu.com/p/{草稿ID}/edit

# 等待页面加载完成
browser_use wait_for_dom_stable --timeout 10

# 点击发布按钮
browser_use click --selector .Button--primary.Button--blue
```

## 工具文件位置

### 主工具脚本
- `/var/minis/shared/my_mini_skills/zhihu-draft-tool/zhihu_draft_tool.py`
- `/var/minis/shared/my_mini_skills/zhihu-draft-tool/zhihu_draft_tool_wrapper.sh`

### 文档和示例
- `README.md` - 完整使用说明
- `test_example.sh` - 使用示例
- `docs/` - API分析文档

## 已验证的API接口

### 1. 创建草稿
```python
POST https://zhuanlan.zhihu.com/api/v4/editor/default-settings
参数：{
  "content_token": "基础草稿ID",
  "title": "文章标题",
  "content": "文章内容",
  "summary": "摘要",
  "comment_permission": "all|registered_only|none"
}
```

### 2. 读取草稿
```python
GET https://zhuanlan.zhihu.com/api/v4/editor/default-settings?content_token={草稿ID}
```

### 3. 更新草稿
```python
PATCH https://zhuanlan.zhihu.com/api/v4/editor/default-settings?content_token={草稿ID}
```

## 实际测试案例

### 测试草稿1：API功能测试
- **ID**: `2028867948278822109`
- **标题**: "知乎草稿API测试 - 已更新"
- **状态**: 草稿（可编辑）
- **编辑链接**: https://zhuanlan.zhihu.com/p/2028867948278822109/edit

### 测试草稿2：大学随记同步
- **ID**: `2028871642558787933`
- **标题**: "不是每一天都闪闪发光，但也都算数"
- **来源**: CSDN文章同步
- **状态**: 草稿（待发布）
- **编辑链接**: https://zhuanlan.zhihu.com/p/2028871642558787933/edit

## 常见问题处理

### 1. Cookie失效
- 重新登录知乎获取新Cookie
- 检查Cookie环境文件路径是否正确

### 2. 基础草稿ID无效
- 使用有效的草稿ID作为模板
- 可以通过访问已有草稿编辑页面获取ID

### 3. 发布按钮灰色
- 检查是否设置了必要的话题
- 确认内容不为空
- 可能需要添加封面图

### 4. 发布后仍在草稿状态
- 知乎可能有审核机制
- 新账号发布可能需要时间
- 检查是否有错误提示

## 使用场景

### 场景1：批量内容发布
- 自动化创建多个草稿
- 从本地目录批量同步Markdown文件
- 统一设置摘要和评论权限

### 场景2：内容同步
- 将CSDN、博客园等平台内容同步到知乎
- 保持格式和内容一致性
- 避免手动复制粘贴

### 场景3：绕过编辑器限制
- 知乎富文本编辑器对前端状态管理严格
- 通过API直接操作数据层
- 避免与编辑器交互的问题

### 场景4：API集成
- 作为其他发布工具的组件
- 集成到自动化工作流中
- 提供知乎发布能力

## 注意事项

### 安全注意事项
1. **Cookie保护**：不要分享或泄露Cookie
2. **使用频率**：避免高频请求，防止被封禁
3. **内容合规**：遵守知乎社区规范

### 技术限制
1. **最终发布**：仍需网页端点击发布按钮
2. **审核机制**：新内容可能需要审核
3. **API稳定性**：知乎可能更改API接口

### 最佳实践
1. **先测试后使用**：先用测试内容验证功能
2. **保存草稿ID**：记录创建的草稿ID便于管理
3. **定期备份**：重要内容本地备份

## 更新记录

### v1.0.0 (2026-04-18)
- 初始版本发布
- 包含API直连创建、读取、更新草稿功能
- 支持从Markdown文件同步内容
- 包含网页端发布流程
- 已验证在实际环境中可用