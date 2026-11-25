---
name: sky-auth
description: >-
  Kimlik doğrulama ve yetkilendirme: Auth.js (NextAuth) / Better Auth / Supabase Auth / Clerk
  seçimi ve kurulumu, oturum stratejileri, OAuth (Google, GitHub, Apple), magic link, e-posta/
  parola, SMS OTP, parola sıfırlama, e-posta doğrulama, 2FA (TOTP), RBAC ve kaynak bazlı yetki,
  çok kiracılı üyelik, oturum iptali, hesap güvenliği ve KVKK rızası. Giriş/kayıt sistemi
  kurarken, rol eklerken veya auth güvenliğini gözden geçirirken kullan.
disable-model-invocation: true
---

# Sky · Auth

`sky-backend-api` genel kuralları (çerez bayrakları, rate limit, hesap sızdırmama) burada
varsayılır; bu skill kurulum ve akışlara odaklanır.

## Hangi çözüm?

| Durum | Öneri | Not |
|---|---|---|
| Next.js, kendi DB'n var, esneklik | **Better Auth** | TS-first, eklentiler (2FA, org, magic link), DB şemasını üretir |
| Next.js, OAuth ağırlıklı, köklü ekosistem | **Auth.js v5** | Adapter'lar (Drizzle/Prisma); kredensiyel akışı zayıf |
| Supabase zaten var | **Supabase Auth** | RLS ile doğal uyum; `@supabase/ssr` ile çerez tabanlı |
| Hızlı ürün, UI hazır, hosted istiyorsun | **Clerk** | Ücretli; kullanıcı verisi dışarıda (KVKK değerlendir) |
| Tam kontrol, küçük yüzey | Kendi oturum tablosu (Lucia tarzı) | Yalnızca kriptoyu kütüphaneye bırak (`@oslojs/*`) |

Kendi parola hash'ini, token'ını, OAuth akışını **yazma**; kütüphaneyi yapılandır.

## Oturum stratejisi

- **DB oturumu** (varsayılan): `sessions` tablosu, çerezde yalnızca rastgele oturum ID'si (≥ 32 byte,
  DB'de hash'li). Anında iptal, cihaz listesi mümkün.
- **JWT oturumu**: sunucusuz/edge kolaylığı; iptal zor → kısa ömür (≤ 15 dk) + refresh rotasyonu.
  Hassas uygulamada DB oturumu tercih.
- Çerez: `HttpOnly; Secure; SameSite=Lax; Path=/`, `__Host-` ön eki mümkünse. Kayan süre
  (her istekte uzat, mutlak üst sınır 30 gün).
- Girişte oturum ID'sini **yenile** (session fixation), parola değişiminde diğer oturumları kapat.

## Akışlar

**E-posta + parola**
- Parola: uzunluk ≥ 8 (öner 12), üst sınır 128; karmaşıklık kuralı yerine sızmış parola kontrolü
  (HIBP k-anonymity) ve yaygın parola listesi. argon2id ile hash.
- Kayıtta e-posta doğrulama token'ı: rastgele, DB'de **hash'li**, tek kullanımlık, 24 saat.
- Giriş hatası tek mesaj: "E-posta veya parola hatalı". Kayıtta "bu e-posta kayıtlı" sızdırma;
  bunun yerine "doğrulama bağlantısı gönderildi" de ve varsa "zaten hesabın var" e-postası at.

**Parola sıfırlama**
1. İstek → her durumda aynı yanıt ("varsa e-posta gönderildi").
2. Token: rastgele 32 byte, DB'de SHA-256 hash, 15–60 dk ömür, tek kullanım.
3. Sıfırlama sonrası tüm oturumları kapat, kullanıcıya bilgi e-postası.

**Magic link / OTP**
- Link: token tek kullanımlık, 10–15 dk; aynı tarayıcıda açılmalı diye zorlamak UX kırar — zorunlu değil.
- SMS OTP (Türkiye'de yaygın): 6 hane, 5 dk, en fazla 5 deneme, ardından kilit; gönderimde
  numara başına ve IP başına rate limit; `autocomplete="one-time-code"`. Maliyet için önce e-posta/magic link düşün.

**OAuth**
- `state` + PKCE kütüphane tarafından; redirect URI'ları tam eşleşme.
- Hesap bağlama: aynı e-posta geldi diye otomatik birleştirme **yapma** (doğrulanmamış e-posta ile
  hesap ele geçirme). Yalnızca sağlayıcı e-postayı doğrulamışsa ve mevcut hesap doğrulanmışsa bağla;
  yoksa giriş yapmış kullanıcıya "hesabı bağla" akışı.
- Apple ile giriş: ad/e-posta yalnızca ilk kez gelir; sakla.

**2FA (TOTP)**
- `otpauth://` QR + manuel anahtar; kurulumda bir kodu doğrulat; 8–10 yedek kod (hash'li).
- Hassas işlemlerde (parola/e-posta değişimi, ödeme ayarı) **yeniden doğrulama** (re-auth) iste.

## Yetkilendirme

**Roller (RBAC)** basit ürün için yeter:
```ts
const permissions = {
  admin:  ["post:read", "post:write", "post:delete", "user:manage"],
  editor: ["post:read", "post:write"],
  viewer: ["post:read"],
} as const satisfies Record<Role, readonly Permission[]>;
export const can = (user: User, p: Permission) => permissions[user.role].includes(p);
```
**Kaynak bazlı** (sahiplik): `post.authorId === user.id || can(user, "post:delete")`.
**Çok kiracılı**: `memberships(user_id, org_id, role)`; her sorgu `org_id` ile; aktif org çerez/URL'de;
üyelik yoksa 404.

Nerede kontrol edilir:
1. **Proxy/middleware**: yalnızca "çerez var mı → /login" kaba yönlendirme. Yetki değil.
2. **Sayfa / layout (Server Component)**: `const user = await requireUser()`; rol uymazsa `redirect` / `notFound`.
   Layout'taki kontrol alt sayfaları korumaz sanma — her sayfa/action kendi kontrolünü yapar.
3. **Server Action / route handler**: kimlik + yetki + sahiplik, her çağrıda.
4. **DB**: Supabase'de RLS; Postgres'te `tenant_id` politikası. UI'da gizleme yetki değildir.

Yardımcılar:
```ts
export const requireUser = cache(async () => {
  const session = await auth();
  if (!session?.user) redirect("/login");
  return session.user;
});
export async function requireRole(role: Role) { const u = await requireUser(); if (u.role !== role) notFound(); return u; }
```
`cache()` ile aynı istekte tekrar sorgulanmaz.

## Supabase özel

- `@supabase/ssr` ile sunucu/istemci istemcileri; oturum çerezde, `proxy.ts`te `getUser()` ile yenile.
- İstemcide **anon key**; `service_role` yalnızca sunucuda, asla `NEXT_PUBLIC_`.
- Her tabloda RLS **açık**; politika `auth.uid()`; `security definer` fonksiyonlarda dikkat.
- `getSession()` istemci çerezine güvenir; sunucuda yetki için `getUser()` (sunucuyla doğrular).

## Hesap güvenliği

- Rate limit: giriş (IP + hesap), kayıt, sıfırlama, OTP. Başarısız girişlerde artan gecikme.
- Bildirim e-postaları: yeni cihazdan giriş, parola/e-posta değişimi, 2FA kapatma.
- E-posta değişimi: eski adrese bilgi + yeni adrese doğrulama; doğrulanmadan değişmez.
- Hesap silme: KVKK gereği mümkün; 7–30 gün bekleme + geri alma, sonra anonimleştir/sil.
- Oturum listesi ve "diğer cihazlardan çık".
- Audit log: giriş/çıkış, rol değişimi, hassas ayarlar (kim, ne zaman, IP).
- Bot: kayıt/OTP'de Turnstile veya hCaptcha; honeypot alanı.

## KVKK / rıza

- Kayıtta aydınlatma metni bağlantısı; ticari ileti için **ayrı**, önceden işaretlenmemiş onay kutusu.
- Rıza kaydı tabloda: ne, ne zaman, hangi metin sürümü, IP.
- Üçüncü taraf auth sağlayıcısı (Clerk vb.) kullanıyorsan veri işleyen sözleşmesini ve yurt dışı aktarım şartını kontrol et.

## Test matrisi

Her korumalı uç nokta için: anonim → 401/redirect; doğru kullanıcı → 200; başka kullanıcı → 403/404;
yanlış rol → 403; süresi dolmuş oturum → 401. Parola sıfırlama token'ı: tekrar kullanım → ret,
süresi dolmuş → ret. OTP: 6. deneme → kilit. Bu testler `sky-testing` yetki matrisine girer.
