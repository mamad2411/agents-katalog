---
name: kk-build
description: Use when building or packaging the SunloginClient KongKong (控控) embedded system using kk_build.sh
triggers:
  - kk_build
  - kk build
  - 控控编译
  - 向日葵交叉编译
  - build kk
tags:
  - build
  - cross-compile
  - embedded
  - sunlogin
  - kk
  - arm
context: |
  ## 项目背景

  kk_build.sh 是向日葵客户端的本地交叉编译构建脚本，主要用于：
  1. 编译控控(KongKong)嵌入式的插件、主程序、kk接口
  2. 编译第三方依赖库(fftw/zlib/protobuf/openssl/lua/eudev/uci等)
  3. 打包编译产物
  4. 上传到 devres.oray.net 服务器

  ## 关键文件位置

  - 构建脚本: `scripts/kk_build.sh` (skill目录，相对于 skill 根目录)
  - skill 根目录: `{plugin_root}/skills/kk-build/`
  - 模块源码: `modules/client/{module}/` (项目根目录下)
  - modules.json: `modules.json` (项目根目录)
  - kk接口源码: `kk_sunlogin_upgrade/` (项目根目录)
  - toolchain.cmake: `toolchain.cmake` (项目根目录)

  ## 重要：项目根目录

  **默认使用 Claude 的工作目录 `(pwd)` 作为项目根目录**，而不是脚本所在位置。
  可通过 `--project_root <path>` 参数手动指定。

  ## 编译产物输出路径

  - 主程序: `build/sunloginclient`, `build/sunloginclient_desktop`
  - 模块插件: `modules/client/{module}/build/sl-client-{module}.so`
  - kk接口库: `kk_sunlogin_upgrade/_install/lib/`
  - 第三方库打包: `{module}-{version}-linux-{target}-{build_version}.zip`

commands:
  info: |
    ## kk_build.sh 参数说明

    | 参数 | 说明 | 必填 |
    |------|------|------|
    | `--cross_chain <path>` | 交叉编译工具链路径 (如 /path/to/toolchain) | 是 |
    | `--target <target>` | 目标平台 (如 arm-openwrt-linux, aarch64-openwrt-linux, arm-rockchip830-linux-uclibcgnueabihf) | 是 |
    | `--modules <modules>` | 指定要编译的模块列表，空格分隔 | 否 |
    | `--main` | 仅编译主程序 | 否 |
    | `--3rd [libs]` | 仅编译第三方依赖库，可指定库名(逗号分隔) | 否 |
| `--sl_other` | 仅编译不在本地编译的第三方依赖库(如sl-control等) | 否 |
| `--debug` | 启用Debug模式编译，默认Release | 否 |
    | `--pack` | 仅执行打包操作，不编译 | 否 |
    | `--quiet` | 静默模式，编译输出重定向到/dev/null | 否 |
    | `--no_upload` | 不上传编译结果，默认上传 | 否 |
    | `--project_root <path>` | 项目根目录，默认: 当前目录 | 否 |
    | `--module_path <name> <path>` | 指定模块的自定义源码路径 | 否 |
    | `--help` | 显示帮助信息 | 否 |

  usage: |
    ## 使用示例

    脚本路径: `scripts/kk_build.sh` (相对于 skill 根目录)

    ```bash
    # 完整编译(模块+主程序)并打包上传
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux

    # Debug模式编译
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --debug

    # 指定模块自定义路径编译
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux \
        --module_path desktop /path/to/desktop/source

    # 仅编译指定模块(如usbip)
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --modules usbip

    # 仅编译主程序
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --main

    # 仅编译第三方依赖库
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --3rd

    # 仅编译指定第三方库(逗号分隔)
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --3rd openssl,zlib

    # 仅编译不在本地编译的第三方依赖库(如sl-control等)
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --sl_other

    # 仅打包(不编译，需先编译)
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --pack

    # 静默模式编译
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --quiet

    # 不上传编译结果
    scripts/kk_build.sh --cross_chain /path/to/toolchain --target arm-openwrt-linux --no_upload
    ```

  modules: |
    ## 支持的模块(插件)列表

    默认模块: `desktop audio usbip ssh camera file kk`

    | 模块名 | 说明 |
    |--------|------|
    | desktop | 桌面控制模块 |
    | audio | 音频控制模块 |
    | usbip | USB远程模块 |
    | ssh | SSH远程模块 |
    | camera | 摄像头模块 |
    | file | 文件传输模块 |
    | kk | 控控特殊接口模块 |

  third_party: |
    ## 第三方依赖库

    脚本自动编译以下第三方库:

    | 库名 | 版本 | 说明 |
    |------|------|------|
    | fftw | 3.3.10 | FFT库 |
    | zlib | 1.2.3 | 压缩库 |
    | protobuf | 3.15.8 | Google协议缓冲区 |
    | openssl | 1.1.1q | OpenSSL加密库 |
    | lua | 5.3.2 | Lua脚本引擎 |
    | eudev | 3.2.9 | 设备管理 |
    | uci | 1.0.0 | OpenWrt UCI库 |
    | replxx | 0.0.4 | 命令行增强库 |

  targets: |
    ## 支持的目标平台

    - `arm-openwrt-linux` - ARM OpenWrt
    - `aarch64-openwrt-linux` - ARM64 OpenWrt
    - `arm-rockchip830-linux-uclibcgnueabihf` - RK芯片ARM

  troubleshooting: |
    ## 常见问题

    1. **cross_chain和target参数必须设置**
       ```
       [ERROR]: cross_chain和target参数必须设置
       ```
       确保同时指定 `--cross_chain` 和 `--target`

    2. **模块路径不存在**
       ```
       [WARN]: 模块路径不存在: ../xxx, 将跳过此模块的编译
       ```
       模块源码需放在与主工程同级的 `modules/client/` 目录，或使用 `--module_path` 指定

    3. **kk_sunlogin_upgrade目录不存在**
       ```
       [ERROR]: kk_sunlogin_upgrade目录不存在！
       ```
       编译kk接口前确保项目根目录下有kk_sunlogin_upgrade源码目录

    4. **第三方库编译需提前安装依赖**
       - json-c开发库 (编译uci时需要)
       - gcc, make, cmake, git, wget等基础工具
       - 可通过 `sudo apt-get install -y libjson-c-dev build-essential cmake git wget` 安装

    5. **上传失败检查**
       - 确认 devres.oray.net 网络可达
       - 检查文件是否已生成
       - 可使用 `--no_upload` 跳过上传