---
name: social-corpus-harvest
description: Collect a verified person, creator, brand, or organization's self-authored public Xiaohongshu, Douyin, and Weibo posts into a local, traceable Markdown dataset with source URLs and provenance. Use for public-content archiving, personal knowledge bases, search/RAG ingestion, content audits, writing-style analysis, portfolio migration, research datasets, or consented AI persona/training preparation. Includes user-local setup, Chrome login guidance, verified account mapping, collection, and review; excludes private content and unverified authorship.
---

# Social Corpus Harvest

把经过人工核验的公开社媒内容整理成一套本地、可搜索、可追溯的 Markdown 数据集。它不只服务于 AI 分身，也适合内容归档、知识库、RAG、风格分析、作品迁移和经授权的数据准备。

## 它对大众有什么用

- **个人或创作者归档**：备份本人公开发布过的文字，保留原始链接和抓取时间。
- **知识库 / RAG**：把分散在多个平台的公开内容转为结构化 Markdown，供本地搜索、问答或检索系统使用。
- **内容复盘**：分析主题、表达方式、发布时间和平台差异。
- **研究与迁移**：为作品集、内容迁移或经过授权的研究准备可核验来源。
- **AI 数据准备**：在身份、版权和用途获得授权后，作为风格建模、AI 人格或训练数据的候选集。

典型请求：

- “把我公开的小红书和微博文章归档到本地。”
- “整理这个创作者本人发布的公开内容，做一个可追溯知识库。”
- “先预览能采集哪些账号和帖子，不要直接下载。”
- “更新上次的数据集，并保留来源清单。”

## 先说明边界

只采集用户明确指定、公开可见、且已经人工核验归属的账号内容。

- 不根据相似昵称猜账号。
- 不采集私密内容、评论区、转发附文、粉丝二创或其他用户的文字。
- 不索取或保存密码、Cookie、Session Token、验证码答案。
- 默认只采集帖子文字和公开元数据；下载或转录音视频必须另行确认。
- 采集成功不等于拥有再发布、商业使用或模型训练权。根据最终用途单独确认版权、平台规则、隐私和主体授权。

## 1. 检查环境

始终从本 Skill 目录运行：

```bash
python scripts/bootstrap.py check --json
```

若 `automatic_ready` 为 `false`，阅读 [first-run.md](references/first-run.md)，向用户说明安装范围，并在获得同意后运行：

```bash
python scripts/bootstrap.py install
```

安装只发生在用户目录，不使用 `sudo`。不要安装与本任务无关的 Agent Reach 渠道。

若自动依赖已就绪但 `ready` 仍为 `false`：

1. 运行 `python scripts/bootstrap.py open-extension`。
2. 请用户安装或启用官方 OpenCLI Chrome 扩展，并保持 Chrome 打开。
3. 运行 `python scripts/bootstrap.py connect`。
4. 只对用户选择的平台运行 `python scripts/bootstrap.py login <platform>`。
5. 让用户在 Chrome 中完成登录或平台安全验证。

只有当 `bootstrap.py check --json` 返回 `ready: true` 时，才说明环境配置完成。

## 2. 确认采集计划

开始前确认：

- 数据主体和准确的主页链接；
- 谁核验了账号，以及核验依据；
- 平台、日期范围、每个平台的数量上限；
- 结果用途：归档、知识库、分析、迁移、研究或 AI 数据准备；
- 仅需公开文字/标题，还是另行授权音视频处理。

用途会影响后续筛选与权利检查，但不会扩大采集范围。

## 3. 建立已核验账号映射

优先使用初始化脚本：

```bash
python scripts/init_profile_map.py "<OUT_DIR>" \
  --subject "主体名称" \
  --verified-by "核验人" \
  --evidence "账号本人提供主页链接" \
  --xiaohongshu "https://www.xiaohongshu.com/user/profile/<id>"
```

只在对应主页已确认时添加 `--douyin` 或 `--weibo`。检查生成的 `<OUT_DIR>/corpus/social_profiles.json`；字段说明见 [profile-map.md](references/profile-map.md)。

初始化脚本会移除临时签名参数，并默认拒绝覆盖已有映射；只有明确需要重建时才使用 `--force`。

## 4. 先预览，再采集

先做只读预检：

```bash
python scripts/harvest_social_corpus.py "<OUT_DIR>" \
  --name "主体名称" \
  --dry-run
```

确认账号映射、平台和限制无误后再采集：

```bash
python scripts/harvest_social_corpus.py "<OUT_DIR>" \
  --name "主体名称"
```

使用 `--refresh` 更新已有采集。`--auto` 只适用于已经采用 `corpus/research_pool.md` 质量门槛的集成流程；普通归档或知识库任务不需要它。

采集器会在账号核验字段、Browser Bridge 或平台适配命令缺失时停止。不要绕过严格映射；只有人工审查过旧项目并明确接受旧证据时，才使用 `--allow-legacy-map`。

## 5. 审核和交付

采集后：

1. 阅读 JSON 汇总，处理每个 `failed_platforms`。
2. 抽查 `corpus/public_social/<platform>/` 中的 Markdown 与原始链接是否一致。
3. 排除转载、他人评论、空文本和作者不一致的内容。
4. 根据最终用途做筛选：适合归档的内容不一定适合公开再发布、RAG 或训练。
5. 将 `corpus/public_social/source_manifest.json` 与数据集一起保留。

最终输出包括：

- 每篇公开内容对应的 Markdown 文件；
- 已核验的账号映射；
- 原始链接、作者、账号标识、发布时间和抓取时间；
- 采集汇总、失败项和来源清单。

## Bundled resources

- `scripts/bootstrap.py`：依赖安装、环境检查、扩展入口和显式登录。
- `scripts/init_profile_map.py`：创建已核验账号映射。
- `scripts/harvest_social_corpus.py`：采集公开内容并写入来源信息。
- `references/first-run.md`：首次使用和常见阻塞处理。
- `references/dependencies.md`：依赖版本、来源和安装边界。
- `references/profile-map.md`：账号映射字段和核验规则。
