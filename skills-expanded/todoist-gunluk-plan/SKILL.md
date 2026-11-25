---
description: Todoist'ten bugünün görevlerini çekip önceliklendirilmiş günlük plan oluşturur
---

# Todoist Günlük Plan

## Amaç

Her sabah Todoist'teki görevleri çekerek 1-2-3 kuralına göre önceliklendirilmiş bir günlük plan oluşturur. Manuel planlama yerine otomatik, tutarlı bir sabah ritüeli sağlar.

**Kategori**: Yapay Zeka ve Otomasyon
**MCP Gereksinimi**: Todoist MCP bağlı olmalı

## Süreç

### Adım 1: Bugünün görevlerini çek

Todoist MCP `find-tasks-by-date` aracını kullan:
- `startDate: "today"` ile bugünün ve geciken görevleri al
- Sonuçları önceliğe göre sırala (p1 > p2 > p3 > p4)

### Adım 2: Görevleri sınıflandır

1-2-3 kuralını uygula:

| Kategori | Kural | Todoist Karşılığı |
|----------|-------|-------------------|
| **1 MUTLAKA** | Bugün bitmezse kriz olur | p1 görevler |
| **2 YAPMALI** | Önemli ama bir gün kayabilir | p2 görevler |
| **3 YAPABİLİR** | İyi olur ama zorunlu değil | p3-p4 görevler |

Eğer p1 görev 1'den fazlaysa: kullanıcıya hangisinin gerçek MUTLAKA olduğunu sor.
Eğer toplam görev 6'dan fazlaysa: fazlalarını yarına taşımayı öner.

### Adım 3: Zaman bloklarını oluştur

Her görev için tahmini süre belirle ve günü yapılandır:

```
09:00 - 10:30  [DERIN ÇALIŞMA] MUTLAKA: [görev adı]
10:30 - 10:45  Ara
10:45 - 12:00  [DERIN ÇALIŞMA] YAPMALI 1: [görev adı]
12:00 - 13:00  Öğle arası
13:00 - 14:00  YAPMALI 2: [görev adı]
14:00 - 15:30  [TOPLU İŞ] YAPABİLİR görevler
15:30 - 16:00  E-posta ve mesajlar
16:00 - 16:15  Gün sonu kapanış
```

Kurallar:
- Sabahı (09:00-12:00) derin çalışmaya ayır
- MUTLAKA görevi her zaman ilk blokta
- E-posta ve mesajları öğleden sonraya at
- 6 saatten fazla aktif çalışma planla**ma**

### Adım 4: Geciken görevleri yönet

Geciken görevler varsa:
- 3+ gündür gecikiyorsa → "Bu görevi ya bugün bitir, ya sil, ya devret" uyarısı ver
- Todoist `reschedule-tasks` ile bugüne taşı veya `update-tasks` ile erteleme nedeni ekle

### Adım 5: Planı sun

Kullanıcıya kısa ve temiz bir günlük plan göster. Uzun açıklama yapma — görev listesi + zaman blokları yeterli.

Sonunda: "Plandan memnunsan başlayalım. Değişiklik yapmak istersen söyle."

## Örnek Çıktı

```
📋 Bugünün Planı — Pazartesi 21.03

MUTLAKA (bugün bitmeli):
• Müşteri teklifini gönder — 09:00-10:30

YAPMALI:
• Blog yazısı taslağı yaz — 10:45-12:00
• Landing page A/B test sonuçlarını analiz et — 13:00-14:00

YAPABİLİR:
• LinkedIn paylaşımı hazırla — 14:00-14:30
• E-posta şablonlarını güncelle — 14:30-15:00
• Fatura takibi — 15:00-15:30

⚠️ Geciken: "Logo revizyonu" 4 gündür bekliyor. Bugün bitir veya sil?

Toplam: 5.5 saat aktif çalışma | 1 kritik | 2 önemli | 3 bonus
```
