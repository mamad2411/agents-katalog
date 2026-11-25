---
name: file-organizer
description: 通过了解上下文、查找重复文件、建议更好的结构和自动执行清理任务，智能地组织计算机上的文件和文件夹。减少认知负担，使您的数字工作区保持整洁，无需手动操作。
---

# 文件组织器

此技能充当您的个人组织助手，帮助您在计算机上维护清晰、合乎逻辑的文件结构，而无需不断手动组织的脑力负担。

## 何时使用此技能

- 您的下载文件夹一团糟
- 您找不到文件，因为它们散落在各处
- 您的重复文件占用空间
- 您的文件夹结构不再合理
- 您想建立更好的组织习惯
- 您正在开始一个新项目并需要一个好的结构
- 您正在归档旧项目之前进行清理

## 此技能做什么

1. **分析当前结构**: 审查您的文件夹和文件以了解您拥有的内容
2. **查找重复项**: 在您的系统中识别重复文件
3. **建议组织**: 根据您的内容提出合理的文件夹结构
4. **自动清理**: 经您批准移动、重命名和组织文件
5. **维护上下文**: 根据文件类型、日期和内容做出明智决定
6. **减少混乱**: 识别您可能不再需要的旧文件

## 如何使用

### 从您的主目录

```
cd ~
```

然后运行 Claude Code 并请求帮助：

```
Help me organize my Downloads folder
```

```
Find duplicate files in my Documents folder
```

```
Review my project directories and suggest improvements
```

### 特定组织任务

```
Organize these downloads into proper folders based on what they are
```

```
Find duplicate files and help me decide which to keep
```

```
Clean up old files I haven't touched in 6+ months
```

```
Create a better folder structure for my [work/projects/photos/etc]
```

## 说明

当用户请求文件组织帮助时：

1. **了解范围**
   
   询问澄清问题：
   - 哪个目录需要组织？(下载、文档、整个主文件夹？)
   - 主要问题是什么？(找不到东西、重复、太乱、没有结构？)
   - 有任何要避免的文件或文件夹吗？(当前项目、敏感数据？)
   - 组织有多积极？(保守 vs. 全面清理)

2. **分析当前状态**
   
   审查目标目录：
   ```bash
   # 获取当前结构概览
   ls -la [target_directory]
   
   # 检查文件类型和大小
   find [target_directory] -type f -exec file {} \; | head -20
   
   # 识别最大的文件
   du -sh [target_directory]/* | sort -rh | head -20
   
   # 统计文件类型
   find [target_directory] -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
   ```
   
   总结发现：
   - 文件和文件夹总数
   - 文件类型细分
   - 大小分布
   - 日期范围
   - 明显的组织问题

3. **识别组织模式**
   
   根据文件，确定逻辑分组：
   
   **按类型**:
   - 文档 (PDFs, DOCX, TXT)
   - 图像 (JPG, PNG, SVG)
   - 视频 (MP4, MOV)
   - 归档 (ZIP, TAR, DMG)
   - 代码/项目 (directories with code)
   - 电子表格 (XLSX, CSV)
   - 演示文稿 (PPTX, KEY)
   
   **按用途**:
   - 工作 vs. 个人
   - 活跃 vs. 归档
   - 特定项目
   - 参考资料
   - 临时/暂存文件
   
   **按日期**:
   - 本年/本月
   - 往年
   - 非常旧 (归档候选)

4. **查找重复项**
   
   当请求时，搜索重复项：
   ```bash
   # 通过哈希查找完全重复项
   find [directory] -type f -exec md5 {} \; | sort | uniq -d
   
   # 查找同名文件
   find [directory] -type f -printf '%f\n' | sort | uniq -d
   
   # 查找大小相似的文件
   find [directory] -type f -printf '%s %p\n' | sort -n
   ```
   
   对于每组重复项：
   - 显示所有文件路径
   - 显示大小和修改日期
   - 建议保留哪个（通常是最新的或命名最好的）
   - **重要**: 在删除之前始终请求确认

5. **提出组织计划**
   
   在进行更改之前提出清晰的计划：
   
   ```markdown
   # [Directory] 组织计划
   
   ## 当前状态
   - X 个文件跨 Y 个文件夹
   - [Size] 总计
   - 文件类型: [breakdown]
   - 问题: [list problems]
   
   ## 提议结构
   
   ```
   [Directory]/
   ├── Work/
   │   ├── Projects/
   │   ├── Documents/
   │   └── Archive/
   ├── Personal/
   │   ├── Photos/
   │   ├── Documents/
   │   └── Media/
   └── Downloads/
       ├── To-Sort/
       └── Archive/
   ```
   
   ## 我将进行的更改
   
   1. **创建新文件夹**: [list]
   2. **移动文件**:
      - X PDFs → Work/Documents/
      - Y images → Personal/Photos/
      - Z old files → Archive/
   3. **重命名文件**: [any renaming patterns]
   4. **删除**: [duplicates or trash files]
   
   ## 需要您决定的文件
   
   - [List any files you're unsure about]
   
   准备好继续了吗？(yes/no/modify)
   ```

6. **执行组织**
   
   批准后，系统地组织：
   
   ```bash
   # 创建文件夹结构
   mkdir -p "path/to/new/folders"
   
   # 移动文件并清晰记录
   mv "old/path/file.pdf" "new/path/file.pdf"
   
   # 使用一致模式重命名文件
   # 示例: "YYYY-MM-DD - Description.ext"
   ```
   
   **重要规则**:
   - 在删除任何内容之前始终确认
   - 记录所有移动以便可能撤消
   - 保留原始修改日期
   - 优雅地处理文件名冲突
   - 如果遇到意外情况，请停止并询问

7. **提供摘要和维护提示**
   
   组织后：
   
   ```markdown
   # 组织完成! ✨
   
   ## 更改内容
   
   - 创建了 [X] 个新文件夹
   - 组织了 [Y] 个文件
   - 通过删除重复项释放了 [Z] GB
   - 归档了 [W] 个旧文件
   
   ## 新结构
   
   [Show the new folder tree]
   
   ## 维护提示
   
   保持组织：
   
   1. **每周**: 排序新下载
   2. **每月**: 审查并归档已完成的项目
   3. **每季度**: 检查新重复项
   4. **每年**: 归档旧文件
   
   ## 您的快速命令
   
   ```bash
   # 查找本周修改的文件
   find . -type f -mtime -7
   
   # 按类型排序下载
   [custom command for their setup]
   
   # 查找重复项
   [custom command]
   ```
   
   想组织另一个文件夹吗？
   ```

## 示例

### 示例 1: 组织下载 (来自 Justin Dielmann)

**用户**: "My Downloads folder is a mess with 500+ files. Help me organize it."

**过程**:
1. 分析下载文件夹
2. 查找模式：工作文档、个人照片、安装程序、随机 PDF
3. 提议结构：
   - Downloads/
     - Work/
     - Personal/
     - Installers/ (DMG, PKG files)
     - Archive/
     - ToSort/ (things needing decisions)
4. 请求确认
5. 根据内容和名称智能移动文件
6. 结果：500 个文件 → 5 个有组织的文件夹

### 示例 2: 查找并删除重复项

**用户**: "Find duplicate files in my Documents and help me decide which to keep."

**输出**:
```markdown
# 发现 23 组重复项 (总计 156 MB)

## 重复项组 1: "proposal.pdf"
- `/Documents/proposal.pdf` (2.3 MB, modified: 2024-03-15)
- `/Documents/old/proposal.pdf` (2.3 MB, modified: 2024-03-15)
- `/Desktop/proposal.pdf` (2.3 MB, modified: 2024-03-10)

**建议**: 保留 `/Documents/proposal.pdf` (正确位置的最新文件)
删除其他 2 个副本？

[继续处理所有重复项...]
```

### 示例 3: 重构项目文件夹

**用户**: "Review my ~/Projects directory and suggest improvements."

**输出**:
```markdown
# ~/Projects 分析

## 当前结构问题
- 混合了活跃和归档项目 (3 年以上)
- 没有一致的命名约定
- 一些项目在根目录，其他在随机子文件夹
- 重复文件夹 (project-name, project-name-old, project-name-v2)

## 提议结构

```
Projects/
├── Active/
│   ├── client-work/
│   ├── side-projects/
│   └── learning/
├── Archive/
│   ├── 2022/
│   ├── 2023/
│   └── 2024/
└── Templates/
```

## 具体更改
1. 移动 2022 年以来未触及的 12 个项目 → Archive/
2. 合并 4 个重复的项目文件夹
3. 将项目重命名为一致格式: "client-name-project-name"
4. 为旧工作创建 Archive

想让我执行这个吗？
```

### 示例 4: 按日期组织照片

**用户**: "Organize my photo folders by year and month."

**输出**: 创建如下结构：
```
Photos/
├── 2023/
│   ├── 01-January/
│   ├── 02-February/
│   └── ...
├── 2024/
│   ├── 01-January/
│   └── ...
└── Unsorted/
```

然后根据 EXIF 数据或文件修改日期移动照片。

## 常见组织任务

### 下载清理
```
Organize my Downloads folder - move documents to Documents, 
images to Pictures, keep installers separate, and archive files 
older than 3 months.
```

### 项目组织
```
Review my Projects folder structure and help me separate active 
projects from old ones I should archive.
```

### 重复删除
```
Find all duplicate files in my Documents folder and help me 
decide which ones to keep.
```

### 桌面清理
```
My Desktop is covered in files. Help me organize everything into 
my Documents folder properly.
```

### 照片组织
```
Organize all photos in this folder by date (year/month) based 
on when they were taken.
```

### 工作/个人分离
```
Help me separate my work files from personal files across my 
Documents folder.
```

##以此专业提示

1. **从小处着手**: 从一个凌乱的文件夹（如下载）开始以建立信任
2. **定期维护**: 每周对下载进行清理
3. **一致命名**: 对重要文件使用 "YYYY-MM-DD - Description" 格式
4. **积极归档**: 将旧项目移至 Archive 而不是删除
5. **保持活跃分离**: 在活跃和归档工作之间保持清晰界限
6. **相信过程**: 让 Claude 处理东西去哪里的认知负担

## 最佳实践

### 文件夹命名
- 使用清晰、描述性的名称
- 避免空格 (使用连字符或下划线)
- 具体: "client-proposals" 而不是 "docs"
- 使用前缀进行排序: "01-current", "02-archive"

### 文件命名
- 包含日期: "2024-10-17-meeting-notes.md"
- 描述性: "q3-financial-report.xlsx"
- 避免在名称中使用版本号 (改用版本控制)
- 移除下载伪影: "document-final-v2 (1).pdf" → "document.pdf"

### 何时归档
- 6 个月以上未触及的项目
- 稍后可能引用的已完成工作
- 迁移到新系统后的旧版本
- 犹豫是否删除的文件 (先归档)

## 相关用例

- 为新电脑设置组织
- 为备份/归档准备文件
- 存储清理前的清理
- 组织共享团队文件夹
- 构建新项目目录
