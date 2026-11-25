---
name: hexo-blog-manager
description: |
  Hexo 博客一键管理工具，配置文件位于 ~/.config/hexo/config.yaml。
  
  核心功能：
  1. 一键创建博客：自动生成封面 → 上传 OSS → 创建 Markdown → 提交 GitHub
  2. AI 封面生成：调用自定义 API（默认 gpt-image-2），支持 16:9 封面
  3. 图片托管：上传到 GitHub_Oss 仓库，生成 jsDelivr CDN 链接
  4. 双重认证：支持 gh CLI（默认）或 GitHub Personal Access Token
  5. 配置管理：统一管理 API Key、GitHub Token、仓库路径等
  
  脚本说明：
  - hexo_config.py：配置读写（init/show/check/set-api-key/set-github-token）
  - generate_cover.py：封面生成（--title/--style/--model）
  - upload_prep.py：OSS 上传准备（Base64 编码）
  - create_post.py：一键创建博客（整合以上所有步骤）
  
  触发场景：用户提到创建博客、发布文章、生成封面、上传图片、Hexo 配置、
  博客管理、图片托管、GitHub 认证时使用。
compatibility: opencode
---

# Hexo Blog & OSS Resource Manager Skill

This skill defines the standard operating procedure (SOP) dedicated to managing blog posts in the `imHansiy/MyHexo` repository and the associated static assets / image hosting in the `imHansiy/GitHub_Oss` repository.

## Configuration

### 配置文件位置
- **路径**: `~/.config/hexo/config.yaml`
- **首次使用**: 运行 `python <SKILL_PATH>/scripts/hexo_config.py init` 创建默认配置

### 配置结构
```yaml
image_api:
  base_url: "https://ducksaymay-lumina.hf.space"  # API 地址
  api_key: "your-api-key-here"                      # API 密钥（必填）
  model: "gpt-image-2"                              # 图片生成模型
  size: "1792x1024"                                 # 图片尺寸（16:9）
  default_prompt_style: "cinematic tech-futuristic style, vibrant lighting, 8k resolution"

github:
  token: "ghp_xxxxxxxxxxxx"      # GitHub Personal Access Token
  use_gh_cli: true                # 是否使用 gh CLI 认证（优先级高于 token）

github_oss:
  repo: "imHansiy/GitHub_Oss"
  cdn_base: "https://jsdelivr.007666.xyz/gh/imHansiy/GitHub_Oss@main"

hexo_blog:
  repo: "imHansiy/MyHexo"
  posts_path: "source/_posts"
```

### GitHub 认证方式

支持两种认证方式（按优先级）：

| 方式 | 配置 | 说明 |
|------|------|------|
| **gh CLI**（默认） | `use_gh_cli: true` | 使用 `gh auth login` 的 OAuth token |
| **Personal Access Token** | `token: "ghp_xxx"` | 直接使用 GitHub PAT |

#### 使用 gh CLI（推荐）
```bash
# 先登录 GitHub CLI
gh auth login

# 配置自动使用 gh CLI
python hexo_config.py show  # 确认 use_gh_cli: true
```

#### 使用 GitHub Token
```bash
# 设置 GitHub Personal Access Token
python hexo_config.py set-github-token ghp_xxxxxxxxxxxxxxxxxxxx
```

**Token 权限要求**：
- `repo` - 完整仓库访问权限
- `workflow` - 如果需要触发 GitHub Actions

### 配置管理命令
```bash
# 查看当前配置
python <SKILL_PATH>/scripts/hexo_config.py show

# 检查配置完整性
python <SKILL_PATH>/scripts/hexo_config.py check

# 设置图片 API Key
python <SKILL_PATH>/scripts/hexo_config.py set-api-key <your-api-key>

# 设置 GitHub Token（如果不使用 gh CLI）
python <SKILL_PATH>/scripts/hexo_config.py set-github-token <your-github-token>

# 初始化默认配置
python <SKILL_PATH>/scripts/hexo_config.py init
```

---

## 一键创建博客（推荐）

### 命令格式
```bash
python <SKILL_PATH>/scripts/create_post.py --title "博客标题" [选项]
```

### 选项参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `--title`, `-t` | 博客标题（必填） | `--title "Python 入门教程"` |
| `--tags` | 标签，逗号分隔 | `--tags "Python,编程,教程"` |
| `--category`, `-c` | 分类 | `--category "编程"` |
| `--skip-cover` | 跳过封面生成 | `--skip-cover` |
| `--skip-upload` | 跳过封面上传 | `--skip-upload` |
| `--auto-commit` | 自动提交到 GitHub | `--auto-commit` |
| `--output`, `-o` | 输出目录 | `--output ./posts` |

### 使用示例
```bash
# 基础用法（生成封面 + 创建 Markdown）
python <SKILL_PATH>/scripts/create_post.py --title "我的第一篇博客"

# 完整用法（自动提交）
python <SKILL_PATH>/scripts/create_post.py \
  --title "Python 异步编程指南" \
  --tags "Python,异步,编程" \
  --category "技术" \
  --auto-commit

# 跳过封面（快速创建）
python <SKILL_PATH>/scripts/create_post.py \
  --title "快速笔记" \
  --skip-cover \
  --auto-commit
```

### 自动化流程
```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 检查配置                                        │
│  → 验证 API Key 和配置完整性                             │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: 生成封面图片                                    │
│  → 调用 AI API 生成 16:9 封面                            │
│  → 保存到临时目录                                        │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: 上传封面到 OSS                                  │
│  → 上传到 GitHub_Oss 仓库                               │
│  → 获取 CDN 链接                                         │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Step 4: 创建 Markdown 文件                              │
│  → 生成带 Frontmatter 的 .md 文件                        │
│  → 包含标题、日期、标签、封面链接                         │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Step 5: 提交到 GitHub（可选）                           │
│  → 复制到 Hexo 仓库                                     │
│  → git commit & push                                    │
└─────────────────────────────────────────────────────────┘
```

### 首次配置流程
1. 运行 `python <SKILL_PATH>/scripts/hexo_config.py init` 创建配置文件
2. 提示用户提供 API Key
3. 运行 `python <SKILL_PATH>/scripts/hexo_config.py set-api-key <key>` 保存
4. 验证配置: `python <SKILL_PATH>/scripts/hexo_config.py check`

---

## Workflow

### 0. 一键创建博客（推荐）
使用 `create_post.py` 脚本可以一键完成博客创建的全部流程：
```bash
python <SKILL_PATH>/scripts/create_post.py --title "博客标题" --tags "标签1,标签2" --category "分类"
```
详见上方「一键创建博客」章节。

---

### 1. Image Preparation & Upload (Image Hosting Flow)
When a Hexo post requires an image (screenshot, diagram, asset):
- **Target Repository**: `imHansiy/GitHub_Oss`
- **Target Path**: `img/YY-MM-DD/filename.extension` (Use the current date to categorize files).
- **Steps**:
    1. Read the image file and encode it to Base64.
    2. Write a JSON payload containing `{"message": "...", "content": "..."}` to a temporary file.
    3. Execute the upload using `gh api --method PUT ... --input temp.json`.
- **CDN Link Format**: `https://jsdelivr.007666.xyz/gh/imHansiy/GitHub_Oss@main/img/YY-MM-DD/filename.extension`

### 2. Blog Cover Generation (AI-Powered)
To make the Hexo blog post list look more professional and textured, generate a cover image using the configured API:

- **Service**: Custom Image Generation API (configured in `~/.config/hexo/config.yaml`)
- **Default Model**: `gpt-image-2`
- **Default Size**: `1792x1024` (16:9 ratio, suitable for blog covers)

#### Steps:
1. **Check Configuration**: Verify API config is complete:
   ```bash
   python <SKILL_PATH>/scripts/hexo_config.py check
   ```
   If not configured, guide user to set up API key.

2. **Generate Image**: Run the script with title or custom prompt:
   ```bash
   # Using blog title (auto-generates professional prompt)
   python <SKILL_PATH>/scripts/generate_cover.py --title "Your Blog Title" cover.png
   
   # Using custom prompt
   python <SKILL_PATH>/scripts/generate_cover.py "A futuristic tech workspace with holographic displays" cover.png
   
   # With custom style
   python <SKILL_PATH>/scripts/generate_cover.py --title "Your Title" --style "minimalist, dark theme" cover.png
   ```

3. **User Review (Mandatory)**: Show the generated `cover.png` to the user and **wait for user confirmation** before proceeding. If the user is not satisfied, adjust the prompt and regenerate.

4. **Store Assets**: Only after user approval, upload the image to the `GitHub_Oss` repository:
   - Run: `python <SKILL_PATH>/scripts/upload_prep.py cover.png "oss: add blog cover"`
   - Execute: `gh api --method PUT /repos/imHansiy/GitHub_Oss/contents/img/YY-MM-DD/cover.png --input temp_payload.json`

5. **Environment Cleanup**: After a successful upload, you **must delete** all locally generated image files, temporary JSON files, and any temporary scripts used during the process.

- **Frontmatter Setup**: Add the `banner: <CDN_LINK>` and `headimg: <CDN_LINK>` fields to the Hexo post's metadata (Frontmatter) to configure the cover display in the Hexo environment.

### 3. Create or Update Hexo Blog Post
- **Target Repository**: `imHansiy/MyHexo`
- **Target Path**: `source/_posts/your-post-title.md`
- **Frontmatter Specification**: Must contain header information compliant with Hexo standards:
  ```yaml
  ---
  title: Post Title
  date: YYYY-MM-DD HH:mm:ss
  tags: [Tag1, Tag2]
  categories: [Category1]
  banner: <CDN_LINK>
  headimg: <CDN_LINK>
  ---
  ```
- **Image Referencing Convention**: The body of the article must **always use** the jsDelivr CDN links constructed in Step 1.

## Rules & Best Practices

- **Atomic Commits**: Use descriptive commit messages, such as `oss: add screenshot for post X` or `feat: new hexo post about Y`.
- **Base64 Encoding**: Always encode binary files (like images) into Base64 format before transmitting them via `gh api`.
- **Bypassing Command Line Limits**: Avoid passing huge Base64 strings directly as command-line arguments; always save them to a temporary JSON file and pass them using the `--input` argument.
- **Result Verification**: After uploading, verify that the file successfully exists via `gh api` before officially writing the image link into the Hexo post.
- **Configuration First**: Always check configuration before using image generation features. Prompt user for API key if not configured.

## Applicable Scenarios
This is a **Hexo-专用 (Hexo-dedicated)** skill. Whenever the user mentions:
- Publishing a blog post
- Adding an article to Hexo
- Uploading a cover for a Hexo article
- Adding an image to the OSS hosting
- Configuring Hexo blog settings

This skill should be triggered and applied.
