---
name: sky-graphql
description: >-
  GraphQL API: ne zaman REST/tRPC yerine, şema tasarımı (tipler, input'lar, nullability,
  pagination connection'ları, hata modeli), code-first (Pothos) ve schema-first, GraphQL Yoga /
  Apollo Server, DataLoader ile N+1 çözümü, yetkilendirme (alan/kaynak seviyesi), sorgu
  karmaşıklığı ve derinlik sınırı, persisted queries, istemci tarafı (urql, Apollo Client,
  graphql-codegen), abonelikler, önbellek ve güvenlik. GraphQL ile çalışırken kullan.
disable-model-invocation: true
---

# Sky · GraphQL

## Ne zaman?

✓ Birçok farklı istemci (web, mobil, ortaklar) farklı veri şekilleri istiyor; zengin ilişkisel veri grafı; dış API ürünü.
✗ Tek TS frontend + backend (tRPC/Server Actions daha basit, bkz. `sky-trpc`); basit CRUD (REST + OpenAPI).

## Şema tasarımı

```graphql
type Booking implements Node {
  id: ID!
  startsAt: DateTime!
  status: BookingStatus!
  client: Client!
  service: Service!
}
enum BookingStatus { PENDING CONFIRMED CANCELLED COMPLETED }

type Query {
  booking(id: ID!): Booking
  bookings(first: Int = 20, after: String, filter: BookingFilter): BookingConnection!
}
input CreateBookingInput { serviceId: ID!, startsAt: DateTime!, clientId: ID! }
type CreateBookingPayload { booking: Booking, errors: [UserError!]! }
type UserError { field: [String!], message: String!, code: String! }
type Mutation { createBooking(input: CreateBookingInput!): CreateBookingPayload! }
```
- Mutation başına tek `input` + `payload` (genişletilebilir); beklenen hatalar `errors` alanında (alan bazlı), beklenmeyenler GraphQL `errors`.
- Liste sayfalaması Relay connection (`edges { node cursor }`, `pageInfo { hasNextPage endCursor }`).
- Nullability bilinçli: ilişki yüklenemeyebiliyorsa nullable; `!` verdiğin alan null dönerse üst nesne tamamen null olur.
- İsimlendirme: tipler PascalCase, alanlar camelCase, enum'lar SCREAMING_CASE; kırıcı değişiklik yerine `@deprecated(reason:)`.

## Sunucu (TypeScript)

- **GraphQL Yoga** (hafif, her runtime) + **Pothos** (code-first, tip güvenli, Prisma/Drizzle eklentileri) — önerilen ikili.
- Apollo Server + schema-first + graphql-codegen resolver tipleri — alternatif.
- Context: kullanıcı, DataLoader örnekleri (istek başına yeni!), db.

## N+1: DataLoader

```ts
const clientLoader = new DataLoader<string, Client>(async (ids) => {
  const rows = await db.select().from(clients).where(inArray(clients.id, [...ids]));
  const map = new Map(rows.map((r) => [r.id, r]));
  return ids.map((id) => map.get(id) ?? new Error(`client ${id} yok`));
});
// resolver: Booking.client = (b, _, ctx) => ctx.loaders.client.load(b.clientId)
```
Her istek için yeni loader (önbellek istek kapsamında, kullanıcılar arası sızma yok).

## Yetkilendirme

Resolver'da değil **iş katmanında** (aynı kural REST ve GraphQL'de geçerli); Pothos scope-auth eklentisi ile alan seviyesi kurallar
(`authScopes: { orgMember: true }`). Node arayüzünde (`node(id:)`) global ID ile her türün yetkisini kontrol et — klasik IDOR kapısı.

## Güvenlik ve maliyet

- Sorgu **derinlik** ve **karmaşıklık** sınırı (graphql-armor), sayfa boyutu üst sınırı (`first ≤ 100`).
- Üretimde **persisted queries** / güvenilir belge listesi: yalnızca bilinen sorgular çalışır (rastgele pahalı sorgu yok).
- Introspection üretimde kapalı (dış API ürünü değilse).
- Rate limit maliyet puanına göre; zaman aşımı.

## İstemci

- **graphql-codegen** (client preset) ile `graphql()` etiketli belgelerden tam tipler.
- urql (hafif) / Apollo Client (normalleştirilmiş önbellek, büyük uygulamalar) / TanStack Query + `graphql-request` (basit).
- Fragment colocation: bileşen kendi verisini fragment ile tanımlar.

## Abonelikler

`graphql-ws` (WebSocket) veya SSE; ölçekte pub/sub (Redis). Çoğu "canlı" ihtiyaç için polling veya ayrı realtime katmanı daha basit (bkz. `sky-realtime`).

## Önbellek

POST istekleri CDN'de önbelleklenmez → persisted queries + GET; yanıt önbelleği (Yoga response cache) kullanıcıya özel veride dikkatli; istemci normalleştirilmiş önbellek.
