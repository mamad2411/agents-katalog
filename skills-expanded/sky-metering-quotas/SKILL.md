---
name: sky-metering-quotas
description: >-
  Plan limitleri, kullanım ölçümü ve kotalar: entitlement (plan → özellik/limit) tablosu,
  sayaç tasarımı (gerçek zamanlı vs toplu), limit uygulama noktaları, %80/%100 uyarıları,
  yumuşak ve sert limit, aşım davranışı (engelle, ücretlendir, yükselt önerisi), kullanıma
  dayalı faturalandırma (Stripe meters), kullanım paneli UI ve "planını yükselt" anları.
  "Free planda 50 randevu limiti", "kota", "kullanım bazlı ücret", "plan limitleri" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Kotalar & Ölçüm

## Entitlement tablosu (tek kaynak)

```ts
export const PLANS = {
  free:  { bookingsPerMonth: 50,   staff: 1,  smsPerMonth: 0,    storageMb: 200,   features: ["online_booking"] },
  pro:   { bookingsPerMonth: 1000, staff: 5,  smsPerMonth: 300,  storageMb: 5000,  features: ["online_booking", "sms", "reports"] },
  team:  { bookingsPerMonth: null, staff: 25, smsPerMonth: 1500, storageMb: 50000, features: ["online_booking", "sms", "reports", "api", "custom_domain"] },
} as const satisfies Record<Plan, Entitlements>;
export const can = (org: Org, f: Feature) => PLANS[org.plan].features.includes(f) || org.addons.includes(f);
```
`null` = sınırsız. Kod içinde `if (org.plan === "pro")` dağınık kontrolleri yok; her şey `can()` / `limit()` üzerinden.
Kurumsal müşteriye özel limitler `org_overrides` tablosu ile.

## Sayaçlar

- **Sayılabilir kaynaklar** (personel, proje): anlık `count(*)` — basit ve doğru.
- **Dönemsel kullanım** (aylık randevu, SMS, AI token): `usage(org_id, metric, period, value)` + atomik artırma:
  `insert … on conflict (org_id, metric, period) do update set value = usage.value + $n returning value`.
- Yüksek hacim (API istekleri): Redis `INCRBY` + periyodik DB'ye boşaltma.
- Dönem: abonelik dönemine hizalı (`current_period_start`), takvim ayı değil.

## Uygulama noktası

```ts
export async function assertWithinLimit(org: Org, metric: Metric, add = 1) {
  const max = PLANS[org.plan][metric];
  if (max === null) return;
  const used = await getUsage(org.id, metric);
  if (used + add > max) throw new LimitError(metric, used, max);   // UI: yükseltme modalı
}
```
- Kontrol **sunucuda**, işlemden önce; sayaç artırımı işlemle aynı transaction'da (yarış durumuna karşı).
- `LimitError` → HTTP 402 / özel hata kodu → istemci yükseltme modalını açar.

## Limit davranışları

| Tür | Davranış | Örnek |
|---|---|---|
| Sert | işlemi engelle | personel sayısı |
| Yumuşak | izin ver, uyar, sonra konuş | depolama %110'a kadar |
| Aşım ücreti | izin ver, fazlayı faturala | SMS paketi aşımı |
| Kısma | yavaşlat | API rate limit |
Müşteri tarafı kritik işlemleri (gelen online randevu) **asla** sert limitle reddetme — müşterinin müşterisini cezalandırma; işletmeye uyarı gönder, kısa tolerans ver.

## Uyarılar (insanların takdir ettiği şeffaflık)

- %80'de e-posta + uygulama içi banner: "Bu ay 40/50 randevu kullandın. Yenilenme: 15 Kasım."
- %100'de: net mesaj + seçenekler ("Pro'ya geç" / "Ek paket al" / "Dönemin bitmesini bekle").
- Uyarılar dönem başına bir kez (tekrar tekrar spam yok).

## Kullanım paneli

Ayarlar → Plan ve kullanım: her metrik için ilerleme çubuğu (yeşil → turuncu → kırmızı), "x/y", yenilenme tarihi,
geçen dönemle karşılaştırma, "Planları karşılaştır" bağlantısı. Kilitli özelliklerde 🔒 + "Pro'da var" tooltip'i;
tıklayınca o özelliği anlatan küçük yükseltme kartı.

## Yükseltme anları (dönüşümün kalbi)

- Limite takılınca, kilitli özelliğe tıklayınca, ekip davetinde koltuk dolunca — bağlamlı modal: ne kazanacak, fiyat, tek tıkla yükselt (Stripe Checkout / kayıtlı kart).
- Yükseltme sonrası anında etki (webhook'u bekleme → iyimser güncelle, webhook doğrulasın) ve kutlama anı.
- Düşürmede: hangi verinin limit dışında kalacağını göster ("3 personel pasif olacak"), veri silme yok.

## Kullanıma dayalı faturalandırma

Stripe Billing Meters: olayları (`sms_sent`, değer) gönder, fatura dönem sonunda hesaplanır. Olay gönderimini kuyruğa al,
idempotency anahtarıyla (bkz. `sky-payments`). Kullanıcıya tahmini fatura göster ("Bu ay tahmini ₺412").
