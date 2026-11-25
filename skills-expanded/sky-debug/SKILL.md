---
name: sky-debug
description: >-
  Web uygulamalarında hata ayıklama yöntemi ve tanı tabloları: yeniden üret → izole et →
  hipotez → doğrula → düzelt → regresyon testi döngüsü; araçlar (DevTools, React DevTools,
  Node inspector, git bisect); hidrasyon hatası, sonsuz render, "use client" sınırı, CORS,
  env undefined, bayat cache, çerez set edilmiyor, build geçmiyor ama dev çalışıyor, bellek
  sızıntısı, yavaş sorgu, kararsız test, Türkçe karakter ve saat dilimi hataları için adım
  adım tanı. "Neden çalışmıyor", "hata alıyorum", "bozuldu", "debug" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Hata Ayıklama

## Yöntem (her seferinde aynı döngü)

1. **Yeniden üret** — kesin adımlar, hangi ortam (dev/prod, tarayıcı, mobil), hangi kullanıcı/veri.
   Yeniden üretilemeyen hatayı "düzelttim" deme; önce log/Sentry'den kanıt topla.
2. **İzole et** — en küçük tekrar: tek bileşen, tek istek, tek sorgu. Yarıya böl: ağ mı, render mı, veri mi?
3. **Hipotez** — "X yüzünden Y oluyor" tek cümle. Birden fazla varsa en ucuz test edilenden başla.
4. **Doğrula** — hipotezi **kanıtla** (log, breakpoint, network sekmesi), tahmini değiştirip "oldu galiba" deme.
5. **Düzelt** — kök nedeni; belirtiyi maskeleyen `try/catch`, `?.` veya `setTimeout` değil.
6. **Regresyon testi** — hatayı yakalayan test yaz, önce kırmızı sonra yeşil.
7. **Raporla** — belirti, kök neden, düzeltme, test; ve "başka nerede aynı kalıp var?" sorusu.

Sakın: aynı değişikliği tekrar deneme, birden fazla şeyi aynı anda değiştirme, konsolda kalan `console.log`.

## Araç kutusu

| Araç | Ne için |
|---|---|
| DevTools **Network** | istek gitti mi, durum kodu, gövde, başlıklar (çerez, CORS), zamanlama; "Preserve log" + "Disable cache" |
| DevTools **Console** | hata yığını; `console.table`, `console.trace`, `copy(obj)`; kaynak haritalı satır |
| DevTools **Elements/Styles** | hesaplanmış CSS, hangi kural kazandı, `:hov` zorlama, layout kayması |
| **React DevTools** | Components (props/state/hooks), Profiler ("neden render oldu") |
| DevTools **Performance** | uzun görevler, layout thrash, INP |
| **Sources** breakpoint | `debugger;` satırı; koşullu breakpoint; XHR breakpoint |
| `NODE_OPTIONS=--inspect` | sunucu tarafı breakpoint (`chrome://inspect`); Next: `NODE_OPTIONS='--inspect' next dev` |
| Next `next build --debug`, `.next/trace` | build sorunları |
| `git bisect` | "hangi commit bozdu" — `git bisect start; bad; good <sha>; run pnpm test` |
| `curl -i` / `httpie` | tarayıcıdan bağımsız API testi (CORS'u dışlar) |
| `EXPLAIN ANALYZE` | yavaş sorgu |
| Sentry breadcrumbs / Replay | prod'da ne oldu (bkz. `sky-observability`) |

## Tanı tabloları

### Hydration mismatch ("Text content does not match", "Hydration failed")
Sebep adayları sırayla: (1) `Date`, `Math.random`, `crypto` render'da; (2) `window`/`localStorage` okuma;
(3) locale/saat dilimi farkı sunucu–istemci (`toLocaleString()` arg'sız); (4) geçersiz HTML iç içe (`<p><div>`, `<a><a>`, `<tr>` dışında `<td>`);
(5) tarayıcı eklentisi DOM'u değiştiriyor (gizli pencerede dene); (6) koşullu render `typeof window !== "undefined"`.
Çözüm: değeri `useEffect`/`useSyncExternalStore` ile istemcide üret; `Intl` ile sabit locale+timeZone; HTML'i düzelt;
yalnızca zaman damgası gibi yerlerde `suppressHydrationWarning`.

### Sonsuz render / "Maximum update depth exceeded"
`setState` render gövdesinde; `useEffect` bağımlılığı her render yeni obje/dizi/fonksiyon (`[]`, `{}`, inline fn);
Zustand/Redux selector'ü yeni obje döndürüyor (`useStore(s => ({a: s.a}))` → `useShallow`); prop olarak `onChange={() => ...}` ile çocuk effect'i.
Tanı: React DevTools Profiler → "why did this render"; effect'e `console.count`.
Çözüm: state'i türet, `useMemo`/`useCallback` ilgili yerde, selector'ü ilkel değere indir, effect'i kaldır (çoğu zaman gereksiz).

### "useState/useEffect only works in a Client Component" / "Functions cannot be passed to Client Components"
Hook içeren dosyaya `"use client"` (yaprağa koy); Server → Client'a fonksiyon/Date/class geçme (string'e çevir, action kullan). Bkz. `sky-nextjs`.

### Sunucu kodu istemciye sızdı (DB/env hatası tarayıcıda, "Module not found: fs")
Bir `"use client"` dosyası sunucu modülünü import ediyor. Zinciri izle (hata yığınındaki import yolu); `import "server-only"` ekle ki build'de yakalansın; veri çekmeyi sunucu bileşenine/action'a taşı.

### CORS hatası
Önce `curl -i` ile isteğin **tarayıcı dışında** çalıştığını doğrula (çalışıyorsa CORS'tur). Preflight (`OPTIONS`) 2xx dönüyor mu? `Access-Control-Allow-Origin` tam origin mi (credentials varken `*` olmaz)? `Allow-Credentials: true` + istemcide `credentials: "include"`? Özel başlıklar `Allow-Headers`ta mı?
Next'te aynı origin'den istek at (route handler) ya da `next.config headers()` ile başlıkları ekle; dev'de `rewrites` proxy en temizi.

### Env `undefined`
İstemcide `NEXT_PUBLIC_`/`VITE_` ön eki var mı? Dev server env değişiminden sonra **yeniden başlatıldı** mı? `.env.local` doğru dizinde mi? Build anında gömüldüğü için Vercel'de env ekledikten sonra **yeniden deploy** edildi mi? `lib/env.ts` doğrulaması varsa hatayı o verir — yoksa ekle.

### Veri bayat / değişiklik görünmüyor
Next: Data Cache (`fetch` cache'li mi?), Router Cache (geri tuşuyla eski sayfa), `revalidateTag/Path` çağrıldı mı, action'dan sonra `router.refresh()`? TanStack Query: `staleTime`, `invalidateQueries` key eşleşiyor mu (`["posts"]` vs `["posts", id]`)? CDN/`Cache-Control` başlığı? Tarayıcı cache'i ("Disable cache" ile dene). Prod ile dev davranışı farklıdır — `next build && next start` ile test et.

### Çerez set edilmiyor / oturum kayboluyor
`Secure` çerez `http://localhost`te set edilmez (localhost istisnası tarayıcıya göre değişir; dev'de `Secure`i kapat). `SameSite=None` için `Secure` şart. `Domain` yanlış (`.example.com` vs `app.example.com`). Cross-site istek → `SameSite=Lax` çerezi göndermez. Server Action/route handler'da `cookies().set` yanıt öncesi çağrılıyor mu? Proxy arkasında `X-Forwarded-Proto` yoksa uygulama HTTP sanıp `Secure` çerezi reddedebilir.

### Build geçmiyor ama dev çalışıyor
Tip hataları (dev tip kontrolü yapmaz): `pnpm typecheck`. Statik sayfa build'de veri çekiyor ve DB/env yok → `dynamic = "force-dynamic"` veya build'de env ver. Edge runtime'da Node modülü. Case-sensitive dosya adı (macOS'ta çalışır, Linux CI'da `Button.tsx` ≠ `button.tsx`). `generateStaticParams` boş/eksik. ESLint hataları build'i kırıyor (`next.config eslint.ignoreDuringBuilds` **geçici**).

### Bellek sızıntısı / sekme ağırlaşıyor
Temizlenmeyen `setInterval`, `addEventListener`, WebSocket/`EventSource`, `ResizeObserver`; effect `return () => cleanup` eksik. Büyük listeyi sanallaştırmadan render. Global cache sınırsız büyüyor (Map). Tanı: DevTools Memory → heap snapshot karşılaştır, "Detached DOM" ara. Sunucuda: `process.memoryUsage()` log, singleton olmayan `PrismaClient` (her istekte yeni bağlantı).

### Yavaş sayfa / istek
Önce ölç (bkz. `sky-perf`): Network'te hangi istek uzun (TTFB mi, indirme mi), Performance'ta uzun görev. Sunucu: `EXPLAIN ANALYZE`, N+1 (döngüde sorgu — ORM log'unu aç), eksik indeks, `count(*)` büyük tablo, serial `await` (paralel `Promise.all` yap), soğuk başlatma (serverless). İstemci: büyük bundle (`ANALYZE=true`), gereksiz re-render (Profiler), görsel boyutu.

### Kararsız test
Gerçek zaman (`setTimeout`, `Date.now`) → fake timers; sıraya bağlı paylaşılan state → her test kendi verisi; `await` eksik (`act` uyarısı); animasyon → reduced-motion; ağ → MSW; `waitForTimeout` → otomatik bekleyen `expect`. Tek başına çalıştır (`--repeat-each 20`) ve sırayı rastgele yap (`--shuffle`) — sıraya bağlıysa ortaya çıkar.

### Türkçe karakter sorunları
Büyük/küçük harf: `toLocaleUpperCase("tr-TR")` (bkz. `sky-i18n`). Arama eşleşmiyor: iki taraf da `tr-TR` lower + `normalize("NFC")`. Sıralama yanlış: `localeCompare(b, "tr")` / DB collation. URL/slug kırık: Türkçe→ASCII dönüştürme. CSV'de Excel bozuk: UTF-8 **BOM**. E-posta/SMS'te `?` karakterleri: encoding header veya sağlayıcı ayarı. Fontta ğ/ş farklı: `latin-ext` alt kümesi. Dosya adlarında Türkçe karakter: depolamaya yüklerken ASCII'ye çevir.

### Tarih/saat 3 saat kaymış
Sunucu UTC, kullanıcı `Europe/Istanbul`. DB'de `timestamptz` kullan (`timestamp` değil), ISO string taşı, gösterimde `Intl.DateTimeFormat(..., { timeZone })`. "Gün başı" hesapları kullanıcı saat diliminde (`date-fns-tz`/Temporal). Yalnızca tarih (doğum günü) için `date` tipi, saat ekleme.

### "Çalışıyordu, bir şey değiştirmedim"
Bağımlılık güncellendi mi (`pnpm-lock.yaml` diff), Node sürümü değişti mi (`.nvmrc`), env değişti mi, üçüncü parti API kırıldı mı (durum sayfası), sertifika/alan adı süresi doldu mu, disk doldu mu, tarih tabanlı bir şey (ay sonu, yaz saati)? `git bisect` ile commit bul.

## Hata raporu biçimi

```
Belirti: … (ne görüldü, nerede, ne zaman, kimde)
Yeniden üretme: 1… 2… 3…
Kök neden: … (dosya:satır; neden böyle oldu)
Düzeltme: … (ne değişti)
Test: … (hangi test yakalıyor)
Aynı kalıp başka yerde: var/yok — …
```

## Kontrol listesi

- [ ] Hata yeniden üretildi (ya da prod kanıtı toplandı)
- [ ] Kök neden kanıtlandı, tahmin edilmedi
- [ ] Düzeltme belirtiyi değil nedeni hedefliyor
- [ ] Regresyon testi var ve önce kırmızıydı
- [ ] Debug kalıntısı (console.log, debugger, geçici kod) temizlendi
- [ ] Aynı kalıp başka yerde arandı
