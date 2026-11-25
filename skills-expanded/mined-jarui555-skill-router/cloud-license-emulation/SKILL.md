---
name: cloud-license-emulation
description: 目标必须联网才能激活（D 类云端校验）时，别想"破解算法"，要想"替代服务端"。三条路：本地模拟服务端 / 中继缓存 / patch 客户端跳过请求。
---

# 云端授权：替代服务端，而不是破解算法

D 类的判定在服务端，客户端里没有"正确答案"。所以在客户端里找算法、写 keygen 全是无效功。

要做的只有三件事之一：

| 路线 | 适用 | 代价 | 副作用 |
| :--- | :--- | :--- | :--- |
| **A 本地模拟服务端** | 客户端不严格校验证书 | 中 | 要处理所有接口 |
| **B 中继缓存** | 授权是静态的（激活一次长期有效） | 低 | 需要一份正版 |
| **C patch 客户端** | 只想跳过校验 | 低 | 功能可能受限 |

**选择顺序**：先看能不能 C（最省事），不行再 A，B 只适合特定场景。

---

## 路线 C：patch 客户端（优先尝试）

先判断一件事：**客户端是"拿到响应后自己判"，还是"完全信任响应"？**

```javascript
// Frida 看客户端怎么处理响应
Interceptor.attach(Module.findExportByName(null, "SSL_read"), {
    onLeave: function (retval) {
        if (retval.toInt32() > 0) {
            console.log(hexdump(this.context.rdx, { length: 512, ansi: true }));
        }
    }
});
```

如果客户端只是 `if (resp.code === 200) unlock()`，那 patch 这个 if 就行，根本不用管服务端。

**判断方法**：断网跑，如果客户端报"网络错误"就退出 → 它依赖响应；如果断网后功能照常 → 它只是"上报"。

**patch 点**：

- 授权判定函数的返回值（`mov eax, 1` / `return true`）
- 网络请求的错误处理分支（超时也当成功）
- "未授权"弹窗的调用点（直接 nop 掉）

**注意**：C 路线最容易漏的是**二次校验**。激活时校验一次，导出/保存时再校验一次。两处都得处理。

---

## 路线 A：本地模拟服务端

### 前提条件

先测客户端到底校验不校验证书：

```bash
# 1. 改 hosts 指向本地
# 2. 起一个自签证书的 HTTPS 服务
# 3. 看客户端是否报证书错误
```

- 不报错 → 直接能模拟
- 报 `SSLHandshakeException` / `CERTIFICATE_VERIFY_FAILED` → 需要先处理校验（见 `network-license-protocol-analysis` 的 unpinning）

### 步骤 1：劫持域名

**桌面端**：改 `hosts`

```
127.0.0.1  license.vendor.com
127.0.0.1  api.vendor.com
```

**Android**：root 后改 `/system/etc/hosts`，或用 Frida hook DNS 解析。

**关键**：先把所有相关域名抓出来。抓包时看 SNI / Host header，别漏了 CDN 或备用域名。

### 步骤 2：生成证书

```bash
# 生成 CA
openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt -days 3650 -nodes \
  -subj "/CN=Fake CA"

# 生成服务器证书（注意 SAN，必须包含被劫持的域名）
openssl req -newkey rsa:2048 -keyout srv.key -out srv.csr -nodes \
  -subj "/CN=license.vendor.com"
openssl x509 -req -in srv.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out srv.crt -days 3650 \
  -extfile <(printf "subjectAltName=DNS:license.vendor.com,DNS:api.vendor.com")
```

**装 CA**：桌面端装到系统信任区；Android 装到系统区（`/system/etc/security/cacerts/`，需 root）。

### 步骤 3：起假服务

```python
# fake_license_server.py
import json, ssl
from http.server import BaseHTTPRequestHandler, HTTPServer

RESP = {
    "/api/activate": {
        "code": 0, "valid": True,
        "expire": "2099-12-31",
        "features": ["pro", "export", "batch"],
        "sign": "____"          # ← 如果客户端验签，这里必须能算对
    },
    "/api/heartbeat": {"code": 0, "valid": True, "expire": "2099-12-31"},
}

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        print(f"[REQ] {self.path}\n{body[:400]}\n")
        path = self.path.split("?")[0]
        resp = RESP.get(path, {"code": 0, "valid": True})
        data = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("srv.crt", "srv.key")
srv = HTTPServer(("0.0.0.0", 443), H)
srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
print("listening :443")
srv.serve_forever()
```

**这个脚本的核心价值是日志** —— 它会把客户端发的每个请求原样打出来。第一遍先让它返回 `{}`，看客户端报什么错，就知道它期待哪些字段。

### 步骤 4：逐字段对齐

```
客户端请求 → 看服务端真实响应（抓包）→ 照抄字段名
```

最容易漏的：

- 字段名大小写（`valid` vs `Valid`）
- 嵌套层级（`data.license.valid`）
- 数值类型（`"1"` vs `1`）
- 多余字段（客户端可能校验 `sign` 字段存在才继续）

### 步骤 5：处理签名（如果有）

如果客户端验签，假响应里的 `sign` 必须能被客户端公钥验证通过。两条路：

1. **替换客户端公钥**（改二进制，见 `license-validation-locate-patch`）
2. **hook 验签函数**，让它永远返回 true

第二条更简单，但要注意验签可能在内置的 crypto 库里（`CryptVerifySignature` / `EVP_DigestVerify` / Java `Signature.verify`），hook 点要找对。

---

## 路线 B：中继缓存

**适用**：授权是"激活一次，长期有效"，且响应里没有短期时效字段。

### 做法

1. 准备一份正版（或别人的正版）
2. 完整走一遍激活流程，抓下所有响应
3. 用 mitmproxy 的 `save` / `replay`，把响应按请求特征（URL + body 关键字段）映射回去
4. 客户端发请求 → mitmproxy 直接返回缓存响应，不转发

```python
# mitmproxy addon：按路径返回缓存
from mitmproxy import http
import json, pathlib

CACHE = json.loads(pathlib.Path("responses.json").read_text())

def request(flow: http.HTTPFlow) -> None:
    key = flow.request.path.split("?")[0]
    if key in CACHE:
        flow.response = http.Response.make(
            200,
            json.dumps(CACHE[key]).encode(),
            {"Content-Type": "application/json"},
        )
```

**致命限制**：如果响应里有 `ts` / `nonce` / 短期 token，缓存重放会被服务端或客户端拒绝。这种情况只能走 A。

**另一个限制**：机器码绑定的授权，缓存响应里带的是**正版那台机器**的机器码。客户端可能校验"响应里的机器码 == 自己的机器码"，这时要 hook 机器码读取，让客户端报出正版的机器码。

---

## 三、混合型：D + 签名

真实商业软件常见：

```
服务端返回 { data: "...", sign: "..." }
客户端用内置公钥验 sign → 通过后才解析 data
```

这种情况下：

1. 单纯改 `data` 无效（签名对不上）
2. 单纯改 `sign` 无效（没有私钥）
3. **必须二选一**：替换公钥 / hook 验签

**判断有没有签名**：把响应里任意一个字节改掉，看客户端报什么错。
- 报"数据损坏"/"校验失败" → 有签名
- 报业务错误 → 没签名，直接改

---

## 四、检查清单

```
[ ] 客户端是否校验证书：     是 / 否
[ ] 是否双向认证：           是 / 否
[ ] 响应是否带签名：         是 / 否
[ ] 签名算法：               RSA / ECDSA / HMAC / 未知
[ ] 有无心跳：               有(间隔___) / 无
[ ] 心跳失败时行为：         报错 / 静默降级 / 无影响
[ ] 授权与哪些接口相关：     激活 / 心跳 / 配置拉取 / 功能开关
[ ] 有无二次校验：           有(在___) / 无
[ ] 机器码是否参与：         是 / 否
```

**最后一项最容易翻车**：模拟服务端跑通了，但导出功能还是失败，因为导出时会重新请求一次配置接口，而那个接口没模拟。

**做法**：把客户端所有出站请求的域名/路径列全，一个不漏地模拟。
