---
name: sky-backend-api
description: >-
  Backend ve API tasarımı: REST/route handler/Server Action/tRPC uç noktaları, girdi doğrulama,
  hata modeli, kimlik doğrulama ve yetkilendirme, oturum, güvenlik başlıkları, CORS, rate limit,
  webhook, dosya yükleme ve gizli anahtar yönetimi. API yazarken, auth eklerken veya backend
  güvenliğini gözden geçirirken kullan.
disable-model-invocation: true
---

# Sky · Backend & API

## Uç nokta anatomisi (her handler bu sırayı izler)

1. **Kimlik** — oturumu/token'ı doğrula → yoksa `401`.
2. **Girdi** — gövde, query, params Zod ile parse → hatalıysa `422` + alan hataları.
3. **Yetki** — bu kullanıcı bu kaynağa bu işlemi yapabilir mi? (sahiplik/rol) → `403` veya
   varlığı gizlemek için `404`.
4. **İş mantığı** — servis katmanında; handler ince kalır.
5. **Yanıt** — yalnızca gereken alanlar (DTO); parola hash'i, iç ID'ler, token sızmaz.

```ts
export async function POST(req: Request) {
  const user = await requireUser();                       // 1
  const input = CreatePost.safeParse(await req.json());   // 2
  if (!input.success) return problem(422, "Geçersiz girdi", input.error.flatten());
  const post = await postService.create(user, input.data); // 3 + 4 servis içinde
  return Response.json(toPostDTO(post), { status: 201 }); // 5
}
```

## REST kuralları

- Kaynak isimleri çoğul isim: `/api/posts/:id/comments`.
- `GET` güvenli ve idempotent; `PUT` tam değiştirme, `PATCH` kısmi; `DELETE` idempotent.
- Durum kodları: 200, 201 (+`Location`), 204, 400, 401, 403, 404, 409 (çakışma), 422, 429, 500.
- Sayfalama: cursor tabanlı (`?cursor=…&limit=20`), `limit` üst sınırlı (≤100).
- Hata gövdesi tek biçimde (RFC 9457 benzeri):
  `{ "type": "...", "title": "...", "status": 422, "errors": { "email": ["..."] } }`
- Sürümleme gerekiyorsa `/api/v1`; kırıcı değişikliği sessiz yapma.
- Tekrar edilebilir POST (ödeme, sipariş) için `Idempotency-Key` başlığı.

## Hata yönetimi

- Beklenen hatalar (doğrulama, bulunamadı, çakışma) tipli hata sınıfı → doğru durum kodu.
- Beklenmeyen hatalar: logla (istek ID'siyle), kullanıcıya genel mesaj; stack trace dönme.
- `catch` içinde hatayı yutma; ya ele al ya yeniden fırlat.

## Auth & oturum

- Parola: **argon2id** (veya bcrypt cost ≥ 12). Asla kendi kripton yok.
- Oturum çerezi: `HttpOnly; Secure; SameSite=Lax; Path=/`; kısa ömür + yenileme.
- JWT'yi `localStorage`'a koyma; çerez tercih et.
- Giriş, kayıt, parola sıfırlama uç noktalarında rate limit ve genel hata mesajı
  ("e-posta veya parola hatalı") — hesap varlığını sızdırma.
- Yetki kontrolü **her** istekte sunucuda; UI'da butonu gizlemek yetki değildir.
- Supabase kullanılıyorsa **RLS her tabloda açık**; `service_role` anahtarı yalnızca sunucuda.
- OAuth'ta `state` ve PKCE kullan.

## Güvenlik kontrol listesi

- [ ] Tüm girdiler doğrulanıyor; SQL yalnızca parametreli/ORM ile
- [ ] Kullanıcı HTML'i render ediliyorsa sanitize (DOMPurify); `dangerouslySetInnerHTML` gerekçeli
- [ ] CSRF: çerez tabanlı auth'ta SameSite + state değiştiren isteklerde origin kontrolü
- [ ] CORS: `*` yok; izinli origin listesi
- [ ] Başlıklar: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `frame-ancestors`
- [ ] Rate limit (IP + kullanıcı) hassas uç noktalarda
- [ ] Dosya yükleme: MIME + boyut sınırı, rastgele dosya adı, depolama sunucu dışı (S3/R2), görüntüleri yeniden kodla
- [ ] SSRF: kullanıcı URL'si fetch ediliyorsa izinli host listesi, iç IP engeli
- [ ] Webhook: imza doğrula (ham gövde üzerinden), zaman damgası toleransı, idempotent işleme
- [ ] Gizli anahtarlar env'de, repoda değil; loglarda maskeli
- [ ] Bağımlılık taraması (`npm audit` / `pnpm audit`)

## Katmanlar

```
route/handler  →  service (iş kuralları, yetki)  →  repository/db (sorgular)
```
Handler HTTP'yi bilir, servis bilmez. Servis test edilebilir saf fonksiyonlara yakın olsun.

## Gözlemlenebilirlik

- Yapılandırılmış log (JSON): `level`, `msg`, `requestId`, `userId`, `durationMs`.
- Kişisel veri ve token loglanmaz.
- Sağlık uç noktası `/api/health` (db bağlantısı dahil).
