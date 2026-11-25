---
name: sunlogin-service
description: >-
  在 sunloginclient 仓库根目录执行 Sunlogin Linux 服务端交叉构建：封装
  auto_compile.py，固定 -p linux，将 -t 同时映射为 -a/-T，可选推断
  CROSS_CHAIN_PATH 作为 -c，可选 -r 上传到 devres（URL 由 embed 路径与
  git branch/short SHA 拼接）。在用户提到 sunlogin 服务端构建、
  auto_compile.py、OpenWrt 服务端编译、sunloginservice 上传时使用。
---

# Sunlogin 服务端交叉构建（sunlogin-service）

## 工作目录

必须在仓库根目录执行（含 `auto_compile.py` 的 `sunloginclient` 根）。

## 推荐入口（包装脚本）

```bash
python ~/.claude/skills/sunlogin-service/scripts/sunlogin_service_build.py -t <target> [-c <cross_path>] [-r] [-d]
```

包装脚本会：

- 固定调用 `python auto_compile.py -p linux -a <target> -t cli -c "-DCROSS_CHAIN_PATH=<cross_path>" -T <target>`
- **`-t` / `--target`（必填）**：交叉目标三元组名，同时作为 `-a` 与 `-T` 的值，`-t`（apptype）固定为 `cli`

### `-c` / `--cross-path`

- 值为**工具链根目录**（不含 `-DCROSS_CHAIN_PATH=` 前缀），脚本会展开为 `auto_compile.py` 的 `-c "-DCROSS_CHAIN_PATH=<path>,-DCMAKE_VERBOSE_MAKEFILE=ON"`
- **未设置时**按顺序解析：
  1. 环境变量 `SUNLOGIN_CROSS_CHAIN_PATH`（全局）
  2. 环境变量 `SUNLOGIN_CROSS_CHAIN_<TARGET>`，其中 `TARGET` 为 `-t` 的大写且 `-` 改为 `_`（例如 `aarch64-openwrt-linux` → `SUNLOGIN_CROSS_CHAIN_AARCH64_OPENWRT_LINUX`）
  3. 脚本内置表（见 `scripts/sunlogin_service_build.py` 中 `DEFAULT_CROSS_BY_TARGET`），可按本机路径改该文件或改用 `-c`/环境变量

### `-r` / `--upload`

- **仅开关**：出现即上传，**不再**由用户拼完整 URL
- 上传地址固定为：`http://devres.oray.net/release/sunlogin/embed/` + `<git_branch>/<git_short_8_sha>`
  - 例如：`http://devres.oray.net/release/sunlogin/embed/feature_lijun_frame_info/a16f78ea`

### `-d` / `--debug`

- 构建 Debug 版本（默认 Release）

## 与原始命令的对应关系

原始示例：

```text
python auto_compile.py -p linux -a aarch64-openwrt-linux -t cli \
  -c "-DCROSS_CHAIN_PATH=/home/lijun/workspace/sunlogin-orayos/staging_dir/toolchain-aarch64_cortex-a53_gcc-12.3.0_glibc,-DCMAKE_VERBOSE_MAKEFILE=ON" \
  -T aarch64-openwrt-linux
```

使用本 skill 时等价思路：

- `-p linux`：由包装脚本固定
- `-a`：由 `-t`（target）提供
- `-t`（apptype）：固定为 `cli`
- `-c`：由 `-c`（路径）或按 target/环境变量推断，自动追加 `-DCMAKE_VERBOSE_MAKEFILE=ON`
- `-T`：由 `-t`（target）提供
- `-r`：包装脚本中改为布尔；若需上传则用 `-r`，URL 按上面规则生成

## 代理执行清单

1. `cd` 到 `sunloginclient` 仓库根目录
2. 确认 `-t` 已提供
3. 运行包装脚本（或手工拼 `auto_compile.py` 时**必须**附带 `-T`、`-t cli`、`-p linux`）
4. 需要上传时追加 `-r`（包装脚本），不要让用户传完整 URL

## 参考文档

- 仓库内：`auto_compile.py`、`.gitlab-ci.yml` 中同类命令
- CMake：`toolchain.cmake`