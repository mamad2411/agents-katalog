---
name: network-license-protocol-analysis
description: 抓包拆解网络授权协议 —— 找出哪个字段是签名、哪个字段决定授权、有没有时效和一次性限制。目标是回答"我能不能只改一个字段就通过"。
---

# 网络授权协议分析

目标不是"看懂协议"，是回答三个问题：

1. **哪个字段决定授权结果？**（改它就行，还是必须重算签名）
2. **有没有签名 / 加密覆盖这个字段？**（有 → 得 hook 签名函数，不能改包）
3. **有没有时效 / 一次性 / 环境绑定？**（有 → 重放会失效）

三个问题答完，方案就定了。

---

## 一、先解决抓包

### 证书固定的四种情况

| 情况 | 表现 | 处理 |
| :--- | :--- | :--- |
| 不校验 | 直接能抓 | 用 mitmproxy / Charles |
| 校验系统证书 | 装 CA 到系统信任区即可 | Android 7+ 要装到系统区（需 root）或改 APK |
| 校验指定证书（pinning） | 装了 CA 仍然握手失败 | Frida hook 校验函数，或 patch 掉 |
| 双向认证（mTLS） | 客户端带证书 | 从客户端提取证书 + 私钥，导入抓包工具 |

**Frida 一把梭（Android）**：

```javascript
// 通用 SSL unpinning —— 按需选一个，不要全开
Java.perform(function () {
    var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var SSLContext = Java.use('javax.net.ssl.SSLContext');
    var TrustManager = Java.registerClass({
        name: 'com.x.TrustAll',
        implements: [X509TrustManager],
        methods: {
            checkClientTrusted: function () {},
            checkServerTrusted: function () {},
            getAcceptedIssuers: function () { return []; }
        }
    });
    var TrustManagers = [TrustManager.$new()];
    var ctx = SSLContext.getInstance('TLS');
    ctx.init(null, TrustManagers, null);
    var factory = ctx.getSocketFactory();
    // 替换所有 SSLSocketFactory 创建点，或 hook OkHttp 的 sslSocketFactory
});
```

**注意**：pinning 常出现在 OkHttp 的 `CertificatePinner`、Volley、或原生层的 `SSL_CTX_set_verify`。Java 层 hook 完还抓不到，就往 native 走。

### 抓到之后先做的事

```
1. 保存完整请求 + 响应（含 header）
2. 记下时间戳
3. 重复同一个操作两次，对比两个请求的差异
```

**对比两次请求**是判断签名字段最快的办法 —— 只有时间戳/nonce 变，说明其他字段是固定的；如果整个 body 都变，可能有整体加密。

---

## 二、拆字段：找签名

### 长度指纹（最实用）

看每个可疑字段的长度和字符集：

| 长度 | 字符集 | 大概率是 |
| :--- | :--- | :--- |
| 32 | hex | MD5 |
| 40 | hex | SHA1 |
| 64 | hex | SHA256 / HMAC-SHA256 |
| 128 | hex | SHA512 |
| 44 | base64（末尾 `=`） | SHA256 的 base64 |
| 24 | base64 | 3DES / 短 token |
| 16 | hex | 4 字节 CRC / 短 ID |
| 不定长 + base64 | 含 `+` `/` | RSA 签名（长度 = 密钥字节数，2048 位 = 344 base64 字符） |

### 判断方法：改一个字段，看签名变不变

```
1. 原样重发 → 应该成功（基线）
2. 改 body 里任意一个业务字段（比如 product_id）→ 重发
3. 看服务端返回什么
```

- 返回"签名错误" → 有签名，且覆盖了这个字段
- 返回正常业务错误（比如"产品不存在"）→ **没有签名覆盖**，可以随便改
- 返回成功 → 这个字段不参与校验

这一步能省掉大量逆向工作。**先做这个，再决定要不要逆算法。**

### 签名覆盖范围的推断

改不同字段，看哪些触发"签名错误"：

```
改 A 字段 → 签名错误
改 B 字段 → 签名错误
改 C 字段 → 正常
```

说明签名 = `f(A, B, 固定值...)`，C 不在里面。

逐个试，能画出签名的输入集合。

---

## 三、判加密

### 三种常见形态

**1. 整个 body 是密文**

```json
{"data": "U2FsdGVkX1+..."}
```

特征：字段只有一个，内容是 base64 或 hex，长度随业务变化。
做法：hook 加密函数（搜 `AES` / `Cipher.getInstance` / `CCCrypt`），在**加密前**打印明文。

**2. 字段级加密**

```json
{"uid": "123", "payload": "xxxxx", "sign": "yyyy"}
```

只有敏感字段加密。
做法：同上，找加密函数的入参。

**3. 自定义异或 / 混淆**

特征：密文和明文等长，字符集奇怪。
做法：抓两组明文-密文对，异或一下看是不是固定 key。

```python
# 两组对比，key 会自己浮出来
k1 = bytes.fromhex(c1); p1 = b'{"valid":true}'
print(bytes(a ^ b for a, b in zip(k1, p1)))
```

---

## 四、时效与一次性

### 时间戳

请求里有 `ts` / `timestamp` / `time` 字段：

- 服务端校验窗口通常是 ±5 分钟
- 重放时**必须更新这个字段**，而且如果它参与签名，就得重算签名

**测试方法**：把 ts 改成 1 小时前，看是否报"请求过期"。报 → 有时效窗口。

### Nonce

有 `nonce` / `rand` / `requestId` 字段：

- 服务端可能记录已用过的 nonce（防重放）
- 测试：同一个 nonce 发两次，第二次失败 → 有防重放

**绕过**：nonce 通常不参与业务逻辑，只参与签名。改 nonce + 重算签名即可。

### 一次性激活

激活接口通常只能调一次：

- 换机器码重新激活 → 看服务端是否拒绝
- 同一机器重复激活 → 看是否返回"已激活"

**这类限制通常做在服务端**，客户端绕不过。要么改服务端响应，要么 patch 客户端的"已激活"判定。

---

## 五、心跳

激活成功后，客户端可能定期发心跳：

```
每 30 分钟 → POST /heartbeat { license_id, machine_code }
→ { valid: true, expire: "2027-01-01" }
```

**心跳是云端授权的命门**：patch 掉激活流程还不够，心跳返回 false 时客户端会锁功能。

处理顺序：

1. 先确认有没有心跳（挂机 2 小时，看有没有周期性请求）
2. 有 → 看心跳返回什么，客户端怎么处理
3. 选择：模拟心跳响应 / patch 心跳处理逻辑 / 掐掉心跳请求

**坑**：有些客户端在心跳失败时**静默降级**（不报错，但功能悄悄受限）。所以要对比心跳正常/异常时的功能差异。

---

## 六、重放测试清单

拿到一个成功响应后，按顺序测：

```
[ ] 原样重放 → 成功？（有防重放就失败）
[ ] 改 ts 为当前时间 → 成功？（有时效窗口就失败）
[ ] 改 nonce → 成功？（nonce 参与签名就失败）
[ ] 改 valid: false → true → 客户端认吗？
[ ] 改 expire 为 2099 → 客户端认吗？
[ ] 改 features 数组加一项 → 客户端认吗？
[ ] 断网 + 本地伪造响应 → 客户端认吗？
```

最后一问最关键：**如果客户端只认 HTTPS 且校验证书，本地伪造就得先过证书这关**（见 `cloud-license-emulation`）。

---

## 七、常见误判

| 现象 | 误判 | 实际 |
| :--- | :--- | :--- |
| 改 `valid:true` 没效果 | 以为签名挡住了 | 客户端读的是另一个字段（`status` / `code`） |
| 重放成功 | 以为没防护 | 防护在心跳里，激活接口本来就允许重放 |
| 抓不到包 | 以为没网络请求 | 走了 QUIC / HTTP3，或 native 层自定义协议 |
| 响应是明文 JSON | 以为没加密 | 签名在 header 里（`X-Sign`） |
| 改了请求没报错 | 以为没签名 | 服务端只对**特定字段**签名，你改的不在里面 |

**排查顺序**：先确认客户端到底读哪个字段（hook JSON 解析 / 在判定点下断看寄存器），再谈改包。反过来做会绕很久。
