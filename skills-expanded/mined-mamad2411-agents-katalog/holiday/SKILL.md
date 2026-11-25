---
name: holiday
version: 0.1.16
description: 假期查询——查某一天是上班还是放假、调休安排、节假日名称。想知道是不是工作日、什么时候放假补班的时候用。【重要】必须先读 skill 原文获取正确命令格式，禁止瞎猜。
---

# 假期查询

## 概述

查任意日期的节假日信息：是否放假、节日名称、调休补班、薪资倍数等。数据来自 timor.tech 公共 API。

```bash
cyeam date holiday                  # 今天
cyeam date holiday 2026-10-01       # 指定日期
cyeam date holiday next-monday       # 不支持，只接受 YYYY-MM-DD
```

## 安装

```bash
# macOS Apple Silicon
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Darwin_arm64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/

# macOS Intel
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Darwin_x86_64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/

# Linux amd64
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Linux_x86_64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/
```

检查安装：`which cyeam && cyeam version`

## 输出

```
日期: 2026-10-01
星期: 周四
状态: 休息日
名称: 国庆节
薪资倍数: 3
```

## 状态说明

| 状态 | 含义 |
|------|------|
| 工作日 | 普通上班日 |
| 休息日 | 法定假日或周末 |
| 周末休息 | 周末 |
| 调休补班 | 调休安排的上班日（如国庆前的周末） |

## 注意事项

- 日期格式必须为 `YYYY-MM-DD`，省略参数默认为今天
- 不需要登录
- 数据档期：当前仅支持已公布的年度节假日安排，未公布的年份会返回空