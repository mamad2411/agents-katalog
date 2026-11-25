---
name: release
description: >-
  发布 FluxDown 新版本或查看已有版本时使用。校验版本 tag（稳定版 vX.Y.Z / 预览版
  vX.Y.Z-rc.N）在推送前合法可用，并按渠道/组件快速列出已有版本。关键词：发布, 发版,
  release, publish, 版本, version, tag, 打标签, 稳定版, 预览版, stable, frontier, rc,
  预发布, prerelease, 查看版本, 已有版本, 最新版本, 更新渠道, changelog, git-cliff
---

# FluxDown 发布与版本查看

FluxDown 用 **SemVer 预发布后缀**区分双渠道：**稳定版 `vX.Y.Z`**、**预览版 `vX.Y.Z-rc.N`**。
推送 `v*` tag 会**立即触发 GitHub Actions 全平台发布流水线（不可逆）**，本次全部组件发布到**同一个**
`vX.Y.Z` release。本 skill 覆盖三件事：**发布前校验版本可用** + **快速查看已有版本** + **失败组件补发**。

> 红线（`.omp/RULES.md`）：**未经用户明确要求，禁止 `git commit` / `push` / tag**。
> 用户要求发版（「发版」「发布 vX.Y.Z」等）即授权本次发布全程：跑 CI + 演练 → 全绿后**直接打 tag 并推送，不再回头确认** → 盯到 release 转正。

## 1. 快速查看已有版本

```bash
# 客户端主线（稳定+预览）最新在前
git tag -l 'v[0-9]*' --sort=-v:refname | head
# 仅稳定版（排除 -rc 预发布）
git tag -l 'v[0-9]*' --sort=-v:refname | grep -v -- '-rc' | head
# 仅预览版（预发布 -rc）
git tag -l 'v[0-9]*-rc*' --sort=-v:refname | head
# 某个 release 已完整发布的组件（统一 release 以 SHA256SUMS-<组件>.txt 哨兵为准）
gh release view "$V" --json assets -q '.assets[].name' | grep '^SHA256SUMS-'
# 历史组件线（拆分时代，已不再新建）最新稳定一个
for p in server-v cli-v mobile-v extension-v; do \
  echo "$p -> $(git tag -l "${p}[0-9]*" --sort=-v:refname | grep -v -- '-rc' | head -1)"; done
# 已发布 release（含 prerelease 标记，需 gh 已登录该私有仓库）
gh release list --limit 20
```

`--sort=-v:refname` 对纯三段式排序精确；混入 `-rc` 时排名近似，需精确按时间用 `--sort=-creatordate`。

## 2. Tag 约定（发布契约）

| 渠道 | tag | 打自分支 | GitHub prerelease | make_latest | 打包范围 |
|---|---|---|---|---|---|
| 稳定版 | `vX.Y.Z` | `stable` | false | true | 客户端 / web / 移动（Android + iOS 侧载 IPA）/ NAS / 扩展 全部 |
| 预览版 | `vX.Y.Z-rc.N` | `main` | true | false | 客户端 / web / 移动（Android + iOS 侧载 IPA）/ NAS，**不含浏览器扩展** |

- 同一次 `v*` push 按目录 diff 决定本次打包哪些组件（app / server / cli / mobile / ios / extension），产物全部上传到这一个 `vX.Y.Z` release；未改动的组件不重建，官网自动沿用它上一个完整版本。历史上的 `server-v*` / `cli-v*` / `mobile-v*` / `extension-v*` 组件 release 不再新建，官网仍兼容读取。
- **扩展发布后无法改版本号**，故 `-rc` tag 跳过 `build-extension`（`changes` 判定 extension=false）。
- latest：`publish-release` 只在「稳定版 + 桌面端完整 + 最高稳定版本」时标记；Rust `FLUXDOWN_APP_VERSION` 与原生 Android `versionName` 保留完整 tag 版本。
- **分支模型**：`main` = 开发分支（超集 / 最新），`stable` = 稳定分支（子集）；`stable` 只经合并/cherry-pick `main` 前进。稳定发布前 `git log stable --not main` 必须为空。
- **CI 分支守卫**（`changes` job 首步）：tag 提交必须在对应分支上——`vX.Y.Z` ∈ `origin/stable`、`vX.Y.Z-rc.N` ∈ `origin/main`，否则整条流水线立即失败（`git merge-base --is-ancestor` 判定）。

## 3. 发布前校验（保证版本可用）

```bash
V=v0.3.0            # 稳定版；预览版示例：V=v0.3.0-rc.1
# 1) 格式合法：稳定 ^v[0-9]+\.[0-9]+\.[0-9]+$ ；预览 ^v[0-9]+\.[0-9]+\.[0-9]+-rc\.[0-9]+$
printf '%s\n' "$V" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+(-rc\.[0-9]+)?$' && echo OK || echo "格式非法"
# 2) tag 不重复
git rev-parse -q --verify "refs/tags/$V" >/dev/null && echo "已存在，换号" || echo "可用"
# 3) 单调递增：新版须高于最新同类（对照下面输出）
git tag -l 'v[0-9]*' --sort=-v:refname | head -3
# 4) 工作树干净、停在目标分支的目标提交（稳定=stable，预览=main）
git status --porcelain    # 须为空
git branch --show-current && git log -1 --oneline
# 4b) 稳定发布额外：stable 不得含 main 没有的提交
git log stable --not main --oneline    # 须为空
# 5) 可选：本地预览 release notes（需装 git-cliff；未装则跳过，CI 仍会生成，无规范 commit 时用默认标题）
command -v git-cliff >/dev/null && git cliff --latest --strip header | head -40
```

版本"可用"的硬条件：格式合法 · tag 不重复 · 高于同渠道最新 · 停在正确分支且工作树干净 · 稳定版 `stable --not main` 为空 · **目标提交 CI 全绿**（tag 推送的 `changes` 会再卡一次：CI 红即在建草稿前失败，仍在跑则等待）。
预览版额外确认：后缀是 `-rc.N` 且 N 递增（预览用户按 SemVer 收 `rc.1 < rc.2 < … < 转正 X.Y.Z`）。

## 4. 发布（不可逆，用户要求发版后全自动）

**只构建一次**：先在目标提交上跑全量 CI + 演练（演练就是正式构建：签名、公证、Docker digest 全做，只是不发布），两者都绿再推 tag；tag 推送复用演练产物（`changes` 自动查找同提交同 tag 的演练），推 tag 后约 5–10 分钟完成上传 / 镜像打 tag / 转正。稳定版与预览版同一流程（预览版 `--ref main`）。

**自动放行**：`.omp/hooks/pre/guard.ts` 推送前按 tag 指向的提交查 GitHub Actions——最近一次 `ci.yml` 与最近一次「Release 演练 `$V`（不发布）」都 `completed + success` 即直接放行，不弹确认；任一不满足（缺演练、仍在跑、失败、本地无 tag）、`--tags` / `--follow-tags` / 变量 refspec 时才回退为弹确认（无 UI 拒绝）。所以推送命令**必须写字面 tag 名**（`git push origin v0.6.4`，不能 `"$V"`）。

```bash
# 0) 第 3 节校验全部通过
git checkout stable      # 预览版改为 main（CI 守卫会拒绝打错分支的 tag）
SHA=$(git rev-parse HEAD)
# 1) 全量 CI + 演练并行触发（无副作用）
gh workflow run ci.yml --ref stable
gh workflow run release.yml --ref stable -f rehearsal=true -f tag="$V" -f component=changed
sleep 10
CI=$(gh run list --workflow ci.yml --commit "$SHA" --event workflow_dispatch --limit 1 --json databaseId -q '.[0].databaseId')
RH=$(gh run list --workflow release.yml --commit "$SHA" --event workflow_dispatch --limit 1 --json databaseId,displayTitle -q ".[] | select(.displayTitle == \"Release 演练 $V（不发布）\") | .databaseId")
# 2) 等两者结束（演练动辄 30–60 分钟：bash 用 timeout: 0 / 后台任务等，不要轮询）
gh run watch "$CI" --exit-status; gh run watch "$RH" --exit-status
# 3) 都 success → 直接发布，不问用户（字面 tag 名，guard 据此校验后放行）
git tag -a v0.6.4 -m v0.6.4
git push origin v0.6.4
# 4) 盯 tag 触发的 Release 运行直到结束，并确认已转正
gh run watch "$(gh run list --workflow release.yml --branch v0.6.4 --event push --limit 1 --json databaseId -q '.[0].databaseId')" --exit-status
gh release view v0.6.4 --json isDraft,isPrerelease,url
```

- **演练 / CI 失败 → 不打 tag**。偶发失败（网络、签名时间戳、ASC 5xx 等，`release-auto-rerun` 已自动重跑过一次仍红）→ `gh run rerun <id> --failed` 后回到第 2 步继续等；确定性失败（编译 / 测试 / 打包脚本错误）→ 停下，向用户报告失败 job 与日志要点，修复属于新的代码改动。
- 演练与 tag 之间分支又前进了 → tag 提交 ≠ 演练提交，guard 不会放行，须在新提交上重跑 CI + 演练。
- 推 tag 后运行失败：按 4b 处理；结束时向用户汇报 release 链接、是否转正、各组件哨兵（第 1 节命令）。

## 4b. 组件打包失败 → 补发（不重跑其余组件）

某组件失败时其余组件照常上传，但 **release 保持草稿**（不触发 `published` webhook / Telegram 公告，官网与客户端仍提供上一版本）；`publish-release` 以失败结束并在 job summary 列出缺失组件与补发命令。tag 与历次补发的应发布组件累计记在说明头部 `<!-- fluxdown:release:begin … expected=… docker=… -->`，全部有完成哨兵（含 Server Docker）后由补齐的那次运行转正。

```bash
# 偶发失败（源码无需改动）：在该运行页点 “Re-run failed jobs”，或
gh run rerun <run-id> --failed
# 需改代码/打包脚本：修复先合入发布分支（稳定版 = stable，预览版 = main），再补发该组件
gh workflow run release.yml --ref main -f tag="$V" -f component=mobile            # 源码 = tag 本身
gh workflow run release.yml --ref main -f tag="$V" -f component=mobile -f source_ref=stable   # 源码含修复
```

- `component`：`app` / `extension` / `server` / `cli` / `mobile` / `ios`，或 `changed`（按该 tag 的变更检测补发全部应发组件）。
- `source_ref` 必须包含该 tag 且在发布分支上；版本号、预发布标记恒取 tag。产物以 `--clobber` 覆盖同名资产，旧清单里不再产出的资产会被删除。
- 补发属于 CI 触发，等同发布动作：本次发版过程中的「Re-run failed jobs」/ 同 tag 补发属已授权范围；发版完成后的补发、或需要改代码的补发，仅在用户明确要求时执行。

## 5. 各渠道发布后可见性（自检预期）

- **官网下载 / `/releases/latest`**：永远只给稳定版（`/api/release` 缺省 = stable；下载页从不带 channel）。
- **预览版**：仅 `/api/release?channel=frontier` 与客户端"更新渠道 = 预览版"可见；预览资产经 `/api/download/<name>?tag=<rc-tag>` 下载。
- **客户端更新判定**：桌面/headless 由 `native/agent/src/update/` 承担，使用 protocol 更新状态；原生移动端见 `mobile/Android` 与 `mobile/FluxDown`。Android 正式包用 `ANDROID_NATIVE_*` 签名，不能覆盖旧 Flutter APK，发布说明必须保留换签名安装提示。

细节见根 `AGENTS.md`「git · 分支 · 发布」、`.omp/knowledge/ops.md`「发布与 CI」与 `.github/workflows/release.yml`。
