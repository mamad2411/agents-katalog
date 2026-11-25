---
name: mcp-registry-publish
description: 将 MCP 项目发布到官方 MCP Registry（registry.modelcontextprotocol.io）的完整工作流：国际化前置、.mcpb 打包、server.json 生成、GitHub Actions 集成（-registry 后缀 tag 显式触发）、发布与验证。使用 /mcp-registry-publish 或要求"发布到官方 MCP Registry"时调用。
---

# Skill: 发布到官方 MCP Registry

将 MCP server 发布到 [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) 的完整流程。本文是**通用模板**，所有 `<占位符>` 按项目替换；两个实战案例均已成功发布：2native-ssh-mcp v1.4.1、websearch-mcpserver v3.1.1（2026-08-29）。

## 使用场景

- 新 MCP 项目要注册官方 MCP Registry
- 已有项目要加 registry 自动发布（含 .mcpb 打包）
- 发布后验证注册状态

## 核心设计（推荐，可调整）

1. **发布是显式动作**：普通 tag（`v1.0.0`）只构建 release；带 `-registry` 后缀的 tag（`v1.0.1-registry`）才触发 registry 发布——避免有问题的版本漏出去
2. **发布前先国际化**：README/docs 英文为主（国际曝光），中文保留为 `.zh-CN.md`，顶部互链
3. **描述规范易读**：registry 的 description 一句话覆盖核心功能 + 安全特性，**≤ 100 字符**（registry API 硬限制，超长 422 拒绝）
4. **打包用 Go CLI 而非 shell/jq**：`mcpb-tool-cli`（独立开源项目，[github.com/daidaiJ/mcpb-tool-cli](https://github.com/daidaiJ/mcpb-tool-cli)，MIT）完成 .mcpb 打包与 server.json 生成，消除 `${__dirname}` 转义、平台映射、sha256 提取等 bash/jq 脆弱点，agent 无需调试脚本
5. **本 skill 自带工具**：`tools/mcp-publisher/mcp-publisher.exe`（Windows 版官方发布器二进制，免下载）；mcpb CLI 通过 `go install github.com/daidaiJ/mcpb-tool-cli@latest` 获取（源码公开可审查，不内置副本）

## 自带工具

```
tools/
└── mcp-publisher/           # 官方发布器（Windows amd64 版，2026-08-29 下载）
    └── mcp-publisher.exe    #   init/login/publish/status/validate
```

- **mcpb CLI**：独立开源项目 [mcpb-tool-cli](https://github.com/daidaiJ/mcpb-tool-cli)（零依赖 Go 标准库，MIT）。安装：`go install github.com/daidaiJ/mcpb-tool-cli@latest`；workflow 中 `go install` 后直接调用 `mcpb` 命令；本地验证同样适用
- **mcp-publisher**：Windows 直接用 `<skill>/tools/mcp-publisher/mcp-publisher.exe`；其他平台从 `github.com/modelcontextprotocol/registry` releases 下载（`mcp-publisher_<os>_<arch>.tar.gz`，Go 二进制非 npm 包）；下载慢/超时走代理（设置 `HTTPS_PROXY` 指向本地代理）

## 前置条件检查（agent 逐项确认）

- [ ] 代码层已英文（MCP 工具描述、错误消息）——MCP 生态标准语言；中文工具描述不影响发布但影响国际曝光
- [ ] README 英文版存在（registry 收录需要国际可读）
- [ ] 已有 release 工作流（6 平台构建，参考 go-release-workflow skill）
- [ ] 本地有 gh CLI 且已登录（`gh auth status`）
- [ ] 确认 GitHub 仓库 owner（registry 名称必须是 `io.github.<owner>/<name>`，发布者需拥有该仓库）
- [ ] 确认二进制名（registry 只发布 MCP server 本体，CLI 等附属二进制不进 registry）

## 官方信息源（发布前核对，避免用过时格式）

- 发布指南：`https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx`
- GitHub Actions 自动发布：`docs/modelcontextprotocol-io/github-actions.mdx`（OIDC 流程：`id-token: write` + `mcp-publisher login github-oidc`，免 secrets）
- mcpb 格式规范：`github.com/modelcontextprotocol/mcpb`（MANIFEST.md + examples/calculator-rust）
- server.json schema：`https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`
- 验证器源码（格式硬约束）：registry 仓库 `internal/validators/registries/mcpb.go`

### 2026-08-29 查证结论（schema/验证器源码核对）

- **packages 条目无 platform 字段**：多平台 = 多个 packages 条目（每平台一个 .mcpb URL），平台信息在 mcpb 内部 manifest 的 `compatibility.platforms` 声明
- **description ≤ 100 字符**：schema `maxLength: 100`，超长 registry API 返回 422
- **name 格式**：`^[a-zA-Z0-9.-]+/[a-zA-Z0-9._-]+$`（如 `io.github.<owner>/<name>`）
- **repository 必填** `url` + `source`（github/gitlab）
- **mcpb 包硬约束**（验证器强制）：`fileSha256` 必填；`identifier` 必须 https、host 限 github.com/gitlab.com、URL 必须含 `mcp`（.mcpb 后缀满足）、路径必须匹配 `/owner/repo/releases/download/tag/filename`；验证器 HEAD 检查 URL（200 或 302+Location 均可）
- **manifest version 不带 v**：mcpb MANIFEST.md 要求 semantic version（`1.0.0`），server.json version 同样去 v

## 完整流程

### 0. 安装 mcpb CLI

```bash
go install github.com/daidaiJ/mcpb-tool-cli@latest   # 源码公开：github.com/daidaiJ/mcpb-tool-cli
```

两个子命令：

```
mcpb pack <flags>        # 生成 <name>-<os>-<arch>.mcpb（zip: manifest.json + server/<binary>）+ .sha256
  --binary <path>        # 平台二进制路径
  --name <name>          # 机器名（manifest name + bundle 文件名）
  --display <display>    # display_name
  --version <v>          # 版本（自动去 v 前缀）
  --description <desc>
  --author <author>
  --os <linux|windows|darwin>   # 自动映射 win32
  --arch <amd64|arm64>
  --out <dir>

mcpb serverjson <flags>  # 从 .mcpb 目录生成 server.json（packages 数组 + 100 字符描述校验）
  --dir <mcpb-dir>       # 含 *.mcpb + *.mcpb.sha256
  --name <io.github.owner/repo>
  --title <title>
  --description <desc>   # >100 字符直接报错（提前发现，避免 422）
  --version <v>
  --repo-url <url>       # 自动推断 source（github/gitlab）
  --base-tag <v1.0.0>    # release tag，用于拼下载 URL
  --expect-packages <N>  # 期望包数量（如 6），不匹配报错——防平台缺失
  --out <path>           # 默认 stdout
```

`mcpb pack` 打包后自动自检：zip 可读 + manifest.json 与 server/<binary> 条目齐全，损坏产物直接报错。

### 1. 修改 release.yml（三处）

参考实现（已验证）：[daidaiJ/2native-ssh-mcp 的 release.yml](https://github.com/daidaiJ/2native-ssh-mcp/blob/HEAD/.github/workflows/release.yml)、[daidaiJ/websearch-mcpserver 的 release.yml](https://github.com/daidaiJ/websearch-mcpserver/blob/HEAD/.github/workflows/release.yml)

**build job**：`if: ${{ !endsWith(github.ref_name, '-registry') }}` + mcpb 打包步骤

```yaml
  build:
    name: Build ${{ matrix.goos }}-${{ matrix.arch }}
    if: ${{ !endsWith(github.ref_name, '-registry') }}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          - goos: windows
            arch: amd64
            ext: .exe
          - goos: windows
            arch: arm64
            ext: .exe
          - goos: linux
            arch: amd64
            ext: ''
          - goos: linux
            arch: arm64
            ext: ''
          - goos: darwin
            arch: amd64
            ext: ''
          - goos: darwin
            arch: arm64
            ext: ''
    steps:
      # ... checkout / setup-go / tidy ...
      - name: Build
        env:
          CGO_ENABLED: '0'
          GOOS: ${{ matrix.goos }}
          GOARCH: ${{ matrix.arch }}
        run: |
          mkdir -p dist
          go build -trimpath -ldflags "-s -w -X main.version=${{ github.ref_name }}" \
            -o dist/<binary>-${{ matrix.goos }}-${{ matrix.arch }}${{ matrix.ext }} .
      - name: Package MCPB bundle
        run: |
          go install github.com/daidaiJ/mcpb-tool-cli@latest
          mcpb pack \
            --binary "dist/<binary>-${{ matrix.goos }}-${{ matrix.arch }}${{ matrix.ext }}" \
            --name <binary> --display "<Display Name>" \
            --version "${{ github.ref_name }}" \
            --description "<≤100 chars>" --author <owner> \
            --os "${{ matrix.goos }}" --arch "${{ matrix.arch }}" --out dist
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: <binary>-${{ matrix.goos }}-${{ matrix.arch }}
          path: |
            dist/<binary>-${{ matrix.goos }}-${{ matrix.arch }}${{ matrix.ext }}
            dist/<binary>-${{ matrix.goos }}-${{ matrix.arch }}.mcpb
            dist/<binary>-${{ matrix.goos }}-${{ matrix.arch }}.mcpb.sha256
          if-no-files-found: error
```

**release job**：`if: ${{ !endsWith(github.ref_name, '-registry') }}`；release notes 用 **gh api 读 annotated tag message**（本地 checkout 的 lightweight tag 不可信，`%(contents)` 会 fallback 到 commit message）；`gh release create` 幂等（先 `delete --yes || true`）；checksum 循环跳过 `.sha256`

```yaml
  release:
    name: Create release
    needs: build
    if: ${{ !endsWith(github.ref_name, '-registry') }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Read tag message
        id: tag
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          REF="$(gh api "repos/$GITHUB_REPOSITORY/git/refs/tags/${{ github.ref_name }}")"
          TYPE="$(echo "$REF" | jq -r '.object.type')"
          if [ "$TYPE" = "tag" ]; then
            SHA="$(echo "$REF" | jq -r '.object.sha')"
            gh api "repos/$GITHUB_REPOSITORY/git/tags/$SHA" --jq '.message' > notes.md
          else
            echo "${{ github.ref_name }}" > notes.md
          fi
      - name: Download binaries
        uses: actions/download-artifact@v4
        with:
          path: dist
          merge-multiple: true
      - name: Generate checksums
        run: |
          cd dist
          for f in <binary>-*; do
            [ -f "$f" ] || continue
            case "$f" in *.sha256) continue ;; esac
            sha256sum "$f" > "$f.sha256"
          done
      - name: Create release
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh release delete "${{ github.ref_name }}" --yes || true
          gh release create "${{ github.ref_name }}" dist/<binary>-* \
            --title "${{ github.ref_name }}" --notes-file notes.md
```

**publish-registry job**（新增）：

```yaml
  publish-registry:
    name: Publish to MCP Registry
    if: ${{ endsWith(github.ref_name, '-registry') }}
    runs-on: ubuntu-latest
    permissions:
      id-token: write   # OIDC 必需
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - name: Download MCPB bundles
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          TAG="${GITHUB_REF#refs/tags/}"          # v1.0.0-registry
          BASE_TAG="${TAG%-registry}"             # v1.0.0
          mkdir -p mcpb-assets
          gh release download "$BASE_TAG" \
            --pattern "*.mcpb" --pattern "*.mcpb.sha256" --dir mcpb-assets
      - name: Install mcp-publisher
        run: |
          curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher
      - name: Authenticate to MCP Registry
        run: ./mcp-publisher login github-oidc
      - name: Generate server.json
        run: |
          TAG="${GITHUB_REF#refs/tags/}"
          BASE_TAG="${TAG%-registry}"
          VERSION="${BASE_TAG#v}"
          go install github.com/daidaiJ/mcpb-tool-cli@latest
          mcpb serverjson \
            --dir mcpb-assets \
            --name io.github.<owner>/<binary> \
            --title "<Display Name>" \
            --description "<≤100 chars>" \
            --version "$VERSION" \
            --repo-url https://github.com/<owner>/<repo> \
            --base-tag "$BASE_TAG" \
            --expect-packages 6 \
            --out server.json
          cat server.json
      - name: Validate server.json
        run: ./mcp-publisher validate
      - name: Publish server to MCP Registry
        run: ./mcp-publisher publish
      - name: Verify registration
        run: |
          TAG="${GITHUB_REF#refs/tags/}"
          VERSION="${TAG%-registry}"
          VERSION="${VERSION#v}"
          curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=<binary>" \
            | jq -e --arg v "$VERSION" \
              '.servers[] | select(.server.name == "io.github.<owner>/<binary>" and .server.version == $v)' \
            > /dev/null
          echo "✅ registered: io.github.<owner>/<binary> $VERSION"
```

### 2. 发布与验证（agent 执行清单）

```bash
# 1. 提交推送改动
git push origin main
# 2. 打普通 tag 构建 release（含 .mcpb）
git tag -a v1.0.0 -m "release notes"
git push origin v1.0.0
gh run watch   # 等构建完成
# 3. 验证 release 产物有 .mcpb（旧 release 没有 .mcpb，publish 会失败）
gh release view v1.0.0 --json assets --jq '.assets[].name' | grep mcpb
# 4. 【推荐】本地 validate：用 mcpb serverjson 生成 server.json 后
#    mcp-publisher validate（验证器会 HEAD 检查每个 .mcpb URL，不实际发布）
#    Windows 直接用 <skill>/tools/mcp-publisher/mcp-publisher.exe
# 5. 确认无误后打 -registry tag 触发发布
git tag -a v1.0.0-registry -m "Publish v1.0.0 to MCP Registry"
git push origin v1.0.0-registry
gh run watch   # 等 publish-registry job 完成
# 6. 验证注册成功（响应结构：servers[].server）
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=<binary>"
```

**发布失败重试**：修复后需删除旧 tag 重打（tag 已存在时重新推送不触发 workflow）：

```bash
git tag -d v1.0.0-registry
git push origin :refs/tags/v1.0.0-registry
git tag -a v1.0.0-registry -m "Publish v1.0.0 to MCP Registry"
git push origin v1.0.0-registry
```

### 3. 本地手动发布（备用，CI 不可用时）

```bash
# Windows：直接用 <skill>/tools/mcp-publisher/mcp-publisher.exe
# 其他平台：从 GitHub releases 下载 mcp-publisher_<os>_<arch>.tar.gz（Go 二进制，非 npm 包）
mcp-publisher login github   # 设备码授权（浏览器访问 github.com/login/device）
mcp-publisher publish        # 当前目录找 server.json
```

## 关键要点（踩过的坑）

1. **mcpb 是 zip 不是裸二进制**：manifest.json + server/ 目录，`server.type: "binary"`，`command` 用 `${__dirname}/server/<bin>` 占位（运行时替换为 bundle 解压目录）
2. **旧 release 没有 .mcpb**：publish-registry 从 `BASE_TAG` release 下载 `.mcpb`，如果该 release 是旧 workflow 构建的（无 .mcpb），`gh release download` 会失败——必须先打新 tag 构建含 .mcpb 的 release
3. **OIDC 免密钥**：`mcp-publisher login github-oidc` + `permissions: id-token: write`，不需要任何 secrets
4. **name 格式硬约束**：`io.github.<owner>/<name>`，发布者必须拥有该 GitHub 仓库（所有权验证）
5. **checksum 循环跳过 .sha256**：`for f in <binary>-*` 会匹配到 .sha256 文件本身，不跳过会生成 `.sha256.sha256` 垃圾
6. **version 提取**：`v1.0.0-registry` → BASE_TAG=`v1.0.0` → VERSION=`1.0.0`（去 v 前缀），registry 版本号不带 v；mcpb manifest 的 version 同样不带 v
7. **mcp-publisher 是 Go 二进制**（GitHub releases 下载），不是 npm 包；命令：init/login/logout/publish/status/validate
8. **验证器会 HEAD 检查 URL**：identifier 必须真实可达（200 或 302+Location），占位符 URL 无法通过 `mcp-publisher validate`
9. **description ≤ 100 字符**：registry API 硬限制，超长返回 422（实测踩坑）；一句话覆盖核心功能 + 安全特性即可；`mcpb serverjson` 会在本地直接报错拦截
10. **文档双语约定**：英文为主（README.md/docs/*.md），中文保留为 `.zh-CN.md`，顶部互链 `> [中文版](...)` / `> [English](...)`；英文文档内交叉引用指向英文版（翻译 agent 容易把链接也翻成中文版，需检查）
11. **发布失败重试**：删旧 tag 重打（见上），同名 tag 重新推送不触发 workflow
12. **release notes 用 gh api 读 annotated tag message**：本地 checkout 的 lightweight tag 不可信（`%(contents)` fallback 到 commit message）；`gh release create` 前先 `delete --yes || true` 保证幂等重跑
13. **平台矩阵 6 平台**：windows/linux/darwin × amd64/arm64（含 windows-arm64、linux-arm64），`fail-fast: false` 避免单平台失败拖垮全部
14. **packages 条目无 platform 字段**：多平台 = 多个 packages 条目，平台信息在 mcpb manifest 的 `compatibility.platforms` 声明（schema 核对结论）
15. **下载 mcp-publisher 慢/超时**：GitHub release 资产 CDN 可能被墙，走代理（设置 `HTTPS_PROXY` 指向本地代理）或 `gh release download --repo modelcontextprotocol/registry`；Windows 直接用本 skill 自带二进制
16. **CI 内闭环验证**：publish-registry job 在 publish 前加 `mcp-publisher validate`（失败即停，不消耗发布配额），publish 后加 curl 自验证步骤（jq 断言 name+version 已注册，失败 job 标红）——agent 无需人工盯结果
17. **--expect-packages 防平台缺失**：serverjson 加 `--expect-packages 6`，某平台 .mcpb 缺失时本地直接报错，避免发布不完整版本
18. **mcpb pack 自带 zip 自检**：打包后验证 zip 可读 + manifest.json/server 条目齐全，损坏产物不进入 release

## 用户偏好速查（作者习惯，可自行取舍）

- **显式触发**：registry 发布必须打 `-registry` 后缀 tag，绝不自动随 release 发布
- **验证闭环**：发布前 `mcp-publisher validate`（可选）+ 发布后 curl 验证 + 检查 Actions job 成功
- **描述规范**：description 一句话覆盖核心功能 + 安全特性，title 用产品名
- **成本控制**：派发子 agent 时声明成本等级（quick/standard/deep）+ 预算，监控 jsonl 防跑偏
- **gh CLI 优先**：GitHub 操作（API/搜索/release）用 gh，不用网页
- **Go CLI 打包**：mcpb 打包与 server.json 生成用 `mcpb-tool-cli`（`go install github.com/daidaiJ/mcpb-tool-cli@latest`），不用 shell/jq 手写

## 参考

- 官方文档：registry.modelcontextprotocol.io（quickstart / package-types / github-actions）
- mcpb 规范：github.com/modelcontextprotocol/mcpb（MANIFEST.md、examples/calculator-rust）
- 验证器源码：registry 仓库 `internal/validators/registries/mcpb.go`
- 实战案例（均已成功发布）：
  - 2native-ssh-mcp v1.4.1（2026-08-29 首次发布，含 description 422 踩坑）
  - websearch-mcpserver v3.1.1（2026-08-29，CLI 打包 + 本地 validate 后一次成功）