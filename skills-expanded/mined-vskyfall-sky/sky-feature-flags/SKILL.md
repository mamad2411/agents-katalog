---
name: sky-feature-flags
description: >-
  Özellik bayrakları ve deneyler: PostHog / GrowthBook / Unleash / Vercel Flags / kendi tablo
  seçimi, boolean ve çok varyantlı bayraklar, kademeli açılış (%5 → %100), kullanıcı/org/plan
  hedefleme, sunucuda değerlendirme ve SSR'da titreme olmaması, A/B testi tasarımı (hipotez,
  metrik, örneklem, süre), istatistiksel tuzaklar, kill switch, bayrak borcu temizliği ve beta
  programı. "Önce birkaç kullanıcıda deneyelim", "A/B testi", "feature flag", "beta" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Özellik Bayrakları & Deneyler

## Neden?

- **Deploy ≠ yayın**: kodu kapalı bayrakla canlıya al, hazır olunca aç — kriz anında kapat (kill switch).
- Kademeli açılış: önce ekip → %5 → %25 → %100, her adımda hata/metrik izle.
- Beta programı: "Yeni özellikleri önce dene" diyen kullanıcılara erken erişim (insanlar ayrıcalıklı hissetmeyi sever).
- A/B testi: iki versiyondan hangisi daha iyi, veriyle karar.

## Araç

| Durum | Seçim |
|---|---|
| Analitikle birlikte, deney istatistiği hazır | **PostHog** |
| Açık kaynak, self-host, güçlü deney motoru | **GrowthBook** |
| Next.js + Vercel, Edge'de değerlendirme | **Vercel Flags SDK** (sağlayıcıyla) |
| Birkaç basit bayrak | `feature_flags(key, enabled, rules jsonb)` tablosu + cache |

## Sunucuda değerlendir (titreme yok)

```ts
// flags.ts (Vercel Flags SDK kalıbı)
export const newBookingFlow = flag<boolean>({
  key: "new-booking-flow",
  decide: async ({ entities }) => posthog.isFeatureEnabled("new-booking-flow", entities.user.id, { groups: { org: entities.org.id } }),
});
// page.tsx (Server Component)
const enabled = await newBookingFlow();
return enabled ? <NewFlow /> : <OldFlow />;
```
İstemci tarafı değerlendirme ilk render'da eski sonra yeni arayüzü gösterir ("titreme"). Sunucuda karar ver,
istemciye bootstrap değeri geç.

## Hedefleme

- Kullanıcı ID'sine göre **kararlı** atama (hash) — aynı kişi her ziyarette aynı varyantı görür.
- Org bazlı (B2B'de bütün ekip aynı deneyimi görsün), plan bazlı (Pro'ya özel), ülke/dil, iç kullanıcılar (`@sirket.com`).
- Kişisel veriyi bayrak servisine gereksiz gönderme.

## A/B testi tasarımı

1. **Hipotez**: "Saat seçimini düğme ızgarası yapmak randevu tamamlama oranını artırır."
2. **Birincil metrik** tek olsun (tamamlama oranı); koruyucu metrikler (iptal oranı, hata).
3. **Örneklem büyüklüğü** önceden hesapla (temel oran, beklenen fark, %80 güç) — küçük trafikte küçük farklar ölçülemez.
4. **Süre**: en az 1–2 tam hafta (hafta içi/sonu döngüsü), örnekleme ulaşmadan bakıp durdurma (peeking) yok.
5. Sonuç: güven aralığıyla raporla; anlamlı değilse "fark yok" da bir sonuçtur.
Tuzaklar: aynı anda çok deney çakışması, yeni-lik etkisi, segmentlere bölüp tesadüfi "kazanan" bulma, bot trafiği.

## Kademeli açılış kontrol listesi

- [ ] Bayrak kapalıyken eski yol tamamen çalışıyor (test)
- [ ] Hata oranı ve performans bayrak varyantına göre etiketli (Sentry tag `flag:new-booking-flow`)
- [ ] Geri alma = bayrağı kapatmak (deploy yok)
- [ ] Her adım için izleme süresi ve devam ölçütü yazılı

## Bayrak borcu

- Her bayrağın sahibi ve **son kullanma tarihi**; %100'e çıkınca 2 hafta içinde kod ve bayrak silinir.
- Aylık "bayrak temizliği": 30 günden uzun %100/%0 olanları listele.
- İsimlendirme: `kebab-case`, amaç belli (`new-booking-flow`, `kill-sms-sending`), tür öneki isteğe bağlı (`exp-`, `ops-`, `beta-`).

## Beta programı UI'ı

Ayarlarda "Erken erişim" sayfası: deneysel özellik kartları (açıklama, ekran görüntüsü, aç/kapa anahtarı,
"Geri bildirim ver" bağlantısı). Açılan özellikte küçük "Beta" rozeti. Kullanıcılar bu sayfayı çok sever.
