---
name: sky-trpc
description: >-
  tRPC ile uçtan uca tip güvenli API: router ve procedure yapısı, context (oturum, db),
  middleware ile korumalı/rol bazlı procedure'ler, Zod girdi doğrulama, hata eşleme,
  TanStack Query entegrasyonu (optimistic, invalidate), Next.js App Router ile sunucu tarafı
  çağrı (server caller, RSC prefetch + hydrate), abonelikler, batching ve ne zaman tRPC
  kullanılmamalı. "tRPC", "tip güvenli API", "frontend-backend tipleri" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · tRPC

## Ne zaman?

✓ Aynı repo (monorepo) TS frontend + backend, iç API, hızlı iterasyon.
✗ Dış tüketiciler (mobil başka dil, ortaklar) → REST/OpenAPI (bkz. `sky-public-api`); basit Next uygulamasında
Server Actions zaten tip güvenli — tRPC şart değil.

## Yapı

```
server/
  trpc.ts           # initTRPC, context, middleware'ler, procedure türleri
  routers/
    booking.ts
    client.ts
  root.ts           # appRouter = router({ booking, client })
app/api/trpc/[trpc]/route.ts   # fetchRequestHandler
```

```ts
// server/trpc.ts
export const createContext = async () => ({ db, session: await auth() });
const t = initTRPC.context<typeof createContext>().create({ transformer: superjson, errorFormatter: zodFlatten });
export const router = t.router;
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.session?.user) throw new TRPCError({ code: "UNAUTHORIZED" });
  return next({ ctx: { ...ctx, user: ctx.session.user } });
});
export const orgProcedure = protectedProcedure.input(z.object({ orgId: z.string().uuid() })).use(async ({ ctx, input, next }) => {
  const m = await getMembership(ctx.user.id, input.orgId);
  if (!m) throw new TRPCError({ code: "NOT_FOUND" });
  return next({ ctx: { ...ctx, membership: m } });
});
```

```ts
// server/routers/booking.ts
export const bookingRouter = router({
  list: orgProcedure.input(z.object({ orgId: z.string().uuid(), cursor: z.string().nullish() }))
    .query(({ ctx, input }) => bookingService.list(ctx.membership, input)),
  create: orgProcedure.input(CreateBooking.extend({ orgId: z.string().uuid() }))
    .mutation(({ ctx, input }) => bookingService.create(ctx.membership, input)),
});
```
Procedure ince; iş mantığı serviste (bkz. `sky-backend-api`).

## İstemci (TanStack Query entegrasyonu)

```tsx
const trpc = useTRPC();
const qc = useQueryClient();
const list = useQuery(trpc.booking.list.queryOptions({ orgId }));
const create = useMutation(trpc.booking.create.mutationOptions({
  onSuccess: () => qc.invalidateQueries({ queryKey: trpc.booking.list.queryKey() }),
}));
```
Girdi/çıktı tipleri otomatik; backend alanı yeniden adlandırınca frontend derlenmez — tRPC'nin sihri bu.

## RSC ile

- Sunucu bileşeninde doğrudan `caller` (HTTP yok) veya `prefetch` + `HydrationBoundary` ile istemci cache'ini doldur.
- Gizli veriler sunucu çağrısında kalır.

## Hatalar

- `TRPCError` kodları: `BAD_REQUEST`, `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `CONFLICT`, `TOO_MANY_REQUESTS`.
- Zod hatalarını `errorFormatter` ile alan bazlı döndür → form `setError` (bkz. `sky-forms`).
- Beklenmeyen hatalar loglanır; istemciye genel mesaj.

## İpuçları

- `superjson` ile Date/Map/Set taşınır.
- Batching (`httpBatchLink`) varsayılan; büyük yanıtlarda `httpBatchStreamLink`.
- Abonelikler (SSE) için `httpSubscriptionLink`; detay `sky-realtime`.
- Router dosyasını 300 satırda böl; procedure adları fiil: `list`, `byId`, `create`, `cancel`.
