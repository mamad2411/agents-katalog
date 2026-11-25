---
name: sky-states-library
description: >-
  Arayüz durumları kütüphanesi: boş durum (ilk kullanım, filtre sonucu boş, temizlenmiş),
  yükleniyor (iskelet, spinner, ilerleme, iyimser), hata (alan, bileşen, sayfa, ağ, yetki,
  404/500), başarı (toast, satır içi, tam ekran), çevrimdışı, bakım, kilitli özellik ve kısmi
  veri durumları için hazır bileşen kalıpları, illüstrasyon stili ve metinleri. "Boş ekran
  çirkin", "yükleniyor durumu", "hata sayfası", "404 tasarla" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Durumlar Kütüphanesi

Her veri gösteren bileşenin 4 hali vardır: **yükleniyor, boş, hata, dolu**. Çoğu tasarım yalnızca "dolu"yu
düşünür; kullanıcının ilk gördüğü ise genelde diğer üçüdür.

## Bileşen seti (`components/ui/states/`)

```tsx
<EmptyState icon={<CalendarPlus />} title="Henüz randevun yok"
  description="Online rezervasyon bağlantını paylaştığında randevular burada görünür."
  action={<Button>Bağlantıyı kopyala</Button>} secondary={<Link href="/yardim/randevu">Nasıl çalışır?</Link>} />
<ErrorState title="Randevular yüklenemedi" description="Bağlantında bir sorun olabilir." onRetry={refetch} />
<Skeleton variant="table" rows={6} />   <Skeleton variant="card" />   <Skeleton variant="text" lines={3} />
<OfflineBanner />   <LockedFeature plan="Pro" feature="Raporlar" />
```
Tek tip API, tek görsel dil — her ekranda yeniden tasarlanmaz.

## Boş durum türleri

| Tür | İçerik |
|---|---|
| İlk kullanım | değer açıklaması + birincil eylem + (ops.) örnek veri / video |
| Filtre/arama sonucu boş | "Eşleşen kayıt yok" + "Filtreleri temizle" + arama önerisi |
| Kullanıcı temizledi | olumlu ton: "Hepsi tamam! 🎉 Bekleyen görev yok." |
| Yetki yok | neden + kimden istenir |
| Henüz veri oluşmadı (rapor) | "Veriler ilk randevudan sonra burada görünecek" + tahmini görünüm (soluk örnek grafik) |

## Yükleniyor seçimi

| Süre / durum | Gösterim |
|---|---|
| < 300ms | hiçbir şey (yanıp sönme olmasın) |
| İçerik şekli biliniyor | **iskelet** (aynı boyut, CLS 0) |
| Buton eylemi | buton içinde spinner, genişlik sabit |
| Uzun işlem, ilerleme biliniyor | ilerleme çubuğu + yüzde + kalan süre |
| Uzun işlem, bilinmiyor | adım metinleri ("Dosya okunuyor… Doğrulanıyor…") |
| Geri alınabilir eylem | **iyimser** — hemen göster, arka planda kaydet |

## Hata katmanları

- **Alan**: input altında, ne + nasıl düzelir.
- **Bileşen**: kart/widget içinde mesaj + "Tekrar dene"; sayfanın kalanı çalışır (hata sınırı).
- **Sayfa**: `error.tsx` — sade, marka uyumlu, "Tekrar dene" + "Ana sayfa" + destek bağlantısı + hata kodu (destek için `requestId`).
- **Ağ/çevrimdışı**: üstte ince bant, otomatik yeniden bağlanma, kuyruktaki işlemler.
- **404**: arama + popüler bağlantılar + hafif espri (marka izin veriyorsa); **500**: dürüst, özür, durum sayfası.
- **Bakım**: tahmini bitiş saati (saat dilimiyle), durum sayfası bağlantısı.

## Başarı

- Küçük eylem → toast ("Kaydedildi") veya satır içi ✓ (1.5 sn).
- Önemli eylem (ödeme, yayınlama) → tam ekran/kart başarı durumu + sonraki adım ("Faturayı indir", "Paylaş").
- İlk kez başarılar → kutlama (bkz. `sky-onboarding`).

## İllüstrasyon stili

- Tek stil seti (çizgi ikon ölçeğinde büyük ikon, ya da tutarlı illüstrasyon ailesi — unDraw rengi markaya ayarlanabilir, ya da özel SVG).
- Boyut ölçülü (≤ 160px), dikkat dağıtmasın; koyu temada da çalışsın (`currentColor` ve token renkleri).
- Hata durumlarında üzücü/korkutucu görsel yok.

## Kontrol listesi (her ekran için)

- [ ] Yükleniyor: iskelet aynı düzende
- [ ] Boş: ilk kullanım ve filtre-boş ayrı
- [ ] Hata: tekrar dene var, veri kaybı yok
- [ ] Kısmi veri: bazı widget'lar hatalıyken diğerleri çalışıyor
- [ ] Çevrimdışı davranış tanımlı
- [ ] Metinler `sky-ux-writing` kurallarına uygun
