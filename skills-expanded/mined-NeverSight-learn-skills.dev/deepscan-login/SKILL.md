---
name: deepscan-login
description: 处理 DeepScan 登录授权流程。支持扫描二维码登录或直接提供 API Key 登录。当用户需要登录、提供了 API Key、进入扫码本前需要授权、token 失效或首次使用时触发。
---

# DeepScan 登录授权

所有脚本路径相对于本 Skill 目录。

支持两种登录方式：**扫码登录** 和 **API Key 登录**。

## Step 1: 检查是否已登录

```bash
python scripts/auth.py get-token
```

- 返回 `{"token": "..."}` → 已登录，跳到 **Token 使用方式**。
- 退出码为 1 → 未登录，根据场景选择下方登录方式。

---

## 方式 A：API Key 登录

当用户直接提供了 API Key（如 `sk-xxxx` 或 `eyJxxx` 格式），直接保存即可：

```bash
python scripts/auth.py save-token {api_key}
```

告知用户：API Key 已保存，登录成功，可以开始使用扫码本功能。

---

## 方式 B：扫码登录

当用户发起登录但未提供 API Key 时，走扫码流程。

### Step 2: 发起授权

```bash
python scripts/auth.py initiate
```

返回示例：

```json
{
  "token": "qIksuKLU",
  "auth_url": "https://qr67.cn/auth/qIksuKLU",
  "qrcode_path": "/tmp/deepscan_qr_qIksuKLU.png",
  "expires_in": 300
}
```

记录返回的 `token`，后续轮询需要使用。

### Step 3: 展示二维码并提示 API Key 选项

同时通过以下两种方式提供二维码，确保用户能在任意环境中扫码：

**方式一：图片（部分 Agent 支持）**

使用 Read 工具读取 `qrcode_path` 指向的 PNG 图片，直接展示给用户。

**方式二：浏览器链接（通用）**

将 `auth_url` 拼接到草料二维码生成链接的 `text` 参数：

```
https://mh.cli.im/?text={auth_url}
```

例如 `auth_url` 为 `https://qr67.cn/auth/qIksuKLU`，则链接为：

```
https://mh.cli.im/?text=https://qr67.cn/auth/qIksuKLU
```

告知用户：

> 请扫描上方二维码，或 [点击此链接](https://mh.cli.im/?text={auth_url}) 在浏览器中打开二维码后扫描，使用「草料扫码器」微信小程序完成登录授权，二维码有效期 5 分钟。
>
> 也可以直接提供 API Key 完成登录（跳过扫码）。

### Step 4: 等待用户扫码

如果用户在等待期间提供了 API Key，直接跳转到**方式 A** 保存即可，无需继续轮询。

每隔 5 秒执行一次，最多 60 次（共 300 秒）：

```bash
python scripts/auth.py poll {token}
```

- 返回 `{"success": false}` → 用户尚未扫码，继续等待。
- 返回 `{"success": true, "api_key": "eyJ..."}` → 授权成功，记录 `api_key`，进入 Step 5。
- 60 次后仍未成功 → 告知用户二维码已过期，可重新发起登录。

轮询期间使用 `sleep 5` 等待，不要向用户输出每次轮询结果。

### Step 5: 保存登录凭证

将轮询返回的 `api_key` 保存（注意：保存的是 `api_key`，不是 Step 2 的短 token）：

```bash
python scripts/auth.py save-token {api_key}
```

告知用户登录成功，可以开始使用扫码本功能。

## Token 使用方式

后续所有接口调用时携带 Header：

```
Authorization: Bearer {token}
```

API 基础地址：`https://data.cli.im/x-deepscan`

## 错误处理

- **网络错误**：提示用户检查网络，可重试。
- **二维码过期**：重新执行 Step 2。
- **Token 失效**（接口返回 401）：删除本地 token 后重新登录。

```bash
python -c "import os; p=os.path.expanduser('~/.deepscan/token'); os.remove(p) if os.path.exists(p) else None"
```
