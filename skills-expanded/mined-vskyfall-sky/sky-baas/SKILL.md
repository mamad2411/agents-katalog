---
name: sky-baas
description: >-
  Hazır backend servisleri (BaaS) ile hızlı geliştirme: Firebase (Auth, Firestore, Storage,
  Cloud Functions, FCM, güvenlik kuralları, App Check), Convex (reaktif sorgular, mutasyonlar,
  şema), PocketBase (tek dosya Go backend), Appwrite ve Supabase karşılaştırması; ne zaman BaaS,
  ne zaman kendi backend'in, veri modelleme (doküman vs ilişkisel), güvenlik kuralları ile yetki,
  maliyet tuzakları ve kilitlenme (vendor lock-in) riski. "Firebase", "Convex", "PocketBase",
  "backend yazmadan", "hazır backend" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · BaaS (hazır backend)

## Seçim

| Servis | Güçlü yanı | Dikkat |
|---|---|---|
| **Supabase** | Postgres (SQL, ilişkiler), RLS, açık kaynak | bkz. `sky-supabase` |
| **Firebase** | olgun, mobil SDK'lar, FCM, Analytics, hosting | Firestore sorgu sınırları, okuma başına ücret |
| **Convex** | TS ile reaktif sorgular (UI otomatik güncellenir), transaction'lı mutasyonlar, tip güvenliği uçtan uca | kendi veri modeli, kilitlenme |
| **PocketBase** | tek Go binary + SQLite, admin paneli, gerçek zamanlı, ucuz VPS'te | tek sunucu ölçeği |
| **Appwrite** | açık kaynak, self-host, auth/db/storage/functions | daha küçük ekosistem |
Prototip, mobil uygulama, küçük ekip → BaaS çok hız kazandırır. Karmaşık iş kuralları, çok kiracılı B2B, sıkı veri kontrolü → kendi backend'in veya Supabase (SQL + RLS).

## Firebase

- **Firestore modelleme**: sorguları önceden tasarla (join yok); denormalizasyon; alt koleksiyonlar; bileşik sorgular için indeks; büyük dizileri belgede tutma.
- **Güvenlik kuralları = yetki katmanı** (istemci doğrudan DB'ye bağlanır!):
```
match /orgs/{orgId}/bookings/{id} {
  allow read: if request.auth != null && exists(/databases/$(database)/documents/orgs/$(orgId)/members/$(request.auth.uid));
  allow create: if request.auth != null && request.resource.data.keys().hasOnly(['clientId','startsAt','serviceId'])
                && request.resource.data.startsAt is timestamp;
}
```
  Kuralları Emulator Suite ile **test et**; `allow read, write: if true` prod'da asla.
- **App Check** (bot/kötüye kullanım koruması), Cloud Functions (v2) ile sunucu tarafı mantık (ödeme webhook'u, bildirim), sırlar Secret Manager'da.
- Maliyet: okuma/yazma başına ücret → dinleyicileri (onSnapshot) dar tut, sayfalama, sayaçlar için toplu/dağıtık sayaç; bütçe alarmı.
- FCM push (bkz. `sky-notifications`), Firebase Hosting (statik + SSR framework desteği).

## Convex

```ts
// convex/bookings.ts
export const upcoming = query({ args: { orgId: v.id("orgs") }, handler: async (ctx, { orgId }) => {
  const user = await requireMember(ctx, orgId);
  return ctx.db.query("bookings").withIndex("by_org_start", (q) => q.eq("orgId", orgId).gte("startsAt", Date.now())).take(50);
}});
export const create = mutation({ args: { orgId: v.id("orgs"), startsAt: v.number(), serviceId: v.id("services") }, handler: async (ctx, a) => { … } });
// React: const bookings = useQuery(api.bookings.upcoming, { orgId });   // değişince otomatik güncellenir
```
Mutasyonlar transaction'lı (yarış durumu yok), sorgular reaktif (gerçek zamanlı ücretsiz gelir), zamanlanmış fonksiyonlar ve action'lar (dış API). Yetki her fonksiyonun içinde.

## PocketBase

`./pocketbase serve` → admin UI, koleksiyonlar, API kuralları (`@request.auth.id = owner`), gerçek zamanlı abonelikler, dosyalar, OAuth; JS/Go ile genişletme (hook'lar). Litestream ile yedek (bkz. `sky-sqlite`). Küçük işletme uygulamaları ve iç araçlar için harika.

## Ortak kurallar

- Yetki **sunucu tarafında** (kurallar/fonksiyonlar), istemci kontrolleri yalnızca UX.
- Sırlar istemci paketinde değil (Firebase web config gizli değildir ama servis hesabı anahtarı gizlidir).
- Veri dışa aktarma ve yedek planı (kilitlenme riskine karşı); iş mantığını servis bağımsız modüllerde tut (bkz. `sky-architecture-patterns` ports & adapters).
- KVKK: veri bölgesi seçimi (AB), alt işleyici listesi (bkz. `sky-privacy-engineering`).
