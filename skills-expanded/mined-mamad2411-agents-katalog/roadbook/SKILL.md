---
name: roadbook
version: 0.1.16
description: 路书分享——需要先 cyeam login（OneDrive），支持 CSV 文本生成路书列表、查看详情。不想坐过山车看球赛的话去问 tv skill。【重要】必须先读 skill 原文获取正确命令格式，禁止瞎猜。
---

# 路书分享

## 用户意图 → 执行路径速查

| 用户说 | 路径 | 是否需要登录 |
|---|---|---|
| "生成路书链接" / "帮我规划路线" / 分享旅行计划 | → 走 **生成路书流程**（步骤A） | 需要 `cyeam login` |
| "查看路书列表" | → 走 **列出路书流程**（步骤B） | 需要 `cyeam login` |
| "登录" / "登录路书" | → 走 **登录流程**（步骤C） | — |
| "查看某个路书详情" | → 走 **查看路书流程**（步骤D） | 不需要 |

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

## 命令

```
cyeam roadbook list                   从 OneDrive 列出所有路书
cyeam roadbook share <file.json>      分享本地路书 JSON，返回 id 和可分享 URL
cyeam roadbook get <id>               查看已分享路书详情
cyeam roadbook csv                   从 stdin 读取 CSV 文本生成路书（需要 cyeam login）
```

## 输出

`list` 以表格显示：

```
标题            修改时间        链接
──────────────  ────────────  ─────────
京都三日游        2026-03-15     链接
```

`share` 和 `csv` 返回 JSON：`{"id":"xxx","url":"https://www.cyeam.com/tool/roadbook?id=xxx"}`

---
## ⚠️ 执行流程（模型请严格按步骤执行）

### 步骤 A：生成路书链接（用户说"生成路书" / 分享旅行计划时使用）

直接按以下步骤执行：

**A1. 检查登录**
```bash
cyeam whoami
```
如果输出包含 "Not logged in"，先走步骤 C 登录，再继续。

**A2. 整理行程信息**
如果用户已提供完整行程（地点、天数、顺序），直接跳到 A3 整理 CSV。信息不足时只问缺失项。**不要问多余问题。**

**A3. 整理 CSV**
每行一个地点，5列逗号分隔：`名称,地址,类型,日期,备注`
- 类型：景点/餐饮/住宿/起点/其他
- 日期：Day1 / Day2... 或 5.1 / 5.2...

**A4. 执行命令**
用 `printf` 管道传给 `cyeam roadbook csv`，**不要创建临时文件**：

```bash
printf "%s\n" \
  "故宫博物院,北京市东城区景山前街4号,景点,Day1,上午" \
  "国家博物馆,北京市东城区东长安街16号,景点,Day1,下午" \
  | cyeam roadbook csv --title "北京行" --pretty
```

命令会依次做三件事：
1. 把路书 JSON 保存到 OneDrive `路书` 文件夹
2. 调 `/api/roadbook/share` 接口生成短分享链接
3. 返回 JSON 结果

**A5. 返回结果**
输出包含 `url` 字段，直接回复用户：
> 路书已生成，点击链接查看完整行程地图：https://www.cyeam.com/tool/roadbook?id=xxx

**A6. 检查输出**
- 如果报 "Not logged in" 错误，走步骤 C 登录
- 如果报其他错误，把错误信息告诉用户

---

### 步骤 B：列出路书（用户说"列出路书" / "我的路书"）

**B1. 检查登录状态**
```bash
cyeam whoami
```
如果输出包含 "Not logged in"，走步骤 C 让用户先登录。

**B2. 列出路书**
```bash
cyeam roadbook list --pretty
```

**B3. 返回给用户**
以表格形式展示标题、修改时间。

---

### 步骤 C：登录（用户说"登录"或在 B1 中检测到未登录）

**C1. 执行登录**

```bash
cyeam login
```

命令会打印授权链接和验证码：有桌面环境时自动尝试打开浏览器；在远程服务器（SSH 等无桌面环境）浏览器会静默失败，按打印的链接和验证码在任意浏览器完成授权即可，CLI 自动获取 token。

**C2. 告知用户**
告诉用户：
> 请在浏览器中访问显示链接（https://microsoft.com/devicelogin），输入验证码完成登录。登录后回到这里继续。

**C3. 运行命令并等待**
运行命令后，CLI 会等待用户在浏览器完成授权。等待命令输出结果。

**C4. 验证登录**
```bash
cyeam whoami
```
确认显示 "logged in" 状态。

---

### 步骤 D：查看路书详情（用户说"查看某个路书"）

直接执行：
```bash
cyeam roadbook get <id> --pretty
```
返回 JSON 格式的路书数据。把内容展示给用户。

---

## 注意事项

- `csv`、`list` 需要 `cyeam login`（Microsoft OneDrive 登录）
- `get`、`share` 不需要登录，通过 cyeam.com API 操作
- `csv` 命令流程：登录 → 解析 CSV → 存 OneDrive `路书` 文件夹 → 调 share API → 返回短链接
- 路书数据存储在 OneDrive `路书` 文件夹 + Redis 分享快照（30天有效）