# AGENTS.md

本文件是 `dsh-desktop` 仓库的开发约定。回复与文档使用简体中文；代码、命令和技术术语保留原文。

## 仓库定位

这是一个 Windows x64 的 Tauri 2 桌面壳：`ui/` 提供静态 WebView 界面，`src-tauri/` 负责 Rust 壳、运行时生命周期、更新、托盘、通知、远程访问和子进程管理，`scripts/` 负责桌面插件、运行时组装、构建和测试。

## Git 硬性限制

- 禁止执行 `git commit`、`git push`、tag 创建或推送、Release 发布。
- 禁止使用 `git worktree`。
- 保留用户已有的未提交改动；修改完成后只报告变更和验证结果，由用户自行提交或发布。
- 不要把凭据、用户配置、缓存、解压运行时、临时日志或本地构建产物加入版本库。

## 目录与所有权

- `ui/`：静态页面与样式；改动后至少运行 `npm run test:ui`。
- `src-tauri/src/`：Rust/Tauri 壳。`lib.rs` 统一处理路径、首启解压、dsh 子进程、插件部署、更新回滚、relay-client 和命令；`migration.rs`、`conversation_portable.rs` 为独立领域模块。
- `scripts/<plugin>/src/`：客户端源码；`lib/`：宿主模块；`index.js`：宿主接线；`build.mjs`：构建入口。维护插件包括 `bridge`、`session-manager`、`change-history`、`file-upload`、`conversation-navigator`、`web-search`。
- `scripts/vision-any/`：`dsh-vision-any` 的桌面本地叠加层；`scripts/relay-client/`：远程访问伴生进程，不是 Cordis 插件；`scripts/relay/`：relay 协议与测试。
- `runtime/`：本地运行时和生成物。`runtime-archive.tar.gz` 只包含 Node/dsh core；`plugins-src/` 是插件规范副本；`relay-client/` 是伴生进程部署副本；`version.json` 记录版本。
- `docs/`：构建与发布文档；`scripts/test-fixtures/`：测试夹具。

不要直接编辑 `scripts/*/client.js` 或 `runtime/plugins-src/` 生成内容；修改源码后运行 `npm run build:plugins`。`src-tauri/target*`、`node_modules/`、`.npm-cache/`、WebView2 数据目录是缓存，不是源码。

## 常用命令

```powershell
npm install --cache .npm-cache
npm run dev
npm run check
npm run build
npm run build:plugins
npm run test:ui
npm run test:plugins
npm run test:conversation-portable
cargo test --manifest-path src-tauri/Cargo.toml
```

运行时与发布：

```powershell
node scripts/fetch-runtime.mjs 0.1.1-rc.2
npm run bundle-runtime
npm run verify:release -- --tag=v0.2.2
npm run release:build
npm run release-dev
npm run release-dev:fast
```

`release:build` 默认使用经过补丁兼容性审核的 `DSH_DESKTOP_RELEASE_DSH_VERSION`（当前默认 `0.1.1-rc.2`）；审核全部 upstream bundle 后才可使用 `latest`。正式发布前运行 `npm run verify:release -- --tag=v<version> --online --runtime`、`npm run test:plugins`、`npm run bundle-runtime`、Rust tests 和 `npm run check`，并确认 `package.json`、`package-lock.json`、`src-tauri/Cargo.toml`、`Cargo.lock`、`tauri.conf.json` 版本一致。不要在本地发布 GitHub Release。

## 运行时与插件契约

安装包从 Tauri resources 读取 core 归档、`plugins-src/`、`relay-client/`、`version.json` 和 `conversation-portable.mjs`。首次启动将 core 解压到安装目录 `runtime/`；不可写时回退到 `%LOCALAPPDATA%\\com.anixuil.dshdesktop\\runtime\\`。插件从 `plugins-src/` 部署到 DSH profile，dsh 更新后恢复，健康检查失败自动回滚；用户已安装的同名第三方 bundle 应复用且不覆盖。

新增或调整桌面插件时，同时检查插件源码、`scripts/bridge.patch.yml`、`scripts/fetch-runtime.mjs` 的 `desktopPlugins`、`src-tauri/src/lib.rs` 的 `DESKTOP_PLUGINS` 和对应 smoke test。第三方 bundle（`dsh-vision-any`、`dshmarket`）走 `plugins-src/` 与 profile `bundles`，不加入桌面插件 patch 清单。

## 风格与测试

JavaScript 使用 ES modules、两空格缩进、`camelCase`；Rust 使用 `rustfmt` 和 `snake_case`。测试脚本命名为 `scripts/test-*.mjs`。客户端渲染变化需同步 fixture，先构建插件再测试；Rust、运行时、更新回滚、插件部署或 relay 变化需运行对应 Rust/宿主测试。静态检查、bundle smoke 和启动成功不等于真实桌面交互已验证；UI/native 行为需在实际 Tauri 或浏览器路径验证并说明边界。

## 本地调试变量

- `DSH_DESKTOP_CONFIG_DIR`：配置、日志和 patch 数据目录
- `DSH_DESKTOP_WEBVIEW_DATA_DIR`：WebView2 数据目录
- `DSH_DESKTOP_DSH_HOME`：传给 dsh 的 `DSH_HOME`
- `DSH_DESKTOP_DSH_PORT`：dsh Web 端口，默认 `3080`
- `DSH_DESKTOP_DEBUG_LOG`：启用壳调试日志
- `DSH_DESKTOP_RUNTIME_INSTALL_TIMEOUT_MS`：运行时 npm 安装超时；`0` 表示禁用
- `DSH_DESKTOP_VISION_TARBALL`：离线指定 `dsh-vision-any` tarball
- `DSH_DESKTOP_RELEASE_DSH_VERSION`：release 构建使用的 dsh 版本
- `DSH_RUNTIME_VERSION`：release runtime 期望版本
- `VOLC_ACCESS_KEY`、`VOLC_SECRET_KEY`、`VOLC_REGION`：余额/用量查询凭据与地域；不得写入仓库

受限 Windows 环境若 cargo 无法访问 crates.io，使用 `node scripts/cargo-mirror.mjs` 并按 `docs/BUILDING.md` 设置 `CARGO_HOME`、`TEMP/TMP`、`LOCALAPPDATA` 和 `DSH_DESKTOP_WEBVIEW_DATA_DIR`。GUI release 进程用 `Start-Process -PassThru` 配合 `Wait-Process` 管理。

## 变更报告

完成后说明修改文件、用户可见影响、实际运行的验证命令及未覆盖的真实运行时/交互证据。发布版本还需说明安装器、updater artifact、`.sig` 和 `latest.json` 是否已由用户在授权环境中生成。
