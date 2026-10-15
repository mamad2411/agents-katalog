---
name: zlibrary
description: "Use when the user wants Z-Library/Zlibrary book workflows: search books, inspect metadata by id/hash, download a chosen book, check profile or remaining quota, compare candidate formats, or use the bundled Zlibrary.py API wrapper."
---

# Zlibrary

通过内置 `scripts/Zlibrary.py` 调用 Z-Library EAPI。优先用脚本完成稳定动作；更细的 API 能力先读对应 reference。

## 能力

| 能力 | 用户例子 | 入口 | 详细说明 |
| --- | --- | --- | --- |
| 搜索书籍 | "搜一下三体" "找英文版 deep learning" | `scripts/zlibrary_cli.py search` | `references/search.md` |
| 书籍信息 | "看这个 id/hash 的详情" | `scripts/zlibrary_cli.py info` | `references/book.md` |
| 下载书籍 | "下载第 2 本" | `scripts/zlibrary_cli.py download` | `references/download.md` |
| 账号与额度 | "还剩几次下载" "检查账号" | `scripts/zlibrary_cli.py quota/profile` | `references/account.md` |
| API 扩展 | "用 Zlibrary.py 的某个接口" | import `scripts/Zlibrary.py` | `references/api_reference.md` |

## 通用规则

1. 根据用户意图先读对应 `references/*.md`，不要只凭方法名猜参数。
2. 不要修改 `scripts/Zlibrary.py`。新增能力时在 `scripts/` 包一层，继续 import 基础库。
3. 不要在回复里展示密码、token、`remix_userkey` 等秘密。
4. 下载前先让用户从搜索结果里确认目标，除非用户已经给出明确的 `id` 和 `hash`。
5. 搜索结果默认用编号表格展示，方便用户后续说"下载第 2 本"。

## 鉴权

优先使用 token：

```bash
export ZLIBRARY_REMIX_USERID="..."
export ZLIBRARY_REMIX_USERKEY="..."
```

也支持邮箱密码：

```bash
export ZLIBRARY_EMAIL="..."
export ZLIBRARY_PASSWORD="..."
```

命令行参数 `--remix-userid/--remix-userkey` 或 `--email/--password` 会覆盖环境变量。
