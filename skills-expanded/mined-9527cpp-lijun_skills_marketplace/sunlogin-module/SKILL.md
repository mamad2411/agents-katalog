---
name: sunlogin-module
description: >-
  在 desktop 仓库根目录执行 Sunlogin Linux 交叉模块构建：封装
  deps/slpackage/script/cmake_build.py，固定 -p linux，将 -t 同时映射为 -a/-t，
  自动用 git HEAD 的 8 位短 SHA 作为 -n（不可手动覆盖），可选推断 include/client_* 作为 -m，
  可选 -r 仅表示是否上传到 devres（URL 由 sl- 与模块名拼接）。在用户提到 sunlogin 交叉编译、
  cmake_build、OpenWrt 模块构建、sl-client 上传时使用。
---

# Sunlogin 模块交叉构建（sunlogin-module）

## 工作目录

必须在仓库根目录执行（含 `deps/slpackage/script/cmake_build.py` 与 `include/` 的 `desktop` 根）。

## 推荐入口（包装脚本）

```bash
python ~/.claude/skills/sunlogin-module/scripts/sunlogin_module_build.py -t <target> [-m <module>] [-c <cross_path>] [-r] [--no-cross-path]
```

包装脚本会：

- 固定调用 `python deps/slpackage/script/cmake_build.py -p linux -a <target> -t <target> ...`
- **始终**设置 `-n` 为 `git rev-parse --short=8 HEAD` 的前 8 位，**禁止**向 `cmake_build.py` 传入用户自定义的 `-n`
- **`-t` / `--target`（必填）**：交叉目标三元组名，同时作为 `-a` 与 `-t`

### `-m` / `--module`

- **必填条件**：在无法从 `include/` 唯一推断时必须显式给出
- **推断规则**：若 `include/` 下恰好只有一个 `client_*` 目录，则 `-m` 取该目录名；若有零个或多个，必须显式 `-m`

### `-c` / `--cross-path`

- 值为**工具链根目录**（不含 `-DCROSS_CHAIN_PATH=` 前缀），脚本会展开为 `cmake_build.py` 的 `-c "-DCROSS_CHAIN_PATH=<path>"`
- **未设置时**按顺序解析：
  1. 环境变量 `SUNLOGIN_CROSS_CHAIN_PATH`（全局）
  2. 环境变量 `SUNLOGIN_CROSS_CHAIN_<TARGET>`，其中 `TARGET` 为 `-t` 的大写且 `-` 改为 `_`（例如 `aarch64-openwrt-linux` → `SUNLOGIN_CROSS_CHAIN_AARCH64_OPENWRT_LINUX`）
  3. 脚本内置表（见 `scripts/sunlogin_module_build.py` 中 `DEFAULT_CROSS_BY_TARGET`），可按本机路径改该文件或改用 `-c`/环境变量
- **`--no-cross-path`**：不向 cmake 传 `CROSS_CHAIN_PATH`，依赖 PATH 中的 `${SL_TOOLCHAIN}-gcc`（与 `deps/slpackage/cmake/toolchain.cmake` 一致）。与 `-c` 互斥

### `-r` / `--upload`

- **仅开关**：出现即上传，**不再**由用户拼完整 URL
- 上传地址固定为：`http://devres.oray.net/oraylibs/sunlogin/sl-` + 将模块名中的 `_` 替换为 `-`（例如 `client_audio` → `http://devres.oray.net/oraylibs/sunlogin/sl-client-audio`）

## 与原始命令的对应关系

原始示例：

```text
python deps/slpackage/script/cmake_build.py -p linux -a aarch64-openwrt-linux \
  -c "-DCROSS_CHAIN_PATH=..." -t aarch64-openwrt-linux -m client_audio -n e3451fdf \
  -r http://devres.oray.net/oraylibs/sunlogin/sl-client-audio
```

使用本 skill 时等价思路：

- `-p linux`：由包装脚本固定
- `-a`、`-t`：均由 `-t`（target）提供
- `-c`：由 `-c`（路径）或按 target/环境变量推断
- `-m`：由 `-m` 或 `include/client_*` 推断
- `-n`：**仅自动**，等于当前提交 8 位短 SHA，用户/代理均不得改传
- `-r`：包装脚本中改为布尔；若需上传则用 `-r`，URL 按上面规则生成

## 代理执行清单

1. `cd` 到 `desktop` 仓库根目录
2. 确认 `-t` 已提供；确认 `-m` 已提供或可唯一推断
3. 运行包装脚本（或手工拼 `cmake_build.py` 时**必须**自带 `git rev-parse --short=8 HEAD` 作为 `-n`，且不得接受用户覆盖）
4. 需要上传时追加 `-r`（包装脚本），不要让用户传完整 URL

## 参考文档

- 仓库内：`kk_cross_build.md`、`.gitlab-ci.yml` 中同类命令
- CMake：`deps/slpackage/cmake/toolchain.cmake`
