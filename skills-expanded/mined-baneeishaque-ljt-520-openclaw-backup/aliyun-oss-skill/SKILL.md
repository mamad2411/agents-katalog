# Aliyun OSS Skill

通过 aliyun-oss MCP 工具 + Node.js SDK 脚本 + ossutil 管理阿里云对象存储和数据处理。

---

## 📖 功能说明

### 核心功能
- 📤 **上传文件** - 单文件、批量上传、断点续传
- 📥 **下载文件** - 单文件、批量下载
- 📋 **列出文件** - 按前缀、分页列出
- 🗑️ **删除文件** - 单文件、批量删除
- 🔗 **获取 URL** - 公开/私有空间 URL 生成
- 📊 **文件信息** - 查看文件详情
- 📁 **目录操作** - 移动、复制、重命名

### 高级功能（通过 SDK）
- 🖼️ **图片处理** - 缩放、裁剪、水印、格式转换
- 🎵 **音视频处理** - 转码、截图
- 🔍 **智能搜索** - 文件搜索和元数据查询
- 📝 **文档处理** - 文档预览、格式转换

---

## 🚀 首次使用 — 自动设置

当用户首次要求操作 OSS 时，按以下流程操作：

### 步骤 1：检查当前状态

```bash
{baseDir}/scripts/setup.sh --check-only
```

**检查内容：**
- ✅ Node.js 环境
- ✅ aliyun-oss MCP 是否已安装
- ✅ ossutil 是否已安装
- ✅ 配置文件是否存在
- ✅ 凭证是否已配置

如果输出显示一切 OK（凭证已配置），跳到「执行策略」。

---

### 步骤 2：如果未配置，引导用户提供凭证

告诉用户：

```
我需要你的阿里云凭证来连接 OSS 存储服务。请提供：

AccessKey ID — 阿里云 AccessKey ID
AccessKey Secret — 阿里云 AccessKey Secret
Region — 地域节点（如 oss-cn-hangzhou, oss-cn-shanghai, oss-cn-beijing）
Bucket — 存储桶名称
Domain（可选） — 访问域名（用于生成文件 URL，如 https://bucket.oss-cn-hangzhou.aliyuncs.com）

你可以在阿里云控制台获取：
- 密钥管理：https://ram.console.aliyun.com/manage/ak
- 存储桶列表：https://oss.console.aliyun.com/bucket
- 地域说明：
  - oss-cn-hangzhou: 华东1（杭州）
  - oss-cn-shanghai: 华东2（上海）
  - oss-cn-beijing: 华北2（北京）
  - oss-cn-shenzhen: 华南1（深圳）
  - oss-cn-hongkong: 中国香港
  - oss-us-west-1: 美国西部1（硅谷）
  - oss-ap-southeast-1: 亚太东南1（新加坡）
```

---

### 步骤 3：用户提供凭证后，运行自动设置

```bash
{baseDir}/scripts/setup.sh \
  --access-key-id "<AccessKey ID>" \
  --access-key-secret "<AccessKey Secret>" \
  --region "<Region>" \
  --bucket "<Bucket>" \
  --domain "<Domain>"
```

**脚本会自动：**

1. ✅ 检查并安装 aliyun-oss MCP 工具（如果有）
2. ✅ 安装 ali-oss Node.js SDK
3. ✅ 安装 ossutil 命令行工具
4. ✅ 将凭证写入 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`），重启后仍可用
5. ✅ 创建配置文件 `{baseDir}/config/oss-config.json`
6. ✅ 验证阿里云 OSS 连接
7. ✅ 测试上传下载功能

**设置完成后即可开始使用。**

---

## 🎯 执行策略

三种方式按优先级降级，确保操作始终可完成：

### 方式一：aliyun-oss MCP 工具（优先）

**特点：** 功能最全，支持存储 + 图片处理 + 音视频处理 + 智能搜索

**使用场景：**
- 需要图片处理（缩放、裁剪、水印）
- 需要音视频转码
- 需要智能搜索
- 需要文档处理

**调用方式：**
```javascript
// 通过 MCP 工具调用
use_mcp_tool("aliyun-oss", "upload_file", {
  localPath: "/path/to/file.txt",
  key: "uploads/file.txt"
})
```

---

### 方式二：Node.js SDK 脚本

**特点：** 稳定可靠，支持基础存储操作

**使用场景：**
- MCP 工具不可用
- 只需要基础存储操作
- 需要自定义处理逻辑

**调用方式：**
```bash
node {baseDir}/scripts/oss_node.mjs upload \
  --local "/path/to/file.txt" \
  --key "uploads/file.txt"

node {baseDir}/scripts/oss_node.mjs download \
  --key "uploads/file.txt" \
  --local "/path/to/file.txt"

node {baseDir}/scripts/oss_node.mjs list \
  --prefix "uploads/" \
  --limit 100
```

---

### 方式三：ossutil 命令行（最后备选）

**特点：** 官方命令行工具，功能全面

**使用场景：**
- MCP 和 SDK 都不可用
- 需要批量操作
- 需要高级功能

**调用方式：**
```bash
# 上传文件
ossutil cp /path/to/file.txt oss://bucket/key

# 下载文件
ossutil cp oss://bucket/key /path/to/file.txt

# 列出文件
ossutil ls oss://bucket/prefix/

# 批量上传
ossutil cp -r /local/dir/ oss://bucket/
```

---

## 📋 使用示例

### 示例1：上传备份文件

**用户说：**
```
帮我上传 /backups/daily-20260301.tar.gz 到阿里云 OSS
```

**AI 执行：**
```javascript
// 优先使用 SDK
result = node scripts/oss_node.mjs upload \
  --local "/backups/daily-20260301.tar.gz" \
  --key "backups/daily-20260301.tar.gz"
```

**返回：**
```
✅ 上传成功！

文件：daily-20260301.tar.gz
大小：15.2 MB
URL：https://bucket.oss-cn-hangzhou.aliyuncs.com/backups/daily-20260301.tar.gz
```

---

### 示例2：列出文件

**用户说：**
```
列出阿里云 OSS backups 目录下的所有文件
```

**AI 执行：**
```javascript
// 使用 Node.js SDK
files = node scripts/oss_node.mjs list --prefix "backups/"
```

**返回：**
```
📋 共找到 15 个文件：

backups/backup-20260301.tar.gz  - 15.2 MB  - 2026-03-01 20:00
backups/backup-20260228.tar.gz  - 14.8 MB  - 2026-02-28 20:00
backups/backup-20260227.tar.gz  - 16.1 MB  - 2026-02-27 20:00
...
```

---

### 示例3：获取文件 URL

**用户说：**
```
给我 images/photo.jpg 的访问链接，1小时有效
```

**AI 执行：**
```javascript
// 使用 Node.js SDK
url = node scripts/oss_node.mjs url \
  --key "images/photo.jpg" --private --expires 3600
```

**返回：**
```
🔗 临时访问链接（1小时有效）：

https://bucket.oss-cn-hangzhou.aliyuncs.com/images/photo.jpg?OSSAccessKeyId=...&Expires=...&Signature=...
```

---

### 示例4：图片处理

**用户说：**
```
把 images/photo.jpg 缩小到 800x600，加水印
```

**AI 执行：**
```javascript
// 使用 Node.js SDK（支持图片处理）
url = node scripts/oss_node.mjs process-image \
  --key "images/photo.jpg" \
  --resize "800x600" \
  --watermark "OpenClaw"
```

**返回：**
```
✅ 图片处理完成！

原图：https://bucket.oss-cn-hangzhou.aliyuncs.com/images/photo.jpg
处理后：https://bucket.oss-cn-hangzhou.aliyuncs.com/images/photo.jpg?x-oss-process=image/resize,w_800,h_600/watermark,...
```

---

### 示例5：批量删除旧备份

**用户说：**
```
删除阿里云 OSS 上 30 天前的备份
```

**AI 执行：**
```javascript
// 使用 Node.js SDK 脚本
const cutoffDate = Date.now() - (30 * 24 * 60 * 60 * 1000);

// 列出所有备份
const files = JSON.parse(execSync('node scripts/oss_node.mjs list --prefix "backups/" --format json'));

// 删除旧备份
for (const file of files) {
  if (file.mtime * 1000 < cutoffDate) {
    execSync(`node scripts/oss_node.mjs delete --key ${file.key} --force`);
  }
}
```

**返回：**
```
🗑️  已删除 12 个旧备份：

backups/backup-20260115.tar.gz
backups/backup-20260114.tar.gz
...
```

---

## 🔧 API 文档

### Node.js SDK 脚本 API

#### 上传文件
```bash
node scripts/oss_node.mjs upload \
  --local <LocalPath> \
  --key <RemoteKey> \
  [--bucket <Bucket>] \
  [--overwrite]
```

#### 下载文件
```bash
node scripts/oss_node.mjs download \
  --key <RemoteKey> \
  --local <LocalPath> \
  [--bucket <Bucket>]
```

#### 列出文件
```bash
node scripts/oss_node.mjs list \
  [--prefix <Prefix>] \
  [--limit <Limit>] \
  [--delimiter <Delimiter>] \
  [--format json|table]
```

#### 删除文件
```bash
node scripts/oss_node.mjs delete \
  --key <RemoteKey> \
  [--bucket <Bucket>] \
  [--force]
```

#### 批量删除
```bash
node scripts/oss_node.mjs batch-delete \
  --file <KeyListFile> \
  [--bucket <Bucket>]
```

#### 获取文件 URL
```bash
node scripts/oss_node.mjs url \
  --key <RemoteKey> \
  [--private] \
  [--expires <Seconds>]
```

#### 获取文件信息
```bash
node scripts/oss_node.mjs stat \
  --key <RemoteKey> \
  [--bucket <Bucket>]
```

#### 移动文件
```bash
node scripts/oss_node.mjs move \
  --src-key <SourceKey> \
  --dest-key <DestKey> \
  [--bucket <Bucket>] \
  [--force]
```

#### 复制文件
```bash
node scripts/oss_node.mjs copy \
  --src-key <SourceKey> \
  --dest-key <DestKey> \
  [--bucket <Bucket>] \
  [--force]
```

---

## ⚙️ 配置文件

### config/oss-config.json

```json
{
  "accessKeyId": "你的AccessKey ID",
  "accessKeySecret": "你的AccessKey Secret",
  "bucket": "你的存储桶名称",
  "region": "oss-cn-hangzhou",
  "domain": "https://你的域名.com",
  "options": {
    "secure": true,
    "timeout": 60000,
    "upload_threshold": 1048576,
    "chunk_size": 1048576,
    "retry_times": 3
  }
}
```

### 配置项说明

| 配置项 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| accessKeyId | string | ✅ | 阿里云 AccessKey ID |
| accessKeySecret | string | ✅ | 阿里云 AccessKey Secret |
| bucket | string | ✅ | 存储桶名称 |
| region | string | ✅ | 地域节点 |
| domain | string | ❌ | 访问域名 |
| secure | boolean | ❌ | 使用 HTTPS |
| timeout | number | ❌ | 超时时间（毫秒） |
| upload_threshold | number | ❌ | 分片上传阈值（字节） |
| chunk_size | number | ❌ | 分片大小（字节） |
| retry_times | number | ❌ | 重试次数 |

---

## 🐛 故障排查

### 问题1：连接失败

**症状：**
```
❌ 连接失败：网络错误
```

**检查：**
1. AccessKey ID 和 AccessKey Secret 是否正确
2. Region 是否正确
3. 网络连接是否正常

**解决：**
```bash
# 检查配置
node scripts/oss_node.mjs check-config

# 测试连接
node scripts/oss_node.mjs test-connection
```

---

### 问题2：权限不足

**症状：**
```
❌ 权限拒绝：403 Forbidden
```

**检查：**
1. AccessKey 是否有对应存储桶的权限
2. RAM 用户权限配置是否正确

**解决：**
```bash
# 重新配置
bash scripts/setup.sh \
  --access-key-id "新的AccessKey ID" \
  --access-key-secret "新的AccessKey Secret" \
  --region "oss-cn-hangzhou" \
  --bucket "mybucket"
```

---

### 问题3：上传失败

**症状：**
```
❌ 上传失败：连接超时
```

**检查：**
1. 网络连接是否正常
2. Region 是否正确
3. 存储桶是否存在

**解决：**
```bash
# 检查配置
node scripts/oss_node.mjs check-config

# 测试连接
node scripts/oss_node.mjs test-connection
```

---

### 问题4：Node.js SDK 未安装

**症状：**
```
❌ Cannot find module 'ali-oss'
```

**解决：**
```bash
# 安装 SDK
cd /home/node/.openclaw/workspace/skills/aliyun-oss-skill
npm install ali-oss

# 或使用自动安装
bash scripts/setup.sh --install-sdk
```

---

### 问题5：ossutil 未安装

**症状：**
```
❌ ossutil: command not found
```

**解决：**
```bash
# 下载并安装
wget https://gosspublic.alicdn.com/ossutil/1.7.17/ossutil-v1.7.17-linux-amd64.zip
unzip ossutil-v1.7.17-linux-amd64.zip
chmod +x ossutil
sudo mv ossutil /usr/local/bin/

# 配置账号
ossutil config -e oss-cn-hangzhou.aliyuncs.com -i <AccessKey ID> -k <AccessKey Secret>
```

---

## 📚 相关文档

- [阿里云 OSS 官方文档](https://help.aliyun.com/product/31815.html)
- [阿里云 OSS Node.js SDK](https://help.aliyun.com/document_detail/32068.html)
- [ossutil 命令行工具](https://help.aliyun.com/document_detail/120075.html)
- [OpenClaw 技能开发指南](https://docs.openclaw.ai/skills)

---

## 🎯 未来计划

- [ ] 支持增量同步
- [ ] 支持断点续传进度查询
- [ ] 支持文件加密上传
- [ ] 支持 Webhook 通知
- [ ] 支持多存储桶管理
- [ ] 支持访问统计分析

---

## 👤 作者

- **创建者**：33 (AI 助手)
- **创建日期**：2026-03-01
- **版本**：v1.0.0
- **参考**：qiniu-kodo 技能架构

---

## 📞 支持

如有问题，请在 OpenClaw 中联系 33。

---

## 📄 许可证

MIT License
