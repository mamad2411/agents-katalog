---
name: sky-node-backend
description: >-
  Node.js / Bun / Deno ile bağımsız backend servisi: Hono, Fastify, Express, NestJS seçimi,
  proje yapısı, Zod doğrulama, merkezi hata yönetimi, env doğrulama, pino log, graceful
  shutdown, güvenlik middleware'leri, OpenAPI üretimi, WebSocket, testler, TypeScript çalıştırma
  (tsx, Node yerleşik TS, Bun, Deno) ve dağıtım. Next.js dışında ayrı API/servis yazarken kullan.
disable-model-invocation: true
---

# Sky · Node Backend

## Framework seçimi

| İhtiyaç | Seçim |
|---|---|
| Hızlı, tip güvenli, her runtime'da (Node/Bun/Deno/Workers) | **Hono** |
| Yüksek performans, şema tabanlı, eklenti ekosistemi | **Fastify** |
| Büyük ekip, katmanlı yapı, DI | **NestJS** |
| Mevcut proje / en yaygın | Express 5 |

## Yapı

```
src/
  index.ts            # sunucuyu başlat, shutdown
  app.ts              # app oluştur, middleware, route'lar (testte de kullanılır)
  config.ts           # env doğrulama (Zod)
  modules/booking/{routes.ts, service.ts, repo.ts, schema.ts}
  lib/{db.ts, logger.ts, errors.ts}
```

## Hono örneği

```ts
const app = new Hono<{ Variables: { user: User } }>();
app.use("*", requestId(), secureHeaders(), cors({ origin: config.FRONTEND_URL, credentials: true }));
app.use("/api/*", auth);
app.post("/api/bookings", zValidator("json", CreateBooking), async (c) => {
  const booking = await bookingService.create(c.get("user"), c.req.valid("json"));
  return c.json(booking, 201);
});
app.onError((err, c) => {
  if (err instanceof AppError) return c.json({ error: { code: err.code, message: err.message } }, err.status);
  log.error({ err, requestId: c.get("requestId") }, "unhandled");
  return c.json({ error: { code: "internal", message: "Beklenmeyen bir hata oluştu" } }, 500);
});
```
`@hono/zod-openapi` ile şemadan OpenAPI + Scalar dokümanı.

## Fastify / NestJS notları

- Fastify: şema ile doğrulama + hızlı serileştirme, `register` ile eklenti kapsülleme, `fastify.inject()` testler.
- NestJS: modül/controller/provider, Guard (auth), Interceptor, ExceptionFilter, DTO doğrulama; küçük servislerde fazla tören.

## Temel parçalar

- **Env**: Zod ile parse, eksikse başlangıçta çök.
- **Log**: pino (JSON), istek ID'si, PII redact (bkz. `sky-observability`).
- **Güvenlik**: güvenlik başlıkları, CORS izinli liste, gövde boyutu sınırı, rate limit.
- **Hata**: tek `AppError` + merkezi işleyici.
- **DB**: Drizzle / Kysely / Prisma; tek bağlantı havuzu.

## Graceful shutdown

```ts
const server = serve({ fetch: app.fetch, port: config.PORT });
for (const sig of ["SIGINT", "SIGTERM"] as const) {
  process.on(sig, async () => {
    log.info("kapanıyor");
    server.close();
    await Promise.race([drainJobs(), sleep(10_000)]);
    await db.end();
    process.exit(0);
  });
}
```
`unhandledRejection`/`uncaughtException` logla ve kontrollü kapan.

## TypeScript çalıştırma

- Geliştirme: `tsx watch src/index.ts` veya Node'un yerleşik tip silme desteği (yalnızca silinebilir sözdizimi — enum/namespace yok).
- Üretim: `tsup`/`esbuild` bundle veya `tsc`; ESM (`"type": "module"`).
- **Bun**: yerleşik TS, `bun test`, paket yöneticisi, `Bun.serve`; native modül uyumluluğunu kontrol et.
- **Deno**: izin bayrakları, yerleşik lint/format/test, `npm:` importları, Deno Deploy.

## Test ve WebSocket

Vitest + `app.request()` (Hono) / `fastify.inject()` / supertest; gerçek DB (Testcontainers), MSW dış API için.
WebSocket: Hono `upgradeWebSocket`, `ws`, Socket.IO; ölçekte Redis adapter (bkz. `sky-realtime`).

## Dağıtım

Docker (`node:22-alpine`, non-root, healthcheck), Fly/Railway/Render; Hono → Cloudflare Workers (bkz. `sky-cloudflare`, `sky-docker`).
