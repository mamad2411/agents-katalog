---
name: zephyr-net-socket
description: Expert guidance for BSD sockets, TLS/DTLS secure sockets, and DNS resolution in Zephyr OS. Covers TCP/UDP socket programming, secure socket creation with mbedTLS, TLS credential management, hostname resolution with getaddrinfo/dns_resolve, mDNS/LLMNR support, and socket offloading. Use when implementing network clients/servers, adding TLS security to connections, resolving hostnames, or configuring socket-based networking.
---

# Zephyr Network Sockets

## Quick Start

1. **Enable Sockets**: `CONFIG_NET_SOCKETS=y` in `prj.conf`
2. **Choose Protocol**: TCP (`CONFIG_NET_TCP=y`) or UDP (`CONFIG_NET_UDP=y`)
3. **Optional TLS**: `CONFIG_NET_SOCKETS_SOCKOPT_TLS=y` for secure sockets
4. **Optional DNS**: `CONFIG_DNS_RESOLVER=y` for hostname resolution
5. **Create Socket**: `socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)`

## Core TCP Client Pattern

```c
#include <zephyr/net/socket.h>

int tcp_client_example(void)
{
    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(8080),
    };
    inet_pton(AF_INET, "192.168.1.100", &addr.sin_addr);

    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock < 0) {
        return -errno;
    }

    int ret = connect(sock, (struct sockaddr *)&addr, sizeof(addr));
    if (ret < 0) {
        close(sock);
        return -errno;
    }

    /* Send/receive data */
    send(sock, "Hello", 5, 0);

    char buf[128];
    int len = recv(sock, buf, sizeof(buf), 0);

    close(sock);
    return 0;
}
```

## Core TCP Server Pattern

```c
int tcp_server_example(void)
{
    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(8080),
        .sin_addr.s_addr = INADDR_ANY,
    };

    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock < 0) {
        return -errno;
    }

    int ret = bind(sock, (struct sockaddr *)&addr, sizeof(addr));
    if (ret < 0) {
        close(sock);
        return -errno;
    }

    ret = listen(sock, 5);  /* Backlog of 5 */
    if (ret < 0) {
        close(sock);
        return -errno;
    }

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client = accept(sock, (struct sockaddr *)&client_addr, &client_len);
        if (client < 0) {
            continue;
        }

        /* Handle client connection */
        char buf[128];
        int len = recv(client, buf, sizeof(buf), 0);
        if (len > 0) {
            send(client, buf, len, 0);  /* Echo back */
        }

        close(client);
    }
}
```

## Socket Types

| Family | Type | Protocol | Description | Kconfig |
|--------|------|----------|-------------|---------|
| AF_INET/AF_INET6 | SOCK_STREAM | IPPROTO_TCP | TCP stream | `CONFIG_NET_TCP` |
| AF_INET/AF_INET6 | SOCK_STREAM | IPPROTO_TLS_1_2 | TLS over TCP | `CONFIG_NET_SOCKETS_SOCKOPT_TLS` |
| AF_INET/AF_INET6 | SOCK_DGRAM | IPPROTO_UDP | UDP datagram | `CONFIG_NET_UDP` |
| AF_INET/AF_INET6 | SOCK_DGRAM | IPPROTO_DTLS_1_2 | DTLS over UDP | `CONFIG_NET_SOCKETS_ENABLE_DTLS` |
| AF_INET/AF_INET6 | SOCK_RAW | IPPROTO_IP | Raw IP packets | `CONFIG_NET_SOCKETS_INET_RAW` |
| AF_PACKET | SOCK_RAW | ETH_P_ALL | Raw L2 packets | `CONFIG_NET_SOCKETS_PACKET` |
| AF_CAN | SOCK_RAW | CAN_RAW | CAN bus | `CONFIG_NET_SOCKETS_CAN` |

## Detailed References

- **BSD Sockets API**: [references/sockets.md](references/sockets.md)
- **TLS/DTLS Secure Sockets**: [references/tls.md](references/tls.md)
- **DNS Resolution**: [references/dns.md](references/dns.md)
- **Kconfig Options**: [references/kconfig.md](references/kconfig.md)
- **File Locations**: [references/locations.md](references/locations.md)

## TLS Quick Start

```c
#include <zephyr/net/socket.h>
#include <zephyr/net/tls_credentials.h>

#define CA_CERT_TAG 1

static const unsigned char ca_cert[] = { /* DER-encoded CA cert */ };

int tls_client_example(void)
{
    /* 1. Register credentials */
    tls_credential_add(CA_CERT_TAG, TLS_CREDENTIAL_CA_CERTIFICATE,
                       ca_cert, sizeof(ca_cert));

    /* 2. Create TLS socket */
    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);

    /* 3. Configure TLS options */
    sec_tag_t tags[] = { CA_CERT_TAG };
    setsockopt(sock, SOL_TLS, TLS_SEC_TAG_LIST, tags, sizeof(tags));

    char hostname[] = "example.com";
    setsockopt(sock, SOL_TLS, TLS_HOSTNAME, hostname, sizeof(hostname));

    /* 4. Connect and use like regular socket */
    struct sockaddr_in addr = { /* ... */ };
    connect(sock, (struct sockaddr *)&addr, sizeof(addr));

    send(sock, "GET / HTTP/1.1\r\n\r\n", 18, 0);

    close(sock);
    return 0;
}
```

## DNS Quick Start (getaddrinfo)

```c
#include <zephyr/net/socket.h>

int dns_lookup_example(void)
{
    struct addrinfo hints = {
        .ai_family = AF_INET,      /* or AF_UNSPEC for IPv4/IPv6 */
        .ai_socktype = SOCK_STREAM,
    };
    struct addrinfo *res;

    int ret = getaddrinfo("example.com", "443", &hints, &res);
    if (ret != 0) {
        printk("DNS lookup failed: %d\n", ret);
        return -1;
    }

    /* Use resolved address */
    int sock = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
    connect(sock, res->ai_addr, res->ai_addrlen);

    freeaddrinfo(res);  /* Free when done */
    return 0;
}
```

## Minimum Kconfig

### Basic Sockets
```
CONFIG_NETWORKING=y
CONFIG_NET_SOCKETS=y
CONFIG_NET_TCP=y
CONFIG_NET_UDP=y
CONFIG_NET_IPV4=y
CONFIG_NET_IPV6=y
```

### With TLS
```
CONFIG_NET_SOCKETS_SOCKOPT_TLS=y
CONFIG_MBEDTLS=y
CONFIG_MBEDTLS_BUILTIN=y
CONFIG_MBEDTLS_ENABLE_HEAP=y
CONFIG_MBEDTLS_HEAP_SIZE=60000
```

### With DNS
```
CONFIG_DNS_RESOLVER=y
CONFIG_DNS_SERVER_IP_ADDRESSES=y
CONFIG_DNS_SERVER1="8.8.8.8"
```

## Common Socket Options

| Level | Option | Description |
|-------|--------|-------------|
| SOL_SOCKET | SO_REUSEADDR | Reuse local address |
| SOL_SOCKET | SO_RCVTIMEO | Receive timeout |
| SOL_SOCKET | SO_SNDTIMEO | Send timeout |
| SOL_SOCKET | SO_BINDTODEVICE | Bind to specific interface |
| SOL_TLS | TLS_SEC_TAG_LIST | TLS credential tags |
| SOL_TLS | TLS_HOSTNAME | Server hostname for SNI |
| SOL_TLS | TLS_PEER_VERIFY | Peer verification level |
| SOL_TLS | TLS_CIPHERSUITE_LIST | Allowed ciphersuites |

## Non-Blocking Sockets

```c
/* Set non-blocking mode */
int flags = fcntl(sock, F_GETFL, 0);
fcntl(sock, F_SETFL, flags | O_NONBLOCK);

/* Or use MSG_DONTWAIT per-call */
recv(sock, buf, sizeof(buf), MSG_DONTWAIT);
```

## poll() for Multiple Sockets

```c
#include <zephyr/net/socket.h>

struct zsock_pollfd fds[2];
fds[0].fd = sock1;
fds[0].events = ZSOCK_POLLIN;
fds[1].fd = sock2;
fds[1].events = ZSOCK_POLLIN;

int ret = zsock_poll(fds, 2, 5000);  /* 5 second timeout */
if (ret > 0) {
    if (fds[0].revents & ZSOCK_POLLIN) {
        /* sock1 has data */
    }
    if (fds[1].revents & ZSOCK_POLLIN) {
        /* sock2 has data */
    }
}
```

## POSIX API Mode

Enable `CONFIG_POSIX_API=y` to use standard function names without `zsock_` prefix:

```c
/* With CONFIG_POSIX_API=y */
socket();   /* Instead of zsock_socket() */
connect();  /* Instead of zsock_connect() */
send();     /* Instead of zsock_send() */
recv();     /* Instead of zsock_recv() */
close();    /* Instead of zsock_close() */
```

## Related Skills

- **zephyr-wifi**: WiFi connectivity before socket operations
- **zephyr-kconfig**: Configure `CONFIG_NET_*` options
- **zephyr-shell-commands**: Network shell for debugging (`CONFIG_NET_SHELL=y`)
- **zephyr-cbor**: Binary serialization for CoAP/UDP payloads