---
name: meta-cogbase
description: "认知底座的包管理器。搜索、安装、更新、卸载认知底座——给 AI agent 安装认知义体的一站式工具。"
---

# meta-cogbase

认知底座的包管理器——搜索、安装、更新、管理认知义体。

**命令**：
- `/meta-cogbase list` — 列出可用/已安装的认知底座
- `/meta-cogbase search <query>` — 按关键词搜索认知底座
- `/meta-cogbase install <name>` — 安装认知底座
- `/meta-cogbase uninstall <name>` — 卸载认知底座
- `/meta-cogbase update [--check|<name>|--all]` — 检查或执行更新
- `/meta-cogbase registry add <url>` — 添加 base 来源
- `/meta-cogbase registry list` — 列出已配置的来源
- `/meta-cogbase registry remove <name>` — 移除来源
- `/meta-cogbase registry refresh` — 刷新来源缓存
- `/meta-cogbase create <name>` — 创建新的认知底座（委托 cognitive-base-creator）
- `/meta-cogbase status` — 显示系统状态

---

## 目录结构

meta-cogbase 使用以下本地目录管理状态：

```
~/.meta-cogbase/
  sources.yml          # 已配置的来源列表
  installed.yml        # 已安装的 bases 记录
  cache/
    bases/             # git clone 缓存（按 base name）
    sources/           # 非官方源的缓存文件
```

首次执行任何命令时，如果 `~/.meta-cogbase/` 不存在，先初始化：
1. 创建上述目录结构
2. 创建 `sources.yml`，包含 official 源：
   ```yaml
   sources:
     - name: official
       type: built-in
       path: <this-skill-dir>/registry/official.yml
   ```
3. 创建空的 `installed.yml`：
   ```yaml
   installed: []
   ```

`<this-skill-dir>` 指本 skill 文件所在目录。agent 可通过检查 SKILL.md 的路径推导。

---

## 1. list — 列出认知底座

当用户执行 `/meta-cogbase list` 时执行。

**步骤**：

### 1.1 加载所有源
1. 读取 `~/.meta-cogbase/sources.yml`
2. 对每个源：
   - `type: built-in` → 直接读取 `path` 指向的 YAML 文件
   - `type: github-repo` / `github-stars` / `custom` → 读取 `cache_path` 指向的缓存文件。如果缓存不存在或超过 7 天，提示用户执行 `registry refresh`
3. 聚合所有源中的 bases 列表

### 1.2 标记安装状态
1. 读取 `~/.meta-cogbase/installed.yml`
2. 对每个 base，检查是否在 installed 列表中
3. 额外检查：如果 cognitive-kernel 已安装，读取 `~/.cognitive-kernel/cognitive-registry.yml`，交叉验证安装状态

### 1.3 格式化输出
以表格形式展示：

```
  NAME                    TIER  STATUS     DESCRIPTION
  first-principles        5     installed  审计假设，分解到可验证基础，无约束重建
  bayesian-reasoning      5     installed  从二元对错转向概率分布，用证据校准置信度
  systems-thinking        5     available  看到反馈循环、涌现、杠杆点的系统性视野
  ...
```

- `installed` = 已安装（绿色）
- `available` = 未安装（默认色）
- 按 tier 排序，同 tier 内按字母排序

### 1.4 过滤参数（可选）
- `/meta-cogbase list --installed` — 只显示已安装
- `/meta-cogbase list --available` — 只显示未安装
- `/meta-cogbase list --tier 5` — 按 tier 过滤

---

## 2. search — 搜索认知底座

当用户执行 `/meta-cogbase search <query>` 时执行。

**步骤**：
1. 按照 §1.1 加载所有源
2. 在每个 base 的以下字段中搜索 `<query>`（不区分大小写）：
   - `name`
   - `display_name`
   - `description`
   - `tags`
3. 按匹配度排序（name 完全匹配 > name 部分匹配 > tags 匹配 > description 匹配）
4. 以 §1.3 的表格格式输出结果
5. 如果无结果：提示"未找到匹配的认知底座。可以尝试 `/meta-cogbase registry add <url>` 添加更多来源。"

**示例**：
- `/meta-cogbase search 第一性原理` → 匹配 first-principles（description 包含关键词）
- `/meta-cogbase search reasoning` → 匹配 bayesian-reasoning, first-principles 等（tags/name 匹配）
- `/meta-cogbase search 矛盾` → 匹配 dialectical-thinking（description 包含"矛盾"）

---

## 3. install — 安装认知底座

当用户执行 `/meta-cogbase install <name>` 时执行。

**步骤**：

### 3.1 查找 base
1. 按照 §1.1 加载所有源
2. 在聚合列表中查找 `name` 完全匹配的 base
3. 如果未找到 → 报错："未找到名为 `<name>` 的认知底座。执行 `/meta-cogbase search <name>` 查看可用的底座。"
4. 如果找到多个同名（来自不同源）→ 列出来源让用户选择

### 3.2 检查是否已安装
1. 读取 `~/.meta-cogbase/installed.yml`
2. 如果已安装 → 提示："`<name>` 已安装（版本: <hash>）。要更新请用 `/meta-cogbase update <name>`。"

### 3.3 获取 base
1. 执行：`git clone --depth 1 <repo-url> ~/.meta-cogbase/cache/bases/<name>`
2. 如果缓存目录已存在 → 先执行 `git -C <cache-dir> pull` 更新
3. 验证 `<cache-dir>/manifest.yml` 存在
4. 验证 `manifest.yml` 中的 `schema_version` 字段（当前支持 v1）

### 3.4 执行安装
检测 cognitive-kernel 是否可用：

**方式 A：通过 kernel 安装（推荐）**
如果 `~/.cognitive-kernel/cognitive-registry.yml` 存在：
1. 告知用户："检测到 cognitive-kernel，将通过 kernel 安装（自动冲突分析）。"
2. 调用 `/cognitive-kernel install ~/.meta-cogbase/cache/bases/<name>`
3. kernel 会处理：冲突分析、预算检查、registry 注册、运行时重新生成

**方式 B：独立安装（降级）**
如果 kernel 未安装：
1. 告知用户："未检测到 cognitive-kernel，将使用独立安装模式。"
2. 检查 `<cache-dir>/install.sh` 是否存在且可执行
3. 执行：`bash <cache-dir>/install.sh`
4. install.sh 会自行检测平台并安装

### 3.5 记录安装
在 `~/.meta-cogbase/installed.yml` 中添加记录：
```yaml
- name: <name>
  version: <git-commit-hash>  # 通过 git -C <cache-dir> rev-parse HEAD 获取
  installed_at: <ISO-timestamp>
  source: <source-name>
  install_method: kernel | standalone
```

### 3.6 报告结果
```
✓ <name> 已安装
  方法: kernel（含冲突分析）/ standalone
  版本: <short-hash>
  来源: <source-name>
```

---

## 4. uninstall — 卸载认知底座

当用户执行 `/meta-cogbase uninstall <name>` 时执行。

**步骤**：

### 4.1 检查是否已安装
1. 读取 `~/.meta-cogbase/installed.yml`
2. 如果未安装 → 报错："<name> 未安装。"

### 4.2 执行卸载
根据 `install_method` 选择方式：

**方式 A：通过 kernel 卸载**
如果 `install_method: kernel` 且 kernel 仍可用：
1. 调用 `/cognitive-kernel uninstall <name>`

**方式 B：独立卸载**
如果 `install_method: standalone` 或 kernel 不可用：
1. 执行：`bash ~/.meta-cogbase/cache/bases/<name>/install.sh --uninstall`

### 4.3 清理记录
1. 从 `~/.meta-cogbase/installed.yml` 中移除该 base 的记录
2. 可选：删除 `~/.meta-cogbase/cache/bases/<name>/` 缓存目录

### 4.4 报告结果
```
✓ <name> 已卸载
```

---

## 5. update — 检查和执行更新

### 5.1 `update --check`

检查所有已安装 bases 是否有新版本。

**步骤**：
1. 读取 `~/.meta-cogbase/installed.yml`
2. 对每个已安装的 base：
   - 获取记录的 version（commit hash）
   - 查询远程最新版本：`git ls-remote <repo-url> HEAD` → 提取 hash
   - 对比两个 hash
3. 输出：
   ```
   NAME                 LOCAL     REMOTE    STATUS
   first-principles     a1b2c3d   e4f5g6h   有更新
   bayesian-reasoning   x7y8z9a   x7y8z9a   已是最新
   ...
   ```

### 5.2 `update <name>`

更新指定 base。

**步骤**：
1. 检查 base 是否已安装
2. 先卸载（§4 流程）
3. 再安装（§3 流程，会 clone 最新版本）
4. 报告更新前后的版本

### 5.3 `update --all`

更新所有有新版本的 bases。

**步骤**：
1. 执行 §5.1 获取有更新的 bases 列表
2. 逐个执行 §5.2
3. 汇总报告

---

## 6. registry — 来源管理

### 6.1 `registry add <url>`

添加新的 base 来源。

**步骤**：

1. **识别 URL 类型**：
   - 匹配 `github.com/<user>/<repo>` → `type: github-repo`
   - 匹配 `github.com/<user>?tab=stars` 或 `github.com/stars/<user>` → `type: github-stars`
   - 以 `.yml` 或 `.yaml` 结尾 → `type: custom`
   - 其他 → 询问用户类型

2. **按类型获取数据**：

   **github-repo**：
   1. `git clone --depth 1 <url> /tmp/meta-cogbase-probe-<random>`
   2. 检查根目录是否有 `manifest.yml` → 单 base 仓库
   3. 如果没有，扫描子目录是否有 `manifest.yml` → 多 base 集合
   4. 为找到的每个 base 构建 registry entry
   5. 写入缓存：`~/.meta-cogbase/cache/sources/<repo-name>.yml`
   6. 清理临时目录

   **github-stars**：
   1. 提取用户名
   2. 调用 GitHub API：`curl -s "https://api.github.com/users/<user>/starred?per_page=100"`
   3. 对每个 starred repo，检查是否包含 `manifest.yml`（通过 GitHub API 查文件树，或 `curl -sf <raw-url>/manifest.yml`）
   4. 为匹配的 repos 构建 registry entries
   5. 写入缓存
   6. **注意**：未认证 API 限制 60 次/小时。如果 starred repos 很多，提醒用户可能需要多次 refresh

   **custom**：
   1. `curl -sf <url>` 下载 YAML
   2. 验证格式符合 registry schema（有 `registry_version`、`bases` 列表）
   3. 写入缓存

3. **更新 sources.yml**：
   ```yaml
   - name: <derived-name>  # 从 URL 推导，如 repo name 或 username-stars
     type: <detected-type>
     url: <original-url>
     cache_path: ~/.meta-cogbase/cache/sources/<name>.yml
     cached_at: <ISO-timestamp>
   ```

### 6.2 `registry list`

列出所有已配置的来源。

**步骤**：
1. 读取 `~/.meta-cogbase/sources.yml`
2. 对每个源，统计其中的 base 数量
3. 输出：
   ```
   NAME        TYPE          BASES  CACHED AT
   official    built-in      19     (always fresh)
   my-repo     github-repo   3      2026-04-15
   alice-stars github-stars  7      2026-04-14
   ```

### 6.3 `registry remove <name>`

**步骤**：
1. 如果 `name` 是 "official" → 拒绝："官方源不能移除。"
2. 从 `sources.yml` 中移除对应条目
3. 删除对应的缓存文件

### 6.4 `registry refresh`

刷新所有非内置源的缓存。

**步骤**：
1. 对每个非 `built-in` 的源，重新执行 §6.1 的数据获取流程
2. 更新 `cached_at` 时间戳
3. 报告刷新了多少个源、多少个 bases

---

## 7. create — 创建新的认知底座

当用户执行 `/meta-cogbase create <name>` 时执行。

**步骤**：
1. 告知用户："委托给 cognitive-base-creator。"
2. 调用 `/cognitive-base-creator`，传入 `<name>` 作为框架名称
3. creator 会引导用户完成创建流程并生成完整的 base 文件集

---

## 8. status — 系统状态

当用户执行 `/meta-cogbase status` 时执行。

**步骤**：
1. 检查 `~/.meta-cogbase/` 是否存在（已初始化？）
2. 统计：
   - 已配置源数量 + 可用 bases 总数
   - 已安装 bases 数量
   - cognitive-kernel 是否可用
   - cognitive-base-creator 是否可用
3. 输出：
   ```
   meta-cogbase status:
     初始化: ✓
     来源: 2 个 (22 个可用 bases)
     已安装: 5 个 bases
     cognitive-kernel: ✓ 已安装
     cognitive-base-creator: ✓ 已安装
   ```

---

## Registry YAML Schema

所有源文件（包括 official.yml 和缓存的源）遵循同一格式：

```yaml
registry_version: 1
name: <source-name>
description: <optional description>
bases:
  - name: <kebab-case-name>        # 必填
    display_name: <display name>    # 可选
    description: <one-line desc>    # 必填
    tier: 5 | 6                     # 必填
    tags: [tag1, tag2]              # 可选，用于搜索
    repo: <git-clone-url>           # 必填
    schema_version: 1               # 必填
```

---

## 与 cognitive-kernel 的协作模式

meta-cogbase 和 cognitive-kernel 的职责划分：

| 操作 | meta-cogbase | cognitive-kernel |
|------|-------------|-----------------|
| 发现 bases | ✓（搜索、浏览目录） | — |
| 获取 bases | ✓（git clone） | — |
| 安装 bases | 委托 → | ✓（冲突分析、6层装配） |
| 卸载 bases | 委托 → | ✓（清理、重新生成） |
| 版本管理 | ✓（对比、更新） | — |
| 来源管理 | ✓（添加/移除源） | — |
| 运行时执行 | — | ✓（L1-L6 干预） |

**降级模式**：如果 kernel 未安装，meta-cogbase 使用每个 base 自带的 `install.sh` 直接安装。功能可用但无冲突分析和 6 层装配。

---

## 错误处理

| 场景 | 处理 |
|------|------|
| git clone 失败 | 报告错误，检查网络连接和 URL 有效性 |
| manifest.yml 不存在 | 报告"该仓库不是有效的认知底座（缺少 manifest.yml）" |
| schema_version 不兼容 | 报告版本不匹配，建议更新 meta-cogbase |
| kernel 不可用 | 自动降级为 standalone 模式，告知用户 |
| GitHub API rate limit | 报告限制，建议等待或使用 `GITHUB_TOKEN` 环境变量 |
| 源缓存过期（>7天） | 提示执行 `registry refresh` |
