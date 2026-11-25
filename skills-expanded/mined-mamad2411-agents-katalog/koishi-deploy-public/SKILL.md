---
name: koishi-deploy-public
description: Koishi 公网部署与对外服务操作指南，覆盖 server 插件、host=0.0.0.0、selfUrl、反向代理、Nginx/Caddy/SSL/域名、Webhook、server-proxy、server-satori，以及控制台 auth 与安全。
---

# Koishi 公网部署

这个 skill 用于把 Koishi 控制台、Webhook、Satori 服务或其他 HTTP 能力安全地暴露到公网。

## 基本原则

1. 先定部署形态，再定配置。
2. 公网暴露前，先做认证与权限控制。
3. 生产环境优先使用反向代理，不建议裸露 Koishi 端口。
4. 只要外部服务需要访问 Koishi，就必须把 `selfUrl` 配成外部可访问地址。
5. WebSocket 场景必须确认代理支持协议升级。
6. 不要建议未文档化的 server API。

## 先判断场景

### 仅局域网访问

适合本地调试、临时演示、同一局域网设备访问。

```yaml
plugins:
  group:server:
    server:mw5hp6:
      host: 0.0.0.0
      port: 5140
```

### 域名 + SSL + 反向代理

适合生产部署。

```yaml
plugins:
  group:server:
    server:mw5hp6:
      host: 127.0.0.1
      port: 5140
      selfUrl: https://bot.example.com
```

前面使用 Caddy 或 Nginx 暴露 HTTPS。

### Webhook / Satori / 跨域控制台

适合平台回调、Satori 协议服务、控制台前后端跨域。关键是：外部必须能访问对应 URL，且代理层和 `selfUrl` 一致。

## server 插件配置

Koishi 的服务器能力来自 `@koishijs/plugin-server`。

- `host`：监听地址。默认 `127.0.0.1`，设为 `0.0.0.0` 监听所有地址。
- `port`：监听端口，常用 `5140`。
- `maxPort`：端口被占用时尝试到哪个上限。
- `selfUrl`：Koishi 对外暴露的公网地址，供 webhook、资源链接、适配器、Satori 等插件使用。

`selfUrl` 不是本地监听地址，而是外部访问者看到的地址，例如：

```yaml
plugins:
  group:server:
    server:mw5hp6:
      selfUrl: https://bot.example.com
```

## Caddy 反向代理

Caddy 适合希望自动处理证书的用户。

```text
bot.example.com {
  reverse_proxy http://127.0.0.1:5140
}
```

如果只是 HTTP 测试：

```text
:80 {
  reverse_proxy http://127.0.0.1:5140
}
```

要点：

- 同机反代时 Koishi 可保持 `host: 127.0.0.1`。
- 域名解析必须指向服务器。
- 80/443 端口需要可达。

## Nginx 反向代理

```nginx
map $http_upgrade $connection_upgrade {
  default upgrade;
  '' close;
}

server {
  server_name bot.example.com;

  location / {
    proxy_pass http://127.0.0.1:5140/;
    proxy_redirect off;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $http_host;
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
  }
}
```

WebSocket 必须保留 `proxy_http_version 1.1`、`Upgrade`、`Connection`。控制台实时连接断开、Satori WS 连不上时优先检查这些。

## selfUrl 规则

必须设置 `selfUrl` 的场景：

- 平台 webhook 回调。
- 插件生成外部可访问链接。
- Satori 或其他 HTTP/WS 服务要被外部访问。
- 通过域名或 HTTPS 访问 Koishi。

推荐写最终外部地址：

```text
https://bot.example.com
```

如果使用子路径部署，也要体现在 `selfUrl` 和反代配置中。

## server-proxy

`server-proxy` 用于解决控制台跨域问题，不是 Nginx/Caddy 的替代品。

```yaml
plugins:
  group:server:
    server-proxy:7k3n2a:
      path: /proxy
```

典型用途：控制台前端请求跨域、资源或接口地址不一致。排查顺序：外部地址是否正确 → 反代是否正常 → `server-proxy.path` 是否匹配。

## server-satori

`server-satori` 提供 Satori 协议服务，可让其他 Koishi 实例或 Satori 客户端通过 HTTP / WebSocket 访问当前实例。

```yaml
plugins:
  group:server:
    server-satori:91kcoc:
      path: /satori
```

公网场景建议明确设置路径，确保代理支持 WebSocket，并让 `selfUrl` 与外部地址一致。

## 控制台安全

公网部署时，安全优先级高于“能访问”。

建议：

- 启用 `@koishijs/plugin-auth`。
- 设置管理员密码。
- 只给必要用户必要权限。
- 如果只需要 webhook，不要开放完整控制台。
- 不要把未认证控制台直接暴露给公网。

回答“能不能直接暴露端口”时：可以，但不推荐。更安全做法是反向代理 + SSL + 登录认证。

## 常见问题

### 只能本机访问

通常是 `host` 还是 `127.0.0.1`。局域网直连要改成 `0.0.0.0`。

### 改了 host 还是访问不了

检查：配置是否重载、端口是否变化、防火墙/安全组是否放行、反代是否指向正确端口。

### webhook 收不到回调

检查：域名是否公网可达、HTTPS 是否符合平台要求、`selfUrl` 是否正确、`path` 是否一致、代理是否转发到 Koishi。

### Nginx 下实时连接断开

检查 WebSocket 代理头：`Upgrade`、`Connection`、`proxy_http_version 1.1`、读写超时。

### 控制台跨域

检查前后端外部地址、反向代理、`server-proxy.path`。
