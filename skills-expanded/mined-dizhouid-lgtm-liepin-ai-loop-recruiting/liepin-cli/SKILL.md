---
name: liepin-cli
description: >-
  猎聘 CLI(@viyzhu/liepin-cli)的安装位置、登录与故障参考。仅当需要登录猎聘、
  排查 CLI 环境问题、或查命令参数时使用;搜人/筛人的作业流程一律走 pxb-liepin skill。
---

# 猎聘 CLI (`liepin-cli`)

全局 npm 包 `@viyzhu/liepin-cli`,保持最新(版本下限由 `pxb-liepin` 的 `doctor.mjs` 把关;安装位置见 `npm root -g`,本工作区可选补丁 `patch-headless.mjs` 就打在它的 `dist/` 上)。

## 红线
本工作区**只通过 `pxb-liepin` 的 `scripts/*.mjs` 调用 CLI**,唯一允许手跑的命令是登录:
```bash
LIEPIN_HEADLESS=false liepin login    # PowerShell: $env:LIEPIN_HEADLESS='false'; liepin login
```
打开登录页让用户扫码;其余命令(search/resume/greet/...)一律不裸敲——发布版默认有头会弹窗,且 greet(打招呼)是流程禁区(沟通归 HR)。

## 查命令参数
```bash
liepin help              # 全部命令
liepin search --help     # 某命令的参数与码表(如 --user-status/--age)
```
不在此维护参数表——以 CLI 自带帮助为准,永不过时。

## 环境与故障
Node ≥ 20 + Chrome/Edge(常见安装路径自动检测,找不到设 `CHROME_PATH`)。
故障处置见仓库根 `README.md` 的「故障速查」表。
