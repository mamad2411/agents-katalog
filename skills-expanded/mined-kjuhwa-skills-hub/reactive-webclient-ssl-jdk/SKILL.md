---
tags: [backend, reactive, webclient, ssl, jdk]
name: reactive-webclient-ssl-jdk
description: Force reactor-netty WebClient to SslProvider.JDK so SSL works in slim containers that lack netty-tcnative native libraries.
trigger: Spring WebFlux WebClient SSL failures in container images; UnsatisfiedLinkError for netty-tcnative / OpenSSL; distroless or Alpine JRE images.
source_project: lucida-domain-apm
version: 1.0.0
category: backend
---

# Reactive WebClient — Force JDK SSL Provider

Reactor-netty auto-prefers OpenSSL via `netty-tcnative` when the native library is on the classpath. In slim container images (JRE-only, `distroless`, Alpine without OpenSSL dev libs), that path blows up with `UnsatisfiedLinkError` or `SSLException: failed to load native library`. Force `SslProvider.JDK` to keep the bytecode portable across image bases.

## Why

OpenSSL is faster than JDK SSL for high-RPS connections, but needs a matching glibc / OpenSSL at runtime. Most backend services make only a handful of internal calls per request — JDK SSL is plenty fast and works in every container base. Forcing JDK avoids an entire class of platform-drift outages.

## Pattern

```java
SslContext sslContext = SslContextBuilder.forClient()
        .sslProvider(SslProvider.JDK)                         // ← key line
        .trustManager(InsecureTrustManagerFactory.INSTANCE)   // dev only
        .build();

HttpClient httpClient = HttpClient.create()
        .secure(ssl -> ssl.sslContext(sslContext));

WebClient webClient = WebClient.builder()
        .clientConnector(new ReactorClientHttpConnector(httpClient))
        .build();
```

## Steps

1. Build the `SslContext` with `.sslProvider(SslProvider.JDK)` explicitly.
2. Wire it into `HttpClient.secure(...)`.
3. Pass the `HttpClient` through `ReactorClientHttpConnector` into the `WebClient.Builder`.
4. Optionally exclude `io.netty:netty-tcnative-*` to prove nothing else pulls it in.

## Counter / Caveats

- Do not use `InsecureTrustManagerFactory` outside dev/test — in production, load a real truststore.
- If you have measured that OpenSSL throughput is required, choose a base image that bundles OpenSSL (`eclipse-temurin:jdk-jammy`) and leave auto-detect on.
- Setting this on one `WebClient` does not affect others — it's a per-client choice.
