---
name: sec-secrets
description: >-
  密钥和敏感数据怎么管：API Key、数据库密码、支付密钥、Webhook 地址放哪里；永远不能出现在哪里（git 历史、日志、URL、
  前端、截图、和 AI 的聊天）；数据库里怎么加密存（libsodium、每条记录绑定、双层钥匙）；密码只存不可逆哈希；
  看明文要二次验证 + 留痕；钥匙和数据分开放；备份用公钥加密；泄露了怎么换；AI 编程助手禁读 .env。
  写任何要存密钥 / 卡号 / 证件 / 第三方 Key 的功能前、上线前、怀疑泄露时用。附 scripts/secret-scan.sh 扫 git 历史。
  触发词：密钥、API Key、泄露、.env、加密存储、数据库加密、卡号加密、日志打码、密钥轮换、备份加密、gitleaks、
  secrets management, key leak, encrypt at rest, log redaction, key rotation, encrypted backup.
---

# sec-secrets：密钥和敏感数据

**一句话：密钥只在两个地方——服务器上权限 600 的文件，或数据库里加了密的字段；其它任何地方出现一次，就当它已经泄露。**

## 1. 放哪里

| 东西 | 放哪 |
|---|---|
| 启动就要用的（数据库密码、主钥匙路径） | 服务器 `.env`，权限 `600`，不进 git，部署时不覆盖 |
| 后台能改的第三方 Key（支付、邮件、短信、Webhook 地址） | 数据库里**加密**存（下面第 3 节），后台只显示“已设置 · 尾号 ab12” |
| 主钥匙（加密上面那些用的） | 数据目录里单独一个文件，`700` 目录 + `600` 文件；**不进数据库、不和数据库导出放一起** |
| 代码里 | 只有变量名；仓库里放 `.env.example`（只有键名，没有值） |

## 2. 永远不能出现的地方

- **git 历史**，包括后来删掉的提交。删文件没用，已经有人 clone 过了：必须换 Key（第 5 节）。
- **日志**：
  - 有的 API 习惯把 Key 放在网址里（`?key=…`），一次调用就会进 nginx 日志、CDN 日志、反向代理日志、日志平台。一次性登录链接、邮箱验证链接、重置密码链接里的 token 也一样。
  - 记日志前把参数打码。nginx 示例（`http {}` 里）：
    ```nginx
    # 参数里有敏感字段名，整段参数换成 [REDACTED]
    map $args $log_args {
        default $args;
        "~*(^|&)(key|api_key|token|t|h|k|code|sig|signature|password|secret)=" "[REDACTED]";
    }
    log_format safe '$remote_addr - [$time_local] "$request_method $uri?$log_args $server_protocol" '
                    '$status $body_bytes_sent "$http_user_agent"';
    access_log /var/log/nginx/access.log safe;
    ```
  - 请求头里的 `Authorization`、`x-api-key`、`Cookie` 不记。网关 / 反向代理（Caddy、Traefik）默认会记请求头，要专门去掉。
  - 推到外部日志平台之前再打码一次（第二道保险）。
- **接口返回和前端代码**：前端能看到的都是公开的。返回用户信息时按字段白名单挑，不要 `SELECT *` 原样返回；公开页面和后台不要共用一个接口。
- **错误页**：生产环境不显示异常栈、SQL、配置。
- **文档、截图、工单、群聊**，以及**和 AI 编程助手的聊天**。让 AI 读 `.env.example`，不读 `.env`。Claude Code 在项目的 `.claude/settings.json` 里禁读：
  ```json
  {
    "permissions": {
      "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./data/**)", "Read(./**/*.key)", "Read(./**/*.pem)"]
    }
  }
  ```
  密钥在聊天里出现过一次，就当它泄露了，换掉。

## 3. 数据库里加密存

用 libsodium（PHP 自带 `sodium_*`，Node 用 `libsodium-wrappers` 或内置 `crypto` 的 AES-256-GCM），别自己发明算法。

**普通的第三方 Key**：

```php
function secret_key(): string {
    $k = @file_get_contents('/srv/app/data/secret.key');           // 32 字节，600 权限
    if ($k === false || strlen($k) !== SODIUM_CRYPTO_SECRETBOX_KEYBYTES) {
        throw new RuntimeException('钥匙文件不见了');               // 不要自动生成新的，见下
    }
    return $k;
}
function enc(#[\SensitiveParameter] string $plain): string {
    $nonce = random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
    return base64_encode($nonce . sodium_crypto_secretbox($plain, $nonce, secret_key()));
}
function dec(string $stored): string {
    $raw = base64_decode($stored, true);
    $n = SODIUM_CRYPTO_SECRETBOX_NONCEBYTES;
    $plain = $raw === false ? false : sodium_crypto_secretbox_open(substr($raw, $n), substr($raw, 0, $n), secret_key());
    if ($plain === false) throw new RuntimeException('解不开');
    return $plain;
}
// 生成钥匙（只做一次）：php -r 'file_put_contents("data/secret.key", sodium_crypto_secretbox_keygen());' && chmod 600 data/secret.key
```

**高敏感数据（完整卡号、证件号）**再加两道：

- **密文绑定到这条记录和这个字段**（AEAD 的附加数据写 `"card:{id}:{field}"`）：有人能改数据库时，也没法把 A 的密文拷到 B 的记录上去冒用。
  ```php
  $nonce = random_bytes(SODIUM_CRYPTO_AEAD_XCHACHA20POLY1305_IETF_NPUBBYTES);
  $ct = sodium_crypto_aead_xchacha20poly1305_ietf_encrypt($pan, "card:$id:pan", $nonce, $fieldKey);
  ```
- **两把钥匙分开放**：外层用主钥匙，内层用第二把钥匙（只在这台服务器上，**故意不进任何备份**）。只拿到数据库 + 备份，解不开。代价：服务器整台没了，这部分数据要用户重新提交——提前想清楚能不能接受。

规矩：

- **能不存就不存**：只需要展示就只存后四位；能交给支付网关托管（token）就别自己存卡号。存完整卡号要看 PCI DSS 的要求。
- **钥匙文件丢了直接报错，不要自动生成新钥匙**——自动生成的话，旧数据永远解不开，而且没人发现。
- **用户密码只存不可逆哈希**：`password_hash()`（bcrypt / argon2id），Node 用 `argon2` 或 `bcrypt`。谁都还原不出原文，包括你自己。
- **看明文要二次验证**：重新输密码、动态码或邮箱验证码，每次都记录（谁、什么时候、看了哪条）+ 推告警，页面 60 秒后自动隐藏。传输可以做端到端：浏览器临时生成一对 ECDH 密钥把公钥发过来，服务器用它加密，只有这个页面解得开，中间任何日志、代理都只看到密文。
- 员工只能看到做事必需的字段；看敏感字段要单独权限。

## 4. 备份

- 备份用**公钥**加密后再传到异地（对象存储）。服务器上只有公钥，私钥只在你自己的电脑上（另存一份到加密 U 盘或密码管理器）。服务器被攻破，攻击者也解不开历史备份。脚本见 `sec-watch/scripts/backup-encrypt.sh`：
  ```bash
  # 生成一次（在你自己的电脑上）：私钥不要上传到服务器
  openssl req -x509 -newkey rsa:4096 -nodes -days 3650 -subj "/CN=backup" \
    -keyout backup-private.pem -out backup-cert.pem
  # 服务器上加密（只需要 backup-cert.pem）
  openssl cms -encrypt -binary -aes256 -outform DER -in db.sql.gz -out db.sql.gz.enc backup-cert.pem
  # 你的电脑上解密
  openssl cms -decrypt -binary -inform DER -in db.sql.gz.enc -inkey backup-private.pem -out db.sql.gz
  ```
- 主钥匙的副本单独放一个目录，**不和数据库导出放在一起**：只拿到备份目录的人解不开加密字段。
- 定期做恢复演练（`sec-watch`）。

## 5. 泄露了怎么办

1. **先换，再查**：在服务商后台生成新 Key → 部署 → 确认新 Key 在用 → 吊销旧 Key。不要先吊销再找新的，网站会停。
2. 查影响：服务商后台看旧 Key 最近的调用记录、花费、来源 IP。
3. 查从哪漏的：`bash scripts/secret-scan.sh` 扫 git 全部历史（装了 `gitleaks` 会优先用）；再查日志、日志平台、聊天记录。
4. 改写 git 历史（`git filter-repo`）只能防以后新 clone 的人，**不能代替换 Key**。
5. 记一笔：什么漏了、怎么漏的、怎么改的流程。

定期换：对外的支付 / 邮件 / 云 Key 至少每年一次，员工离职当天换掉他碰过的。

## 改完的检查清单

- [ ] `secret-scan.sh` 没有命中；`git ls-files` 里没有 `.env`
- [ ] 日志（本地、CDN、网关、日志平台）里搜 `key=`、`token=`、`Bearer` 搜不到明文
- [ ] 数据库里第三方 Key 都是密文，后台只显示尾号
- [ ] 钥匙文件 600、目录 700，钥匙副本和数据库导出不在同一个目录
- [ ] 删掉钥匙文件，网站报错而不是悄悄生成新钥匙（在测试环境试）
- [ ] 加密备份能在你自己的电脑上解开
