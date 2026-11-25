---
name: yunzhi-cloudphone-checkin
description: 云智手机 (yunzhi.play.cn / 爱游戏天翼云机) 每日登录福利与云机空间权益 (benefit 158) 自动化签到与卡片领取 Skill。专为好友分享与团队落地设计，内置纯前端控制台一键脚本、Chrome CDP 无感自动化、Direct HTTP 命令行多驱动，完美解决边缘 WAF 503 与 TLS 指纹拦截。Triggers: 云智手机签到, yunzhi 签到, 云机空间福利, 天翼云手机打卡, play.cn 签到, 云智每日福利, new-gm.cn 签到.
---

# 云智手机 (yunzhi.play.cn) 自动化签到与云机空间领取

本 Skill 完整封装了电信爱游戏 / 天翼云智手机（`https://yunzhi.play.cn/ai/?channel_code=00000042`）每日签到与权益领取的全部反编译逆向成果。

**核心权益**：每日自动领取「今日登录福利」弹窗发放的 **2 天云机空间服务卡（benefitConfigId: 158）**，并自动下发绑定至当前正在运行中的云机设备，实现云手机空间长期免维护自动续期。

---

## 目录与自包含文件

本 Skill 经过深度解耦与脱敏，完全**自包含（Self-Contained）**，可整体打包分享给好友或部署于独立服务器：

```
~/.agents/skills/yunzhi-cloudphone-checkin/
├── SKILL.md                          # 本文档：分享指南、凭据获取、快速上手与架构说明
├── scripts/
│   ├── browser_console_one_click.js  # 【推荐分享】浏览器 F12 控制台一键签到纯 JS 脚本（零依赖）
│   ├── yunzhi_checkin.py             # 全功能 Python 独立命令行（支持 CDP、Direct HTTP、只读烟测）
│   └── capture_traffic.py            # CDP 协议抓包与逆向调试分析工具
├── references/
│   ├── protocol.md                   # 完整逆向协议文档：双签名数学公式、规范化请求头与接口定义
│   └── pitfalls.md                   # 生产实战踩坑指南：WAF 503 TLS 指纹、MQ 异步入账延迟、大整数精度
└── tests/
    └── test_signatures.py            # 离线单元测试：保证签名与抓包验证向量逐字节一致，守卫凭据安全
```

> **安全与凭据边界**：本 Skill 内部代码**绝对不含任何真实个人 Token**。所有日志均强制对 Token 进行截断脱敏（如 `eyJhbGci...3AGf2Q`），杜绝敏感凭据泄露。

---

## 三种运行模式对比（分享选择）

| 模式 | 适用人群 | 依赖要求 | WAF 免疫 | 运行体验 |
|---|---|---|:---:|---|
| **模式 1：控制台一键脚本** | 普通好友、非技术用户 | 现代浏览器即可，**零安装依赖** | 100% | 复制粘贴到控制台，3 秒完成 |
| **模式 2：Chrome CDP 驱动** | 本地开发机、个人桌面定时任务 | Python 3 + Playwright + 桌面 Chrome | 100% | 免提取 Token，自动识别云机并打卡 |
| **模式 3：Direct HTTP 命令行** | Linux VPS、无桌面轻量 Docker 容器 | Python 3 + Token (可选 curl_cffi) | 需模拟指纹 | 纯命令行传参，支持 cron 与 Webhook |

---

## 快速上手（分享给好友指南）

### 模式 1：浏览器控制台一键签到（最推荐分享）

这是向没有任何编程或 Python 环境的好友分享时体验最好的方式：

1. **登录网页**：在 Chrome / Edge / Safari 等任意电脑浏览器中打开 [云智手机入口](https://yunzhi.play.cn/ai/?channel_code=00000042) 并完成登录。
2. **打开控制台**：按键盘 **F12**（Mac 用户按 `Command + Option + I`，或网页右键点击「检查」），切换到 **Console**（控制台）标签页。
3. **粘贴运行**：打开本项目中的 [`scripts/browser_console_one_click.js`](scripts/browser_console_one_click.js)，全选复制并粘贴到控制台，敲击回车！
4. **即刻生效**：控制台将打印带有彩色彩标的执行进度，自动完成弹窗领取与云机续期：
   ```
   🚀 云智手机一键自动打卡与 2 天云机空间领取开始...
   [1/4] 凭据读取成功: eyJhbGci...xyz123
   [2/4] 每日登录弹窗福利领取成功 (2 天云机空间卡)！
   [3/4] 正在查询待生效卡片与云机设备...
   [4/4] 目标云机: D0026092223823038，正在开通卡片...
   🎉 全部流程完成！云机最新有效期至: 2026-11-28 21:48:38
   ```

---

### 模式 2：Chrome CDP 自动化模式（推荐个人自动化）

借助 Chrome DevTools Protocol，脚本自动挂载到已登录的 Chrome 实例，无需每次手动拷贝 Token，且 100% 绕过边缘 WAF。

1. **启动带调试端口的 Chrome**（以个人日常 Profile 启动）：
   - **macOS**:
     ```bash
     /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
     ```
   - **Windows**:
     ```cmd
     chrome.exe --remote-debugging-port=9222
     ```
2. **运行签到脚本**：
   ```bash
   # 完整签到流程
   python3 scripts/yunzhi_checkin.py --cdp http://127.0.0.1:9222

   # 只读烟测（仅检查登录态与配额，不消耗卡片）
   python3 scripts/yunzhi_checkin.py --cdp http://127.0.0.1:9222 --smoke

   # 输出 JSON 供通知机器人或定时器消费
   python3 scripts/yunzhi_checkin.py --cdp http://127.0.0.1:9222 --json
   ```

---

### 模式 3：Direct HTTP 命令行模式（适合服务器与 Docker）

在没有 GUI 桌面的服务器环境中，可以通过传入 Token 直接调用：

#### 1. 如何获取 Token？
在已登录 `https://yunzhi.play.cn` 的浏览器中，按 F12 进入 Console，执行以下一行命令即可将 Token 自动复制到剪贴板：
```javascript
copy(localStorage.getItem('cloud_phone_token'));
```

#### 2. 执行命令
```bash
# 环境变量传参
export YUNZHI_TOKEN="eyJhbGciOi..."
python3 scripts/yunzhi_checkin.py

# 或 CLI 显式传参
python3 scripts/yunzhi_checkin.py --token "eyJhbGciOi..."
```

> **注意（WAF 避坑）**：由于云智接口开启了 TLS 指纹审查，服务器端直连推荐安装 `curl_cffi`（`pip install curl_cffi`）。脚本检测到该库时会自动启用 `chrome120` 浏览器指纹模拟；若未安装且遇到 HTTP 503，请改用模式 1 或模式 2。

---

## 协议逆向与双签名核心速查

云智手机网关采用了**双签名体系**（详见 [`references/protocol.md`](references/protocol.md)）：

1. **Body MD5 业务体签名**：
   - 盐值：`7f9e2d08c1b5a3709e4f6d2a8c0e1b3f`
   - 公式：`sign = MD5(sorted_params("k=v&...") + salt)`
2. **Header HMAC-SHA256 通信头签名**：
   - 秘钥：`8822FF81B6623e6f338d6F2A7F49DA83`
   - 排除头（Qu 表）：`content-length`, `host`, `connection`, `accept-encoding`, `user-agent`, `sign`, `content-type`, `accept`, `device_code`, `model`, `api_level`, `cache-control`
   - 规则：`HMAC-SHA256("METHOD\n/yunzhi+path\nparams\nbody\ncanonical_headers\n", key)`
   - **时序核心**：必须先算 Body MD5 嵌入 body，再对包含体签名的「最终请求体」计算 Header HMAC。

---

## 常见排障与避坑指南

若运行过程中遇到异常，请对照以下高频场景排查（更详尽的分析见 [`references/pitfalls.md`](references/pitfalls.md)）：

1. **HTTP 503 WAF 拦截**：
   - **原因**：直连 Python OpenSSL TLS 握手特征被网关识别拦截。
   - **解决**：改用 `--cdp` 模式，或使用 `browser_console_one_click.js`，或安装 `curl_cffi`。
2. **弹窗领取成功但卡片未开通**：
   - **原因**：后端消息队列发卡存在 1~2 秒入账延迟。
   - **解决**：脚本已内置自动缓冲与重试机制，若手动调用请在 claim 后等待 2 秒再查 benefit。
3. **账户有多台云机，续期到了错误设备**：
   - **解决**：脚本内置设备过滤器，严格优先选取 `status == 2`（运行中）的活跃实例，不会误绑定到已过期或历史机器。
4. **离线测试回归验证**：
   - 任何改动后可直接执行单元测试验证签名数学正确性：
     ```bash
     python3 tests/test_signatures.py
     ```
