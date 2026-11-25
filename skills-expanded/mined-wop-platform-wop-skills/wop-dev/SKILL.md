---
name: wop-dev
description: WOP 协议开发指导——canonicalRequest/必传 header 契约/三套件/L2 信封/F6/I7 心智模型与六语言 SDK 速查。商户工程师用 agent 写对接代码时使用。前置：需安装 wop-cli 基座 skill。
---

# wop-dev（开发指导 skill）

> 前置：需安装 **wop-cli** 基座（对拍/自测工具）；协议真源：
> [crypto-strategy-spec](https://github.com/wop-platform/wop-specs/blob/main/crypto/crypto-strategy-spec.md) v0.3-reviewed
> + [sdk-spec](https://github.com/wop-platform/wop-specs/blob/main/sdk/wop-sdk-spec.md) v1.0-ratified（含附录 D1–D5；§2.1 header 契约 / §2.2 错误契约 2026-08-31 增补；crypto D14 已钉）
> **安全纪律：先读 [SECURITY.md](../SECURITY.md)——私钥边界优先于一切开发便利**

## 何时用

- 商户工程师（或其 agent）用任意语言写 WOP 对接代码
- 联调签名不过，需要协议细节定位
- 选择套件 / 设计密钥管理 / 实现回调验签

## 心智模型（一张图）

```
build_request 五步（纯函数，零网络）：
套件解析(WOP-<RSA3072|RSA4096|SM2>-<SHA256|SM3>)
  → 恒必传头(全入签): appkey/nonce/timestamp + digest(有body,GET缺) + encrypt(仅L2)
  → x-wop-content-digest(有 body 必产必入签: "<alg> <小写hex>")
  → x-wop-sign(四段式: <securityReq> v1/<expiredSeconds>/<signedHeaders>/<b64url签名>)
  → [L2] 数字信封(AES-256-GCM/SM4-GCM 全文加密, wire={"encrypted":...})
响应/回调验证 F6 顺序（固定不可换）：
验签 → digest 复核 → DEK 解包 → alg 族比对 → bulk 解密
```

深入阅读（按需加载，不要一次全读）：

- [references/protocol.md](references/protocol.md) —— 协议全貌：套件/必传 header 契约（D14）/签名/信封/错误契约（WopError）/F6/I7/附录 D 纪律/事故案例
- [references/sdks/](references/sdks/) —— 六语言速查（安装/最小示例入口/套件矩阵）

## 黄金法则（agent 写代码必守）

1. **永远用官方 SDK**，不手搓 base64url/签名/信封——尾随位 12 条格式规则刚在六仓引发大修（2026-08-29 审计），标准库宽容陷阱（.NET/JDK/CPython/PHP 对非 canonical 尾随位静默丢位）手搓必踩
2. **验签/解密失败的错误输出保持模糊**（I7）——不区分密钥不符/tag 失败/算法错位，防 oracle
3. **SM2 签名 = 裸 r‖s 64 字节（禁 DER）**；SM2 密文 = C1C3C2（禁旧国标 C1C2C3）；全部 base64url **无填充**（拒 `=`）；SM2 签名 ZA 的 userId = 出向 `x-wop-appkey` 值（D14，禁库默认/空串——签名身份与请求身份恒同源）
4. 写操作调用前向用户复述确认（SECURITY.md S7）
5. 自研实现的测试**不得复用被测的出向代码构造入向响应**（D5 防镜像偏差——PHP L2 信封事故根源）

## 联调对拍方法论

签名不过（OP_GW_1022，响应不告诉你为什么）时：

1. 固定输入（method/path/body/level），用 `wop sign` 产出官方 draft
2. 同输入跑商户自研实现，产出 draft
3. 逐 header diff：`x-wop-content-digest` 是确定性可比锚（与时间/nonce 无关）；
   `x-wop-sign` 含时间戳不可直接比，但四段式结构可验
4. 首差异即根因候选——对照 protocol.md 格式规则核查

三大高频根因（按命中率排序）：base64url 尾随位非规范 / SM2 签名 DER 编码 / C1C2C3 旧国标顺序。
