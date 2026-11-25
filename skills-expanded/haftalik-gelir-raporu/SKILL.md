---
description: Todoist tamamlanan görevleri ve takvim verilerini birleştirerek haftalık verimlilik ve iş raporu oluşturur
---

# Haftalık Gelir ve Verimlilik Raporu

## Amaç

Haftalık değerlendirmeyi otomatikleştir. Todoist'ten tamamlanan görevleri, takvimden geçen haftanın etkinliklerini çekerek solopreneur'un haftalık performans raporunu oluşturur. "Bu hafta ne yaptım?" sorusunun somut cevabı.

**Kategori**: Yapay Zeka ve Otomasyon
**MCP Gereksinimi**: Todoist MCP + Google Calendar MCP bağlı olmalı

## Süreç

### Adım 1: Tamamlanan görevleri çek

Todoist MCP `find-completed-tasks` aracını kullan:
- Son 7 günün tamamlanan görevlerini al
- Projelere göre grupla

### Adım 2: Takvim etkinliklerini çek

Google Calendar MCP `gcal_list_events` ile:
- Geçen haftanın tüm etkinliklerini al
- Toplantı sayısını ve toplam süresini hesapla

### Adım 3: Verimlilik metrikleri hesapla

| Metrik | Hesaplama | Sağlıklı Aralık |
|--------|-----------|-----------------|
| Tamamlanan görev | Todoist'ten toplam | 15-25/hafta |
| Toplantı saati | Takvimden toplam | <8 saat/hafta |
| Derin çalışma oranı | (40 saat - toplantı) / 40 | >%70 |
| Görev tamamlama oranı | Tamamlanan / (Tamamlanan + Geciken) | >%80 |

### Adım 4: Kategorize et

Tamamlanan görevleri şu kategorilere ayır (Todoist proje adlarına göre):
- **İnşa**: Ürün geliştirme, kod, tasarım
- **Pazarlama**: İçerik, SEO, sosyal medya
- **Satış**: Müşteri iletişimi, teklifler
- **Yönetim**: Admin, faturalar, planlama

### Adım 5: Raporu oluştur

Kullanıcıya kısa, okunabilir bir haftalık rapor sun.

## Örnek Çıktı

```
📊 Haftalık Rapor — 14-20 Mart

ÖZET
  Tamamlanan: 22 görev ✅
  Geciken: 3 görev ⚠️
  Toplantılar: 4 toplantı (5.5 saat)
  Derin çalışma oranı: %78 ✅

KATEGORİ DAĞILIMI
  İnşa:      █████████░ 9 görev (%41)
  Pazarlama:  ██████░░░░ 6 görev (%27)
  Satış:      ████░░░░░░ 4 görev (%18)
  Yönetim:    ███░░░░░░░ 3 görev (%14)

ÖNE ÇIKANLAR
  ✅ Yeni landing page yayınlandı
  ✅ 3 blog yazısı tamamlandı
  ✅ 2 müşteri teklifi gönderildi

GECİKENLER
  ⚠️ Logo revizyonu — 5 gün gecikmeli
  ⚠️ E-posta otomasyon kurulumu — 3 gün gecikmeli
  ⚠️ Fatura takibi — 2 gün gecikmeli

KARŞILAŞTIRMA (geçen hafta → bu hafta)
  Görev: 18 → 22 (+%22) ↑
  Toplantı: 7 saat → 5.5 saat ↓ (iyi!)
  Derin çalışma: %65 → %78 ↑

GELECEKHAFTANINÖNCELİĞİ
  Geciken 3 görevi temizle + yeni müşteri adaylarına ulaş
```
